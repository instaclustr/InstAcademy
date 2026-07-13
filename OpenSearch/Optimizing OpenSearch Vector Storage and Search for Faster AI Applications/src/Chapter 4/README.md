# Chapter 4 — Performance meets precision: RAG optimization in OpenSearch

**Chapter 4** · [Vector Storage & Search for AI](../../README.md)

← [Chapter 3](../Chapter%203/README.md) · [How to run labs](../../HANDS-ON-GUIDE.md) · **Next:** [Chapter 5](../Chapter%205/README.md)

Take a working RAG pipeline and make it production-ready, layer by layer: tune the **pipeline** (Lesson 4-1), the **index** (Lesson 4-2), and the **query** (Lesson 4-3), then expose it all to AI agents through the **built-in MCP server** (Lesson 4-4). Everything runs against one bookstore dataset so you can watch each optimization change the numbers.

## One index, built right the first time

This chapter builds a single chunked index — **`bookstore-rag`** (nested `content_chunks` + a 768-dim `content_embedding` on FAISS HNSW + exact-typed metadata) — up front, then pulls every pipeline, index, and query lever against it. **Index-time decisions are hard to undo**, so Lesson 4-2 examines what an unoptimized first attempt looks like and why this index is shaped the way it is.

> **Data note.** The course bulk file ([`rest/bulk/chapter-4-bookstore-rag.ndjson`](../../rest/bulk/chapter-4-bookstore-rag.ndjson)) is 256 real book summaries enriched with deterministic `genre`, `price`, `rating`, `publication_year`, and `in_stock` fields so the filtering, reranking, and rank-evaluation steps return meaningful results. Values are stable across runs (derived from `book_id`).

## Prerequisites

- Complete [Chapter 1 · Lesson 1](../Chapter%201/README.md) — cluster connectivity.
- A cluster with **ML Commons**, **k-NN**, and the **AI Search** plugin (the course 3-node Instaclustr cluster). See [cluster setup](../../CREATE_CLUSTER.md).
- Open **OpenSearch Dashboards → Dev Tools** (learn mode) or the [Bruno `Chapter 4`](../../bruno/Chapter%204/) collection (fast mode — flat, numbered up to `50`; the numbering has gaps where steps were consolidated).
- **Save as you go:** `model_group_id`, `model_id`, `task_id`. In Bruno, set them as `modelGroupId`, `modelId`, `taskId`, `agentId` environment variables.
- For k-NN / hybrid / profiling / rank-eval steps, open [`bookstore-rag-query-vector.json`](bookstore-rag-query-vector.json) in this folder — a pre-baked 768-dimensional query vector. Paste its array wherever a step shows `[ /* paste 768 floats … */ ]`.

> **OpenSearch 3.x note.** `nmslib` was removed in OpenSearch 3.0; **FAISS** is the production k-NN engine (Lucene remains available). This chapter uses `engine: faiss` with the `hnsw` method throughout. `text_chunking`, `_rank_eval`, and the MCP server APIs below were verified against the OpenSearch 3.x documentation.

---

# Lesson 4-1 — Optimizing RAG pipelines

**Goal:** build the bookstore RAG pipeline — chunked at ingest, embedded server-side — then pull the levers that matter most: engine selection (FAISS HNSW), result-set size and filtering, hybrid search, and reranking.

**Why two levers?** RAG optimization is a trade-off between **performance** (retrieval latency) and **accuracy** (retrieval quality). Faster is not always better; the goal is to tune the balance for your use case.

