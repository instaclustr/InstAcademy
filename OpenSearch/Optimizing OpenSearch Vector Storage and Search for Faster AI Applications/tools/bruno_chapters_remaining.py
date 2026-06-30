"""Chapter generator functions for generate-bruno-requests.py (exec'd with injected globals)."""

from __future__ import annotations

CHUNKING_SCRIPT = (
    "if (ctx.content_chunks == null) { ctx.content_chunks = []; } else { "
    "def normalized_chunks = []; "
    "for (int i = 0; i < ctx.content_chunks.size(); i++) { "
    "def chunk = ctx.content_chunks.get(i); "
    "if (chunk != null) { normalized_chunks.add(['text': chunk, 'chunk_index': i]); } } "
    "ctx.content_chunks = normalized_chunks; }"
)


def ch1_lesson4() -> None:
    p = "Chapter 1/Lesson 4"
    write(f"{p}/01-delete-dest-index.bru", bru_http("Delete my-optimized-vector-index", 1, "DELETE", "/my-optimized-vector-index"))
    write(f"{p}/02-delete-source-index.bru", bru_http("Delete my-vector-index", 2, "DELETE", "/my-vector-index"))
    write(
        f"{p}/03-create-source-index.bru",
        bru_http(
            "Create my-vector-index (256-dim knn)",
            3,
            "PUT",
            "/my-vector-index",
            body="""{
  "settings": { "index.knn": true },
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "my_vector": {
        "type": "knn_vector",
        "dimension": 256,
        "method": {
          "engine": "lucene",
          "space_type": "l2",
          "name": "hnsw",
          "parameters": {}
        }
      }
    }
  }
}""",
        ),
    )
    write(
        f"{p}/04-create-dest-index.bru",
        bru_http(
            "Create my-optimized-vector-index (128-dim knn)",
            4,
            "PUT",
            "/my-optimized-vector-index",
            body="""{
  "settings": { "index.knn": true },
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "my_vector": {
        "type": "knn_vector",
        "dimension": 128,
        "method": {
          "engine": "lucene",
          "space_type": "l2",
          "name": "hnsw",
          "parameters": {}
        }
      }
    }
  }
}""",
        ),
    )
    write(
        f"{p}/05-bulk-source-index.bru",
        bru_http(
            "Bulk index sample vectors",
            5,
            "POST",
            "/_bulk",
            body=bulk_ndjson("chapter-1-lesson-4-vector-index.ndjson"),
            body_type="file",
        ),
    )
    write(f"{p}/06-refresh-source-index.bru", bru_http("Refresh my-vector-index", 6, "POST", "/my-vector-index/_refresh"))
    write(
        f"{p}/07-reindex-truncate-vectors.bru",
        bru_http(
            "Reindex with vector truncation",
            7,
            "POST",
            "/_reindex?wait_for_completion=true",
            body="""{
  "source": { "index": "my-vector-index" },
  "dest": { "index": "my-optimized-vector-index" },
  "script": {
    "source": "ctx._source.my_vector = ctx._source.my_vector.subList(0, 128);",
    "lang": "painless"
  }
}""",
        ),
    )


def ch2_lesson4() -> None:
    p = "Chapter 2/Lesson 4"
    write(f"{p}/01-delete-vector-search-index.bru", bru_http("Delete vector-search-index", 1, "DELETE", "/vector-search-index"))
    write(
        f"{p}/02-delete-ingest-pipeline.bru",
        bru_http("Delete vector-search-embeddings-pipeline", 2, "DELETE", "/_ingest/pipeline/vector-search-embeddings-pipeline"),
    )
    write(
        f"{p}/03-undeploy-model.bru",
        bru_http(
            "Undeploy ML model",
            3,
            "POST",
            "/_plugins/_ml/models/{{modelId}}/_undeploy",
            note="Set taskId and poll if response includes task_id.",
        ),
    )
    write(f"{p}/04-poll-undeploy-task.bru", ml_poll(4))
    write(f"{p}/05-delete-model.bru", bru_http("Delete ML model", 5, "DELETE", "/_plugins/_ml/models/{{modelId}}"))


def ch2_lesson5() -> None:
    p = "Chapter 2/Lesson 5"
    write(
        f"{p}/01-cluster-routing-settings.bru",
        bru_http(
            "Cluster routing allocation and rebalance",
            1,
            "PUT",
            "/_cluster/settings",
            body="""{
  "persistent": {
    "cluster.routing.allocation.enable": "all",
    "cluster.routing.rebalance.enable": "all"
  }
}""",
        ),
    )


