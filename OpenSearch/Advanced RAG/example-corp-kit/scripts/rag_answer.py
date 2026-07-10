"""
End-to-end RAG answer: retrieve -> pack -> generate, using the remote
LLM deployed through the ML Commons connector (Lab 0's LLM step).

Retrieval is the tuned hybrid pipeline from Lab 1; packing dedupes on
parent_id and respects a token budget (lesson 2.2's split); generation
instructs the model to answer ONLY from the packed evidence and cite
chunk IDs.

Standard library only. Usage:
    python3 scripts/rag_answer.py --llm-id <LLM_MODEL_ID> \
        --model-id <EMBED_MODEL_ID> \
        --query "how do I fix ERR-2209" [--customer-version 4.8]
"""
import argparse
import json
import sys

from oscommon import request

INDEX = "support-docs"
KB_FILTER = {"terms": {
    "doc_type": ["product-docs", "integration-guide", "known-issue",
                 "api-reference"]}}
CONTEXT_BUDGET_WORDS = 1500  # ~2000 tokens of evidence


def retrieve(query, embed_model_id, k=8):
    lex = {"bool": {"must": {"match": {"text": query}},
                    "filter": [KB_FILTER]}}
    neural = {"query_text": query, "model_id": embed_model_id,
              "k": 50, "filter": KB_FILTER}
    body = {"size": k,
            "_source": ["chunk_id", "parent_id", "title", "parent_text",
                        "doc_type", "product_version"],
            "query": {"hybrid": {"queries": [
                lex, {"neural": {"embedding": neural}}]}}}
    status, resp = request(
        "POST", f"{INDEX}/_search?search_pipeline=support-hybrid-tuned",
        body=body, timeout=60)
    if status >= 300:
        sys.exit(f"retrieval failed HTTP {status}: {str(resp)[:300]}")
    return resp["hits"]["hits"]


def pack(hits):
    """Parent-child payoff: search matched the child, the model reads
    the parent. Dedupe parents, stay inside the evidence budget."""
    seen, blocks, words = set(), [], 0
    for h in hits:
        src = h["_source"]
        pid = src.get("parent_id") or src["chunk_id"]
        if pid in seen:
            continue
        text = src.get("parent_text") or ""
        n = len(text.split())
        if words + n > CONTEXT_BUDGET_WORDS and blocks:
            break
        seen.add(pid)
        words += n
        blocks.append(f"[{src['chunk_id']}] {src['title']}\n{text}")
    return "\n\n".join(blocks), [b.split("]")[0][1:] for b in blocks]


def generate(llm_id, query, evidence, customer_version):
    ctx = f"The customer is on product version {customer_version}. " \
        if customer_version else ""
    prompt = (
        "You are Example Corp's internal support assistant. Answer the "
        "agent's question using ONLY the evidence below. Cite the chunk "
        "IDs in square brackets for every claim. If the evidence does "
        "not fully answer the question, or does not apply to this "
        "customer's version, say so explicitly instead of guessing.\n\n"
        f"{ctx}Question: {query}\n\nEvidence:\n{evidence}\n\nAnswer:")
    # The connector splices ${parameters.prompt} into a JSON template,
    # so the prompt must arrive JSON-escaped (newlines, quotes).
    escaped = json.dumps(prompt)[1:-1]
    status, resp = request(
        "POST", f"_plugins/_ml/models/{llm_id}/_predict",
        body={"parameters": {"prompt": escaped}}, timeout=120)
    if status >= 300:
        sys.exit(f"generation failed HTTP {status}: {str(resp)[:400]}")
    # dataAsMap carries the provider's native response body
    try:
        out = resp["inference_results"][0]["output"][0]["dataAsMap"]
        if "candidates" in out:   # Gemini
            return out["candidates"][0]["content"]["parts"][0]["text"]
        if "message" in out:      # Cohere v2 chat
            return " ".join(p.get("text", "")
                            for p in out["message"]["content"]).strip()
        sys.exit(f"unrecognized provider payload: {str(out)[:400]}")
    except (KeyError, IndexError):
        sys.exit(f"unexpected LLM response shape: {str(resp)[:400]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--llm-id", required=True,
                    help="remote LLM model id from Lab 0's LLM step")
    ap.add_argument("--model-id", required=True,
                    help="embedding model id from Lab 0")
    ap.add_argument("--query", required=True)
    ap.add_argument("--customer-version", default=None)
    args = ap.parse_args()

    hits = retrieve(args.query, args.model_id)
    if not hits:
        sys.exit("retrieval returned nothing; is Lab 1 complete?")
    evidence, chunk_ids = pack(hits)
    print(f"packed {len(chunk_ids)} parent sections: {chunk_ids}\n")
    print(generate(args.llm_id, args.query, evidence,
                   args.customer_version))


if __name__ == "__main__":
    main()