> **ML Commons prerequisites (already set in Chapter 2).** The persistent settings from [Chapter 2 · Step 2](../Chapter%202/README.md#step-2--enable-ml-commons-cluster-settings) — URL model registration, `only_run_on_ml_node: false` (required to deploy models on this 3-node cluster), and the relaxed native-memory threshold — are still in effect. Starting fresh at this chapter? Run Chapter 2 Step 2 first, then come back.

### Step 1: Reuse the model group from Chapter 2

**Why** — model groups scope access to a set of models. The `huggingface-models` group already exists from Chapter 2 Step 3 — reuse its `model_group_id` rather than creating another group. If you still have the id, skip to Step 2; if not, look it up:

**Request**
```http
POST _plugins/_ml/model_groups/_search
{ "query": { "match": { "name": "huggingface-models" } } }
```
**Save** — the group's `_id` as `model_group_id`.
**Fast mode** — `02-find-model-group.bru`

> **Never delete this group** — it contains models registered by other chapters; only remove models you personally registered into it. (On a fresh cluster with no group yet, create it with the `POST _plugins/_ml/model_groups/_register` body from Chapter 2 Step 3.)

### Step 2: Register `all-mpnet-base-v2`

**Why** — embedding-model choice moves recall by 10–20% on domain data. `all-mpnet-base-v2` (768-dim) is a stronger general-English encoder than Chapter 2's DistilBERT — a good RAG default. Replace `YOUR_MODEL_GROUP_ID`.

**Request**
```http
POST _plugins/_ml/models/_register
{
  "name": "huggingface/sentence-transformers/all-mpnet-base-v2",
  "version": "1.0.1",
  "model_group_id": "YOUR_MODEL_GROUP_ID",
  "model_format": "TORCH_SCRIPT"
}
```
**Expected** — a `task_id`. Poll `GET _plugins/_ml/tasks/YOUR_TASK_ID` until `"state": "COMPLETED"`.
**Save** — `model_id`.
**Fast mode** — `03-register-mpnet-model.bru` → `04-poll-register-task.bru`

### Step 3: Deploy the model

**Why** — deploying loads the model into memory for inference at ingest and query time.

**Request**
```http
POST _plugins/_ml/models/YOUR_MODEL_ID/_deploy
```
**Expected** — a `task_id`; poll until `COMPLETED`. Write down the returned `model_id` (in Bruno, set `modelId` in the **Local** environment).
**Fast mode** — `05-deploy-model.bru` → `06-poll-deploy-task.bru`

### Step 4: Create the chunking ingest pipeline

**Why** — a 2,000-word description is too long for one embedding; models truncate past ~512 tokens. The native `text_chunking` processor splits `content` into overlapping segments at ingest. `fixed_token_length` with `token_limit: 384` (~75% of a 512-token budget, leaving headroom) and `overlap_rate: 0.2` (20% overlap so boundary context is not lost — valid range is 0–0.5). A Painless step reshapes the raw chunk array into `{text, chunk_index}` objects for the nested field, then `text_embedding` embeds the whole `content` into `content_embedding`. Replace `YOUR_MODEL_ID`.

**Request**
```http
PUT _ingest/pipeline/bookstore-chunking-pipeline
{
  "description": "Chunk and embed book content for RAG",
  "processors": [
    {
      "text_chunking": {
        "algorithm": { "fixed_token_length": { "token_limit": 384, "overlap_rate": 0.2, "tokenizer": "standard" } },
        "field_map": { "content": "content_chunks" }
      }
    },
    {
      "script": {
        "lang": "painless",
        "source": "if (ctx.content_chunks == null) { ctx.content_chunks = []; } else { def n = []; for (int i = 0; i < ctx.content_chunks.size(); i++) { def c = ctx.content_chunks.get(i); if (c != null) { n.add(['text': c, 'chunk_index': i]); } } ctx.content_chunks = n; }"
      }
    },
    {
      "text_embedding": { "model_id": "YOUR_MODEL_ID", "field_map": { "content": "content_embedding" } }
    }
  ]
}
```
> **Structured documents.** For content with clear headers you can chunk with the `delimiter` algorithm (splits on `\n\n` by default) first, then apply `fixed_token_length` as a second pass for more coherent chunks.

**Expected** — `"acknowledged": true`.
**Fast mode** — `21-create-chunking-pipeline.bru`

### Step 5: Create the `bookstore-rag` index (FAISS HNSW, chunked)

**Why** — for production vector workloads **FAISS + HNSW** gives fast approximate nearest-neighbor search: `m` controls graph connectivity (higher = better recall, more memory) and `ef_construction` controls how carefully the graph is built — `m=16, ef_construction=128` is a balanced starting point. `content_chunks` is `nested` (required to keep each chunk's fields together), `genre` is `keyword` (exact filter, not full-text), and `refresh_interval` starts at `30s` — the catalog updates nightly, not per second.

**Request** — delete first if re-running: `DELETE bookstore-rag`.
```http
PUT bookstore-rag
{
  "settings": {
    "index": { "knn": true, "default_pipeline": "bookstore-chunking-pipeline", "refresh_interval": "30s" }
  },
  "mappings": {
    "properties": {
      "book_id": { "type": "keyword" }, "title": { "type": "text" }, "author": { "type": "text" },
      "content": { "type": "text" },
      "content_chunks": {
        "type": "nested",
        "properties": { "text": { "type": "text" }, "chunk_index": { "type": "integer" } }
      },
      "content_embedding": {
        "type": "knn_vector", "dimension": 768,
        "method": { "engine": "faiss", "name": "hnsw", "space_type": "l2", "parameters": { "m": 16, "ef_construction": 128 } }
      },
      "genre": { "type": "keyword" }, "price": { "type": "float" }, "rating": { "type": "float" },
      "publication_year": { "type": "integer" }, "in_stock": { "type": "boolean" }
    }
  }
}
```
**Expected** — `"acknowledged": true`.
**Fast mode** — `22-delete-bookstore-rag.bru` (optional) → `23-create-bookstore-rag.bru`

### Step 6: Fast bulk load (refresh off → bulk → force-merge → refresh on)

**Why** — the default 1-second refresh creates a new Lucene segment on every cycle, adding merge overhead during a batch load. Disable refresh for the load, then force-merge to collapse many small segments into a few large ones (fewer files to scan = faster search), then restore the refresh and make docs visible. Expect several minutes on a trial cluster — each document is chunked and embedded server-side (one inference per document).

**Request**
```http
PUT bookstore-rag/_settings
{ "index": { "refresh_interval": "-1" } }
```
Bulk-load — `POST _bulk?timeout=600s` then paste [`rest/bulk/chapter-4-bookstore-rag.ndjson`](../../rest/bulk/chapter-4-bookstore-rag.ndjson) (action lines target `bookstore-rag`). Allow several minutes for chunking + embedding.
```http
POST bookstore-rag/_forcemerge?max_num_segments=5
```
```http
PUT bookstore-rag/_settings
{ "index": { "refresh_interval": "1s" } }
```
```http
POST bookstore-rag/_refresh
```
Then check the shard picture — shard count is a near-permanent, one-time decision. Target **10–30 GB/shard** for search-heavy RAG, **30–50 GB** for write-heavy, and for pure vector start at **50 GB**, reducing toward **10 GB** if queries are hybrid and latency-sensitive (`number_of_shards = total_data_size_GB / target_shard_size_GB`; at ~5 GB for 500k books, one primary shard is plenty):
```http
GET _cat/shards/bookstore-rag?v&h=index,shard,prirep,state,docs,store&format=json
```
**Expected** — bulk `"errors": false` (if any item errors, check the model is deployed and `ML_MODEL_ID` is correct); force-merge returns `_shards` success; refresh makes all docs searchable; one row per shard with `docs` and `store`.
**Fast mode** — `24-disable-refresh.bru` → `25-bulk-bookstore-rag.bru` → `26-force-merge.bru` → `27-restore-refresh.bru` → `28-refresh-bookstore-rag.bru` → `29-cat-shards.bru`

### Step 7: k-NN search — the result-set-size lever

**Why** — vector search returns the top-`k` neighbors. Ask for only what you need (`size: 10`) and fetch only the fields you use with `_source` — over thousands of queries per hour, lean responses add up. Paste the stored query vector.

**Request**
```http
GET bookstore-rag/_search
{
  "size": 10,
  "_source": ["title", "author", "genre", "price", "rating"],
  "query": {
    "knn": {
      "content_embedding": { "vector": [ /* paste 768 floats from bookstore-rag-query-vector.json */ ], "k": 10 }
    }
  }
}
```
**Expected** — 10 nearest-neighbor hits, each `_source` limited to the five listed fields.
**Fast mode** — `11-knn-search.bru`

### Step 8: Filtered k-NN search — the filtering lever

**Why** — filtering is the biggest performance win: narrow the candidate set by exact metadata **before** the vector pass. FAISS supports filtered k-NN (efficient filtering), so a query for "mystery under $20 with good ratings" only scores books that already match. `must` drives scoring; `filter` clauses are cheap yes/no gates.

**Request**
```http
GET bookstore-rag/_search
{
  "size": 10,
  "_source": ["title", "author", "genre", "price", "rating"],
  "query": {
    "knn": {
      "content_embedding": {
        "vector": [ /* paste 768 floats */ ],
        "k": 10,
        "filter": {
          "bool": {
            "must": [ { "term": { "genre": "mystery" } } ],
            "filter": [
              { "range": { "price": { "lte": 20 } } },
              { "range": { "rating": { "gte": 4.0 } } }
            ]
          }
        }
      }
    }
  }
}
```
**Expected** — only mystery books priced ≤ $20 with rating ≥ 4.0 (six such books exist in the sample data).
**Fast mode** — `12-knn-filtered-search.bru`

### Step 9: Hybrid search — create the pipeline and run it

**Why** — vector and BM25 scores live on different scales, so you cannot average them raw. A `normalization-processor` rescales both to 0–1 (`min_max`) and blends them with weights you control. Here `[0.3, 0.7]` maps in clause order to `[keyword, vector]` — semantic relevance matters more for a bookstore. The `hybrid` query then combines the exact-match precision of BM25 with the semantic reach of k-NN; its clause order must match the pipeline's `weights` order.

**Request** — create the pipeline:
```http
PUT _search/pipeline/bookstore-hybrid-pipeline
{
  "description": "Hybrid search pipeline for bookstore RAG",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": { "technique": "min_max" },
        "combination": {
          "technique": "arithmetic_mean",
          "parameters": { "weights": [0.3, 0.7] }
        }
      }
    }
  ]
}
```
**Request** — run the hybrid query through it:
```http
GET bookstore-rag/_search?search_pipeline=bookstore-hybrid-pipeline
{
  "size": 10,
  "_source": { "excludes": ["content_embedding", "content_chunks"] },
  "query": {
    "hybrid": {
      "queries": [
        { "match": { "content": { "query": "mystery novel with an unreliable narrator" } } },
        { "knn": { "content_embedding": { "vector": [ /* paste 768 floats */ ], "k": 10 } } }
      ]
    }
  }
}
```
**Expected** — `"acknowledged": true`, then hits with normalized, blended `_score` values; the embedding and chunks are excluded from `_source`.
**Fast mode** — `13-create-hybrid-pipeline.bru` → `14-hybrid-search.bru`

### Step 10: Reranking with business signals

**Why** — reranking reorders the candidate set using signals that were not part of similarity: recency, rating, availability. A `function_score` query boosts recent, highly-rated, in-stock books so business-relevant results float to the top.

> **Reconciling note.** The video shows this as a Painless response processor that mutates `hit._score` and re-sorts `ctx._source`. That snippet is illustrative — OpenSearch has no response processor that re-sorts hits by an arbitrary Painless score. The runnable, supported equivalent is a `function_score` query (below), which produces the same "boost recent + highly-rated + in-stock" ranking.

**Request**
```http
GET bookstore-rag/_search
{
  "size": 10,
  "_source": ["title", "author", "genre", "rating", "publication_year", "in_stock"],
  "query": {
    "function_score": {
      "query": { "knn": { "content_embedding": { "vector": [ /* paste 768 floats */ ], "k": 10 } } },
      "functions": [
        { "field_value_factor": { "field": "rating", "factor": 0.1, "missing": 3.0 } },
        { "filter": { "range": { "publication_year": { "gte": 2020 } } }, "weight": 1.2 },
        { "filter": { "term": { "in_stock": true } }, "weight": 1.15 }
      ],
      "score_mode": "sum",
      "boost_mode": "sum"
    }
  }
}
```
**Expected** — the same candidate books, reordered so recent, highly-rated, in-stock titles rank higher.
**Fast mode** — `15-rerank-function-score.bru`

---

# Lesson 4-2 — Optimizing indexes for RAG

**Goal:** understand the index-design choices that are hard to change later — and see that the index you built in Lesson 4-1 already makes them: correct field types, native chunking, intentional shard sizing, and the fast-bulk recipe. One hands-on lever remains: warming and preloading the vector files.

**The unoptimized baseline (read-along).** A common starting point: a flat index with `text` on fields you actually filter on (ISBN, genre), no vector field, and the default 1-second refresh. It works for keyword search but is not RAG-ready. There's no need to create a bad index just to read its mapping back — study it here and spot the problems:

```json
{
  "settings": { "index": { "number_of_shards": 2, "number_of_replicas": 1 } },
  "mappings": {
    "properties": {
      "book_id": { "type": "text" }, "title": { "type": "text" }, "author": { "type": "text" },
      "isbn": { "type": "text" }, "genre": { "type": "text" }, "published_year": { "type": "integer" },
      "price": { "type": "float" }, "rating": { "type": "integer" }, "content": { "type": "text" }
    }
  }
}
```

The three problems: no `knn_vector` field, `text` (not `keyword`) on `genre`/`isbn` — so filters run full-text analysis instead of exact matches — and the default 1-second refresh. The index you built in Steps 4–6 fixes all three.

### Step 11: Warm and preload the vector files

**Why** — after a restart HNSW graphs sit on disk and the first queries pay a load penalty. **Warmup** loads graphs into native memory. `index.store.preload` mmaps the k-NN `vec` (vectors) and `vem` (vector metadata) files into the OS file cache on index open — which requires a close → set → open cycle. Make warmup part of your deploy checklist after index creation and any large load.

**Request**
```http
GET _plugins/_knn/warmup/bookstore-rag
```
```http
GET _plugins/_knn/stats
```
```http
POST bookstore-rag/_close
```
```http
PUT bookstore-rag/_settings
{ "index": { "store": { "preload": ["vec", "vem"] } } }
```
```http
POST bookstore-rag/_open
```
```http
GET _cluster/health/bookstore-rag?wait_for_status=yellow&timeout=60s
```
**Expected** — warmup reports warmed shards; after `_open`, health reaches `yellow` (or `green`). In the k-NN stats watch `graph_memory_usage_percentage`, `cache_hit_rate` (rises toward 1.0 after warming), and `graph_query_requests`.

> **Circuit breaker — already configured.** You set `knn.memory.circuit_breaker.limit` to 50% in Chapter 2 Step 15; it's the same knob and still applies here. Raise it only if the stats above show `graph_memory_usage_percentage` pressing the limit — and remember it's a persistent, cluster-wide setting on a shared lab cluster.
**Fast mode** — `30-knn-warmup-bookstore-rag.bru` → `31-knn-stats-bookstore-rag.bru` → `32-close-index.bru` → `33-set-preload.bru` → `34-open-index.bru` → `35-cluster-health.bru`

> **Production checklist (runbook).** 1) create chunking pipeline → 2) create index → 3) disable refresh → 4) bulk load → 5) force-merge + restore refresh → 6) warm k-NN → 7) verify shards + stats. Seven repeatable, verifiable steps.