def ch3_lesson1() -> None:
    p = "Chapter 3/Lesson 1"
    write(
        f"{p}/01-enable-url-model-registration.bru",
        bru_http(
            "Enable URL model registration",
            1,
            "PUT",
            "/_cluster/settings",
            body='{"persistent": {"plugins.ml_commons.allow_registering_model_via_url": true}}',
        ),
    )
    write(
        f"{p}/02-register-model-group.bru",
        bru_http(
            "Register model group",
            2,
            "POST",
            "/_plugins/_ml/model_groups/_register",
            body="""{
  "name": "huggingface-models",
  "description": "A group for Hugging Face transformer models"
}""",
            note="Save model_group_id into modelGroupId.",
        ),
    )
    write(
        f"{p}/03-register-sparse-model.bru",
        bru_http(
            "Register neural sparse encoding model",
            3,
            "POST",
            "/_plugins/_ml/models/_register",
            body="""{
  "name": "amazon/neural-sparse/opensearch-neural-sparse-encoding-v1",
  "version": "1.0.1",
  "model_group_id": "{{modelGroupId}}",
  "model_format": "TORCH_SCRIPT"
}""",
            note="On COMPLETED, save model_id to sparseModelId.",
        ),
    )
    write(f"{p}/04-poll-register-task.bru", ml_poll(4))
    write(
        f"{p}/05-deploy-sparse-model.bru",
        bru_http("Deploy sparse model", 5, "POST", "/_plugins/_ml/models/{{sparseModelId}}/_deploy"),
    )
    write(f"{p}/06-poll-deploy-task.bru", ml_poll(6))
    write(
        f"{p}/07-create-search-pipeline.bru",
        bru_http(
            "Create nlp-search-normalization-pipeline",
            7,
            "PUT",
            "/_search/pipeline/nlp-search-normalization-pipeline",
            body="""{
  "description": "Post processor for hybrid search",
  "phase_results_processors": [{
    "normalization-processor": {
      "normalization": { "technique": "min_max" },
      "combination": {
        "technique": "arithmetic_mean",
        "parameters": { "weights": [0.3, 0.7] }
      }
    }
  }]
}""",
        ),
    )
    write(f"{p}/08-delete-sparse-index.bru", bru_http("Delete my-sparse-neural-index", 8, "DELETE", "/my-sparse-neural-index"))
    write(
        f"{p}/09-create-sparse-index.bru",
        bru_http(
            "Create my-sparse-neural-index",
            9,
            "PUT",
            "/my-sparse-neural-index",
            body="""{
  "settings": { "index": { "number_of_shards": 2, "number_of_replicas": 1 } },
  "mappings": {
    "properties": {
      "passage_text": { "type": "text" },
      "passage_chunk": { "type": "text" },
      "passage_embedding": {
        "type": "nested",
        "properties": { "sparse_encoding": { "type": "rank_features" } }
      }
    }
  }
}""",
        ),
    )
    write(
        f"{p}/10-create-ingest-pipeline.bru",
        bru_http(
            "Create nlp-ingest-pipeline",
            10,
            "PUT",
            "/_ingest/pipeline/nlp-ingest-pipeline",
            body="""{
  "description": "A sparse encoding ingest pipeline",
  "processors": [
    {
      "text_chunking": {
        "algorithm": {
          "fixed_token_length": {
            "token_limit": 5,
            "overlap_rate": 0.5,
            "tokenizer": "standard"
          }
        },
        "field_map": { "passage_text": "passage_chunk" }
      }
    },
    {
      "sparse_encoding": {
        "model_id": "{{sparseModelId}}",
        "prune_type": "max_ratio",
        "prune_ratio": 0.1,
        "field_map": { "passage_chunk": "passage_embedding" }
      }
    }
  ]
}""",
        ),
    )
    write(
        f"{p}/11-attach-default-pipeline.bru",
        bru_http(
            "Attach default ingest pipeline",
            11,
            "PUT",
            "/my-sparse-neural-index/_settings",
            body='{"index": {"default_pipeline": "nlp-ingest-pipeline"}}',
        ),
    )
    write(
        f"{p}/12-bulk-sparse-index.bru",
        bru_http(
            "Bulk ingest sparse index data",
            12,
            "POST",
            "/_bulk?timeout=600s",
            body=bulk_ndjson("chapter-3-lesson-1-sparse-index.ndjson"),
            body_type="file",
            note="Chunking + sparse encoding per document — may take several minutes.",
        ),
    )
    write(
        f"{p}/13-hybrid-sparse-search.bru",
        bru_http(
            "Hybrid BM25 + neural_sparse search",
            13,
            "POST",
            "/my-sparse-neural-index/_search?search_pipeline=nlp-search-normalization-pipeline",
            body="""{
  "_source": { "excludes": ["passage_embedding"] },
  "query": {
    "hybrid": {
      "queries": [
        { "match": { "passage_text": { "query": "a hero" } } },
        {
          "nested": {
            "path": "passage_embedding",
            "score_mode": "max",
            "query": {
              "neural_sparse": {
                "passage_embedding.sparse_encoding": {
                  "query_text": "a hero",
                  "model_id": "{{sparseModelId}}"
                }
              }
            }
          }
        }
      ]
    }
  }
}""",
        ),
    )


