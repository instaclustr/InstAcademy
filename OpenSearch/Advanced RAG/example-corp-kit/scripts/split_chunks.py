"""
Lab 4: load one asset family from chunks.jsonl into its purpose-built
index. The index itself is created by the copy-paste requests in the
lab; this script only does the batching loop.

For vector indexes it sends batches through the support-embed pipeline
(?pipeline=), so embedding happens server-side exactly as in Lab 1. The
issues index skips the pipeline: 15 exact records with literal error
codes make vector overhead pure waste (lesson 4.2).

Standard library only. Usage:
    python3 scripts/split_chunks.py --family tickets --model-id <MODEL_ID> \
        --chunks corpus/example-corp-corpus-v2.1.0/chunks.jsonl
"""
import argparse
import functools
import json
import sys
import time
from pathlib import Path

from oscommon import request

print = functools.partial(print, flush=True)

FAMILIES = {
    # family: (doc_types, index, embed?)
    "docs":    (["product-docs", "integration-guide"], "support-docs-v2", True),
    "tickets": (["support-ticket"], "support-tickets-v1", True),
    "issues":  (["known-issue"], "support-issues-v1", False),
    "api":     (["api-reference"], "support-api-v1", True),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=sorted(FAMILIES))
    ap.add_argument("--model-id", required=True)
    ap.add_argument("--chunks", required=True)
    ap.add_argument("--batch-size", type=int, default=100)
    args = ap.parse_args()

    doc_types, index, embed = FAMILIES[args.family]
    docs = [c for c in
            (json.loads(l) for l in
             Path(args.chunks).read_text().splitlines() if l.strip())
            if c["doc_type"] in doc_types]

    path = "_bulk" + ("?pipeline=support-embed" if embed else "")
    total, sent, batch_size = len(docs), 0, args.batch_size

    # resume support, same as Lab 1's loader
    status, resp = request("GET", f"{index}/_count")
    already = resp.get("count", 0) if status == 200 else 0
    i = max(0, already - batch_size)
    if i:
        print(f"  resuming: {already} docs already indexed")
    sent = i

    while i < len(docs):
        batch = docs[i:i + batch_size]
        lines = []
        for c in batch:
            lines.append(json.dumps(
                {"index": {"_index": index, "_id": c["chunk_id"]}}))
            doc = dict(c)
            doc["embedding_model_id"] = args.model_id if embed else None
            doc["embedding_model_version"] = "1" if embed else None
            lines.append(json.dumps(
                {k: v for k, v in doc.items() if v is not None}))
        try:
            status, resp = request("POST", path,
                                   ndjson="\n".join(lines) + "\n",
                                   timeout=600)
        except OSError as e:
            print(f"  timeout at {i} ({e}): waiting 30s, halving batch")
            batch_size = max(25, batch_size // 2)
            time.sleep(30)
            continue
        if status == 429:
            print(f"  bulk rejection at {i}: backing off 10s, halving batch")
            batch_size = max(25, batch_size // 2)
            time.sleep(10)
            continue
        if status >= 300 or resp.get("errors"):
            sys.exit(f"bulk failed HTTP {status}: {str(resp)[:400]}")
        i += len(batch)
        sent += len(batch)
        print(f"  {index}: {sent}/{total}")
        time.sleep(0.2)

    print(f"Done. {sent} chunks in {index}.")


if __name__ == "__main__":
    main()
