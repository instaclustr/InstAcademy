"""Remove every support-* asset this lab created, so the shared cluster is
left clean. Safe to run more than once. Undeploys and deletes the model,
deletes the model group, both pipelines, and the index.
"""
import json, time
from osc import os_req

INDEX = "support-advrag-kb"

def show(label, resp):
    print(f"{label}: {json.dumps(resp)[:160]}")

# index
c, r = os_req("DELETE", f"/{INDEX}")
show("delete index", r)

# search pipeline + ingest pipeline
c, r = os_req("DELETE", "/_search/pipeline/support-advrag-hybrid")
show("delete search pipeline", r)
c, r = os_req("DELETE", "/_ingest/pipeline/support-advrag-embed")
show("delete ingest pipeline", r)

# model: read id, undeploy, delete
try:
    mid = open("model_id.txt").read().strip()
except FileNotFoundError:
    mid = None
if mid:
    c, r = os_req("POST", f"/_plugins/_ml/models/{mid}/_undeploy")
    show("undeploy model", r)
    time.sleep(3)
    c, r = os_req("DELETE", f"/_plugins/_ml/models/{mid}")
    show("delete model", r)

# model group
c, s = os_req("POST", "/_plugins/_ml/model_groups/_search",
              {"query": {"term": {"name.keyword": "advanced-rag-models"}}, "size": 1})
hits = s.get("hits", {}).get("hits", [])
if hits:
    gid = hits[0]["_id"]
    c, r = os_req("DELETE", f"/_plugins/_ml/model_groups/{gid}")
    show("delete model group", r)

print("teardown complete")
