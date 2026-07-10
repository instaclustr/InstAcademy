# Lesson 4.2 code samples: Multi-Index Agents

## Split the corpus along its natural seams

Runnable: `scripts/split_chunks.py` loads chunks.jsonl by doc_type
into four bulk files and creates the indexes plus aliases:

| Index | Contents | Retrieval strategy |
| --- | --- | --- |
| support-docs-v1 | product-docs + integration-guide | hybrid + parent-child |
| support-tickets-v1 | support-ticket | vector-weighted fusion |
| support-issues-v1 | known-issue | lexical first |
| support-api-v1 | api-reference | exact path + semantic |

## Per-index search pipelines (strategy per asset)

Tickets lean semantic (customers describe symptoms in customer words):

```json
PUT _search/pipeline/support-tickets-weighted
{
  "phase_results_processors": [
    { "normalization-processor": {
        "normalization": { "technique": "min_max" },
        "combination": { "technique": "arithmetic_mean",
                         "parameters": { "weights": [0.2, 0.8] } } } }
  ]
}
```

Known issues stay lexical (error codes are literal strings, corpus is
tiny): plain `match` query, no pipeline needed.

## The _msearch meta-tool: breadth in one round trip

```json
GET support-issues,support-docs,support-tickets,support-api/_msearch
{ "index": "support-issues" }
{ "size": 3, "query": { "match": { "text": "ERR-2209 handshake" } } }
{ "index": "support-docs" }
{ "size": 5, "query": { "match": { "text": "TLS setting connector 4.8" } } }
{ "index": "support-tickets" }
{ "size": 3, "query": { "match": { "text": "ERR-2209 resolved version 4.9" } } }
{ "index": "support-api" }
{ "size": 2, "query": { "match": { "text": "connector test endpoint" } } }
```

Tool guidance in the description: sequential calls when results should
steer the next step, _msearch when you need broad evidence fast.

## Aliases: tools never point at physical indexes

```json
POST /_aliases
{
  "actions": [
    { "add": { "index": "support-issues-v1", "alias": "support-issues" } },
    { "add": { "index": "support-tickets-v1", "alias": "support-tickets" } },
    { "add": { "index": "support-api-v1", "alias": "support-api" } }
  ]
}
```

When 1.4's model lifecycle forces a reindex, the alias flips and every
agent keeps working mid-conversation.

## Document-level security: law below the agent

Security plugin role restricting a tenant-scoped agent to its own
tickets (public knowledge stays readable):

```json
PUT _plugins/_security/api/roles/support_agent_northwind
{
  "index_permissions": [{
    "index_patterns": ["support-*"],
    "dls": "{\"bool\":{\"should\":[{\"term\":{\"acl\":\"public\"}},{\"term\":{\"tenant_id\":\"northwind-logistics\"}}]}}",
    "allowed_actions": ["read"]
  }]
}
```

An agent's instructions are suggestions. DLS is enforced in the cluster,
so a prompt cannot talk its way into another tenant's tickets.

---

# Lesson 4.3 code samples: Guardrails & Production

## Four ceilings, checked every loop iteration

```python
from dataclasses import dataclass, field
import time

@dataclass
class Ceilings:
    max_iterations: int = 5
    max_tokens: int = 12000        # enforced via 3.6 token usage tracking
    max_seconds: float = 30.0
    max_cost_usd: float = 0.25     # per conversation

@dataclass
class LoopState:
    started: float = field(default_factory=time.time)
    iterations: int = 0
    tokens: int = 0
    cost_usd: float = 0.0

def ceiling_hit(state: LoopState, c: Ceilings):
    if state.iterations >= c.max_iterations: return "iterations"
    if state.tokens >= c.max_tokens:         return "tokens"
    if time.time() - state.started >= c.max_seconds: return "wall_clock"
    if state.cost_usd >= c.max_cost_usd:     return "cost"
    return None

# Hitting a ceiling is NOT an error:
# stop -> answer from gathered evidence -> flag confidence -> escalate.
# Same graceful degradation as the chapter 3 retry budget.
```

## CRAG tool wrapper: every tool returns evidence + verdict

```python
def graded_tool(search_fn, grade_fn):
    def wrapped(query, customer_version):
        hits = search_fn(query)
        verdicts = grade_fn(query, hits, customer_version)   # ch3 grader
        return {
            "results": hits,
            "grade": summarize(verdicts),          # pass / weak / fail
            "reason": worst_reason(verdicts),      # e.g. "version fit"
        }
    return wrapped
# The agent observes evidence AND verdict together, so weak evidence
# triggers an immediate reformulated call instead of a confident answer.
```

## Semantic answer cache in front of the agent

Same `support-cache-embed` pipeline as the routing cache (lesson 4.1),
field-mapped `query_text` -> `query_embedding`.

```json
PUT support-answer-cache
{
  "settings": { "index": { "knn": true, "default_pipeline": "support-cache-embed" } },
  "mappings": {
    "properties": {
      "query_text":      { "type": "text" },
      "query_embedding": { "type": "knn_vector", "dimension": 384,
        "method": { "name": "hnsw", "engine": "faiss",
                    "space_type": "innerproduct" } },
      "answer":          { "type": "text" },
      "source_chunk_ids":{ "type": "keyword" },
      "product_version": { "type": "keyword" },
      "plan_tier":       { "type": "keyword" },
      "created_at":      { "type": "date" }
    }
  }
}
```

Lookup, scoped by version and tier, conservative threshold:

```json
GET support-answer-cache/_search
{
  "size": 1,
  "min_score": 1.7,
  "query": {
    "bool": {
      "must": { "neural": { "query_embedding": {
        "query_text": "snowflake schema discovery timeout",
        "model_id": "<MODEL_ID>", "k": 3 } } },
      "filter": [
        { "term": { "product_version": "4.9" } },
        { "term": { "plan_tier": "professional" } }
      ]
    }
  }
}
```

Invalidation is wired to the 1.4 update patterns: the nightly docs sync
and the known-issues webhook delete cache entries whose
source_chunk_ids were touched.

```json
POST support-answer-cache/_delete_by_query
{
  "query": { "terms": { "source_chunk_ids": ["KI-0004#0.0", "GUIDE-002#3.0"] } }
}
```

## Structured tool failure (never crash, never silently retry)

```python
def safe_tool_call(tool, *args, timeout=8):
    try:
        return tool(*args)
    except TimeoutError:
        return {"error": "timeout",
                "guidance": "Fall back to support-docs and note the gap "
                            "in your answer."}
    except Exception as e:
        return {"error": type(e).__name__,
                "guidance": "Try an alternative index or answer from "
                            "evidence gathered so far with reduced "
                            "confidence."}
# Structured errors are observations the agent can reason about.
```

## Agent trace document (extends the 3.3 traces index)

```json
POST support-traces/_doc
{
  "request_id": "REQ-99213",
  "agent_run": {
    "iterations": 2,
    "token_usage": { "input": 3812, "output": 921 },
    "steps": [
      { "reason": "error-code shaped, check known issues first",
        "tool": "search_known_issues",
        "args": { "query": "schema discovery timeout" },
        "grade": "pass" },
      { "reason": "workaround applies to 4.9, get exact steps",
        "tool": "search_docs",
        "args": { "query": "Snowflake schema scope setting" },
        "grade": "pass" }
    ],
    "ceiling_events": []
  }
}
```
