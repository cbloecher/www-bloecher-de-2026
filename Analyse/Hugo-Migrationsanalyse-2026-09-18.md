# WordPress → Hugo – Migrationsanalyse

**Stand:** 18.09.2026  
**Ziel:** Umbau von `www.bloecher.de` von WordPress/Enfold auf eine statische, responsive und mehrsprachige Website.

## Entscheidung

Für das Zielbild ist **Hugo die bevorzugte Architektur**.

Hugo übernimmt dabei ausschließlich:

- Content-Struktur,
- Mehrsprachigkeit,
- Templates/Partials,
- Asset-Pipeline,
- statischen Build.

Die ausgelieferte Website besteht aus **semantischem HTML, CSS und minimalem Vanilla JavaScript**. Ein fertiges Hugo-Theme oder ein JavaScript-Framework ist nicht vorgesehen.

## Warum Hugo hier gut passt

Die Website ist überwiegend eine klassische Unternehmens- und Leistungswebsite. Es gibt aktuell keinen Hinweis darauf, dass serverseitige Laufzeitlogik oder ein komplexes Frontend-Framework benötigt wird.

Die wesentlichen Anforderungen passen direkt zu Hugo:

- responsive statische Ausgabe,
- DE/EN mit Perspektive auf weitere Sprachen,
- stabile und kontrollierbare URL-Struktur,
- zentrale Templates statt dupliziertem HTML,
- Markdown/strukturierte Front-Matter-Daten,
- sehr gute Eignung für Git- und LLM-gestützte Pflege,
- Build ohne PHP und Datenbank,
- kleine Angriffsfläche und einfache Bereitstellung.

## Ist-Zustand WordPress

### Relevante Komponenten

Aus dem gesicherten Bestand:

- Polylang 3.8.9
- Yoast SEO 22.1
- Google Sitemap Generator 4.1.21
- Enfold 5.6.10
- historisch zusätzlich Enfold gb/black 4.8.1
- zwei Child-Themes:
  - `enfold-child`
  - `enfold-child-black`

Die beiden gesicherten Child-Themes enthalten praktisch keine eigene Logik oder Gestaltung. `functions.php` und `style.css` sind im Wesentlichen unveränderte Child-Theme-Platzhalter. Daraus folgt: Die heutige Darstellung steckt überwiegend in Enfold/Avia-Konfiguration und Datenbankinhalten, nicht in individuell programmiertem Theme-Code.

### Mehrsprachigkeit

Polylang bestätigt, dass die Sprachbeziehungen in WordPress als strukturierte Daten vorliegen bzw. vorlagen. Diese Informationen sollten bei der Migration gezielt extrahiert werden.

Aus der bestehenden SEO-Analyse ist bekannt:

- DE und EN sind vorhanden,
- englische URLs weisen teilweise fehlerhafte doppelte Slugs auf,
- hreflang-Verknüpfungen sind nicht zuverlässig,
- diese Fehler dürfen nicht in das neue System übernommen werden.

### Inhalte

Die aktuelle Website enthält bereits brauchbaren fachlichen Content. Das Problem ist weniger fehlender Inhalt als dessen technische und semantische Strukturierung.

Bekannte Themen:

- Aluminium-Sandguss,
- Modell-/Werkzeugbau,
- 3D-gedruckte Formen und Kerne,
- Bearbeitung/Folgeprozesse,
- Qualität und Prüfverfahren,
- Unternehmensinformationen,
- Kontakt/Anfrage.

### Medien

Der WordPress-Medienbestand wurde bereits stark bereinigt:

- WordPress-generierte Thumbnail-/Resize-Derivate wurden entfernt,
- Originaldateien bleiben erhalten,
- Hash-Dubletten wurden identifiziert,
- der verbleibende Bestand ist klein genug für Git.

Die neue Hugo-Seite soll responsive Bildgrößen selbst erzeugen. WordPress-Derivate werden nicht übernommen.

## Zielarchitektur

Empfohlene Repo-Struktur:

