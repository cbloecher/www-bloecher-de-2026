#!/usr/bin/env bash
set -euo pipefail

# Snapshot der live ausgelieferten HTML/CSS-Referenz von www.bloecher.de.
# Dient nur als Design-/Migrationsreferenz, nicht zur 1:1-Übernahme von Enfold.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT="$ROOT/migration-source/reference-live"
HTML="$OUT/html"
CSS="$OUT/css"

mkdir -p "$HTML" "$CSS"

BASE="https://www.bloecher.de"

declare -A PAGES=(
  [start]="/"
  [leistungen]="/leistungen/"
  [sandguss]="/leistungen/aluminium-sandguss/"
  [modellbau]="/leistungen/modellbau/"
  [3d-druck]="/leistungen/3d-druck/"
  [unternehmen]="/unternehmen/"
  [kontakt]="/unternehmen/kontakt/"
)

: > "$OUT/css-urls.txt"

for name in "${!PAGES[@]}"; do
  path="${PAGES[$name]}"
  echo "[HTML] $BASE$path"
  curl -L --fail --silent --show-error     -A 'Mozilla/5.0 Hugo migration reference snapshot'     "$BASE$path"     -o "$HTML/$name.html"

  python3 - "$HTML/$name.html" "$BASE$path" >> "$OUT/css-urls.txt" <<'PY'
import re, sys
from pathlib import Path
from urllib.parse import urljoin

html_path = Path(sys.argv[1])
base_url = sys.argv[2]
text = html_path.read_text(encoding="utf-8", errors="replace")

for href in re.findall(
    r'<link\b[^>]*rel=["\'][^"\']*stylesheet[^"\']*["\'][^>]*href=["\']([^"\']+)["\']',
    text,
    flags=re.I,
):
    print(urljoin(base_url, href))
PY
done

sort -u "$OUT/css-urls.txt" -o "$OUT/css-urls.txt"

n=0
while IFS= read -r url; do
  [ -n "$url" ] || continue
  n=$((n+1))
  base="$(basename "${url%%\?*}")"
  [ -n "$base" ] || base="style.css"
  file="$(printf '%02d-%s' "$n" "$base")"

  echo "[CSS ] $url"
  curl -L --fail --silent --show-error     -A 'Mozilla/5.0 Hugo migration reference snapshot'     "$url"     -o "$CSS/$file"

  printf '%s\t%s\n' "$file" "$url"
done < "$OUT/css-urls.txt" > "$OUT/css-files.tsv"

cat > "$OUT/README.md" <<'EOF'
# Live-Referenz www.bloecher.de

Snapshot der aktuell ausgelieferten WordPress-/Enfold-Seite als Referenz für den Hugo-Neuaufbau.

Zweck:
- Typografie
- Abstände
- Farbsystem
- Header/Navigation
- Unterseiten-Charakter
- wiederkehrende Gestaltungsmuster

Nicht vorgesehen:
- Enfold technisch übernehmen
- CSS 1:1 weiterverwenden
- WordPress-/Plugin-Abhängigkeiten in Hugo nachbauen

Die Hugo-Seite soll die visuelle Identität treffen, aber technisch und semantisch neu aufgebaut werden.
EOF

echo
echo "[OK] Snapshot: $OUT"
echo "[OK] HTML-Dateien: $(find "$HTML" -type f | wc -l)"
echo "[OK] CSS-Dateien:  $(find "$CSS" -type f | wc -l)"
