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
APK_DOCS_DIR="${OPENHOUSE_APK_DOCS_DIR:-/root/projects/smallphoneai/openhouseai-app/app/src/main/assets/openhouse/docs-public}"

[ -d "$DOCS_DIR" ] || die "Missing docs directory: $DOCS_DIR"
[ -d "$APK_DOCS_DIR" ] || die "Missing APK docs-public directory: $APK_DOCS_DIR"

log "Syncing public docs snapshot to APK assets: $APK_DOCS_DIR"
APK_DOCS_PARENT=$(dirname "$APK_DOCS_DIR")
APK_DOCS_TMP="${APK_DOCS_DIR}.tmp.$$"

mkdir -p "$APK_DOCS_PARENT"
rm -rf "$APK_DOCS_TMP"
mkdir -p "$APK_DOCS_TMP"
cp -a "$DOCS_DIR/." "$APK_DOCS_TMP/"
rm -rf "$APK_DOCS_DIR"
mv "$APK_DOCS_TMP" "$APK_DOCS_DIR"
log "APK docs snapshot updated."
