"""Connect to an OpenSearch instance and verify the connection.

This is the "hello world" of the learning path. If this script prints a
cluster name and version, your ``src/.env`` is wired up and every later
lesson should be able to talk to your cluster.
"""

import sys
from pathlib import Path

# Lesson scripts live deep inside ``src/Chapter .../...`` and need to import
# from ``src/utils``. ``parents[2]`` is the ``src/`` directory; adding it to
# ``sys.path`` makes ``from utils.opensearch_client import ...`` work.
# This same 3-line stanza appears at the top of nearly every lesson script.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

# ``src_env_file(__file__)`` resolves to ``src/.env`` so every lesson reads the
# same connection settings. Editing one file reconfigures the whole course.
client = open_search_client_from_env_file(src_env_file(__file__))

if __name__ == "__main__":
    # Tries ``client.info()`` and prints the cluster name + version. Failures
    # print a friendly message instead of raising — useful when you're still
    # debugging your local setup.
    print_opensearch_connection_test(client)
