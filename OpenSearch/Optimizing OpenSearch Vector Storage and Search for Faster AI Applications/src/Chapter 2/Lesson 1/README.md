# Chapter 2 Lesson 1 — Setting up your neural search pipeline

**InstAcademy → OpenSearch:** Lesson 2-1 · [Optimizing OpenSearch Vector Storage and Search for Faster AI Applications](../../../OpenSearch%20Learning%20Path%201.docx) — enable ML Commons, register and deploy **`msmarco-distilbert-base-tas-b`**, and smoke-test text embedding inference.

## Overview

### Goals

By the end of this lesson you will:

1. Enable **URL-based model registration** on your cluster (required before Hugging Face artifacts can be downloaded).
2. Create an ML Commons **model group** named **`huggingface-models`**.
3. **Register** the sentence-transformer model **`huggingface/sentence-transformers/msmarco-distilbert-base-tas-b`** (TorchScript **1.0.3**).
4. **Deploy** the model so it is loaded for inference.
5. Call the **text_embedding** predict API and confirm 768-dimensional vectors are returned.

These steps prepare **`ML_MODEL_ID`** for [Lesson 2](../Lesson%202/README.md), where the same model id is wired into an ingest pipeline.

### Prerequisites

- Complete [Chapter 1 Lesson 1-1](../../Chapter%201/1-1/README.md): cluster connectivity and **`src/sample-data.json`**.
- Complete [cluster setup](../../CREATE_CLUSTER.md): trial cluster with **AI Search / ML Commons** enabled and your IP on the firewall.
- Open **OpenSearch Dashboards** → **Dev Tools** (or use Bruno fast mode: [`bruno/Chapter 2/Lesson 1/`](../../../bruno/Chapter%202/Lesson%201/)).
- Keep a notepad (or **`src/.env`**) for ids returned by ML Commons:

| Variable | Example | Used in |
|----------|---------|---------|
| `model_group_id` | `model_group_id` from Step 3 | Step 4 (register model) |
| `model_id` | `model_id` from Step 4 / deploy task | Steps 5–6; set **`ML_MODEL_ID`** in **`src/.env`** for Lesson 2 |
| `task_id` | from register or deploy responses | Poll with **`GET _plugins/_ml/tasks/{task_id}`** |

---

## Lab steps

### **Step 1: Verify cluster connectivity**

**Why**  
ML registration fails with opaque errors when auth or TLS is wrong. Confirm REST access before downloading a model.

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
  "version": { "number": "2.x.x" },
  "tagline": "The OpenSearch Project: https://opensearch.org/"
}
```

**Fast mode**  
`bruno/Chapter 2/Lesson 1/01-cluster-info.bru`


### **Step 2: Allow registering models via URL**

**Why**  
ML Commons blocks fetching model artifacts from external URLs by default. This persistent cluster setting must be **`true`** before registration can pull the Hugging Face TorchScript artifact.

**Request** — paste into Dev Tools:

```http
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.allow_registering_model_via_url": true
  }
}
```

**Expected**

```json
{
  "acknowledged": true,
  "persistent": {
    "plugins.ml_commons.allow_registering_model_via_url": "true"
  }
}
```

**Fast mode**  
`bruno/Chapter 2/Lesson 1/02-enable-url-model-registration.bru`


### **Step 3: Register a model group**

**Why**  
Every ML Commons model belongs to a **model group** for organization and access control. Create the group once, then pass its id into model registration.

**Request** — paste into Dev Tools:

```http
POST _plugins/_ml/model_groups/_register
{
  "name": "huggingface-models",
  "description": "A group for Hugging Face transformer models"
}
```

**Expected**

```json
{
  "model_group_id": "...",
  "status": "CREATED"
}
```

**Save**  
copy **`model_group_id`** — you need it in Step 4.

If the group already exists, reuse the existing **`model_group_id`** from Dev Tools instead of recreating.

**Fast mode**  
`bruno/Chapter 2/Lesson 1/03-register-model-group.bru`


### **Step 4: Register the embedding model**

**Why**  
Registration downloads and validates the **`msmarco-distilbert-base-tas-b`** TorchScript artifact on the cluster. This runs **asynchronously**; the HTTP response usually returns a **`task_id`** to poll.

Replace **`YOUR_MODEL_GROUP_ID`** with the id from Step 3.

**Request** — paste into Dev Tools:

```http
POST _plugins/_ml/models/_register
{
  "name": "huggingface/sentence-transformers/msmarco-distilbert-base-tas-b",
  "version": "1.0.3",
  "model_group_id": "YOUR_MODEL_GROUP_ID",
  "model_format": "TORCH_SCRIPT"
}
```

**Expected**

```json
{
  "task_id": "...",
  "status": "CREATED"
}
```

Some clusters finish synchronously and return **`model_id`** directly without a **`task_id`**.

#### **Poll the registration task**

If you received a **`task_id`**, poll until **`state`** is **`COMPLETED`** or **`FAILED`**:

**Request** — paste into Dev Tools:

```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