---

# Lesson 4-3 — Query optimization

**Goal:** the fastest wins, because they need no re-indexing. Profile a query to find the bottleneck, measure retrieval quality with `_rank_eval`, and centralize query logic in search pipelines so application code never changes. Runs against `bookstore-rag`.

> **Profiling and explain (read-along).** Two debugging tools worth knowing, neither worth running here:
>
> - `"profile": true` on any search returns a per-component timing breakdown (`query`/`collector` in nanoseconds) — the tool for finding which clause is slow. **But on OpenSearch 3.5.0, `profile` + a `hybrid` query throws a 500 `null_pointer_exception`** in the neural-search plugin (verified live — the hybrid collector doesn't support the profiler wrapper). Profile the `match` and `knn` sub-queries independently instead; Chapter 5 profiles a plain query hands-on.
> - `explain=true` returns a per-hit `_explanation` tree of sub-scorers (BM25 term weights, vector similarity, normalization contributions). Expensive — debugging only, never in production.

### Step 12: Measure quality with `_rank_eval`

**Why** — a unit test for search quality. Provide test queries and the IDs you consider relevant (with ratings); OpenSearch returns a metric like `mean_reciprocal_rank` or precision@k. Use it to compare keyword vs hybrid, chunk sizes, or models with numbers instead of vibes. The IDs below are real books in the sample data (Moby Dick `2701`, Sherlock `1661`, Dracula `345`, Frankenstein `84`).

**Request**
```http
GET bookstore-rag/_rank_eval
{
  "requests": [
    {
      "id": "whale_query",
      "request": { "query": { "match": { "content": "whale sea captain revenge" } } },
      "ratings": [ { "_index": "bookstore-rag", "_id": "2701", "rating": 3 } ]
    },
    {
      "id": "detective_query",
      "request": { "query": { "match": { "content": "detective mystery investigation" } } },
      "ratings": [ { "_index": "bookstore-rag", "_id": "1661", "rating": 3 } ]
    },
    {
      "id": "gothic_query",
      "request": { "query": { "match": { "content": "gothic horror monster" } } },
      "ratings": [
        { "_index": "bookstore-rag", "_id": "345", "rating": 3 },
        { "_index": "bookstore-rag", "_id": "84", "rating": 2 }
      ]
    }
  ],
  "metric": { "mean_reciprocal_rank": { "k": 10, "relevant_rating_threshold": 1 } }
}
```
**Expected** — a top-level `metric_score` plus per-query `details`. Edit ratings or swap `match` for a `hybrid` query and re-run to watch the score move.
**Fast mode** — `38-rank-eval.bru`

### Step 13: A request-processor search pipeline, set as the index default

**Why** — search pipelines run three processor types: **request** (transform the query before it runs), **phase-results** (between query and fetch — where normalization lives), and **response** (modify results). A `filter_query` request processor injects an `in_stock: true` filter into *every* search, so you can change search behavior without redeploying the app. Setting it as `index.search.default_pipeline` applies it to every query automatically (distinct from `index.default_pipeline`, which is ingest); bypass it for one request with `?search_pipeline=_none`.

**Request** — create the pipeline:
```http
PUT _search/pipeline/bookstore-stock-filter
{
  "description": "Filter out-of-stock books from every search",
  "request_processors": [
    { "filter_query": { "query": { "term": { "in_stock": true } }, "tag": "stock_filter" } }
  ]
}
```
**Request** — make it the index default:
```http
PUT bookstore-rag/_settings
{ "index.search.default_pipeline": "bookstore-stock-filter" }
```
**Expected** — `"acknowledged": true` for both. Every subsequent search now hides out-of-stock books.
**Fast mode** — `39-create-stock-filter-pipeline.bru` → `40-set-default-search-pipeline.bru`

> **Combining filtering and normalization (read-along).** In principle one pipeline can do both — a `filter_query` request processor for business rules plus a `normalization-processor` for hybrid relevance. **Don't build it on OpenSearch 3.5.0:** verified live, the filtering works but the blended scores come back raw and un-normalized when the two processor types share a pipeline (identical to a plain `knn` query's scores instead of the 0.0–1.0 range `bookstore-hybrid-pipeline` produces alone in Step 9). Running two separate pipelines back-to-back doesn't help either — only one search pipeline applies per request. Until the neural-search plugin fixes the interaction, put business-rule filters in a `bool` clause inside the hybrid query itself when you need normalized scores **and** filtering together.

