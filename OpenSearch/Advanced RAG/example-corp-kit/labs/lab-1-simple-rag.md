# Lab 1: Simple RAG & Hybrid Search (Chapter 1)

**Time:** ~60 minutes (about 10 of them waiting on ingest).
**Requires:** Lab 0 complete, `OS_URL` and `MODEL_ID` exported in this
shell.

**The story so far:** Example Corp's support team answers the same
questions all day, and the answers are scattered across five data
assets: product docs, integration guides, ticket history, a known
issues database, and the API reference. In this lab you stand up the
retrieval layer of the support tool: build the index and pipelines
yourself, ingest the corpus, feel the difference between lexical,
semantic, and hybrid retrieval on real support questions, and then stop
trusting your feelings and measure it.

---

## Part A: Build the ingest machinery (lessons 1.3, 1.4)

## Step 1: Look at what you're about to ingest

**What you're doing:** reading one chunk of the corpus before you index
a single byte of it.

```bash
head -1 corpus/example-corp-corpus-v2.1.0/chunks.jsonl | python3 -m json.tool
```

**Expected result:** one JSON document. Notice three things before
moving on:

- `chunk_id` (`DOC-00001#0.0`): a stable ID in
  `document#section.child` form. Re-ingesting can never duplicate,
  because the same chunk always writes to the same ID. That is lesson
  1.3's idempotence rule, visible in the data.
- the metadata block (`doc_type`, `product_version`, `acl`,
  `updated_at`, `related_error_codes`): stamped at parse time, not
  bolted on later. These fields power the security filters in Part C
  and the correction logic in Lab 3.
- `parent_text` riding alongside the searchable `text`: parent-child
  chunking. You search the small precise child; the LLM receives the
  full parent section.

**Checkpoint 1.1:** you can point at the `chunk_id`, the `acl` field,
and `parent_text` in the output and say what each is for.

## Step 2: Create the ingest pipeline

**What you're doing:** creating the pipeline that turns text into
vectors at ingest time. Paste this exactly; it uses the `MODEL_ID` you
exported in Lab 0.

```bash
curl -s -X PUT "$OS_URL/_ingest/pipeline/support-embed" \
  -H 'Content-Type: application/json' -d '{
  "description": "Embedding at ingest for the support tool. The model here MUST match the model used at query time.",
  "processors": [
    { "text_embedding": {
        "model_id": "'$MODEL_ID'",
        "field_map": { "text": "embedding" } } }
  ]
}'
```

**Why:** this is the manual path from lesson 1.1. Every document that
enters the index flows through this `text_embedding` processor, which
calls your deployed model and writes a 384-dimension vector into the
`embedding` field. Ingest-side embedding and query-side embedding will
use the same `model_id`, which is the one rule lesson 1.1 said matters
more than the rest: same model, same dimensionality, same vector space.

**Expected result:** `{"acknowledged":true}`

## Step 3: Create the index and its alias

**What you're doing:** creating `support-docs-v1` with an explicit
mapping (no dynamic guessing for the fields retrieval depends on), and
putting the alias `support-docs` in front of it.

```bash
curl -s -X PUT "$OS_URL/support-docs-v1" -H 'Content-Type: application/json' -d '{
  "settings": {
    "index": {
      "knn": true,
      "number_of_shards": 2,
      "number_of_replicas": 1,
      "default_pipeline": "support-embed"
    }
  },
  "mappings": {
    "properties": {
      "text":         { "type": "text" },
      "parent_text":  { "type": "text", "index": false },
      "embedding": {
        "type": "knn_vector",
        "dimension": 384,
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "space_type": "innerproduct",
          "parameters": { "m": 16, "ef_construction": 128 }
        }
      },
      "chunk_id":     { "type": "keyword" },
      "parent_id":    { "type": "keyword" },
      "source_id":    { "type": "keyword" },
      "doc_type":     { "type": "keyword" },
      "title":        { "type": "text", "fields": { "raw": { "type": "keyword" } } },
      "section_heading": { "type": "text" },
      "section_path": { "type": "keyword" },
      "product_area": { "type": "keyword" },
      "product_version": { "type": "keyword" },
      "acl":          { "type": "keyword" },
      "updated_at":   { "type": "date" },
      "related_error_codes": { "type": "keyword" },
      "embedding_model_id":      { "type": "keyword" },
      "embedding_model_version": { "type": "keyword" }
    }
  }
}'
```

