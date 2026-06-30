#!/usr/bin/env python3
"""Generate NDJSON bulk files for Dev Tools and Bruno from src/sample-data.json.

Run from repo root:
    python tools/generate-bulk-ndjson.py

Outputs under rest/bulk/ — one file per lesson index shape.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SAMPLE = REPO / "src" / "sample-data.json"
OUT = REPO / "rest" / "bulk"


def load_books() -> list[dict]:
    data = json.loads(SAMPLE.read_text(encoding="utf-8"))
    return data.get("results", [])


def passage_text(book: dict) -> str:
    summaries = book.get("summaries") or []
    return summaries[0] if summaries else ""


def write_ndjson(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {path} ({len(lines) // 2} docs)")


def ch2_lesson2_vector_index(books: list[dict]) -> None:
    lines: list[str] = []
    for book in books:
        doc = {
            "id": str(book.get("id", "")),
            "title": book.get("title", ""),
            "authors": book.get("authors", []),
            "subjects": book.get("subjects", []),
            "passage_text": passage_text(book),
            "bookshelves": book.get("bookshelves", []),
        }
        bid = doc["id"]
        lines.append(json.dumps({"index": {"_index": "vector-search-index", "_id": bid}}))
        lines.append(json.dumps(doc))
    write_ndjson(OUT / "chapter-2-lesson-2-vector-search-index.ndjson", lines)


def ch3_sparse_index(books: list[dict]) -> None:
    lines: list[str] = []
    for book in books:
        doc = {
            "id": str(book.get("id", "")),
            "title": book.get("title", ""),
            "passage_text": passage_text(book),
        }
        bid = doc["id"]
        lines.append(json.dumps({"index": {"_index": "my-sparse-neural-index", "_id": bid}}))
        lines.append(json.dumps(doc))
    write_ndjson(OUT / "chapter-3-lesson-1-sparse-index.ndjson", lines)


def ch4_bookstore_rag(books: list[dict], index: str = "bookstore-rag-index") -> None:
    lines: list[str] = []
    for book in books:
        text = passage_text(book)
        doc = {
            "book_id": str(book.get("id", "")),
            "title": book.get("title", ""),
            "authors": [a.get("name", "") for a in book.get("authors", [])],
            "passage_text": text,
            "content": text,
        }
        bid = doc["book_id"]
        lines.append(json.dumps({"index": {"_index": index, "_id": bid}}))
        lines.append(json.dumps(doc))
    write_ndjson(OUT / f"chapter-4-{index}.ndjson", lines)


def ch2_lesson2_sample_three(books: list[dict]) -> None:
    """Small inline-friendly bulk (3 docs) for learn-mode READMEs."""
    subset = books[:3]
    lines: list[str] = []
    for book in subset:
        doc = {
            "id": str(book.get("id", "")),
            "title": book.get("title", ""),
            "authors": book.get("authors", []),
            "subjects": book.get("subjects", []),
            "passage_text": passage_text(book),
            "bookshelves": book.get("bookshelves", []),
        }
        bid = doc["id"]
        lines.append(json.dumps({"index": {"_index": "vector-search-index", "_id": bid}}))
        lines.append(json.dumps(doc))
    write_ndjson(OUT / "sample-three-books-vector-search-index.ndjson", lines)


def ch1_keyword_sample() -> None:
    books = [
        {
            "isbn": "978-0143127740",
            "title": "The Martian",
            "author": "Andy Weir",
            "genre": "Science Fiction",
            "publisher": "Crown Publishing",
            "description": "An astronaut stranded on Mars fights to survive until rescue is possible.",
            "price": 16.99,
            "in_stock": True,
            "published_year": 2014,
        },
        {
            "isbn": "978-0307277677",
            "title": "The Road",
            "author": "Cormac McCarthy",
            "genre": "Fiction",
            "publisher": "Vintage",
            "description": "A father and son journey through a post-apocalyptic landscape.",
            "price": 15.95,
            "in_stock": True,
            "published_year": 2006,
        },
        {
            "isbn": "978-0061120084",
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "genre": "Classic",
            "publisher": "Harper Perennial",
            "description": "A coming-of-age story set in the American South.",
            "price": 12.99,
            "in_stock": False,
            "published_year": 1960,
        },
    ]
    lines: list[str] = []
    for book in books:
        lines.append(json.dumps({"index": {"_index": "keyword-index", "_id": book["isbn"]}}))
        lines.append(json.dumps(book))
    write_ndjson(OUT / "chapter-1-keyword-index-sample.ndjson", lines)


def ch1_lesson4_vectors(books: list[dict] | None = None) -> None:
    """Three docs with deterministic 256-dim vectors (matches main.py)."""
    def sample_vector(dim: int, seed: float) -> list[float]:
        return [((i * 0.017 + seed) % 1.0) for i in range(dim)]

    sample_docs = [
        {"_id": "1", "title": "Intro to search", "seed": 0.1},
        {"_id": "2", "title": "Vectors in practice", "seed": 0.3},
        {"_id": "3", "title": "Scaling retrieval", "seed": 0.55},
    ]
    lines: list[str] = []
    for doc in sample_docs:
        body = {
            "title": doc["title"],
            "my_vector": sample_vector(256, doc["seed"]),
        }
        lines.append(json.dumps({"index": {"_index": "my-vector-index", "_id": doc["_id"]}}))
        lines.append(json.dumps(body))
    write_ndjson(OUT / "chapter-1-lesson-4-vector-index.ndjson", lines)


def main() -> None:
    if not SAMPLE.is_file():
        raise SystemExit(f"Missing {SAMPLE} — run Chapter 1 data-loader first or commit sample-data.json")
    books = load_books()
    ch1_keyword_sample()
    ch1_lesson4_vectors()
    ch2_lesson2_sample_three(books)
    ch2_lesson2_vector_index(books)
    ch3_sparse_index(books)
    ch4_bookstore_rag(books, "bookstore-rag-index")
    ch4_bookstore_rag(books, "bookstore-rag")


if __name__ == "__main__":
    main()
