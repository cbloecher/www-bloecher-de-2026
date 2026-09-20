# Changelog – Theme Pico Corp

Stand: 20.09.2026  
Branch: `theme-pico-corp`  
Upstream: [PhantomPixelDev/hugo-theme-pico-corp](https://github.com/PhantomPixelDev/hugo-theme-pico-corp)

## Leitlinie

Pico Corp bleibt ein extern eingebundenes Upstream-Theme. Anpassungen erfolgen bevorzugt über Hugo-Konfiguration, Content/Front Matter, i18n und `assets/css/custom.css`. Template-Overrides werden nur eingesetzt, wenn sich eine Anforderung auf diesen Ebenen nicht robust lösen lässt.

## Upstream-Basis

- Theme-Commit festgesetzt auf `7b43e743259f6b9e61a2a8195bf3aa723df6954e`.
- `hugo/tools/setup-pico-corp-theme.sh` lädt exakt diesen Commit.
- Damit sind lokale Builds und GitHub-Pages-Builds reproduzierbar.
- Ein Upstream-Update erfolgt künftig bewusst durch Änderung von `THEME_REF` und anschließende Prüfung.

## Hugo-Konfiguration

- Blöcher-Orange `#ed9c10` als Primärfarbe.
- Heller Modus fest eingestellt; Theme-Umschalter deaktiviert.
- Ecken über `radius = "0rem"` bewusst kantig.
- Systemnahe Sans-Serif-Typografie.
- Logo, Firma, Anschrift, Telefon und E-Mail eingetragen.
- DE als Standardsprache unter `/`, EN unter `/en/`.
- Sprachabhängige Footer-Texte ergänzt.
- Footer-Navigation für Leistungen und Unternehmen in DE und EN ergänzt.
- Rechtliche Footer-Navigation für Impressum und Datenschutz in DE ergänzt.
- Globale aggressive CTA-Blöcke und Header-CTA deaktiviert.
- Analytics nicht konfiguriert; dadurch keine externen Tracking-Requests.

## Inhalte und Startseite

- Kuratierte WordPress-Inhalte bleiben maßgeblich und wurden nicht erneut importiert.
- Hero in DE und EN mit Blöcher-Bild, zurückhaltenden CTAs und technischen Kennzahlen.
- Leistungsübersicht auf der Startseite ergänzt:
  - DE liest aus `/leistungen/`.
  - EN liest aus `/services/`.
- Die DE-/EN-Leistungsübersichten aktivieren über Front Matter `type: "services"` das vorhandene Upstream-Layout `services/section.html`; kein eigener Section-Template-Fork.
- Leistungsseiten besitzen kuratierte `summary`- und `highlights`-Angaben für klar erkennbare, informative Navigationskarten.
- Am Ende jeder Leistungsdetailseite erzeugt der additive Shortcode `bloecher-service-nav` automatisch sprachabhängig denselben Pico-Corp-Leistungsblock wie die Übersicht.
- Die aktuelle Leistung bleibt an ihrer Rasterposition sichtbar, ist ausgegraut und nicht verlinkt; `aria-current="page"` kennzeichnet sie semantisch.

## Gestaltung

Anpassungen liegen in `hugo/assets/css/custom.css`:

- Containerbreite und Abschnittsabstände gemäß Blöcher-Styleguide.
- Systemschrift statt Webfont.
- Weißer, leichter Header mit feiner Trennlinie.
- Logo-Höhe explizit gesetzt, damit das Logo den verfügbaren Headerraum nutzt und lesbar bleibt.
- Orange für Eyebrows und Kennzahlen.
- Keine Karten-Schatten.
- Keine Rundungen bei Buttons und Flächen.
- Ruhige helle Alternativflächen.
- Seitenkopf, Fließtext, Bilder und Leistungsraster verwenden denselben Container und eine durchgängige linke Kante.
- Absätze und Listen bleiben für gute Lesbarkeit auf `50rem` begrenzt; breite Inhaltsblöcke nutzen die verfügbare Containerbreite.
- Responsive Anpassungen für Header, Logo und Hero-Bild.
- Leistungskarten mit orangefarbener Führungslinie, sichtbarem Pfeil sowie klaren Hover- und Tastatur-Fokuszuständen als Navigation hervorgehoben.
- Der Block „Weitere Leistungen“ übernimmt unverändert das responsive Upstream-Raster `grid-auto grid-auto--gap-lg`: drei Spalten auf breiten Ansichten und automatische Reduktion auf kleineren Ansichten.
- Die aktuelle Leistung wird als graue, nicht interaktive Karte mit sprachabhängigem Hinweis „Aktuelle Leistung“/„Current service“ dargestellt.

## Bilder

- Die fünf bereits referenzierten Originalbilder für Sandguss, Modellbau, 3D-Sanddruck, 3D-Scannen und Temperierung aus `migration-source` nach `hugo/assets/images/imported/2023/11/` übernommen.
- Weitere vorhandene Originalbilder den zentralen Seiten für Werkzeuge + Formen, Prototypen + Ersatzteile, Leistungen, Unternehmen und Qualität in DE und EN zugeordnet.
- Darstellung über die responsive Hugo-Bildpipeline von Pico Corp.
- Referenzgalerie für Aluminium-Sandguss in DE und EN mit acht Originalmotiven, individuellen Alt-Texten und sichtbaren Bildunterschriften ergänzt.
- Neuer eigener Shortcode `bloecher-gallery`: nutzt das Pico-Corp-Galerieraster, ohne den unzugänglichen Upstream-Shortcode mit leerem `alt` zu überschreiben.
- Seiten ohne fachlich passendes Motiv bleiben bewusst ohne dekoratives Ersatzbild.

## Übersetzungen

- `hugo/i18n/de.toml` ergänzt.
- Theme-Chrome, Navigation, Footer, Formulare, 404-Seite und weitere UI-Texte sind damit auf Deutsch statt über englische Fallbacks verfügbar.

## GitHub Pages

- Workflow um Checkout, Theme-Setup und Build von `theme-pico-corp` ergänzt.
- Ausgabe erfolgt unter `/pico-corp/`.
- Pushes auf `theme-pico-corp` lösen Build und Validierung aus; veröffentlicht wird wegen der GitHub-Pages-Umgebung ausschließlich aus `main`.
- Der zuvor statisch auf `https://hugo.bloecher.de/sitemap.xml` festgelegte `robots.txt` wurde entfernt. Hugo erzeugt ihn nun passend zur jeweiligen Build-`baseURL`.

## Gezielt begründeter Template-Override

Datei: `hugo/layouts/_markup/render-link.html`

Zweck:

- Kuratierte Inhalte enthalten root-relative Markdown-Links wie `/leistungen/3d-druck/`.
- Solche Links würden in der GitHub-Pages-Vorschau den Unterpfad `/pico-corp/` verlieren.
- Der Override ergänzt bei internen root-relativen Markdown-Links die jeweils aktive Hugo-`baseURL`.
- Externe Links und das übrige Upstream-Verhalten bleiben unverändert.

Zweiter gezielter Override: `hugo/layouts/_partials/page-header.html`.

- Pico Corp rendert das bereits kuratierte Front-Matter-Feld `hero.image` auf normalen Inhalts- und Bereichsseiten nicht.
- Der Override übernimmt den unveränderten Upstream-Seitenkopf und ergänzt darunter ein responsives Bild über die vorhandene Theme-Bildpipeline.
- WebP, `srcset`, intrinsische Bildmaße und Alt-Texte bleiben damit Aufgabe des Themes.

Damit bestehen derzeit genau zwei kleine Pico-Corp-Template-Overrides.

## Offene Punkte

1. Sichtbare DE/EN-Sprachumschaltung; Pico Corp bringt dafür aktuell keine fertige Komponente mit.
2. Englische Fassungen von Impressum und Datenschutz fehlen im Content.
3. Reihenfolge, Zusammenfassungen und Bildzuschnitte der Leistungskarten fachlich und visuell prüfen.
4. Kontaktseiten und deaktivierten Formularzustand abschließend gestalten.
5. OpenGraph-Standardbild, Favicons und Organization-Schema vervollständigen.
6. Accessibility-Prüfung mit Tastatur, Kontrasttest und automatisiertem Audit.
7. Responsive Sichtprüfung auf kleinen Mobilgeräten, Tablet und breitem Desktop.
8. Verbleibendes Bildinventar und mobile Zuschnitte im visuellen Review prüfen.