def ch4_lesson1() -> None:
    p = "Chapter 4/Lesson 1"
    qv = query_vector_json()
    write(
        f"{p}/01-enable-url-model-registration.bru",
        bru_http(
            "Enable URL model registration",
            1,
            "PUT",
            "/_cluster/settings",
            body='{"persistent": {"plugins.ml_commons.allow_registering_model_via_url": true}}',
        ),
    )
    write(
        f"{p}/02-register-model-group.bru",
        bru_http(
            "Register model group",
            2,
            "POST",
            "/_plugins/_ml/model_groups/_register",
            body="""{
  "name": "huggingface-models",
  "description": "A group for Hugging Face transformer models"
}""",
            note="Save model_group_id into modelGroupId.",
        ),
    )
    write(
        f"{p}/03-register-mpnet-model.bru",
        bru_http(
            "Register all-mpnet-base-v2 model",
            3,
            "POST",
            "/_plugins/_ml/models/_register",
            body="""{
  "name": "huggingface/sentence-transformers/all-mpnet-base-v2",
  "version": "1.0.1",
  "model_group_id": "{{modelGroupId}}",
  "model_format": "TORCH_SCRIPT"
}""",
            note="On COMPLETED, save model_id to modelId.",
        ),
    )
    write(f"{p}/04-poll-register-task.bru", ml_poll(4))
    write(f"{p}/05-deploy-model.bru", bru_http("Deploy model", 5, "POST", "/_plugins/_ml/models/{{modelId}}/_deploy"))
    write(f"{p}/06-poll-deploy-task.bru", ml_poll(6))
    write(
        f"{p}/07-create-hybrid-search-pipeline.bru",
        bru_http(
            "Create bookstore-hybrid-pipeline",
            7,
            "PUT",
            "/_search/pipeline/bookstore-hybrid-pipeline",
            body="""{
  "description": "Hybrid search pipeline for bookstore RAG",
  "phase_results_processors": [{
    "normalization-processor": {
      "normalization": { "technique": "min_max" },
      "combination": {
        "technique": "arithmetic_mean",
        "parameters": { "weights": [0.3, 0.7] }
      }
    }
  }]
}""",
        ),
    )
    write(
        f"{p}/08-create-ingest-pipeline.bru",
        bru_http(
            "Create bookstore-rag-ingest-pipeline",
            8,
            "PUT",
            "/_ingest/pipeline/bookstore-rag-ingest-pipeline",
            body="""{
  "description": "Pipeline for processing OpenSearch index data",
  "processors": [{
    "text_embedding": {
      "model_id": "{{modelId}}",
      "field_map": { "passage_text": "passage_embedding" }
    }
  }]
}""",
        ),
    )
    write(
        f"{p}/09-create-bookstore-rag-index.bru",
        bru_http(
            "Create bookstore-rag-index",
            9,
            "PUT",
            "/bookstore-rag-index",
            body="""{
  "settings": {
    "index.knn": true,
    "index": { "number_of_shards": 2, "number_of_replicas": 1 },
    "default_pipeline": "bookstore-rag-ingest-pipeline"
  },
  "mappings": {
    "properties": {
      "book_id": { "type": "keyword" },
      "title": { "type": "text" },
      "author": { "type": "text" },
      "isbn": { "type": "keyword" },
      "genre": { "type": "keyword" },
      "published_year": { "type": "integer" },
      "chunk_index": { "type": "integer" },
      "passage_text": { "type": "text" },
      "passage_embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "engine": "lucene",
          "space_type": "l2",
          "name": "hnsw",
          "parameters": {}
        }
      }
    }
  }
}""",
        ),
    )
    write(
        f"{p}/10-bulk-bookstore-rag-index.bru",
        bru_http(
            "Bulk ingest bookstore-rag-index",
            10,
            "POST",
            "/_bulk?timeout=600s",
            body=bulk_ndjson("chapter-4-bookstore-rag-index.ndjson"),
            body_type="file",
        ),
    )
    write(
        f"{p}/11-knn-search.bru",
        bru_http(
            "k-NN search with stored query vector",
            11,
            "POST",
            "/bookstore-rag-index/_search",
            body=f"""{{
  "query": {{
    "knn": {{
      "passage_embedding": {{
        "vector": {qv},
        "k": 10
      }}
    }}
  }},
  "profile": "true",
  "size": 10,
  "_source": ["title", "author", "price", "rating", "genre"]
}}""",
        ),
    )
    write(
        f"{p}/12-hybrid-search.bru",
        bru_http(
            "Hybrid keyword + k-NN search",
            12,
            "POST",
            "/bookstore-rag-index/_search?search_pipeline=bookstore-hybrid-pipeline",
            body=f"""{{
  "_source": {{ "excludes": ["passage_embedding"] }},
  "size": 10,
  "query": {{
    "hybrid": {{
      "queries": [
        {{ "match": {{ "passage_text": {{ "query": "mystery novel under $20" }} }} }},
        {{
          "knn": {{
            "passage_embedding": {{
              "vector": {qv},
              "k": 10
            }}
          }}
        }}
      ]
    }}
  }}
}}""",
        ),
    )
    write(f"{p}/13-knn-warmup.bru", bru_http("k-NN warmup bookstore-rag-index", 13, "GET", "/_plugins/_knn/warmup/bookstore-rag-index"))
    write(f"{p}/14-knn-stats.bru", bru_http("k-NN stats", 14, "GET", "/_plugins/_knn/stats"))
    write(
        f"{p}/15-knn-circuit-breaker.bru",
        bru_http(
            "Set k-NN memory circuit breaker",
            15,
            "PUT",
            "/_cluster/settings",
            body='{"persistent": {"knn.memory.circuit_breaker.limit": "60%"}}',
        ),
    )


