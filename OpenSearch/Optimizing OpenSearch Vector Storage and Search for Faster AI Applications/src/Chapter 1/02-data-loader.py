"""Fetch books from the Gutendex API and save to ``src/sample-data.json``.

What this script teaches:
    * How to pull paginated data from a public REST API using only the Python
      standard library (no ``requests`` dependency).
    * How later OpenSearch lessons expect the data to be shaped on disk.

The dataset itself is used from Chapter 2 onward (neural ingest). Chapter 1 only
needs it downloaded. Output is a JSON object with top-level ``count`` and
``results`` (a list of book records), written next to ``src/`` so every chapter
can find it at the same relative path.
"""

import json
from pathlib import Path

# ``urllib.request`` ships with Python — using it instead of ``requests`` keeps
# this lesson dependency-free. For real apps prefer ``httpx`` or ``requests``.
from urllib.request import urlopen

# This file lives at ``src/Chapter 1/02-data-loader.py``; ``parents[1]`` is
# ``src/``. Writing to ``src/sample-data.json`` means every lesson script can load
# the same file from a known relative location without re-downloading it.
SAMPLE_DATA_PATH = Path(__file__).resolve().parents[1] / "sample-data.json"

# Gutendex is a free JSON API in front of Project Gutenberg (public-domain books).
# Perfect lab data: real titles/authors/summaries with no auth required.
GUTENDEX_URL = "https://gutendex.com/books"

# Set to None to fetch all pages (thousands of books), or a small integer to
# keep the demo dataset manageable. 3 pages * 32 results = ~96 books, plenty
# for indexing and search experiments without hammering the API.
MAX_PAGES = 3


def fetch_gutendex_books(max_pages=None):
    """Fetch books from Gutendex API with pagination (follows the 'next' URL).

    Gutendex returns a JSON envelope like::

        { "count": 75123, "next": "https://...&page=2", "results": [...] }

    The ``next`` URL is ``None`` once you reach the last page. This is a classic
    pagination pattern — the caller just walks until ``next`` is falsy.
    """
    url = GUTENDEX_URL
    all_results = []
    pages_fetched = 0
    data: dict = {}

    while url:
        # Respect the ``max_pages`` cap before making the next HTTP call.
        if max_pages is not None and pages_fetched >= max_pages:
            break
        with urlopen(url) as response:
            data = json.loads(response.read().decode())
        results = data.get("results", [])
        all_results.extend(results)
        pages_fetched += 1
        url = data.get("next")  # next page URL, or None when done

    # ``count`` is the total number of books in Gutendex (same on every page).
    return all_results, data.get("count", 0)


if __name__ == "__main__":
    try:
        results, total_count = fetch_gutendex_books(max_pages=MAX_PAGES)
        print(f"Gutendex: fetched {len(results)} books (total available: {total_count})")
        SAMPLE_DATA_PATH.write_text(
            json.dumps({"count": total_count, "results": results}, indent=2),
            encoding="utf-8",
        )
        print(f"Saved to {SAMPLE_DATA_PATH}")
    except Exception as e:
        # Broad catch: DNS, TLS, HTTP, or JSON errors — this is a lab helper.
        print(f"Gutendex request failed: {e}")
