"""
Generate the known issues and workarounds database as JSONL, one record per
error code in the taxonomy. This is the asset the support tool checks in Chapter 3
when grading whether retrieved context matches the customer's version.

Usage:
    python generate_known_issues.py --out ../output/known_issues.jsonl
"""
import argparse
import json
from datetime import datetime
from pathlib import Path

from taxonomy import ERROR_CODES, PRODUCT_AREAS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="../output/known_issues.jsonl")
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for i, (code, (title, area, cause, workaround, affects, fixed)) in enumerate(
            sorted(ERROR_CODES.items()), 1):
        records.append({
            "source_id": f"KI-{i:04d}",
            "doc_type": "known-issue",
            "error_code": code,
            "title": title,
            "product_area": area,
            "product_area_label": PRODUCT_AREAS[area]["label"],
            "symptom": f"Users encounter {code} ({title.lower()}).",
            "root_cause": cause,
            "workaround": workaround,
            "affected_versions": affects,
            "fixed_in_version": fixed,
            "status": "fixed" if fixed else "open",
            "acl": "public",
            "updated_at": datetime(2026, 6, 30).strftime("%Y-%m-%d"),
        })
    out.write_text("\n".join(json.dumps(r) for r in records))
    print(f"Wrote {len(records)} known issues to {out}")


if __name__ == "__main__":
    main()
