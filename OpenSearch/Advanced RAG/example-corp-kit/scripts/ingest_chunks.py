"""
Bulk load chunks.jsonl into the support-docs index (Lab 1).

The index, alias, and the support-embed ingest pipeline are created by
the copy-paste requests in the lab BEFORE this runs; this script only
does the part that needs a loop: batching 8,955 chunks through _bulk
with backpressure handling, per lesson 1.4.

Standard library only. Usage:
    export OS_URL=https://user:pass@your-cluster:9200
    python3 scripts/ingest_chunks.py --model-id <MODEL_ID> \
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-id", required=True)
    ap.add_argument("--chunks", required=True)
    ap.add_argument("--index", default="support-docs-v1")
    ap.add_argument("--batch-size", type=int, default=100)
    args = ap.parse_args()

    chunks = [json.loads(l)
              for l in Path(args.chunks).read_text().splitlines() if l.strip()]
    total, batch_size = len(chunks), args.batch_size
    started = time.time()

    # Auto-resume: chunks index in file order with stable _ids, so if a
    # previous run was interrupted, skip what is already there (minus one
    # batch of overlap; re-indexing the same _id is harmless).
    status, resp = request("GET", f"{args.index}/_count")
    already = resp.get("count", 0) if status == 200 else 0
    i = max(0, already - batch_size)
    if i:
        print(f"  resuming: {already} docs already indexed, "
              f"restarting from chunk {i}")
    sent = i
    while i < len(chunks):
        batch = chunks[i:i + batch_size]
        lines = []
        for c in batch:
            lines.append(json.dumps(
                {"index": {"_index": args.index, "_id": c["chunk_id"]}}))
            doc = dict(c)
            # model lineage per chunk, lesson 1.4
            doc["embedding_model_id"] = args.model_id
            doc["embedding_model_version"] = "1"
            lines.append(json.dumps(doc))
        try:
            status, resp = request("POST", "_bulk",
                                   ndjson="\n".join(lines) + "\n",
                                   timeout=600)
        except OSError as e:
            # Embedding a batch can outlast slow networks; the cluster is
            # fine, the client just stopped waiting. Ease off and retry.
            print(f"  timeout at {i} ({e}): waiting 30s, halving batch")
            batch_size = max(25, batch_size // 2)
            time.sleep(30)
            continue

        rejected = status == 429 or (
            isinstance(resp, dict) and resp.get("errors") and any(
                item["index"].get("status") == 429
                for item in resp.get("items", [])))
        if rejected:
            # Backpressure: slow the producer, never retry-storm the cluster
            print(f"  bulk rejection at {i}: backing off 10s, halving batch")
            batch_size = max(50, batch_size // 2)
            time.sleep(10)
            continue
        if status >= 300:
            sys.exit(f"bulk failed with HTTP {status}: {str(resp)[:400]}")
        if resp.get("errors"):
            failed = [it["index"] for it in resp["items"]
                      if it["index"].get("error")]
            sys.exit(f"{len(failed)} docs failed, first: "
                     f"{json.dumps(failed[0])[:400]}\n"
                     "Stopping loudly: docs indexed without embeddings "
                     "break retrieval later (lesson 1.4).")
        i += len(batch)
        sent += len(batch)
        print(f"  indexed {sent}/{total} (batch={batch_size}, "
              f"took={resp['took']}ms)")
        # be a polite tenant on a shared cluster
        time.sleep(0.2)

    mins = (time.time() - started) / 60
    print(f"Done. {sent} chunks indexed into {args.index} "
          f"in {mins:.1f} min.")


if __name__ == "__main__":
    main()
