#!/usr/bin/env python3
"""Generate Bruno .bru request files for InstAcademy OpenSearch course.

Run from repo root: python tools/generate-bruno-requests.py
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BRUNO = REPO / "bruno"


def bru_http(
    name: str,
    seq: int,
    method: str,
    path: str,
    *,
    body: str | None = None,
    body_type: str = "json",
    note: str = "",
) -> str:
    m = method.lower()
    lines = [
        "meta {",
        f"  name: {name}",
        "  type: http",
        f"  seq: {seq}",
        "}",
        "",
    ]
    if note:
        lines.extend([f"docs {{\n{note}\n}}", ""])
    lines.extend([
        f"{m} {{",
        f"  url: {{{{baseUrl}}}}{path}",
        f"  body: {body_type if body else 'none'}",
        "  auth: basic",
        "}",
        "",
        "auth:basic {",
        "  username: {{username}}",
        "  password: {{password}}",
        "}",
    ])
    if body and body_type == "json":
        lines.extend(["", "body:json {", body, "}"])
    elif body and body_type == "file":
        lines.extend(["", "body:file {", body, "}"])
    return "\n".join(lines) + "\n"


_FILES_WRITTEN = 0


def write(rel: str, content: str) -> None:
    global _FILES_WRITTEN
    path = BRUNO / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    _FILES_WRITTEN += 1


def bulk_ndjson(filename: str) -> str:
    return f"file: ../../../rest/bulk/{filename}\n  contentType: application/x-ndjson"


def query_vector_json() -> str:
    path = REPO / "src/Chapter 4/Lesson 1/001-bookstore-rag-query-vector.json"
    return path.read_text(encoding="utf-8").strip()


def ml_poll(seq: int = 99) -> str:
    return bru_http(
        "Poll ML task",
        seq,
        "GET",
        "/_plugins/_ml/tasks/{{taskId}}",
        note="Run repeatedly after register/deploy until state is COMPLETED. "
        "Set taskId from the previous response. Copy model_id when done.",
    )


def ch1() -> None:
    base = "Chapter 1"
    write(
        f"{base}/Lesson 1/01-cluster-info.bru",
        bru_http("Cluster info", 1, "GET", "/"),
    )
    write(
        f"{base}/Lesson 2/01-delete-keyword-index.bru",
        bru_http("Delete keyword-index if exists", 1, "DELETE", "/keyword-index"),
    )
    write(
        f"{base}/Lesson 2/02-create-keyword-index.bru",
        bru_http(
            "Create keyword-index",
            2,
            "PUT",
            "/keyword-index",
            body="""{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword", "ignore_above": 256 }
        }
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
    write(
        f"{base}/Lesson 2/03-bulk-sample-books.bru",
        bru_http(
            "Bulk index sample books",
            3,
            "POST",
            "/_bulk",
            body=bulk_ndjson("chapter-1-keyword-index-sample.ndjson"),
            body_type="file",
        ),
    )
    write(
        f"{base}/Lesson 2/04-refresh-keyword-index.bru",
        bru_http("Refresh keyword-index", 4, "POST", "/keyword-index/_refresh"),
    )


def ch2_lesson1() -> None:
    p = "Chapter 2/Lesson 1"
    write(f"{p}/01-cluster-info.bru", bru_http("Cluster info", 1, "GET", "/"))
    write(
        f"{p}/02-enable-url-model-registration.bru",
        bru_http(
            "Enable URL model registration",
            2,
            "PUT",
            "/_cluster/settings",
            body="""{
  "persistent": {
    "plugins.ml_commons.allow_registering_model_via_url": true
  }
}""",
        ),
    )
    write(
        f"{p}/03-register-model-group.bru",
        bru_http(
            "Register model group",
            3,
            "POST",
            "/_plugins/_ml/model_groups/_register",
            body="""{
  "name": "huggingface-models",
  "description": "A group for Hugging Face transformer models"
}""",
            note="Save model_group_id from the response into modelGroupId.",
        ),
    )
    write(
        f"{p}/04-register-model.bru",
        bru_http(
            "Register msmarco-distilbert model",
            4,
            "POST",
            "/_plugins/_ml/models/_register",
            body="""{
  "name": "huggingface/sentence-transformers/msmarco-distilbert-base-tas-b",
  "version": "1.0.3",
  "model_group_id": "{{modelGroupId}}",
  "model_format": "TORCH_SCRIPT"
}""",
            note="If response has task_id, set taskId and poll. On COMPLETED, save model_id to modelId.",
        ),
    )
    write(f"{p}/05-poll-ml-task.bru", ml_poll(5))
    write(
        f"{p}/06-deploy-model.bru",
        bru_http(
            "Deploy model",
            6,
            "POST",
            "/_plugins/_ml/models/{{modelId}}/_deploy",
            note="Poll again if deploy returns task_id.",
        ),
    )
    write(f"{p}/07-poll-ml-task-deploy.bru", ml_poll(7))
    write(
        f"{p}/08-text-embedding-predict.bru",
        bru_http(
            "Text embedding predict",
            8,
            "POST",
            "/_plugins/_ml/_predict/text_embedding/{{modelId}}",
            body="""{
  "text_docs": ["historical fiction with an underdog story"],
  "target_response": ["sentence_embedding"]
}""",
        ),
    )


