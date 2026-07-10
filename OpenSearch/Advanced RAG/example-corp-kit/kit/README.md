# Example Corp Data Kit

Everything needed to generate the Example Corp demo corpus for the
Advanced RAG with OpenSearch learning path, chunk it, load it into
OpenSearch 3.6+, and evaluate retrieval quality on camera.

## What gets generated

| Asset | File(s) | Course outline mapping |
| --- | --- | --- |
| Product documentation | `output/docs/*.md` (400 pages, scalable) | 8,000+ pages of product docs |
| Integration guides | `output/integration_guides/*.md` (50) | 50+ integration guides |
| Ticket history | `output/tickets.jsonl` (5,000, scalable to 200k) | 3 years, 200k+ tickets |
| Known issues DB | `output/known_issues.jsonl` | Known issues and workarounds |
| API reference | `output/api_reference/*.md` + `openapi-lite.json` | API reference documentation |
| Chunks | `output/chunks.jsonl` | Lesson 1.3 parent-child output |
| Golden query set | `output/golden_set.jsonl` (200 labeled queries) | Lesson 1.3 evaluation |

Everything is deterministic under `--seed 42` and internally consistent:
error codes, versions, and integrations line up across all five assets,
so a ticket about ERR-2209 always resolves to the same known issue,
Snowflake guide, and docs pages. Those links generate the golden set
labels for free.

## Distribution model: build once, share the batch

Learners do not run the generators. The course maintainer builds one
canonical batch and distributes it, so every learner ingests
byte-identical data and every eval number matches the videos.

Maintainer (once per corpus version):

```bash
cd generators
python build_release.py --version 1.0.0
# -> dist/example-corp-corpus-v1.0.0.tar.gz (checksummed, ~0.6 MB)
```

Learner (in the labs):

```bash
tar xzf example-corp-corpus-v1.0.0.tar.gz
python generators/verify_corpus.py --corpus example-corp-corpus-v1.0.0
python generators/ingest_opensearch.py --model-id <MODEL_ID> \
  --dimension 384 --chunks example-corp-corpus-v1.0.0/chunks.jsonl
```

verify_corpus.py checks every file against the sha256 manifest and
refuses mismatches, so "it works on my corpus" cannot happen. Two rules
keep results consistent course-wide: never regenerate locally (any
generator edit is a new corpus version, bump --version and redistribute),
and standardize the embedding model
(huggingface/sentence-transformers/all-MiniLM-L6-v2, 384 dims), because
neural and hybrid metrics depend on the model as much as the data.
Generation remains deterministic under seed 42, verified byte-identical
across rebuilds, so a lost batch can always be rebuilt exactly.

## Quick start

```bash
cd generators
python generate_docs.py --pages 400
python generate_integration_guides.py
python generate_known_issues.py
python generate_api_reference.py
python generate_tickets.py --count 5000
python chunk_documents.py
python generate_golden_set.py --count 200
```

Scale up for the full-size demo: `--pages 8000` and `--count 200000`.

## Load into OpenSearch (Instaclustr Managed Platform, 3.6+)

1. Enable the AI Search plugin on the cluster.
2. Register and deploy an embedding model (see `code-samples/lesson-1-4.md`
   for the connector and model group calls). Note the model_id and
   its dimension.
3. Load:

```bash
export OS_URL=https://user:pass@your-cluster:9200
python generators/ingest_opensearch.py --model-id <MODEL_ID> --dimension 384
```

This creates the `support-embed` ingest pipeline, the
`support-docs-v1` index (knn_vector, Faiss HNSW) behind the
`support-docs` alias, and both hybrid search pipelines
(`support-hybrid-rrf` and `support-hybrid-weighted`).

## Evaluate

```bash
python generators/eval_retrieval.py --mode bm25 --k 5
python generators/eval_retrieval.py --mode neural --k 5 --model-id <ID>
python generators/eval_retrieval.py --mode hybrid --k 5 --model-id <ID> \
  --search-pipeline support-hybrid-rrf
```

Prints hit rate@k, precision@k, and MRR. Running all three back to back
is the on-screen ablation for lesson 1.3.

## Code map: every course section to its code

| Section | Code samples | Runnable scripts |
| --- | --- | --- |
| 1.1 OpenSearch as a RAG Engine | code-samples/lesson-1-1.md | eval_retrieval.py (ef_search sweep) |
| 1.2 Building the RAG Pipeline | code-samples/lesson-1-2.md | eval_retrieval.py (RRF vs weighted) |
| 1.3 Chunking, Ingestion & Quality | code-samples/lesson-1-3.md | chunk_documents.py, generate_golden_set.py, eval_retrieval.py |
| 1.4 Connectors, Ingest & Updates | code-samples/lesson-1-4.md | ingest_opensearch.py |
| 2.1 The Conversation Problem | code-samples/lesson-2-1.md | (skip-logic + rewrite prompt inline) |
| 2.2 Memory & Token Management | code-samples/lesson-2-2.md | (ISM policy + Memory API inline) |
| 2.3 Query Enhancement Patterns | code-samples/lesson-2-3.md | (HyDE, _msearch, router inline) |
| 3.1 Retrieval Diagnostics | code-samples/lesson-3-1-and-3-2.md | correction_loop.py (score_shape) |
| 3.2 The Correction Loop | code-samples/lesson-3-1-and-3-2.md | correction_loop.py |
| 3.3 Evaluation & Observability | code-samples/lesson-3-3.md | (traces mapping, RAGAS, feedback labels) |
| 4.1 Routing & ReAct | code-samples/lesson-4-1.md | (router, route cache, tool descriptions) |
| 4.2 Multi-Index Agents | code-samples/lesson-4-2-and-4-3.md | split_indexes.py |
| 4.3 Guardrails & Production | code-samples/lesson-4-2-and-4-3.md | (ceilings, CRAG wrapper, semantic cache) |
| 5.1 / 5.2 Conclusion | decision content only, no code | |

The chapter 3 on-camera demo:

```bash
python generators/correction_loop.py --query "how do I fix ERR-2209" \
  --customer-version 4.8
```

runs the version mismatch case end to end: score gate, metadata grading
catching the 5.0-only fix, reformulation with a version filter, retry
against the ticket history, and honest low-confidence signaling when the
budget is spent. The chapter 4 index split:

```bash
python generators/split_indexes.py --model-id <MODEL_ID> --dimension 384
```

## Reusing the corpus in later chapters

The taxonomy was designed so later chapters need zero new data:

- Chapter 2 (memory): follow-up questions reuse error codes and features
  ("what about on version 4.9?" resolves against `product_version`).
- Chapter 3 (corrective): the version mismatch failure case is built in.
  ERR-2209 is fixed in 5.0; retrieving the 5.x fix for a 4.8 customer is
  the canonical low-confidence correction demo.
- Chapter 4 (agentic): the four support indexes are the four asset
  families (docs+guides, tickets, known issues, API reference); split
  `chunks.jsonl` by `doc_type` to create them.