```bash
curl -s -X POST "$OS_URL/_aliases" -H 'Content-Type: application/json' -d '{
  "actions": [ { "add": { "index": "support-docs-v1", "alias": "support-docs" } } ]
}'
```

**Why, three design decisions worth reading before you move on:**

- **`knn: true` + the `embedding` mapping** is lesson 1.1's ANN setup:
  Faiss engine (the default choice at scale), HNSW graph, and the two
  index-time knobs you heard about, `m` and `ef_construction`. The
  query-time knob, `ef_search`, stays a query-time decision.
- **`default_pipeline: support-embed`** means nothing can enter this
  index without passing through the embedding processor. Fail-loudly by
  construction, per lesson 1.4.
- **The alias** is lesson 1.4's zero-downtime trick. Everything you
  build from here on talks to `support-docs`, never to `-v1`. When a
  model change forces a reindex someday, you flip the alias and nothing
  else changes.

**Expected result:** both calls return `{"acknowledged":true}` (the
index creation also echoes the index name).

## Step 4: Create both hybrid search pipelines

**What you're doing:** creating the two fusion strategies from lesson
1.2 as search pipelines, so Part B can compare them on the same query.

Reciprocal rank fusion (rank-based, no score calibration needed):

```bash
curl -s -X PUT "$OS_URL/_search/pipeline/support-hybrid-rrf" \
  -H 'Content-Type: application/json' -d '{
  "description": "Hybrid merge via reciprocal rank fusion",
  "phase_results_processors": [
    { "score-ranker-processor": {
        "combination": { "technique": "rrf", "rank_constant": 60 } } }
  ]
}'
```

Normalized weighted fusion (min_max, 40% lexical / 60% semantic):

```bash
curl -s -X PUT "$OS_URL/_search/pipeline/support-hybrid-weighted" \
  -H 'Content-Type: application/json' -d '{
  "description": "Hybrid merge via min_max normalization, 0.4 lexical / 0.6 semantic",
  "phase_results_processors": [
    { "normalization-processor": {
        "normalization": { "technique": "min_max" },
        "combination": {
          "technique": "arithmetic_mean",
          "parameters": { "weights": [0.4, 0.6] } } } }
  ]
}'
```

**Why two:** RRF merges by rank, so it never has to compare a BM25
score to a cosine similarity; its one knob is `rank_constant`. Weighted
fusion gives you explicit control but is only as reliable as its
normalization. Lesson 1.2's play: start with RRF, and only move to
weighted once your eval harness (Part D) can prove the change is an
improvement.

**Expected result:** `{"acknowledged":true}` twice.

## Step 5: Ingest

**What you're doing:** loading all 8,955 chunks through the embedding
pipeline, in modest batches, with backpressure handling.

```bash
python3 scripts/ingest_chunks.py --model-id $MODEL_ID \
  --chunks corpus/example-corp-corpus-v2.1.0/chunks.jsonl
```

**What's happening while you wait:** every batch of 100 chunks goes to
`_bulk`, and the `support-embed` pipeline embeds each one before
indexing it. The wait you are feeling right now IS the lesson 1.4
point: at ingest time, embedding is the bottleneck, not indexing.
Expect the first batch to be the slowest (the model is warming up),
then steady progress lines, roughly 5-15 minutes total depending on
cluster size.

**How it should feel:** steady lines like
`indexed 4200/8955 (batch=100, took=64ms)`. If you see
`bulk rejection... backing off` or `timeout... halving batch`, that is
the backpressure discipline from lesson 1.4 working as designed, not an
error: slow the producer, never retry-storm a shared cluster. The
script is also resumable; if it dies, run the same command again and it
picks up where it left off (stable chunk IDs make re-runs harmless,
which is what idempotent ingestion means). One honest footnote if you
do resume: re-indexing the overlap batch leaves deleted document
versions behind, which nudges BM25's corpus statistics until segments
merge, so your Step 11 numbers may drift by a few thousandths compared
to an uninterrupted run.

**Expected result (final line, your minutes will vary):**

```
Done. 8955 chunks indexed into support-docs-v1 in 9.2 min.
```

**Checkpoint 1.2:** two verifications. Count everything:

