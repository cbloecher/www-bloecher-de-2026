#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
THEME_DIR="$ROOT/themes/hugo-theme-pico-corp"
THEME_REPOSITORY="https://github.com/PhantomPixelDev/hugo-theme-pico-corp.git"
THEME_REF="7b43e743259f6b9e61a2a8195bf3aa723df6954e"

if [ ! -d "$THEME_DIR/.git" ]; then
  rm -rf "$THEME_DIR"
  git init "$THEME_DIR"
  git -C "$THEME_DIR" remote add origin "$THEME_REPOSITORY"
fi

git -C "$THEME_DIR" fetch --depth 1 origin "$THEME_REF"
git -C "$THEME_DIR" checkout --detach --force FETCH_HEAD

echo "Pico Corp theme ready at ${THEME_REF}: $THEME_DIR"
