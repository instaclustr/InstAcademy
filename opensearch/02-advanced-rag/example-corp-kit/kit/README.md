# Example Corp corpus generators

> **Maintainer-only.** Learners never run anything in this folder. The
> course ships a pre-built corpus at `../corpus/example-corp-corpus-v2.1.0/`,
> and every learner works from those exact bytes so results reproduce.
> These generators exist to rebuild that corpus, and they are the one
> place in the kit that needs `pip install requests`.

Everything needed to regenerate the Example Corp demo corpus for the
Advanced RAG with OpenSearch learning path: generate the five assets,
chunk them, and build a release.

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
2. Register and deploy an embedding model (see Chapter 1 of the course
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
