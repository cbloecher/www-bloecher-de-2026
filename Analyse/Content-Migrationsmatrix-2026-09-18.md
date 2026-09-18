# Content-Migrationsmatrix WordPress → Hugo

**Stand:** 18.09.2026  
**Quelle:** `migration-source/export/wordpress-content.json`

## Bestand

- 34 veröffentlichte Seiten
- 20 DE
- 14 EN
- 14 DE/EN-Übersetzungspaare
- 6 Seiten nur DE
- 0 verwaiste EN-Seiten

## Zielprinzip

- Deutsch bleibt Standardsprache ohne Sprachpräfix.
- Englisch liegt unter `/en/`.
- Sprachversionen werden über einen stabilen `translationKey` gekoppelt.
- Bestehende fachlich sinnvolle URLs bleiben nach Möglichkeit erhalten.
- Fehlerhafte oder historisch ungünstige URLs werden per 301 auf die neue kanonische URL geleitet.
- Demo-/Testseiten werden nicht migriert.

## DE/EN-Paare

| translationKey | DE aktuell | EN aktuell | Hugo-Ziel DE | Hugo-Ziel EN | Hinweis |
|---|---|---|---|---|---|
| home | `/` | `/en/foundry/` | `/` | `/en/` | EN-Startseite auf echten Sprach-Root legen |
| company | `/unternehmen/` | `/en/about-us/` | `/unternehmen/` | `/en/about-us/` | beibehalten |
| contact | `/unternehmen/kontakt/` | `/en/about-us/contact-us/` | `/unternehmen/kontakt/` | `/en/about-us/contact-us/` | beibehalten |
| quality | `/unternehmen/zertifizierung/` | `/en/about-us/quality-management/` | `/unternehmen/zertifizierung/` | `/en/about-us/quality-management/` | semantisch eher Qualität als nur Zertifizierung |
| directions | `/unternehmen/anfahrt/` | `/en/about-us/how-to-find-us/` | `/unternehmen/anfahrt/` | `/en/about-us/how-to-find-us/` | beibehalten |
| services | `/leistungen/` | `/en/services/` | `/leistungen/` | `/en/services/` | beibehalten |
| aluminium-sand-casting | `/leistungen/aluminium-sandguss/` | `/en/services/aluminium-sandcasting/` | `/leistungen/aluminium-sandguss/` | `/en/services/aluminium-sand-casting/` | EN-Schreibweise vereinheitlichen; Redirect alt→neu |
| model-making | `/leistungen/modellbau/` | `/en/services/model-making/` | `/leistungen/modellbau/` | `/en/services/model-making/` | beibehalten |
| 3d-print | `/leistungen/3d-druck/` | `/en/services/3d-print/` | `/leistungen/3d-druck/` | `/en/services/3d-print/` | beibehalten |
| temperature-control | `/leistungen/temperierung/` | `/en/services/temperature-control/` | `/leistungen/temperierung/` | `/en/services/temperature-control/` | beibehalten |
| 3d-scan | `/leistungen/3d-scannen/` | `/en/services/3d-scan/` | `/leistungen/3d-scannen/` | `/en/services/3d-scan/` | beibehalten |
| prototypes-spares | `/prototypen-ersatzteil/` | `/en/prototypes-and-spare-parts/` | `/prototypen-ersatzteil/` | `/en/prototypes-and-spare-parts/` | später ggf. in Leistungsstruktur einordnen |
| tools-molds | `/guss-fuer-werkzeuge-formen/` | `/en/tools-and-molds/` | `/guss-fuer-werkzeuge-formen/` | `/en/tools-and-molds/` | beibehalten |
| spares-on-demand | `/ersatzteile-nach-bedarf-de/` | `/en/ersatzteile-nach-bedarf-english/` | **zu prüfen** | **zu prüfen** | URL-Namen sind redaktionelle Altlasten; Inhalt/Notwendigkeit prüfen |

## Nur DE

| Seite | Aktuelle URL | Vorschlag |
|---|---|---|
| DEMO-CB: gb-Elemente | `/demo-cb-gb-elemente/` | **nicht migrieren**, 404/410 bzw. aus Index entfernen |
| DEMO-CB: Mediaelemente | `/00-demo-cb/` | **nicht migrieren**, 404/410 bzw. aus Index entfernen |
| Impressum | `/impressum/` | migrieren, DE ausreichend |
| Datenschutzerklärung | `/datenschutzerklaerung/` | migrieren, Inhalt separat rechtlich aktuell halten |
| weitere Leistungen & Technologien | `/leistungen/technologie/` | migrieren oder fachlich in Leistungsseiten auflösen |
| Jobs | `/jobs/` | migrieren; EN nur bei Bedarf ergänzen |

## Redirect-Mindestmenge

Mindestens folgende Redirects sind bereits absehbar:

```text
/en/foundry/                         -> /en/
/en/services/aluminium-sandcasting/ -> /en/services/aluminium-sand-casting/
```

Zusätzlich müssen die aus der SEO-Analyse bekannten fehlerhaften doppelten EN-Pfade auf ihre kanonischen Ziele zeigen, z. B.:

```text
/en/foundry//foundry                         -> /en/
/en/services/3d-print//3d-print              -> /en/services/3d-print/
/en/about-us/quality-management//quality-management
                                            -> /en/about-us/quality-management/
```

Vor Go-live wird aus Sitemap, WordPress-Export und Webserver-/Crawl-Daten eine vollständige Redirect-Matrix erzeugt.

## Empfohlene Hugo-Dateien

```text
content/
├── de/
│   ├── _index.md
│   ├── unternehmen/
│   │   ├── _index.md
│   │   ├── kontakt.md
│   │   ├── zertifizierung.md
│   │   └── anfahrt.md
│   ├── leistungen/
│   │   ├── _index.md
│   │   ├── aluminium-sandguss.md
│   │   ├── modellbau.md
│   │   ├── 3d-druck.md
│   │   ├── temperierung.md
│   │   ├── 3d-scannen.md
│   │   └── technologie.md
│   ├── prototypen-ersatzteil.md
│   ├── guss-fuer-werkzeuge-formen.md
│   ├── jobs.md
│   ├── impressum.md
│   └── datenschutzerklaerung.md
└── en/
    ├── _index.md
    ├── about-us/
    │   ├── _index.md
    │   ├── contact-us.md
    │   ├── quality-management.md
    │   └── how-to-find-us.md
    ├── services/
    │   ├── _index.md
    │   ├── aluminium-sand-casting.md
    │   ├── model-making.md
    │   ├── 3d-print.md
    │   ├── temperature-control.md
    │   └── 3d-scan.md
    ├── prototypes-and-spare-parts.md
    └── tools-and-molds.md
```

## Noch nicht automatisch entscheiden

Diese Punkte bleiben bewusst redaktionell offen:

- Wird `Ersatzteile nach Bedarf` eigenständig weitergeführt oder in `Prototypen + Ersatzteile` integriert?
- Wird `weitere Leistungen & Technologien` eine eigene Landingpage oder in die Kernleistungen aufgeteilt?
- Soll `Zertifizierung` zukünftig als breitere Seite `Qualität` geführt werden?
- Sollen Prototypen/Ersatzteile und Werkzeuge/Formen unter `/leistungen/` eingeordnet werden?

Für den ersten Hugo-Prototyp sollten die aktuellen URLs zunächst weitgehend erhalten bleiben. Strukturänderungen können danach mit sauberer Redirect-Matrix erfolgen.
