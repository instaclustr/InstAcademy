# Lab 4: Agentic RAG (Chapter 4)

**Time:** ~45 minutes (about 5 waiting on the ticket re-embed).
**Requires:** Labs 1 and 3 complete, `OS_URL` and `MODEL_ID` exported
(`LLM_ID` too if you are on the LLM path).

**The story:** one pipeline, however good, treats every query the same.
In this lab you split the corpus into four purpose-built indexes behind
aliases, give each the retrieval it deserves, walk a ReAct trace by
hand, build the routing cache and the semantic answer cache, and put
the guardrails in place that make agency shippable.

---

## Step 1: Create the four indexes

**What you're doing:** creating one index per asset family, each with
its own settings, exactly the seams lesson 4.2 described. Three get
vectors. One deliberately does not.

Set a reusable mapping fragment first (paste as one block):

```bash
MAPCOMMON='"text":{"type":"text"},"parent_text":{"type":"text","index":false},"chunk_id":{"type":"keyword"},"parent_id":{"type":"keyword"},"source_id":{"type":"keyword"},"doc_type":{"type":"keyword"},"title":{"type":"text","fields":{"raw":{"type":"keyword"}}},"section_heading":{"type":"text"},"section_path":{"type":"keyword"},"product_area":{"type":"keyword"},"product_version":{"type":"keyword"},"acl":{"type":"keyword"},"updated_at":{"type":"date"},"related_error_codes":{"type":"keyword"},"embedding_model_id":{"type":"keyword"},"embedding_model_version":{"type":"keyword"}'
EMB='"embedding":{"type":"knn_vector","dimension":384,"method":{"name":"hnsw","engine":"faiss","space_type":"innerproduct","parameters":{"m":16,"ef_construction":128}}}'
```

Docs + guides (hybrid with parent-child, as designed in lesson 1.3):

```bash
curl -s -X PUT "$OS_URL/support-docs-v2" -H 'Content-Type: application/json' -d '{
  "settings": { "index": { "knn": true, "number_of_shards": 1, "number_of_replicas": 1 } },
  "mappings": { "properties": { '"$MAPCOMMON"','"$EMB"' } }
}'
```

Tickets (vectors, because customers describe symptoms in customer
words):

```bash
curl -s -X PUT "$OS_URL/support-tickets-v1" -H 'Content-Type: application/json' -d '{
  "settings": { "index": { "knn": true, "number_of_shards": 1, "number_of_replicas": 1 } },
  "mappings": { "properties": { '"$MAPCOMMON"','"$EMB"' } }
}'
```

API reference (vectors plus exact-match fields for endpoint paths):

```bash
curl -s -X PUT "$OS_URL/support-api-v1" -H 'Content-Type: application/json' -d '{
  "settings": { "index": { "knn": true, "number_of_shards": 1, "number_of_replicas": 1 } },
  "mappings": { "properties": { '"$MAPCOMMON"','"$EMB"',"path":{"type":"keyword"},"method":{"type":"keyword"} } }
}'
```

Known issues, and read this one twice: **no `knn` setting, no embedding
field**:

```bash
curl -s -X PUT "$OS_URL/support-issues-v1" -H 'Content-Type: application/json' -d '{
  "settings": { "index": { "number_of_shards": 1, "number_of_replicas": 1 } },
  "mappings": { "properties": { '"$MAPCOMMON"' } }
}'
```

**Why issues gets no vectors:** 15 exact records with literal error
codes. Error codes are lexical gifts; vector overhead on this index
buys nothing. This is lesson 4.2's argument in one mapping: the
document type drives the retrieval configuration.

**Expected result:** four `{"acknowledged":true,...}` responses.

## Step 2: Route the chunks

**What you're doing:** loading each asset family into its index. Same
loader discipline as Lab 1 (batches, backpressure, resumable), one
family at a time:

