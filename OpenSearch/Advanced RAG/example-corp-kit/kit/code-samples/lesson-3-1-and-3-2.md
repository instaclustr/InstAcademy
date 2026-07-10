# Lesson 3.1 code samples: Retrieval Diagnostics

## Score shape check: healthy separation vs flat huddle

```python
def score_shape(hits):
    """Cheapest retrieval alarm you can build. Runs on every request."""
    scores = [h["_score"] for h in hits]
    if not scores:
        return {"verdict": "empty"}
    top = scores[0]
    separation = (top - scores[1]) / top if len(scores) > 1 and top else 0.0
    spread = (top - scores[-1]) / top if top else 0.0
    if separation < 0.05 and spread < 0.15:
        return {"verdict": "flat", "top": top}       # nothing really matched
    if separation >= 0.15:
        return {"verdict": "clear_leader", "top": top}
    return {"verdict": "uncertain", "top": top}
```

Compare relative shape, never absolute values: BM25 scores and fused
hybrid scores live on different scales.

## _explain: why did this chunk win?

```json
GET support-docs/_search
{
  "explain": true,
  "size": 3,
  "query": { "match": { "text": "ERR-2209 connector handshake" } }
}
```

The explanation decomposes each score into term matches and clause
contributions. In the version mismatch case, _explain shows a perfectly
healthy ERR-2209 match, which is the point: score diagnostics catch weak
retrieval, not relevant-but-wrong-fit retrieval. That needs a grader.

---

# Lesson 3.2 code samples: The Correction Loop

Full runnable version: `scripts/correction_loop.py`. The pieces:

## Pass 1: the _score gate (free)

```python
def score_gate(hits):
    shape = score_shape(hits)
    if shape["verdict"] == "clear_leader":
        return "proceed"
    if shape["verdict"] in ("flat", "empty"):
        return "correct"      # do not grade garbage
    return "grade"            # middle band goes to the LLM grader
```

## Pass 2: the LLM grader (reads, checks fit)

```python
GRADER_PROMPT = """Grade whether this chunk supports answering the
customer's question. Answer in JSON only:
{{"relevant": true/false, "version_fit": true/false/null, "reason": "..."}}

Customer question: {query}
Customer product version: {customer_version}

Chunk metadata:
  affected_versions: {affected}
  fixed_in_version: {fixed_in}
Chunk text:
{chunk_text}

version_fit is false if the chunk's fix or workaround requires a version
newer than the customer's."""
```

The grader compares `customer_version` (from the ticket) against
`affected_versions` / `fixed_in_version` (stamped at ingest in lesson
1.3). This is what catches a 4.8 customer being handed the 5.0-only
TLS setting for ERR-2209.

## Correction moves, driven by the grader's reason

```python
def reformulate(query, reason, customer_version, error_codes):
    if "version" in reason:
        # hard pre-filter: 5.0-only content cannot enter the candidate set
        return query, {"term": {"product_version": customer_version}}
    if error_codes:
        code = error_codes[0]
        title = ERROR_CODE_TITLES.get(code, "")
        return f"{query} {title}", None   # expand code with its title
    return distill(query), None           # strip customer noise
```

## The retry budget (the discipline)

```python
MAX_RETRIES = 2

def corrective_retrieve(client, query, customer_version):
    filters = None
    for attempt in range(MAX_RETRIES + 1):
        hits = retrieve(client, query, filters)
        decision = score_gate(hits)
        if decision == "proceed":
            return hits, "confident", attempt
        if decision == "grade":
            verdicts = grade(query, hits, customer_version)
            passing = [h for h, v in zip(hits, verdicts) if v["relevant"]
                       and v.get("version_fit") is not False]
            if passing:
                return passing, "confident", attempt
            reason = next(v["reason"] for v in verdicts if not v["relevant"]
                          or v.get("version_fit") is False)
        else:
            reason = "flat scores"
        if attempt < MAX_RETRIES:
            query, filters = reformulate(query, reason,
                                         customer_version, find_codes(query))
    return hits, "low_confidence", MAX_RETRIES   # answer honestly + escalate
```

## Confidence signaling to the generation prompt

```python
LOW_CONFIDENCE_BANNER = """NOTE: The retrieved evidence is partial or may
not match the customer's version. State clearly what is known and what is
not. Do not guess. Recommend escalation to a support engineer."""
```
