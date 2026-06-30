#!/usr/bin/env python3
"""Copy lesson READMEs into site-docs/ for MkDocs (run before mkdocs build).

Usage (from repo root):
    python tools/sync-mkdocs-content.py
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SITE_DOCS = REPO / "site-docs"

GITHUB_REPO = "https://github.com/instaclustr/InstAcademy"
GITHUB_BRANCH = "main"
COURSE_GITHUB_PATH = (
    "OpenSearch/Optimizing OpenSearch Vector Storage and Search for Faster AI Applications"
)


def _github_blob(rel: str) -> str:
    return f"{GITHUB_REPO}/blob/{GITHUB_BRANCH}/{COURSE_GITHUB_PATH}/{rel}"


def _github_tree(rel: str) -> str:
    return f"{GITHUB_REPO}/tree/{GITHUB_BRANCH}/{COURSE_GITHUB_PATH}/{rel}"


DOCX_GITHUB_URL = _github_blob("OpenSearch%20Learning%20Path%201.docx")
BULK_GITHUB_URL = _github_tree("rest/bulk/")
BRUNO_GITHUB = _github_tree("bruno")

# (source path relative to repo, destination path under site-docs/)
PAGES: list[tuple[str, str]] = [
    ("docs/HANDS-ON-GUIDE.md", "index.md"),
    ("CREATE_CLUSTER.md", "getting-started/cluster-setup/index.md"),
    ("bruno/README.md", "fast-mode/bruno/index.md"),
    ("src/Chapter 1/README.md", "chapter-1/index.md"),
    ("src/Chapter 1/1-1/README.md", "chapter-1/lesson-1-1/index.md"),
    ("src/Chapter 1/1-2/README.md", "chapter-1/lesson-1-2/index.md"),
    ("src/Chapter 1/1-4/README.md", "chapter-1/lesson-1-4/index.md"),
    ("src/Chapter 2/README.md", "chapter-2/index.md"),
    ("src/Chapter 2/Lesson 1/README.md", "chapter-2/lesson-1/index.md"),
    ("src/Chapter 2/Lesson 2/README.md", "chapter-2/lesson-2/index.md"),
    ("src/Chapter 2/Lesson 4/README.md", "chapter-2/lesson-4/index.md"),
    ("src/Chapter 2/Lesson 5/README.md", "chapter-2/lesson-5/index.md"),
    ("src/Chapter 3/README.md", "chapter-3/index.md"),
    ("src/Chapter 3/Lesson 1/README.md", "chapter-3/lesson-1/index.md"),
    ("src/Chapter 4/README.md", "chapter-4/index.md"),
    ("src/Chapter 4/Lesson 1/README.md", "chapter-4/lesson-1/index.md"),
    ("src/Chapter 4/Lesson 2/README.md", "chapter-4/lesson-2/index.md"),
    ("src/Chapter 4/Lesson 3/README.md", "chapter-4/lesson-3/index.md"),
    ("src/Chapter 5/README.md", "chapter-5/index.md"),
    ("src/Chapter 5/Lesson 1/README.md", "chapter-5/lesson-1/index.md"),
    ("src/Chapter 5/Lesson 2/README.md", "chapter-5/lesson-2/index.md"),
    ("src/Chapter 5/Lesson 3/README.md", "chapter-5/lesson-3/index.md"),
    ("src/Chapter 5/Lesson 5/README.md", "chapter-5/lesson-5/index.md"),
]

# Rewrite GitHub-style README links → MkDocs site paths (order: longest first).
LINK_REWRITES: list[tuple[str, str]] = [
    (r"\]\(\.\./\.\./\.\./OpenSearch%20Learning%20Path%201\.docx\)", f"]({DOCX_GITHUB_URL})"),
    (r"\]\(\.\./\.\./OpenSearch%20Learning%20Path%201\.docx\)", f"]({DOCX_GITHUB_URL})"),
    (r"\]\(\.\./\.\./\.\./\.\./OpenSearch%20Learning%20Path%201\.docx\)", f"]({DOCX_GITHUB_URL})"),
    (r"\]\(\.\./CREATE_CLUSTER\.md\)", "](../getting-started/cluster-setup/)"),
    (r"\]\(\.\./\.\./CREATE_CLUSTER\.md\)", "](../../getting-started/cluster-setup/)"),
    (r"\]\(\.\./bruno/\)", "](../fast-mode/bruno/)"),
    (r"\]\(\.\./src/Chapter%201/1-1/README\.md\)", "](../chapter-1/lesson-1-1/)"),
    (r"\]\(\.\./src/Chapter%201/1-2/README\.md\)", "](../chapter-1/lesson-1-2/)"),
    (r"\]\(\.\./src/Chapter%201/1-4/README\.md\)", "](../chapter-1/lesson-1-4/)"),
    (r"\]\(\.\./src/Chapter%202/README\.md\)", "](../chapter-2/)"),
    (r"\]\(\.\./src/Chapter%203/README\.md\)", "](../chapter-3/)"),
    (r"\]\(\.\./src/Chapter%204/README\.md\)", "](../chapter-4/)"),
    (r"\]\(\.\./src/Chapter%205/README\.md\)", "](../chapter-5/)"),
    (r"\]\(\.\./\.\./CREATE_CLUSTER\.md\)", "](../../getting-started/cluster-setup/)"),
    (r"\]\(\.\./\.\./\.\./CREATE_CLUSTER\.md\)", "](../../getting-started/cluster-setup/)"),
    (r"\]\(\.\./\.\./\.\./\.\./CREATE_CLUSTER\.md\)", "](../../../getting-started/cluster-setup/)"),
    (r"\]\(\.\./\.\./docs/HANDS-ON-GUIDE\.md\)", "](../)"),
    (r"\]\(\.\./\.\./\.\./docs/HANDS-ON-GUIDE\.md\)", "](../../)"),
    (r"\]\(\.\./\.\./\.\./\.\./docs/HANDS-ON-GUIDE\.md\)", "](../../../)"),
    (r"\]\(\.\./\.\./docs/HANDS-ON-GUIDE\.md#how-to-read-a-lesson\)", "](../#how-to-read-a-lesson)"),
    (r"\]\(\.\./\.\./\.\./docs/HANDS-ON-GUIDE\.md#how-to-read-a-lesson\)", "](../../#how-to-read-a-lesson)"),
    (r"\]\(\.\./bruno/README\.md\)", "](../fast-mode/bruno/)"),
    (r"\]\(\.\./\.\./bruno/README\.md\)", "](../../fast-mode/bruno/)"),
    (r"\]\(\.\./\.\./\.\./bruno/README\.md\)", "](../../../fast-mode/bruno/)"),
    (r"\]\(\.\./\.\./\.\./\.\./bruno/README\.md\)", "](../../../../fast-mode/bruno/)"),
    (r"\]\(\.\./\.\./bruno/\)", "](../../fast-mode/bruno/)"),
    (r"\]\(\.\./\.\./\.\./bruno/\)", "](../../../fast-mode/bruno/)"),
    (r"\]\(\.\./\.\./\.\./\.\./bruno/\)", "](../../../../fast-mode/bruno/)"),
    (r"\]\(\.\./Chapter%201/1-1/README\.md\)", "](../chapter-1/lesson-1-1/)"),
    (r"\]\(\.\./Chapter%201/1-2/README\.md\)", "](../chapter-1/lesson-1-2/)"),
    (r"\]\(\.\./Chapter%201/1-4/README\.md\)", "](../chapter-1/lesson-1-4/)"),
    (r"\]\(\.\./Chapter%201/README\.md\)", "](../chapter-1/)"),
    (r"\]\(\.\./\.\./Chapter%201/1-1/README\.md\)", "](../../chapter-1/lesson-1-1/)"),
    (r"\]\(\.\./\.\./Chapter%201/1-2/README\.md\)", "](../../chapter-1/lesson-1-2/)"),
    (r"\]\(\.\./\.\./Chapter%201/1-4/README\.md\)", "](../../chapter-1/lesson-1-4/)"),
    (r"\]\(\.\./\.\./Chapter%201/README\.md\)", "](../../chapter-1/)"),
    (r"\]\(\.\./\.\./Chapter%202/README\.md\)", "](../../chapter-2/)"),
    (r"\]\(\.\./\.\./Chapter%203/README\.md\)", "](../../chapter-3/)"),
    (r"\]\(\.\./\.\./Chapter%204/README\.md\)", "](../../chapter-4/)"),
    (r"\]\(\.\./\.\./Chapter%205/README\.md\)", "](../../chapter-5/)"),
    (r"\]\(\.\./\.\./\.\./Chapter%201/README\.md\)", "](../../../chapter-1/)"),
    (r"\]\(\.\./\.\./\.\./Chapter%202/README\.md\)", "](../../../chapter-2/)"),
    (r"\]\(\.\./\.\./\.\./Chapter%203/README\.md\)", "](../../../chapter-3/)"),
    (r"\]\(\.\./\.\./\.\./Chapter%204/README\.md\)", "](../../../chapter-4/)"),
    (r"\]\(\.\./\.\./\.\./Chapter%205/README\.md\)", "](../../../chapter-5/)"),
    (r"\]\(\.\./Lesson%201/README\.md\)", "](lesson-1/)"),
    (r"\]\(\.\./Lesson%202/README\.md\)", "](lesson-2/)"),
    (r"\]\(\.\./Lesson%204/README\.md\)", "](lesson-4/)"),
    (r"\]\(\.\./Lesson%205/README\.md\)", "](lesson-5/)"),
    (r"\]\(\.\./1-1/README\.md\)", "](lesson-1-1/)"),
    (r"\]\(\.\./1-2/README\.md\)", "](lesson-1-2/)"),
    (r"\]\(\.\./1-4/README\.md\)", "](lesson-1-4/)"),
    (r"\]\(\.\./\.\./\.\./Chapter%202/Lesson%201/README\.md\)", "](../../../chapter-2/lesson-1/)"),
    (r"\]\(\.\./\.\./\.\./Chapter%204/Lesson%202/README\.md\)", "](../../../chapter-4/lesson-2/)"),
    (r"\]\(\.\./\.\./\.\./Chapter%204/Lesson%203/README\.md\)", "](../../../chapter-4/lesson-3/)"),
    (r"\]\(\.\./\.\./\.\./\.\./src/Chapter%201/1-1/README\.md\)", "](../../chapter-1/lesson-1-1/)"),
    (r"\]\(\.\./\.\./\.\./\.\./src/Chapter%201/1-2/README\.md\)", "](../../chapter-1/lesson-1-2/)"),
    (r"\]\(\.\./\.\./\.\./\.\./src/Chapter%201/1-4/README\.md\)", "](../../chapter-1/lesson-1-4/)"),
    (r"\]\(\.\./\.\./\.\./\.\./src/Chapter%202/README\.md\)", "](../../chapter-2/)"),
    (r"\]\(\.\./\.\./\.\./\.\./src/Chapter%203/README\.md\)", "](../../chapter-3/)"),
    (r"\]\(\.\./\.\./\.\./\.\./src/Chapter%204/README\.md\)", "](../../chapter-4/)"),
    (r"\]\(\.\./\.\./\.\./\.\./src/Chapter%205/README\.md\)", "](../../chapter-5/)"),
    (r"\]\(\.\./\.\./rest/bulk/", f"]({BULK_GITHUB_URL}"),
    (r"\]\(\.\./\.\./\.\./rest/bulk/", f"]({BULK_GITHUB_URL}"),
    (r"\]\(\.\./\.\./\.\./\.\./rest/bulk/", f"]({BULK_GITHUB_URL}"),
    (r"\]\(\.\./\.\./\.\./\.\./\.\./rest/bulk/", f"]({BULK_GITHUB_URL}"),
    (r"\]\(\.\./\.\./\.\./\.\./\.\./\.\./rest/bulk/", f"]({BULK_GITHUB_URL}"),
    (r"\]\(\.\./\.\./\.\./\.\./\.\./\.\./\.\./rest/bulk/", f"]({BULK_GITHUB_URL}"),
]

# Simple string replacements (applied after regex pass).
PLAIN_REPLACEMENTS: list[tuple[str, str]] = [
    ("](Lesson%201/README.md)", "](lesson-1/)"),
    ("](Lesson%202/README.md)", "](lesson-2/)"),
    ("](Lesson%203/README.md)", "](lesson-3/)"),
    ("](Lesson%204/README.md)", "](lesson-4/)"),
    ("](Lesson%205/README.md)", "](lesson-5/)"),
    ("](1-1/README.md)", "](lesson-1-1/)"),
    ("](1-2/README.md)", "](lesson-1-2/)"),
    ("](1-4/README.md)", "](lesson-1-4/)"),
    ("](../README.md#lesson-3-video-only)", "](../#lesson-3-video-only)"),
    ("](../README.md)", "](../)"),
    ("](../../Chapter%202/Lesson%201/README.md)", "](../../chapter-2/lesson-1/)"),
    ("](../../Chapter%204/Lesson%201/README.md)", "](../../chapter-4/lesson-1/)"),
    ("](../../Chapter%204/Lesson%202/README.md)", "](../../chapter-4/lesson-2/)"),
    ("](../../Chapter%205/Lesson%201/README.md)", "](../../chapter-5/lesson-1/)"),
    ("](../Chapter%202/Lesson%201/README.md)", "](../chapter-2/lesson-1/)"),
    ("](../Chapter%204/Lesson%202/README.md)", "](../chapter-4/lesson-2/)"),
    ("](../Chapter%203/README.md)", "](../chapter-3/)"),
    ("](../Chapter%204/README.md)", "](../chapter-4/)"),
    ("](../Chapter%205/README.md)", "](../chapter-5/)"),
    ("](../Lesson%203/README.md)", "](lesson-3/)"),
    ("](../docs/HANDS-ON-GUIDE.md)", "](../../)"),
    ("](../rest/bulk/", f"]({BULK_GITHUB_URL}"),
]


def rewrite_links(text: str, *, dest_rel: str) -> str:
    for pattern, replacement in LINK_REWRITES:
        text = re.sub(pattern, replacement, text)
    for old, new in PLAIN_REPLACEMENTS:
        text = text.replace(old, new)
    # Bruno collection lives in the repo, not the static site — link to GitHub.
    text = re.sub(
        r"\]\(\.\./(\.\./)*(bruno/[^)]+)\)",
        lambda m: f"]({BRUNO_GITHUB}/{m.group(2).replace('%20', ' ')})",
        text,
    )
    if dest_rel == "index.md":
        text = text.replace("](../getting-started/", "](getting-started/")
        text = text.replace("](../chapter-", "](chapter-")
        text = text.replace("](../fast-mode/", "](fast-mode/")
        text = text.replace(
            "](../OpenSearch%20Learning%20Path%201.docx)",
            f"]({DOCX_GITHUB_URL})",
        )
        text = text.replace(
            "](../rest/bulk/",
            f"]({BULK_GITHUB_URL}",
        )
    if "cluster-setup" in dest_rel:
        text = text.replace("](./img/", "](../../assets/img/")
        text = text.replace("](img/", "](../../assets/img/")
    return text


def sync() -> None:
    if SITE_DOCS.exists():
        shutil.rmtree(SITE_DOCS)
    SITE_DOCS.mkdir()

    assets_img = SITE_DOCS / "assets" / "img"
    shutil.copytree(REPO / "img", assets_img)

    styles_src = REPO / "docs" / "stylesheets"
    if styles_src.is_dir():
        shutil.copytree(styles_src, SITE_DOCS / "stylesheets")

    for src_rel, dest_rel in PAGES:
        src = REPO / src_rel
        dest = SITE_DOCS / dest_rel
        if not src.is_file():
            raise FileNotFoundError(f"Missing source for MkDocs sync: {src}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        content = rewrite_links(src.read_text(encoding="utf-8"), dest_rel=dest_rel)
        dest.write_text(content, encoding="utf-8")
        print(f"  {src_rel} → {dest_rel}")

    print(f"\nSynced {len(PAGES)} pages to {SITE_DOCS.relative_to(REPO)}/")


if __name__ == "__main__":
    sync()
