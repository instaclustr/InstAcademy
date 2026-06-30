"""Print the mapping of ``my-index`` — the smallest possible diagnostic call.

``GET /<index>/_mapping`` is one of the first things you reach for when:
    * Wondering "did my mapping change take effect?"
    * Investigating "why is this query returning weird results?" (mapping
      decides analysis/tokenization for every field).
    * Comparing prod vs staging mappings before a deploy.

The response is a nested dict: ``{index_name: {"mappings": {...}}}``. The
inner ``mappings`` is exactly the shape you'd pass to ``indices.create()``.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, src_env_file

import json



def main() -> None:
    client = open_search_client_from_env_file(src_env_file(__file__))
    index_name = "my-index"
    # Plain ``get_mapping`` — no transformation. The response is verbose but
    # complete; you can copy/paste it back into a future ``indices.create``.
    response = client.indices.get_mapping(index=index_name)
    print(json.dumps(response, indent=2, default=str))


if __name__ == "__main__":
    main()