```bash
curl -s "$OS_URL/support-docs/_count?filter_path=count"
```

Expected: `{"count":8955}`. Then verify the "fail loudly" property,
zero chunks without embeddings:

```bash
curl -s "$OS_URL/support-docs/_count" -H 'Content-Type: application/json' \
  -d '{"query":{"bool":{"must_not":{"exists":{"field":"embedding"}}}}}'
```

Expected: `"count":0`. If it is anything else, stop and re-run Step 5;
lesson 1.4 explained why silently missing embeddings are the worst
failure in this system: the cluster stays healthy while retrieval
quietly decays.

## Part B: Feel the retrieval strategies (lessons 1.1, 1.2)

## Step 6: The error code (BM25's home turf)

**What you're doing:** running lesson 1.1's first query, the customer
who pastes an error code:

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 3, "_source": ["title","doc_type"],
  "query": { "match": { "text": "ERR-2209" } }
}' | python3 -m json.tool
```

**Expected result:** every hit is ERR-2209 content, but notice *which*
asset dominates: ticket chunks ("ERR-2209 when rotating Presto
credentials", "Getting ERR-2209 on every attempt") and the API
reference's connector-test endpoint. Three years of tickets mention
this code a lot, and BM25 happily surfaces all of them at similar
scores.

Now ask for the canonical answer instead of the whole pile: same query,
filtered to the knowledge assets:

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 3, "_source": ["title","doc_type"],
  "query": { "bool": {
    "must": { "match": { "text": "ERR-2209" } },
    "filter": [ { "terms": { "doc_type": ["known-issue","product-docs","integration-guide"] } } ] } }
}' | python3 -m json.tool
```

**Expected result:** rank 1 is the known issue
`ERR-2209: Connector handshake failed` with a `_score` around 2.9,
clearly above the ~2.2 docs chunks below it.

**Why:** when the literal text is the signal, BM25 wins, exactly as
lesson 1.1 said. And you just met a theme Lab 4 turns into
architecture: different assets answer different questions, and
`doc_type` is how you aim.

**Checkpoint 1.3:** in the filtered query, the known issue leads with
visible score separation. That separation is what lesson 3.1 will call
a healthy score shape.

## Step 7: The vague symptom (where BM25 fails and vectors shine)

Now the customer who does not paste codes, only frustration. To see the
docs story the lesson told, keep the `product-docs` filter on both
legs. Lexical first:

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 3, "_source": ["title","doc_type"],
  "query": { "bool": {
    "must": { "match": { "text": "charts spin forever and never appear" } },
    "filter": [ { "term": { "doc_type": "product-docs" } } ] } }
}' | python3 -m json.tool
```

**Expected result:** off-topic matches like
`Troubleshooting pagination` and `Troubleshooting API authentication`.
No docs page uses the customer's words, so BM25 grabs incidental terms.

Then the same question through the vector leg:

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 3, "_source": ["title","doc_type"],
  "query": { "bool": {
    "must": { "neural": { "embedding": {
      "query_text": "charts spin forever and never appear",
      "model_id": "'$MODEL_ID'", "k": 200 } } },
    "filter": [ { "term": { "doc_type": "product-docs" } } ] } }
}' | python3 -m json.tool
```

**Expected result:** rank 1 is `Troubleshooting dashboard rendering`.
Zero words in common with the question, and it is exactly the right
page.

**Why:** embeddings capture meaning, so semantically similar chunks
match even when the vocabulary does not. And one more observation worth
pausing on: run the BM25 query *without* the docs filter and the ticket
history nails even this vague phrasing, because some past customer
already said it almost the same way. Hold that thought; it is why
lesson 1.3 calls the ticket history a gift, and why Lab 4 gives tickets
their own index and strategy.

**How it should feel:** this is the moment the course pivot clicks.
Neither strategy is better. They are better at different questions.

**Checkpoint 1.4:** the neural top-3 leads with dashboard rendering
content; the BM25 top-3 for this query is visibly off-topic.

## Step 8: Hybrid, both legs at once

**What you're doing:** running lesson 1.2's hybrid query, where an
exact term and a described symptom arrive in the same question, through
both fusion pipelines.

