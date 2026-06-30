# Chapter 5 — Production cluster tuning

**InstAcademy → OpenSearch:** [Optimizing OpenSearch Vector Storage and Search for Faster AI Applications](../../) — Chapter 5

| Navigate | Link |
|----------|------|
| **Course home** | [README.md](../../README.md) |
| **Hands-on guide** | [docs/HANDS-ON-GUIDE.md](../../docs/HANDS-ON-GUIDE.md) |
| **OpenSearch courses** | [OpenSearch/](../../../) |
| **InstAcademy home** | [InstAcademy/](../../../../) |

Shard management, index optimization, vector storage modes, and query backpressure on a 3-node lab cluster.

## Overview

### Prerequisites

- [Chapter 1 Lesson 1](../Chapter%201/1-1/README.md) — cluster connectivity
- [Chapter 4 Lesson 2](../Chapter%204/Lesson%202/README.md) — `bookstore-rag-all-together` index (for shrink / force-merge labs)
- 3-node Instaclustr trial with AI Search Plugin — lab cluster only, not production

### Lessons

| Folder | Course | Topic |
|--------|--------|-------|
| [Lesson 1](Lesson%201/README.md) | 5-1 | Routing, shards, force merge, cluster health |
| [Lesson 2](Lesson%202/README.md) | 5-2 | Shrink, reindex, k-NN index versions |
| [Lesson 3](Lesson%203/README.md) | 5-3 | Vector storage modes (`on_disk` vs `in_memory`) |
| *(video only)* | 5-4 | Secure, resilient AI apps — no lab folder |
| [Lesson 5](Lesson%205/README.md) | 5-5 | Index routing, search backpressure |

Suggested order: **1 → 2 → 3 → 5**

## How to run

**Learn mode** — [hands-on guide](../../docs/HANDS-ON-GUIDE.md)

**Fast mode** — [bruno/Chapter 5/](../../bruno/Chapter%205/)
