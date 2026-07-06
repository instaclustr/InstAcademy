"""Run the same query with lexical-only then sparse-only, and print both rankings.

This is the "why hybrid?" demo: the two lists differ. BM25 (``match``) ranks by
exact term overlap; ``neural_sparse`` ranks by learned token importance, so it
surfaces thematically relevant books that don't share the exact query words.
Lesson 3-2 (``09-hybrid-search.py``) then fuses these two branches.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

_ENV_FILE = _SRC_ROOT / ".env"
load_dotenv(_ENV_FILE)

client = open_search_client_from_env_file(_ENV_FILE)
print_opensearch_connection_test(client, raise_on_error=True)

INDEX = "my-sparse-neural-index"
QUERY_TEXT = "a hero on a dangerous sea voyage"
model_id = (os.environ.get("ML_MODEL_ID") or "").strip()
if not model_id:
    print("Set ML_MODEL_ID in src/.env (deployed sparse encoding model).", file=sys.stderr)
    sys.exit(1)


def print_top(label, response):
    print(f"\n=== {label} ===")
    for i, hit in enumerate(response.get("hits", {}).get("hits", [])[:5], start=1):
        src = hit.get("_source", {})
        print(f"  {i}. score={hit.get('_score'):.4f} id={src.get('id')} title={src.get('title', '')[:60]}")


# --- Lexical only (BM25) ---
lexical = client.search(
    index=INDEX,
    body={
        "_source": {"excludes": ["passage_embedding", "passage_chunk"]},
        "size": 5,
        "query": {"match": {"passage_text": QUERY_TEXT}},
    },
)
print_top("Lexical only (BM25 match)", lexical)

# --- Sparse only (neural_sparse over nested chunks) ---
sparse = client.search(
    index=INDEX,
    body={
        "_source": {"excludes": ["passage_embedding", "passage_chunk"]},
        "size": 5,
        "query": {
            "nested": {
                "path": "passage_embedding",
                "score_mode": "max",
                "query": {
                    "neural_sparse": {
                        "passage_embedding.sparse_encoding": {
                            "query_text": QUERY_TEXT,
                            "model_id": model_id,
                        }
                    }
                },
            }
        },
    },
)
print_top("Sparse only (neural_sparse)", sparse)

print("\nCompare the two orderings — the gap between them is what hybrid search closes.")
