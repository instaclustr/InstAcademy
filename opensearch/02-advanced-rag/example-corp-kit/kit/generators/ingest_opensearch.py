"""
Set up OpenSearch 3.6+ for the course and bulk load chunks.jsonl.

Creates:
  1. Ingest pipeline `support-embed` with a text_embedding processor
  2. Index `support-docs-v1` (knn_vector, faiss hnsw) behind alias
     `support-docs`
  3. Search pipeline `support-hybrid-rrf` (score-ranker-processor, rank based)
  4. Search pipeline `support-hybrid-weighted` (normalization-processor, min_max
     plus arithmetic_mean with explicit weights)
  5. Bulk loads with modest batches and backpressure, per lesson 1.4

Prereqs: a deployed text embedding model in ML Commons. Pass its model_id.
On Instaclustr Managed Platform, enable the AI Search plugin, then register
and deploy a model (see code-samples/lesson-1-4.md for connector setup).

Usage:
    export OS_URL=https://user:pass@your-cluster:9200
    python ingest_opensearch.py --model-id <MODEL_ID> --dimension 384
"""
import argparse
import json
import os
import time
from pathlib import Path

import requests

ALIAS = "support-docs"


def put(base, path, body):
    r = requests.put(f"{base}/{path}", json=body, timeout=60)
    if r.status_code >= 300:
        raise RuntimeError(f"PUT {path} -> {r.status_code}: {r.text[:400]}")
    return r.json()


def ingest_pipeline(model_id):
    return {
        "description": "the support tool embedding at ingest. The model here MUST "
                       "match the model used at query time.",
        "processors": [
            {"text_embedding": {
                "model_id": model_id,
                "field_map": {"text": "embedding"}}}
        ],
    }


def index_body(dimension):
    return {
        "settings": {
            "index": {
                "knn": True,
                "number_of_shards": 2,
                "number_of_replicas": 1,
                "default_pipeline": "support-embed",
            }
        },
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "parent_text": {"type": "text", "index": False},
                "embedding": {
                    "type": "knn_vector",
                    "dimension": dimension,
                    "method": {
                        "name": "hnsw",
                        "engine": "faiss",
                        "space_type": "innerproduct",
                        "parameters": {"m": 16, "ef_construction": 128},
                    },
                },
                "chunk_id": {"type": "keyword"},
                "parent_id": {"type": "keyword"},
                "source_id": {"type": "keyword"},
                "doc_type": {"type": "keyword"},
                "title": {"type": "text",
                          "fields": {"raw": {"type": "keyword"}}},
                "section_heading": {"type": "text"},
                "section_path": {"type": "keyword"},
                "product_area": {"type": "keyword"},
                "product_version": {"type": "keyword"},
                "acl": {"type": "keyword"},
                "updated_at": {"type": "date"},
                "related_error_codes": {"type": "keyword"},
                # model lineage per chunk, lesson 1.4
                "embedding_model_id": {"type": "keyword"},
                "embedding_model_version": {"type": "keyword"},
            }
        },
    }


HYBRID_RRF = {
    "description": "Hybrid merge via reciprocal rank fusion",
    "phase_results_processors": [
        {"score-ranker-processor": {
            "combination": {
                "technique": "rrf",
                "rank_constant": 60,
            }}}
    ],
}

HYBRID_WEIGHTED = {
    "description": "Hybrid merge via min_max normalization, 0.4 lexical / "
                   "0.6 semantic",
    "phase_results_processors": [
        {"normalization-processor": {
            "normalization": {"technique": "min_max"},
            "combination": {
                "technique": "arithmetic_mean",
                "parameters": {"weights": [0.4, 0.6]},
            }}}
    ],
}


def bulk_load(base, chunks_path, model_id, batch_size, index_name):
    chunks = [json.loads(l) for l in Path(chunks_path).read_text().splitlines()]
    total, sent = len(chunks), 0
    i = 0
    while i < len(chunks):
        batch = chunks[i:i + batch_size]
        lines = []
        for c in batch:
            lines.append(json.dumps(
                {"index": {"_index": index_name, "_id": c["chunk_id"]}}))
            doc = dict(c)
            doc["embedding_model_id"] = model_id
            doc["embedding_model_version"] = "1"
            lines.append(json.dumps(doc))
        r = requests.post(f"{base}/_bulk",
                          data="\n".join(lines) + "\n",
                          headers={"Content-Type": "application/x-ndjson"},
                          timeout=300)
        resp = r.json()
        rejected = r.status_code == 429 or (
            resp.get("errors") and any(
                item["index"].get("status") == 429
                for item in resp.get("items", [])))
        if rejected:
            # Backpressure: slow the producer, never retry-storm the cluster
            print(f"  bulk rejection at {i}, backing off 10s and halving batch")
            batch_size = max(50, batch_size // 2)
            time.sleep(10)
            continue
        if resp.get("errors"):
            failed = [it["index"] for it in resp["items"]
                      if it["index"].get("error")]
            raise RuntimeError(
                f"{len(failed)} docs failed, first: "
                f"{json.dumps(failed[0])[:400]}. Do not continue silently: "
                "docs indexed without embeddings break retrieval later.")
        i += len(batch)
        sent += len(batch)
        print(f"  indexed {sent}/{total} (batch={batch_size}, "
              f"took={resp['took']}ms)")
    return sent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-id", required=True)
    ap.add_argument("--dimension", type=int, default=384)
    ap.add_argument("--chunks", default="../output/chunks.jsonl")
    ap.add_argument("--batch-size", type=int, default=200)
    ap.add_argument("--index-version", default="v1")
    args = ap.parse_args()

    base = os.environ["OS_URL"].rstrip("/")
    index_name = f"support-docs-{args.index_version}"

    print("1/5 ingest pipeline")
    put(base, "_ingest/pipeline/support-embed",
        ingest_pipeline(args.model_id))

    print("2/5 index + alias")
    put(base, index_name, index_body(args.dimension))
    requests.post(f"{base}/_aliases", json={"actions": [
        {"add": {"index": index_name, "alias": ALIAS}}]}, timeout=30)

    print("3/5 search pipeline support-hybrid-rrf")
    put(base, "_search/pipeline/support-hybrid-rrf", HYBRID_RRF)

    print("4/5 search pipeline support-hybrid-weighted")
    put(base, "_search/pipeline/support-hybrid-weighted", HYBRID_WEIGHTED)

    print("5/5 bulk load")
    n = bulk_load(base, args.chunks, args.model_id, args.batch_size,
                  index_name)
    print(f"Done. {n} chunks indexed into {index_name} (alias {ALIAS}).")


if __name__ == "__main__":
    main()