def ch4_lesson2() -> None:
    p = "Chapter 4/Lesson 2"
    write(
        f"{p}/01-create-books-unoptimized.bru",
        bru_http(
            "Create books-unoptimized index",
            1,
            "PUT",
            "/books-unoptimized",
            body="""{
  "settings": { "index": { "number_of_shards": 2, "number_of_replicas": 1 } },
  "mappings": {
    "properties": {
      "book_id": { "type": "text" },
      "title": { "type": "text" },
      "author": { "type": "text" },
      "isbn": { "type": "text" },
      "genre": { "type": "text" },
      "published_year": { "type": "integer" },
      "price": { "type": "float" },
      "rating": { "type": "integer" },
      "content": { "type": "text" }
    }
  }
}""",
        ),
    )
    write(
        f"{p}/02-create-chunking-pipeline.bru",
        bru_http(
            "Create bookstore-chunking-pipeline",
            2,
            "PUT",
            "/_ingest/pipeline/bookstore-chunking-pipeline",
            body=f"""{{
  "description": "Chunk book content for RAG embedding",
  "processors": [
    {{
      "text_chunking": {{
        "algorithm": {{
          "fixed_token_length": {{
            "token_limit": 384,
            "overlap_rate": 0.2,
            "tokenizer": "standard"
          }}
        }},
        "field_map": {{ "content": "content_chunks" }}
      }}
    }},
    {{
      "script": {{
        "lang": "painless",
        "source": "{CHUNKING_SCRIPT}"
      }}
    }},
    {{
      "text_embedding": {{
        "model_id": "{{{{modelId}}}}",
        "field_map": {{ "content": "content_embedding" }}
      }}
    }}
  ]
}}""",
        ),
    )
    write(
        f"{p}/03-create-bookstore-rag-index.bru",
        bru_http(
            "Create bookstore-rag index",
            3,
            "PUT",
            "/bookstore-rag",
            body="""{
  "settings": {
    "index": {
      "knn": true,
      "default_pipeline": "bookstore-chunking-pipeline",
      "refresh_interval": "30s"
    }
  },
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "author": { "type": "text" },
      "content": { "type": "text" },
      "content_chunks": {
        "type": "nested",
        "properties": {
          "text": { "type": "text" },
          "chunk_index": { "type": "integer" }
        }
      },
      "content_embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "engine": "faiss",
          "name": "hnsw",
          "parameters": { "m": 16, "ef_construction": 128 }
        }
      },
      "genre": { "type": "keyword" },
      "price": { "type": "float" },
      "rating": { "type": "float" },
      "publication_year": { "type": "integer" },
      "in_stock": { "type": "boolean" }
    }
  }
}""",
        ),
    )
    write(
        f"{p}/04-disable-refresh.bru",
        bru_http(
            "Disable refresh for bulk load",
            4,
            "PUT",
            "/bookstore-rag/_settings",
            body='{"index": {"refresh_interval": "-1"}}',
        ),
    )
    write(
        f"{p}/05-bulk-bookstore-rag.bru",
        bru_http(
            "Bulk ingest bookstore-rag",
            5,
            "POST",
            "/_bulk?timeout=600s",
            body=bulk_ndjson("chapter-4-bookstore-rag.ndjson"),
            body_type="file",
            note="Chunking + embedding per document — may take several minutes.",
        ),
    )
    write(
        f"{p}/06-force-merge.bru",
        bru_http("Force merge bookstore-rag", 6, "POST", "/bookstore-rag/_forcemerge?max_num_segments=5"),
    )
    write(
        f"{p}/07-restore-refresh.bru",
        bru_http(
            "Restore refresh interval",
            7,
            "PUT",
            "/bookstore-rag/_settings",
            body='{"index": {"refresh_interval": "1s"}}',
        ),
    )
    write(f"{p}/08-refresh-index.bru", bru_http("Refresh bookstore-rag", 8, "POST", "/bookstore-rag/_refresh"))
    write(
        f"{p}/09-cat-shards.bru",
        bru_http(
            "Cat shards for bookstore-rag",
            9,
            "GET",
            "/_cat/shards/bookstore-rag?v=true&h=index,shard,prirep,state,docs,store&format=json",
        ),
    )
    write(f"{p}/10-knn-warmup.bru", bru_http("k-NN warmup bookstore-rag", 10, "GET", "/_plugins/_knn/warmup/bookstore-rag"))
    write(f"{p}/11-knn-stats.bru", bru_http("k-NN stats", 11, "GET", "/_plugins/_knn/stats"))
    write(f"{p}/12-close-index.bru", bru_http("Close bookstore-rag for preload", 12, "POST", "/bookstore-rag/_close"))
    write(
        f"{p}/13-set-preload.bru",
        bru_http(
            "Set index.store.preload",
            13,
            "PUT",
            "/bookstore-rag/_settings",
            body='{"index": {"store": {"preload": ["vec", "vem"]}}}',
        ),
    )
    write(f"{p}/14-open-index.bru", bru_http("Reopen bookstore-rag", 14, "POST", "/bookstore-rag/_open"))
    write(
        f"{p}/15-cluster-health.bru",
        bru_http(
            "Wait for yellow health on bookstore-rag",
            15,
            "GET",
            "/_cluster/health/bookstore-rag?wait_for_status=yellow&timeout=60s",
        ),
    )


