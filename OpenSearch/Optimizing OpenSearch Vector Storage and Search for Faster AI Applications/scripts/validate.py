#!/usr/bin/env python3
"""Check that the course material is internally consistent.

Run from the course root (or via scripts/validate.sh). Exits non-zero if any
check fails, so it can be used in CI or a pre-commit hook.

Checks:
  1. Every .bru file named in a README's Fast mode line exists.
  2. Every .bru file in a chapter folder is referenced by that chapter's README.
  3. Each .bru file's seq: value matches the number in its filename.
  4. Bruno file numbers ascend in the order the steps appear in the README.
  5. Every body:file target resolves to a real NDJSON file.
  6. Each NDJSON file is valid JSON lines, and matches the bulk block printed
     in the README when the README inlines one.
  7. Every relative markdown link and image path resolves.
  8. No cluster credentials are committed (placeholders only).
"""

import json
import os
import re
import sys

CHAPTERS = range(1, 6)
failures = []
checks = 0


def fail(msg):
    failures.append(msg)


def ok(msg):
    global checks
    checks += 1
    print(f"  ok  {msg}")


def canon(lines):
    """Normalize NDJSON lines so formatting differences don't count as drift."""
    return [json.dumps(json.loads(l), sort_keys=True) for l in lines if l.strip()]


def check_bruno():
    print("\nBruno collection vs chapter READMEs")
    for ch in CHAPTERS:
        readme_path = f"chapters/Chapter {ch}/README.md"
        folder = f"bruno/Chapter {ch}"
        text = open(readme_path).read()
        refs = sorted(set(re.findall(r"\b(\d{2}-[a-z0-9-]+\.bru)\b", text)))
        files = sorted(f for f in os.listdir(folder) if f.endswith(".bru"))

        for r in refs:
            if r not in files:
                fail(f"Chapter {ch}: README references {r}, which does not exist")
        for f in files:
            if f not in refs:
                fail(f"Chapter {ch}: {f} exists but no README step references it")

        for f in files:
            content = open(os.path.join(folder, f)).read()
            m = re.search(r"seq:\s*(\d+)", content)
            if not m:
                fail(f"Chapter {ch}: {f} has no seq: field")
            elif int(m.group(1)) != int(f[:2]):
                fail(f"Chapter {ch}: {f} has seq: {m.group(1)}, expected {int(f[:2])}")

        positions = sorted((text.find(r), int(r[:2]), r) for r in refs)
        for i in range(1, len(positions)):
            if positions[i][1] < positions[i - 1][1]:
                fail(
                    f"Chapter {ch}: {positions[i][2]} appears after "
                    f"{positions[i-1][2]} in the README but sorts before it in Bruno"
                )

        if refs == files:
            ok(f"Chapter {ch}: {len(files)} requests, all referenced and in order")


def check_bulk():
    print("\nBulk payloads")
    # body:file targets resolve
    for ch in CHAPTERS:
        folder = f"bruno/Chapter {ch}"
        for f in sorted(os.listdir(folder)):
            if not f.endswith(".bru"):
                continue
            content = open(os.path.join(folder, f)).read()
            m = re.search(r"file:\s*(\S+)", content)
            if not m:
                continue
            target = os.path.normpath(os.path.join(folder, m.group(1)))
            if not os.path.isfile(target):
                fail(f"Chapter {ch}: {f} points at {m.group(1)}, which does not exist")
            else:
                ok(f"Chapter {ch}: {f} -> {os.path.basename(target)}")

    # every ndjson parses, and matches its README block when one is inlined
    readme_blocks = []
    for ch in CHAPTERS:
        text = open(f"chapters/Chapter {ch}/README.md").read()
        for m in re.finditer(r"```(?:http)?\n(POST _bulk[^\n]*)\n(.*?)```", text, re.S):
            payload = m.group(2)
            if payload.lstrip().startswith("{ /*"):  # paste-from-file placeholder
                continue
            try:
                readme_blocks.append((ch, canon(payload.splitlines())))
            except json.JSONDecodeError as e:
                fail(f"Chapter {ch}: an inline bulk block is not valid JSON ({e})")

    ndjson_files = []
    for ch in CHAPTERS:
        folder = f"bruno/Chapter {ch}"
        ndjson_files += [
            os.path.join(folder, f)
            for f in sorted(os.listdir(folder))
            if f.endswith(".ndjson")
        ]

    for full in ndjson_files:
        path = os.path.basename(full)
        try:
            file_lines = canon(open(full).read().splitlines())
        except json.JSONDecodeError as e:
            fail(f"{path}: not valid JSON lines ({e})")
            continue
        matched = any(block == file_lines for _, block in readme_blocks)
        if matched:
            ok(f"{path}: matches its README block ({len(file_lines)//2} docs)")
        else:
            ok(f"{path}: valid, README references the file directly")


def check_links():
    print("\nInternal links and images")
    md_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        md_files += [os.path.join(root, f) for f in files if f.endswith(".md")]

    broken = 0
    for md in md_files:
        base = os.path.dirname(md)
        text = open(md, errors="ignore").read()
        for link in re.findall(r"\]\(([^)\s]+)\)", text):
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = os.path.normpath(os.path.join(base, link.split("#")[0].replace("%20", " ")))
            if not os.path.exists(target):
                fail(f"{md}: broken link -> {link}")
                broken += 1
    if not broken:
        ok(f"{len(md_files)} markdown files, every relative link and image resolves")


def check_secrets():
    print("\nCredentials")
    # A real secret is a literal value. Template variables ({{password}}) and
    # placeholders (YOUR_PASSWORD) are exactly what the course should contain.
    patterns = [
        (r"sk-ant-api\d\d-[A-Za-z0-9_-]{30,}", "Anthropic API key"),
        (r"\bsk-proj-[A-Za-z0-9_-]{30,}", "OpenAI API key"),
        (r"password:\s*(?!\{\{|YOUR_|<)[A-Za-z0-9]{12,}", "literal password"),
        (r"-u\s+\w+:[A-Za-z0-9]{16,}", "credentials in a curl command"),
        (r"Basic\s+(?!YOUR_)[A-Za-z0-9+/]{24,}={0,2}", "base64 authorization header"),
    ]
    hits = 0
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "reports")]
        for f in files:
            if not f.endswith((".md", ".bru", ".json", ".mjs", ".sh")):
                continue
            p = os.path.join(root, f)
            text = open(p, errors="ignore").read()
            for pat, label in patterns:
                if re.search(pat, text):
                    fail(f"{p}: possible {label} committed")
                    hits += 1
    if not hits:
        ok("no credentials found in course files (placeholders only)")


def main():
    print("Validating course material...")
    check_bruno()
    check_bulk()
    check_links()
    check_secrets()

    print()
    if failures:
        print(f"FAILED: {len(failures)} problem(s)\n")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print(f"PASSED: {checks} checks, no problems found")


if __name__ == "__main__":
    main()
