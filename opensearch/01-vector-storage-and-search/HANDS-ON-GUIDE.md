← [Course index](README.md) · [Cluster setup](CLUSTER-SETUP.md) · [Bruno collection](bruno/README.md) · **Next:** [Chapter 1](chapters/01-configuring-vector-search/README.md)

# How to run the labs

📋 Read once · 🧪 Dev Tools console or Bruno fast mode · ⏱ About 5 minutes

This page is the entry point for the hands-on part of the course. Read it once, then work through the chapters in order. Each chapter is a single workshop page at `chapters/<chapter-slug>/README.md` that walks through every step of that chapter, and you run those steps against your own OpenSearch cluster.

**Before you start:** you need a running cluster and its connection details. If you don't have one yet, go to [cluster setup](CLUSTER-SETUP.md) first; it takes about 15 minutes.

---

## 📋 How a chapter is laid out

Every chapter follows the same shape, so once you've done one, you know how to read them all.

| Element | What it is |
|---|---|
| **Lesson N-M** | A section matching the lesson in the video |
| **Step N** | One thing you do, numbered across the whole chapter. Do them in order |
| **Request** | The REST call to run, ready to copy |
| **Expected** | The real response from the cluster this course was validated on, and what the interesting parts of it mean |
| **Save** | A value (a model id, a task id) that a later step needs |
| **Fast mode** | The matching Bruno request, if you'd rather click than type |

Steps build on each other, so work through them in order. If something breaks, the Bruno collection is the fastest way to catch back up.

Each chapter ends with a **wrap-up**, a **what you learned** summary, and a **cleanup** section that removes what the chapter created.

## 🧪 Two ways to run the steps

### Dev Tools (the main path)

Dev Tools is the console built into OpenSearch Dashboards, and it's where you run almost every request in this course. To get there:

1. Open your **Dashboards URL** in a browser. It's on the **Connection Info** tab of your cluster in the Instaclustr console, and it looks like this (note the port, **5601**, not 9200):

   ```
   https://opensearch-dashboards.<your-cluster-id>.cnodes.io:5601
   ```

2. Log in with the same username and password you use for the cluster (`icopensearch` by default).
3. Open the menu at the top left, scroll to **Management**, and choose **Dev Tools**. Or jump straight there:

   ```
   https://opensearch-dashboards.<your-cluster-id>.cnodes.io:5601/app/dev_tools#/console
   ```

You'll see a split screen: type requests on the left, responses appear on the right. Paste a **Request** from the chapter page, click the green play button (or press **Ctrl+Enter**), and compare what comes back to the **Expected** block.

Everything a step needs is printed on the chapter page, including the bulk data. There is nothing to download or generate.

### Bruno (fast mode)

[Bruno](https://www.usebruno.com/downloads) is a free REST client. The [`bruno/`](bruno/) collection contains every request in the course, so you can run a chapter without typing. It's useful for catching up, recovering from a mistake, or re-running a chapter quickly.

1. Install Bruno and open the `bruno/` folder as a collection.
2. In the **Local** environment, set `baseUrl`, `username`, and `password` from your cluster's connection info.
3. Open a chapter folder and run the requests in numbered order.

The [Bruno guide](bruno/README.md) covers the variables you fill in as you go.

## 🛟 Things worth knowing before you start

**Values you carry forward.** A few steps produce ids that later steps need, mainly `model_group_id`, `model_id`, and `task_id`. Each one is flagged with **Save** where it appears. Keep them in a scratch file, or in Bruno's **Local** environment variables.

**Model registration and deployment are asynchronous.** Those calls return a `task_id` immediately and finish in the background, so you poll until the task reports `"state": "COMPLETED"` before moving on:

```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

Registration can take a minute or two, because the cluster is downloading a model. This is normal, and the chapters tell you when to expect it.

**Every step runs.** There is no read-along filler in this course: each numbered step sends a real request and produces a result you can inspect. Where a production practice is worth knowing but not worth demonstrating on a trial cluster, it appears as a short note inside the step that raises it, not as a step of its own.

**Clean up when you finish a chapter.** Each chapter's cleanup section removes the indexes, pipelines, and models it created. Running it keeps your trial cluster tidy and avoids surprises in the next chapter.

## 📚 Course order

| Chapter | What you build |
|---|---|
| [Chapter 1](chapters/01-configuring-vector-search/README.md) | Vector fundamentals: k-NN indexes, HNSW and IVF, quantization and storage modes |
| [Chapter 2](chapters/02-neural-search-pipelines/README.md) | A neural search pipeline: deploy an embedding model, embed at ingest, search by meaning |
| [Chapter 3](chapters/03-hybrid-search/README.md) | Sparse encoding, hybrid search, and comparing score normalization against RRF |
| [Chapter 4](chapters/04-rag-optimization/README.md) | Production RAG: chunking, filtering, reranking, quality measurement, and connecting an AI agent over MCP |
| [Chapter 5](chapters/05-production-optimizations/README.md) | Running it in production: shard triage, index lifecycle, memory savings, and query tuning |

---

### Ready to start some hands-on fun??
**Make sure your Cluster is ready** and start with [Chapter 1](chapters/01-configuring-vector-search/README.md)!
