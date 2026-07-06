# Chapter 1 — Configuring and optimizing vector search

**Chapter 1 workshop** · [Vector Storage & Search for AI](../../README.md)

← [Course index](../../README.md) · [How to run labs](../../HANDS-ON-GUIDE.md) · **Next:** [Chapter 2](../Chapter%202/README.md)

This is the hands-on companion to Chapter 1 of the video course. Everything the
videos demonstrate — index settings, HNSW/IVF method parameters, exact k-NN,
disk-based and memory-optimized storage, chunking, shard sizing, and dimension
reduction — is turned into a request you can run yourself in **Dev Tools** (or
[Bruno fast mode](../../bruno/Chapter%201/)).

The chapter is one continuous workshop, organized into four sections that match
the lessons:

| Section | Lesson | What you build |
|---------|--------|----------------|
| [1-1](#lesson-1-1--vector-search-fundamentals-and-configuration) | Vector search fundamentals and configuration | A `knn_vector` index; inspect settings, shards, segments; disk-based + memory-optimized variants |
| [1-2](#lesson-1-2--choosing-the-right-type-of-vector-search) | Exact k-NN, HNSW, IVF | Run all three search methods on the same data and compare |
| [1-3](#lesson-1-3--gpus-vs-cpus-concept-checkpoint) | GPUs vs CPUs | Concept checkpoint + cluster inspection calls |
| [1-4](#lesson-1-4--vector-storage-and-search-optimizations) | Storage & search optimizations | Chunking, shard/ISM management, dimension reduction |

Work through the sections in order — later steps reuse earlier indexes. A
[cleanup section](#cleanup) at the end removes everything you created.

## How to read a step

Every step uses the same layout (see the [lab guide](../../HANDS-ON-GUIDE.md)):

- **Why** — the concept from the video, in plain language.
- **Request** — paste into **Dev Tools** (Dashboards → Dev Tools).
- **Expected** — what success looks like.
- **Save** — values you'll reuse later.
- **Fast mode** — the matching Bruno request in [`bruno/Chapter 1/`](../../bruno/Chapter%201/).

## Prerequisites

- A running **Instaclustr OpenSearch cluster** (3-node trial, **AI Search
  Plugin** enabled) reachable from your browser — see [cluster setup](../../CREATE_CLUSTER.md).
  Your IP must be on the firewall allow-list.
- **OpenSearch 2.19+ (targeted at 3.5+).** A few features used here
  (`mode: on_disk`, memory-optimized search) are newest in the 3.x line; each
  step notes its minimum version.
- **Dev Tools** open, or [Bruno](../../bruno/README.md) configured with
  `baseUrl`, `username`, `password`.
- Sample floating-point vectors used in these labs are tiny (8-dimensional) and
  ship as bulk files under [`rest/bulk/`](../../rest/bulk/) so you never type
  raw vectors by hand. Real embeddings arrive in Chapter 2.

> **Engine note (important for OpenSearch 3.x).** OpenSearch ships three vector
> engines: **`faiss`** (the **default**), **`lucene`**, and **`nmslib`**.
> `nmslib` is **deprecated** in favor of `faiss` and `lucene` — do not use it for
> new indexes. The Chapter 1 video mentions all three engines as equals; that was
> accurate for older releases, but for 3.5+ prefer `faiss` (used throughout this
> workshop) or `lucene`. Only `faiss` implements **IVF**; `lucene` adds smart
> filtering for smaller deployments.

---

## Lesson 1-1 — Vector search fundamentals and configuration

**Concept — vectors and embeddings.** A *vector* is a list of numbers describing
a point in multi-dimensional space by its direction and magnitude. It lets you
reason about non-numeric data (text, images, audio) numerically. A *vector
embedding* is one piece of real data after a machine-learning model has
translated it into that space — for example, one book's description turned into
768 floats. Each dimension captures a facet of the data (a naive color embedding
might use 3 dimensions for red/green/blue); higher dimensionality captures more
nuance at the cost of more storage and compute. OpenSearch stores embeddings in a
`knn_vector` field and searches them by distance.

**Concept — the cost/performance balance.** Tuning a vector index is always a
trade between **search performance** and **operational cost**, where cost breaks
down into three resources: **CPU, RAM, and storage**. Two structural knobs
dominate:

- **Shards** — more shards means smaller shards and more parallelism, but each
  shard adds coordination overhead. You'll size these in [Lesson 1-4](#step-16-shard-sizing-and-ism-rollover).
- **Segments** — Lucene stores each shard as a set of immutable segments. More
  segments means higher search latency, so merging segments is a core tuning
  lever (Step 5 below).

### Step 1: Verify cluster connectivity

**Why**  
Every later step assumes basic auth and TLS work. `GET /` returns the cluster
name and version — a five-second smoke test that saves hours of debugging bulk
or model errors later. It also confirms your engine version so you know which
features (like `on_disk` mode) are available.

**Request**

```http
GET /
```

**Expected**

```json
{
  "name": "...",
  "cluster_name": "...",
  "version": { "number": "3.x.x", "...": "..." },
  "tagline": "The OpenSearch Project: https://opensearch.org/"
}
```

`401 Unauthorized` → check username/password. A timeout → check that your IP is
on the Instaclustr firewall list.

**Save** — the `version.number`; a few steps note a minimum version.

**Fast mode** — `01-cluster-info.bru`

### Step 2: Create a vector index

**Why**  
`knn_vector` is the field type that stores embeddings. Three settings do the
heavy lifting:

- **`index.knn: true`** — turns on the k-NN data structures for the index. Without
  it you cannot run approximate `knn` queries.
- **`dimension`** — the exact length of every vector. It must match your
  embedding model; a mismatch fails at index time.
- **`method`** — the ANN algorithm and engine. Here `hnsw` on `faiss` (the
  default engine). `space_type` is the distance function (`l2` = Euclidean); it
  can sit at the top level of the field or inside `method`. The HNSW parameters
  **`m`** (links per node, default 16) and **`ef_construction`** (build-time
  candidate list, default 100) trade graph quality against build cost and memory.

**Request**

```http
PUT vector-fundamentals
{
  "settings": {
    "index": {
      "knn": true,
      "knn.algo_param.ef_search": 100
    }
  },
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "my_vector": {
        "type": "knn_vector",
        "dimension": 8,
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "parameters": {
            "m": 16,
            "ef_construction": 100
          }
        }
      }
    }
  }
}
```

**Expected**

```json
{ "acknowledged": true, "shards_acknowledged": true, "index": "vector-fundamentals" }
```

If it already exists from a previous run, `DELETE vector-fundamentals` first.

**Save** — index name `vector-fundamentals`.

**Fast mode** — `02-create-vector-index.bru`

### Step 3: Inspect the mapping and settings

**Why**  
Reading back the mapping confirms OpenSearch accepted your `knn_vector`
configuration and shows the effective defaults it filled in — useful when you
want to know exactly what `m`, `ef_construction`, and `space_type` your index is
actually using.

**Request**

```http
GET vector-fundamentals/_mapping
```

**Expected** — the `my_vector` field echoed back with `type: knn_vector`,
`dimension: 8`, and your `method` block.

**Fast mode** — `03-get-mapping.bru`

### Step 4: Index a few vectors

**Why**  
You need documents in the index before shards, segments, and search become
meaningful. The bulk API indexes many documents in one request as alternating
action/source lines (NDJSON). These three vectors are 8-dimensional so they're
readable.

**Request** — run the `POST _bulk` line, then paste the entire contents of
[`rest/bulk/chapter-1-lesson-1-vectors.ndjson`](../../rest/bulk/chapter-1-lesson-1-vectors.ndjson)
below it, ending with a blank line:

```http
POST _bulk
```

The file contains lines like:

```json
{"index": {"_index": "vector-fundamentals", "_id": "1"}}
{"title": "Intro to Vector Search", "my_vector": [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]}
```

**Expected** — `"errors": false` and three `"result": "created"` items.

**Fast mode** — `04-bulk-fundamentals.bru`

### Step 5: Inspect shards and segments, then force-merge

**Why**  
This is the "segment management" the video calls out. `_cat/shards` shows how the
index is distributed; `_cat/segments` shows the immutable Lucene segments inside
each shard. Because more segments means higher query latency, `_forcemerge`
collapses them — here down to one segment — which is a common optimization for
read-heavy indexes that are no longer being written. (Only force-merge indexes
that are done ingesting; it is expensive.)

**Request** — how the index is spread across nodes:

```http
GET _cat/shards/vector-fundamentals?v
```

**Request** — the segments inside the shard:

```http
GET _cat/segments/vector-fundamentals?v
```

**Request** — merge to a single segment:

```http
POST vector-fundamentals/_forcemerge?max_num_segments=1
```

**Expected** — `_cat/segments` after the merge shows a single row per shard.

**Fast mode** — `05-cat-shards.bru`, `06-cat-segments.bru`, `07-forcemerge.bru`

### Step 6: Disk-based (on_disk) storage

**Why**  
Disk-based vector search stores full-fidelity vectors on disk and keeps only a
compressed form in memory, cutting RAM cost while preserving strong recall
through a two-phase quantize-then-rescore search. You enable it with
**`mode: on_disk`** and tune the memory/recall trade with **`compression_level`**
(valid values `1x`, `2x`, `4x`, `8x`, `16x`, `32x`; `on_disk` defaults to `32x`).
The video calls the compression step *scalar quantization* — that is one of the
encoders OpenSearch uses under the hood — and notes recall is very high but not
perfectly exact. Requires OpenSearch 2.17+ and `float` vectors.

**Request**

```http
PUT vector-disk-demo
{
  "settings": { "index": { "knn": true } },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 8,
        "space_type": "l2",
        "mode": "on_disk",
        "compression_level": "16x"
      }
    }
  }
}
```

**Expected** — `"acknowledged": true`. Note we set only `mode` and
`compression_level`; OpenSearch chooses the `faiss` engine and a quantizing
encoder for you. (You cannot set both `compression_level` and a manual
`method.encoder`.)

**Fast mode** — `08-create-disk-index.bru`

### Step 7: Memory-optimized storage

**Why**  
Memory-optimized search is the other low-footprint option the video describes:
instead of loading the whole index into RAM, OpenSearch memory-maps the index
files and lets the operating system page vector data in and out on demand. This
is what you reach for when the index doesn't fit in memory or you want to shrink
the footprint and can accept slightly higher latency. In OpenSearch 3.1+ it is
activated by combining **`mode: on_disk`** with **`compression_level: 1x`** (i.e.
on-disk layout with no quantization).

**Request**

```http
PUT vector-memopt-demo
{
  "settings": { "index": { "knn": true } },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 8,
        "space_type": "l2",
        "mode": "on_disk",
        "compression_level": "1x"
      }
    }
  }
}
```

**Expected** — `"acknowledged": true`.

> **Trade-offs recap.** Across every setting here you are balancing **speed, cost,
> and accuracy**. In-memory HNSW is fastest but costs the most RAM; `on_disk` with
> compression trades a little recall for large memory savings; memory-optimized
> mapping trades latency for the ability to run on smaller nodes. Match the knob
> to your business priority (uptime, cost, scale), not to raw benchmark numbers.

**Fast mode** — `09-create-memopt-index.bru`

---

## Lesson 1-2 — Choosing the right type of vector search

**Concept — kNN vs aNN.** Two families of vector search:

- **Exact k-nearest-neighbor (kNN)** compares the query against *every* indexed
  vector. It has perfect recall but its cost grows linearly with the dataset, so
  it doesn't scale.
- **Approximate nearest neighbor (aNN)** still uses distance math, but a
  specialized data structure narrows the search to a small set of candidate
  vectors first — letting it search billions of vectors in milliseconds. The two
  aNN methods here are **HNSW** and **IVF**.
  - **HNSW (Hierarchical Navigable Small World)** builds a layered graph. Search
    starts at a sparse top layer, hops to the closest node, then descends into
    denser layers — like finding a book by narrowing from *Art* → *Modern art* →
    the exact title. Very fast and scales well, at a high memory cost.
  - **IVF (Inverted File Index)** uses k-means to cluster vectors around
    **centroids**. Each centroid owns a bucket (the "inverted file") of its
    vectors. A query only scans the buckets of the nearest centroids, so most
    vectors are skipped — fast even on huge datasets, with lower memory than
    HNSW, but it requires a **training** step first. IVF is `faiss`-only.

You'll run all three against the same 10 product vectors and compare.

### Step 8: Create the products index (HNSW)

**Why**  
This `faiss`/`hnsw` index is both the HNSW demo and the source of training data
for IVF later. The `category` keyword field lets us demonstrate filtered exact
search. We set `m` and `ef_construction` explicitly so you can see the knobs from
Lesson 1-1 in a realistic index.

**Request**

```http
PUT products-hnsw
{
  "settings": { "index": { "knn": true } },
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "category": { "type": "keyword" },
      "product_vector": {
        "type": "knn_vector",
        "dimension": 8,
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "parameters": { "m": 16, "ef_construction": 128 }
        }
      }
    }
  }
}
```

**Expected** — `"acknowledged": true`.

**Fast mode** — `10-create-products-hnsw.bru`

### Step 9: Bulk-index the product vectors

**Why**  
Ten small products (three rough clusters: electronics, books, outdoor) give the
search methods something to distinguish.

**Request** — run the line, then paste
[`rest/bulk/chapter-1-lesson-2-vectors.ndjson`](../../rest/bulk/chapter-1-lesson-2-vectors.ndjson),
ending with a blank line:

```http
POST _bulk
```

**Expected** — `"errors": false`, ten created items.

**Fast mode** — `11-bulk-products.bru`

### Step 10: Refresh

**Why**  
OpenSearch is near-real-time; a refresh makes the new documents immediately
searchable (and visible to `_reindex` later).

**Request**

```http
POST products-hnsw/_refresh
```

**Fast mode** — `12-refresh-products-hnsw.bru`

### Step 11: Exact k-NN with a scoring script

**Why**  
Exact kNN is done with a **scoring script**, not the `knn` query. The special
`knn_score` script (note `"lang": "knn"`) computes the true distance from the
query vector to every matched document — a brute-force scan with perfect recall.
Use it for small datasets where accuracy is non-negotiable. `space_type` is chosen
at query time here, and `query_value` must match the field's `dimension`.

**Request**

```http
GET products-hnsw/_search
{
  "size": 3,
  "query": {
    "script_score": {
      "query": { "match_all": {} },
      "script": {
        "source": "knn_score",
        "lang": "knn",
        "params": {
          "field": "product_vector",
          "query_value": [0.90, 0.90, 0.10, 0.10, 0.05, 0.05, 0.10, 0.10],
          "space_type": "l2"
        }
      }
    }
  }
}
```

**Expected** — the three electronics products (`Wireless Headphones`,
`Bluetooth Speaker`, `Smart Watch`) rank highest, because the query vector sits in
the electronics cluster.

**Fast mode** — `13-exact-knn-score-script.bru`

### Step 12: Exact k-NN with a pre-filter

**Why**  
The scoring-script approach shines when you need **heavy pre-filtering**: you
restrict the candidate set *first* with a normal query, then compute exact
distances only over what survives. Here we score exact distance only across the
`books` category. (Approximate `knn` queries filter differently and can return
fewer than `k` results after filtering; the scoring script avoids that.)

**Request**

```http
GET products-hnsw/_search
{
  "size": 3,
  "query": {
    "script_score": {
      "query": {
        "bool": { "filter": { "term": { "category": "books" } } }
      },
      "script": {
        "source": "knn_score",
        "lang": "knn",
        "params": {
          "field": "product_vector",
          "query_value": [0.10, 0.10, 0.90, 0.90, 0.10, 0.10, 0.10, 0.10],
          "space_type": "l2"
        }
      }
    }
  }
}
```

**Expected** — only `books` products are scored and returned; electronics and
outdoor are excluded by the filter.

**Fast mode** — `14-exact-knn-prefilter.bru`

### Step 13: Approximate search with HNSW

**Why**  
The `knn` query runs the approximate HNSW search you configured on the index — it
walks the graph instead of scanning every vector. `k` is how many neighbors to
return; `method_parameters.ef_search` widens the search list at query time
(higher = more accurate, slower). On this tiny dataset the results match exact
search, but on millions of vectors this is orders of magnitude faster.

**Request**

```http
GET products-hnsw/_search
{
  "size": 3,
  "query": {
    "knn": {
      "product_vector": {
        "vector": [0.90, 0.90, 0.10, 0.10, 0.05, 0.05, 0.10, 0.10],
        "k": 3,
        "method_parameters": { "ef_search": 100 }
      }
    }
  }
}
```

**Expected** — the same electronics products as Step 11, this time via the graph.

**Fast mode** — `15-hnsw-knn-query.bru`

### Step 14: Train an IVF model

**Why**  
IVF must learn its centroids before it can index anything, so you **train a
model** with the Train API. It reads vectors from an existing `knn_vector` field
(`products-hnsw`), clusters them into `nlist` buckets, and stores a reusable
model. `nprobes` (how many buckets to scan at query time) can be set now or per
query. Training needs at least `nlist` vectors; we use `nlist: 4` against 10
vectors. Training is asynchronous — the call returns immediately with a
`model_id`.

**Request**

```http
POST _plugins/_knn/models/_train
{
  "training_index": "products-hnsw",
  "training_field": "product_vector",
  "dimension": 8,
  "description": "IVF model for Chapter 1 products",
  "space_type": "l2",
  "method": {
    "name": "ivf",
    "engine": "faiss",
    "parameters": { "nlist": 4, "nprobes": 2 }
  }
}
```

**Expected**

```json
{ "model_id": "xxxxxxxxxxxxxxxxxx" }
```

**Save** — the returned `model_id`; the next three steps use it. In the requests
below, replace **`YOUR_MODEL_ID`** with this value.

**Fast mode** — `16-train-ivf-model.bru`

> **Known engine quirk (OpenSearch 3.5.0) — single-node only.** The Train API
> reads training vectors directly from the live `products-hnsw` segment's
> native/mmap vector storage. On a single-node Docker 3.5.0 setup this can leave
> that index's segment reader in a bad state immediately afterward — searches or
> `_reindex` reads against `products-hnsw` fail with
> `search_phase_execution_exception` / `already_closed_exception:
> ... MemorySegmentIndexInput ...`. If you hit this after training, it is not a
> mistake in your request: `POST products-hnsw/_close` then `POST
> products-hnsw/_open` reopens the segment readers and resolves it. **Verified
> not to reproduce on a real 3-node Instaclustr cluster** (3 data/ingest/ml nodes
> + 3 dedicated managers, OpenSearch 3.5.0, `products-hnsw` with 1 replica): the
> train → poll → search/`GET _doc` (x8) → reindex → IVF query sequence ran back
> to back with zero errors, no close/reopen needed. If you're on a multi-node
> cluster and still see this, it is a genuine anomaly worth investigating rather
> than an expected quirk.

### Step 15: Poll the model until it's ready

**Why**  
Training runs in the background. Poll the model until its `state` is `created`
(from `training`); only then can an index use it.

**Request**

```http
GET _plugins/_knn/models/YOUR_MODEL_ID?filter_path=state,error
```

**Expected**

```json
{ "state": "created" }
```

If `state` is `failed`, the `error` field explains why (most often too few
training vectors for `nlist`).

**Fast mode** — `17-poll-ivf-model.bru`

### Step 16: Create the IVF index from the model

**Why**  
An IVF-backed field references the trained model with **`model_id`** instead of a
`method` block — the model already carries the dimension, engine, and centroids.

**Request**

```http
PUT products-ivf
{
  "settings": { "index": { "knn": true } },
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "category": { "type": "keyword" },
      "product_vector": {
        "type": "knn_vector",
        "model_id": "YOUR_MODEL_ID"
      }
    }
  }
}
```

**Expected** — `"acknowledged": true`.

**Fast mode** — `18-create-products-ivf.bru`

### Step 17: Copy the data into the IVF index

**Why**  
`_reindex` copies every document from `products-hnsw` into `products-ivf`
server-side; as each vector lands it is assigned to its nearest IVF centroid.

**Request**

```http
POST _reindex?wait_for_completion=true
{
  "source": { "index": "products-hnsw" },
  "dest": { "index": "products-ivf" }
}
```

**Expected** — `"total": 10, "created": 10, "failures": []`. Then refresh:

```http
POST products-ivf/_refresh
```

**Fast mode** — `19-reindex-to-ivf.bru`, `20-refresh-products-ivf.bru`

### Step 18: Search the IVF index

**Why**  
The same `knn` query now runs against IVF. `method_parameters.nprobes` controls
how many centroid buckets are scanned — raise it for better recall, lower it for
speed. Because most buckets are skipped, IVF stays fast on very large datasets
while using less memory than HNSW.

**Request**

```http
GET products-ivf/_search
{
  "size": 3,
  "query": {
    "knn": {
      "product_vector": {
        "vector": [0.90, 0.90, 0.10, 0.10, 0.05, 0.05, 0.10, 0.10],
        "k": 3,
        "method_parameters": { "nprobes": 4 }
      }
    }
  }
}
```

**Expected** — electronics products rank highest again, retrieved through IVF
buckets.

**Fast mode** — `21-ivf-knn-query.bru`

### Decision framework

You cannot maximize **performance**, **resource cost**, and **operational cost**
all at once — pick two, and the method follows:

| Method | Accuracy | Speed at scale | Memory | Training | Best for |
|--------|----------|----------------|--------|----------|----------|
| **Exact k-NN** (scoring script) | Perfect | Poor (linear) | Low | None | Small datasets; accuracy non-negotiable; heavy pre-filtering |
| **HNSW** (`faiss`/`lucene`) | High | Excellent | High | None | Low-latency search on large datasets where RAM is available |
| **IVF** (`faiss` only) | High | Excellent | Lower than HNSW | Required | Very large datasets with constrained memory; can absorb training overhead |

---

## Lesson 1-3 — GPUs vs CPUs (concept checkpoint)

This lesson in the video is a decision framework, not a build — a managed
Instaclustr trial cluster has no GPUs, and GPU acceleration in OpenSearch applies
to **index building** (especially building large HNSW graphs), not to serving
queries. Below is the framework plus a few inspection calls so you can reason
about your own cluster's compute.

**The framework.**

- **Why GPUs.** CPUs are versatile and handle work sequentially; GPUs run massively
  parallel, which suits the dense linear algebra of building vector indexes. GPU
  acceleration can cut index-build time for hundreds of millions to billions of
  vectors from **days to hours**. Search queries still run on CPU but benefit from
  the faster-built index.
- **Why CPUs are often enough.** Modern CPUs include **SIMD** (Single Instruction,
  Multiple Data) units; OpenSearch uses SIMD in the `faiss` engine (AVX2/AVX-512
  on x86, Neon on ARM) to speed up distance math. For smaller datasets or
  infrequent rebuilds, CPU indexing is cheaper and simpler.
- **The real cost of GPUs.** Beyond hardware price, GPUs carry heavy operational
  overhead: specialized drivers, libraries, and expertise.
- **Rule of thumb.** Reach for GPU acceleration when rebuilding indexes *at scale*
  or iterating rapidly on index configuration. Otherwise CPU is the reliable,
  cost-effective default. It's "right tool for the job," not "GPU good, CPU bad."

### Step 19: Confirm the k-NN plugin is installed

**Why**  
Vector search depends on the k-NN plugin. This lists installed plugins per node so
you can confirm `opensearch-knn` (which bundles the `faiss` engine and its SIMD
libraries) is present.

**Request**

```http
GET _cat/plugins?v
```

**Expected** — a row containing `opensearch-knn` on each node.

**Fast mode** — `22-cat-plugins.bru`

### Step 20: Inspect node CPU

**Why**  
GPU-vs-CPU decisions start with knowing your CPU capacity. This returns the
available processor count per node, which bounds how much parallelism your
CPU-based index builds and SIMD-accelerated searches can use.

**Request**

```http
GET _nodes/os?filter_path=nodes.*.os.available_processors,nodes.*.os.name
```

**Expected** — `available_processors` for each node.

**Fast mode** — `23-nodes-os.bru`

### Step 21: Inspect k-NN engine statistics

**Why**  
The k-NN stats endpoint reports graph-build and query activity (cache hits, graph
memory, script compilations). It's how you observe whether index building — the
part GPUs would accelerate — is a bottleneck on your CPU cluster.

**Request**

```http
GET _plugins/_knn/stats?pretty
```

**Expected** — a JSON body of counters such as `graph_memory_usage`,
`knn_query_requests`, and `script_compilations`.

**Fast mode** — `24-knn-stats.bru`

---

## Lesson 1-4 — Vector storage and search optimizations

Three techniques that keep large vector deployments fast and affordable:
**chunking**, **shard management (ISM)**, and **dimension reduction**.

### Chunking

**Concept.** Embedding models have strict token limits (many popular models
handle ~512 tokens, roughly 1,000–1,200 characters). Feed them a document that's
too long and they silently **truncate** it, losing context and producing a poor
embedding. **Chunking** splits a long document into smaller pieces, embeds each
piece separately, and stores each chunk as its own document linked back to the
parent. Benefits: every chunk fits the model (better embeddings) and smaller
chunks give sharper semantic matches. Costs: more chunks means more embeddings
means more storage, and you often reassemble the parent context at retrieval time.

### Step 22: Create a chunked index

**Why**  
The chunk data model is one document per chunk, each carrying its own
`chunk_vector`, the `chunk_text`, and a `parent_id` (keyword) that ties chunks of
the same source document together so you can regroup them after retrieval.

**Request**

```http
PUT kb-chunks
{
  "settings": { "index": { "knn": true } },
  "mappings": {
    "properties": {
      "parent_id": { "type": "keyword" },
      "chunk_text": { "type": "text" },
      "chunk_vector": {
        "type": "knn_vector",
        "dimension": 8,
        "space_type": "l2",
        "method": { "name": "hnsw", "engine": "faiss" }
      }
    }
  }
}
```

**Expected** — `"acknowledged": true`.

**Fast mode** — `25-create-kb-chunks.bru`

### Step 23: Bulk-index the chunks

**Why**  
Two knowledge-base articles are split into five chunks total. In a real pipeline a
chunker produces these pieces and an embedding model (Chapter 2) fills each
`chunk_vector`.

**Request** — run the line, then paste
[`rest/bulk/chapter-1-lesson-4-chunks.ndjson`](../../rest/bulk/chapter-1-lesson-4-chunks.ndjson),
ending with a blank line:

```http
POST _bulk
```

Then refresh:

```http
POST kb-chunks/_refresh
```

**Expected** — `"errors": false`, five created items.

**Fast mode** — `26-bulk-chunks.bru`, `27-refresh-kb-chunks.bru`

### Step 24: Retrieve chunks, then regroup by parent

**Why**  
A vector query returns individual chunks; the parent article is reassembled
afterward. First retrieve the nearest chunks, then use a `terms` aggregation on
`parent_id` to see which source documents the best chunks came from — the
"post-processing to reassemble context" the video describes.

**Request** — nearest chunks:

```http
GET kb-chunks/_search
{
  "size": 3,
  "_source": ["parent_id", "chunk_text"],
  "query": {
    "knn": {
      "chunk_vector": {
        "vector": [0.88, 0.12, 0.12, 0.10, 0.10, 0.10, 0.11, 0.10],
        "k": 3
      }
    }
  }
}
```

**Request** — regroup the matches by source document:

```http
GET kb-chunks/_search
{
  "size": 0,
  "query": {
    "knn": {
      "chunk_vector": {
        "vector": [0.88, 0.12, 0.12, 0.10, 0.10, 0.10, 0.11, 0.10],
        "k": 5
      }
    }
  },
  "aggs": {
    "by_parent": { "terms": { "field": "parent_id" } }
  }
}
```

**Expected** — the router-setup chunks (`kb1`) rank highest, and the aggregation
buckets group hits under `kb1` / `kb2`.

**Fast mode** — `28-search-chunks.bru`, `29-aggregate-by-parent.bru`

### Step 25: Shard sizing and ISM rollover

**Why**  
Shard sizing is a balance: **smaller shards** parallelize better but add
coordination overhead when there are too many; **larger shards** reduce overhead
but raise per-query latency because each search scans more data. For data that
grows continuously (logs, events), **Index State Management (ISM)** policies
automate rollover — starting a fresh index once the current one hits a size or age
threshold — so shards never grow unbounded. This policy rolls an index over at 10
GB or 1 day.

**Request**

```http
PUT _plugins/_ism/policies/vector-rollover-policy
{
  "policy": {
    "description": "Roll vector indexes over by size or age to keep shards healthy",
    "default_state": "hot",
    "states": [
      {
        "name": "hot",
        "actions": [
          { "rollover": { "min_size": "10gb", "min_index_age": "1d" } }
        ],
        "transitions": []
      }
    ],
    "ism_template": [
      { "index_patterns": ["vector-logs-*"], "priority": 100 }
    ]
  }
}
```

**Expected** — a `_id` of `vector-rollover-policy` and `_version` in the response.
The `ism_template` auto-applies the policy to any future `vector-logs-*` index (no
such index exists in this lab, so nothing rolls over yet — this step shows how the
policy is defined).

**Fast mode** — `30-create-ism-policy.bru`

### Dimension reduction

**Concept.** Vector dimensionality drives both storage and search cost —
lower-dimension vectors are cheaper to store and faster to search, at some
accuracy cost. There are two ways to reduce dimensions:

- **In-place reduction** — reindex within the same index. Fast, but risky because
  you're mutating the index your application reads from.
- **Rebuild in a new index** — create a new, smaller-dimension index and remap the
  data into it. Safer, easy to roll back, and the recommended approach — which is
  exactly what the next steps do (256 → 128 dimensions).

### Step 26: Create the source vector index (256-dim)

**Why**  
A 256-dimensional `faiss`/`hnsw` index stands in for a production embedding index.

**Request**

```http
PUT my-vector-index
{
  "settings": { "index": { "knn": true } },
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "my_vector": {
        "type": "knn_vector",
        "dimension": 256,
        "space_type": "l2",
        "method": { "name": "hnsw", "engine": "faiss" }
      }
    }
  }
}
```

**Expected** — `"acknowledged": true`.

**Fast mode** — `31-create-source-256.bru`

### Step 27: Bulk-index the 256-dim vectors

**Why**  
Vectors are large, so use the pre-generated bulk file rather than typing 256
floats per document.

**Request** — run the line, then paste
[`rest/bulk/chapter-1-lesson-4-vector-index.ndjson`](../../rest/bulk/chapter-1-lesson-4-vector-index.ndjson),
ending with a blank line:

```http
POST _bulk
```

Then refresh:

```http
POST my-vector-index/_refresh
```

**Expected** — `"errors": false`, three created items.

**Fast mode** — `32-bulk-source-256.bru`, `33-refresh-source-256.bru`

### Step 28: Create the destination index (128-dim)

**Why**  
Halving the dimension roughly halves the per-vector memory and the HNSW graph
footprint. This is the smaller "rebuild" target.

**Request**

```http
PUT my-optimized-vector-index
{
  "settings": { "index": { "knn": true } },
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "my_vector": {
        "type": "knn_vector",
        "dimension": 128,
        "space_type": "l2",
        "method": { "name": "hnsw", "engine": "faiss" }
      }
    }
  }
}
```

**Expected** — `"acknowledged": true`.

**Fast mode** — `34-create-dest-128.bru`

### Step 29: Reindex with Painless truncation

**Why**  
`_reindex` copies each document server-side and a **Painless** script transforms it
in flight. `subList(0, 128)` keeps the first 128 elements of each vector — a
simple truncation from 256 to 128 dimensions. The destination mapping's
`dimension` must match, or indexing fails. (Truncation is the simplest reduction;
real pipelines might instead re-embed with a smaller model or apply PCA.)

**Request**

```http
POST _reindex?wait_for_completion=true
{
  "source": { "index": "my-vector-index" },
  "dest": { "index": "my-optimized-vector-index" },
  "script": {
    "source": "ctx._source.my_vector = ctx._source.my_vector.subList(0, 128);",
    "lang": "painless"
  }
}
```

**Expected**

```json
{ "total": 3, "created": 3, "updated": 0, "failures": [] }
```

`_reindex` does **not** refresh the destination index for you. Refresh before
verifying, or a search run immediately after can come back empty even though the
documents were created (near-real-time visibility, not a failure):

```http
POST my-optimized-vector-index/_refresh
```

**Request** — confirm the documents landed:

```http
GET my-optimized-vector-index/_search
{ "size": 3, "_source": ["title"] }
```

**Fast mode** — `35-reindex-truncate.bru`, `36-refresh-dest.bru`, `37-verify-dest.bru`

### Real-world scenarios (recap)

- **Customer support search** — chunk long troubleshooting guides so each step
  becomes its own embedding; the assistant stops missing steps.
- **E-commerce semantic search** — reduce embeddings from 768 to 384 dimensions
  to cut vector storage nearly in half with minimal accuracy loss.
- **Logging & observability** — right-size shards and let ISM roll over old
  indices so nodes never get overloaded.
- **RAG with fast turnaround** — smaller dimensions speed retrieval; chunking
  feeds the LLM the most relevant snippets.

---

## Cleanup

Remove everything this workshop created so you start Chapter 2 clean.

**Request** — delete all lab indexes in one call:

```http
DELETE vector-fundamentals,vector-disk-demo,vector-memopt-demo,products-hnsw,products-ivf,kb-chunks,my-vector-index,my-optimized-vector-index
```

**Request** — delete the ISM policy:

```http
DELETE _plugins/_ism/policies/vector-rollover-policy
```

**Request** — delete the trained IVF model (replace `YOUR_MODEL_ID`; a model must
be unused by any index before it can be deleted):

```http
DELETE _plugins/_knn/models/YOUR_MODEL_ID
```

**Fast mode** — `38-cleanup-indexes.bru`, `39-delete-ism-policy.bru`,
`40-delete-ivf-model.bru`

---

## What you learned

- How `knn_vector`, `index.knn`, `dimension`, `space_type`, and the HNSW `m` /
  `ef_construction` / `ef_search` parameters shape a vector index.
- How to inspect shards and segments and force-merge for lower query latency.
- How `mode: on_disk` + `compression_level` (disk-based) and memory-optimized
  mapping cut memory cost.
- How to run **exact k-NN** (scoring script), **HNSW**, and **IVF** (train +
  model) search, and how to choose between them.
- The GPU-vs-CPU decision framework and how to inspect your cluster's compute.
- How chunking, ISM-based shard management, and dimension reduction optimize
  storage and search at scale.

## Reference scripts

Optional Python equivalents live alongside this README (they mirror the same REST
calls once you've run the Dev Tools steps). They read connection settings from
`src/.env` (copy from `src/.env.example`).

| Script | Mirrors |
|--------|---------|
| `01-opensearch-status.py` | Step 1 — connectivity (`GET /`) |
| `02-data-loader.py` | Downloads the shared Gutendex dataset used from Chapter 2 on |
| `03-create-vector-index.py` | Steps 2, 6, 7 — HNSW, on_disk, and memory-optimized indexes |
| `04-dimension-reduction.py` | Steps 26–29 — 256→128 reindex with Painless |

## Next chapter

[Chapter 2](../Chapter%202/README.md) — register a real embedding model and build a
neural search pipeline.
