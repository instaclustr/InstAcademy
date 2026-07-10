# Lesson 2.3 code samples: Query Enhancement Patterns

## HyDE: retrieve with a hypothetical, generate from the real chunks

```python
HYDE_PROMPT = """Write one short documentation paragraph that would answer
this customer question about a BI platform. Use precise product
vocabulary (dashboards, render, refresh, connector, timeout). Do not
address the customer. Return only the paragraph.

Question: {query}"""

def hyde_retrieve(client, query, model_id, k=10):
    hypothetical = llm(HYDE_PROMPT.format(query=query))
    return client.search(index="support-docs", body={
        "size": k,
        "query": {"neural": {"embedding": {
            "query_text": hypothetical,   # embed the fiction
            "model_id": model_id,
            "k": k * 10,
        }}},
    })
# "dashboards are acting weird lately" -> hypothetical mentions render
# timeouts and cross-filters -> lands on the real performance page.
```

## Decomposition via _msearch: one round trip, parallel sub-queries

"Does the Salesforce connector support OAuth, and how do I rotate the
credentials?" decomposes into two searches in a single request:

```json
GET support-docs/_msearch
{ }
{ "size": 5, "query": { "match": { "text": "Salesforce connector OAuth support" } } }
{ }
{ "size": 5, "query": { "match": { "text": "connector credential rotation ERR-2231" } } }
```

```python
def branched_retrieve(client, sub_queries, index="support-docs", k=5):
    body = []
    for q in sub_queries:
        body.append({})
        body.append({"size": k, "query": {"match": {"text": q}}})
    responses = client.msearch(index=index, body=body)["responses"]
    seen, merged = set(), []
    for sub_q, resp in zip(sub_queries, responses):
        for hit in resp["hits"]["hits"]:
            if hit["_id"] not in seen:          # dedupe on chunk_id
                seen.add(hit["_id"])
                hit["_sub_query"] = sub_q       # keep attribution
                merged.append(hit)
    return merged
```

## Adaptive triggering: the cheap router in front of everything

```python
import re

ERR_CODE = re.compile(r"\bERR-\d{4}\b")
COMPOUND = re.compile(r"\b(and|versus|vs\.?|or)\b", re.IGNORECASE)
TECH_VOCAB = re.compile(
    r"\b(connector|dashboard|dataset|refresh|API|SSO|SCIM|webhook|alert)\b",
    re.IGNORECASE)

def route(query: str, needs_rewrite) -> str:
    if needs_rewrite(query):        # from lesson 2.1
        return "rewrite"
    if COMPOUND.search(query) and len(query.split()) > 8:
        return "decompose"
    if not ERR_CODE.search(query) and not TECH_VOCAB.search(query):
        return "hyde"               # vague: no code, no product vocabulary
    return "straight_through"       # most traffic: full speed Ch1 pipeline
```

Routing itself must stay cheap: an ERR pattern match is a free,
unambiguous signal. If the router costs as much as the enhancement it
gates, you gained nothing.
