"""
Retrieval-only evaluation against the golden set (lesson 1.3 metrics).

Runs each golden query against OpenSearch and reports hit rate@k,
precision@k, and MRR, so you can run the Lab 1 ablation: bm25 vs neural
vs hybrid on identical data.

Standard library only. Usage:
    export OS_URL=https://user:pass@your-cluster:9200
    python3 scripts/eval_retrieval.py --mode bm25 --k 5 \
        --golden corpus/example-corp-corpus-v2.1.0/golden_set.jsonl
    python3 scripts/eval_retrieval.py --mode hybrid --k 5 \
        --model-id <MODEL_ID> --search-pipeline support-hybrid-rrf \
        --golden corpus/example-corp-corpus-v2.1.0/golden_set.jsonl
"""
import argparse
import json
import os
import sys
from pathlib import Path

from oscommon import request

INDEX = os.environ.get("OS_INDEX", "support-advrag-kb")

# The golden set labels answers in the knowledge base (docs, guides,
# known issues). Ticket chunks are where the golden QUERIES came from,
# so retrieving them back is circular, not correct. --kb-only scopes
# every eval query to the answer-bearing assets.
KB_FILTER = {"terms": {
    "doc_type": ["product-docs", "integration-guide", "known-issue",
                 "api-reference"]}}


def build_query(mode, query, model_id, k, kb_only, vector_field):
    if mode == "bm25":
        q = {"match": {"text": query}}
        if kb_only:
            q = {"bool": {"must": q, "filter": [KB_FILTER]}}
        return {"size": k, "_source": False, "query": q}
    if mode == "neural":
        neural = {"query_text": query, "model_id": model_id, "k": k * 10}
        if kb_only:
            neural["filter"] = KB_FILTER
        return {"size": k, "_source": False,
                "query": {"neural": {vector_field: neural}}}
    if mode == "hybrid":
        lex = {"match": {"text": query}}
        if kb_only:
            lex = {"bool": {"must": lex, "filter": [KB_FILTER]}}
        neural = {"query_text": query, "model_id": model_id, "k": k * 10}
        if kb_only:
            neural["filter"] = KB_FILTER
        return {"size": k, "_source": False,
                "query": {"hybrid": {"queries": [
                    lex, {"neural": {vector_field: neural}}]}}}
    raise ValueError(mode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["bm25", "neural", "hybrid"],
                    default="bm25")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--golden", required=True)
    ap.add_argument("--model-id", default=None)
    ap.add_argument("--search-pipeline", default=None,
                    help="support-hybrid-rrf or support-hybrid-weighted")
    ap.add_argument("--kb-only", action="store_true",
                    help="restrict retrieval to knowledge-base doc types")
    ap.add_argument("--vector-field", default="text_embedding",
                    help="knn_vector field the neural leg searches; must "
                         "match the index mapping (the course index "
                         "support-advrag-kb uses text_embedding)")
    args = ap.parse_args()

    if args.mode in ("neural", "hybrid") and not args.model_id:
        sys.exit(f"--model-id is required for mode={args.mode}")

    path = f"{INDEX}/_search"
    if args.search_pipeline:
        path += f"?search_pipeline={args.search_pipeline}"

    golden = [json.loads(l)
              for l in Path(args.golden).read_text().splitlines() if l.strip()]
    hits_at_k, precision_sum, rr_sum = 0, 0.0, 0.0

    for n_done, g in enumerate(golden, 1):
        body = build_query(args.mode, g["query"], args.model_id, args.k,
                           args.kb_only, args.vector_field)
        status, resp = request("POST", path, body=body, timeout=60)
        if status >= 300:
            sys.exit(f"query {n_done} failed HTTP {status}: "
                     f"{str(resp)[:300]}")
        returned = [h["_id"] for h in resp["hits"]["hits"]]
        relevant = set(g["relevant_chunk_ids"])

        rel_positions = [i for i, cid in enumerate(returned, 1)
                         if cid in relevant]
        if rel_positions:
            hits_at_k += 1
            rr_sum += 1.0 / rel_positions[0]
        precision_sum += len(rel_positions) / args.k
        if n_done % 50 == 0:
            print(f"  ...{n_done}/{len(golden)} queries", file=sys.stderr)

    n = len(golden)
    print(f"mode={args.mode} pipeline={args.search_pipeline or '-'} "
          f"kb_only={args.kb_only} "
          f"k={args.k} queries={n}")
    print(f"  hit_rate@{args.k}:  {hits_at_k / n:.3f}")
    print(f"  precision@{args.k}: {precision_sum / n:.3f}")
    print(f"  MRR:          {rr_sum / n:.3f}")


if __name__ == "__main__":
    main()
