"""
Shared OpenSearch HTTP helper for the lab scripts. Standard library only:
no pip installs. Reads the cluster URL (with credentials) from the OS_URL
environment variable, format https://user:pass@host:9200.
"""
import base64
import json
import os
import ssl
import sys
import urllib.parse
import urllib.request


def endpoint():
    raw = os.environ.get("OS_URL")
    if not raw:
        sys.exit("OS_URL is not set. Lab 0 Step 1 explains how to set it.")
    parts = urllib.parse.urlsplit(raw.rstrip("/"))
    base = f"{parts.scheme}://{parts.hostname}"
    if parts.port:
        base += f":{parts.port}"
    auth = None
    if parts.username:
        token = f"{parts.username}:{parts.password or ''}"
        auth = "Basic " + base64.b64encode(token.encode()).decode()
    return base, auth


_CTX = ssl.create_default_context()
if os.environ.get("OS_VERIFY", "true").lower() == "false":
    _CTX.check_hostname = False
    _CTX.verify_mode = ssl.CERT_NONE


def request(method, path, body=None, ndjson=None, timeout=120):
    """Send one request; return (status_code, parsed_json)."""
    base, auth = endpoint()
    url = f"{base}/{path.lstrip('/')}"
    data, ctype = None, None
    if ndjson is not None:
        data, ctype = ndjson.encode(), "application/x-ndjson"
    elif body is not None:
        data, ctype = json.dumps(body).encode(), "application/json"
    req = urllib.request.Request(url, data=data, method=method)
    if ctype:
        req.add_header("Content-Type", ctype)
    if auth:
        req.add_header("Authorization", auth)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        payload = e.read().decode()
        try:
            payload = json.loads(payload)
        except ValueError:
            pass
        return e.code, payload