```bash
python3 scripts/split_chunks.py --family docs    --model-id $MODEL_ID --chunks corpus/example-corp-corpus-v2.1.0/chunks.jsonl
python3 scripts/split_chunks.py --family tickets --model-id $MODEL_ID --chunks corpus/example-corp-corpus-v2.1.0/chunks.jsonl
python3 scripts/split_chunks.py --family issues  --model-id $MODEL_ID --chunks corpus/example-corp-corpus-v2.1.0/chunks.jsonl
python3 scripts/split_chunks.py --family api     --model-id $MODEL_ID --chunks corpus/example-corp-corpus-v2.1.0/chunks.jsonl
```

The docs and tickets families re-embed (a few minutes each); issues
loads instantly with no embedding pipeline at all.

Now put every tool behind an alias, including flipping `support-docs`
from the everything-index to the docs-only index, the exact
zero-downtime move lesson 1.4 taught:

```bash
curl -s -X POST "$OS_URL/_aliases" -H 'Content-Type: application/json' -d '{
  "actions": [
    { "remove": { "index": "support-docs-v1", "alias": "support-docs" } },
    { "add":    { "index": "support-docs-v2", "alias": "support-docs" } },
    { "add":    { "index": "support-tickets-v1", "alias": "support-tickets" } },
    { "add":    { "index": "support-issues-v1",  "alias": "support-issues" } },
    { "add":    { "index": "support-api-v1",     "alias": "support-api" } }
  ]
}'
```

**Why aliases and never physical names:** when a model change forces a
reindex, the alias flips from v1 to v2 and every agent tool keeps
working mid-conversation. No deploy, no broken tools. (One local
consequence: `support-docs` now means docs+guides only. Lab 3's
correction loop script searches the combined index; if you re-run it
after this lab, it still works because `support-docs-v1` still exists
and the loop filters by doc_type either way.)

**Checkpoint 4.1:** four aliases resolve and the counts match:

```bash
curl -s "$OS_URL/_cat/aliases/support-*?h=alias,index" | sort
curl -s "$OS_URL/_cat/indices/support-docs-v2,support-tickets-v1,support-issues-v1,support-api-v1?h=index,docs.count"
```

Expected: `support-docs -> support-docs-v2` (5,068), tickets 3,816,
issues 15, api 56. (Run a `_refresh` on the indexes if counts look
behind; bulk loads become countable on refresh.)

## Step 3: Feel per-index strategy

**What you're doing:** asking two different question shapes, each
against the index and strategy built for it. The exact lookup, lexical,
on the tiny index:

```bash
curl -s "$OS_URL/support-issues/_search" -H 'Content-Type: application/json' \
  -d '{"size":1,"_source":["title"],"query":{"match":{"text":"ERR-2288"}}}' | python3 -m json.tool
```

**Expected result:** `ERR-2288: Schema discovery timed out` at rank 1,
instantly, from a 15-document index with zero vector overhead.

The customer-words search, vector-weighted (0.2 lexical / 0.8
semantic), on tickets. First create the tickets fusion pipeline:

```bash
curl -s -X PUT "$OS_URL/_search/pipeline/support-tickets-weighted" \
  -H 'Content-Type: application/json' -d '{
  "description": "Tickets lean semantic: customers describe symptoms in customer words",
  "phase_results_processors": [
    { "normalization-processor": {
        "normalization": { "technique": "min_max" },
        "combination": { "technique": "arithmetic_mean", "parameters": { "weights": [0.2, 0.8] } } } }
  ]
}'
```

```bash
curl -s "$OS_URL/support-tickets/_search?search_pipeline=support-tickets-weighted" \
  -H 'Content-Type: application/json' -d '{
  "size": 3, "_source": ["title"],
  "query": { "hybrid": { "queries": [
    { "match": { "text": "schema list never finishes loading" } },
    { "neural": { "embedding": {
      "query_text": "schema list never finishes loading",
      "model_id": "'$MODEL_ID'", "k": 50 } } }
  ] } }
}' | python3 -m json.tool
```

