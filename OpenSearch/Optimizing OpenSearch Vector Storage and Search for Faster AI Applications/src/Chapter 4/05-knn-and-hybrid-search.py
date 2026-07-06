"""Chapter 4 · Steps 8-12 — k-NN, filtered k-NN, hybrid search, and function_score rerank.

Uses the checked-in 768-dim query vector (bookstore-rag-query-vector.json) so retrieval
quality is isolated from query-time embedding.
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

INDEX = "bookstore-rag-index"
vector = json.loads((Path(__file__).resolve().parent / "bookstore-rag-query-vector.json").read_text())


def titles(resp):
    return [h["_source"].get("title") for h in resp["hits"]["hits"]]


# Step 8: plain k-NN, lean _source.
resp = client.search(index=INDEX, body={
    "size": 10, "_source": ["title", "author", "genre", "price", "rating"],
    "query": {"knn": {"content_embedding": {"vector": vector, "k": 10}}},
})
print("k-NN:", titles(resp))

# Step 9: filtered k-NN — mystery, <= $20, rating >= 4.
resp = client.search(index=INDEX, body={
    "size": 10, "_source": ["title", "author", "genre", "price", "rating"],
    "query": {"knn": {"content_embedding": {"vector": vector, "k": 10, "filter": {"bool": {
        "must": [{"term": {"genre": "mystery"}}],
        "filter": [{"range": {"price": {"lte": 20}}}, {"range": {"rating": {"gte": 4.0}}}],
    }}}}},
})
print("Filtered k-NN:", titles(resp))

# Step 10: hybrid pipeline (min-max normalization, weights [0.3 keyword, 0.7 vector]).
client.transport.perform_request("PUT", "/_search/pipeline/bookstore-hybrid-pipeline", body={
    "description": "Hybrid search pipeline for bookstore RAG",
    "phase_results_processors": [{"normalization-processor": {
        "normalization": {"technique": "min_max"},
        "combination": {"technique": "arithmetic_mean", "parameters": {"weights": [0.3, 0.7]}},
    }}],
})
print("Created bookstore-hybrid-pipeline")

# Step 11: hybrid search.
resp = client.search(index=INDEX, params={"search_pipeline": "bookstore-hybrid-pipeline"}, body={
    "size": 10, "_source": {"excludes": ["content_embedding"]},
    "query": {"hybrid": {"queries": [
        {"match": {"content": {"query": "mystery novel with an unreliable narrator"}}},
        {"knn": {"content_embedding": {"vector": vector, "k": 10}}},
    ]}},
})
print("Hybrid:", titles(resp))

# Step 12: rerank with business signals (recency + rating + in_stock).
resp = client.search(index=INDEX, body={
    "size": 10, "_source": ["title", "rating", "publication_year", "in_stock"],
    "query": {"function_score": {
        "query": {"knn": {"content_embedding": {"vector": vector, "k": 10}}},
        "functions": [
            {"field_value_factor": {"field": "rating", "factor": 0.1, "missing": 3.0}},
            {"filter": {"range": {"publication_year": {"gte": 2020}}}, "weight": 1.2},
            {"filter": {"term": {"in_stock": True}}, "weight": 1.15},
        ],
        "score_mode": "sum", "boost_mode": "sum",
    }},
})
print("Reranked:", titles(resp))
