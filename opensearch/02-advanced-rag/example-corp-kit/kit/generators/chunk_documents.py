"""
Chunk the generated corpus using the strategies taught in lesson 1.3:

  product docs + integration guides + API reference -> heading-based
      parent-child (parent = H2 section, children = paragraph groups)
  tickets and known issues -> field-based structured chunks (no splitting)

Output is one chunks.jsonl ready for the ingest script. Chunk IDs are
stable and idempotent: {source_id}#{section_index}.{child_index}, which is
exactly the property lesson 1.4 requires for safe re-ingestion.

Usage:
    python chunk_documents.py --output-dir ../output
"""
import argparse
import json
import re
from pathlib import Path

MAX_CHILD_TOKENS = 60   # approx whitespace tokens; small children, parents carry context
MIN_CHILD_TOKENS = 20


def approx_tokens(text):
    return len(text.split())


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n\n?", text, re.S)
    meta = {}
    body = text
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(": ")
            try:
                meta[k] = json.loads(v)
            except json.JSONDecodeError:
                meta[k] = v
        body = text[m.end():]
    return meta, body


def split_sections(body):
    """Split markdown on H2 headings. Returns [(heading, text), ...]."""
    parts = re.split(r"^## ", body, flags=re.M)
    sections = []
    lead = parts[0].strip()
    title_match = re.match(r"^# (.+)$", lead, re.M)
    title = title_match.group(1) if title_match else "Introduction"
    lead_body = re.sub(r"^# .+$", "", lead, flags=re.M).strip()
    if lead_body:
        sections.append((title, lead_body))
    for part in parts[1:]:
        heading, _, text = part.partition("\n")
        sections.append((heading.strip(), text.strip()))
    return sections


def group_paragraphs(text):
    """Greedy sentence-aware grouping under the child token budget."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    children, current = [], []
    count = 0
    for p in paragraphs:
        t = approx_tokens(p)
        if current and count + t > MAX_CHILD_TOKENS:
            children.append("\n\n".join(current))
            current, count = [], 0
        current.append(p)
        count += t
    if current:
        children.append("\n\n".join(current))
    # merge trailing tiny child into previous
    if len(children) > 1 and approx_tokens(children[-1]) < MIN_CHILD_TOKENS:
        children[-2] += "\n\n" + children[-1]
        children.pop()
    return children


def chunk_markdown_dir(dirpath, chunks):
    for f in sorted(Path(dirpath).glob("*.md")):
        meta, body = parse_frontmatter(f.read_text())
        source_id = meta.get("source_id", f.stem)
        for si, (heading, text) in enumerate(split_sections(body)):
            parent_id = f"{source_id}#{si}"
            parent_text = f"{heading}\n\n{text}"
            for ci, child in enumerate(group_paragraphs(text) or [text]):
                chunks.append({
                    "chunk_id": f"{parent_id}.{ci}",
                    "parent_id": parent_id,
                    "source_id": source_id,
                    "doc_type": meta.get("doc_type"),
                    "title": meta.get("title"),
                    "section_heading": heading,
                    "section_path": meta.get("section_path"),
                    "product_area": meta.get("product_area"),
                    "product_version": meta.get("product_version")
                        or meta.get("min_version"),
                    "acl": meta.get("acl", "public"),
                    "updated_at": meta.get("updated_at"),
                    "related_error_codes": meta.get("related_error_codes", []),
                    "text": f"{meta.get('title', '')} > {heading}\n\n{child}",
                    "parent_text": parent_text,
                })


def chunk_tickets(path, chunks, limit=None):
    if not Path(path).exists():
        return
    for i, line in enumerate(Path(path).read_text().splitlines()):
        if limit and i >= limit:
            break
        t = json.loads(line)
        if t["status"] == "open" or not t.get("resolution"):
            continue  # only resolved tickets belong in the knowledge index
        chunks.append({
            "chunk_id": f"{t['ticket_id']}#0.0",
            "parent_id": f"{t['ticket_id']}#0",
            "source_id": t["ticket_id"],
            "doc_type": "support-ticket",
            "title": t["subject"],
            "section_heading": "Resolution",
            "section_path": f"Tickets > {t['product_area']}",
            "product_area": t["product_area"],
            "product_version": t["product_version"],
            "acl": "internal",
            "updated_at": t["created_at"][:10],
            "related_error_codes": [t["error_code"]] if t.get("error_code") else [],
            "text": (f"Ticket: {t['subject']}\n\nProblem: {t['body']}\n\n"
                     f"Resolution: {t['resolution']}"),
            "parent_text": None,
        })


def chunk_known_issues(path, chunks):
    if not Path(path).exists():
        return
    for line in Path(path).read_text().splitlines():
        k = json.loads(line)
        chunks.append({
            "chunk_id": f"{k['source_id']}#0.0",
            "parent_id": f"{k['source_id']}#0",
            "source_id": k["source_id"],
            "doc_type": "known-issue",
            "title": f"{k['error_code']}: {k['title']}",
            "section_heading": "Known issue",
            "section_path": f"Known Issues > {k['product_area_label']}",
            "product_area": k["product_area"],
            "product_version": None,
            "acl": k["acl"],
            "updated_at": k["updated_at"],
            "related_error_codes": [k["error_code"]],
            "text": (f"{k['error_code']}: {k['title']}\n\n"
                     f"Symptom: {k['symptom']}\nRoot cause: {k['root_cause']}\n"
                     f"Workaround: {k['workaround']}\n"
                     f"Affected versions: {', '.join(k['affected_versions'])}\n"
                     f"Fixed in: {k['fixed_in_version'] or 'not yet fixed'}"),
            "parent_text": None,
        })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", default="../output")
    ap.add_argument("--ticket-limit", type=int, default=2000,
                    help="Cap tickets indexed into the knowledge base")
    args = ap.parse_args()

    out = Path(args.output_dir)
    chunks = []
    chunk_markdown_dir(out / "docs", chunks)
    chunk_markdown_dir(out / "integration_guides", chunks)
    chunk_markdown_dir(out / "api_reference", chunks)
    chunk_tickets(out / "tickets.jsonl", chunks, args.ticket_limit)
    chunk_known_issues(out / "known_issues.jsonl", chunks)

    (out / "chunks.jsonl").write_text("\n".join(json.dumps(c) for c in chunks))
    parents = len({c["parent_id"] for c in chunks})
    print(f"Wrote {len(chunks)} child chunks ({parents} parents) to "
          f"{out / 'chunks.jsonl'}")


if __name__ == "__main__":
    main()
