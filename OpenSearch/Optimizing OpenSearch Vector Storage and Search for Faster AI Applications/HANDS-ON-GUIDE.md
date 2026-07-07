# Hands-on lab guide

**Vector Storage & Search for AI** — InstAcademy OpenSearch course

| | |
|---|---|
| **Course index** | [README.md](README.md) |
| **Cluster setup** | [CREATE_CLUSTER.md](CREATE_CLUSTER.md) |

This is the **single entry point** for running the labs. Each chapter has **one workshop README** at `src/Chapter N/README.md` that walks through every lesson of that chapter, in order.

## How to read a chapter workshop

Every chapter workshop uses the same layout:

| Label | What it means |
|-------|----------------|
| **Lesson N-M** | Section matching the video lesson the steps come from |
| **Goals** | What you will have when the section is done |
| **Prerequisites** | What to complete first |
| **Step N** | One action in Dev Tools — do these in order |
| **Why** | Reason this step exists and the concept behind it |
| **Request** | Full REST call to copy into Dev Tools |
| **Expected** | What a successful response looks like |
| **Save** | Values to write down for later steps |
| **Fast mode** | Matching Bruno request if you want a shortcut |

Work through **Step 1**, then **Step 2**, and so on. Do not skip ahead unless you are using fast mode to recover.

## Two ways to work

### Learn mode (recommended)

Open **OpenSearch Dashboards → Dev Tools** and follow each lesson README step by step. You build the cluster state yourself.

You need your Instaclustr cluster host, username, and password. The course uses a **3-node** cluster with the **AI Search Plugin** — see [cluster setup](CREATE_CLUSTER.md).

### Fast mode (Bruno)

Use the [bruno](bruno/) collection to run the same REST calls with less typing. Good for catching up or fixing a mistake.

1. Install [Bruno](https://www.usebruno.com/downloads)
2. Open the `bruno/` folder as a collection
3. Set `baseUrl`, `username`, and `password` in the **Local** environment
4. Turn off SSL certificate verification in Bruno settings
5. Open the chapter folder (flat, numbered `01-…`) and run requests in `seq` order; poll ML tasks until `state` is `COMPLETED`

Details: [bruno/README.md](bruno/README.md)

## Configuration

**Dev Tools / Bruno** — cluster URL, username, password

**Save while you work:** `model_group_id`, `model_id`, `task_id` (when polling ML tasks). In Bruno, keep them in the **Local** environment variables ([bruno/README.md](bruno/README.md) lists them all).

## Sample data

Chapters 2–5 bulk-index a shared Gutendex (Project Gutenberg) book dataset; Chapter 1 uses small hand-crafted vector payloads. All bulk bodies ship ready-to-use in [rest/bulk](rest/bulk/) — there is nothing to download or generate.

## ML task polling

Register and deploy often return a `task_id` immediately. Poll until `state` is `COMPLETED`:

```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

In Bruno, use the **Poll ML task** request in the same chapter folder.

## Mostly-theory lessons

Every lesson now has hands-on steps in its chapter workshop, but a few remain lighter on runnable work because the concepts are architectural:

| Lesson | Topic | What you still run |
|--------|--------|--------------------|
| 1-3 | GPUs vs CPUs | Inspection calls: `_cat/plugins`, `_nodes/os`, `_plugins/_knn/stats` |
| 5-4 | Secure, resilient AI apps | Health monitoring + role/user creation via the Security API; TLS/audit config is reference-only on managed clusters |

Lesson 4-4 (MCP server, steps for OpenSearch 3.3+) includes an optional section that needs an external LLM API key.

## Course order

1. [Chapter 1](src/Chapter%201/README.md) — vector fundamentals, kNN/HNSW/IVF, storage optimizations
2. [Chapter 2](src/Chapter%202/README.md) — neural search pipeline and model management
3. [Chapter 3](src/Chapter%203/README.md) — sparse, hybrid, and RRF search
4. [Chapter 4](src/Chapter%204/README.md) — RAG optimization and the MCP server
5. [Chapter 5](src/Chapter%205/README.md) — production cluster tuning
