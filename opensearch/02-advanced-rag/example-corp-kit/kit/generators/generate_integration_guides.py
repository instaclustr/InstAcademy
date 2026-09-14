"""
Generate the 50+ integration guides as markdown (optionally convertible to
PDF later, which gives lesson 1.3 a real parsing exercise: guides contain
tables, numbered steps, and boilerplate headers).

Usage:
    python generate_integration_guides.py --out ../output/integration_guides
"""
import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

from taxonomy import INTEGRATIONS, ERROR_CODES, PRODUCT_NAME, VERSIONS


def guide(rng, idx, name, category, auth):
    source_id = f"GUIDE-{idx:03d}"
    updated = datetime(2026, 6, 30) - timedelta(days=rng.randint(0, 700))
    min_version = rng.choice(VERSIONS[:-1])

    connector_errors = [(c, e) for c, e in ERROR_CODES.items()
                        if e[1] == "connectors"]
    picked = rng.sample(connector_errors, k=2)

    lines = [
        f"# {name} integration guide",
        "",
        f"Connect {name} to {PRODUCT_NAME} to query {category} data directly "
        f"from dashboards and the SQL Workbench. Requires platform version "
        f"{min_version} or later.",
        "",
        "## Prerequisites",
        "",
        f"1. A {name} account with permission to create credentials",
        f"2. Authentication method: {auth}",
        "3. Network access from the platform IP ranges to your "
        f"{name} endpoint (see the IP allowlisting page)",
        "",
        "## Connection settings",
        "",
        "| Field | Required | Notes |",
        "| --- | --- | --- |",
        f"| Host | Yes | Your {name} endpoint hostname |",
        "| Port | Yes | Default varies by deployment |",
        f"| Credential | Yes | {auth} |",
        "| Schema scope | No | Limit discovery to named schemas to avoid ERR-2288 |",
        "| TLS version | No | TLS 1.3 recommended; required by some warehouses |",
        "",
        "## Setup steps",
        "",
        "1. In the workspace, open Data Connectors and choose "
        f"{name} from the catalog.",
        f"2. Enter the connection settings above and provide your {auth} credential.",
        "3. Run the connection test. A successful test validates network "
        "reachability, authentication, and schema access in one pass.",
        "4. Choose the schemas to expose. Scoping schemas speeds up discovery "
        "on large catalogs.",
        "5. Save. The connector appears in the dataset builder within one minute.",
        "",
        "## Common errors",
        "",
    ]
    for code, (etitle, _a, cause, workaround, affects, fixed) in picked:
        lines += [f"### {code}: {etitle}", "",
                  f"Cause: {cause}.", "",
                  f"Resolution: {workaround}."]
        if fixed:
            lines += ["", f"Fixed in version {fixed}. Affected versions: "
                          f"{', '.join(affects)}."]
        lines.append("")

    lines += [
        "## Credential rotation",
        "",
        f"Rotate {name} credentials from the connector settings page. "
        "Rotation is zero downtime: the platform validates the new credential "
        "before retiring the old one. Expired credentials surface as ERR-2231 "
        "in the connector health panel.",
    ]

    meta = {
        "source_id": source_id,
        "title": f"{name} integration guide",
        "doc_type": "integration-guide",
        "integration": name,
        "category": category,
        "section_path": f"Integrations > {name}",
        "min_version": min_version,
        "acl": "public",
        "updated_at": updated.strftime("%Y-%m-%d"),
        "related_error_codes": [c for c, _ in picked] + ["ERR-2231"],
    }
    fm = "---\n" + "\n".join(f"{k}: {json.dumps(v)}" for k, v in meta.items()) + "\n---\n\n"
    return meta, fm + "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="../output/integration_guides")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    manifest = []
    for i, (name, category, auth) in enumerate(INTEGRATIONS, 1):
        meta, content = guide(rng, i, name, category, auth)
        fname = f"{meta['source_id']}-{name.lower().replace(' ', '-')}.md"
        (out / fname).write_text(content)
        manifest.append(meta)
    (out / "_manifest.jsonl").write_text("\n".join(json.dumps(m) for m in manifest))
    print(f"Wrote {len(manifest)} integration guides to {out}")


if __name__ == "__main__":
    main()