**Expected result:** tickets where customers described the same symptom
("Schema list never finishes loading, started this morning", ...).

**Checkpoint 4.2:** two questions, two indexes, two strategies, and you
can say why each fits: literal string on a tiny lexical index vs
customer phrasing on a semantically weighted one. (You also just
reused Lab 1 Step 12's discipline: those 0.2/0.8 weights are the ones
the golden set proved out.)

## Step 4: Be the agent (the ReAct trace from lesson 4.1, by hand)

**What you're doing:** executing the course's two-iteration agent trace
yourself. The customer on 4.9 writes: "schema discovery times out on
our biggest warehouse."

**Iteration 1. Reason:** sounds like a known failure mode; check the
known issues database first. **Act:**

```bash
curl -s "$OS_URL/support-issues/_search" -H 'Content-Type: application/json' -d '{
  "size": 1, "_source": ["title","text"],
  "query": { "match": { "text": "schema discovery timed out large warehouse" } }
}' | python3 -m json.tool
```

**Observe (read the returned `text`):** ERR-2288, root cause is the
information_schema query exceeding 120 seconds, workaround is scoping
the connection to specific schemas, affected versions 4.8 through 5.0,
fixed in 5.1.

**Iteration 2. Reason:** the workaround applies to 4.9; now get the
customer the exact steps. **Act:**

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 2, "_source": ["title","section_heading"],
  "query": { "match": { "text": "how to configure schema discovery scope schemas" } }
}' | python3 -m json.tool
```

**Observe:** the schema discovery configuration pages. **Answer:**
acknowledge the known issue, give the scoping steps, mention the 5.1
fix, cite both sources.

**Why this matters:** no pipeline you wrote chose that two-step
sequence; the *reasoning* chose it, and a different query would compose
differently. In production the agent framework runs this loop, and it
chooses tools by reading their descriptions, nothing else. Which is why
lesson 4.1's unglamorous design lever is the one to remember: write
tool descriptions like documentation for a sharp new teammate on their
first day. "Searches Example Corp known issues; returns error code,
affected versions, and workaround; prefer for error codes and
version-specific failures" gets used precisely. "Searches docs" gets
used vaguely and wrongly.

**Checkpoint 4.3:** you ran both iterations and can name what the agent
observed at each step that steered the next one.

## Step 5: The _msearch meta-tool (breadth in one round trip)

**What you're doing:** gathering the chapter 3 nemesis's evidence from
three indexes at once, one network round trip:

```bash
curl -s "$OS_URL/_msearch" -H 'Content-Type: application/x-ndjson' --data-binary $'{"index":"support-issues"}\n{"size":1,"_source":["title"],"query":{"match":{"text":"ERR-2209 handshake"}}}\n{"index":"support-docs"}\n{"size":2,"_source":["title"],"query":{"match":{"text":"TLS 1.3 connector advanced settings"}}}\n{"index":"support-tickets"}\n{"size":2,"_source":["title"],"query":{"match":{"text":"ERR-2209 resolved"}}}\n' \
  | python3 -c "
import sys, json
for i, r in enumerate(json.load(sys.stdin)['responses'], 1):
    print(f'--- sub-search {i} ---')
    for h in r['hits']['hits']:
        print(' ', h['_source']['title'][:65])"