---

# Lesson 4-4 — Connecting AI agents with the built-in MCP server

**Goal:** expose the cluster to AI agents through the **Model Context Protocol (MCP)**. OpenSearch ships a built-in MCP server in ML Commons: flip one cluster setting and any MCP-compatible client can discover and call tools (list indexes, read mappings, run searches) without custom integration code.

> **Version + environment.** The built-in MCP server APIs are recent: tool register/list were **introduced in 3.1**, the **Streamable HTTP** transport at `/_plugins/_ml/mcp` in **3.3**. Step 14 (enable + register tools) is safe on any 3.3+ cluster. The **appendix** steps (A1–A3: external LLM connector + conversational agent) require an **external LLM API key** and outbound network access, which the managed course cluster may not permit — treat them as an optional, read-along section and substitute your own provider/credentials.

### Step 14: Enable the MCP server and register tools

**Why** — one persistent setting turns the cluster into an MCP server exposed at `/_plugins/_ml/mcp` (Streamable HTTP) and `/_plugins/_ml/mcp/sse` (SSE) — no restart. Registering tools then lets clients discover and call them; the core tools map to the operations you have used all chapter: list indexes, read a mapping, run a search.

**Request** — enable the server:
```http
PUT _cluster/settings
{
  "persistent": { "plugins.ml_commons.mcp_server_enabled": "true" }
}
```
**Request** — register the tools:
```http
POST _plugins/_ml/mcp/tools/_register
{
  "tools": [
    { "name": "ListIndexTool",    "type": "ListIndexTool",    "description": "List indexes in the cluster" },
    { "name": "IndexMappingTool", "type": "IndexMappingTool", "description": "Read an index mapping" },
    { "name": "SearchIndexTool",  "type": "SearchIndexTool",  "description": "Run a search query against an index" }
  ]
}
```
Confirm:
```http
GET _plugins/_ml/mcp/tools/_list
```
**Expected** — `"acknowledged": true` for the setting; the registered tools appear in `_list`.
**Fast mode** — `43-enable-mcp-server.bru` → `44-register-mcp-tools.bru` → `45-list-mcp-tools.bru`

