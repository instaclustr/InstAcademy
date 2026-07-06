"""Lesson 2-2 Step 7: create an ingest pipeline that embeds passage_text.

An **ingest pipeline** is a named, server-side chain of **processors** that mutate
every document as it's indexed. Attach it to an index via ``default_pipeline`` and
you can index plain text — OpenSearch calls your deployed model and writes the
embedding into the doc for you. This decouples your application from embedding
generation entirely: clients write raw text, the cluster does the rest.
"""

import os
import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

# Load ``src/.env`` into os.environ before we read ML_MODEL_ID below.
from dotenv import load_dotenv

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

_ENV_FILE = _SRC_ROOT / ".env"
load_dotenv(_ENV_FILE)

client = open_search_client_from_env_file(_ENV_FILE)
print_opensearch_connection_test(client, raise_on_error=True)

# PUT _ingest/pipeline/<pipeline_id>
pipeline_id = "vector-search-embeddings-pipeline"
response = client.ingest.put_pipeline(
    id=pipeline_id,
    body={
        "description": "Generate passage_embedding from passage_text at index time",
        # The ``text_embedding`` processor reads ``passage_text``, calls the
        # deployed model, and writes the result into ``passage_embedding`` (the
        # knn_vector field the index mapping expects). ``field_map`` is
        # {source_field: dest_field}.
        "processors": [
            {
                "text_embedding": {
                    "model_id": os.getenv("ML_MODEL_ID"),
                    "field_map": {"passage_text": "passage_embedding"},
                }
            }
        ],
    },
)

if response.get("acknowledged"):
    print(f"Created ingest pipeline: {pipeline_id}")
else:
    print("Pipeline response:", response)
