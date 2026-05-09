#!/bin/sh
set -eu

log() {
  printf '%s\n' "$*"
}

warn() {
  printf 'WARN: %s\n' "$*" >&2
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

  if [ ! -f "$ROOT_DIR/requirements.txt" ]; then
    die "Missing $ROOT_DIR/requirements.txt"
  fi

  log "install: python deps (pip --user)"
  if python3 -m pip install --user -r "$ROOT_DIR/requirements.txt"; then
    log "done"
    return 0
  fi

  # Many distro-managed Pythons enforce PEP 668 (externally managed env) and reject even --user installs.
  # Retry with an explicit override flag.
  warn "pip install --user failed; retrying with --break-system-packages"
  python3 -m pip install --user --break-system-packages -r "$ROOT_DIR/requirements.txt"
  log "done"
}

main "$@"
