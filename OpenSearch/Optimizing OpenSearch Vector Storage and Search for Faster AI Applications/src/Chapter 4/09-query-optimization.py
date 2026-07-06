"""Chapter 4 · Steps 20-25 — profile, explain, rank_eval, and search pipelines.

Runs against the chunked bookstore-rag index built by 07-chunking-index.py.
"""

import json
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

client = open_search_client_from_env_file(_SRC / ".env")
print_opensearch_connection_test(client, raise_on_error=True)

INDEX = "bookstore-rag"
vector = json.loads((Path(__file__).resolve().parent / "bookstore-rag-query-vector.json").read_text())

hybrid = {"hybrid": {"queries": [
    {"match": {"content": {"query": "mystery novel unreliable narrator"}}},
    {"knn": {"content_embedding": {"vector": vector, "k": 10}}},
]}}

# Step 20: profile.
resp = client.search(index=INDEX, params={"search_pipeline": "bookstore-hybrid-pipeline"}, body={
    "profile": True, "size": 10, "_source": {"excludes": ["content_embedding", "content_chunks"]}, "query": hybrid,
})
print("Has profile object:", "profile" in resp)

# Step 21: explain.
resp = client.search(index=INDEX, params={"search_pipeline": "bookstore-hybrid-pipeline", "explain": "true"}, body={
    "size": 3, "_source": {"excludes": ["content_embedding", "content_chunks"]}, "query": hybrid,
})
print("First hit has _explanation:", "_explanation" in resp["hits"]["hits"][0])

# Step 22: rank_eval (MRR@10) against real book IDs.
rank = client.transport.perform_request("POST", f"/{INDEX}/_rank_eval", body={
    "requests": [
        {"id": "whale_query", "request": {"query": {"match": {"content": "whale sea captain revenge"}}},
         "ratings": [{"_index": INDEX, "_id": "2701", "rating": 3}]},
        {"id": "detective_query", "request": {"query": {"match": {"content": "detective mystery investigation"}}},
         "ratings": [{"_index": INDEX, "_id": "1661", "rating": 3}]},
        {"id": "gothic_query", "request": {"query": {"match": {"content": "gothic horror monster"}}},
         "ratings": [{"_index": INDEX, "_id": "345", "rating": 3}, {"_index": INDEX, "_id": "84", "rating": 2}]},
    ],
    "metric": {"mean_reciprocal_rank": {"k": 10, "relevant_rating_threshold": 1}},
})
print("Rank eval metric_score:", rank.get("metric_score"))

# Step 23: request-processor pipeline (filter out-of-stock).
client.transport.perform_request("PUT", "/_search/pipeline/bookstore-stock-filter", body={
    "description": "Filter out-of-stock books from every search",
    "request_processors": [{"filter_query": {"query": {"term": {"in_stock": True}}, "tag": "stock_filter"}}],
})
print("Created bookstore-stock-filter")

# Step 24: set default search pipeline.
client.indices.put_settings(index=INDEX, body={"index.search.default_pipeline": "bookstore-stock-filter"})
print("Set default search pipeline")

# Step 25: full pipeline (filter + normalization).
client.transport.perform_request("PUT", "/_search/pipeline/bookstore-full-pipeline", body={
    "description": "Full bookstore search pipeline: stock filter + hybrid normalization",
    "request_processors": [{"filter_query": {"query": {"term": {"in_stock": True}}, "tag": "stock_filter"}}],
    "phase_results_processors": [{"normalization-processor": {
        "normalization": {"technique": "min_max"},
        "combination": {"technique": "arithmetic_mean", "parameters": {"weights": [0.3, 0.7]}},
    }}],
})
resp = client.search(index=INDEX, params={"search_pipeline": "bookstore-full-pipeline"}, body={
    "size": 10, "_source": {"excludes": ["content_embedding", "content_chunks"]},
    "query": {"hybrid": {"queries": [
        {"match": {"content": {"query": "whale"}}},
        {"knn": {"content_embedding": {"vector": vector, "k": 10}}},
    ]}},
})
print("Full-pipeline hits:", len(resp["hits"]["hits"]))