def ch4_lesson3() -> None:
    p = "Chapter 4/Lesson 3"
    qv = query_vector_json()
    write(
        f"{p}/01-explain-hybrid-search.bru",
        bru_http(
            "Explain hybrid search on bookstore-rag",
            1,
            "POST",
            "/bookstore-rag/_search?search_pipeline=bookstore-hybrid-pipeline&explain=true",
            body=f"""{{
  "query": {{
    "hybrid": {{
      "queries": [
        {{ "match": {{ "content": {{ "query": "whale" }} }} }},
        {{ "knn": {{ "content_embedding": {{ "vector": {qv}, "k": 10 }} }} }}
      ]
    }}
  }}
}}""",
        ),
    )
    write(
        f"{p}/02-rank-eval.bru",
        bru_http(
            "Rank eval hybrid search",
            2,
            "POST",
            "/bookstore-rag/_rank_eval",
            body=f"""{{
  "requests": [{{
    "id": "mystery_query",
    "request": {{
      "query": {{
        "hybrid": {{
          "queries": [
            {{ "match": {{ "content": {{ "query": "whale" }} }} }},
            {{ "knn": {{ "content_embedding": {{ "vector": {qv}, "k": 10 }} }} }}
          ]
        }}
      }}
    }},
    "ratings": [
      {{ "_index": "bookstore-rag", "_id": "2701", "rating": 0 }}
    ]
  }}],
  "metric": {{
    "mean_reciprocal_rank": {{
      "k": 10,
      "relevant_rating_threshold": 1
    }}
  }}
}}""",
        ),
    )
    write(
        f"{p}/03-create-score-filter-pipeline.bru",
        bru_http(
            "Create bookstore-score-filter pipeline",
            3,
            "PUT",
            "/_search/pipeline/bookstore-score-filter",
            body="""{
  "description": "Change scores on books based on ratings and publish date from search results",
  "request_processors": [{
    "filter_query": {
      "query": {
        "script_score": {
          "query": "in_stock: true",
          "script": {
            "source": "(doc['publish_date'].value - 2020)* 0.5 + doc['ratings'].value * 0.1"
          }
        }
      }
    }
  }]
}""",
        ),
    )
    write(
        f"{p}/04-set-default-search-pipeline.bru",
        bru_http(
            "Set default search pipeline on bookstore-rag",
            4,
            "PUT",
            "/bookstore-rag/_settings",
            body='{"index.search.default_pipeline": "bookstore-stock-filter"}',
            note="Requires bookstore-stock-filter pipeline to exist.",
        ),
    )
    write(
        f"{p}/05-create-full-pipeline.bru",
        bru_http(
            "Create bookstore-full-pipeline",
            5,
            "PUT",
            "/_search/pipeline/bookstore-full-pipeline",
            body="""{
  "description": "Full bookstore search pipeline",
  "request_processors": [{
    "filter_query": {
      "query": { "term": { "in_stock": true } },
      "tag": "stock_filter"
    }
  }],
  "phase_results_processors": [{
    "normalization-processor": {
      "normalization": { "technique": "min_max" },
      "combination": {
        "technique": "arithmetic_mean",
        "parameters": { "weights": [0.3, 0.7] }
      }
    }
  }]
}""",
        ),
    )


