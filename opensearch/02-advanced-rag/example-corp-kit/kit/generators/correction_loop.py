"""
Chapter 3 on-camera demo: the corrective RAG loop against the the support tool
corpus, including the version mismatch case (ERR-2209, customer on 4.8,
fix requires 5.0).

The score gate and metadata grading run with no LLM at all, so the demo
works on any cluster. Plug a real LLM grader in via grade_with_llm() for
the full version (an Anthropic or ML Commons call slots in directly).

Usage:
    export OS_URL=https://user:pass@your-cluster:9200
    python correction_loop.py --query "how do I fix ERR-2209" \
        --customer-version 4.8
"""
import argparse
import json
import os
import re

import requests

MAX_RETRIES = 2
ERR_CODE = re.compile(r"\bERR-\d{4}\b")


def retrieve(base, index, query, version_filter=None, k=5):
    body = {"size": k,
            "_source": ["title", "text", "doc_type", "related_error_codes"],
            "query": {"match": {"text": query}}}
    if version_filter:
        body["query"] = {"bool": {
            "must": body["query"],
            "filter": [{"bool": {"should": [
                {"term": {"product_version": version_filter}},
                {"bool": {"must_not": {"exists": {"field": "product_version"}}}},
            ]}}],
        }}
    r = requests.post(f"{base}/{index}/_search", json=body, timeout=30)
    r.raise_for_status()
    return r.json()["hits"]["hits"]


def score_shape(hits):
    scores = [h["_score"] for h in hits]
    if not scores:
        return "empty"
    top = scores[0]
    sep = (top - scores[1]) / top if len(scores) > 1 and top else 0
    spread = (top - scores[-1]) / top if top else 0
    if sep < 0.05 and spread < 0.15:
        return "flat"
    if sep >= 0.15:
        return "clear_leader"
    return "uncertain"


def grade_metadata(hit, customer_version):
    """The check the version mismatch case demands: does the evidence
    fit THIS customer? Reads fields stamped at ingest (lesson 1.3).
    Swap in grade_with_llm() for semantic relevance grading too."""
    src = hit["_source"]
    text = src.get("text", "")
    m = re.search(r"[Ff]ixed in(?: version)?:? (\d\.\d)", text)
    if m and customer_version:
        fixed_in = m.group(1)
        if tuple(map(int, customer_version.split("."))) < \
           tuple(map(int, fixed_in.split("."))):
            # fix requires a newer version; is a workaround also present?
            if "workaround" not in text.lower() and \
               "Resolution:" not in text:
                return False, (f"version fit: fix requires {fixed_in}, "
                               f"customer on {customer_version}")
    return True, "ok"


def reformulate(query, reason, customer_version, base):
    if "version" in reason and customer_version:
        print(f"  correction: add hard version filter "
              f"product_version={customer_version}")
        return query, customer_version, "support-docs"
    codes = ERR_CODE.findall(query)
    if codes:
        # expand the code with its human title from the known issue
        hits = retrieve(base, "support-issues", codes[0], k=1)
        if hits:
            title = hits[0]["_source"]["title"]
            expanded = f"{query} {title}"
            print(f"  correction: expand query with known-issue title -> "
                  f"'{expanded}'")
            return expanded, None, "support-tickets"
    print("  correction: retry against ticket history "
          "(a human wrote down what worked)")
    return query, None, "support-tickets"


def run(base, query, customer_version):
    index, version_filter = "support-docs", None
    for attempt in range(MAX_RETRIES + 1):
        print(f"\nattempt {attempt}: index={index} "
              f"filter={version_filter or '-'} query='{query}'")
        hits = retrieve(base, index, query, version_filter)
        shape = score_shape(hits)
        print(f"  score shape: {shape} "
              f"(top={hits[0]['_score']:.2f})" if hits else "  no hits")

        if shape in ("flat", "empty"):
            reason = "flat scores"
        else:
            verdicts = [grade_metadata(h, customer_version) for h in hits]
            passing = [h for h, (ok, _) in zip(hits, verdicts) if ok]
            failing = [(h, r) for h, (ok, r) in zip(hits, verdicts) if not ok]
            for h, r in failing:
                print(f"  grader FAIL: {h['_source']['title'][:60]} ({r})")
            if passing:
                print(f"\nCONFIDENT after {attempt} correction(s). "
                      f"Evidence:")
                for h in passing[:3]:
                    print(f"  - [{h['_source']['doc_type']}] "
                          f"{h['_source']['title'][:70]}")
                return
            reason = failing[0][1] if failing else "no passing evidence"

        if attempt < MAX_RETRIES:
            query, version_filter, index = reformulate(
                query, reason, customer_version, base)

    print(f"\nLOW CONFIDENCE: retry budget ({MAX_RETRIES}) spent.")
    print("Signal to generation: evidence partial, state knowns and "
          "unknowns, escalate to a human with the trail attached.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default="how do I fix ERR-2209")
    ap.add_argument("--customer-version", default="4.8")
    args = ap.parse_args()
    run(os.environ["OS_URL"].rstrip("/"), args.query, args.customer_version)
