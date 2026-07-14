# Steps per chapter

Quick reference for how many hands-on steps each chapter workshop contains.
Update this file whenever steps are added, removed, or renumbered.

Last updated: 2026-07-14 (total: **72 steps**)

| Chapter | Steps | Numbering | Notes |
|---------|-------|-----------|-------|
| [Chapter 1](Chapter%201/README.md) — Configuring and optimizing vector search | **16** | 1–16, chapter-wide | Lessons 1-1 (Steps 1–6), 1-2 (Steps 7–14), 1-3 (Steps 15–16). Bruno: 35 requests, `01`–`35` sequential |
| [Chapter 2](Chapter%202/README.md) — Building neural search pipelines | **16** | 1–16, chapter-wide | Plus cleanup items C1–C5. Bruno numbering starts at `02` (connectivity step removed) |
| [Chapter 3](Chapter%203/README.md) — Mastering hybrid search | **14** | Per lesson: 3-1 has 1–9, 3-2 has 1–3, 3-3 has 1–2 | Untouched by the streamlining passes; every step feeds the five-way ranking comparison |
| [Chapter 4](Chapter%204/README.md) — RAG optimization | **15** | 1–15, chapter-wide | Single chunked `bookstore-rag` index built up front. Step 15 connects Claude Desktop over MCP (needs Node 18+ locally) |
| [Chapter 5](Chapter%205/README.md) — Production optimizations | **11** | 1–11, chapter-wide | Awareness, watermarks, shrink recipe, priority tiers, and backpressure are read-along **Reference** blocks, not steps |

## Regenerating the counts

From the course root, this prints every step header per chapter:

```bash
for c in 1 2 3 4 5; do
  echo "=== Chapter $c ==="
  grep -oE "^#{3,4} \*{0,2}(Step [0-9]+|A[0-9])" "src/Chapter $c/README.md"
done
```