def ch5_lesson1() -> None:
    p = "Chapter 5/Lesson 1"
    write(
        f"{p}/01-routing-awareness.bru",
        bru_http(
            "Cluster routing awareness settings",
            1,
            "PUT",
            "/_cluster/settings",
            body="""{
  "persistent": {
    "cluster.routing.allocation.awareness.attributes": "zone",
    "cluster.routing.allocation.awareness.force.zone.values": "zone1,zone2,zone3"
  }
}""",
        ),
    )
    write(
        f"{p}/02-cat-shards-by-node.bru",
        bru_http("Cat shards sorted by node", 2, "GET", "/_cat/shards?v=true&s=node&format=json"),
    )
    write(
        f"{p}/03-force-merge.bru",
        bru_http(
            "Force merge bookstore-rag-all-together",
            3,
            "POST",
            "/bookstore-rag-all-together/_forcemerge?max_num_segments=5",
        ),
    )
    write(
        f"{p}/04-create-my-index.bru",
        bru_http(
            "Create my-index (too many shards demo)",
            4,
            "PUT",
            "/my-index",
            body='{"settings": {"number_of_shards": 6, "number_of_replicas": 1}}',
        ),
    )
    write(f"{p}/05-cluster-health-before.bru", bru_http("Cluster health before replica fix", 5, "GET", "/_cluster/health"))
    write(
        f"{p}/06-set-replicas-zero.bru",
        bru_http(
            "Set my-index replicas to 0",
            6,
            "PUT",
            "/my-index/_settings",
            body='{"number_of_replicas": 0}',
        ),
    )
    write(f"{p}/07-cluster-health-after.bru", bru_http("Cluster health after replica fix", 7, "GET", "/_cluster/health"))
    write(
        f"{p}/08-cat-shards.bru",
        bru_http(
            "Cat shards with unassigned reason",
            8,
            "GET",
            "/_cat/shards?v=true&h=index,shard,prirep,state,node,unassigned.reason&format=json",
        ),
    )
    write(
        f"{p}/09-cat-allocation.bru",
        bru_http(
            "Cat allocation overview",
            9,
            "GET",
            "/_cat/allocation?v=true&h=node,disk.used_percent,disk.avail&format=json",
        ),
    )
    write(
        f"{p}/10-allocation-explain.bru",
        bru_http(
            "Explain shard allocation",
            10,
            "POST",
            "/_cluster/allocation/explain",
            body='{"index": "my-index", "shard": 1, "primary": true}',
        ),
    )
    write(
        f"{p}/11-disk-watermarks.bru",
        bru_http(
            "Set disk watermark settings",
            11,
            "PUT",
            "/_cluster/settings",
            body="""{
  "persistent": {
    "cluster.routing.allocation.disk.watermark.low": "85%",
    "cluster.routing.allocation.disk.watermark.high": "90%",
    "cluster.routing.allocation.disk.watermark.flood_stage": "95%"
  }
}""",
        ),
    )
    write(
        f"{p}/12-get-watermarks.bru",
        bru_http(
            "Get cluster settings (watermarks)",
            12,
            "GET",
            "/_cluster/settings?include_defaults=true&flat_settings=true",
        ),
    )


