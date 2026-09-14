#!/usr/bin/env python3
"""
Resolve every relative Markdown link in the repo and report the ones that miss.

Checks BOTH halves of a link:
  - the file path resolves on disk
  - any #fragment matches a heading in the target file

The second half matters more than it looks. GitHub derives a heading's anchor
from its text, so editing a heading — including adding a leading emoji, which
shifts the slug — silently breaks every link pointing at it.

    python3 _migration/check_links.py

Exit status is the number of broken links, so this drops straight into CI.
"""

import os
import posixpath
import re
import subprocess
import sys
import urllib.parse

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(
    ["git", "-C", _HERE, "rev-parse", "--show-toplevel"],
    capture_output=True, text=True, check=True,
).stdout.strip()
MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^#{1,6}\s+(.*)$", re.M)
# GitHub-flavoured Markdown allows raw HTML, and the badge blocks use <img>.
HTML_SRC = re.compile(r"<img\b[^>]*?\bsrc=[\"']([^\"']+)[\"']", re.I)


def slug(text):
    """Approximate GitHub's heading slugger: strip inline markup, lowercase,
    keep alphanumerics/hyphen/underscore, spaces become hyphens."""
    s = text.strip()
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"\*\*([^*]*)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]*)\*", r"\1", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    return "".join(c for c in s.lower() if c.isalnum() or c in "-_ ").replace(" ", "-")


def main():
    files = [
        f for f in subprocess.run(
            ["git", "-C", REPO, "ls-files", "*.md"],
            capture_output=True, text=True, check=True,
        ).stdout.splitlines() if f
    ]

    anchors = {}
    for path in files:
        full = os.path.join(REPO, path)
        if os.path.isfile(full):
            with open(full, encoding="utf-8") as fh:
                anchors[path] = {slug(h) for h in HEADING.findall(fh.read())}

    broken, checked = [], 0

    for path in files:
        full = os.path.join(REPO, path)
        if not os.path.isfile(full):
            continue
        with open(full, encoding="utf-8") as fh:
            text = fh.read()

        for target in MD_LINK.findall(text) + HTML_SRC.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "<")):
                continue
            if target.startswith("#"):
                frag, rel = target[1:], path
            else:
                clean, _, frag = target.partition("#")
                if not clean:
                    continue
                rel = posixpath.normpath(
                    posixpath.join(posixpath.dirname(path), urllib.parse.unquote(clean))
                )
                checked += 1
                if not os.path.exists(os.path.join(REPO, rel)):
                    broken.append((path, target, f"no such path: {rel}"))
                    continue
                if not frag:
                    continue
            checked += 1
            if rel not in anchors:
                broken.append((path, target, "anchor target is not a tracked .md file"))
            elif urllib.parse.unquote(frag) not in anchors[rel]:
                broken.append((path, target, f"no heading in {rel} yields #{frag}"))

    for src, target, why in broken:
        print(f"BROKEN  {src}\n          link: {target}\n          {why}")

    print(f"\n{checked} links checked ({len(anchors)} files), {len(broken)} broken")
    return len(broken)


if __name__ == "__main__":
    sys.exit(min(main(), 125))
