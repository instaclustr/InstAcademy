# Hands-on lab guide

**InstAcademy → OpenSearch → Optimizing OpenSearch Vector Storage and Search for Faster AI Applications**

| Navigate | Link |
|----------|------|
| **Up to OpenSearch courses** | [OpenSearch/](../../) |
| **Up to InstAcademy home** | [InstAcademy/](../../../) |
| **Course README** | [README.md](../README.md) |

This folder contains the hands-on labs for that InstAcademy course. The voice script is [Optimizing OpenSearch Vector Storage and Search for Faster AI Applications (script).docx](https://github.com/instaclustr/InstAcademy/blob/main/OpenSearch/Optimizing%20OpenSearch%20Vector%20Storage%20and%20Search%20for%20Faster%20AI%20Applications/OpenSearch%20Learning%20Path%201.docx); each lesson README follows that script.

**Prefer the formatted site?** [Open the lab guide on GitHub Pages](https://instaclustr.github.io/InstAcademy/) (search, tabs, copy buttons on code blocks). Setup: [PUBLISHING.md](PUBLISHING.md).

## How to read a lesson

Every hands-on lesson uses the same layout:

| Label | What it means |
|-------|----------------|
| **InstAcademy → OpenSearch** | Breadcrumb — which InstAcademy course this lesson belongs to |
| **Goals** | What you will have when the lesson is done |
| **Prerequisites** | What to complete first |
| **Step N** | One action in Dev Tools — do these in order |
| **Why** | Reason this step exists (matches the video) |
| **Request** | Full REST call to copy into Dev Tools |
| **Expected** | What a successful response looks like |
| **Save** | Values to write down for later steps |
| **Fast mode** | Matching Bruno request if you want a shortcut |

Work through **Step 1**, then **Step 2**, and so on. Do not skip ahead unless you are using fast mode to recover.

## Two ways to work

### Learn mode (recommended)

Open **OpenSearch Dashboards → Dev Tools** and follow each lesson README step by step. You build the cluster state yourself.

You need your Instaclustr cluster host, username, and password. The course uses a **3-node** cluster with the **AI Search Plugin** — see [cluster setup](../CREATE_CLUSTER.md).

### Fast mode (Bruno)

Use the [bruno](../bruno/) collection to run the same REST calls with less typing. Good for catching up or fixing a mistake.

1. Install [Bruno](https://www.usebruno.com/downloads)
2. Open the `bruno/` folder as a collection
3. Set `baseUrl`, `username`, and `password` in the **Local** environment
4. Turn off SSL certificate verification in Bruno settings
5. Run requests in folder order; poll ML tasks until `state` is `COMPLETED`

Details: [bruno/README.md](../bruno/README.md)

## Configuration

**Dev Tools / Bruno**

- Cluster URL, username, password

**Optional `src/.env`** (for Python reference scripts only)

- `OPENSEARCH_HOST`, `OPENSEARCH_USERNAME`, `OPENSEARCH_PASSWORD`
- `ML_MODEL_ID` after you deploy a model

Copy from `src/.env.example`.

**While you work, save on a notepad**

- `model_group_id`
- `model_id`
- `task_id` (when polling ML tasks)

## Sample data

Lessons bulk-index books from `src/sample-data.json`.

- Small examples are inline in lesson READMEs
- Full 256-book payloads are in [rest/bulk](../rest/bulk/)
- Refresh the file once with `python data-loader.py` (Chapter 1 Lesson 1)

## ML task polling

Register and deploy often return a `task_id` immediately. The model is not ready until the task state is `COMPLETED`.

**Request**

```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

Run every few seconds. When `state` is `COMPLETED`, copy `model_id` from the response.

In Bruno, use the **Poll ML task** request in the same lesson folder.

## Video-only segments (no lab folder)

- **Lesson 1-3** — GPUs vs CPUs
- **Lesson 2-3** — Choosing embedding processors (dense/sparse labs are in Chapters 2–3)
- **Lesson 4-4** — OpenSearch MCP server
- **Lesson 5-4** — Secure, resilient AI apps

## Suggested order

1. [Chapter 1 Lesson 1](../src/Chapter%201/1-1/README.md) — connectivity and sample data
2. [Chapter 1 Lesson 2](../src/Chapter%201/1-2/README.md) — keyword index
3. [Chapter 1 Lesson 4](../src/Chapter%201/1-4/README.md) — vector index and reindex
4. [Chapter 2](../src/Chapter%202/README.md) — neural search pipeline
5. [Chapter 3](../src/Chapter%203/README.md) — hybrid and sparse search
6. [Chapter 4](../src/Chapter%204/README.md) — RAG optimization
7. [Chapter 5](../src/Chapter%205/README.md) — production cluster tuning

## Reference scripts

Each lesson folder has commented Python files that run the same REST calls. Use them after you have done the Dev Tools steps once, or to compare your results.
