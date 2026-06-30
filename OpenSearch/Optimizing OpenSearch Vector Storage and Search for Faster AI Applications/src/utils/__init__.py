"""Shared helpers for OpenSearch learning-path scripts.

This ``utils`` package centralizes things every lesson needs:
  * Building an ``OpenSearch`` client (with or without a ``.env`` file).
  * Verifying connectivity (``print_opensearch_connection_test``).
  * Polling long-running ML Commons tasks (model register/deploy/undeploy).

Lesson scripts add ``src/`` to ``sys.path`` and then ``import`` from here so they
don't repeat the connection / polling boilerplate. See ``opensearch_client.py``
and ``opensearch_ml.py`` for details on each helper.
"""

from .opensearch_client import (
    load_src_dotenv,
    open_search_client_from_connection,
    open_search_client_from_env_file,
    print_opensearch_connection_test,
    src_env_file,
)
from .opensearch_ml import get_ml_task_status, poll_ml_task

__all__ = [
    "get_ml_task_status",
    "load_src_dotenv",
    "open_search_client_from_connection",
    "open_search_client_from_env_file",
    "poll_ml_task",
    "print_opensearch_connection_test",
    "src_env_file",
]
