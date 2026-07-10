# Lab 2: RAG with Memory (Chapter 2)

**Time:** ~35 minutes. **Requires:** Lab 1 complete (index populated),
`OS_URL` and `MODEL_ID` exported (`LLM_ID` too if you are on the LLM
path from Lab 0 Step 6).

**The story:** your Lab 1 system answers single questions well. Real
support conversations are threads, not turns. In this lab you watch
your own system fail on the second turn of a conversation, then build
the memory layer that fixes it: a conversation index with real tenant
isolation, skip logic, query rewriting, and the two query enhancements
from lesson 2.3.

---

## Step 1: Break your own system

**What you're doing:** replaying the exact two-turn failure from lesson
2.1. Turn one of a real support thread:

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 3, "_source": ["title"],
  "query": { "match": { "text": "how do I fix ERR-2209" } }
}' | python3 -m json.tool
```

**Expected result:** confident, on-topic hits about ERR-2209, the
connector handshake failure.

Now embed the customer's follow-up exactly as they typed it:

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 3, "_source": ["title"],
  "query": { "neural": { "embedding": {
    "query_text": "what about on version 4.9?",
    "model_id": "'$MODEL_ID'", "k": 50 } } }
}' | python3 -m json.tool
```

**Expected result:** junk. There is no error code, no connector, no
topic in those five words, and the results show it: unrelated titles,
similar middling scores.

**Why:** a stateless pipeline embeds exactly the words it is given.
"What about on version 4.9" is a meaningless vector on its own. Every
follow-up that leans on pronouns, ellipsis, corrections, or
comparatives fails the same way.

**Checkpoint 2.1:** the turn-two results contain nothing about ERR-2209
or connectors. Write down the top result title; you will compare it in
Step 5.

## Step 2: Give conversations a home

**What you're doing:** creating the conversation index from lesson 2.1,
one document per message, with a boring, exact mapping.

```bash
curl -s -X PUT "$OS_URL/support-conversations" -H 'Content-Type: application/json' -d '{
  "mappings": { "properties": {
    "conversation_id":     { "type": "keyword" },
    "turn":                { "type": "integer" },
    "role":                { "type": "keyword" },
    "text":                { "type": "text" },
    "created_at":          { "type": "date" },
    "tenant_id":           { "type": "keyword" },
    "retrieved_chunk_ids": { "type": "keyword" }
  } }
}'
```

**Why the mapping looks like this:** you will fetch by conversation and
recency far more often than you will search this semantically, so it is
keyword fields and a date, no vectors. And note
`retrieved_chunk_ids`: when the tool answers a turn, it writes *what it
retrieved* onto that turn's document. Those chunk IDs are breadcrumbs
back to the topic, and they cost nothing to keep.

**Expected result:** `{"acknowledged":true,...,"index":"support-conversations"}`

Now write the two turns of our thread (note the breadcrumbs on turn 1):

```bash
curl -s -X POST "$OS_URL/support-conversations/_doc?refresh=true" -H 'Content-Type: application/json' -d '{
  "conversation_id":"CONV-LAB2","turn":1,"role":"assistant",
  "text":"ERR-2209 is a TLS handshake failure. Enable TLS 1.3 in connector advanced settings.",
  "created_at":"2026-07-05T10:00:00Z","tenant_id":"northwind-logistics",
  "retrieved_chunk_ids":["KI-0004#0.0","GUIDE-002#3.0"]
}'
curl -s -X POST "$OS_URL/support-conversations/_doc?refresh=true" -H 'Content-Type: application/json' -d '{
  "conversation_id":"CONV-LAB2","turn":2,"role":"user",
  "text":"what about on version 4.9?",
  "created_at":"2026-07-05T10:01:00Z","tenant_id":"northwind-logistics"
}'
```

**Expected result:** two `{"_index":"support-conversations",...,"result":"created"}` responses.

## Step 3: Prove tenant isolation

**What you're doing:** running the same conversation read twice, once
as the right tenant, once as the wrong one.