```bash
curl -s "$OS_URL/support-docs/_search?search_pipeline=support-hybrid-rrf" \
  -H 'Content-Type: application/json' -d '{
  "size": 5, "_source": ["title","doc_type"],
  "query": { "hybrid": { "queries": [
    { "match": { "text": "Snowflake connector failing ERR-2209" } },
    { "neural": { "embedding": {
      "query_text": "Snowflake connector failing with ERR-2209",
      "model_id": "'$MODEL_ID'", "k": 50 } } }
  ] } }
}' | python3 -m json.tool
```

Now the same body through the weighted pipeline, and compare the
orderings:

```bash
curl -s "$OS_URL/support-docs/_search?search_pipeline=support-hybrid-weighted" \
  -H 'Content-Type: application/json' -d '{
  "size": 5, "_source": ["title","doc_type"],
  "query": { "hybrid": { "queries": [
    { "match": { "text": "Snowflake connector failing ERR-2209" } },
    { "neural": { "embedding": {
      "query_text": "Snowflake connector failing with ERR-2209",
      "model_id": "'$MODEL_ID'", "k": 50 } } }
  ] } }
}' | python3 -m json.tool
```

**Expected result:** both pipelines surface connector-handshake and
Snowflake content (ticket chunks dominate the top 5, for the same
reason as Step 6: the ticket history mentions this failure constantly).
Two things to notice. The orderings differ between RRF and weighted,
which is expected, not a bug: they are different merge strategies over
the same two candidate lists. And the score *scales* are wildly
different: RRF scores are small rank-derived numbers (~0.03), weighted
scores are normalized to 0-1. This is lesson 3.1's warning made
visible: absolute scores are not comparable across query types or
pipelines.

**Checkpoint 1.5:** you can say which two legs ran, and why the
orderings differ between the two pipelines.

## Part C: Filters are security (lesson 1.2)

## Step 9: The pre-filter

**What you're doing:** retrieving as a standard-tier customer, with the
tier constraint applied *inside* the candidate set, not after.

```bash
curl -s "$OS_URL/support-docs/_search" -H 'Content-Type: application/json' -d '{
  "size": 5, "_source": ["title","acl","product_version"],
  "query": { "bool": {
    "must": { "match": { "text": "schema discovery timed out" } },
    "filter": [
      { "terms": { "acl": ["public", "standard"] } }
    ] } }
}' | python3 -m json.tool
```

**Expected result:** every hit's `acl` is `public` or `standard`.

**Checkpoint 1.6:** nothing enterprise-tier appears, because it never
entered the candidate set. Say out loud why this beats filtering after
retrieval; if your answer includes "the LLM can never see what
retrieval never returned," you have it. Lesson 1.2's rule: pre-filter
the hard requirements (tenant, tier, version), consider post-filtering
only for soft signals.

## Part D: Stop feeling, start measuring (lesson 1.3)

## Step 10: Meet the golden set

**What you're doing:** looking at the answer key before you grade
anything with it.

```bash
head -1 corpus/example-corp-corpus-v2.1.0/golden_set.jsonl | python3 -m json.tool
```

**Expected result:** one query object: the query text, its type, the
resolved ticket it came from, and `relevant_chunk_ids`, the chunk-level
labels. There are 300 of these. Resolved tickets already linked
customer questions to the docs that answered them, so the labels came
practically for free, exactly as lesson 1.3 promised.

## Step 11: Run the ablation

**What you're doing:** evaluating retrieval alone (no LLM anywhere),
three strategies on the identical golden set. Roughly 3-4 minutes per
run. One flag deserves a sentence before you run it: `--kb-only`
restricts eval retrieval to the knowledge-base assets (docs, guides,
known issues, API reference). The golden *queries* were harvested from
resolved tickets, so letting eval retrieve ticket chunks would mean
finding the question again instead of the answer, a circularity that
inflates nothing but your confusion.

```bash
export OS_INDEX=support-docs
python3 scripts/eval_retrieval.py --mode bm25 --k 5 --kb-only \
  --golden corpus/example-corp-corpus-v2.1.0/golden_set.jsonl
python3 scripts/eval_retrieval.py --mode neural --k 5 --kb-only --model-id $MODEL_ID \
  --golden corpus/example-corp-corpus-v2.1.0/golden_set.jsonl
python3 scripts/eval_retrieval.py --mode hybrid --k 5 --kb-only --model-id $MODEL_ID \
  --search-pipeline support-hybrid-rrf \
  --golden corpus/example-corp-corpus-v2.1.0/golden_set.jsonl
```

