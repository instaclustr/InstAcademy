"""
Generate support ticket history as JSONL. Tickets reference the same error
codes, versions, and integrations as the docs, so resolutions can point at
real DOC and GUIDE source_ids. Those links become free ground-truth labels
for the golden query set.

Usage:
    python generate_tickets.py --count 5000 --out ../output/tickets.jsonl \
        --docs-manifest ../output/docs/_manifest.jsonl \
        --guides-manifest ../output/integration_guides/_manifest.jsonl
"""
import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

from taxonomy import (ERROR_CODES, PRODUCT_AREAS, INTEGRATIONS, VERSIONS,
                      PLAN_TIERS, FIRST_NAMES, tenant_id)

SUBJECT_TEMPLATES = {
    "error": [
        "{code} when {doing}",
        "Getting {code} on every attempt",
        "Urgent: {etitle_lower} blocking our team",
        "{etitle} keeps happening since we upgraded to {version}",
    ],
    "howto": [
        "How do we set up {feature}?",
        "Question about {feature}",
        "Best way to configure {feature} for {n} users?",
        "Can {feature} work with {integration}?",
    ],
    "symptom": [
        "{symptom}",
        "{symptom}, started this morning",
        "{symptom} for one of our workspaces",
    ],
}

DOINGS = {
    "dashboards": ["loading our exec dashboard", "exporting a dashboard to PDF",
                   "opening a shared dashboard on mobile"],
    "connectors": ["connecting to {integration}", "testing a new {integration} connection",
                   "rotating {integration} credentials"],
    "datasets": ["running the nightly refresh", "adding a calculated field",
                 "enabling incremental refresh"],
    "alerts": ["sending threshold alerts to Slack", "delivering scheduled reports"],
    "sql-workbench": ["running a long query in the workbench"],
    "api": ["calling the REST API from our backend", "embedding a dashboard"],
    "admin": ["provisioning users through SCIM", "logging in with SSO"],
}

SYMPTOMS = {
    "dashboards": ["Dashboard takes forever to load", "Charts render blank",
                   "Cross filters stopped working"],
    "connectors": ["Snowflake connection keeps dropping",
                   "Schema list never finishes loading"],
    "datasets": ["Nightly refresh has been stuck for hours",
                 "Users can see rows they should not see"],
    "alerts": ["Alert emails arriving hours late", "Webhooks silently failing"],
    "sql-workbench": ["Queries dying around the five minute mark"],
    "api": ["Embedded dashboards showing an expired link error",
            "API calls suddenly returning 429s"],
    "admin": ["New hires not appearing after SCIM sync", "SSO login loop"],
}

BODY_OPENERS = [
    "Hi team,", "Hello,", "Hi support,", "Hey,",
]
FRUSTRATION = [
    "This is blocking our month-end reporting.",
    "Our analysts have been unable to work since this started.",
    "We have a board meeting tomorrow and need this fixed.",
    "Low priority, but wanted to flag it.",
    "This has happened three times this week.",
]