```bash
curl -s "$OS_URL/support-conversations/_search" -H 'Content-Type: application/json' \
  -d '{"query":{"bool":{"filter":[{"term":{"conversation_id":"CONV-LAB2"}},{"term":{"tenant_id":"northwind-logistics"}}]}}}' \
  | python3 -c "import sys,json; print('hits:', json.load(sys.stdin)['hits']['total']['value'])"
```

**Expected result:** `hits: 2`

```bash
curl -s "$OS_URL/support-conversations/_search" -H 'Content-Type: application/json' \
  -d '{"query":{"bool":{"filter":[{"term":{"conversation_id":"CONV-LAB2"}},{"term":{"tenant_id":"bluepeak-financial"}}]}}}' \
  | python3 -c "import sys,json; print('hits:', json.load(sys.stdin)['hits']['total']['value'])"
```

**Expected result:** `hits: 0`

**Why:** Northwind's conversation history must never leak into a
Bluepeak session. `tenant_id` rides as a filter on every single read of
this index, the same hard pre-filter discipline from lesson 1.2, now
applied to memory.

**Checkpoint 2.2:** 2 then 0. If the second query returns anything but
0, your filter is wrong; treat that as a security bug, not a quality
bug, exactly as lesson 2.1 said.

## Step 4: Skip logic (decide WHETHER to rewrite, for free)

**What you're doing:** running lesson 2.1's cheap gate that decides
which turns need the rewriter at all. No cluster involved; this runs
locally, which is the point: it is free.

```bash
python3 - << 'EOF'
import re
CONTEXT_DEPENDENT = re.compile(
    r"\b(it|that|this one|those|them|same|the (first|second|last) (one|option))\b"
    r"|^(what about|and on|how about|also)\b", re.IGNORECASE)
def needs_rewrite(q):
    # four or fewer words is almost never a standalone question
    return len(q.split()) <= 4 or bool(CONTEXT_DEPENDENT.search(q))
for q in ["what about on version 4.9?",
          "how do I fix ERR-2209",
          "does it work with SSO?",
          "how do I configure report bursting for 200 users"]:
    print(f"{needs_rewrite(q)!s:5}  {q}")
EOF
```

**Expected result:**

```
True   what about on version 4.9?
False  how do I fix ERR-2209
True   does it work with SSO?
False  how do I configure report bursting for 200 users
```

**Why:** rewriting costs an LLM call on every turn it runs, and most
turns do not need it. A regex catches pronouns, fragments, and
references; in practice the rewriter fires on roughly a third of
turns, meaning two thirds of your traffic skips an entire LLM call. At
500 tickets a day, this regex is a budget line. Lesson 2.1's principle,
worth tattooing somewhere visible: spend intelligence only where the
query needs it.

**Checkpoint 2.3:** True, False, True, False, in that order.

## Step 5: The rewrite

**What you're doing:** running lesson 2.1's rewriter for real: the LLM
reads the recent history plus turn 1's breadcrumbs and produces a
standalone query.

```bash
curl -s -X POST "$OS_URL/_plugins/_ml/models/$LLM_ID/_predict" \
  -H 'Content-Type: application/json' -d '{
  "parameters": { "prompt": "Rewrite the customer'"'"'s follow-up as one standalone search query that needs no conversation context. Conversation so far: [assistant, answered from chunks KI-0004 (known issue ERR-2209 connector handshake failed) and GUIDE-002 (Snowflake integration guide)]: ERR-2209 is a TLS handshake failure. Enable TLS 1.3 in connector advanced settings. [customer follow-up]: what about on version 4.9? Reply with ONLY the rewritten query text, nothing else." }
}' | python3 scripts/llm_text.py
```

**Sample output from our validated run** (yours will differ in wording;
per Lab 0's variance caveat, what must hold is that the error code, the
Snowflake/connector topic, and the version all reappear):

```
How to enable TLS 1.3 in connector advanced settings for version 4.9 to resolve ERR-2209 TLS handshake failure?
```

