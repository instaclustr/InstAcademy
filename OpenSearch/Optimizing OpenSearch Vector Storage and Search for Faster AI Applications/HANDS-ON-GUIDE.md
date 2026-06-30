# Hands-on lab guide

**Vector Storage & Search for AI** — InstAcademy OpenSearch course

| | |
|---|---|
| **Course index** | [README.md](README.md) |
| **Cluster setup** | [CREATE_CLUSTER.md](CREATE_CLUSTER.md) |

This is the **single entry point** for running the labs. Step-by-step REST instructions live in each lesson README under `src/Chapter …/`.

## How to read a lesson

Every hands-on lesson uses the same layout:

| Label | What it means |
|-------|----------------|
| **Chapter N · Lesson M** | Which lab you are in (matches the folder name) |
| **Goals** | What you will have when the lesson is done |
| **Prerequisites** | What to complete first |
| **Step N** | One action in Dev Tools — do these in order |
| **Why** | Reason this step exists |
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
5. Run requests in folder order; poll ML tasks until `state` is `COMPLETED`

Details: [bruno/README.md](bruno/README.md)

## Configuration

**Dev Tools / Bruno** — cluster URL, username, password

**Optional `src/.env`** (Python reference scripts only) — copy from `src/.env.example`; set `ML_MODEL_ID` after you deploy a model.

**Save while you work:** `model_group_id`, `model_id`, `task_id` (when polling ML tasks).

## Sample data

Lessons bulk-index books from `src/sample-data.json`. Full payloads are in [rest/bulk](rest/bulk/). Refresh once with `python data-loader.py` in [Chapter 1 · Lesson 1](src/Chapter%201/Lesson%201/README.md).

## ML task polling

Register and deploy often return a `task_id` immediately. Poll until `state` is `COMPLETED`:

```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

In Bruno, use the **Poll ML task** request in the same lesson folder.

## Lessons without a lab folder

Some course lessons are theory-only — there is no hands-on folder for them:

| Chapter · Lesson | Topic |
|------------------|--------|
| Chapter 1 · Lesson 3 | GPUs vs CPUs |
| Chapter 2 · Lesson 3 | Choosing embedding processors |
| Chapter 4 · Lesson 4 | OpenSearch MCP server |
| Chapter 5 · Lesson 4 | Secure, resilient AI apps |

## Chapter 3 — special layout

Unlike other chapters, **Chapter 3 has one lab folder** (`Lesson 1`) that walks through hybrid search rationale, sparse index setup, and score normalization in a single README. Start at [Chapter 3 · Lesson 1](src/Chapter%203/Lesson%201/README.md).

## Course order

1. [Chapter 1 · Lesson 1](src/Chapter%201/Lesson%201/README.md) — connectivity and sample data
2. [Chapter 1 · Lesson 2](src/Chapter%201/Lesson%202/README.md) — keyword index
3. [Chapter 1 · Lesson 4](src/Chapter%201/Lesson%204/README.md) — vector index and reindex
4. [Chapter 2](src/Chapter%202/README.md) — neural search pipeline
5. [Chapter 3](src/Chapter%203/README.md) — hybrid and sparse search
6. [Chapter 4](src/Chapter%204/README.md) — RAG optimization
7. [Chapter 5](src/Chapter%205/README.md) — production cluster tuning

Optional Python scripts in each lesson folder mirror the same REST calls after you have completed the Dev Tools steps once.
