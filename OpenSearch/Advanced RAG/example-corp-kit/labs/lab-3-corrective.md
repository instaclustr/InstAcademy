# Lab 3: Corrective RAG (Chapter 3)

**Time:** ~30 minutes. **Requires:** Lab 1 complete, `OS_URL` and
`MODEL_ID` exported (`LLM_ID` too if you are on the LLM path).

**The story:** the scariest RAG failure is not retrieval returning
nothing. It is retrieval returning the almost-right thing, fluently. In
this lab you reproduce the course's version mismatch case on your own
cluster, learn to read score shapes, use `_explain`, and then run the
correction loop, watching it succeed, and watching it fail honestly.

---

## Step 1: Serve a customer an impossible answer

**What you're doing:** playing the support tool answering a customer on
version 4.8 who hit ERR-2209. Retrieve the canonical answer:

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 1, "_source": ["title","text"],
  "query": { "bool": {
    "must": { "match": { "text": "ERR-2209" } },
    "filter": [ { "term": { "doc_type": "known-issue" } } ] } }
}' | python3 -m json.tool
```

**Expected result:** the known issue, and read its text carefully:

```
ERR-2209: Connector handshake failed
Symptom: Users encounter ERR-2209 (connector handshake failed).
Root cause: TLS negotiation failed because the warehouse requires TLS 1.3
Workaround: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later
Affected versions: 4.8, 4.9
Fixed in: 5.0
```

**Why this is the whole chapter in one document:** the retrieval was
relevant (exactly the right topic). A model summarizing it would be
faithful. And the answer is *impossible for this customer to follow*:
the fix, and even the "workaround," require 5.0, and the customer is on
4.8. Nothing in Lab 1's pipeline compares the customer's version to the
`Affected versions` / `Fixed in` facts sitting right there in the
chunk. Garbage in does not look like garbage. It looks like a polished,
cited answer.

**Checkpoint 3.1:** you can point at the two facts that never met: the
customer's version (4.8, from the ticket) and the chunk's
`Fixed in: 5.0`.

## Step 2: Learn to read score shapes (lesson 3.1)

**What you're doing:** running a healthy query and a sick one, and
looking only at the scores. Healthy first:

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 8, "_source": false,
  "query": { "bool": {
    "must": { "match": { "text": "ERR-2209" } },
    "filter": [ { "terms": { "doc_type": ["known-issue","product-docs","integration-guide"] } } ] } }
}' | python3 -c "import sys,json; print(' '.join(f'{h[\"_score\"]:.2f}' for h in json.load(sys.stdin)['hits']['hits']))"
```

**Expected result:** `2.92 2.21 2.21 2.21 2.18 2.18 2.18 2.18`
A clear leader, a visible drop, then the tail. Something specific
matched.

