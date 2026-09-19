#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
THEME_DIR="$ROOT/themes/hugo-arcana"

if [ -d "$THEME_DIR/.git" ]; then
  git -C "$THEME_DIR" pull --ff-only
else
  rm -rf "$THEME_DIR"
  git clone --depth 1 https://github.com/Weichwerke-Heidrich-Software/hugo-arcana-fork.git "$THEME_DIR"
fi

echo "Arcana theme ready: $THEME_DIR"
