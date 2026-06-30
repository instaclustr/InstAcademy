"""Build an ingest pipeline that chunks book content and embeds each chunk.

Three-processor pipeline:
    1. ``text_chunking``: split ``content`` into fixed-length token windows,
       write them as a flat array into ``content_chunks``.
    2. ``script`` (Painless): turn the flat array into objects with
       ``{text, chunk_index}`` so each chunk has a stable index.
    3. ``text_embedding``: embed the full ``content`` (not the chunks) into
       a 768-dim ``content_embedding`` k-NN vector.

Note that step 3 embeds the *whole* document content into a single vector,
while step 1+2 keep the per-chunk text for nested keyword/RAG retrieval.
That's a common design when you want both whole-doc semantic recall AND
per-chunk grounding for an LLM.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

import json
import os


client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

pipeline_id = "bookstore-chunking-pipeline"
# Reuse the same model id from src/.env — must match the embedding model the
# index mapping was built around.
embedding_model_id = os.environ.get("ML_MODEL_ID", "")
pipeline_body = {
    "description": "Chunk book content for RAG embedding",
    "processors": [
        {
            "text_chunking": {
                "algorithm": {
                    "fixed_token_length": {
                        # 384 tokens — close to the practical input limit for
                        # most sentence transformer models. Larger chunks = more
                        # context per chunk but fewer chunks per doc.
                        "token_limit": 384,
                        # 20% overlap stops important phrases from being split
                        # across a hard chunk boundary.
                        "overlap_rate": 0.2,
                        "tokenizer": "standard",
                    }
                },
                "field_map": {
                    # Read ``content``, write the resulting chunks into ``content_chunks``.
                    "content": "content_chunks",
                },
            }
        },
        {
            "script": {
                # Painless: OpenSearch's sandboxed JVM scripting language.
                # Quick reference: ``ctx`` is the document being indexed,
                # ``ctx._source`` would be the source map. Inside an ingest
                # processor you access source fields directly as ``ctx.fieldname``.
                "lang": "painless",
                "source": """
                    if (ctx.content_chunks == null) {
                        ctx.content_chunks = [];
                    } else {
                        def normalized_chunks = [];
                        for (int i = 0; i < ctx.content_chunks.size(); i++) {
                            def chunk = ctx.content_chunks.get(i);
                            if (chunk != null) {
                                normalized_chunks.add([
                                    'text': chunk,
                                    'chunk_index': i
                                ]);
                            }
                        }
                        ctx.content_chunks = normalized_chunks;
                    }
                """,
            }
        },
        {
            "text_embedding": {
                "model_id": embedding_model_id,
                "field_map": {
                    # Embed full content, not the chunks. The whole-doc vector
                    # is what k-NN search will use; the chunk objects are kept
                    # for downstream RAG (passing text snippets to an LLM).
                    "content": "content_embedding",
                },
            }
        },
    ],
}

try:
    response = client.ingest.put_pipeline(id=pipeline_id, body=pipeline_body)
    print(json.dumps(response, indent=2))
    print(f"Pipeline '{pipeline_id}' created/updated successfully.")
except Exception as e:
    # Re-raise after logging so the script exits non-zero on failure —
    # important for CI-style runs of the full lesson.
    print(f"Failed to create/update pipeline '{pipeline_id}': {e}")
    raise
