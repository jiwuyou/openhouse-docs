#!/bin/sh
set -eu

log() {
  printf '%s\n' "$*"
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

SCRIPT_DIR=$(cd "$(dirname "$0")" >/dev/null 2>&1 && pwd)
ROOT_DIR=$(cd "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd)

require_cmd() {
  cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    die "Missing required command: $cmd"
  fi
}

main() {
  require_cmd python3

  if [ ! -f "$ROOT_DIR/scripts/build_docs_site.py" ]; then
    die "Missing $ROOT_DIR/scripts/build_docs_site.py"
  fi

  if python3 -c 'import markdown_it' >/dev/null 2>&1; then
    ver="$(python3 -c 'import markdown_it; print(getattr(markdown_it, "__version__", "unknown"))' 2>/dev/null || printf 'unknown')"
    log "ok: markdown_it importable (version: $ver)"
  else
    die "python dependency missing: markdown_it (run scripts/install.sh)"
  fi

  # Read-only check: verify the build script exists and parses, but do not generate site artifacts.
  python3 -c '
import ast
from pathlib import Path
path = Path("'"$ROOT_DIR/scripts/build_docs_site.py"'")
ast.parse(path.read_text(encoding="utf-8"))
' >/dev/null 2>&1 || die "build_docs_site.py has a syntax error"

  log "ok: build_docs_site.py syntax"
  log "note: build is not run in check mode; run: python3 scripts/build_docs_site.py"
}

main "$@"
