"""Create an ingest pipeline that turns ``passage_text`` into embeddings on the fly.

What's an "ingest pipeline"?
    A named, server-side chain of **processors** that mutate every document
    as it's indexed. Once attached to an index (via ``default_pipeline``),
    you can index plain text and OpenSearch will quietly call your deployed
    ML model and write the embedding into the doc for you.

This decouples your application from embedding generation entirely — clients
just write the raw text, the cluster does the rest.
"""

import os
import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import (
    load_src_dotenv,
    open_search_client_from_env_file,
    print_opensearch_connection_test,
    src_env_file,
)

# Load ``src/.env`` into ``os.environ`` *before* we read ``ML_MODEL_ID`` below.
# The client builder also calls load_dotenv internally, but that runs later.
load_src_dotenv(__file__)

# Configure your OpenSearch connection.
client = open_search_client_from_env_file(src_env_file(__file__))

# ``raise_on_error=True`` makes a connection failure abort the script — we
# don't want to silently "succeed" before the actual API call below.
print_opensearch_connection_test(client, raise_on_error=True)

# Create ingest pipeline via API: PUT _ingest/pipeline/<pipeline_id>
pipeline_id = "vector-search-embeddings-pipeline"
response = client.ingest.put_pipeline(
    id=pipeline_id,
    body={
        "description": "Pipeline for processing OpenSearch index data",
        # Processors run in order. Here there's only one — the
        # ``text_embedding`` processor reads ``passage_text`` from the incoming
        # doc, calls the deployed model, and writes the result back into
        # ``passage_embedding`` (the field name your index mapping expects).
        "processors": [
            {
                "text_embedding": {
                    # The model id you saved from Lesson 1's deploy step.
                    # Stored in ``src/.env`` so this lesson can find it.
                    "model_id": os.getenv("ML_MODEL_ID"),
                    # ``field_map`` is ``{source_field: dest_field}``.
                    # You can map multiple fields in one processor.
                    "field_map": {
                        "passage_text": "passage_embedding"
                    }
                }
            }
        ],
    },
)

# ``acknowledged: true`` means the master node accepted the change. It does NOT
# mean every data node has it yet — for ingest pipelines that's usually fine
# because the cluster state propagates within milliseconds.
if response.get("acknowledged"):
    print(f"Created ingest pipeline: {pipeline_id}")
else:
    print("Pipeline response:", response)