def ch5_lesson2() -> None:
    p = "Chapter 5/Lesson 2"
    write(
        f"{p}/01-create-my-index-bookstore.bru",
        bru_http(
            "Create my-index bookstore mappings",
            1,
            "PUT",
            "/my-index",
            body="""{
  "settings": { "index": { "number_of_shards": 1, "number_of_replicas": 0 } },
  "mappings": {
    "properties": {
      "book_id": { "type": "keyword" },
      "title": {
        "type": "text",
        "fields": { "keyword": { "type": "keyword", "ignore_above": 256 } }
      },
      "author": { "type": "keyword" },
      "isbn": { "type": "keyword" },
      "genre": { "type": "keyword" },
      "publisher": { "type": "keyword" },
      "description": { "type": "text" },
      "price": { "type": "float" },
      "in_stock": { "type": "boolean" },
      "published_year": { "type": "integer" }
    }
  }
}""",
        ),
    )
    write(f"{p}/02-get-mapping.bru", bru_http("Get my-index mapping", 2, "GET", "/my-index/_mapping"))
    write(
        f"{p}/03-shrink-block-writes.bru",
        bru_http(
            "Shrink step 1: pin shards and block writes",
            3,
            "PUT",
            "/bookstore-rag-all-together/_settings",
            body="""{
  "settings": {
    "index.routing.allocation.require._name": "node-1",
    "index.blocks.write": true
  }
}""",
        ),
    )
    write(
        f"{p}/04-shrink-index.bru",
        bru_http(
            "Shrink step 2: shrink index",
            4,
            "POST",
            "/bookstore-rag-all-together/_shrink/bookstore-rag-all-together-shrunk",
            body="""{
  "settings": {
    "index.number_of_shards": 1,
    "index.number_of_replicas": 1,
    "index.codec": "best_compression"
  }
}""",
        ),
    )
    write(
        f"{p}/05-shrink-clear-routing.bru",
        bru_http(
            "Shrink step 3: clear routing requirement",
            5,
            "PUT",
            "/bookstore-rag-all-together-shrunk/_settings",
            body='{"index.routing.allocation.require._name": null}',
        ),
    )
    write(
        f"{p}/06-shrink-force-merge.bru",
        bru_http(
            "Shrink step 4: force merge shrunk index",
            6,
            "POST",
            "/bookstore-rag-all-together-shrunk/_forcemerge?max_num_segments=1",
        ),
    )
    write(
        f"{p}/07-shrink-alias-swap.bru",
        bru_http(
            "Shrink step 5: alias swap",
            7,
            "POST",
            "/_aliases",
            body="""{
  "actions": [
    { "remove": { "index": "bookstore-rag-all-together", "alias": "bookstore-rag-all-together-alias" } },
    { "add": { "index": "bookstore-rag-all-together-shrunk", "alias": "bookstore-rag-all-together-alias" } }
  ]
}""",
        ),
    )
    write(
        f"{p}/08-shrink-delete-old.bru",
        bru_http("Shrink step 6: delete old index", 8, "DELETE", "/bookstore-rag-all-together"),
    )
    write(
        f"{p}/09-reindex-books.bru",
        bru_http(
            "Reindex my-index to my-index-new with script",
            9,
            "POST",
            "/_reindex?slices=5&wait_for_completion=true",
            body="""{
  "source": { "index": "my-index" },
  "dest": { "index": "my-index-new" },
  "script": {
    "source": "ctx._source.title = ctx._source.title + ' ' + ctx._source.author; ctx._source.remove('author');",
    "lang": "painless"
  }
}""",
        ),
    )
    write(
        f"{p}/10-create-book-embeddings-v2.bru",
        bru_http(
            "Create book-embeddings-v2 index",
            10,
            "PUT",
            "/book-embeddings-v2",
            body="""{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "book_id": { "type": "keyword" },
      "title": { "type": "text" },
      "embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "name": "hnsw",
          "space_type": "l2",
          "engine": "faiss",
          "parameters": { "ef_construction": 128, "m": 16 }
        }
      },
      "model_version": { "type": "keyword" },
      "created_at": { "type": "date" }
    }
  }
}""",
        ),
    )
    write(
        f"{p}/11-create-book-embeddings-v3.bru",
        bru_http(
            "Create book-embeddings-v3 index",
            11,
            "PUT",
            "/book-embeddings-v3",
            body="""{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "book_id": { "type": "keyword" },
      "title": { "type": "text" },
      "embedding": {
        "type": "knn_vector",
        "dimension": 1024,
        "method": {
          "name": "hnsw",
          "space_type": "l2",
          "engine": "faiss",
          "parameters": { "ef_construction": 256, "m": 32 }
        }
      },
      "model_version": { "type": "keyword" },
      "model_name": { "type": "keyword" },
      "created_at": { "type": "date" }
    }
  }
}""",
        ),
    )


