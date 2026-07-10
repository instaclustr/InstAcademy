# Example Corp Data Kit & Labs

Everything for the hands-on side of the "Advanced RAG with OpenSearch"
learning path: the canonical Example Corp demo corpus, five copy-paste
labs (one per chapter), the loader/eval scripts they call, and the
maintainer tooling that generates it all.

## Layout

```
README.md            this file
CLAUDE.md            validation-run instructions (for automated testing)
TEST_SPEC.md         the validation spec (infra phases + lab pedagogy)
TEST_REPORT.md       latest validation results (checkpoints, eval numbers)
corpus/
  example-corp-corpus-v2.1.0.tar.gz   the canonical batch every learner uses
labs/
  lab-0-setup.md         environment, corpus verify, model deploy
  lab-1-simple-rag.md    Chapter 1: ingest, hybrid retrieval, eval + tuning
  lab-2-memory.md        Chapter 2: conversations, rewriting, HyDE, _msearch, ISM
  lab-3-corrective.md    Chapter 3: score shapes, _explain, correction loop, traces
  lab-4-agentic.md       Chapter 4: index split, ReAct by hand, caches, guardrails
scripts/                 stdlib-only Python the labs invoke (no pip installs)
  verify_corpus.py       checksum-verify the extracted corpus
  ingest_chunks.py       Lab 1 bulk loader (batches, backpressure, resumable)
  eval_retrieval.py      Lab 1 ablation: hit rate@k / precision@k / MRR
  correction_loop.py     Lab 3 corrective RAG demo (no LLM required)
  split_chunks.py        Lab 4 per-family loader
kit/
  code-samples/          per-lesson request bodies for the course videos
  generators/            maintainer-only corpus generators (requires `requests`)
```

## Design rules the labs follow

- **Copy-paste first.** Every cluster interaction a learner performs is
  a `curl` (or a script invocation) pasted from the lab markdown, with
  what/why/expected-result stated at each step. No hidden setup.
- **Two paths, one course.** The primary path connects a real LLM
  (Gemini free tier, via an ML Commons connector created in Lab 0 Step
  6) so rewriting, HyDE, grading, and full RAG answers run against a
  live model; those steps carry a variance caveat and behavioral (not
  verbatim) checkpoints. Every LLM step also has a marked **No-LLM
  alternative** where the learner performs the model's job by hand
  with validated text, keeping the whole course runnable with zero API
  keys. Either way there are no pip installs: the embedding model
  (`all-MiniLM-L6-v2`, 384 dims) runs inside the cluster, and scripts
  use only the Python standard library.
- **One prefix.** Every cluster resource the course creates is named
  `support-*` (indexes, aliases, ingest/search pipelines, ISM policy),
  so cleanup is one wildcard and collisions are impossible.
- **Same data, same model, same numbers.** Learners verify the corpus
  against a sha256 manifest before ingesting and never regenerate
  locally. Embedding vectors are bit-identical for every learner; eval
  metrics reproduce within ~0.02 per cell (BM25 score ties and HNSW
  graph construction vary with ingest history), with the strategy
  ordering and the tuning win reproducing every time.

## What is in the corpus (canonical batch v2.1.0)

| Asset | Count | Course mapping |
| --- | --- | --- |
| Product docs pages | 1,000 | "8,000+ pages of product docs" |
| Integration guides | 50 | "50+ integration guides" |
| Ticket history | 10,000 (4,000 indexed as chunks) | "3 years, 200k+ tickets" |
| Known issues DB | 15 | known issues and workarounds |
| API reference | 14 pages | API reference |
| Chunks (parent-child) | 8,955 | lesson 1.3 output |
| Golden query set | 300 labeled queries | lesson 1.3 evaluation |

Counts are demo scale on purpose: full-scale ingest on a shared
cluster would be impolite, and nothing pedagogical changes. Everything
is deterministic under `--seed 42` and internally consistent: ERR-2209
resolves to the same known issue, guides, and docs pages across all
five assets, which is what makes the golden set labels free and the
chapter 3 version mismatch case reproducible.

## Cluster prerequisites

OpenSearch 3.1+ (course targets 3.6+) with the k-NN, ML Commons,
neural-search, and index-management plugins (the Instaclustr Managed
Platform AI Search add-on covers this), and at least one ML-capable
node. Validated end to end on OpenSearch 3.5.0 (3 data/ML nodes,
medium size); see TEST_REPORT.md.

## Maintainer: rebuilding the corpus

Learners never do this. Any generator change is a new corpus version:

```bash
cd kit/generators
python build_release.py --version <NEW_VERSION>
```

builds, checksums, and verifies reproducibility. Re-validate the labs
(TEST_SPEC.md) before distributing a new batch, then update the version
string everywhere it appears in `labs/` and `scripts/`.

## Code map: course sections to kit code

| Section | Code samples | Lab |
| --- | --- | --- |
| 1.1 OpenSearch as a RAG Engine | code-samples/lesson-1-1.md | Lab 1 Parts B |
| 1.2 Building the RAG Pipeline | code-samples/lesson-1-2.md | Lab 1 Parts B-C |
| 1.3 Chunking, Ingestion & Quality | code-samples/lesson-1-3.md | Lab 1 Parts A, D |
| 1.4 Connectors, Ingest & Updates | code-samples/lesson-1-4.md | Lab 0, Lab 1 Part A |
| 2.1 The Conversation Problem | code-samples/lesson-2-1.md | Lab 2 Steps 1-5 |
| 2.2 Memory & Token Management | code-samples/lesson-2-2.md | Lab 2 Steps 8-9 |
| 2.3 Query Enhancement Patterns | code-samples/lesson-2-3.md | Lab 2 Steps 6-7 |
| 3.1 Retrieval Diagnostics | code-samples/lesson-3-1-and-3-2.md | Lab 3 Steps 2-3 |
| 3.2 The Correction Loop | code-samples/lesson-3-1-and-3-2.md | Lab 3 Step 4 |
| 3.3 Evaluation & Observability | code-samples/lesson-3-3.md | Lab 3 Step 5 |
| 4.1 Routing & ReAct | code-samples/lesson-4-1.md | Lab 4 Steps 4, 6 |
| 4.2 Multi-Index Agents | code-samples/lesson-4-2-and-4-3.md | Lab 4 Steps 1-3, 5 |
| 4.3 Guardrails & Production | code-samples/lesson-4-2-and-4-3.md | Lab 4 Steps 7-8 |
| 5.1 / 5.2 Conclusion | decision content only, no code | |