```text
/
├── hugo.toml
├── content/
│   ├── de/
│   │   ├── _index.md
│   │   ├── leistungen/
│   │   ├── unternehmen/
│   │   ├── qualitaet/
│   │   └── kontakt/
│   └── en/
│       ├── _index.md
│       ├── services/
│       ├── company/
│       ├── quality/
│       └── contact/
├── layouts/
│   ├── _default/
│   ├── partials/
│   │   ├── head.html
│   │   ├── header.html
│   │   ├── footer.html
│   │   ├── hreflang.html
│   │   ├── schema.html
│   │   └── responsive-image.html
│   └── shortcodes/
├── assets/
│   ├── css/
│   └── js/
├── static/
│   ├── favicon/
│   └── documents/
├── data/
│   └── company.yaml
└── migration-source/
```

## URL-Strategie

Empfohlen:

```text
DE: https://www.bloecher.de/
EN: https://www.bloecher.de/en/
FR: https://www.bloecher.de/fr/   # perspektivisch
```

Deutsch bleibt Standardsprache ohne Präfix.

Beispiele:

```text
/leistungen/
/leistungen/aluminium-sandguss/
/leistungen/3d-sanddruck/
/unternehmen/
/qualitaet/
/kontakt/

/en/services/
/en/services/aluminium-sand-casting/
/en/services/3d-sand-printing/
/en/company/
/en/quality/
/en/contact/
```

Die Sprachversionen werden über Hugos Translation-Mechanismus miteinander verbunden. URL-Slugs dürfen sprachspezifisch sein; die fachliche Verbindung erfolgt über Translation Keys bzw. die Hugo-Sprachzuordnung.

## Content-Modell

Jede Inhaltsseite sollte mindestens folgende Front-Matter-Daten besitzen:

```yaml
title:
description:
slug:
translationKey:
draft:
seo:
  title:
  description:
  noindex: false
hero:
  image:
  alt:
```

Technische Leistungsseiten können zusätzlich strukturierte Fakten besitzen:

```yaml
facts:
  max_weight:
  max_dimensions:
  lot_sizes:
  materials:
  processes:
  standards:
```

Damit stehen relevante Angaben nicht nur als Fließtext, sondern bei Bedarf auch strukturiert für Tabellen, Fact-Boxen, JSON-LD oder spätere maschinenlesbare Ausgaben zur Verfügung.

## SEO-/KI-Grundlagen im Hugo-Template

Von Anfang an zentral in den Templates vorsehen:

- individuelle `<title>`,
- individuelle Meta-Description,
- Canonical URL,
- `hreflang` für alle Übersetzungen,
- `x-default`,
- OpenGraph-Basisdaten,
- semantische H1/H2/H3-Struktur,
- Sitemap,
- robots.txt,
- Organization-/LocalBusiness-JSON-LD,
- optional Service-JSON-LD auf Leistungsseiten,
- sinnvolle Alt-Texte für inhaltstragende Bilder.

`llms.txt` kann später ergänzt werden, ist aber keine Voraussetzung.

## Responsive Medien

Originalbilder sollen als Quellmaterial erhalten bleiben.

Hugo erzeugt je nach Einsatz:

- unterschiedliche Breiten,
- moderne Formate wie WebP,
- `srcset` und `sizes`,
- definierte Qualitätsstufen.

Damit entfällt die bisherige WordPress-Sammlung zahlreicher dauerhaft gespeicherter Bildderivate.

## Was nicht migriert wird

Bewusst nicht 1:1 übernehmen:

- Enfold-/Avia-Markup,
- Avia-Shortcodes,
- WordPress-Thumbnail-Dateien,
- generierte Enfold-CSS-/JS-Dateien,
- WordPress-Plugins,
- WordPress-Theme-Code,
- fehlerhafte historische EN-URLs,
- Platzhaltertexte,
- generische SEO-Metadaten.

Das Ziel ist keine technische Kopie von WordPress, sondern eine **inhaltliche und visuelle Neuabbildung mit sauberem statischem Zielmodell**.

## Redirect-Konzept

Vor dem Umschalten muss eine vollständige Zuordnung erstellt werden:

```text
alte URL -> neue kanonische URL -> HTTP 301
```

Besonders wichtig sind:

- alle derzeit indexierten DE-URLs,
- alle EN-URLs,
- fehlerhafte doppelte EN-Slugs,
- eventuell umbenannte Leistungsseiten,
- URLs alter Medien/Dokumente, sofern extern verlinkt.

Die Redirect-Liste wird versioniert und vor Go-live gegen den alten Sitemap-/URL-Bestand getestet.

## Migrationsphasen

### Phase 1 – Quellen sichern und inventarisieren