Now paste YOUR rewritten query into the retrieval it repairs (replace
the `query_text` with what your model produced):

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 3, "_source": ["title"],
  "query": { "neural": { "embedding": {
    "query_text": "<PASTE YOUR REWRITTEN QUERY HERE>",
    "model_id": "'$MODEL_ID'", "k": 50 } } }
}' | python3 -m json.tool
```

> **No-LLM alternative:** skip the predict call and use the rewrite the
> course validated by hand:
> `does the ERR-2209 TLS workaround apply to the Snowflake connector on version 4.9`

**Expected result:** ERR-2209 and Snowflake connector content back on
top, night-and-day against your Step 1 turn-two junk.

**Why one rewrite repairs three things at once:** the error code is
back, so the BM25 leg has something to bite. The topic is back, so the
vector leg lands in the right neighborhood. And a version number
appeared, which a 1.2-style pre-filter can enforce as a hard
constraint.

**Checkpoint 2.4:** compare with the title you wrote down in
Checkpoint 2.1. Same customer intent, completely different retrieval.

## Step 6: HyDE (lesson 2.3)

**What you're doing:** rescuing a vague query. First feel it fail:

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 3, "_source": ["title"],
  "query": { "neural": { "embedding": {
    "query_text": "dashboards are acting weird lately",
    "model_id": "'$MODEL_ID'", "k": 50 } } }
}' | python3 -m json.tool
```

**Expected result:** ticket chunks: "Dashboard takes forever to load,"
three different customers' versions of it. Interesting, but look at
what you found: *other people with the same problem*, not the answer.
Vague customer phrasing lands in the neighborhood of other vague
customer phrasing.

Now HyDE's trick: have the LLM draft the *hypothetical documentation
passage* that would answer this question:

```bash
curl -s -X POST "$OS_URL/_plugins/_ml/models/$LLM_ID/_predict" \
  -H 'Content-Type: application/json' -d '{
  "parameters": { "prompt": "A customer of a BI platform says: dashboards are acting weird lately. Write the short documentation paragraph (2-3 sentences, technical documentation voice) that would most likely answer this complaint, covering the most probable cause. Reply with ONLY the paragraph." }
}' | python3 scripts/llm_text.py
```

**Sample output from our validated run** (yours will differ; what
matters is that it reads like documentation, in documentation
vocabulary):

```
Recent updates to the platform's data processing engine may have introduced temporary
inconsistencies in dashboard rendering. Users experiencing unusual behavior are advised
to clear their browser cache and ensure they are using the latest version of the platform
to mitigate potential display issues. If problems persist, please contact support for
further assistance.
```

Search with YOUR hypothetical passage instead of the customer's
sentence (paste it as the `query_text`):

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 3, "_source": ["title"],
  "query": { "neural": { "embedding": {
    "query_text": "<PASTE YOUR HYPOTHETICAL PASSAGE HERE>",
    "model_id": "'$MODEL_ID'", "k": 50 } } }
}' | python3 -m json.tool
```

> **No-LLM alternative:** use the validated hypothetical passage:
> `Dashboard render performance troubleshooting. If dashboards load slowly or time out, check widget query duration against the render budget, review auto refresh intervals, and enable result caching on the underlying dataset.`

**Expected result:** the documentation itself. With the validated
passage the top 3 is `How dashboard rendering works`,
`Troubleshooting dashboard rendering`, and
`Dashboard Rendering settings reference`; with your own model's passage
the exact titles may vary, but they should be dashboard
rendering/performance docs pages, not tickets.

**Why it works:** the hypothetical passage is fiction, but it is
fiction written in the vocabulary of the real docs, so in vector space
it lands inside the docs cluster instead of among fellow complaints.
You retrieve with the hypothetical, then generate from the real chunks
you found; the fake document never reaches the customer.

**Checkpoint 2.5:** the vague query's top 3 is tickets (the problem,
restated); the HyDE-style query's top 3 is docs (the answer).

## Step 7: Decomposition with _msearch (lesson 2.3)

**What you're doing:** answering a compound question ("does Salesforce
support OAuth, and how do I rotate the credentials?") as two standalone
sub-queries in one round trip.

```bash
curl -s "$OS_URL/support-docs/_msearch" -H 'Content-Type: application/x-ndjson' --data-binary $'{}\n{"size":3,"_source":["title"],"query":{"match":{"text":"Salesforce connector OAuth support"}}}\n{}\n{"size":3,"_source":["title"],"query":{"match":{"text":"credential rotation refresh token expired ERR-2231"}}}\n' \
  | python3 -c "