```

**Expected result:** three labeled blocks: the known issue from
`support-issues`; connector docs pages from `support-docs` (titles
like `Connector Credential Rotation settings reference`; their Common
errors sections carry the TLS fix, even when the page title is about
something else); and resolved ERR-2209 tickets from `support-tickets`.

**Why two gather modes:** this is the same `_msearch` you met in lesson
2.3, promoted from pipeline trick to agent tool. Give the agent both
modes and say so in the descriptions: sequential calls when each result
should steer the next search (Step 4), `_msearch` when you need breadth
fast (this step).

**Checkpoint 4.4:** three sub-responses in one call, each from a
different index.

## Step 6: The routing cache (the cost math, live)

**What you're doing:** caching routing decisions in the cluster, so
repeat questions never pay for a router again. Create a small ingest
pipeline that embeds cache entries server-side, then the cache index:

```bash
curl -s -X PUT "$OS_URL/_ingest/pipeline/support-cache-embed" \
  -H 'Content-Type: application/json' -d '{
  "description": "Embeds query_text for the routing and answer caches",
  "processors": [
    { "text_embedding": {
        "model_id": "'$MODEL_ID'",
        "field_map": { "query_text": "query_embedding" } } }
  ]
}'
```

```bash
curl -s -X PUT "$OS_URL/support-route-cache" -H 'Content-Type: application/json' -d '{
  "settings": { "index": { "knn": true, "default_pipeline": "support-cache-embed" } },
  "mappings": { "properties": {
    "query_text": {"type":"text"},
    "query_embedding": {"type":"knn_vector","dimension":384,
      "method":{"name":"hnsw","engine":"faiss","space_type":"innerproduct"}},
    "route": {"type":"keyword"}, "created_at": {"type":"date"}
  } }
}'
```

Seed one routing decision (in production, the router writes this on
every cache miss):

```bash
curl -s -X POST "$OS_URL/support-route-cache/_doc?refresh=true" -H 'Content-Type: application/json' -d '{
  "query_text": "how do I set up report bursting",
  "route": "howto_path",
  "created_at": "2026-07-09T12:00:00Z"
}'
```

Now the money moment. A different customer asks the same question in a
different outfit:

```bash
curl -s "$OS_URL/support-route-cache/_search?filter_path=hits.hits._score,hits.hits._source.route" \
  -H 'Content-Type: application/json' -d '{
  "size": 1, "min_score": 1.7,
  "query": { "neural": { "query_embedding": {
    "query_text": "steps to configure report bursting",
    "model_id": "'$MODEL_ID'", "k": 1 } } }
}' | python3 -m json.tool
```

**Expected result:** a hit, `route: howto_path`, score ~1.93. Zero
router calls. And prove the threshold protects you, with a genuinely
different question:

```bash
curl -s "$OS_URL/support-route-cache/_search?filter_path=hits.hits._score" \
  -H 'Content-Type: application/json' -d '{
  "size": 1, "min_score": 1.7,
  "query": { "neural": { "query_embedding": {
    "query_text": "why did my export to PDF fail",
    "model_id": "'$MODEL_ID'", "k": 1 } } }
}' | python3 -m json.tool
```

**Expected result:** `{}`. No hit; that question scores ~1.20, below
the 1.7 threshold, so it goes to the router and then into the cache.

**Why:** support traffic is brutally repetitive: the same twenty
questions arrive dressed forty different ways. At 500 tickets a day
with a 70% cache hit rate, that lookup just deleted 70% of your routing
spend, every day. The search engine is subsidizing the AI.

**Checkpoint 4.5:** the paraphrase hits (score above 1.7, route
returned), the unrelated question misses, and you can say what the
`min_score` threshold is protecting you from.

## Step 7: The semantic answer cache, scoped or nothing

**What you're doing:** caching whole answers, with the chapter 3 lesson
built into the cache key. Same embedding pipeline, richer mapping:

```bash
curl -s -X PUT "$OS_URL/support-answer-cache" -H 'Content-Type: application/json' -d '{
  "settings": { "index": { "knn": true, "default_pipeline": "support-cache-embed" } },
  "mappings": { "properties": {
    "query_text": {"type":"text"},
    "query_embedding": {"type":"knn_vector","dimension":384,
      "method":{"name":"hnsw","engine":"faiss","space_type":"innerproduct"}},
    "answer": {"type":"text"}, "source_chunk_ids": {"type":"keyword"},
    "product_version": {"type":"keyword"}, "plan_tier": {"type":"keyword"},
    "created_at": {"type":"date"}
  } }
}'
```

Cache one answered question, scoped to the customer context it was
answered for:

```bash
curl -s -X POST "$OS_URL/support-answer-cache/_doc?refresh=true" -H 'Content-Type: application/json' -d '{
  "query_text": "how do I fix ERR-2209",
  "answer": "ERR-2209 is a TLS handshake failure. On 5.0+, enable TLS 1.3 in the connector advanced settings.",
  "source_chunk_ids": ["KI-0004#0.0"],
  "product_version": "5.1", "plan_tier": "standard",
  "created_at": "2026-07-09T12:05:00Z"
}'
```

A 5.1 standard-tier customer asks a paraphrase; the filter rides inside
the k-NN lookup:

```bash
curl -s "$OS_URL/support-answer-cache/_search?filter_path=hits.hits._score,hits.hits._source.answer" \
  -H 'Content-Type: application/json' -d '{
  "size": 1, "min_score": 1.7,
  "query": { "neural": { "query_embedding": {
    "query_text": "what is the fix for ERR-2209",
    "model_id": "'$MODEL_ID'", "k": 1,
    "filter": { "bool": { "must": [
      { "term": { "product_version": "5.1" } },
      { "term": { "plan_tier": "standard" } }
    ] } }
  } } }
}' | python3 -m json.tool
```

**Expected result:** the cached answer, in milliseconds, zero LLM
calls, zero tool calls.

Now the customer who must NOT get it, same question, version 4.8:

```bash
curl -s "$OS_URL/support-answer-cache/_search?filter_path=hits.hits._score" \
  -H 'Content-Type: application/json' -d '{
  "size": 1, "min_score": 1.7,
  "query": { "neural": { "query_embedding": {
    "query_text": "what is the fix for ERR-2209",
    "model_id": "'$MODEL_ID'", "k": 1,
    "filter": { "bool": { "must": [
      { "term": { "product_version": "4.8" } },
      { "term": { "plan_tier": "standard" } }
    ] } }
  } } }
}' | python3 -m json.tool
```

**Expected result:** `{}`. Lab 3 in one empty response: a cached 5.1
answer served to a 4.8 customer would be the version mismatch failure
wearing a performance optimization costume. Scope your cache keys or do
not cache.

Finally, invalidation, wired to the lesson 1.4 update patterns (the
nightly docs sync and the known-issues webhook are the triggers in
production):

```bash
curl -s -X POST "$OS_URL/support-answer-cache/_delete_by_query?refresh=true" \
  -H 'Content-Type: application/json' \
  -d '{"query":{"terms":{"source_chunk_ids":["KI-0004#0.0"]}}}'
