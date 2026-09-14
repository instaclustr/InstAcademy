#!/usr/bin/env bash
# Validate that the course material is internally consistent.
# Checks the Bruno collection against the chapter READMEs, the bulk payloads
# against the blocks printed in the READMEs, and every internal link.
# Usage: scripts/validate.sh   (from the course root; needs Python 3)

set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/validate.py
