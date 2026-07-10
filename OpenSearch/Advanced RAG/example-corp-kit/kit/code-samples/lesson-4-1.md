# Lesson 4.1 code samples: Routing & the ReAct Loop

## Layered router: rules > classifier > LLM

```python
import re

ERR_CODE = re.compile(r"\bERR-\d{4}\b")
API_HINT = re.compile(r"\b(endpoint|API|/v2/|curl|rate limit|webhook)\b", re.I)
COMPARE  = re.compile(r"\b(vs\.?|versus|difference between|compare)\b", re.I)

def route(query: str) -> str:
    # Layer 1: rules catch the unambiguous, for free
    if ERR_CODE.search(query):
        return "known_issues_path"
    if COMPARE.search(query):
        return "comparison_path"
    if API_HINT.search(query):
        return "api_path"
    # Layer 2: cached decision?
    cached = route_cache_lookup(query)
    if cached:
        return cached
    # Layer 3: LLM router for the genuinely weird, then cache it
    decision = llm_route(query)
    route_cache_store(query, decision)
    return decision
```

## The classification cache in OpenSearch

Uses the `support-cache-embed` ingest pipeline (same `text_embedding`
pattern as `support-embed` in lesson 1.4, field-mapped
`query_text` -> `query_embedding`) to embed cache entries server-side.

```json
PUT support-route-cache
{
  "settings": { "index": { "knn": true, "default_pipeline": "support-cache-embed" } },
  "mappings": {
    "properties": {
      "query_text":      { "type": "text" },
      "query_embedding": { "type": "knn_vector", "dimension": 384,
        "method": { "name": "hnsw", "engine": "faiss",
                    "space_type": "innerproduct" } },
      "route":           { "type": "keyword" },
      "created_at":      { "type": "date" }
    }
  }
}
```

Semantic lookup (same 20 questions, 40 different outfits):

```json
GET support-route-cache/_search
{
  "size": 1,
  "min_score": 1.7,
  "query": { "neural": { "query_embedding": {
    "query_text": "how do I set up report bursting",
    "model_id": "<MODEL_ID>", "k": 1 } } }
}
```

The savings math on screen: 500 tickets/day, 70% cache hit rate, LLM
routing spend drops 70%, every day.

## Tool descriptions: the unglamorous design lever

```python
TOOLS = [
  {
    "name": "search_known_issues",
    "description": (
      "Searches Example Corp known issues. Returns error code, symptom, "
      "root cause, workaround, affected_versions, fixed_in_version. "
      "PREFER THIS for error codes (ERR-XXXX) and version-specific "
      "failures. Small, exact corpus."),
  },
  {
    "name": "search_docs",
    "description": (
      "Searches product documentation and integration guides (hybrid, "
      "parent-child). Returns full sections with settings tables. Prefer "
      "for how-to and configuration questions."),
  },
  {
    "name": "search_tickets",
    "description": (
      "Searches 3 years of resolved support tickets. Returns problem + "
      "human-verified resolution. Prefer when you need what actually "
      "worked for another customer, especially on older versions."),
  },
  {
    "name": "search_api_reference",
    "description": (
      "Searches the REST API reference by endpoint path and description. "
      "Returns method, parameters, error codes, curl example. Prefer for "
      "endpoint, parameter, and rate limit questions."),
  },
]
```

Bad description: "searches docs". The agent chooses tools by reading
these strings and nothing else. Write them like documentation for a
sharp new teammate on day one.

## 3.6: token usage tracking + agentic memory

The 3.6 agent framework reports token usage per interaction in the
response, normalized across providers. Log it on every trace; the 4.3
token ceiling is enforced against this number.

Agentic memory container (3.3+, used by the conversational agent):

```json
POST /_plugins/_ml/memory_containers/_create
{
  "name": "support-agent-memory",
  "configuration": {
    "embedding_model_type": "TEXT_EMBEDDING",
    "embedding_model_id": "<EMBED_MODEL_ID>",
    "llm_id": "<LLM_MODEL_ID>",
    "strategies": [
      { "type": "SUMMARY",  "namespace": ["tenant_id", "session_id"] },
      { "type": "SEMANTIC", "namespace": ["tenant_id"] }
    ]
  }
}
```