```

**Expected result:** `"deleted": 1`. When a source chunk changes, every
answer built on it dies with it.

**Checkpoint 4.6:** hit for 5.1, miss for 4.8, and the invalidation
deleted exactly the entries citing the changed chunk.

## Step 8: Guardrails you can recite

**What you're doing:** no cluster calls here; this one is a discipline
check, because it is the part production teams get wrong first. Every
agent run stays inside four ceilings, checked on every ReAct
iteration:

1. **Iterations:** at most 5 trips around the loop.
2. **Tokens per request:** enforced with per-interaction token usage
   tracking (a 3.6 agent-framework feature; keep it visible).
3. **Wall clock:** if the answer is not assembled in time for the SLA,
   more searching is not the fix.
4. **Cost per conversation:** a forty-turn escalation should not cost
   more than the human it is assisting.

And the design decision that matters more than the numbers: hitting a
ceiling is **not an error**. The agent stops, answers from the evidence
it has already gathered, flags reduced confidence, and escalates to a
human.

**Checkpoint 4.7 (explain-it-back):** name the four ceilings from
memory and say what happens when one fires. If your answer is "error,"
reread; the answer is "stop, answer from gathered evidence, flag
confidence, escalate", the same graceful degradation as Lab 3's retry
budget. Whether the limit is retries, iterations, or tokens: this
system fails honest, never confident.

## Step 9: The payoff: one true RAG answer (LLM path)

**What you're doing:** running the entire build end to end: tuned
hybrid retrieval, parent-child packing under a token budget, and real
generation with citations, honoring the customer's version. First, the
customer who can be helped:

```bash
python3 scripts/rag_answer.py --llm-id $LLM_ID --model-id $MODEL_ID \
  --query "how do I fix ERR-2209" --customer-version 5.1
