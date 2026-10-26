#!/bin/bash
# Execute the shared lossless YouTube caption pipeline for stdin video IDs.
# Usage: <ids on stdin> | transcribe-ids.sh <dest_dir> [--force]
# Reports: <dest>/<ID>.md; retained acquisitions: <dest>/transcripts/<ID>/.
# Only checksum-verified successes are skipped. --force always reacquires.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 -B "$SCRIPT_DIR/transcribe_ids.py" "$@"