import sys, json
for i, r in enumerate(json.load(sys.stdin)['responses'], 1):
    print(f'--- sub-query {i} ---')
    for h in r['hits']['hits']:
        print(' ', h['_source']['title'][:70])"
```

**Expected result:** two labeled result blocks:

```
--- sub-query 1 ---
  ERR-2231 when connecting to Salesforce
  Salesforce integration guide
  Salesforce integration guide
--- sub-query 2 ---
  Connector Credential Rotation overview
  Connector Credential Rotation overview
  Troubleshooting connector credential rotation
```

**Why:** embed a compound question whole and you get an average of two
topics, a vector pointing between the OAuth section and the rotation
section, mediocre for both. `_msearch` executes both standalone
sub-queries in a single network round trip; merge and deduplicate on
chunk ID, and the model gets complete evidence for both halves. Lesson
2.3's heuristic: an "and," an "or," or a "versus" in a question means
consider splitting.

**Checkpoint 2.6:** the response contains exactly two `responses`
objects, each on its own topic.

## Step 8: Retention with ISM (lesson 2.2)

**What you're doing:** giving conversation data an expiry date, inside
the cluster, with an Index State Management policy.

```bash
curl -s -X PUT "$OS_URL/_plugins/_ism/policies/support-conversation-retention" \
  -H 'Content-Type: application/json' -d '{
  "policy": {
    "description": "Delete conversation indexes past the 90 day retention window",
    "default_state": "active",
    "states": [
      { "name": "active",
        "actions": [],
        "transitions": [
          { "state_name": "delete", "conditions": { "min_index_age": "90d" } } ] },
      { "name": "delete",
        "actions": [ { "delete": {} } ],
        "transitions": [] }
    ]
  }
}'
```

**Expected result:** a JSON echo of the policy with an `_id` of
`support-conversation-retention`.

**Why:** conversations are user data with a compliance clock. ISM
handles rollover and deletion inside the cluster, no external cron. And
the terminology note from lesson 2.2, because your fingers will betray
you if you come from Elasticsearch: it is ISM (Index State Management)
in OpenSearch, not ILM. Same job, different name, and your automation
cares about the difference.

**Checkpoint 2.7:** `GET $OS_URL/_plugins/_ism/policies/support-conversation-retention`
returns the policy. (In production you would attach it to the
conversation indexes with an ISM template; for the lab, creating and
reading it is enough.)

## Step 9 (optional): The platform's memory, ML Commons Memory API

**What you're doing:** creating the same kind of conversation storage
using OpenSearch's native Memory API instead of your own index.

```bash
curl -s -X POST "$OS_URL/_plugins/_ml/memory" -H 'Content-Type: application/json' \
  -d '{"name":"CONV-LAB2 native"}'
```

**Expected result:** `{"memory_id":"<some id>"}`. Add a message to it
(paste your `memory_id`):

```bash
curl -s -X POST "$OS_URL/_plugins/_ml/memory/<MEMORY_ID>/messages" \
  -H 'Content-Type: application/json' -d '{
  "input":"what about on version 4.9?",
  "response":"On 4.9 the TLS 1.3 setting is not available yet; use the known-issue workaround.",
  "origin":"support-tool-lab2"
}'
```

**Expected result:** `{"message_id":"<some id>"}`. Read the thread back:

```bash
curl -s "$OS_URL/_plugins/_ml/memory/<MEMORY_ID>/messages" | python3 -m json.tool
```

**Why you built it by hand first:** now you can evaluate this managed
abstraction against a design you actually understand: how rewriting
sees history, how summarization compresses, what enters the prompt, how
tenant isolation is enforced. Lesson 2.2's graduation criterion: adopt
the native API the day its defaults match the design you now know how
to specify.

---

**What you built:** conversation storage with real tenant isolation,
free skip logic, a rewrite you performed by hand, HyDE, `_msearch`
decomposition, and a retention policy.
**What you should be able to explain:** why turn two failed, what one
rewrite repairs, when NOT to spend the rewrite call, and why memory
gets the same access discipline as the document index. Lab 3 asks a
harder question: what happens when retrieval succeeds and is still
wrong?