def make_ticket(rng, n, doc_lookup, guide_lookup):
    created = datetime(2023, 7, 1) + timedelta(
        minutes=rng.randint(0, 3 * 365 * 24 * 60))
    kind = rng.choices(["error", "howto", "symptom"], weights=[45, 35, 20])[0]
    area = rng.choice(list(PRODUCT_AREAS))
    version = rng.choice(VERSIONS)
    integration = rng.choice(INTEGRATIONS)[0]
    name = rng.choice(FIRST_NAMES)
    relevant = []

    if kind == "error":
        code = rng.choice(list(ERROR_CODES))
        etitle, area, cause, workaround, affects, fixed = ERROR_CODES[code]
        doing = rng.choice(DOINGS[area]).format(integration=integration)
        subject = rng.choice(SUBJECT_TEMPLATES["error"]).format(
            code=code, etitle=etitle, etitle_lower=etitle.lower(),
            doing=doing, version=version)
        body = (f"{rng.choice(BODY_OPENERS)}\n\nWe are seeing {code} while "
                f"{doing}. We are on version {version}. "
                f"{rng.choice(FRUSTRATION)}\n\nThanks,\n{name}")
        resolution = (f"Identified as {code} ({etitle}). {workaround}."
                      + (f" Customer upgraded to {fixed} where this is fixed."
                         if fixed else ""))
        relevant = doc_lookup.get(code, []) + guide_lookup.get(code, [])
    elif kind == "howto":
        feature = rng.choice(PRODUCT_AREAS[area]["features"])
        subject = rng.choice(SUBJECT_TEMPLATES["howto"]).format(
            feature=feature, integration=integration,
            n=rng.choice([25, 50, 200, 500]))
        body = (f"{rng.choice(BODY_OPENERS)}\n\nWe want to roll out {feature} "
                f"across the org and could not find the exact steps in the "
                f"docs. Could you point us in the right direction?\n\n"
                f"Thanks,\n{name}")
        resolution = (f"Shared the {feature} documentation and walked through "
                      f"configuration on a call.")
        relevant = doc_lookup.get(("feature", feature), [])
        code = None
    else:
        symptom = rng.choice(SYMPTOMS[area])
        subject = rng.choice(SUBJECT_TEMPLATES["symptom"]).format(symptom=symptom)
        body = (f"{rng.choice(BODY_OPENERS)}\n\n{symptom}. Nothing changed on "
                f"our side as far as we know. We are on version {version}. "
                f"{rng.choice(FRUSTRATION)}\n\n{name}")
        area_codes = [c for c, e in ERROR_CODES.items() if e[1] == area]
        code = rng.choice(area_codes) if area_codes and rng.random() < 0.7 else None
        if code:
            etitle, _a, cause, workaround, _af, _fx = ERROR_CODES[code]
            resolution = (f"Root cause matched known issue {code}: {cause}. "
                          f"{workaround}.")
            relevant = doc_lookup.get(code, [])
        else:
            resolution = "Resolved after clarifying configuration with the customer."

    status = rng.choices(["resolved", "closed", "open"], weights=[70, 25, 5])[0]
    return {
        "ticket_id": f"TKT-{created.year}-{n:06d}",
        "created_at": created.isoformat(timespec="seconds"),
        "status": status,
        "subject": subject,
        "body": body,
        "product_area": area,
        "product_version": version,
        "error_code": code,
        "plan_tier": rng.choice(PLAN_TIERS),
        "tenant_id": tenant_id(rng),
        "resolution": resolution if status != "open" else None,
        "relevant_source_ids": sorted(set(relevant))[:4],
        "doc_type": "support-ticket",
    }


def load_lookup(manifest_path, feature_key=False):
    """Map error codes (and features) to source_ids from a manifest."""
    lookup = {}
    p = Path(manifest_path)
    if not p.exists():
        return lookup
    for line in p.read_text().splitlines():
        m = json.loads(line)
        for code in m.get("related_error_codes", []):
            lookup.setdefault(code, []).append(m["source_id"])
        if feature_key and m.get("doc_type") == "product-docs":
            # crude feature key: section_path middle element lowered
            parts = m["section_path"].split(" > ")
            if len(parts) >= 2:
                lookup.setdefault(("feature", parts[1].lower()), []).append(
                    m["source_id"])
    return lookup


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=5000)
    ap.add_argument("--out", default="../output/tickets.jsonl")
    ap.add_argument("--docs-manifest", default="../output/docs/_manifest.jsonl")
    ap.add_argument("--guides-manifest",
                    default="../output/integration_guides/_manifest.jsonl")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    doc_lookup = load_lookup(args.docs_manifest, feature_key=True)
    guide_lookup = load_lookup(args.guides_manifest)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for n in range(1, args.count + 1):
            f.write(json.dumps(make_ticket(rng, n, doc_lookup, guide_lookup)) + "\n")
    print(f"Wrote {args.count} tickets to {out}")


if __name__ == "__main__":
    main()
