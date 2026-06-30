"""Create an ingest pipeline that chunks text then sparse-encodes into nested passage_embedding.

Pipeline flow (top to bottom):
    1. ``text_chunking``: split ``passage_text`` into fixed-length token chunks,
       write them into ``passage_chunk`` (an array of strings).
    2. ``sparse_encoding``: for each chunk, call the deployed sparse model and
       emit a nested object with ``sparse_encoding`` (token -> weight) under
       ``passage_embedding``.

The result matches the mapping created in ``003-sparse-data-index.py`` so a
``neural_sparse`` query over the nested field can score per-chunk.

Why chunking?
    Sparse encoders (and dense ones) have a max sequence length. Long passages
    get truncated unless we split them into smaller chunks. Chunking also
    improves precision — a query is more likely to find a relevant short
    passage than to find a long doc that's only partly relevant.
"""

import os
import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import (
    load_src_dotenv,
    open_search_client_from_env_file,
    print_opensearch_connection_test,
    src_env_file,
)

load_src_dotenv(__file__)

# Fail fast with a helpful message if the lab hasn't deployed/configured the
# sparse model yet. Without ``ML_MODEL_ID`` the pipeline can't be built.
if not (os.environ.get("ML_MODEL_ID") or "").strip():
    print("Set ML_MODEL_ID in src/.env (deployed sparse encoding model).", file=sys.stderr)
    sys.exit(1)

client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# Chunk source text into passage_chunk, then encode each chunk into nested
# passage_embedding (see OpenSearch: "Text chunking using a sparse encoding processor").
pipeline_id = "nlp-ingest-pipeline"
response = client.ingest.put_pipeline(
    id=pipeline_id,
    body={
        "description": "A sparse encoding ingest pipeline",
        "processors": [
            {
                "text_chunking": {
                    "algorithm": {
                        # ``fixed_token_length`` chunks by token count rather
                        # than characters (smarter for ML inputs).
                        "fixed_token_length": {
                            # 5 tokens per chunk is unusually small — kept low
                            # for this lesson so you can clearly see the per-chunk
                            # output. Real apps use 128–512.
                            "token_limit": 5,
                            # 50% overlap so important phrases that span a chunk
                            # boundary still get encoded together at least once.
                            "overlap_rate": 0.5,
                            # ``standard`` is the default OpenSearch text analyzer.
                            "tokenizer": "standard",
                        }
                    },
                    # Read from passage_text, write the array of chunks into passage_chunk.
                    "field_map": {
                        "passage_text": "passage_chunk",
                    },
                },
            },
            {
                "sparse_encoding": {
                    "model_id": os.environ.get("ML_MODEL_ID"),
                    # ``prune_type`` + ``prune_ratio`` discard low-weight tokens
                    # to keep the sparse vector small. ``max_ratio`` 0.1 means
                    # we keep only weights >= 10% of the max weight in that vector.
                    # Lower ratio = more accurate but bigger vectors.
                    "prune_type": "max_ratio",
                    "prune_ratio": 0.1,
                    # Per-chunk encoding writes nested objects under passage_embedding.
                    "field_map": {
                        "passage_chunk": "passage_embedding",
                    },
                }
            },
        ],
    },
)

if response.get("acknowledged"):
    print(f"Created ingest pipeline: {pipeline_id}")
else:
    print("Response:", response)

# Attach the pipeline to the target index as the **default** — every document
# indexed into ``my-sparse-neural-index`` now goes through chunking + encoding
# unless the indexing call explicitly disables it.
index_name = "my-sparse-neural-index"
client.indices.put_settings(
    index=index_name,
    body={"index": {"default_pipeline": pipeline_id}},
)
print(f"Attached pipeline {pipeline_id} to index {index_name} (default_pipeline)")