def ch5_lesson3() -> None:
    p = "Chapter 5/Lesson 3"
    write(
        f"{p}/01-create-archive-on-disk.bru",
        bru_http(
            "Create book-embeddings-archive (on_disk)",
            1,
            "PUT",
            "/book-embeddings-archive",
            body="""{
  "settings": { "index.knn": true },
  "mappings": {
    "properties": {
      "embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "mode": "on_disk"
      }
    }
  }
}""",
        ),
    )
    write(
        f"{p}/02-create-efficient-in-memory.bru",
        bru_http(
            "Create book-embeddings-efficient (in_memory)",
            2,
            "PUT",
            "/book-embeddings-efficient",
            body="""{
  "settings": { "index.knn": true },
  "mappings": {
    "properties": {
      "embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "mode": "in_memory",
        "data_type": "float"
      }
    }
  }
}""",
        ),
    )


def ch5_lesson5() -> None:
    p = "Chapter 5/Lesson 5"
    write(f"{p}/01-create-orders-index.bru", bru_http("Create orders index", 1, "PUT", "/orders"))
    write(f"{p}/02-create-book-browse-index.bru", bru_http("Create book-browse index", 2, "PUT", "/book-browse"))
    write(
        f"{p}/03-route-orders-to-power.bru",
        bru_http(
            "Route orders to power tier",
            3,
            "PUT",
            "/orders/_settings",
            body='{"index.routing.allocation.require.node_type": "power"}',
        ),
    )
    write(
        f"{p}/04-route-browse-to-standard.bru",
        bru_http(
            "Route book-browse to standard tier",
            4,
            "PUT",
            "/book-browse/_settings",
            body='{"index.routing.allocation.require.node_type": "standard"}',
        ),
    )
    write(
        f"{p}/05-search-backpressure-thresholds.bru",
        bru_http(
            "Search backpressure thresholds",
            5,
            "PUT",
            "/_cluster/settings",
            body="""{
  "persistent": {
    "search_backpressure.mode": "monitor_only",
    "search_backpressure.search_shard_task.cpu_time_millis_threshold": 30000,
    "search_backpressure.search_shard_task.elapsed_time_millis_threshold": 45000,
    "search_backpressure.search_task.total_heap_percent_threshold": 0.05,
    "search_backpressure.node_duress.cpu_threshold": 0.90,
    "search_backpressure.node_duress.heap_threshold": 0.70
  }
}""",
        ),
    )
    write(
        f"{p}/06-search-backpressure-cancellation.bru",
        bru_http(
            "Search backpressure cancellation limits",
            6,
            "PUT",
            "/_cluster/settings",
            body="""{
  "persistent": {
    "search_backpressure.search_task.cancellation_rate": 0.05,
    "search_backpressure.search_task.cancellation_burst": 10,
    "search_backpressure.search_shard_task.cancellation_rate": 0.05,
    "search_backpressure.search_shard_task.cancellation_burst": 15
  }
}""",
        ),
    )
    write(
        f"{p}/07-search-backpressure-stats.bru",
        bru_http("Search backpressure stats", 7, "GET", "/_nodes/stats/search_backpressure"),
    )
