#!/usr/bin/env python3
"""Normalize lesson README markdown for readability.

Run from repo root: python tools/format-lesson-markdown.py
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TARGETS = list((REPO / "src").rglob("README.md")) + [REPO / "HANDS-ON-GUIDE.md"]


def format_content(text: str) -> str:
    # InstAcademy breadcrumb (formerly "Course alignment")
    text = re.sub(
        r"^> \*\*Course alignment:\*\*",
        "**InstAcademy → OpenSearch:**",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^\*\*Course alignment\*\* ",
        "**InstAcademy → OpenSearch:** ",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^\*\*Course alignment:\*\*",
        "**InstAcademy → OpenSearch:**",
        text,
        flags=re.MULTILINE,
    )

    # Step headings: ## Step 3 — Title  ->  ### **Step 3: Title**
    text = re.sub(
        r"^## Step (\d+) — (.+)$",
        r"### **Step \1: \2**",
        text,
        flags=re.MULTILINE,
    )

    # Sub-step under polling (### Poll the ...) -> bold label style
    text = re.sub(
        r"^### (Poll .+)$",
        r"#### **\1**",
        text,
        flags=re.MULTILINE,
    )

    # Insert "Lab steps" section before first step if missing
    if "### **Step 1:" in text and "## Lab steps" not in text:
        text = re.sub(
            r"(\n)(### \*\*Step 1:)",
            r"\1## Lab steps\n\n\2",
            text,
            count=1,
        )

    # Standard labels (drop trailing colons for cleaner scan)
    replacements = [
        (r"\*\*Why:\*\*", "**Why**"),
        (r"\*\*Expected response \(shape\):\*\*", "**Expected**"),
        (r"\*\*Expected \(shape\):\*\*", "**Expected**"),
        (r"\*\*Expected \(immediate response — shape\):\*\*", "**Expected**"),
        (r"\*\*Expected when finished successfully:\*\*", "**Expected**"),
        (r"\*\*Expected when deploy succeeds:\*\*", "**Expected**"),
        (r"\*\*Expected:\*\*", "**Expected**"),
        (r"\*\*Save this value:\*\*", "**Save**"),
        (r"\*\*What happens:\*\*", "**Why**"),
    ]
    for old, new in replacements:
        text = re.sub(old, new, text)

    # Why / Save / Expected: content on next line when inline
    text = re.sub(
        r"^\*\*Why\*\* ([^\n]+)$",
        r"**Why**  \n\1",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^\*\*Save\*\* ([^\n]+)$",
        r"**Save**  \n\1",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^\*\*Expected\*\* ([^\n`]+)$",
        r"**Expected**  \n\1",
        text,
        flags=re.MULTILINE,
    )

    # Fast mode: plain label, not blockquote
    text = re.sub(
        r"^> \*\*Fast mode:\*\* (.+)$",
        r"**Fast mode**  \n\1",
        text,
        flags=re.MULTILINE,
    )

    # Remove horizontal rules between steps (visual noise)
    text = re.sub(r"\n---\n\n(### \*\*Step )", r"\n\n\1", text)
    text = re.sub(r"\n---\n\n(#### \*\*Poll )", r"\n\n\1", text)

    # Add "Request" label before http blocks missing one
    def ensure_request_label(match: re.Match[str]) -> str:
        block = match.group(0)
        start = match.start()
        prefix = text[max(0, start - 200) : start]
        if "**Request**" in prefix:
            return block
        return "\n**Request** — paste into Dev Tools:\n\n" + block

    text = re.sub(r"\n(```http\n)", ensure_request_label, text)

    # What you'll accomplish -> Overview subsection
    text = text.replace("## What you'll accomplish", "## Overview\n\n### Goals")
    text = text.replace("## Before you start", "### Prerequisites")

    # Optional Python reference table -> simpler heading
    text = text.replace("## Optional Python reference", "## Reference scripts")

    # Collapse 3+ blank lines
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    return text.rstrip() + "\n"


def main() -> None:
    for path in TARGETS:
        if not path.is_file():
            continue
        original = path.read_text(encoding="utf-8")
        updated = format_content(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"Updated {path.relative_to(REPO)}")
        else:
            print(f"No change {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
