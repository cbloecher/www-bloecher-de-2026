# Bildmigrationsmatrix WordPress → Hugo/Pico Corp

**Stand:** 21.09.2026  
**Branch:** `theme-pico-corp`  
**Quelle:** WordPress-Export und gesicherter Medienbestand unter `migration-source/wordpress/wp-content/uploads/`

## Ergebnis

Die fachlich relevanten Bilder des bisherigen Webauftritts sind in Hugo übernommen und den DE-/EN-Seiten zugeordnet. Hugo verarbeitet die Originaldateien beim Build responsiv zu WebP-Varianten mit `srcset`, Bildmaßen und Lazy Loading.

| Bereich | DE/EN | Status | Umsetzung |
|---|---|---|---|
| Startseite | ja | vollständig | Gebäude-/Gießereimotiv als Hero |
| Leistungen | ja | vollständig | Leitbild plus 8 historische Leistungs-/Prozessmotive; generischer WordPress-Platzhalter bewusst entfernt |
| Aluminium-Sandguss | ja | vollständig | Leitbild plus 8 Originalmotive |
| Modellbau | ja | vollständig | Originalmotiv |
| 3D-Sanddruck | ja | vollständig | Originalmotiv |
| Temperierung | ja | fachlich ersetzt | Gesichertes Temperierungsmotiv; das referenzierte Schweißbild fehlt im Medienbestand |
| 3D-Scannen | ja | vollständig | Handscanner als Leitbild plus GOM-Ölwanne |
| Werkzeuge + Formen | ja | vollständig | ursprüngliches Bodenwerkzeug plus 9 historische Galeriemotive |
| Prototypen + Ersatzteile | ja | vollständig | Leitbild plus 5 Prozess- und 9 Bauteilmotive |
| Unternehmen | ja | vollständig | Gebäude-/Standortmotiv |
| Qualität/Zertifizierung | ja | vollständig | Messtechnik als Leitbild plus ISO-Zertifikat |
| Anfahrt | ja | vollständig | historische Anfahrtsskizze |
| Jobs | nur DE | vollständig | historisches Gebäudebild |
| Kontakt | ja | bewusst bildlos | direkte Kontaktfunktion hat Vorrang |
| Impressum/Datenschutz | nur DE | bewusst bildlos | keine dekorativen Bilder |
| Weitere Leistungen & Technologien | nur DE | bewusst bildlos | Inhalt ist noch redaktionell zu klären |

## Bewusste Abweichungen

- `placeholder.jpg` aus der früheren Leistungsübersicht wird nicht übernommen, da es kein fachliches Bild ist.
- Das in WordPress referenzierte Bild `giesserei-bloecher_schweissen_temperierung-edelstahl.jpg` ist im gesicherten Upload-Bestand nicht vorhanden. Das bereits vorhandene Bild `giesserei-bloecher_temperierung.jpg` bleibt als fachlich passende Ersatzquelle.
- WordPress-Thumbnails wie `-180x180` und `-212x300` werden nicht übernommen. Hugo verwendet die gesicherten Originaldateien und berechnet die benötigten Ausgabegrößen selbst.

## Technische Prüfung

- Bilder liegen unter `hugo/assets/images/`.
- Galerien verwenden `bloecher-gallery` mit individuellem Alt-Text und sichtbarer Bildunterschrift.
- Verarbeitung erfolgt über das Pico-Corp-Partial `utils/image.html`.
- Erwartete Build-Ausgabe: WebP, responsive Breiten, `srcset`, intrinsische Maße und Lazy Loading.
