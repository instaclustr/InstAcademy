# Chapter 5 — Production cluster tuning

**Chapter 5** · [Vector Storage & Search for AI](../../README.md)

← [Chapter 4](../Chapter%204/README.md) · [How to run labs](../../HANDS-ON-GUIDE.md)

Shard management, index optimization, vector storage modes, and query backpressure on a 3-node lab cluster.

## Prerequisites

- [Chapter 1 · Lesson 1](../Chapter%201/Lesson%201/README.md) — cluster connectivity
- [Chapter 4 · Lesson 2](../Chapter%204/Lesson%202/README.md) — `bookstore-rag-all-together` index (for shrink / force-merge labs)
- 3-node Instaclustr trial with AI Search Plugin — lab cluster only, not production

## Lessons

| Lab folder | Topic |
|------------|--------|
| [Lesson 1](Lesson%201/README.md) | Routing, shards, force merge, cluster health |
| [Lesson 2](Lesson%202/README.md) | Shrink, reindex, k-NN index versions |
| [Lesson 3](Lesson%203/README.md) | Vector storage modes (`on_disk` vs `in_memory`) |
| *(theory only — no lab)* | Secure, resilient AI apps |
| [Lesson 5](Lesson%205/README.md) | Index routing, search backpressure |

Suggested order: **Lesson 1 → 2 → 3 → 5**.

Labs: **Dev Tools** ([guide](../../HANDS-ON-GUIDE.md)) or [Bruno `Chapter 5`](../../bruno/Chapter%205/).
