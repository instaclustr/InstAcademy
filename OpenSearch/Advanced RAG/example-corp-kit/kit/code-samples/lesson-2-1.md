# Lesson 2.1 code samples: The Conversation Problem

## Conversation index mapping

Designed for the real access patterns: fetch by conversation, ordered by
turn, always filtered by tenant.

```json
PUT support-conversations
{
  "mappings": {
    "properties": {
      "conversation_id":     { "type": "keyword" },
      "turn":                { "type": "integer" },
      "role":                { "type": "keyword" },
      "text":                { "type": "text" },
      "created_at":          { "type": "date" },
      "tenant_id":           { "type": "keyword" },
      "retrieved_chunk_ids": { "type": "keyword" }
    }
  }
}
```

## Write a turn (with the retrieval breadcrumbs)

```json
POST support-conversations/_doc
{
  "conversation_id": "CONV-8841",
  "turn": 1,
  "role": "assistant",
  "text": "ERR-2209 is a TLS handshake failure. Enable TLS 1.3 in the connector advanced settings...",
  "created_at": "2026-07-02T14:03:22Z",
  "tenant_id": "northwind-logistics",
  "retrieved_chunk_ids": ["KI-0004#0.0", "GUIDE-002#3.0"]
}
```

## Read recent history (tenant filter is mandatory)

```json
GET support-conversations/_search
{
  "size": 6,
  "sort": [{ "turn": "desc" }],
  "query": {
    "bool": {
      "filter": [
        { "term": { "conversation_id": "CONV-8841" } },
        { "term": { "tenant_id": "northwind-logistics" } }
      ]
    }
  }
}
```

## Skip logic: rewrite only when the query depends on context

```python
import re

CONTEXT_DEPENDENT = re.compile(
    r"\b(it|that|this one|those|them|same|the (first|second|last) (one|option))\b"
    r"|^(what about|and on|how about|also)\b",
    re.IGNORECASE,
)

def needs_rewrite(query: str) -> bool:
    words = query.split()
    if len(words) <= 6:                 # fragments
        return True
    if CONTEXT_DEPENDENT.search(query): # pronouns / references
        return True
    return False

# "what about on version 4.9?"      -> True  (rewrite)
# "how do I fix ERR-2209?"          -> False (straight to retrieval)
```

## Rewrite prompt (LLM call, fired ~1/3 of turns)

```python
REWRITE_PROMPT = """You rewrite follow-up support questions so they stand alone.

Recent conversation:
{history}

Chunks used to answer the previous turn: {chunk_titles}

Follow-up question: {query}

Rewrite the follow-up as one standalone question that includes the product
area, any error code, and any version mentioned in the thread. Return only
the rewritten question."""
```

Turn 2 "what about on version 4.9?" rewrites to
"Does the ERR-2209 TLS workaround apply to the Snowflake connector on
version 4.9?" which restores the BM25 leg (code), the vector leg (topic),
and gives the 1.2 pre-filter a version to enforce.
