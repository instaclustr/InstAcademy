# Chapter 3 — Mastering hybrid search in OpenSearch

**InstAcademy → OpenSearch:** [Optimizing OpenSearch Vector Storage and Search for Faster AI Applications](../../) — Chapter 3

| Navigate | Link |
|----------|------|
| **Course home** | [README.md](../../README.md) |
| **Hands-on guide** | [docs/HANDS-ON-GUIDE.md](../../docs/HANDS-ON-GUIDE.md) |
| **OpenSearch courses** | [OpenSearch/](../../../) |
| **InstAcademy home** | [InstAcademy/](../../../../) |

Combine **lexical (BM25)** and **neural sparse** retrieval: sparse model, chunking ingest pipeline, search pipeline normalization, and hybrid queries on `my-sparse-neural-index`.

## Overview

### Goals

- Register and deploy the neural sparse encoding model
- Build sparse index + ingest pipeline with chunking
- Run hybrid search with score normalization

### Prerequisites

- [Chapter 1 Lesson 1](../Chapter%201/1-1/README.md) — `src/sample-data.json`
- [Chapter 2 Lesson 1](../Chapter%202/Lesson%201/README.md) — ML Commons basics (reuse `huggingface-models` group if it exists)
- Cluster with ML Commons and neural sparse / AI search enabled

### Course lesson map

- **3-1** — Why hybrid search; score-scale problem → Steps 4 and 9 in Lesson 1
- **3-2** — Build sparse hybrid end to end → Steps 1–8 in Lesson 1
- **3-3** — Normalization weights → Steps 4 and 9 in Lesson 1

## Lab

**[Lesson 1](Lesson%201/README.md)** — full hands-on (Dev Tools step by step)

**Fast mode:** [bruno/Chapter 3/Lesson 1/](../../bruno/Chapter%203/Lesson%201/)

## Next

[Chapter 4](../Chapter%204/README.md) — bookstore RAG optimization