## Appendix (optional): LLM-driven agents

### A1: Connect an external LLM

**Why** — the MCP server exposes tools, but an LLM decides which to call. ML Commons registers a remote model via a connector. Replace the credential with your own; this creates the connector and model in one call.

**Request**
```http
POST _plugins/_ml/models/_register
{
  "name": "Bookstore Agent LLM",
  "function_name": "remote",
  "description": "GPT model for bookstore agent",
  "connector": {
    "name": "OpenAI Chat Connector",
    "description": "Connector to OpenAI chat completions",
    "version": 1,
    "protocol": "http",
    "parameters": { "model": "gpt-4o" },
    "credential": { "openAI_key": "<YOUR_OPENAI_API_KEY>" },
    "actions": [
      {
        "action_type": "predict",
        "method": "POST",
        "url": "https://api.openai.com/v1/chat/completions",
        "headers": { "Authorization": "Bearer ${credential.openAI_key}" },
        "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": ${parameters.messages} }"
      }
    ]
  }
}
```
**Expected** — a `task_id`; poll for the `model_id`, then `POST _plugins/_ml/models/<model_id>/_deploy`. Bedrock, Anthropic Claude, and Cohere use the same connector framework (see the OpenSearch connectors docs).
**Save** — `model_id`.
**Fast mode** — `46-register-llm-connector-model.bru`

