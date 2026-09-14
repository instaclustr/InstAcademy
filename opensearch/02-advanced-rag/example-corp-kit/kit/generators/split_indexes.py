"""
Split chunks.jsonl into the four support indexes for chapter 4
(multi-index agents), create indexes with per-asset retrieval settings,
set aliases, and bulk load.

  support-docs-v1     product-docs + integration-guide  (hybrid + parent-child)
  support-tickets-v1  support-ticket                    (vector-weighted)
  support-issues-v1   known-issue                       (lexical first)
  support-api-v1      api-reference                     (exact path + semantic)

Usage:
    export OS_URL=https://user:pass@your-cluster:9200
    python split_indexes.py --model-id <MODEL_ID> --dimension 384
"""
import argparse
import json
import os
from pathlib import Path

import requests

ROUTING = {
    "product-docs": "docs",
    "integration-guide": "docs",
    "support-ticket": "tickets",
    "known-issue": "issues",
    "api-reference": "api",
}

# issues stays lexical-only: tiny corpus, literal error codes,
# vector overhead buys nothing
NEEDS_VECTORS = {"docs", "tickets", "api"}

TICKETS_PIPELINE = {
    "description": "Tickets lean semantic: customers describe symptoms "
                   "in customer words",
    "phase_results_processors": [
        {"normalization-processor": {
            "normalization": {"technique": "min_max"},
            "combination": {"technique": "arithmetic_mean",
                            "parameters": {"weights": [0.2, 0.8]}}}}
    ],
}


def index_body(family, dimension):
    props = {
        "text": {"type": "text"},
        "parent_text": {"type": "text", "index": False},
        "chunk_id": {"type": "keyword"},
        "parent_id": {"type": "keyword"},
        "source_id": {"type": "keyword"},
        "doc_type": {"type": "keyword"},
        "title": {"type": "text", "fields": {"raw": {"type": "keyword"}}},
        "section_path": {"type": "keyword"},
        "product_area": {"type": "keyword"},
        "product_version": {"type": "keyword"},
        "acl": {"type": "keyword"},
        "tenant_id": {"type": "keyword"},
        "updated_at": {"type": "date"},
        "related_error_codes": {"type": "keyword"},
        "embedding_model_id": {"type": "keyword"},
        "embedding_model_version": {"type": "keyword"},
    }
    settings = {"index": {"number_of_shards": 1, "number_of_replicas": 1}}
    if family in NEEDS_VECTORS:
        settings["index"]["knn"] = True
        settings["index"]["default_pipeline"] = "support-embed"
        props["embedding"] = {
            "type": "knn_vector", "dimension": dimension,
            "method": {"name": "hnsw", "engine": "faiss",
                       "space_type": "innerproduct",
                       "parameters": {"m": 16, "ef_construction": 128}},
        }
    if family == "api":
        # exact matching on endpoint paths
        props["path"] = {"type": "keyword"}
        props["method"] = {"type": "keyword"}
    return {"settings": settings, "mappings": {"properties": props}}


def put(base, path, body):
    r = requests.put(f"{base}/{path}", json=body, timeout=60)
    if r.status_code >= 300:
        raise RuntimeError(f"PUT {path} -> {r.status_code}: {r.text[:300]}")


def bulk(base, index, docs, batch=200):
    for i in range(0, len(docs), batch):
        lines = []
        for d in docs[i:i + batch]:
            lines.append(json.dumps({"index": {"_index": index,
                                               "_id": d["chunk_id"]}}))
            lines.append(json.dumps(d))
        r = requests.post(f"{base}/_bulk", data="\n".join(lines) + "\n",
                          headers={"Content-Type": "application/x-ndjson"},
                          timeout=300)
        resp = r.json()
        if resp.get("errors"):
            bad = [it["index"] for it in resp["items"] if it["index"].get("error")]
            raise RuntimeError(f"{len(bad)} failures in {index}, first: "
                               f"{json.dumps(bad[0])[:300]}")
    print(f"  {index}: {len(docs)} chunks")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-id", required=True)
    ap.add_argument("--dimension", type=int, default=384)
    ap.add_argument("--chunks", default="../output/chunks.jsonl")
    ap.add_argument("--version", default="v1")
    args = ap.parse_args()

    base = os.environ["OS_URL"].rstrip("/")
    buckets = {"docs": [], "tickets": [], "issues": [], "api": []}
    for line in Path(args.chunks).read_text().splitlines():
        c = json.loads(line)
        fam = ROUTING.get(c["doc_type"])
        if fam:
            c["embedding_model_id"] = args.model_id
            c["embedding_model_version"] = "1"
            buckets[fam].append(c)

    print("search pipeline: support-tickets-weighted")
    put(base, "_search/pipeline/support-tickets-weighted", TICKETS_PIPELINE)

    actions = []
    for fam, docs in buckets.items():
        index = f"support-{fam}-{args.version}"
        alias = f"support-{fam}"
        print(f"index {index} ({len(docs)} chunks)")
        put(base, index, index_body(fam, args.dimension))
        bulk(base, index, docs)
        actions.append({"add": {"index": index, "alias": alias}})

    requests.post(f"{base}/_aliases", json={"actions": actions}, timeout=30)
    print("aliases set: support-docs, support-tickets, "
          "support-issues, support-api")


if __name__ == "__main__":
    main()