Now a query whose answer does not exist in the corpus:

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 8, "_source": false,
  "query": { "bool": {
    "must": { "match": { "text": "everything felt slower after the office move last week" } },
    "filter": [ { "terms": { "doc_type": ["known-issue","product-docs","integration-guide"] } } ] } }
}' | python3 -c "import sys,json; print(' '.join(f'{h[\"_score\"]:.2f}' for h in json.load(sys.stdin)['hits']['hits']))"
```

**Expected result:** `1.74 1.74 1.74 1.74 1.73 1.73 1.73 1.73`
A low, flat huddle. Nothing really matched; you are looking at the
eight *least irrelevant* chunks in the index.

**Why:** train your eye on relative shape, not absolute values
(absolute scores are not comparable across query types, as you saw with
RRF vs weighted scores in Lab 1). Flat AND low is a retrieval alarm you
can compute in one line, and it becomes the free first pass of the
correction loop in Step 4.

**Checkpoint 3.2:** you can label both lists (healthy / sick) and say
what each shape means.

## Step 3: Ask the engine WHY (\_explain)

**What you're doing:** decomposing a score with `explain`.

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 1, "explain": true, "_source": ["title"],
  "query": { "match": { "text": "ERR-2209" } }
}' | python3 -m json.tool | head -60
```

**Expected result:** the winner plus an `_explanation` tree: which
terms matched in which fields, what each clause contributed, how the
pieces combined ("sum of:", term frequencies, field norms).

**Why, and the limit that motivates Step 4:** `_explain` tells you
whether the query, the chunking, or a field weight put the wrong chunk
on top. But run it mentally against Step 1: the explanation there would
show a *perfectly healthy* lexical match on ERR-2209. Score diagnostics
catch weak retrieval. They cannot catch relevant retrieval that fails
the customer's context. For that you need a grader that reads.

**Checkpoint 3.3:** you found the term-level contributions inside
`_explanation`, and you can say what _explain cannot catch.

## Step 4: Run the correction loop, all three outcomes

**What you're doing:** running the two-pass loop from lesson 3.2: a
free score-shape gate, then a grader that reads each chunk's version
facts against the customer, then corrections driven by the grader's
reasons, inside a retry budget of 2.

The customer who gets caught (and honestly refused):

```bash
python3 scripts/correction_loop.py --query "how do I fix ERR-2209" --customer-version 4.8
```

**Expected result, walk it line by line:**

- **attempt 0** (knowledge base): the score gate lets the results
  through (the shape is not flat-AND-low), then the grader fails every
  chunk with
  `version fit: instructions require 5.0, customer on 4.8`.
  The metadata you stamped in Lab 1 just became a correction signal.
- **correction 1:** adds the hard version pre-filter (lesson 1.2's
  move).
- **attempt 1:** still fails: 4.8-scoped docs describe the same
  5.0-gated fix. Look closely and you may spot a bonus finding:
  `granularity: section truncated by a chunk boundary before its
  resolution`. That is a lesson 1.3 anti-pattern (a chunk split before
  its fix), caught live by the grader.
- **correction 2:** pivots to the ticket history, because somewhere a
  human wrote down what actually worked.
- **attempt 2:** the resolved tickets all say "upgrade to 5.0," which
  is still gated for this customer. Budget spent.
- **Final line:** `LOW CONFIDENCE: retry budget (2) spent.` The system
  says what it knows, what it does not, and hands off to a human with
  the trail attached.

The customer who sails through:

```bash
python3 scripts/correction_loop.py --query "how do I fix ERR-2209" --customer-version 5.1
```

**Expected result:** `CONFIDENT after 0 correction(s)`, with the known
issue and connector docs as evidence. Same chunks, different customer,
opposite verdict; that is what "evidence fit" means.

And the pre-5.0 customer who CAN be helped (a different issue with an
ungated workaround):

```bash
python3 scripts/correction_loop.py --query "how do I fix ERR-2288" --customer-version 4.9
```

**Expected result:** `CONFIDENT after 0 correction(s)` with no FAIL
lines at all. Internally the grader saw that the ERR-2288 fix requires
5.1, but it passes the chunks anyway because the workaround (scope the
connection to specific schemas) has no version gate; passing chunks
print no reasons, only failing ones do.

**How it should feel:** the system is arguing with itself, cheaply, and
losing the argument is allowed. An assistant that says "I am not
certain, here is what I found, here is who can help" builds trust with
every miss. One that guesses burns trust with every hit.

**Checkpoint 3.4:** the 4.8 run shows `version fit` FAILs and ends LOW
CONFIDENCE without exceeding 3 retrieval attempts; both other runs
reach CONFIDENT with zero corrections.

**Checkpoint 3.5 (the explain-it-back moment):** in one sentence, why
did metadata you ingested in Lab 1 just prevent a wrong answer in Lab
3? Target answer: the grader compared the customer's version against
the version facts stamped on the chunk at parse time in lesson 1.3,
fields that looked like bookkeeping until this moment.

## Step 4b: The grader that reads, for real (LLM path)

**What you're doing:** the loop you just ran graded with regexes over
metadata, which is cheap and deterministic but narrow. Lesson 3.2's
production grader is an LLM that *reads*. Hand the real model the exact
evidence-fit question for our 4.8 customer:

```bash
curl -s -X POST "$OS_URL/_plugins/_ml/models/$LLM_ID/_predict" \
  -H 'Content-Type: application/json' -d '{
  "parameters": { "prompt": "You are a retrieval grader for a support assistant. The customer is on product version 4.8. Retrieved chunk: ERR-2209: Connector handshake failed. Symptom: Users encounter ERR-2209 (connector handshake failed). Root cause: TLS negotiation failed because the warehouse requires TLS 1.3. Workaround: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later. Affected versions: 4.8, 4.9. Fixed in: 5.0. Question: does this chunk give THIS customer an actionable fix? Reply with ONLY one line of JSON: {\"pass\": true or false, \"reason\": \"short reason\"}" }
}' | python3 scripts/llm_text.py
```

**Sample output from our validated run** (wording varies per Lab 0's
caveat; the verdict must not):

```
{"pass": false, "reason": "The customer is on version 4.8, and the workaround requires version 5.0 or later."}
```

**Why this matters:** the LLM grader reaches the same verdict as your
metadata grader (FAIL on version fit) but it got there by *reading*,
with no regex that had to anticipate the failure shape. That is what
you pay the model call for: the middle band of cases no metadata rule
anticipated. Production systems run exactly the two-pass design you
just experienced: free score gate first, reading grader only on what
survives it.

**Checkpoint 3.5b:** your grader returns `"pass": false` with a reason
about the version. If your model passes the chunk, read its reason;
then tighten the prompt (say "the workaround itself requires 5.0") and
run it again, you just did prompt iteration on a grader, which is a
production skill, not a lab failure.

> **No-LLM alternative:** skip this step; the metadata grader in Step 4
> already demonstrated the verdict, and the script's docstring shows
> where an LLM grader slots in.

## Step 5: Make it observable (lesson 3.3)

**What you're doing:** creating the traces index, logging one request
trace, and answering a dashboard question with an aggregation.

```bash
curl -s -X PUT "$OS_URL/support-traces" -H 'Content-Type: application/json' -d '{
  "mappings": { "properties": {
    "request_id": {"type":"keyword"}, "created_at": {"type":"date"},
    "product_area": {"type":"keyword"}, "customer_version": {"type":"keyword"},
    "query": {"type":"text"}, "rewritten_query": {"type":"text"},
    "retrieved_chunk_ids": {"type":"keyword"},
    "grader_verdicts": {"type":"keyword"}, "retries": {"type":"integer"},
    "confidence": {"type":"keyword"}, "faithfulness": {"type":"float"},
    "context_relevance": {"type":"float"},
    "latency_ms": {"properties": {"retrieval":{"type":"integer"},"grading":{"type":"integer"},"total":{"type":"integer"}}}
  } }
}'
```

Log the trace of your Step 4 run (in production, the pipeline writes
this automatically on every request):

```bash
curl -s -X POST "$OS_URL/support-traces/_doc?refresh=true" -H 'Content-Type: application/json' -d '{
  "request_id":"REQ-LAB3-001","created_at":"2026-07-09T11:00:00Z",
  "product_area":"connectors","customer_version":"4.8",
  "query":"how do I fix ERR-2209","retries":2,
  "grader_verdicts":["fail:version-fit","fail:version-fit","fail:version-fit"],
  "confidence":"low","faithfulness":0.91,"context_relevance":0.44,
  "latency_ms":{"retrieval":180,"grading":420,"total":842}
}'
```

Then ask a dashboard question as a query: which product areas grade
worst, and what does correction cost there?

```bash
curl -s "$OS_URL/support-traces/_search" -H 'Content-Type: application/json' -d '{
  "size": 0,
  "aggs": { "by_area": { "terms": { "field": "product_area" },
    "aggs": { "avg_faithfulness": { "avg": { "field": "faithfulness" } },
              "avg_retries":      { "avg": { "field": "retries" } } } } }
}' | python3 -m json.tool
```

**Expected result:** one `connectors` bucket with
`avg_faithfulness: 0.91` and `avg_retries: 2.0`.

**Why:** one synthetic document, but the shape is the real thing: every
request logs a trace, and "which product areas grade worst this week"
becomes a query instead of a data export. Quality regressions show up
as chart movements days before they show up as angry escalations. In
Lab 4, agent runs write into this same index.

**Checkpoint 3.6:** the aggregation returns the bucket with both
averages.

---

**What you built:** eyes (score shapes, `_explain`), a conscience (a
grader that checks evidence fit, with a retry budget), and a memory of
its own behavior (traces).
**What you should be able to explain:** why the version mismatch is
scarier than a hallucination, why hitting the retry budget is a
feature, and what only a grader that reads can catch. Lab 4 hands this
well-instrumented system the steering wheel.
