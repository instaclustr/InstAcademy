[InstAcademy](../../) · [OpenSearch courses](../)

# Optimizing OpenSearch Vector Storage and Search for Faster AI Applications

**Course version 1.0** · validated end to end on **OpenSearch 3.5.0** · [changelog](CHANGELOG.md)

Build a production vector-search system on OpenSearch, one working piece at a time. You'll create k-NN indexes by hand, deploy an embedding model inside your cluster, run semantic and hybrid searches over real book data, tune a RAG retrieval layer until you can measure the improvement, and finish by connecting an AI agent to the index you built.

Everything is hands-on: **72 steps across five chapters**, each one a real request against your own cluster. Every **Expected** response printed in this course is the actual output from a live OpenSearch 3.5.0 run, not an idealized example.

---

## Start here

| | |
|---|---|
| **1. [Set up your cluster](CLUSTER-SETUP.md)** | Sign up for a free trial, create an OpenSearch cluster with the AI Search Plugin, open the firewall, and collect your connection details. About 15 minutes. |
| **2. [Learn how to run the labs](HANDS-ON-GUIDE.md)** | How a chapter is laid out, how to reach Dev Tools, and the two ways to run each step. Read this once. |
| **3. [Start Chapter 1](chapters/Chapter%201/README.md)** | Build your first vector index and search it. |

## The five chapters

| | Chapter | What you build |
|---|---|---|
| **1** | [Configuring and optimizing vector search](chapters/Chapter%201/README.md) | k-NN indexes from scratch: HNSW and IVF, quantization, storage modes, and the memory and shard levers everything else builds on |
| **2** | [Building neural search pipelines](chapters/Chapter%202/README.md) | Deploy a real embedding model inside the cluster, embed documents at ingest time, and search by meaning instead of keywords |
| **3** | [Mastering hybrid search](chapters/Chapter%203/README.md) | Sparse encoding, then hybrid search: compare lexical, sparse, dense, and two ways of fusing them side by side on the same query |
| **4** | [RAG optimization](chapters/Chapter%204/README.md) | A production retrieval layer: chunking, filtered k-NN, reranking with business rules, measured quality, and an AI agent querying your index over MCP |
| **5** | [Production optimizations](chapters/Chapter%205/README.md) | Break a cluster and triage it back to green, automate the index lifecycle, prove what fp16 quantization saves, and tune queries with real measurements |

## What's in this repository

| Path | What it is |
|---|---|
| [`chapters/Chapter N/`](chapters/Chapter%201/) | The five chapter workshops. This is the course |
| [`bruno/`](bruno/) | Fast mode: every request in the course as a Bruno collection, with the bulk data each chapter sends |
| [`screenshots/`](screenshots/) | Diagrams and console captures used by the chapters |
| [`CLUSTER-SETUP.md`](CLUSTER-SETUP.md) | Sign-up, cluster creation, firewall, connection details |
| [`HANDS-ON-GUIDE.md`](HANDS-ON-GUIDE.md) | How to run the labs |
| [`CHANGELOG.md`](CHANGELOG.md) | Course versions and which OpenSearch version each was validated on |

## What you need

- A **NetApp Instaclustr** OpenSearch cluster with the **AI Search Plugin** (free 30-day trial, no credit card). [Cluster setup](CLUSTER-SETUP.md) walks you through it.
- **OpenSearch 3.5 or later.** (From the Instaclustr platform)
- Chapter 4's final step is **optional** but requires Claude Desktop and Node 18+. The step is not required

## Contributing

Found a step that doesn't work? That's worth an issue. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for what to include and the house rules for changes, and [`SECURITY.md`](SECURITY.md) for credential handling and the lab shortcuts that are not production practice.

## Support

[Instaclustr open-source project status](https://www.instaclustr.com/support/documentation/announcements/instaclustr-open-source-project-status/)