```

**Sample output from our validated run** (yours will differ in wording,
per Lab 0's caveat; it must cite chunk IDs and give the TLS 1.3
setting):

```
packed 8 parent sections: ['DOC-00404#0.0', 'DOC-00639#0.0', 'DOC-00498#2.0', ...]

To fix ERR-2209, you need to enable TLS 1.3 in the connector advanced
settings. This resolution is available in version 5.0 and later
[DOC-00298#3.0, DOC-00445#2.0, DOC-00204#2.0]. Since the customer is on
version 5.1, this solution applies to their version.

Steps to resolve ERR-2209:
1. Navigate to the connector settings.
2. Access the advanced settings.
3. Enable TLS 1.3.

This issue was fixed in version 5.0, and versions 4.8 and 4.9 were
affected [DOC-00298#3.0, DOC-00445#2.0, DOC-00204#2.0].
```

Now the chapter 3 nemesis, the customer the evidence does NOT fit:

```bash
python3 scripts/rag_answer.py --llm-id $LLM_ID --model-id $MODEL_ID \
  --query "how do I fix ERR-2209" --customer-version 4.8
```

**Sample output from our validated run:**

```
packed 8 parent sections: ['DOC-00404#0.0', 'DOC-00639#0.0', 'DOC-00498#2.0', ...]

The error ERR-2209 occurs because the TLS negotiation failed due to the
warehouse requiring TLS 1.3, which is not supported in your current
version (4.8) [DOC-00298#3.0, DOC-00445#2.0, DOC-00210#2.0].

Resolution:
The issue is fixed in version 5.0 and later, where you can enable
TLS 1.3 in the connector advanced settings [DOC-00298#3.0,
DOC-00445#2.0, DOC-00210#2.0]. Since you are on version 4.8, the
recommended solution is to upgrade to version 5.0 or later to resolve
this error.

If upgrading is not an option, please contact support for further
assistance, as there is no workaround available for version 4.8.
```

**Why this is the right last step of the build:** look at what just
composed. Lab 1's retrieval and tuning chose the evidence. Lab 1's
parent-child chunking decided what the model read. The prompt carries
chapter 3's discipline: answer only from evidence, cite sources, and
say so when the evidence does not fit this customer. If your 4.8 answer
hedges or refuses instead of prescribing the 5.0-only fix, your system
just beat the failure case this whole course was built around, with
the LLM as the last step, not the load-bearing one. Retrieval quality
was the product all along.

**Checkpoint 4.8:** the 5.1 answer prescribes the TLS 1.3 fix with
chunk-ID citations; the 4.8 answer explicitly flags that the fix
requires 5.0 rather than presenting it as actionable.

> **No-LLM alternative:** you have already seen every component of this
> step separately: the retrieval in Lab 1, the packing rule in lesson
> 2.2, and the honest refusal in Lab 3's LOW CONFIDENCE ending. The
> sample outputs above show what the assembled system produces.

---

**What you built:** four purpose-built indexes behind flip-able
aliases, a hand-run ReAct trace, a one-round-trip evidence gatherer, a
routing cache that pays for itself, a scoped answer cache with real
invalidation, and the ceilings that keep all of it shippable.
**What you should be able to explain:** why the five assets never
wanted one index, why tool descriptions are a design surface, and why
security and cost controls live below the agent, not in its prompt.
That is the full build. The conclusion's decision framework tells you
how much of it YOUR system actually needs.
