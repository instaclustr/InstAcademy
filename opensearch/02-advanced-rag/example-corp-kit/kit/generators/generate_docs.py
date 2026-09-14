"""
Generate Example Corp product documentation pages as markdown with YAML
frontmatter. Deterministic under a fixed seed.

Usage:
    python generate_docs.py --pages 400 --out ../output/docs

Each page carries the metadata that lesson 1.3 tells learners to stamp
early: source_id, section_path, doc_type, product_version, acl, updated_at.
"""
import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

from taxonomy import (PRODUCT_AREAS, ERROR_CODES, VERSIONS, PLAN_TIERS,
                      PRODUCT_NAME)

PAGE_KINDS = ["overview", "how-to", "reference", "troubleshooting", "concepts"]

INTRO_TEMPLATES = [
    "{feature_title} lets your team {benefit} without leaving {product}.",
    "This page explains how {feature} works in {product} and how to configure it for production workloads.",
    "{feature_title} is available on version {version} and later. This guide covers setup, limits, and common failure modes.",
]

BENEFITS = [
    "act on data faster", "reduce time to insight", "standardize reporting",
    "keep dashboards responsive at scale", "control who sees what",
    "automate repetitive analysis",
]

BODY_TEMPLATES = [
    "To enable {feature}, open the workspace settings panel and select the {area_label} tab. Changes apply within one refresh cycle and do not require a restart.",
    "By default, {feature} is limited to {limit} per workspace on the {tier} tier. Administrators can raise this limit from the admin console.",
    "When {feature} is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.",
    "Performance tip: {feature} performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.",
    "Audit events for {feature} are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.",
    "If your organization uses SAML SSO, {feature} inherits group membership from your identity provider on each login.",
]

SETTINGS_ROWS = [
    ("enabled", "boolean", "true", "Turns the feature on for the workspace"),
    ("max_concurrency", "integer", "8", "Upper bound on parallel executions"),
    ("timeout_seconds", "integer", "300", "Hard stop for a single execution"),
    ("retry_count", "integer", "2", "Automatic retries before surfacing an error"),
    ("notify_on_failure", "boolean", "true", "Sends an email to workspace admins on failure"),
]


def slug(text):
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")


def build_page(rng, idx, area_key, feature, kind, version):
    area = PRODUCT_AREAS[area_key]
    feature_title = feature.title()
    title = {
        "overview": f"{feature_title} overview",
        "how-to": f"How to configure {feature}",
        "reference": f"{feature_title} settings reference",
        "troubleshooting": f"Troubleshooting {feature}",
        "concepts": f"How {feature} works",
    }[kind]
    source_id = f"DOC-{idx:05d}"
    section_path = f"{area['label']} > {feature_title} > {title}"
    updated = datetime(2026, 6, 30) - timedelta(days=rng.randint(0, 900))
    acl = rng.choice(["public"] * 8 + PLAN_TIERS)

    lines = []
    intro = rng.choice(INTRO_TEMPLATES).format(
        feature=feature, feature_title=feature_title, product=PRODUCT_NAME,
        benefit=rng.choice(BENEFITS), version=version)
    lines += [f"# {title}", "", intro, ""]

    lines += ["## Configuration", ""]
    for t in rng.sample(BODY_TEMPLATES, k=5):
        lines.append(t.format(feature=feature, area_label=area["label"],
                              limit=rng.choice([5, 10, 25, 50, 100]),
                              tier=rng.choice(PLAN_TIERS)))
        lines.append("")

    if kind in ("reference", "how-to"):
        lines += ["## Settings", "",
                  "| Setting | Type | Default | Description |",
                  "| --- | --- | --- | --- |"]
        for row in rng.sample(SETTINGS_ROWS, k=rng.randint(3, 5)):
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")

    # Troubleshooting section wires docs to the error-code taxonomy,
    # which is what makes ticket -> docs retrieval labels possible.
    area_errors = [(c, e) for c, e in ERROR_CODES.items() if e[1] == area_key]
    related = rng.sample(area_errors, k=min(len(area_errors), rng.randint(1, 2))) \
        if area_errors else []
    if related:
        lines += ["## Common errors", ""]
        for code, (etitle, _a, cause, workaround, affects, fixed) in related:
            lines.append(f"### {code}: {etitle}")
            lines.append("")
            lines.append(f"Cause: {cause}.")
            lines.append("")
            lines.append(f"Resolution: {workaround}.")
            if fixed:
                lines.append("")
                lines.append(f"This issue is fixed in version {fixed}. "
                             f"Affected versions: {', '.join(affects)}.")
            lines.append("")

    frontmatter = {
        "source_id": source_id,
        "title": title,
        "doc_type": "product-docs",
        "section_path": section_path,
        "product_area": area_key,
        "product_version": version,
        "acl": acl,
        "updated_at": updated.strftime("%Y-%m-%d"),
        "related_error_codes": [c for c, _ in related],
    }
    fm = "---\n" + "\n".join(
        f"{k}: {json.dumps(v)}" for k, v in frontmatter.items()) + "\n---\n\n"
    return source_id, frontmatter, fm + "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=400)
    ap.add_argument("--out", default="../output/docs")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    manifest = []

    combos = [(a, f) for a, d in PRODUCT_AREAS.items() for f in d["features"]]
    for i in range(1, args.pages + 1):
        area_key, feature = combos[(i - 1) % len(combos)]
        kind = PAGE_KINDS[(i - 1) // len(combos) % len(PAGE_KINDS)]
        version = rng.choice(VERSIONS)
        source_id, meta, content = build_page(rng, i, area_key, feature, kind, version)
        (out / f"{source_id}-{slug(meta['title'])[:60]}.md").write_text(content)
        manifest.append(meta)

    (out / "_manifest.jsonl").write_text(
        "\n".join(json.dumps(m) for m in manifest))
    print(f"Wrote {len(manifest)} docs pages to {out}")


if __name__ == "__main__":
    main()
