#!/usr/bin/env bash
set -euo pipefail

#OUT="analyse/wordpress"
#WP="wordpress"
#SQL="mysqldump.txt"


OUT="analyse/wordpress"
WP="."
SQL="mysqldump.txt"



mkdir -p "$OUT"

if [[ ! -d "$WP" ]]; then
  echo "[ERR] Verzeichnis '$WP' nicht gefunden."
  exit 1
fi
if [[ ! -f "$SQL" ]]; then
  echo "[ERR] Datei '$SQL' nicht gefunden."
  exit 1
fi

cat > "$OUT/README.md" <<'EOT'
# WordPress-Migrationsanalyse

Automatisch erzeugte, sanitiserte Bestandsaufnahme der bestehenden bloecher.de-WordPress-Installation.

Der originale SQL-Dump, Benutzer-Passworthashes, `wp-config.php` und andere Zugangsdaten sind bewusst **nicht** enthalten.
EOT

{
  echo "=== WordPress Version ==="
  grep "\$wp_version" "$WP/wp-includes/version.php" 2>/dev/null || true
  echo
  echo "=== PHP/WordPress Kernstruktur ==="
  find "$WP" -maxdepth 1 -mindepth 1 -printf '%f\n' 2>/dev/null | sort
} > "$OUT/01-wordpress-version-und-struktur.txt"

{
  echo "=== Plugins ==="
  find "$WP/plugins" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' 2>/dev/null | sort
  echo
  echo "=== Themes ==="
  find "$WP/themes" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' 2>/dev/null | sort
} > "$OUT/02-plugins-und-themes.txt"

{
  echo "=== wp-content Verzeichnisse ==="
  find "$WP" -maxdepth 2 -type d 2>/dev/null | sort
  echo
  echo "=== Uploads Groesse ==="
  du -sh "$WP/uploads" 2>/dev/null || true
  echo
  echo "=== Anzahl Upload-Dateien ==="
  find "$WP/uploads" -type f 2>/dev/null | wc -l
  echo
  echo "=== Dateiendungen in uploads ==="
  find "$WP/uploads" -type f 2>/dev/null \
    | sed -n 's/.*\.//p' \
    | tr '[:upper:]' '[:lower:]' \
    | sort | uniq -c | sort -nr | head -100
} > "$OUT/03-medienbestand.txt"

{
  echo "=== Tabellen ==="
  grep -oE 'CREATE TABLE [`"]?[^`"( ]+' "$SQL" \
    | sed -E 's/CREATE TABLE [`"]?//' \
    | sort -u
} > "$OUT/04-datenbank-tabellen.txt"

{
  echo "=== Relevante WordPress Tabellen ==="
  grep -oE 'CREATE TABLE [`"]?[^`"( ]+' "$SQL" \
    | sed -E 's/CREATE TABLE [`"]?//' \
    | grep -Ei 'posts|postmeta|terms|termmeta|term_taxonomy|term_relationships|options|icl_|pll_|trp_' \
    | sort -u || true
} > "$OUT/05-relevante-tabellen.txt"

{
  echo "=== Mehrsprachigkeits-Hinweise ==="
  grep -Eio 'wpml|icl_[A-Za-z0-9_]*|polylang|pll_[A-Za-z0-9_]*|translatepress|trp_[A-Za-z0-9_]*|weglot|multilingual' "$SQL" \
    | sort | uniq -c | sort -nr | head -200 || true
} > "$OUT/06-mehrsprachigkeit.txt"

{
  echo "=== Enfold / Avia Hinweise ==="
  grep -Eio 'avia_[A-Za-z0-9_-]*|av_[A-Za-z0-9_-]*|enfold|aviaLayoutBuilder|avia_builder' "$SQL" \
    | sort | uniq -c | sort -nr | head -300 || true
} > "$OUT/07-enfold-avia.txt"

{
  echo "=== WordPress Post Types / Status Hinweise ==="
  grep -Ei 'INSERT INTO [`"]?[^`"]*posts' "$SQL" \
    | grep -Eo "'(page|post|attachment|revision|nav_menu_item|publish|draft|private|inherit|trash)'" \
    | sort | uniq -c | sort -nr || true
} > "$OUT/08-posttypes-status.txt"

{
  echo "=== Interne URL-/Domain-Hinweise ==="
  grep -Eo 'https?://(www\.)?bloecher\.de[^" <>)]*' "$SQL" \
    | sed 's/[[:space:]]*$//' \
    | sort -u \
    | head -2000 || true
} > "$OUT/09-interne-urls.txt"

{
  echo "=== Externe Domains aus SQL-Dump ==="
  grep -Eo 'https?://[^/" <>)]+' "$SQL" \
    | sed -E 's#https?://##' \
    | tr '[:upper:]' '[:lower:]' \
    | grep -vE '(^|www\.)bloecher\.de$' \
    | sort | uniq -c | sort -nr | head -300 || true
} > "$OUT/10-externe-domains.txt"

{
  echo "=== Shortcode-Typen ==="
  grep -Eo '\[[A-Za-z_][A-Za-z0-9_-]*' "$SQL" \
    | tr -d '[' \
    | sort | uniq -c | sort -nr | head -300 || true
} > "$OUT/11-shortcodes.txt"

{
  echo "=== Sprach-/Pfad-Indikatoren in Uploads ==="
  find "$WP/uploads" -type f 2>/dev/null \
    | sed "s#^$WP/uploads/##" \
    | grep -Ei '(^|/)(de|en|english|deutsch)(/|[-_])|[-_](de|en)\.' \
    | head -1000 || true
} > "$OUT/12-upload-sprachindikatoren.txt"

find "$WP/uploads" -type f 2>/dev/null \
  | sed "s#^$WP/uploads/##" \
  | sort > "$OUT/13-upload-dateiliste.txt"

{
  echo "=== Theme-Dateien (max. 3 Ebenen) ==="
  find "$WP/themes" -maxdepth 3 -type f 2>/dev/null \
    | sed "s#^$WP/themes/##" \
    | sort | head -5000
} > "$OUT/14-theme-dateiliste.txt"

{
  echo "=== Plugin-Dateien (max. 2 Ebenen) ==="
  find "$WP/plugins" -maxdepth 2 -type f 2>/dev/null \
    | sed "s#^$WP/plugins/##" \
    | sort | head -5000
} > "$OUT/15-plugin-dateiliste.txt"

cat > "$OUT/ANALYSE-HINWEISE.md" <<'EOT'
# Hinweise zur Analyse

Diese Dateien dienen ausschließlich der technischen Migration von WordPress zu Hugo.

Enthalten sind:
- WordPress-Version und Verzeichnisstruktur
- Plugins und Themes
- Medienbestand und Dateiliste
- Datenbank-Tabellenstruktur
- Hinweise auf Mehrsprachigkeits-Plugins
- Hinweise auf Enfold/Avia
- Shortcode-Typen
- interne URLs und externe Domains

Bewusst nicht enthalten:
- kompletter SQL-Dump
- `wp-config.php`
- Benutzerkonten
- Passwort-Hashes
- API-Keys / Secrets
- Session-/Auth-Schlüssel

Falls für die eigentliche Inhaltsmigration später konkrete Seiteninhalte benötigt werden,
sollten diese gezielt und sanitisiert exportiert werden, statt den kompletten SQL-Dump zu versionieren.
EOT

echo
printf '[OK] Analyse erzeugt unter: %s\n\n' "$OUT"
find "$OUT" -maxdepth 1 -type f -printf '%f\n' | sort

