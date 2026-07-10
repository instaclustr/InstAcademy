"""
Verify a downloaded the support tool corpus against its manifest. Learners run
this once after extracting the tarball, before ingesting. Guarantees
every learner is working from byte-identical data, so lab results match
the course videos.

Usage:
    tar xzf example-corp-corpus-v2.1.0.tar.gz
    python verify_corpus.py --corpus example-corp-corpus-v2.1.0
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True,
                    help="path to the extracted corpus directory")
    args = ap.parse_args()

    root = Path(args.corpus)
    manifest_path = root / "CORPUS_MANIFEST.json"
    if not manifest_path.exists():
        sys.exit(f"No CORPUS_MANIFEST.json in {root}. Wrong directory?")

    manifest = json.loads(manifest_path.read_text())
    print(f"{manifest['name']} v{manifest['version']} "
          f"(built {manifest['built_at']})")

    expected = manifest["sha256"]
    missing, mismatched = [], []
    for rel, digest in expected.items():
        p = root / rel
        if not p.exists():
            missing.append(rel)
        elif sha256(p) != digest:
            mismatched.append(rel)

    extra = [str(p.relative_to(root)) for p in root.rglob("*")
             if p.is_file() and str(p.relative_to(root)) not in expected
             and p.name != "CORPUS_MANIFEST.json"]

    if missing or mismatched:
        for f in missing:
            print(f"  MISSING:    {f}")
        for f in mismatched:
            print(f"  MISMATCHED: {f}")
        sys.exit(f"\nFAILED: corpus does not match manifest "
                 f"({len(missing)} missing, {len(mismatched)} mismatched). "
                 f"Re-download the tarball; do not regenerate locally.")

    if extra:
        print(f"  note: {len(extra)} extra file(s) not in manifest "
              f"(ignored): {extra[:3]}")

    counts = manifest["counts"]
    print(f"OK: {len(expected)} files verified. "
          f"{counts['chunks']} chunks, {counts['golden_queries']} golden "
          f"queries, {counts['tickets']} tickets.")
    print("Next: python3 scripts/ingest_chunks.py --model-id <MODEL_ID> "
          f"--chunks {root / 'chunks.jsonl'}")


if __name__ == "__main__":
    main()
