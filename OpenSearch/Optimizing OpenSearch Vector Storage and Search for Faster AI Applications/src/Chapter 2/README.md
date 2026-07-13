# Chapter 2 — Building neural search pipelines

**Chapter 2** · [Vector Storage & Search for AI](../../README.md)

← [Chapter 1](../Chapter%201/README.md) · [How to run labs](../../HANDS-ON-GUIDE.md) · **Next:** [Chapter 3](../Chapter%203/README.md)

This is the **single hands-on workshop** for Chapter 2. It is organized into one section per video lesson (2-1 … 2-5). Work top to bottom: each section builds on the cluster state left by the one before it. Every step uses the house layout — **Why**, **Request**, **Expected**, **Save**, and **Fast mode**.

> **How to read a step.** Run the **Request** in **OpenSearch Dashboards → Dev Tools**. **Fast mode** points at the matching [Bruno](../../bruno/Chapter%202/) request (identical body). See [HANDS-ON-GUIDE.md](../../HANDS-ON-GUIDE.md) for setup.

## What you will build

```
Raw text ─▶ Ingest pipeline (text_embedding) ─▶ 768-dim vector ─▶ k-NN index
                                                                      │
Natural-language query ─▶ same model ─▶ query vector ─▶ ANN search ─▶ semantic results
```

By the end you will have registered and deployed a sentence-transformer model with ML Commons, wired it into an ingest pipeline, bulk-loaded books, run semantic and hybrid queries, compared dense vs. sparse embeddings, inspected the model lifecycle, and tuned the cluster/index/query layers for neural search.

## Target version

Written for **OpenSearch 3.5+**. Where the video script simplifies or predates current behavior, a **Note** reconciles it with 3.5+.

## Prerequisites

- [Chapter 1 · Lesson 1](../Chapter%201/README.md) — cluster connectivity.
- [Cluster setup](../../CREATE_CLUSTER.md) — a **3-node** Instaclustr cluster with the **AI Search / ML Commons** plugin and your IP on the firewall.
- **Dev Tools** open (or Bruno fast mode: [`bruno/Chapter 2/`](../../bruno/Chapter%202/)).
- A notepad (or the Bruno **Local** environment) for ids returned by ML Commons:

| Variable | From | Used in |
|----------|------|---------|
| `model_group_id` | Lesson 2-1 Step 3 | Register model |
| `model_id` (dense) | Lesson 2-1 Step 4/5 | Pipeline, queries; save as `ML_MODEL_ID` |
| `task_id` | any register/deploy/undeploy | Poll with `GET _plugins/_ml/tasks/{task_id}` |

**ML task polling.** Register, deploy, and undeploy return a `task_id` immediately and finish **asynchronously**. Poll `GET _plugins/_ml/tasks/YOUR_TASK_ID` every 2–3 seconds until `state` is `COMPLETED` (or `FAILED`). This pattern repeats throughout the chapter.

---

## Lesson 2-1 — Setting up your pipeline

*Register and deploy `msmarco-distilbert-base-tas-b` with ML Commons, then smoke-test embedding inference.*

Neural search needs a model that turns text into vectors **inside** the cluster. ML Commons is OpenSearch's built-in framework for that: you **register** a model (metadata + artifact download), **deploy** it (load weights into node memory), and then any ingest pipeline or query can call it — no external model server to host, scale, or monitor.

### Step 1 — Verify cluster connectivity

**Why**
ML registration fails with opaque errors when auth or TLS is wrong. Confirm REST access before downloading a model.

**Request**

```http
GET /
```

**Expected**

```json
{
  "cluster_name": "...",
  "version": { "number": "3.x.x" },
  "tagline": "The OpenSearch Project: https://opensearch.org/"
}
```

**Fast mode** `bruno/Chapter 2/01-cluster-info.bru`

### Step 2 — Enable ML Commons cluster settings

**Why**
A few persistent settings make model registration/deployment reliable on a small managed cluster:

- **`allow_registering_model_via_url`** — lets ML Commons fetch model artifacts from external URLs. Not strictly required for OpenSearch-provided pretrained models registered by *name + version*, but needed if you later register a custom `model_url`, so we turn it on now.
- **`only_run_on_ml_node: false`** — our 3-node cluster has **no dedicated ML nodes**. This lets the model load on data nodes; otherwise deploy fails with "no ML node found." ([docs](https://docs.opensearch.org/latest/ml-commons-plugin/pretrained-models/))
- **`model_access_control_enabled: false`** — keeps model-group access simple for the lab (no backend-role wiring).
- **`native_memory_threshold: 99`** — raises the guard that blocks deployment when native memory is scarce, so a trial cluster doesn't refuse a small model.

**Request**

```http
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.allow_registering_model_via_url": true,
    "plugins.ml_commons.only_run_on_ml_node": false,
    "plugins.ml_commons.model_access_control_enabled": false,
    "plugins.ml_commons.native_memory_threshold": 99
  }
}
```

**Expected** `acknowledged: true` with the four keys echoed under `persistent`.

> **Note (script reconciliation).** The video shows only `allow_registering_model_via_url`. On a cluster **with** dedicated ML nodes that single setting is enough; on the course's 3-node cluster you also need `only_run_on_ml_node: false`.

**Fast mode** `bruno/Chapter 2/02-enable-url-model-registration.bru`

### Step 3 — Register a model group

**Why**
Every ML Commons model belongs to a **model group** — the unit of organization and access control. Create it once, then pass its id into model registration.

**Request**

```http
POST _plugins/_ml/model_groups/_register
{
  "name": "huggingface-models",
  "description": "A group for Hugging Face transformer models"
}
```

**Expected**

```json
{ "model_group_id": "...", "status": "CREATED" }
```

**Save** `model_group_id` for Step 4. If the group already exists, reuse its id instead of recreating.

**Fast mode** `bruno/Chapter 2/03-register-model-group.bru`

### Step 4 — Register the embedding model

**Why**
Registration downloads and validates the pretrained **`msmarco-distilbert-base-tas-b`** artifact on the cluster and assigns it a **`model_id`**. `TORCH_SCRIPT` selects the TorchScript serialization (ONNX is the other option). This runs asynchronously and returns a `task_id`.

Replace `YOUR_MODEL_GROUP_ID` with the id from Step 3.

**Request**

```http
POST _plugins/_ml/models/_register
{
  "name": "huggingface/sentence-transformers/msmarco-distilbert-base-tas-b",
  "version": "1.0.3",
  "model_group_id": "YOUR_MODEL_GROUP_ID",
  "model_format": "TORCH_SCRIPT"
}
```

**Expected**

```json
{ "task_id": "...", "status": "CREATED" }
```

**Poll** until complete:

```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

```json
{ "state": "COMPLETED", "model_id": "...", "task_type": "REGISTER_MODEL" }
```

**Save** `model_id`. This is your dense **`ML_MODEL_ID`** for the rest of the chapter.

> **Note.** `version: 1.0.3` and `model_format: TORCH_SCRIPT` are the current values for this model in the OpenSearch pretrained-model repository, which outputs **768-dimensional** vectors. ([docs](https://docs.opensearch.org/latest/ml-commons-plugin/pretrained-models/)) The video's "384-dimensional" line is a *generic* example — always match your index `dimension` to the model you actually deploy (768 here).

**Fast mode** `bruno/Chapter 2/04-register-model.bru`, then poll with `05-poll-ml-task.bru` (set `taskId`).

### Step 5 — Deploy the model

**Why**
Registration stores the artifact on disk; **deploy** loads it into node memory so `_predict`, ingest pipelines, and neural queries can run inference. The model moves `DEPLOYING → DEPLOYED`.

Replace `YOUR_MODEL_ID` with the id from Step 4.

**Request**

```http
POST _plugins/_ml/models/YOUR_MODEL_ID/_deploy
```

**Expected** `{ "task_id": "...", "status": "CREATED" }`

**Poll** the deploy task the same way:

```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

```json
{ "state": "COMPLETED", "model_id": "YOUR_MODEL_ID", "task_type": "DEPLOY_MODEL" }
```

**Save** confirm `model_id` and write it down — every later step that says `YOUR_MODEL_ID` means this value (in Bruno, set `modelId` in the **Local** environment).

**Fast mode** `bruno/Chapter 2/06-deploy-model.bru`, then `07-poll-ml-task-deploy.bru`.

### Step 6 — Smoke-test embedding inference

**Why**
Proves the deployed model returns vectors **before** you attach it to a pipeline. Text-embedding models are dispatched by algorithm, so they use the `/_predict/text_embedding/{model_id}` route (mixing this up returns a 400).

**Request**

```http
POST _plugins/_ml/_predict/text_embedding/YOUR_MODEL_ID
{
  "text_docs": ["Some example text to embed.", "Another sentence for testing."],
  "return_number": true,
  "target_response": ["sentence_embedding"]
}
```

**Expected** `inference_results` with one `sentence_embedding` per input, each a **768-float** dense vector (every position populated).

**Fast mode** `bruno/Chapter 2/08-text-embedding-predict.bru`

---

## Lesson 2-2 — Ingesting data and running queries

*Wire the model into an ingest pipeline, bulk-load books, and run semantic and hybrid queries on `vector-search-index`.*

An ingest pipeline is a named, server-side chain of **processors** that transforms every document as it is indexed. Attach one as an index's `default_pipeline` and clients can write plain text — OpenSearch calls the model and stores the vector for you, whether you index one document or bulk-insert thousands.

**Order matters:** create the **pipeline** before the **index** (the index references it in `default_pipeline`).

### Step 7 — Create the ingest pipeline

**Why**
The **`text_embedding`** processor reads `passage_text`, calls your deployed model, and writes the vector into `passage_embedding`. `field_map` is `{ source_field: vector_field }`.

Replace `YOUR_MODEL_ID` with `ML_MODEL_ID`.

**Request**

```http
PUT _ingest/pipeline/vector-search-embeddings-pipeline
{
  "description": "Generate passage_embedding from passage_text at index time",
  "processors": [
    {
      "text_embedding": {
        "model_id": "YOUR_MODEL_ID",
        "field_map": {
          "passage_text": "passage_embedding"
        }
      }
    }
  ]
}
```

**Expected** `{ "acknowledged": true }`

> **Note.** The processor also accepts `batch_size` (documents embedded per inference call, default `1`) and `skip_existing` (skip fields that already hold an embedding). ([docs](https://docs.opensearch.org/latest/ingest-pipelines/processors/text-embedding/)) Raising `batch_size` speeds up bulk ingest — see Lesson 2-5.

**Fast mode** `bruno/Chapter 2/09-create-ingest-pipeline.bru`

### Step 8 — Create the vector search index

**Why each setting**

- **`index.knn: true`** — enables ANN query support for `knn_vector` fields.
- **`default_pipeline`** — every document indexed here runs through the embeddings pipeline automatically.
- **`dimension: 768`** — must match the model's output; a mismatch fails ingestion.
- **`engine: lucene`, `name: hnsw`, `space_type: l2`** — a solid, easy-to-operate HNSW baseline.

**Request**

```http
PUT vector-search-index
{
  "settings": {
    "index.knn": true,
    "default_pipeline": "vector-search-embeddings-pipeline"
  },
  "mappings": {
    "properties": {
      "id": { "type": "text" },
      "title": { "type": "text" },
      "authors": { "type": "object", "enabled": false },
      "subjects": { "type": "keyword" },
      "bookshelves": { "type": "keyword" },
      "passage_text": { "type": "text" },
      "passage_embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "engine": "lucene",
          "space_type": "l2",
          "name": "hnsw",
          "parameters": {}
        }
      }
    }
  }
}
```

**Expected**

```json
{ "acknowledged": true, "shards_acknowledged": true, "index": "vector-search-index" }
```

If it already exists from a previous run: `DELETE vector-search-index` first.

**Fast mode** `bruno/Chapter 2/10-create-vector-search-index.bru`

### Step 9 — Bulk-index the book dataset

**Why**
Bulk indexing amortizes network overhead. Each document triggers the default pipeline, which embeds `passage_text` server-side. Expect **several minutes** on a trial cluster — one model inference per document.

The full body (256 books) is in [`rest/bulk/chapter-2-lesson-2-vector-search-index.ndjson`](../../rest/bulk/chapter-2-lesson-2-vector-search-index.ndjson). In Dev Tools: run the `POST _bulk` line, paste the **entire** `.ndjson` contents on the following lines (alternating action/source), and end with a **blank line**.

**Request**

```http
POST _bulk?timeout=60s
```

First lines of the payload look like:

```json
{"index": {"_index": "vector-search-index", "_id": "45304"}}
{"id": "45304", "title": "The City of God, Volume I", "authors": [...], "subjects": [...], "passage_text": "\"The City of God, Volume I\" by ...", "bookshelves": [...]}
```

**Expected** `errors: false`. If any item errors, the usual causes are an **undeployed model**, wrong **`model_id`** in the pipeline, or a **dimension mismatch**.

**Fast mode** `bruno/Chapter 2/11-bulk-ingest-books.bru` (body file points at the same `.ndjson`).

### Step 10 — Refresh the index

**Why**
OpenSearch is near-real-time. A refresh makes the bulk-indexed documents searchable immediately.

**Request**

```http
POST vector-search-index/_refresh
```

**Expected** `_shards.failed: 0`.

**Fast mode** `bruno/Chapter 2/12-refresh-index.bru`

### Step 11 — Set a default query model (optional but recommended)

**Why**
A **`neural_query_enricher`** search-pipeline processor injects a `default_model_id` into every neural query, so you can omit `model_id` from the query body. This keeps queries clean and prevents the classic "query model ≠ index model" recall bug. ([docs](https://docs.opensearch.org/latest/search-plugins/search-pipelines/neural-query-enricher/))

Replace `YOUR_MODEL_ID` with `ML_MODEL_ID`, then attach the pipeline as the index's default search pipeline.

**Request**

```http
PUT _search/pipeline/default-model-pipeline
{
  "request_processors": [
    {
      "neural_query_enricher": {
        "default_model_id": "YOUR_MODEL_ID"
      }
    }
  ]
}
```

```http
PUT vector-search-index/_settings
{
  "index.search.default_pipeline": "default-model-pipeline"
}
```

**Expected** `acknowledged: true` for both.

**Fast mode** `bruno/Chapter 2/13-set-default-model-search-pipeline.bru` creates the pipeline. The Bruno neural-search requests (14, 26) then apply it with the equivalent `?search_pipeline=default-model-pipeline` query parameter instead of the index-default setting, so the body still omits `model_id`.

### Step 12 — Run your first neural (semantic) query

**Why**
This is where semantic search becomes real. OpenSearch embeds your natural-language query with the **same** model used at ingest, then does ANN search against stored vectors — returning documents closest in **meaning**, not wording. Because Step 11 set a default model, the query omits `model_id`.

**Request**

```http
GET vector-search-index/_search
{
  "_source": { "excludes": ["passage_embedding"] },
  "query": {
    "neural": {
      "passage_embedding": {
        "query_text": "an ambitious scientist who comes to regret his own creation",
        "k": 10
      }
    }
  }
}
```

**Expected** Top hits ranked by semantic similarity — e.g. *Frankenstein; or, the Modern Prometheus* should surface even though the query shares almost no keywords with the summary. That is the semantic advantage, and it confirms the full pipeline (model → ingest → index → query) works end to end.

> **Note.** If you skipped Step 11, add `"model_id": "YOUR_MODEL_ID"` alongside `query_text`. `k` is the neighbors requested per shard before the coordinating node merges — higher `k` improves recall at more cost (see Lesson 2-5).

**Fast mode** `bruno/Chapter 2/14-neural-search.bru`

### Step 13 — Hybrid neural + keyword search

**Why**
Semantic `neural` handles paraphrase and intent; lexical `match` (BM25) nails exact terms. Combining them in a `bool.should` with `script_score` weights is a **hand-rolled hybrid baseline**. (Chapter 3 introduces the dedicated `hybrid` query with proper score normalization.) The `filter` restricts candidates first — a preview of the filtering optimization in Lesson 2-5.

**Request**

```http
GET vector-search-index/_search
{
  "_source": { "excludes": ["passage_embedding"] },
  "query": {
    "bool": {
      "filter": { "wildcard": { "id": "*1" } },
      "should": [
        {
          "script_score": {
            "query": {
              "neural": {
                "passage_embedding": {
                  "query_text": "historical fiction with an underdog story",
                  "model_id": "YOUR_MODEL_ID",
                  "k": 100
                }
              }
            },
            "script": { "source": "_score * 1.5" }
          }
        },
        {
          "script_score": {
            "query": {
              "match": { "passage_text": "historical fiction with an underdog story" }
            },
            "script": { "source": "_score * 1.7" }
          }
        }
      ]
    }
  }
}
```

**Expected** Hits with `_score`, `title`, `passage_text` (embedding excluded). Titles about historical or underdog narratives rank highly. Try flipping the `1.5`/`1.7` weights to see neural vs. lexical influence.

**Fast mode** `bruno/Chapter 2/15-hybrid-neural-keyword-search.bru`

---

## Lesson 2-3 — Choosing your text embedding processor

*Compare dense and sparse embedding shapes, then use a decision framework to pick the right processor.*

A text embedding processor turns raw text into a vector inside an ingest pipeline. The big choice is **dense vs. sparse**:

| | **Dense** (`text_embedding`) | **Sparse** (`sparse_encoding`) |
|---|---|---|
| Shape | Every dimension has a value (e.g. 768 floats) | Very high-dimensional, mostly zeros — a token→weight map |
| Captures | Deep semantic meaning, paraphrase | Important terms, lexical precision + some semantics |
| Best for | Semantic search, recommendations, RAG | Massive datasets, low latency, hybrid/lexical-leaning search |
| Cost | Heavier compute at ingest and query | Lighter, cheaper to store, scales horizontally |

You already produced a **dense** vector in Step 6 — a flat list of 768 floating-point numbers, every position populated (the "compact, filled" vector from the video's split-screen). For contrast, a **sparse** encoder run on the same text (`"today is sunny"`) returns a **token → weight** map instead:

```json
{ "today": 1.42, "sunny": 1.31, "weather": 0.44, "...": 0.12 }
```

Only meaningful terms appear — the "very tall, mostly zeros" vector represented compactly. You'll register, deploy, and search with a sparse model hands-on in **Chapter 3** (its Steps 2–3 register `opensearch-neural-sparse-encoding-v1`, and its `neural_sparse` queries use it against real data), so there's no need to load a second model into this chapter's memory budget just to look at its output.

### Decision framework

1. **Start from the use case.** Deep semantic understanding (customer support, recommendations, RAG retrieval) → **dense**. Huge datasets or very low latency (product search, log analytics, filtering millions of small docs) → **sparse**.
2. **Consider dimensionality.** Higher-dimensional dense vectors add nuance but cost storage and query time. Sparse vectors have tens of thousands of *possible* dimensions yet stay cheap because almost all are zero.
3. **Consider pipeline cost.** Dense models use more compute at ingest and search; sparse models are lighter and scale horizontally.

There is no one-size-fits-all processor. For the course bookstore, matching **book titles** — where you want exact and near-exact matches — is a natural fit for **hybrid** search (Chapter 3), which pairs a lexical/sparse signal with dense semantics.

> **Note (other processors).** A third processor, **`text_image_embedding`**, produces multimodal vectors from text *and* an image using a CLIP-style model — useful for "search by picture" but out of scope here (it needs a multimodal model and image inputs). OpenSearch 3.1+ also adds the **`semantic`** field type, which folds model inference into the mapping so you can skip a separate ingest pipeline; this workshop uses the explicit pipeline so the moving parts stay visible.

---

## Lesson 2-4 — AI model management with ML Commons

*Inspect the model lifecycle with the management APIs. (Teardown lives in the Cleanup section so fast-mode users don't delete the index before Lesson 2-5.)*

ML Commons manages the whole lifecycle — **register → deploy → infer → undeploy → delete** — inside the cluster. You have already registered, deployed, and run inference. These APIs let you observe and operate a running model.

### Step 14 — Inspect the model: metadata, profile, and stats

**Why**
Three read-only views of a running model. **Get** returns the registered metadata and current `model_state` (e.g. `DEPLOYED`), dimension, and group — the source of truth for what is loaded. The **Profile API** returns runtime data — which worker nodes host the model and per-request latency (min/max/avg, p50/p90/p99) — so you can confirm inference routing and see where time goes ([docs](https://docs.opensearch.org/latest/ml-commons-plugin/api/profile/)). **Stats** aggregates ML request counts and failures across nodes — a quick health check for the ML layer.

**Request** — model metadata:

```http
GET _plugins/_ml/models/YOUR_MODEL_ID
```

**Request** — runtime profile:

```http
GET _plugins/_ml/profile/models/YOUR_MODEL_ID
```

**Request** — cluster-wide ML stats:

```http
GET _plugins/_ml/stats
```

**Expected** Metadata with `model_state: "DEPLOYED"` and `model_config` (including `embedding_dimension: 768`); a `models` object with `worker_nodes` and `model_inference_stats` (empty is normal until the model has served at least one request — run Step 12 first); and per-node counters such as `ml_request_count`.

**Fast mode** `bruno/Chapter 2/19-get-model.bru` → `20-model-profile.bru` → `21-ml-stats.bru`

> **Why in-cluster management matters.** Because register/deploy/infer/undeploy all happen where your data lives, you avoid hosting, load-balancing, and monitoring an external model server. Inference stays low-latency and the whole lifecycle is a few REST calls. External/remote models (via connectors) follow the same lifecycle and are covered in Chapter 4.

---

## Lesson 2-5 — Optimizing neural search

*Neural search is powerful but demanding. Tune three layers — cluster, index, and query — for speed and cost.*

Run these against the live `vector-search-index` from Lesson 2-2.

### Cluster layer

**ANN indexing parallelism (teaching).** OpenSearch auto-scales ANN graph-build threads by CPU: clusters with **< 32 cores** default to **1** indexing thread; **≥ 32 cores** step up to **4**, so large instances build vector indexes faster. You can also set `knn.algo_param.index_thread_qty` explicitly, but the automatic default is usually right.

#### Step 15 — Set the k-NN memory circuit breaker

**Why**
The k-NN plugin holds ANN graphs in **native** memory (outside the JVM heap). Its circuit breaker caps that usage and evicts least-recently-used graphs before the node OOMs. Default is **50%** of the memory left after the heap. ([docs](https://docs.opensearch.org/latest/vector-search/settings/)) Setting it explicitly makes the guardrail visible; lower it on memory-tight nodes, raise it (carefully) on vector-heavy ones.

**Request**

```http
PUT _cluster/settings
{
  "persistent": {
    "knn.memory.circuit_breaker.enabled": true,
    "knn.memory.circuit_breaker.limit": "50%"
  }
}
```

**Expected** `acknowledged: true` with both keys echoed.

**Fast mode** `bruno/Chapter 2/22-knn-circuit-breaker-limit.bru`

**Shards & replicas (teaching).** Keep shard sizes **10–30 GiB** when search latency matters, **30–50 GiB** for write-heavy/log workloads. Over-sharding wastes CPU on metadata; under-sharding kills parallelism. Each **replica** can serve ANN queries in parallel (lower latency) but multiplies vector storage and graph size (higher cost). ANN graphs are expensive to move, so favor stable placement — see the routing note at the end of this lesson.

### Index layer

#### Step 16 — Raise the refresh interval, then force-merge

**Why**
Every refresh creates Lucene segments, and many small segments slow ANN traversal. During heavy ingest, raise `refresh_interval` (30s is common, or `-1` to disable) to cut segment churn, then **force-merge** afterward so the k-NN graph lives in fewer, larger segments.

**Request** — raise refresh interval:

```http
PUT vector-search-index/_settings
{
  "index.refresh_interval": "30s"
}
```

**Request** — after ingestion, consolidate segments:

```http
POST vector-search-index/_forcemerge?max_num_segments=1
```

**Expected** `acknowledged: true` for the settings update; `_shards.failed: 0` for the force-merge (it can take a while on large indexes).

**Fast mode** `bruno/Chapter 2/23-set-refresh-interval.bru`, then `24-force-merge.bru`.

> **Index modes & dimensionality (teaching).** OpenSearch supports **`in_memory`** (default — ANN graphs resident in native memory, fastest) and **`on_disk`** (introduced 2.17 — graphs offloaded with 32× compression + rescoring, far less RAM for large datasets). Mode is fixed at index creation. You already built and inspected an `on_disk` index in **Chapter 1 Step 6** (`vector-disk-demo`) — the mechanics are identical at production scale; only the `dimension` changes, so there is no need to create another demo index here.
>
> Higher vector **dimensionality** improves nuance but raises index size and query latency — choosing the embedding dimension (768 here) is one of the most consequential pipeline decisions. ([docs](https://docs.opensearch.org/latest/vector-search/optimizing-storage/disk-based-vector-search/))

### Query layer

> **ANN search breadth — `ef_search` (teaching).** `index.knn.algo_param.ef_search` is the size of the dynamic candidate list explored per query (default **100**). Higher = better recall, slower search; lower = faster, less accurate. It is a **dynamic** index setting — tune it live via `PUT vector-search-index/_settings` with no reindex ([docs](https://docs.opensearch.org/latest/vector-search/settings/)). Since 100 is already the default, there is nothing to change here.

#### Step 17 — Filter before vectors (metadata filtering)

**Why**
The single most effective query optimization: apply a metadata filter so ANN only scores a small, relevant subset instead of millions of vectors. The `neural` query accepts a `filter`; the Lucene/Faiss engines pick pre-filtering vs. efficient filtering during HNSW traversal automatically based on selectivity.

**Request**

```http
GET vector-search-index/_search
{
  "_source": { "excludes": ["passage_embedding"] },
  "query": {
    "neural": {
      "passage_embedding": {
        "query_text": "a tragic romance",
        "k": 10,
        "filter": {
          "term": { "bookshelves": "Category: Romance" }
        }
      }
    }
  }
}
```

**Expected** Only documents matching the filter are scored, then ranked by semantic similarity. On a large corpus this dramatically cuts latency. (If Step 11's default model isn't set, add `"model_id": "YOUR_MODEL_ID"`.)

**Fast mode** `bruno/Chapter 2/26-neural-search-filtered.bru`

> **Batching (teaching).** Applications that fire many tiny neural queries (autocomplete, chat-agent steps) can raise ingest throughput with the processor's `batch_size` (Step 7 Note) and reduce repeated graph traversal by batching requests — one traversal serves many inputs.

> **Stable shard routing (teaching).** Performance and resilience go together: routing settings (`cluster.routing.allocation.enable`, `cluster.routing.rebalance.enable`) decide when shards allocate and rebalance. For vector workloads, avoid unnecessary rebalancing — ANN graphs are costly to relocate, and movement during peak query or bulk ingest hurts latency. Both knobs default to `all`, which is correct for normal operation, so there is nothing to set here; operators flip `allocation.enable: none` before a rolling restart, then restore `all`. (Optional refinement: `cluster.routing.allocation.allow_rebalance: indices_all_active` rebalances only after all shards of an index are active.)


---

## Cleanup

Run this **last**, once you are done with the chapter. Order matters: delete the index and pipelines, then **undeploy before delete** on any model (the cluster refuses to delete a deployed model). **Skip the model deletes** if you are continuing to Chapter 3 — it reuses the dense model (`ML_MODEL_ID`) for its comparison step.

### C1 — Delete the search pipeline

```http
DELETE _search/pipeline/default-model-pipeline
```

**Fast mode** `bruno/Chapter 2/29-delete-search-pipeline.bru`

### C2 — Delete the vector index

```http
DELETE vector-search-index
```

A `404` is fine if already gone. **Fast mode** `bruno/Chapter 2/30-delete-vector-search-index.bru`

### C3 — Delete the ingest pipeline

```http
DELETE _ingest/pipeline/vector-search-embeddings-pipeline
```

**Fast mode** `bruno/Chapter 2/31-delete-ingest-pipeline.bru`

### C4 — Undeploy models

**Why** A deployed model holds node memory and cannot be deleted until undeployed.

```http
POST _plugins/_ml/models/YOUR_MODEL_ID/_undeploy
```

Poll `GET _plugins/_ml/tasks/YOUR_TASK_ID` until `state` is terminal. A `400` (not deployed) or `404` (missing) means undeploy isn't needed.

**Fast mode** `bruno/Chapter 2/32-undeploy-model.bru`, poll `34-poll-ml-task-undeploy.bru`.

### C5 — Delete models (optional)

```http
DELETE _plugins/_ml/models/YOUR_MODEL_ID
```

**Fast mode** `bruno/Chapter 2/35-delete-model.bru`

---

## What you learned

- The ML Commons lifecycle: **enable settings → model group → register → poll → deploy → poll → predict**.
- How the **`text_embedding`** processor and **`default_pipeline`** generate vectors automatically at ingest, and how **`neural_query_enricher`** sets a default query model.
- **Neural** (semantic) vs. **hybrid** neural + lexical queries, and the **dense vs. sparse** decision framework (Chapter 3 goes hands-on with sparse).
- Model management with **get / profile / stats**, and teardown with **undeploy → delete**.
- Optimizing every layer: circuit breaker, shard/replica strategy, `on_disk` mode, refresh interval + force-merge, `ef_search`, metadata filtering, and stable routing.

## Next chapter

[Chapter 3](../Chapter%203/README.md) — neural **sparse** encoding, sparse ingest pipelines, and the dedicated **`hybrid`** query with score normalization.