Status: weitgehend abgeschlossen.

Vorhanden:

- Medienoriginale,
- Child-Theme-Reste,
- Plugin-/Theme-Inventar,
- bisherige SEO-/KI-Analyse,
- lokale vollständige SQL-Quelle außerhalb von Git.

Noch fehlend:

- sanitiserter Inhaltsauszug aus WordPress,
- Polylang-Sprachzuordnung,
- vollständige aktuelle URL-Liste,
- relevante SEO-Metadaten pro Seite.

### Phase 2 – Content-Export

Aus dem lokalen SQL-Dump gezielt extrahieren:

- veröffentlichte Seiten,
- Seitentitel,
- Slugs,
- Parent-/Child-Struktur,
- `post_content`,
- relevante `postmeta`,
- Polylang-Sprachinformation,
- Übersetzungsbeziehungen,
- ggf. Yoast Title/Description,
- Medienreferenzen.

Nicht exportieren:

- Benutzer,
- Passwort-Hashes,
- Sessions,
- API-Keys,
- Secrets,
- unnötige Plugin-Konfiguration.

**Dies ist der nächste technische Arbeitsschritt.**

### Phase 3 – Hugo-Grundgerüst

- Hugo-Konfiguration,
- Sprachkonfiguration DE/EN,
- Base-Template,
- Navigation,
- Footer,
- SEO-/Schema-Partials,
- responsive Bild-Pipeline,
- Grund-CSS.

### Phase 4 – Content-Konvertierung

- Avia/Enfold-Inhalt aus den Seiten extrahieren,
- Layout-Shortcodes entfernen,
- fachlichen Inhalt in Markdown überführen,
- Bilder zuordnen,
- Überschriften normalisieren,
- Platzhalter entfernen,
- DE/EN paaren.

LLM-Unterstützung ist hierfür sinnvoll, aber die Transformation bleibt deterministisch prüfbar über Git-Diffs.

### Phase 5 – visuelle Umsetzung

Nicht Enfold technisch kopieren, sondern die bestehende visuelle Identität gezielt neu umsetzen:

- Typografie,
- Grün-/Schwarz-/Weiß-Farbsystem,
- Navigation,
- Hero-Bereiche,
- Leistungsblöcke,
- Bildsprache,
- responsive Verhalten.

### Phase 6 – SEO-/Qualitätssicherung

Automatisierte Checks:

- keine gebrochenen internen Links,
- genau ein redaktionelles H1 je Inhaltsseite,
- Canonical vorhanden,
- hreflang vollständig,
- keine doppelten Canonicals,
- keine leeren relevanten Meta-Descriptions,
- keine falschen Sprachpfade,
- Sitemap enthält nur kanonische URLs,
- strukturierte Daten syntaktisch valide,
- 404-/Redirect-Test gegen Alt-URL-Liste.

### Phase 7 – Deployment

Empfohlenes Modell:

```text
Git
 -> Hugo Build
 -> statisches public/
 -> Webserver
```

Kein PHP und keine Datenbank im Produktivbetrieb erforderlich.

## Offener Punkt: Redaktion

Für die Architektur ist noch zu entscheiden, wie Inhalte später gepflegt werden:

1. Git/Markdown + LLM/IDE – technisch am einfachsten und sehr gut versionierbar.
2. optional später ein Git-basiertes CMS/Editor-Frontend für nichttechnische Redakteure.

Die Hugo-Struktur sollte so gebaut werden, dass Option 2 später ergänzt werden kann, ohne das Content-Modell zu ändern.

## Bewertung

Die bisherigen Quellen bestätigen die Architekturentscheidung:

**Hugo + eigene Templates + Markdown/strukturierte Daten + minimales Vanilla JS ist für bloecher.de das passende Zielbild.**

Die Migration ist zusätzlich günstiger als zunächst angenommen, weil in den gesicherten Child-Themes praktisch keine individuelle WordPress-Programmlogik steckt. Die eigentliche Aufgabe besteht damit vor allem aus:

1. sauberer Content-Extraktion,
2. Entkopplung von Avia/Enfold,
3. Definition eines stabilen Content- und URL-Modells,
4. visueller Neuabbildung,
5. Redirect-/SEO-Sicherung.

Der unmittelbar nächste Schritt ist der **sanitisierte Content-/Polylang-Export aus dem lokalen SQL-Dump**.