def ch2_lesson2() -> None:
    p = "Chapter 2/Lesson 2"
    write(
        f"{p}/01-create-ingest-pipeline.bru",
        bru_http(
            "Create vector-search-embeddings-pipeline",
            1,
            "PUT",
            "/_ingest/pipeline/vector-search-embeddings-pipeline",
            body="""{
  "description": "Pipeline for processing OpenSearch index data",
  "processors": [
    {
      "text_embedding": {
        "model_id": "{{modelId}}",
        "field_map": {
          "passage_text": "passage_embedding"
        }
      }
    }
  ]
}""",
        ),
    )
    write(
        f"{p}/02-create-vector-search-index.bru",
        bru_http(
            "Create vector-search-index",
            2,
            "PUT",
            "/vector-search-index",
            body="""{
  "settings": {
    "index.knn": true,
    "default_pipeline": "vector-search-embeddings-pipeline"
  },
  "mappings": {
    "properties": {
      "id": { "type": "text" },
      "passage_embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "engine": "lucene",
          "space_type": "l2",
          "name": "hnsw",
          "parameters": {}
        }
      },
      "passage_text": { "type": "text" },
      "title": { "type": "text" },
      "authors": { "type": "object", "enabled": false },
      "subjects": { "type": "keyword" },
      "bookshelves": { "type": "keyword" }
    }
  }
}""",
        ),
    )
    write(
        f"{p}/03-bulk-ingest-books.bru",
        bru_http(
            "Bulk ingest sample books",
            3,
            "POST",
            "/_bulk?timeout=60s",
            body=bulk_ndjson("chapter-2-lesson-2-vector-search-index.ndjson"),
            body_type="file",
            note="Embedding runs in the ingest pipeline — may take several minutes.",
        ),
    )
    write(
        f"{p}/04-neural-search.bru",
        bru_http(
            "Neural + keyword search",
            4,
            "GET",
            "/vector-search-index/_search",
            body="""{
  "_source": { "excludes": ["passage_embedding"] },
  "query": {
    "bool": {
      "filter": { "wildcard": { "id": "*1" } },
      "should": [
        {
          "script_score": {
            "query": {
              "neural": {
                "passage_embedding": {
                  "query_text": "historical fiction with an underdog story",
                  "model_id": "{{modelId}}",
                  "k": 100
                }
              }
            },
            "script": { "source": "_score * 1.5" }
          }
        },
        {
          "script_score": {
            "query": {
              "match": { "passage_text": "historical fiction with an underdog story" }
            },
            "script": { "source": "_score * 1.7" }
          }
        }
      ]
    }
  }
}""",
        ),
    )


def _run_remaining_chapters() -> None:
    remaining_path = Path(__file__).parent / "bruno_chapters_remaining.py"
    g: dict = {
        "write": write,
        "bru_http": bru_http,
        "ml_poll": ml_poll,
        "bulk_ndjson": bulk_ndjson,
        "query_vector_json": query_vector_json,
    }
    exec(compile(remaining_path.read_text(encoding="utf-8"), str(remaining_path), "exec"), g)
    for name in (
        "ch1_lesson4",
        "ch2_lesson4",
        "ch2_lesson5",
        "ch3_lesson1",
        "ch4_lesson1",
        "ch4_lesson2",
        "ch4_lesson3",
        "ch5_lesson1",
        "ch5_lesson2",
        "ch5_lesson3",
        "ch5_lesson5",
    ):
        g[name]()


def main() -> None:
    global _FILES_WRITTEN
    _FILES_WRITTEN = 0
    ch1()
    ch2_lesson1()
    ch2_lesson2()
    _run_remaining_chapters()
    print(f"Generated {_FILES_WRITTEN} Bruno .bru request files under {BRUNO.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
