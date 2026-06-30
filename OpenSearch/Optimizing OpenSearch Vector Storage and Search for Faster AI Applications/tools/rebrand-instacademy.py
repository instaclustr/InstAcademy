#!/usr/bin/env python3
"""Apply InstAcademy course branding to markdown and config files.

Run from repo root: python tools/rebrand-instacademy.py
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

COURSE_TITLE = (
    "Optimizing OpenSearch Vector Storage and Search for Faster AI Applications"
)
BREADCRUMB_LABEL = "**InstAcademy → OpenSearch:**"
OLD_LINK_TEXT = "OpenSearch Learning Path 1"
NEW_LINK_TEXT = COURSE_TITLE

GLOBS = [
    REPO / "README.md",
    REPO / "mkdocs.yml",
    REPO / "bruno" / "bruno.json",
    REPO / "bruno" / "README.md",
    REPO / "docs" / "HANDS-ON-GUIDE.md",
    REPO / "docs" / "PUBLISHING.md",
    REPO / "CREATE_CLUSTER.md",
    REPO / "tools" / "generate-bruno-requests.py",
    REPO / "tools" / "sync-mkdocs-content.py",
    *REPO.glob("src/**/README.md"),
]


def rebrand_text(text: str) -> str:
    text = text.replace("**Course alignment:**", BREADCRUMB_LABEL)
    text = text.replace(f"[{OLD_LINK_TEXT}]", f"[{NEW_LINK_TEXT}]")
    text = text.replace(
        "OpenSearch Learning Path 1 — Hands-on Labs",
        f"InstAcademy · OpenSearch — {COURSE_TITLE}",
    )
    text = text.replace('"name": "OpenSearch Learning Path 1"', f'"name": "InstAcademy · OpenSearch"')
    text = text.replace(
        "Generate Bruno .bru request files for OpenSearch Learning Path 1.",
        f"Generate Bruno .bru request files for InstAcademy OpenSearch course.",
    )
    # Lesson / chapter line: "Lesson 2-1 in [" → "Lesson 2-1 · ["
    text = re.sub(
        r"((?:Lesson|Lessons|Chapter)[^\n]*?) in \[",
        r"\1 · [",
        text,
    )
    # Intro paragraphs
    text = text.replace(
        "Hands-on labs for the **OpenSearch Learning Path 1** video course.",
        f"Hands-on labs for **InstAcademy → OpenSearch → {COURSE_TITLE}**.",
    )
    text = text.replace(
        "The voice script is [`OpenSearch Learning Path 1.docx`]",
        f"The voice script is [`{COURSE_TITLE} (script).docx`]",
    )
    text = text.replace(
        "The voice script is [OpenSearch Learning Path 1.docx]",
        f"The voice script is [{COURSE_TITLE} (script).docx]",
    )
    text = re.sub(
        r"\*\*Optimizing OpenSearch vector storage and search for faster AI applications\*\* \(Learning Path 1\)",
        f"**{COURSE_TITLE}**",
        text,
        flags=re.IGNORECASE,
    )
    text = text.replace(
        "(Learning Path 1). The voice script",
        ". The voice script",
    )
    text = text.replace(
        "site_description: Dev Tools lab guide for Optimizing OpenSearch vector storage and search for faster AI applications",
        f"site_description: InstAcademy OpenSearch hands-on labs — {COURSE_TITLE}",
    )
    if "# Creating a NetApp Instaclustr Cluster for this Course" in text:
        text = text.replace(
            "# Creating a NetApp Instaclustr Cluster for this Course",
            f"# Creating a NetApp Instaclustr Cluster\n\n**InstAcademy → OpenSearch → {COURSE_TITLE}**",
        )
    return text


def main() -> None:
    updated = 0
    for path in GLOBS:
        if not path.is_file():
            continue
        original = path.read_text(encoding="utf-8")
        new = rebrand_text(original)
        if new != original:
            path.write_text(new, encoding="utf-8")
            print(f"Updated {path.relative_to(REPO)}")
            updated += 1
    print(f"\nRebranded {updated} files.")


if __name__ == "__main__":
    main()
