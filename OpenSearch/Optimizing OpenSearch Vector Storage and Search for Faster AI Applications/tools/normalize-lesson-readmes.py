#!/usr/bin/env python3
"""Normalize lesson README headers, links, and cluster-setup paths."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LESSON_GLOB = "src/Chapter */Lesson */README.md"

CREATE_CLUSTER_REL = "../../../CREATE_CLUSTER.md"
SCRIPT_REL = "../../../voice-script.docx"
GITHUB_CLUSTER = re.compile(
    r"https://github\.com/instaclustr/InstAcademy/blob/main/OpenSearch/Optimizing%20OpenSearch%20Vector%20Storage%20and%20Search%20for%20Faster%20AI%20Applications/CREATE_CLUSTER\.md"
)
GITHUB_SCRIPT = re.compile(
    r"https://github\.com/instaclustr/InstAcademy/blob/main/OpenSearch/Optimizing%20OpenSearch%20Vector%20Storage%20and%20Search%20for%20Faster%20AI%20Applications/OpenSearch%20Learning%20Path%201\.docx"
)
OLD_SCRIPT_REL = re.compile(
    r"\]\(\.\./\.\./\.\./OpenSearch%20Learning%20Path%201\.docx\)"
)


def chapter_lesson(path: Path) -> tuple[int, int]:
    ch = le = 0
    for part in path.parts:
        if part.startswith("Chapter "):
            ch = int(part.split()[1])
        if part.startswith("Lesson "):
            le = int(part.split()[1])
    if not ch or not le:
        raise ValueError(f"Could not parse chapter/lesson from {path}")
    return ch, le


def lesson_subline(ch: int, le: int, description: str) -> str:
    if ch == 3 and le == 1:
        return (
            f"**Chapter 3 · Lesson 1** (one lab — video scripts **3-1**, **3-2**, **3-3**) · "
            f"[Voice script]({SCRIPT_REL}) — {description}"
        )
    return f"**Chapter {ch} · Lesson {le}** · [Voice script]({SCRIPT_REL}) — {description}"


def nav_line(ch: int) -> str:
    return (
        f"← [Chapter {ch} overview](../README.md) · "
        f"[How to run labs](../../../docs/HANDS-ON-GUIDE.md)"
    )


def normalize(path: Path) -> bool:
    ch, le = chapter_lesson(path)
    text = path.read_text(encoding="utf-8")
    original = text

    # Extract description from existing InstAcademy line (after em dash).
    desc_match = re.search(
        r"\*\*InstAcademy → OpenSearch:\*\*[^\n]+—\s*(.+)",
        text,
    )
    description = desc_match.group(1).strip() if desc_match else ""

    # Replace InstAcademy breadcrumb line + insert compact nav.
    text = re.sub(
        r"\*\*InstAcademy → OpenSearch:\*\*[^\n]+\n",
        lesson_subline(ch, le, description) + "\n\n" + nav_line(ch) + "\n",
        text,
        count=1,
    )

    text = GITHUB_CLUSTER.sub(CREATE_CLUSTER_REL, text)
    text = text.replace(
        f"]({CREATE_CLUSTER_REL})",
        f"]({CREATE_CLUSTER_REL})",
    )
    text = GITHUB_SCRIPT.sub(SCRIPT_REL, text)
    text = OLD_SCRIPT_REL.sub(f"]({SCRIPT_REL})", text)

    # Fix duplicate Why in Chapter 1 Lesson 1 Step 1.
    if ch == 1 and le == 1:
        text = text.replace(
            "**Why**  \nEvery later lesson assumes basic auth and TLS work. A five-second smoke test saves hours of debugging bulk or ML errors.\n\n**Why**  \n`GET /` returns cluster name, version, and tag line.",
            "**Why**  \nEvery later lesson assumes basic auth and TLS work. `GET /` returns cluster name, version, and tag line — a five-second smoke test saves hours of debugging bulk or ML errors later.",
        )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(REPO.glob(LESSON_GLOB)):
        if normalize(path):
            changed += 1
            print(f"  {path.relative_to(REPO)}")
    print(f"Updated {changed} lesson READMEs")


if __name__ == "__main__":
    main()
