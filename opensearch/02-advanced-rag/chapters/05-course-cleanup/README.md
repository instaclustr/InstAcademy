← **Previous:** [Chapter 4](../04-rag-with-memory/README.md) · [Course index](../../README.md) · [How to run labs](../../HANDS-ON-GUIDE.md) →

# Course cleanup

🧹 Optional · 🔧 Dev Tools console · ⏱ About 5 minutes

You've finished the course. This page removes everything the labs created — the conversation memories, the knowledge base index, the two pipelines, the embedding model, and its model group — so your cluster is left clean for whatever you build next.

**This is optional.** Nothing the course created runs on a schedule or costs you anything beyond the trial, and when the free trial ends every running resource is removed from your account automatically. Run this cleanup if you'd rather keep a tidy cluster to keep experimenting on, or if you're about to hand the cluster back and move on to another Instaclustr managed technology. If you'd rather just delete the whole cluster, skip to [the last section](#or-delete-the-whole-cluster).

Everything here runs in **Dev Tools**, the same console you used through the course. Prefer a script? The kit ships [`example-corp-kit/rag-runner/teardown.py`](../../example-corp-kit/rag-runner/), which removes the index, pipelines, model, and model group in one run.

---

## 1. Delete the conversation memories

Chapter 4 created three memories: the two you made by hand in Steps 2 and 9, and the one the chat server created at startup in Step 12. Delete each one; deleting a memory also removes all of its messages.

**Request** - if you saved the three `memory_id` values, delete them one at a time:

```http
DELETE _plugins/_ml/memory/YOUR_MEMORY_ID
```

**Expected** - the memory and its messages are gone.

```json
{ "success": true }
```

**Request** - if you did not save the ids, list every memory on the cluster first, then delete each by the `memory_id` it shows:

```http
GET _plugins/_ml/memory/
```

**Expected** - a `memories` array. Copy each `memory_id` and run the `DELETE` above for it, until the list comes back empty.

```json
{
  "memories": [
    { "memory_id": "EJvN2J8BEWv-bbzhjph8", "name": "acme-analytics dashboard issue", "...": "..." }
  ]
}
```

---

## 2. Remove the knowledge base, pipelines, and model

This is the rest of what the course built, all of it created in Chapter 1 and reused ever since. Remove it in this order — the model has to be undeployed before it can be deleted, and deleted before its group can be.

**Request** - run these in order, in Dev Tools. Replace `YOUR_MODEL_ID` and `YOUR_MODEL_GROUP_ID` with the ids you saved in Chapter 1:

```http
DELETE support-advrag-kb

DELETE _search/pipeline/support-advrag-hybrid

DELETE _ingest/pipeline/support-advrag-embed

POST _plugins/_ml/models/YOUR_MODEL_ID/_undeploy

DELETE _plugins/_ml/models/YOUR_MODEL_ID

DELETE _plugins/_ml/model_groups/YOUR_MODEL_GROUP_ID
```

**Expected** - `{ "acknowledged": true }` from the index and pipeline deletes, a per-node report from the undeploy, and `"result": "deleted"` from the model and model group deletes. Undeploy the model before deleting it, or the delete is refused while it is still loaded.

> **Lost your model id?** Find it again without re-registering:
>
> ```http
> POST _plugins/_ml/models/_search
> { "query": { "match": { "name": "all-MiniLM-L6-v2" } }, "_source": ["name", "model_state"] }
> ```

---

## Or delete the whole cluster

If you're done with OpenSearch entirely, you don't need to remove anything piece by piece — delete the cluster from the [Instaclustr Management Console](https://console2.instaclustr.com/?source=InstAcademy_OpenSearch_Advanced_RAG) and everything above goes with it. Your free trial still has time on it, so this is also the moment to spin up a different managed technology and keep exploring. Whatever you leave running is removed automatically when the trial ends.

Thanks for building this with us.

---

← [Chapter 4](../04-rag-with-memory/README.md) · [Course index](../../README.md) · [Report a problem with this page](https://github.com/instaclustr/instacademy/issues/new/choose) · 🏁 [Back to the course index](../../README.md) →
