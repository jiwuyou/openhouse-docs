#!/usr/bin/env sh
set -eu

log() {
  printf '[OpenHouse docs] %s\n' "$*"
}

die() {
  printf '[OpenHouse docs] ERROR: %s\n' "$*" >&2
  exit 1
}

SCRIPT_DIR=$(cd "$(dirname "$0")" >/dev/null 2>&1 && pwd)
ROOT_DIR=$(cd "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd)
DOCS_DIR="$ROOT_DIR/docs"

[ -d "$DOCS_DIR" ] || die "Missing docs directory: $DOCS_DIR"
[ -f "$DOCS_DIR/START_HERE.md" ] || die "Missing START_HERE.md in $DOCS_DIR"

is_current_ubuntu() {
  [ -r /etc/os-release ] && grep -qi '^ID=ubuntu' /etc/os-release
}

termux_home() {
  if is_current_ubuntu; then
    printf '%s\n' /data/data/com.termux/files/home
  else
    printf '%s\n' "${HOME:-/data/data/com.termux/files/home}"
  fi
}

ensure_symlink() {
  target="$1"
  link_path="$2"
  parent=$(dirname "$link_path")
  mkdir -p "$parent"

  if [ -L "$link_path" ] || [ -f "$link_path" ]; then
    rm -f "$link_path"
  elif [ -e "$link_path" ]; then
    backup="${link_path}.backup-$(date +%Y%m%d%H%M%S)"
    mv "$link_path" "$backup"
    log "Backed up non-symlink path: $link_path -> $backup"
  fi

  ln -sfn "$target" "$link_path"
}

copy_docs() {
  target="$1"
  parent=$(dirname "$target")
  tmp="${target}.tmp.$$"
  mkdir -p "$parent"
  rm -rf "$tmp"
  mkdir -p "$tmp"
  cp -a "$DOCS_DIR/." "$tmp/"
  rm -rf "$target"
  mv "$tmp" "$target"
}

TERMUX_HOME=$(termux_home)
TARGET_DIR="${OPENHOUSE_DOC_TARGET:-$TERMUX_HOME/openhouseai-docs/official}"
AGENT_NOTES_DIR="$TERMUX_HOME/openhouseai-docs/agent-notes"
LEGACY_DOC_ROOT="$TERMUX_HOME/smallphoneai-docs"
OPENHOUSE_ROOT="$TERMUX_HOME/openhouse"

log "Syncing public docs to $TARGET_DIR"
copy_docs "$TARGET_DIR"
mkdir -p "$AGENT_NOTES_DIR" "$LEGACY_DOC_ROOT" "$OPENHOUSE_ROOT"
ensure_symlink "$TARGET_DIR" "$OPENHOUSE_ROOT/docs"
ensure_symlink "$TARGET_DIR" "$LEGACY_DOC_ROOT/official"
ensure_symlink "$AGENT_NOTES_DIR" "$LEGACY_DOC_ROOT/agent-notes"

if is_current_ubuntu; then
  mkdir -p "$HOME/openhouse" "$HOME/openhouseai-docs" "$HOME/smallphoneai-docs"
  ensure_symlink "$TARGET_DIR" "$HOME/openhouse/docs"
  ensure_symlink "$TARGET_DIR" "$HOME/openhouseai-docs/official"
  ensure_symlink "$AGENT_NOTES_DIR" "$HOME/openhouseai-docs/agent-notes"
  ensure_symlink "$TARGET_DIR" "$HOME/smallphoneai-docs/official"
  ensure_symlink "$AGENT_NOTES_DIR" "$HOME/smallphoneai-docs/agent-notes"
fi

log "Public docs synced."
printf '%s\n' "$TARGET_DIR"
printf '%s\n' "$OPENHOUSE_ROOT/docs"
