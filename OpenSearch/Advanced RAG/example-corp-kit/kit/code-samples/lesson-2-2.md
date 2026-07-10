# Lesson 2.2 code samples: Memory Strategies & Token Management

## Hybrid memory assembly (summary of the old + verbatim recent)

```python
def build_memory_block(turns, summary, budget_tokens=2000,
                       verbatim_turns=4):
    """Summary holds the plot, the window holds the details."""
    recent = turns[-verbatim_turns:]
    recent_text = "\n".join(f"{t['role']}: {t['text']}" for t in recent)
    block = f"Conversation summary:\n{summary}\n\nRecent turns:\n{recent_text}"
    while approx_tokens(block) > budget_tokens and verbatim_turns > 2:
        verbatim_turns -= 1
        recent = turns[-verbatim_turns:]
        recent_text = "\n".join(f"{t['role']}: {t['text']}" for t in recent)
        block = f"Conversation summary:\n{summary}\n\nRecent turns:\n{recent_text}"
    return block

def approx_tokens(text):
    return int(len(text.split()) * 1.3)
```

## Explicit token budget (write it down, enforce it)

```python
CONTEXT_BUDGET = {
    "total":            8000,
    "retrieved_chunks": 4000,   # evidence is never crowded out
    "memory":           2000,   # summarize harder if exceeded
    "instructions":     1200,
    "headroom":          800,
}
```

## ISM policy: session expiry (ISM, not ILM)

Rolls conversation indexes daily and deletes them past a 90 day
retention window.

```json
PUT _plugins/_ism/policies/support-conversation-retention
{
  "policy": {
    "description": "Roll daily, delete conversations after 90 days",
    "default_state": "active",
    "states": [
      {
        "name": "active",
        "actions": [
          { "rollover": { "min_index_age": "1d" } }
        ],
        "transitions": [
          { "state_name": "delete", "conditions": { "min_index_age": "90d" } }
        ]
      },
      {
        "name": "delete",
        "actions": [ { "delete": {} } ]
      }
    ],
    "ism_template": [
      { "index_patterns": ["support-conversations-*"], "priority": 100 }
    ]
  }
}
```

## ML Commons Memory API (the native alternative, 2.12+)

Create a memory, then log each question/answer pair as a message.

```json
POST /_plugins/_ml/memory
{
  "name": "CONV-8841 northwind-logistics"
}
```

```json
POST /_plugins/_ml/memory/<MEMORY_ID>/messages
{
  "input": "what about on version 4.9?",
  "prompt_template": "<the assembled prompt>",
  "response": "On 4.9 the TLS 1.3 setting is not available yet...",
  "origin": "support-tool",
  "additional_info": { "tenant_id": "northwind-logistics", "turn": 2 }
}
```

Conversational search pipelines can then carry the memory ID in
`generative_qa_parameters` so context handling happens in the cluster.

3.6 note: the agent framework's agentic memory (memory containers,
introduced 3.3) goes further, extracting and persisting facts across
sessions. Chapter 4 uses it; the create call lives in lesson-4-1.md.
