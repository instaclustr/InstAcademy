# Chapter 1 Lesson 1 — Vector search fundamentals and configuration

**InstAcademy → OpenSearch:** Lesson 1-1 · [Optimizing OpenSearch Vector Storage and Search for Faster AI Applications](../../OpenSearch%20Learning%20Path%201.docx) — connectivity and shared sample data for later labs.

## Overview

### Goals

By the end of this lesson you will:

1. Confirm your **Instaclustr OpenSearch cluster** is reachable from your browser and from REST.
2. Download the **Gutendex book dataset** used throughout the course (`src/sample-data.json`).

The video lesson covers vector settings conceptually; this lab focuses on **getting your environment ready** before Chapter 2's neural pipeline.

### Prerequisites

- Complete [cluster setup](../../CREATE_CLUSTER.md): 3-node trial, **AI Search Plugin** enabled, your IP on the firewall.
- Open **OpenSearch Dashboards** → **Dev Tools** (or use Bruno fast mode: [`bruno/Chapter 1/Lesson 1-1/`](../../bruno/Chapter%201/Lesson%201-1/)).

Keep a notepad (or `src/.env`) for:

| Variable | Example | Used in |
|----------|---------|---------|
| Cluster URL | `https://123.45.67.89:9200` | Every lesson |
| Username | `icopensearch` | Basic auth |
| Password | *(from console)* | Basic auth |

---

## Lab steps

### **Step 1: Verify cluster connectivity**

**Why**  
Every later lesson assumes basic auth and TLS work. A five-second smoke test saves hours of debugging bulk or ML errors.

**Why**  
`GET /` returns cluster name, version, and tag line.

In **Dev Tools**, run:

**Request** — paste into Dev Tools:

```http
GET /
```

**Expected**

```json
{
  "name": "...",
  "cluster_name": "...",
  "cluster_uuid": "...",
  "version": { "number": "2.x.x", ... },
  "tagline": "The OpenSearch Project: https://opensearch.org/"
}
```

If you see `401 Unauthorized`, check username/password. If the request times out, verify your IP is on the Instaclustr firewall list.

**Fast mode**  
`bruno/Chapter 1/Lesson 1-1/01-cluster-info.bru`


### **Step 2: Download the course sample dataset**

**Why**  
Later lessons bulk-index the same 256 Project Gutenberg books so your results match the course. Pre-downloading avoids repeated calls to the public Gutendex API and works offline.

The repo may already include `src/sample-data.json`. Refresh it if you want the latest Gutendex pages.

**Option A — one-time Python helper (recommended):**

From `src/Chapter 1/1-1/`:

```bash
pip install -r ../../../requirements.txt
python data-loader.py
```

This writes **`src/sample-data.json`** (256 books with titles, authors, summaries, etc.).

**Option B — manual download:** Gutendex API is at `https://gutendex.com/books/` — not required if you use the committed file.

**Verify:** the file exists and is non-empty:

```bash
ls -la ../../../sample-data.json
```

You do **not** index this file in Lesson 1-1; Chapter 2 onward bulk-load it into OpenSearch.

---

## What you learned

- How to confirm REST access to your managed cluster.
- Where the shared **`sample-data.json`** lives and why the course uses a fixed dataset.

## Next lesson

[Chapter 1 Lesson 2](../1-2/README.md) — create a **keyword** bookstore index and bulk a few sample documents using Dev Tools.

## Reference scripts

| Script | Same as |
|--------|---------|
| `opensearch-status.py` | Step 1 (`GET /`) |
| `data-loader.py` | Step 2 (Gutendex download) |