### A2: Register a conversational agent

**Why** — an agent coordinates the LLM and tools using the ReAct pattern (Reason → Act → Observe). `memory.type: conversation_index` stores chat history for follow-ups; the tools array is what the LLM may call. Replace `YOUR_MODEL_ID`.

**Request**
```http
POST _plugins/_ml/agents/_register
{
  "name": "Bookstore Search Agent",
  "type": "conversational",
  "description": "AI agent for bookstore search and recommendations",
  "llm": {
    "model_id": "YOUR_MODEL_ID",
    "parameters": { "max_iteration": 10, "response_filter": "$.choices[0].message.content" }
  },
  "memory": { "type": "conversation_index" },
  "parameters": { "_llm_interface": "openai/v1/chat/completions" },
  "tools": [
    { "type": "ListIndexTool",    "name": "ListIndexTool" },
    { "type": "IndexMappingTool", "name": "IndexMappingTool" },
    { "type": "SearchIndexTool",  "name": "SearchIndexTool", "parameters": { "input": "${parameters.question}" } },
    { "type": "QueryPlanningTool" }
  ],
  "app_type": "os_chat"
}
```
**Expected** — an `agent_id`.
**Save** — `agent_id`.
**Fast mode** — `47-register-conversational-agent.bru`

### A3: Run the agent

