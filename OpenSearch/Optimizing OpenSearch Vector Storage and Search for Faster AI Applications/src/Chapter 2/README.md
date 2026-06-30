# Chapter 2 — Building neural search pipelines

**InstAcademy → OpenSearch:** [Optimizing OpenSearch Vector Storage and Search for Faster AI Applications](../../) — Chapter 2

| Navigate | Link |
|----------|------|
| **Course home** | [README.md](../../README.md) |
| **Hands-on guide** | [docs/HANDS-ON-GUIDE.md](../../docs/HANDS-ON-GUIDE.md) |
| **OpenSearch courses** | [OpenSearch/](../../../) |
| **InstAcademy home** | [InstAcademy/](../../../../) |

Enable ML Commons, register and deploy a sentence-transformer model, wire embeddings into ingest pipelines, bulk-load books, and run hybrid search.

## Overview

### Prerequisites

- [Chapter 1 Lesson 1](../Chapter%201/1-1/README.md) — `src/.env` and `src/sample-data.json`
- Cluster with ML Commons / AI search enabled

### Lessons

| Folder | Course | Topic |
|--------|--------|-------|
| [Lesson 1](Lesson%201/README.md) | 2-1 | Register, deploy, smoke-test `msmarco-distilbert-base-tas-b` |
| [Lesson 2](Lesson%202/README.md) | 2-2 | Ingest pipeline, bulk load, hybrid search |
| *(video only)* | 2-3 | Choosing embedding processors — no lab folder |
| [Lesson 4](Lesson%204/README.md) | 2-4 | Cleanup index, pipeline, model |
| [Lesson 5](Lesson%205/README.md) | 2-5 | Cluster routing settings |

Run Lessons **1** then **2** in order. Use **4** to reset. **5** is standalone.

**Lesson 2-3** is video-only: compares dense models and `text_embedding` trade-offs. The lab uses `msmarco-distilbert-base-tas-b` from Lesson 1.

## How to run

**Learn mode** — Dev Tools, follow each lesson README ([guide](../../docs/HANDS-ON-GUIDE.md))

**Fast mode** — [bruno/Chapter 2/](../../bruno/Chapter%202/)

## Next

[Chapter 3](../Chapter%203/README.md) — neural sparse and hybrid search
