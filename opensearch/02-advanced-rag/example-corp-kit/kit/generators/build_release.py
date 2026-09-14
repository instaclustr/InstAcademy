"""
Build the canonical the support tool corpus release: one batch, generated once
by the course maintainer, distributed to all learners so every lab and
every eval number matches the videos exactly.

Runs the full generation pipeline at the canonical scale with the
canonical seed, computes sha256 checksums for every file, writes a
release manifest, and packages a single distributable tarball.

Usage:
    python build_release.py --version 1.0.0
    # -> ../dist/example-corp-corpus-v1.0.0.tar.gz

Learners never run this. They download the tarball, verify it with
verify_corpus.py, and go straight to ingest_opensearch.py.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

# Canonical parameters. Changing ANY of these is a new corpus version.
CANONICAL = {
    "seed": 42,
    "docs_pages": 1000,
    "tickets": 10000,
    "golden_queries": 300,
    "tickets_indexed": 4000,   # resolved tickets loaded into the KB index
}

PIPELINE = [
    ["generate_docs.py", "--pages", str(CANONICAL["docs_pages"]),
     "--seed", str(CANONICAL["seed"])],
    ["generate_integration_guides.py", "--seed", str(CANONICAL["seed"])],
    ["generate_known_issues.py"],
    ["generate_api_reference.py"],
    ["generate_tickets.py", "--count", str(CANONICAL["tickets"]),
     "--seed", str(CANONICAL["seed"])],
    ["chunk_documents.py", "--ticket-limit",
     str(CANONICAL["tickets_indexed"])],
    ["generate_golden_set.py", "--count", str(CANONICAL["golden_queries"]),
     "--seed", str(CANONICAL["seed"])],
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True, help="e.g. 1.0.0")
    ap.add_argument("--output-dir", default="../output")
    ap.add_argument("--dist-dir", default="../dist")
    args = ap.parse_args()

    out = Path(args.output_dir)
    if out.exists():
        shutil.rmtree(out)  # canonical build starts clean, always
    out.mkdir(parents=True)

    print(f"Building canonical corpus v{args.version} "
          f"(seed={CANONICAL['seed']})")
    for cmd in PIPELINE:
        print(f"  running {cmd[0]}")
        r = subprocess.run([sys.executable] + cmd, capture_output=True,
                           text=True)
        if r.returncode != 0:
            print(r.stdout, r.stderr)
            sys.exit(f"FAILED: {cmd[0]}")

    # Checksum every file in the corpus
    files = sorted(p for p in out.rglob("*") if p.is_file())
    checksums = {str(p.relative_to(out)): sha256(p) for p in files}

    counts = {
        "docs_pages": len(list((out / "docs").glob("DOC-*.md"))),
        "integration_guides": len(list(
            (out / "integration_guides").glob("GUIDE-*.md"))),
        "known_issues": len((out / "known_issues.jsonl")
                            .read_text().splitlines()),
        "api_pages": len(list((out / "api_reference").glob("API-*.md"))),
        "tickets": len((out / "tickets.jsonl").read_text().splitlines()),
        "chunks": len((out / "chunks.jsonl").read_text().splitlines()),
        "golden_queries": len((out / "golden_set.jsonl")
                              .read_text().splitlines()),
    }

    manifest = {
        "name": "example-corp-corpus",
        "version": args.version,
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "canonical_parameters": CANONICAL,
        "counts": counts,
        "note": ("Synthetic corpus for the Advanced RAG with OpenSearch "
                 "learning path. Example Corp is fictional. Identical for "
                 "every learner: do not regenerate; verify with "
                 "verify_corpus.py and ingest as-is."),
        "reproducibility": ("Neural and hybrid eval numbers additionally "
                            "depend on the embedding model. The course "
                            "standard is "
                            "huggingface/sentence-transformers/"
                            "all-MiniLM-L6-v2 (384 dims). Same corpus + "
                            "same model = same numbers as the videos."),
        "sha256": checksums,
    }
    (out / "CORPUS_MANIFEST.json").write_text(json.dumps(manifest, indent=2))

    dist = Path(args.dist_dir)
    dist.mkdir(parents=True, exist_ok=True)
    tarball = dist / f"example-corp-corpus-v{args.version}.tar.gz"
    with tarfile.open(tarball, "w:gz") as tf:
        tf.add(out, arcname=f"example-corp-corpus-v{args.version}")

    print(json.dumps(counts, indent=2))
    print(f"\nRelease: {tarball} "
          f"({tarball.stat().st_size / 1_048_576:.1f} MB)")
    print(f"Manifest sha256 of chunks.jsonl: "
          f"{checksums['chunks.jsonl'][:16]}...")


if __name__ == "__main__":
    main()