**What the three numbers mean:** hit rate@5 is coverage (did a right
chunk make the top 5 at all); precision@5 is purity (how much of the
top 5 is signal); MRR is position (how high the first right answer
sits). Lesson 1.3's triage logic: low hit rate points at parsing,
chunking, or embedding; good hit rate with low MRR points at
granularity, fusion, or reranking.

**Expected result:** within about 0.02 of this reference table, per
cell:

| mode | hit_rate@5 | precision@5 | MRR |
| --- | --- | --- | --- |
| bm25 | 0.513 | 0.123 | 0.319 |
| neural | 0.633 | 0.147 | 0.339 |
| hybrid (rrf) | 0.550 | 0.139 | 0.323 |

Why "about" and not "exactly," when Lab 0 promised identical vectors?
Because two things about retrieval are legitimately not deterministic
across ingest runs even on identical data: this corpus produces many
exactly tied BM25 scores (tie order depends on segment layout), and
HNSW graph construction has its own run-to-run variation. The
*embedding* of a given text is bit-identical everywhere; the *ranking*
around ties is not. The relationships below are the real contract, and
they reproduce every time.

**How to read it, because this table has a surprise in it:** neural
wins on this golden set, and unweighted hybrid lands between the legs
instead of on top. Why: these golden queries were written the way
customers write ("signed embed url expired", "schema list never
finishes loading"), which is the vector leg's home turf, so the BM25
leg's misses dilute the fused list. This is not "hybrid is bad"; it is
"fusion has parameters, and defaults are not destiny." Your production
traffic will have a different query mix (more pasted error codes
shifts the balance back toward the lexical leg), which is exactly why
you measure on YOUR queries instead of trusting anyone's defaults,
including this course's.

**Checkpoint 1.7:** each of your cells is within ~0.02 of the table,
and the ordering holds: neural > hybrid-rrf > bm25 on hit rate.

## Step 12: Close the loop, tune the fusion

**What you're doing:** acting on the measurement, exactly the move
lesson 1.2 promised: move from defaults only when the golden set proves
the change. The ablation says the semantic leg deserves more weight, so
build a candidate pipeline at 0.2 lexical / 0.8 semantic:

```bash
curl -s -X PUT "$OS_URL/_search/pipeline/support-hybrid-tuned" \
  -H 'Content-Type: application/json' -d '{
  "description": "Eval-tuned min_max weights: 0.2 lexical / 0.8 semantic",
  "phase_results_processors": [
    { "normalization-processor": {
        "normalization": { "technique": "min_max" },
        "combination": {
          "technique": "arithmetic_mean",
          "parameters": { "weights": [0.2, 0.8] } } } }
  ]
}'
```

And prove it against the same golden set:

```bash
python3 scripts/eval_retrieval.py --mode hybrid --k 5 --kb-only --model-id $MODEL_ID \
  --search-pipeline support-hybrid-tuned \
  --golden corpus/example-corp-corpus-v2.1.0/golden_set.jsonl
```

**Expected result** (same ~0.02 tolerance as Step 11):

```
mode=hybrid pipeline=support-hybrid-tuned kb_only=True k=5 queries=300
  hit_rate@5:  0.610
  precision@5: 0.141
  MRR:          0.337
```

**Why this matters more than the specific numbers:** one weight change,
measured: hit rate 0.550 -> 0.610, an 11% relative improvement, and now
you know the direction the dial turns on this data. You did not guess,
you did not tune by vibes, and you have a number to defend in code
review. That is the discipline the rest of the course builds on.

**Checkpoint 1.8:** your tuned hit rate clearly beats your Step 11
hybrid-rrf hit rate (by roughly 0.05 or more), and you can say why
weighted fusion could be tuned here when RRF could not (RRF has no
weights, only the rank constant).

---

**What you built:** an ingested, hybrid, filtered, measured retrieval
layer, and you created every piece of it yourself: pipeline, mapping,
alias, fusion, filters, eval.
**What you should be able to explain to a teammate:** why ERR-2209 and
"dashboards feel slow" need different retrieval, why filters run inside
the candidate set, and what your three eval numbers each diagnose.
Lab 2 breaks this system with a two-turn conversation.
