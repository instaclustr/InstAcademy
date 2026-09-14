"""
Generate the REST API reference for the Example Corp platform as one JSON
spec plus one markdown page per endpoint. Endpoints reference the same
error codes as everything else (ERR-6601 rate limits, ERR-6640 embed URLs).

Usage:
    python generate_api_reference.py --out ../output/api_reference
"""
import argparse
import json
from pathlib import Path

ENDPOINTS = [
    ("GET", "/v2/dashboards", "List dashboards",
     [("workspace_id", "string", True), ("page", "integer", False),
      ("page_size", "integer", False)],
     ["ERR-6601"]),
    ("GET", "/v2/dashboards/{dashboard_id}", "Get a dashboard",
     [("dashboard_id", "string", True)], ["ERR-6601"]),
    ("POST", "/v2/dashboards/{dashboard_id}/export", "Export a dashboard to PDF",
     [("dashboard_id", "string", True), ("format", "string", False),
      ("dpi", "integer", False)],
     ["ERR-1210", "ERR-6601"]),
    ("POST", "/v2/embed/urls", "Create a signed embed URL",
     [("dashboard_id", "string", True), ("user_attributes", "object", False),
      ("expires_in", "integer", False)],
     ["ERR-6640", "ERR-6601"]),
    ("GET", "/v2/datasets", "List datasets",
     [("workspace_id", "string", True)], ["ERR-6601"]),
    ("POST", "/v2/datasets/{dataset_id}/refresh", "Trigger a dataset refresh",
     [("dataset_id", "string", True), ("mode", "string", False)],
     ["ERR-3305", "ERR-6601"]),
    ("GET", "/v2/datasets/{dataset_id}/refresh/{job_id}", "Get refresh status",
     [("dataset_id", "string", True), ("job_id", "string", True)], ["ERR-6601"]),
    ("GET", "/v2/connectors", "List connectors",
     [("workspace_id", "string", True)], ["ERR-6601"]),
    ("POST", "/v2/connectors/{connector_id}/test", "Test a connector",
     [("connector_id", "string", True)], ["ERR-2209", "ERR-2231", "ERR-2288"]),
    ("POST", "/v2/alerts", "Create an alert",
     [("dashboard_id", "string", True), ("condition", "object", True),
      ("channels", "array", True)],
     ["ERR-4402", "ERR-6601"]),
    ("POST", "/v2/webhooks", "Register a webhook",
     [("url", "string", True), ("events", "array", True),
      ("secret", "string", False)],
     ["ERR-4415", "ERR-6601"]),
    ("GET", "/v2/audit/events", "Query audit events",
     [("from", "string", True), ("to", "string", True),
      ("actor", "string", False)],
     ["ERR-6601"]),
    ("POST", "/v2/scim/Users", "Provision a user (SCIM)",
     [("userName", "string", True), ("emails", "array", True)],
     ["ERR-7733"]),
    ("GET", "/v2/queries/{query_id}/results", "Fetch SQL Workbench results",
     [("query_id", "string", True), ("cursor", "string", False)],
     ["ERR-5501", "ERR-6601"]),
]

AUTH_NOTE = (
    "All endpoints require a service account bearer token in the "
    "Authorization header. Rate limit: 600 requests per minute per service "
    "account. Exceeding it returns HTTP 429 with error code ERR-6601."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="../output/api_reference")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    manifest = []
    spec = {"title": "Example Corp Platform API v2", "auth": AUTH_NOTE,
            "endpoints": []}

    for i, (method, path, summary, params, errors) in enumerate(ENDPOINTS, 1):
        source_id = f"API-{i:03d}"
        endpoint_slug = path.strip("/").replace("/", "-").replace("{", "").replace("}", "")
        lines = [
            f"# {method} {path}", "",
            summary + ".", "",
            AUTH_NOTE, "",
            "## Parameters", "",
            "| Name | Type | Required |",
            "| --- | --- | --- |",
        ]
        lines += [f"| {n} | {t} | {'Yes' if r else 'No'} |" for n, t, r in params]
        lines += ["", "## Errors", ""]
        lines += [f"- {e}" for e in errors]
        lines += ["", "## Example", "", "```bash",
                  f"curl -X {method} \\",
                  f"  'https://api.example-corp.com{path}' \\",
                  "  -H 'Authorization: Bearer $TOKEN'",
                  "```"]

        meta = {
            "source_id": source_id,
            "title": f"{method} {path}",
            "doc_type": "api-reference",
            "section_path": f"API Reference > {summary}",
            "method": method, "path": path,
            "related_error_codes": errors,
            "acl": "public",
            "updated_at": "2026-06-30",
        }
        fm = "---\n" + "\n".join(f"{k}: {json.dumps(v)}" for k, v in meta.items()) + "\n---\n\n"
        (out / f"{source_id}-{method.lower()}-{endpoint_slug}.md").write_text(
            fm + "\n".join(lines))
        manifest.append(meta)
        spec["endpoints"].append(
            {"method": method, "path": path, "summary": summary,
             "params": [{"name": n, "type": t, "required": r} for n, t, r in params],
             "errors": errors})

    (out / "_manifest.jsonl").write_text("\n".join(json.dumps(m) for m in manifest))
    (out / "openapi-lite.json").write_text(json.dumps(spec, indent=2))
    print(f"Wrote {len(manifest)} API reference pages to {out}")


if __name__ == "__main__":
    main()
