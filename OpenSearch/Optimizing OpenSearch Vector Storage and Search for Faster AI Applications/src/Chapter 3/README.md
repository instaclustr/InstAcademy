# Chapter 3 — Mastering hybrid search in OpenSearch

**Chapter 3** · [Vector Storage & Search for AI](../../README.md)

← [Chapter 2](../Chapter%202/README.md) · [How to run labs](../../HANDS-ON-GUIDE.md) · **Next:** [Chapter 4](../Chapter%204/README.md)

> **One combined lab.** Unlike other chapters, Chapter 3 has a **single lab folder** (`Lesson 1`) that covers hybrid search rationale, sparse index setup, and score normalization. Follow the steps in order inside that README.

Combine **lexical (BM25)** and **neural sparse** retrieval: sparse model, chunking ingest pipeline, search pipeline normalization, and hybrid queries on `my-sparse-neural-index`.

## Prerequisites

- [Chapter 1 · Lesson 1](../Chapter%201/Lesson%201/README.md) — `src/sample-data.json`
- [Chapter 2 · Lesson 1](../Chapter%202/Lesson%201/README.md) — ML Commons basics (reuse `huggingface-models` group if it exists)
- Cluster with ML Commons and neural sparse / AI search enabled

## Lab

| Lab folder | Topic |
|------------|--------|
| [Lesson 1](Lesson%201/README.md) | Sparse hybrid search (full hands-on) |

Labs: **Dev Tools** ([guide](../../HANDS-ON-GUIDE.md)) or [Bruno `Chapter 3/Lesson 1`](../../bruno/Chapter%203/Lesson%201/).
