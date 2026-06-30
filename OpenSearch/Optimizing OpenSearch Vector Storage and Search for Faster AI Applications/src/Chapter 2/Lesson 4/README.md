# Chapter 2 Lesson 4 — AI model management with ML Commons

**InstAcademy → OpenSearch:** Lesson 2-4 · [Optimizing OpenSearch Vector Storage and Search for Faster AI Applications](../../../OpenSearch%20Learning%20Path%201.docx) — tear down Lesson 2 artifacts and optionally **undeploy** and **delete** the embedding model from Lesson 1.

## Overview

### Goals

By the end of this lesson you will:

1. **Delete** index **`vector-search-index`** created in Lesson 2.
2. **Delete** ingest pipeline **`vector-search-embeddings-pipeline`**.
3. Optionally **undeploy** and **delete** the ML model referenced by **`ML_MODEL_ID`** in **`src/.env`**.

This frees disk and node memory between chapters. Skip model deletion if you plan to reuse the same **`ML_MODEL_ID`** in [Chapter 3](../../Chapter%203/README.md).

### Prerequisites

- Complete [Lesson 2](../Lesson%202/README.md) (index and pipeline exist).
- Open **Dev Tools** (or Bruno fast mode: [`bruno/Chapter 2/Lesson 4/`](../../../bruno/Chapter%202/Lesson%204/)).
- Have **`ML_MODEL_ID`** in **`src/.env`** if you want full model teardown (optional).

| Resource | Name |
|----------|------|
| Index | `vector-search-index` |
| Ingest pipeline | `vector-search-embeddings-pipeline` |
| Model | value of **`ML_MODEL_ID`** |

**Order matters:** delete the **index** first, then the **pipeline**, then **undeploy** before **delete model** (the cluster rejects deleting a deployed model).

---

## Lab steps

### **Step 1: Delete the vector search index**

**Why**  
Removes indexed documents and k-NN graph data from the cluster. A missing index is fine — this step is idempotent.

**Request** — paste into Dev Tools:

```http
DELETE vector-search-index
```

**Expected**

```json
{
  "acknowledged": true
}
```

A **`404`** is acceptable if the index was already deleted.

**Fast mode**  
`bruno/Chapter 2/Lesson 4/01-delete-vector-search-index.bru`


### **Step 2: Delete the ingest pipeline**

**Why**  
Removes the **`text_embedding`** processor configuration so it cannot be referenced by new indexes.

**Request** — paste into Dev Tools:

```http
DELETE _ingest/pipeline/vector-search-embeddings-pipeline
```

**Expected**

```json
{
  "acknowledged": true
}
```

A **`404`** is acceptable if the pipeline was already removed.

**Fast mode**  
`bruno/Chapter 2/Lesson 4/02-delete-ingest-pipeline.bru`


### **Step 3: Undeploy the ML model (optional)**

**Why**  
A **deployed** model occupies node memory. You must **undeploy** before **`DELETE`** on the model registration. Skip this step and Step 4 if you are keeping the model for the next chapter.

Replace **`YOUR_MODEL_ID`** with **`ML_MODEL_ID`** from **`src/.env`**.

**Request** — paste into Dev Tools:

```http
POST _plugins/_ml/models/YOUR_MODEL_ID/_undeploy
```

**Expected**

```json
{
  "task_id": "...",
  "status": "CREATED"
}
```

Some clusters return success without a **`task_id`** when undeploy completes synchronously.

#### **Poll the undeploy task**

If the response includes **`task_id`**, poll until **`state`** is terminal:

**Request** — paste into Dev Tools:

```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

Repeat every **2–3 seconds** until **`state`** is **`COMPLETED`** or **`FAILED`**.

**Expected when undeploy succeeds:**

```json
{
  "task_id": "...",
  "state": "COMPLETED",
  "model_id": "YOUR_MODEL_ID",
  "task_type": "UNDEPLOY_MODEL"
}
```

**Save**  
confirm **`model_id`** matches **`YOUR_MODEL_ID`** before Step 4.

If undeploy returns **`400`** (not deployed) or **`404`** (model missing), you can proceed to Step 4 or stop — both mean undeploy is not required.

**Fast mode**  
`bruno/Chapter 2/Lesson 4/03-undeploy-model.bru` then **`04-poll-ml-task.bru`**


### **Step 4: Delete the ML model registration (optional)**

**Why**  
Removes the model artifact from ML Commons storage. Only run after a successful undeploy (or if the model was never deployed).

Replace **`YOUR_MODEL_ID`** with the same id used in Step 3.

**Request** — paste into Dev Tools:

```http
DELETE _plugins/_ml/models/YOUR_MODEL_ID
```

**Expected**

```json
{
  "_index": ".plugins-ml-model",
  "_id": "YOUR_MODEL_ID",
  "result": "deleted"
}
```

After deletion, remove **`ML_MODEL_ID`** from **`src/.env`** or update it when you register a new model.

**Fast mode**  
`bruno/Chapter 2/Lesson 4/05-delete-model.bru`

---

## What you learned

- How to remove **indexes** and **ingest pipelines** created for neural search labs.
- The ML Commons lifecycle in reverse: **undeploy → poll → delete model**.
- When to **keep** a deployed model vs. tear it down between chapters.

## Next lesson

[Chapter 2 Lesson 5](../Lesson%205/README.md) — cluster **routing** settings for shard allocation and rebalancing (standalone operations practice).

## Reference scripts

| Script | Same as |
|--------|---------|
| `001-cleanup.py` | Steps 1–4 (index, pipeline, optional undeploy + delete when **`ML_MODEL_ID`** is set) |
