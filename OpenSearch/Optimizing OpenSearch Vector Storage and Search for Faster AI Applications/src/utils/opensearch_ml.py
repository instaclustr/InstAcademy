"""ML Commons helpers (tasks, models, etc.).

OpenSearch's ML Commons plugin runs long operations (register model, deploy
model, undeploy model) as **async tasks**. The HTTP response returns a
``task_id`` immediately; you then poll a separate endpoint to learn when the
work actually finished.

This module wraps that polling pattern so each lesson does not have to
re-implement the sleep/check/timeout loop.
"""

from __future__ import annotations

import time
from typing import Any

from opensearchpy import OpenSearch  # type: ignore[import-untyped]


def get_ml_task_status(client: OpenSearch, task_id: str) -> Any:
    """GET ``/_plugins/_ml/tasks/{task_id}`` and return the parsed response body.

    The response is a dict with at least a ``state`` field, e.g.
    ``"CREATED"``, ``"RUNNING"``, ``"COMPLETED"``, or ``"FAILED"``. When
    ``state == "COMPLETED"`` for a register call the dict also contains
    ``model_id``, which subsequent scripts pass back in to deploy/use.
    """
    # The Python client has no native wrapper for ML Commons routes, so we drop
    # down to the raw transport and hit the plugin's REST endpoint directly.
    return client.transport.perform_request("GET", f"/_plugins/_ml/tasks/{task_id}")


def poll_ml_task(
    client: OpenSearch,
    task_id: str,
    *,
    timeout_seconds: int = 120,
    poll_interval: float = 2.0,
) -> dict[str, Any] | Any:
    """Poll task status until ``COMPLETED``, ``FAILED``, or timeout.

    Why a polling loop?
        ML Commons tasks (download, register, deploy a model) can take from a
        few seconds (a small encoder) to a few minutes (large models on cold
        clusters). The HTTP call that kicks one off returns *immediately* with
        only a ``task_id`` — there's no streaming/notification mechanism, so
        we fetch status every ``poll_interval`` seconds.

    Args:
        client: An ``OpenSearch`` client.
        task_id: ID returned by a register/deploy/undeploy call.
        timeout_seconds: Give up after this many seconds and return a fake
            ``{"state": "TIMEOUT"}`` so the caller can decide what to do.
        poll_interval: Seconds between status checks. Keep this >= 1s to avoid
            spamming the cluster.
    """
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        task = get_ml_task_status(client, task_id)
        if isinstance(task, dict):
            state = task.get("state")
            # Only these two states are terminal — anything else means "keep
            # polling" (CREATED, RUNNING, etc.).
            if state in {"COMPLETED", "FAILED"}:
                return task
        time.sleep(poll_interval)
    # Timeout: synthesize a result so callers can branch on ``state`` without
    # special-casing ``None`` everywhere.
    return {"task_id": task_id, "state": "TIMEOUT"}
