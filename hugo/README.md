# Hugo – www.bloecher.de

Dies ist das neue statische Hugo-Projekt für www.bloecher.de.

## Verzeichnisstruktur

```text
hugo/
├── hugo.toml
├── archetypes/
├── assets/
├── content/
│   ├── de/
│   └── en/
├── data/
├── i18n/
├── layouts/
├── static/
├── tools/
├── public/        # generiert, nicht versioniert
└── resources/     # generiert, nicht versioniert
```

`public/` ist ausschließlich Build-Ausgabe und wird von Hugo bei jedem Build neu erzeugt.

Für die Testsubdomain kann der DocumentRoot auf

```text
.../www-bloecher-de-2026/hugo/public
```

zeigen.

## Lokaler/Server-Build

```bash
cd hugo
hugo --cleanDestinationDir
```

Für einen Preview-Server:

```bash
hugo server --bind 0.0.0.0 --baseURL https://hugo.bloecher.de/
```

## Sprache

- DE ist Standardsprache und liegt direkt unter `/`
- EN liegt unter `/en/`
- weitere Sprachen können später über `[languages.xx]` ergänzt werden

## Migration

Quelle:

```text
../migration-source/export/wordpress-content.json
```

Der Konverter unter `tools/migrate_wordpress.py` erzeugt zunächst reviewbare Hugo-Inhaltsdateien.


## WordPress-Inhalte importieren

Vom Verzeichnis `hugo/`:

```bash
python3 tools/migrate_wordpress.py
```

Der Importer erzeugt bzw. aktualisiert:

```text
content/de/
content/en/
assets/images/imported/
```

Er ist bewusst konservativ. Nicht sicher konvertierbare Avia-Bausteine werden als
`migration_review` im Front Matter bzw. als `MIGRATION-REVIEW` im Inhalt markiert.