Repeat every **2–3 seconds** (up to ~2 minutes on a trial cluster). While the task runs you may see:

```json
{
  "task_id": "...",
  "state": "RUNNING",
  "task_type": "REGISTER_MODEL"
}
```

**Expected**

```json
{
  "task_id": "...",
  "state": "COMPLETED",
  "model_id": "...",
  "task_type": "REGISTER_MODEL"
}
```

**Save**  
copy **`model_id`** from the completed task (or from the initial response if no task was returned).

If **`state`** is **`FAILED`**, check cluster logs and ensure the cluster can reach Hugging Face over HTTPS.

**Fast mode**  
`bruno/Chapter 2/Lesson 1/04-register-model.bru` then **`05-poll-ml-task.bru`** (set **`taskId`** in the Bruno environment between runs).


### **Step 5: Deploy the model**

**Why**  
Registration stores the artifact on disk; **deploy** loads it into memory on ML nodes so **`_predict`** and ingest pipelines can run inference.

Replace **`YOUR_MODEL_ID`** with the id from Step 4.

**Request** — paste into Dev Tools:

```http
POST _plugins/_ml/models/YOUR_MODEL_ID/_deploy
```

**Expected**

```json
{
  "task_id": "...",
  "status": "CREATED"
}
```

#### **Poll the deploy task**

If the response includes **`task_id`**, poll the same way as Step 4:

**Request** — paste into Dev Tools:

```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

**Expected**

```json
{
  "task_id": "...",
  "state": "COMPLETED",
  "model_id": "YOUR_MODEL_ID",
  "task_type": "DEPLOY_MODEL"
}
```

**Save**  
confirm **`model_id`**, then add to **`src/.env`**:

```bash
ML_MODEL_ID=YOUR_MODEL_ID
```

**Fast mode**  
`bruno/Chapter 2/Lesson 1/06-deploy-model.bru` then **`07-poll-ml-task-deploy.bru`**


### **Step 6: Smoke-test text embedding inference**

**Why**  
Proves the deployed model returns vectors before you attach it to ingest pipelines in Lesson 2. If this fails, bulk indexing with **`text_embedding`** will fail too.

Replace **`YOUR_MODEL_ID`** with your deployed model id.

**Request** — paste into Dev Tools:

```http
POST _plugins/_ml/_predict/text_embedding/YOUR_MODEL_ID
{
  "text_docs": ["Some example text to embed.", "Another sentence for testing."],
  "return_number": true,
  "target_response": ["sentence_embedding"]
}
```

**Expected** JSON with **`inference_results`** (or equivalent) containing **768-float** **`sentence_embedding`** vectors — one per input string.

**Fast mode**  
`bruno/Chapter 2/Lesson 1/08-text-embedding-predict.bru`

---

## What you learned

- How to enable **URL model registration** and create an ML Commons **model group**.
- The **register → poll → deploy → poll** lifecycle for TorchScript embedding models.
- How to call **`/_predict/text_embedding/{model_id}`** and capture **`ML_MODEL_ID`** for later lessons.

## Next lesson

[Chapter 2 Lesson 2](../Lesson%202/README.md) — create ingest pipeline **`vector-search-embeddings-pipeline`**, index **`vector-search-index`**, bulk-load books, and run hybrid neural + keyword search.

## Reference scripts

| Script | Same as |
|--------|---------|
| `001-setup.py` | Steps 1–3 (connectivity, cluster setting, model group) |
| `002-register-model.py` | Step 4 + task polling |
| `003-deploy-model.py` | Step 5 + task polling |
| `004-generate-embeddings.py` | Step 6 (text embedding predict) |
