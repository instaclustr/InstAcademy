# Chapter 1 · Lesson 2 — Choosing the right type of vector search (keyword baseline)

**Chapter 1 · Lesson 2** — text vs keyword field types before vector search.

← [Chapter 1 overview](../README.md) · [How to run labs](../../../HANDS-ON-GUIDE.md)

## Overview

### Goals

Create a small **keyword + text** bookstore index and bulk-index three sample books. This is the lexical baseline later lessons compare against neural and hybrid search.

### Prerequisites

- Complete [Lesson 1](../Lesson%201/README.md) (cluster connectivity).
- Open **Dev Tools**.

---

## Lab steps

### **Step 1: Remove a previous run (optional)**

**Why**  
Index mappings are mostly immutable. If you change field types, delete and recreate the index.

**Request** — paste into Dev Tools:

```http
DELETE keyword-index
```

A `404` is fine — the index did not exist yet.

**Fast mode**  
`02-create-keyword-index.bru` folder includes delete as step 1.


### **Step 2: Create the keyword index**

**Why each mapping choice:**

- **`text`** — analyzed (tokenized, lowercased) for full-text search on titles and descriptions.
- **`keyword`** — exact match for ISBN, genre, author (faceting, filtering, sorting).
- **`title` multi-field** — search analyzed `title`, sort/aggregate on `title.keyword`.
- **1 shard, 0 replicas** — minimal footprint on a trial cluster.

**Request** — paste into Dev Tools:


```http
PUT keyword-index
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword", "ignore_above": 256 }
        }
      },
      "author": { "type": "keyword" },
      "isbn": { "type": "keyword" },
      "genre": { "type": "keyword" },
      "publisher": { "type": "keyword" },
      "description": { "type": "text" },
      "price": { "type": "float" },
      "in_stock": { "type": "boolean" },
      "published_year": { "type": "integer" }
    }
  }
}
```

**Expected** `"acknowledged": true`


### **Step 3: Bulk index three sample books**

**Why**  
The bulk API indexes many documents in one request. Each document is two lines: an **action** line, then the **source** JSON.

**Request** — paste into Dev Tools:

```http
POST _bulk
{ "index": { "_index": "keyword-index", "_id": "978-0143127740" } }
{ "isbn": "978-0143127740", "title": "The Martian", "author": "Andy Weir", "genre": "Science Fiction", "publisher": "Crown Publishing", "description": "An astronaut stranded on Mars fights to survive until rescue is possible.", "price": 16.99, "in_stock": true, "published_year": 2014 }
{ "index": { "_index": "keyword-index", "_id": "978-0307277677" } }
{ "isbn": "978-0307277677", "title": "The Road", "author": "Cormac McCarthy", "genre": "Fiction", "publisher": "Vintage", "description": "A father and son journey through a post-apocalyptic landscape.", "price": 15.95, "in_stock": true, "published_year": 2006 }
{ "index": { "_index": "keyword-index", "_id": "978-0061120084" } }
{ "isbn": "978-0061120084", "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic", "publisher": "Harper Perennial", "description": "A coming-of-age story set in the American South.", "price": 12.99, "in_stock": false, "published_year": 1960 }
```

**Expected** `"errors": false` and three `"result": "created"` (or `"updated"`) entries.

**Fast mode**  
`bruno/Chapter 1/Lesson 2/03-bulk-sample-books.bru` uses [`rest/bulk/chapter-1-keyword-index-sample.ndjson`](../../../rest/bulk/chapter-1-keyword-index-sample.ndjson).


### **Step 4: Refresh and search**

**Why**  
OpenSearch is near-real-time; refresh makes new docs visible immediately.

**Request** — paste into Dev Tools:

```http
POST keyword-index/_refresh
```

Try a keyword-style query:

```http
GET keyword-index/_search
{
  "query": {
    "match": {
      "description": "Mars survival"
    }
  }
}
```

**Expected**  
*The Martian* ranks highly (keyword overlap on "Mars").

---

## What you learned

- Difference between **`text`** and **`keyword`** fields.
- How to **create an index**, **bulk** documents, and run a **match** query.

## Next lesson

- **Chapter 1 · Lesson 3 (theory only)** — GPUs vs CPUs — no lab folder. See [lessons without a lab folder](../../../HANDS-ON-GUIDE.md#lessons-without-a-lab-folder).
- **Hands-on:** [Lesson 4](../Lesson%204/README.md) — `knn_vector` index and `_reindex` with dimension truncation.

## Reference scripts

`create-keyword-index.py` performs Steps 1–4 in one run.
