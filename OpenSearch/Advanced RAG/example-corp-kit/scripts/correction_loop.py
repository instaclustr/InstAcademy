"""
Chapter 3 demo: the corrective RAG loop against the Example Corp corpus,
including the version mismatch case (ERR-2209, customer on 4.8, fix
requires 5.0).

The score gate and metadata grading run with no LLM at all, so the demo
works on any cluster and gives every learner identical output. A real
deployment swaps grade_metadata() for an LLM grader (an ML Commons or
Anthropic call slots in directly); the loop shape stays identical.

Works right after Lab 1: all five asset types live in the single
support-docs index, so "retry against the ticket history" is a doc_type
filter, not a separate index.

Standard library only. Usage:
    export OS_URL=https://user:pass@your-cluster:9200
    python3 scripts/correction_loop.py --query "how do I fix ERR-2209" \
        --customer-version 4.8
"""
import argparse
import re
import sys

from oscommon import request

MAX_RETRIES = 2
INDEX = "support-docs"

# Attempt 0 searches the knowledge base (where canonical answers live);
# a correction can pivot to the ticket history (where human-verified
# resolutions live).
# (api-reference is excluded here: an endpoint page mentioning an error
# code is not a fix, and the metadata grader cannot read intent)
KB_TYPES = ["known-issue", "product-docs", "integration-guide"]

FIXED_IN = re.compile(r"[Ff]ixed in(?: version)?:? (\d\.\d)")
VERSION_GATE = re.compile(r"available in (\d\.\d) and later")
ERR_CODE = re.compile(r"\bERR-\d{4}\b")


def vtuple(v):
    return tuple(map(int, v.split(".")))


def retrieve(query, doc_types, version_filter=None, k=5):
    body = {"size": k,
            "_source": ["title", "text", "doc_type", "product_version",
                        "related_error_codes"],
            "query": {"match": {"text": query}}}
    filters = [{"terms": {"doc_type": doc_types}}]
    if version_filter:
        filters.append({"bool": {"should": [
            {"term": {"product_version": version_filter}},
            {"bool": {"must_not": {"exists": {"field": "product_version"}}}},
        ]}})
    body["query"] = {"bool": {"must": body["query"], "filter": filters}}
    status, resp = request("POST", f"{INDEX}/_search", body=body, timeout=60)
    if status >= 300:
        sys.exit(f"search failed HTTP {status}: {str(resp)[:300]}")
    return resp["hits"]["hits"]


def score_shape(hits):
    """The lesson 3.1 shape check: separation vs flat huddle."""
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


def grade_metadata(hit, customer_version, query):
    """The check the version mismatch case demands: does the evidence fit
    THIS question and THIS customer? Reads the metadata stamped into the
    chunk at ingest (lesson 1.3). Three rules:

    1. Topic fit: if the query names an error code, the chunk must
       actually cover that code (related_error_codes).
    2. If the chunk says the issue is fixed in a version NEWER than the
       customer's, the fix itself does not apply to them.
    3. A workaround only rescues the chunk if the workaround is not
       itself gated behind that newer version ("available in X and
       later").
    """
    src = hit["_source"]
    codes = ERR_CODE.findall(query)
    if codes:
        # the chunk must cover the code in its own text, not just
        # inherit it from parent-level metadata
        covered = set(src.get("related_error_codes") or [])
        text_body = src.get("text", "")
        missing = [c for c in codes
                   if c not in covered or c not in text_body]
        if missing:
            return False, f"topic fit: chunk does not cover {missing[0]}"

    if not customer_version:
        return True, "ok"
    text = src.get("text", "")
    cust = vtuple(customer_version)

    # Grade the section about the queried code, not the whole chunk;
    # a neighboring error's workaround must not rescue this one.
    seg = text
    if codes:
        m_sec = re.search(rf"### {codes[0]}.*?(?=\n### |\Z)", text, re.S)
        if m_sec:
            seg = m_sec.group(0)
            if "Resolution:" not in seg and "workaround" not in seg.lower():
                # lesson 1.3 anti-pattern caught in the wild: the chunker
                # split this entry before its fix
                return False, ("granularity: section truncated by a chunk "
                               "boundary before its resolution")

    gate = VERSION_GATE.search(seg)
    if gate and cust < vtuple(gate.group(1)):
        return False, (f"version fit: instructions require "
                       f"{gate.group(1)}, customer on {customer_version}")
    m = FIXED_IN.search(seg)
    if m and cust < vtuple(m.group(1)):
        if "workaround" in seg.lower() or "Resolution:" in seg:
            return True, "ok (ungated workaround present)"
        return False, (f"version fit: fix requires {m.group(1)}, "
                       f"customer on {customer_version}")
    return True, "ok"


def reformulate(query, reason, customer_version, version_filter, doc_types):
    """Escalation ladder from lesson 3.2, driven by the grader's reason
    and by what has already been tried."""
    if "version" in reason and customer_version and not version_filter:
        print(f"  correction 1: add hard version pre-filter "
              f"product_version={customer_version} (lesson 1.2)")
        return query, customer_version, doc_types
    print("  correction 2: pivot to the ticket history; somewhere in "
          "10,000 tickets a human wrote down what actually worked")
    return query, version_filter, ["support-ticket"]


def run(query, customer_version):
    version_filter, doc_types = None, KB_TYPES
    for attempt in range(MAX_RETRIES + 1):
        where = "knowledge base" if doc_types == KB_TYPES else "ticket history"
        print(f"\nattempt {attempt}: source={where} "
              f"version_filter={version_filter or '-'} query='{query}'")
        hits = retrieve(query, doc_types, version_filter)
        shape = score_shape(hits)
        if hits:
            print(f"  score shape: {shape} (top={hits[0]['_score']:.2f})")
        else:
            print("  no hits")

        # lesson 3.1: FLAT AND LOW is the alarm. Flat alone can just
        # mean many similar candidates (ticket dedupe territory).
        if shape == "empty" or (shape == "flat"
                                and hits[0]["_score"] < 2.0):
            reason = "flat and low scores (nothing really matched)"
            print(f"  score gate: {reason}, skip grading")
        else:
            verdicts = [grade_metadata(h, customer_version, query)
                        for h in hits]
            passing = [h for h, (ok, _) in zip(hits, verdicts) if ok]
            failing = [(h, r) for h, (ok, r) in zip(hits, verdicts) if not ok]
            for h, r in failing:
                print(f"  grader FAIL: {h['_source']['title'][:55]} ({r})")
            if passing:
                print(f"\nCONFIDENT after {attempt} correction(s). Evidence:")
                for h in passing[:3]:
                    print(f"  - [{h['_source']['doc_type']}] "
                          f"{h['_source']['title'][:70]}")
                return
            reason = failing[0][1] if failing else "no passing evidence"

        if attempt < MAX_RETRIES:
            query, version_filter, doc_types = reformulate(
                query, reason, customer_version, version_filter, doc_types)

    print(f"\nLOW CONFIDENCE: retry budget ({MAX_RETRIES}) spent.")
    print("Signal to generation: evidence partial, state knowns and "
          "unknowns, escalate to a human with the trail attached.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default="how do I fix ERR-2209")
    ap.add_argument("--customer-version", default="4.8")
    args = ap.parse_args()
    run(args.query, args.customer_version)
