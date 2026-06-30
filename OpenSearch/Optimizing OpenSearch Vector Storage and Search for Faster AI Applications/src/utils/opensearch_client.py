"""Build an OpenSearch client from a lesson ``.env`` file or explicit parameters.

The lesson scripts share one ``src/.env`` (host, username, password, optional
``ML_MODEL_ID``). This module turns that file (or explicit args) into a configured
``opensearchpy.OpenSearch`` instance you can call like a normal HTTP client.

Why a helper module?
  * Each lesson lives in ``src/<Chapter>/<Lesson>/*.py``. Without a helper we'd
    duplicate the ``hosts``/``http_auth``/``use_ssl`` plumbing in every script.
  * Most local labs run plain HTTP on ``localhost:9200``; managed clusters use
    TLS + basic auth. The defaults here favour the safer (TLS) path so you don't
    accidentally send credentials over plaintext to a production cluster.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

# python-dotenv reads KEY=VALUE pairs from a ``.env`` file into ``os.environ``.
# Installed as a dependency so the lessons don't have to hand-roll a parser.
from dotenv import load_dotenv

# ``opensearchpy`` is the official Python client. ``# type: ignore`` is just
# telling type-checkers the package ships without inline type stubs.
from opensearchpy import OpenSearch  # type: ignore[import-untyped]


def print_opensearch_connection_test(
    client: OpenSearch,
    *,
    include_version: bool = True,
    raise_on_error: bool = False,
) -> dict[str, Any] | None:
    """Call ``client.info()`` and print a short connectivity summary for lab scripts.

    ``client.info()`` hits ``GET /`` on the cluster — the cheapest endpoint to
    confirm the client is configured correctly (host, port, TLS, credentials).

    Args:
        client: An already-constructed ``OpenSearch`` instance.
        include_version: When True, print the cluster's version number.
        raise_on_error: When True, re-raise connection errors so a CI/lab run
            fails loudly. Default False is friendlier for interactive use.

    Returns the info mapping on success, or ``None`` on failure (unless ``raise_on_error``).
    """
    try:
        info = client.info()
        print("Connected to OpenSearch")
        # ``cluster_name`` is whatever was set in ``cluster.name`` on the node(s).
        print(f"Cluster: {info.get('cluster_name', 'unknown')}")
        if include_version:
            ver = info.get("version")
            # ``info["version"]`` is a dict like ``{"number": "2.13.0", ...}``.
            # Be defensive in case a future server changes shape.
            if isinstance(ver, dict):
                print(f"Version: {ver.get('number', 'unknown')}")
            else:
                print("Version: unknown")
        return info
    except Exception as exc:
        # Broad ``except`` is intentional here — DNS, TLS, auth, and HTTP errors
        # all funnel up as different exception types, and lab scripts just want
        # to know "connection worked or not".
        print(f"Connection failed: {exc}")
        if raise_on_error:
            raise
        return None


def src_env_file(__file__: str | Path) -> Path:
    """Return the path to the shared ``src/.env`` for lesson scripts at ``src/<chapter>/<lesson>/*.py``.

    ``parents[2]`` walks up three levels:
        src/Chapter 2/Lesson 1/001-setup.py   # __file__
        src/Chapter 2/Lesson 1                # parents[0]
        src/Chapter 2                         # parents[1]
        src/                                  # parents[2]  <-- env lives here

    All lessons read the same ``src/.env`` so you only configure your cluster once.
    """
    return Path(__file__).resolve().parents[2] / ".env"


def load_src_dotenv(__file__: str | Path, *, override: bool = False) -> Path:
    """Load ``src/.env`` into ``os.environ`` (for code that reads env vars before building a client).

    Use this when a script calls ``os.environ.get("ML_MODEL_ID")`` *before* it
    constructs the client. ``open_search_client_from_env_file`` already calls
    ``load_dotenv`` internally, but it only runs at client-build time.
    """
    path = src_env_file(__file__)
    # ``override=False`` keeps existing environment values (handy when CI sets
    # secrets that should win over a local ``.env``).
    load_dotenv(path, override=override)
    return path


def open_search_client_from_env_file(
    env_file: Path,
    *,
    use_ssl: bool | None = None,
    verify_certs: bool | None = None,
    port: int | None = None,
) -> OpenSearch:
    """Load ``env_file`` with python-dotenv, then return a configured ``OpenSearch`` client.

    The ``.env`` is expected to contain:
        OPENSEARCH_HOST=<hostname>
        OPENSEARCH_USERNAME=<user>      (optional)
        OPENSEARCH_PASSWORD=<password>  (optional)
        ML_MODEL_ID=<deployed model id> (used by individual lessons, not here)

    When ``use_ssl`` or ``verify_certs`` is ``None``, TLS verification defaults to enabled
    (matching managed clusters). Pass ``False`` for local HTTP-only clusters.
    """
    load_dotenv(env_file)
    # Three-way: None means "use the safe default", explicit True/False overrides.
    use_ssl_eff = True if use_ssl is None else use_ssl
    verify_eff = True if verify_certs is None else verify_certs
    port_eff = 9200 if port is None else port
    client_kwargs: dict = {
        # ``hosts`` is a list because the client can round-robin across nodes.
        "hosts": [{"host": os.environ.get("OPENSEARCH_HOST", "localhost"), "port": port_eff}],
        # gzip request bodies on the wire (big bulk requests benefit a lot).
        "http_compress": True,
        "use_ssl": use_ssl_eff,
        "verify_certs": verify_eff,
    }
    username = os.environ.get("OPENSEARCH_USERNAME")
    password = os.environ.get("OPENSEARCH_PASSWORD")
    # Only attach basic-auth credentials if both are present; an unauthenticated
    # local node should not have ``http_auth`` set at all.
    if username and password:
        client_kwargs["http_auth"] = (username, password)
    return OpenSearch(**client_kwargs)


def open_search_client_from_connection(
    *,
    host: str = "localhost",
    port: int = 9200,
    use_ssl: bool = False,
    verify_certs: bool = False,
    http_auth: tuple[str, str] | None = None,
) -> OpenSearch:
    """Build a client without reading a ``.env`` file (local demos and notebooks).

    Mirrors ``open_search_client_from_env_file`` but with explicit arguments —
    useful when you want to spin up a one-off client inside a Jupyter cell or
    a unit test without touching the filesystem.
    """
    kwargs: dict = {
        "hosts": [{"host": host, "port": port}],
        "http_compress": True,
        "use_ssl": use_ssl,
        "verify_certs": verify_certs,
    }
    if http_auth is not None:
        kwargs["http_auth"] = http_auth
    return OpenSearch(**kwargs)
