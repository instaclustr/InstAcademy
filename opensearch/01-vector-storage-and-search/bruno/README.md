← [Course index](../README.md) · [How to run labs](../HANDS-ON-GUIDE.md)

# Fast mode — Bruno REST collection

🧪 Fast mode · 151 requests across 5 chapters · 🔧 Requires [Bruno](https://www.usebruno.com/)

Run the same REST calls as the chapter workshop READMEs without typing them into Dev Tools. Use this to **catch up**, **recover after a mistake**, or **smoke-test** a cluster.

## 📋 Setup (once)

1. Install [Bruno](https://www.usebruno.com/downloads).
2. **Open Collection** → select this `bruno/` folder.
3. Open **Environments → Local** and set:

   | Variable | Example | Notes |
   |----------|---------|--------|
   | `baseUrl` | `https://123.45.67.89:9200` | Cluster URL from Instaclustr (no trailing slash) |
   | `username` | `icopensearch` | As shown in the console |
   | `password` | *(your password)* | |
   | `modelGroupId` | | Fill after **Register model group** |
   | `modelId` | | Fill after register/deploy **COMPLETED** (dense model, Chapters 2–4) |
   | `taskId` | | Update when polling ML tasks |
   | `ivfModelId` | | Chapter 1 — fill with the `model_id` from **Train IVF model** |
   | `sparseModelId` | | Chapters 2–3 — the **sparse** model's id (keep separate from `modelId`) |

   The pipeline-name variables (`hybridPipelineId`, `bookstoreHybridPipelineId`) are pre-filled and never need editing.

4. SSL certificate verification can stay **on**: Instaclustr trial clusters present valid, publicly trusted certificates. If you run the collection against a self-managed cluster with a self-signed certificate instead, turn verification off in **Settings → SSL/TLS Certificate Verification**.

5. Select the **Local** environment in the top-right before sending requests.

## 🧪 How to run a chapter

1. Open the chapter folder (e.g. `Chapter 2`). Requests are numbered in workshop order and match the steps in that chapter's README under `chapters/Chapter …/README.md`.
2. Run requests **top to bottom** (`seq` order).
3. After **Register model** or **Deploy model**, if the response contains `task_id`:
   - Set `taskId` in the environment (or edit the Poll request URL).
   - Run **Poll ML task** repeatedly until `"state": "COMPLETED"`.
   - Copy `model_id` into `modelId`.
4. Bulk requests send an `.ndjson` file that sits in the same chapter folder as the request. In Bruno, `@file(...)` paths are relative to the collection root (`bruno/`), e.g. `01-configuring-vector-search/chapter-1-lesson-1-vectors.ndjson`.

## 📚 Folder layout

```
bruno/
  environments/
    Local.bru          # Your cluster credentials
  01-configuring-vector-search/           # 01–40 · vector fundamentals, kNN/HNSW/IVF, storage optimizations
  02-neural-search-pipelines/           # 01–36 · neural search pipeline, model management, tuning
  03-hybrid-search/           # 01–19 · sparse, hybrid, and RRF search
  04-rag-optimization/           # 01–51 · RAG pipeline, chunking, query optimization, MCP server
  05-production-optimizations/           # 01–72 · shards, index optimization, security, query tuning
```

Each chapter folder is **flat** — requests are numbered `01-…`, `02-…` in the same order as the steps in the matching chapter workshop (`chapters/Chapter …/README.md`).

## 🧪 Learn mode vs fast mode

| | Learn mode | Fast mode (Bruno) |
|---|------------|-------------------|
| Where | Dev Tools in Dashboards | Bruno app |
| Goal | Understand each API | Same outcome, less typing |
| ML tasks | You poll manually in Dev Tools | **Poll ML task** request |
| Bulk data | Printed in the chapter page | The `.ndjson` file beside the request |

Start with [Learn mode](../HANDS-ON-GUIDE.md) at least once; use Bruno when you need speed or recovery.
