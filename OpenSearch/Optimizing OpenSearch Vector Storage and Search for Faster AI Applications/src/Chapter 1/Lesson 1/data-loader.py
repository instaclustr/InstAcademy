"""Fetch books from Gutendex API and save to sample-data.json.

What this script teaches:
    * How to pull paginated data from a public REST API using only the Python
      standard library (no ``requests`` dependency).
    * How later OpenSearch lessons expect the data to be shaped on disk.

Output matches what later chapters expect: a JSON object with top-level ``count``
and ``results`` (list of book records). It is written next to ``src/``, not
inside this lesson folder, so every chapter can find it at the same relative path.
"""

import json
from pathlib import Path

# ``urllib.request`` ships with Python — using it instead of ``requests`` keeps
# this lesson dependency-free. For real apps prefer ``httpx`` or ``requests``.
from urllib.request import urlopen

# ``parents[2]`` is ``src/`` (this file lives under Chapter 1/Lesson 1).
# Writing to ``src/sample-data.json`` means *every* lesson script can load the
# same file from a known relative location without re-downloading it.
SAMPLE_DATA_PATH = Path(__file__).resolve().parents[2] / "sample-data.json"

# Gutendex is a free JSON API in front of Project Gutenberg (public-domain books).
# Perfect lab data: real titles/authors/summaries with no auth required.
GUTENDEX_URL = "https://gutendex.com/books"

# Set to None to fetch all pages (thousands of books), or a small integer to
# keep the demo dataset manageable. 3 pages * 32 results = ~96 books, plenty
# for indexing and search experiments without hammering the API.
MAX_PAGES = 3


def fetch_gutendex_books(max_pages=None):
    """Fetch books from Gutendex API with pagination (follows 'next' URL).

    Gutendex returns a JSON envelope like::

        { "count": 75123, "next": "https://...&page=2", "results": [...] }

    The ``next`` URL is ``None`` once you reach the last page. This is a
    classic pagination pattern — the caller doesn't have to know the total page
    count, just walk until ``next`` is falsy.
    """
    url = GUTENDEX_URL
    all_results = []
    pages_fetched = 0
    data: dict = {}

    while url:
        # Respect the ``max_pages`` cap before making the next HTTP call —
        # otherwise we'd do one extra request and throw it away.
        if max_pages is not None and pages_fetched >= max_pages:
            break
        with urlopen(url) as response:
            # ``response.read()`` is bytes; decode to a string before json.loads.
            data = json.loads(response.read().decode())
        results = data.get("results", [])
        # ``extend`` (not ``append``) so we accumulate one flat list, not a
        # list of lists.
        all_results.extend(results)
        pages_fetched += 1
        url = data.get("next")  # next page URL, or None when done

    # ``count`` is the total number of books in Gutendex (same on every page),
    # NOT ``len(results)``. We forward it so consumers can see "we fetched 96
    # out of 75123 available".
    return all_results, data.get("count", 0)


if __name__ == "__main__":
    # ``if __name__ == "__main__"`` is the standard "only run this when the
    # file is executed directly, not when imported" guard. Lets other scripts
    # ``from data-loader import fetch_gutendex_books`` without side effects.
    try:
        results, total_count = fetch_gutendex_books(max_pages=MAX_PAGES)
        print(f"Gutendex: fetched {len(results)} books (total available: {total_count})")
        # Persist as JSON so the data survives between lessons. ``indent=2``
        # makes the file human-readable for poking around with an editor.
        SAMPLE_DATA_PATH.write_text(
            json.dumps({"count": total_count, "results": results}, indent=2),
            encoding="utf-8",
        )
        print(f"Saved to {SAMPLE_DATA_PATH}")
    except Exception as e:
        # Broad catch: DNS, TLS, HTTP errors, JSON issues — script is a lab helper, not a library.
        # In production code you'd narrow this to ``URLError`` / ``HTTPError`` etc.
        print(f"Gutendex request failed: {e}")