**Why** — the agent discovers the index (`ListIndexTool`), reads its fields (`IndexMappingTool`), builds and runs a filtered query (`SearchIndexTool` / `QueryPlanningTool`), and answers. The response includes a `memory_id` for follow-up turns.

**Request**
```http
POST _plugins/_ml/agents/YOUR_AGENT_ID/_execute
{
  "parameters": { "question": "Find me highly rated mystery novels published after 2020 that are currently in stock" }
}
```
Follow-up (reuse the returned `memory_id`):
```http
POST _plugins/_ml/agents/YOUR_AGENT_ID/_execute
{
  "parameters": { "question": "Which of those has the best reviews?", "memory_id": "<memory_id_from_previous>" }
}
```
**Expected** — a final answer plus the reasoning trace and a `memory_id`.
**Fast mode** — `48-execute-agent.bru`

**External MCP clients.** Any MCP client can connect to the same server — point it at `{{baseUrl}}/_plugins/_ml/mcp` (Streamable HTTP) with your cluster credentials. LangChain agents, Claude Desktop, or Cursor can reuse the exact indexes and pipelines you built this chapter.

**Security.** The MCP server and agents inherit the caller's permissions. In production, create a dedicated read-only service account scoped to `bookstore-rag`, restrict which tools the agent can access (no `delete_index` for a customer-facing agent), and require TLS + authentication for external clients.

---

## Cleanup

Remove what this chapter created (order: search pipelines, indexes, ingest pipelines, model):
```http
DELETE _search/pipeline/bookstore-hybrid-pipeline
DELETE _search/pipeline/bookstore-stock-filter
DELETE bookstore-rag
DELETE _ingest/pipeline/bookstore-chunking-pipeline
```
Optionally undeploy the model (`POST _plugins/_ml/models/YOUR_MODEL_ID/_undeploy`) if no other chapter needs it. The index delete has a matching Bruno request: `50-cleanup-delete-bookstore-rag.bru`. (Earlier revisions of this workshop also created `bookstore-rag-index`, `books-unoptimized`, and the `bookstore-rag-ingest-pipeline` — delete them too if present; a `404` means they're already gone.)

## What you learned

- **Pipeline:** FAISS HNSW vs Lucene, result-set/filtering discipline, k-NN caching, hybrid normalization, and reranking with business signals.
- **Index:** native `text_chunking`, `nested` chunks, intentional shard sizing, the fast-bulk recipe, and vector warm/preload.
- **Query:** profiling, `_rank_eval`, and centralizing filters + normalization in search pipelines.
- **Agents:** enabling the built-in MCP server and (optionally) wiring an LLM-driven conversational agent.
