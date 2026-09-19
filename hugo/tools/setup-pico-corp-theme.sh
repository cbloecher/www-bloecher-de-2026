#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
THEME_DIR="$ROOT/themes/hugo-theme-pico-corp"

if [ -d "$THEME_DIR/.git" ]; then
  git -C "$THEME_DIR" pull --ff-only
else
  rm -rf "$THEME_DIR"
  git clone --depth 1 https://github.com/PhantomPixelDev/hugo-theme-pico-corp.git "$THEME_DIR"
fi

echo "Pico Corp theme ready: $THEME_DIR"
