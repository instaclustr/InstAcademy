"""
Build the golden query set for retrieval-only evaluation (lesson 1.3).

Queries are paraphrases of real support questions. Labels come from the
ticket -> source_id links created during ticket generation, expanded to
chunk level using chunks.jsonl. Output format:

    {"query_id": "Q-0001", "query": "...", "relevant_source_ids": [...],
     "relevant_chunk_ids": [...], "query_type": "error|howto|symptom"}

Usage:
    python generate_golden_set.py --count 200 --out ../output/golden_set.jsonl
"""
import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

PARAPHRASE = {
    "error": [
        "what does {code} mean",
        "how do I fix {code}",
        "{code} {etitle_lower}",
        "keep getting {etitle_lower}, what should I check",
    ],
    "howto": [
        "how to set up {feature}",
        "steps to configure {feature}",
        "{feature} configuration",
    ],
    "symptom": [
        "{symptom_lower}",
        "{symptom_lower} how to troubleshoot",
    ],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=200)
    ap.add_argument("--tickets", default="../output/tickets.jsonl")
    ap.add_argument("--chunks", default="../output/chunks.jsonl")
    ap.add_argument("--out", default="../output/golden_set.jsonl")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)

    # source_id -> chunk_ids (chunk-level labels beat doc-level labels;
    # a doc-level hit can hide a granularity problem)
    source_to_chunks = defaultdict(list)
    code_to_chunks = defaultdict(list)
    for line in Path(args.chunks).read_text().splitlines():
        c = json.loads(line)
        source_to_chunks[c["source_id"]].append(c["chunk_id"])
        for code in c.get("related_error_codes") or []:
            code_to_chunks[code].append(c["chunk_id"])

    tickets = [json.loads(l) for l in Path(args.tickets).read_text().splitlines()]
    labeled = [t for t in tickets if t.get("relevant_source_ids")]
    rng.shuffle(labeled)

    from taxonomy import ERROR_CODES
    seen_queries = set()
    golden = []
    for t in labeled:
        if len(golden) >= args.count:
            break
        code = t.get("error_code")
        if code and code in ERROR_CODES:
            etitle = ERROR_CODES[code][0]
            q = rng.choice(PARAPHRASE["error"]).format(
                code=code, etitle_lower=etitle.lower())
            qtype = "error"
            # Rank labels by asset relevance: the known issue record is the
            # canonical answer for an error code query
            priority = {"KI": 0, "GU": 1, "DO": 2, "AP": 3, "TK": 4}
            chunk_labels = sorted(
                set(code_to_chunks.get(code, [])),
                key=lambda c: (priority.get(c[:2], 5), c))[:12]
        else:
            q = t["subject"].lower().rstrip("?") + ""
            qtype = "howto"
            chunk_labels = sorted({cid for s in t["relevant_source_ids"]
                                   for cid in source_to_chunks.get(s, [])})[:12]
        if q in seen_queries or not chunk_labels:
            continue
        seen_queries.add(q)
        golden.append({
            "query_id": f"Q-{len(golden) + 1:04d}",
            "query": q,
            "query_type": qtype,
            "source_ticket": t["ticket_id"],
            "relevant_source_ids": t["relevant_source_ids"],
            "relevant_chunk_ids": chunk_labels,
        })

    Path(args.out).write_text("\n".join(json.dumps(g) for g in golden))
    print(f"Wrote {len(golden)} golden queries to {args.out}")


if __name__ == "__main__":
    main()
