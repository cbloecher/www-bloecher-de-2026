# Avia-/Enfold-Inventar für die Migration

**Stand:** 18.09.2026  
**Quelle:** 34 veröffentlichte Seiten aus dem sanitisierten WordPress-Export.

## Befund

Der Seiteninhalt ist stark mit Avia Layout Builder / Enfold-Shortcodes durchsetzt. Das ist erwartbar und kein Grund, Enfold technisch zu übernehmen.

Die Migration sollte den **fachlichen Inhalt und die semantische Funktion** der Komponenten extrahieren, nicht deren Shortcode-Struktur 1:1 nachbauen.

## Häufigste relevante Avia-Bausteine

| Shortcode | Vorkommen | Ziel in Hugo/HTML |
|---|---:|---|
| `av_heading` | 107 | H1/H2/H3 anhand Inhalt und Seitengliederung |
| `av_hr` | 69 | meist Layout-Dekoration; häufig entfallen |
| `av_textblock` | 46 | Markdown/HTML-Fließtext |
| `av_cell` | 41 | responsive Grid/Section |
| `av_image` | 39 | responsive-image Partial |
| `av_one_third` | 35 | Grid-Spalte |
| `av_one_full` | 28 | Section/Container |
| `av_section` | 22 | Section |
| `av_one_half` | 20 | Grid-Spalte |
| `av_icon_box` | 19 | Feature-/Info-Card |
| `av_timeline_item` | 17 | Timeline/Listenelement |
| `av_two_third` | 17 | Grid-Spalte |
| `av_icongrid_item` | 16 | Card/Grid-Item |
| `av_contact_field` | 16 | Formularfeld; separat neu umsetzen |
| `av_one_fifth` | 16 | Grid-Spalte |
| `av_cell_one_fourth` | 16 | Grid-Spalte |
| `av_font_icon` | 11 | Icon, nur übernehmen wenn semantisch nötig |
| `av_row` | 11 | Grid-Zeile |
| `av_one_fourth` | 8 | Grid-Spalte |
| `av_layout_row` | 6 | Section/Grid |
| `av_submenu_item` | 6 | Navigation/Ankerlinks |
| `av_gallery` | 5 | Galerie-Komponente |
| `av_icongrid` | 4 | Card/Grid |
| `av_contact` | 4 | Kontaktformular, nicht als Shortcode migrieren |
| `av_submenu` | 3 | lokale Navigation |
| `av_timeline` | 3 | Timeline |
| `av_table` | 3 | semantische HTML-Tabelle |
| `av_fullscreen_slide` | 3 | Hero/Slider; Slider-Nutzen kritisch prüfen |

Weitere seltene Avia-Komponenten kommen vor (Tabs, Toggles, Charts, Masonry, Portfolio, Testimonials usw.). Gerade auf den beiden DEMO-CB-Seiten ist ein Teil davon nur Demonstrationsinhalt und für die echte Migration irrelevant.

## Konvertierungsstrategie

### 1. Semantik zuerst

Beispiel:

```text
[av_heading ...]
```

wird nicht mechanisch zu einem Hugo-Shortcode `heading`, sondern zu normalem Markdown/HTML:

```markdown
## Überschrift
```

### 2. Layout vereinfachen

Avia-Spalten wie:

```text
av_one_third
av_two_third
av_one_half
av_cell
```

werden nur dort als explizite Layout-Komponente erhalten, wo die visuelle Gruppierung inhaltlich sinnvoll ist.

Standard-Fließtext wird nicht unnötig mit Hugo-Shortcodes umhüllt.

### 3. Wiederverwendbare fachliche Komponenten

Nur wiederkehrende sinnvolle Muster bekommen Hugo-Partials/Shortcodes, z. B.:

- Hero
- Fact Grid
- Feature Cards
- Bilder/Galerien
- CTA
- Timeline
- Kontaktblock
- technische Datentabelle

### 4. Formulare

`av_contact` / `av_contact_field` werden nicht konvertiert.

Für die statische Zielseite braucht es eine bewusste neue Lösung, z. B.:

- Mail-Link/Telefon als einfachste Variante,
- externer Formular-Endpunkt,
- kleiner eigener Backend-Endpunkt.

Das ist eine separate Architekturentscheidung.

### 5. Bilder

`av_image` wird auf die bereinigten Originalmedien gemappt.

Hugo erzeugt daraus bei Build-Zeit responsive Varianten und moderne Formate. Die entfernten WordPress-Thumbnails werden nicht rekonstruiert.

## Automatisierbarkeit

Die Migration lässt sich zu großen Teilen automatisieren:

1. Shortcodes tokenisieren/parsen.
2. Textblöcke und Überschriften extrahieren.
3. Bild-IDs/URLs auf Medienoriginale mappen.
4. bekannte Layout-Komponenten in eine vereinfachte Zwischenstruktur überführen.
5. daraus Markdown + Front Matter erzeugen.
6. schwierige/seltene Komponenten als Review-Marker ausgeben.

Wichtig: Nicht mit Regex allein die komplette verschachtelte Avia-Struktur "wegstrippen". Für verschachtelte Shortcodes ist ein kleiner Parser bzw. Stack-basierter Tokenizer robuster.

## Geplanter Konverter

Empfohlene Pipeline:

```text
wordpress-content.json
        ↓
Avia tokenizer/parser
        ↓
normalized page AST
        ↓
rules
 ├─ heading → heading
 ├─ textblock → markdown/html
 ├─ image → image reference
 ├─ section/grid → structural grouping
 └─ unknown → review marker
        ↓
content/de + content/en
```

Unbekannte oder nicht sicher konvertierbare Elemente werden nicht still verworfen, sondern als Review-Marker dokumentiert.

## Priorität der Implementierung

1. `av_heading`
2. `av_textblock`
3. `av_image`
4. `av_section`, `av_one_full`
5. Grid-Spalten
6. Icon-/Feature-Boxen
7. Tabellen
8. Timeline
9. Galerie
10. Sonderkomponenten

Damit lässt sich der Großteil der echten Inhaltsseiten bereits automatisch in einen reviewbaren Hugo-Rohstand überführen.
