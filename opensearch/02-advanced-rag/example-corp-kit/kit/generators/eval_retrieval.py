"""
Retrieval-only evaluation against the golden set (lesson 1.3 metrics).

Runs each golden query against OpenSearch and reports hit rate@k,
precision@k, and MRR. Works with match (BM25), neural, or hybrid queries
so you can demo the ablation table on camera.

Usage:
    export OS_URL=https://user:pass@your-cluster:9200
    python eval_retrieval.py --mode bm25 --k 5
    python eval_retrieval.py --mode hybrid --k 5 --model-id <model_id> \
        --search-pipeline support-hybrid-rrf
"""
import argparse
import json
import os
from pathlib import Path

import requests

INDEX = os.environ.get("OS_INDEX", "support-docs")


def build_query(mode, query, model_id, k):
    if mode == "bm25":
        return {"size": k, "_source": False,
                "query": {"match": {"text": query}}}
    if mode == "neural":
        return {"size": k, "_source": False,
                "query": {"neural": {"embedding": {
                    "query_text": query, "model_id": model_id, "k": k * 10}}}}
    if mode == "hybrid":
        return {"size": k, "_source": False,
                "query": {"hybrid": {"queries": [
                    {"match": {"text": query}},
                    {"neural": {"embedding": {
                        "query_text": query, "model_id": model_id,
                        "k": k * 10}}},
                ]}}}
    raise ValueError(mode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["bm25", "neural", "hybrid"],
                    default="bm25")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--golden", default="../output/golden_set.jsonl")
    ap.add_argument("--model-id", default=None)
    ap.add_argument("--search-pipeline", default=None,
                    help="e.g. support-hybrid-rrf or support-hybrid-weighted (hybrid mode)")
    args = ap.parse_args()

    base = os.environ["OS_URL"].rstrip("/")
    url = f"{base}/{INDEX}/_search"
    if args.search_pipeline:
        url += f"?search_pipeline={args.search_pipeline}"

    golden = [json.loads(l) for l in Path(args.golden).read_text().splitlines()]
    hits_at_k = 0
    precision_sum = 0.0
    rr_sum = 0.0

    for g in golden:
        body = build_query(args.mode, g["query"], args.model_id, args.k)
        r = requests.post(url, json=body, timeout=30, verify=True)
        r.raise_for_status()
        returned = [h["_id"] for h in r.json()["hits"]["hits"]]
        relevant = set(g["relevant_chunk_ids"])

        rel_positions = [i for i, cid in enumerate(returned, 1)
                         if cid in relevant]
        if rel_positions:
            hits_at_k += 1
            rr_sum += 1.0 / rel_positions[0]
        precision_sum += len(rel_positions) / args.k

    n = len(golden)
    print(f"mode={args.mode} pipeline={args.search_pipeline or '-'} "
          f"k={args.k} queries={n}")
    print(f"  hit_rate@{args.k}:  {hits_at_k / n:.3f}")
    print(f"  precision@{args.k}: {precision_sum / n:.3f}")
    print(f"  MRR:          {rr_sum / n:.3f}")


if __name__ == "__main__":
    main()
