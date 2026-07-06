"""Connect to an OpenSearch instance and verify the connection.

This is the "hello world" of the learning path (Chapter 1, Step 1). If this
script prints a cluster name and version, your ``src/.env`` is wired up and every
later lesson should be able to talk to your cluster.
"""

import sys
from pathlib import Path

# This script lives at ``src/Chapter 1/01-opensearch-status.py``. ``parents[1]``
# is the ``src/`` directory; adding it to ``sys.path`` makes ``from
# utils.opensearch_client import ...`` work, and ``src/.env`` lives right there.
_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import (
    open_search_client_from_env_file,
    print_opensearch_connection_test,
)

# All lessons read the same ``src/.env`` so you only configure your cluster once.
client = open_search_client_from_env_file(_SRC_ROOT / ".env")

if __name__ == "__main__":
    # Tries ``client.info()`` and prints the cluster name + version. Failures
    # print a friendly message instead of raising — useful when you're still
    # debugging your setup.
    print_opensearch_connection_test(client)
