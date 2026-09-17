# SEO- & KI-Aufbereitung – Analyse www.bloecher.de

**Datum:** 17.09.2026  
**Geprüfte Domain:** https://www.bloecher.de  
**Basis:** WordPress, „Google Sitemap Generator“-Plugin

## Zusammenfassung

Die Website ist technisch grundsätzlich gut erreichbar und liefert verwertbaren, serverseitig ausgelieferten Fließtext. Es besteht also kein grundlegendes Rendering- oder Crawlability-Problem.

Die wesentlichen Defizite liegen vielmehr in der **technischen und semantischen Aufbereitung der vorhandenen Inhalte**:

- generische bzw. nicht gepflegte Meta-Daten,
- fehlende strukturierte Daten,
- uneindeutige Überschriftenhierarchien,
- fehlerhafte URL-Strukturen auf englischen Seiten,
- fehlende bzw. schwache Bildbeschreibungen,
- teilweise noch öffentlich sichtbare Platzhalterinhalte.

Für klassische Suchmaschinen und KI-gestützte Such- und Antwortsysteme ist damit bereits brauchbares Rohmaterial vorhanden, die Inhalte werden jedoch nicht so eindeutig strukturiert und ausgezeichnet, wie es möglich wäre.

Das zentrale Ziel sollte deshalb nicht nur „SEO“ sein, sondern eine **saubere, maschinenlesbare Wissensstruktur** der Website: Was fertigt Blöcher? Mit welchen Verfahren, Werkstoffen, Abmessungen und Losgrößen? Für welche Anwendungen? Mit welchen Qualitäts- und Prüfverfahren? Wo befindet sich das Unternehmen und wie ist es erreichbar?

---

## Positive Ausgangslage

Mehrere wichtige Grundlagen funktionieren bereits und sollten beibehalten werden:

- Die Seiten liefern echten Fließtext direkt im HTML; kein relevantes JavaScript-Rendering-Problem wurde festgestellt.
- Unterseiten enthalten bereits umfangreichen fachlichen Inhalt; beispielsweise umfasst `/leistungen/` rund 800–900 Wörter.
- `robots.txt` blockiert keine wesentlichen Inhalte und verweist auf die Sitemap.
- Ein Sitemap-Index ist vorhanden; `page-sitemap.xml` listet rund 31 URLs.
- Auf der Startseite ist ein Canonical-Tag vorhanden.
- Ein Favicon ist eingerichtet.
- Auf Leistungsseiten stehen bereits konkrete, für Suchmaschinen und KI-Systeme gut nutzbare Fakten, z. B. zu:
  - Aluminium-Sandguss,
  - Bauteilgewichten bis ca. 2.500 kg,
  - Größenordnungen bis etwa 6 m³,
  - kleinen Losgrößen,
  - 3D-gedruckten Formen und Kernen,
  - Temperierungen und weiteren Fertigungsmöglichkeiten.

Damit besteht kein grundsätzliches Content-Defizit. Der Schwerpunkt sollte auf **Struktur, Eindeutigkeit, Qualitätssicherung und technischer Kennzeichnung** liegen.

---

## Befunde

### 1. Title & Meta-Description – hohe Priorität

Auf den geprüften Seiten entspricht die Meta-Description weitgehend dem Title-Tag und folgt einem offensichtlich generischen WordPress-/Plugin-Muster:

- Startseite: `Startseite-DE - Giesserei Blöcher GmbH`
- Leistungen: `Leistungen - Giesserei Blöcher GmbH`
- EN-Startseite: `Startseite-EN - Giesserei Blöcher GmbH`

Diese Texte beschreiben weder Inhalt noch Nutzen der jeweiligen Seite. Zentrale Suchbegriffe und Differenzierungsmerkmale fehlen, beispielsweise:

- Aluminium-Sandguss,
- Biedenkopf / Hessen,
- Bauteilgrößen bzw. Gewichtsbereich,
- Prototypen / Kleinserien,
- 3D-gedruckte Formen und Kerne.

### Bewertung

Title und Meta-Description sollten für jede relevante Seite individuell gepflegt werden. Die Meta-Description ist zwar kein direkter Ranking-Faktor, beeinflusst aber die Darstellung und Verständlichkeit eines Suchtreffers und kann damit die Klickrate verbessern.

---

### 2. Keine strukturierten Daten / Schema.org – hohe Priorität

Auf der geprüften Startseite wurde kein JSON-LD mit strukturierten Unternehmensdaten gefunden.

Für Blöcher bieten sich insbesondere an:

- `Organization` bzw. ein geeigneter `LocalBusiness`-Typ,
- Name,
- postalische Adresse,
- Telefonnummer,
- Website,
- Logo,
- ggf. Öffnungs-/Geschäftszeiten,
- Verknüpfungen zu relevanten Unternehmensprofilen,
- auf Leistungsseiten ggf. passende `Service`-Informationen.

### Bewertung

Strukturierte Daten helfen Suchmaschinen und anderen maschinellen Systemen, Fakten über Unternehmen und Leistungen eindeutig zu interpretieren. Sie sind jedoch **kein Garant** für Rich Results, Knowledge Panels oder die Zitierung durch KI-Systeme.

Der Nutzen liegt primär in der eindeutigen, standardisierten Bereitstellung ohnehin vorhandener Fakten.

---

### 3. Überschriftenstruktur semantisch uneindeutig – mittlere bis hohe Priorität

Auf `/leistungen/` wurden mehrere H1-Überschriften gefunden, unter anderem:

- „Übersicht Leistungen“
- „Von Ihren CAD Daten zum fertigen Abguss“
- „IHR SPEZIALIST FÜR ANSPRUCHSVOLLEN ALUMINIUM SANDGUSS“

Zusätzlich wirkt die Hierarchie aus H1/H2/H3/H4 teilweise uneinheitlich bzw. versprungen.

### Bewertung

Mehrere H1-Tags sind in modernem HTML **nicht automatisch ein SEO-Fehler**. Problematisch ist hier vielmehr, dass das Hauptthema und die inhaltliche Gliederung für Mensch und Maschine nicht eindeutig genug abgebildet werden.

Empfehlung:

- pro Seite ein klar erkennbares Hauptthema,
- eine konsistente Hierarchie H1 → H2 → H3,
- Überschriften nach inhaltlicher Bedeutung und nicht nach gewünschter Schriftgröße verwenden.

Eine einzelne H1 pro Seite ist als redaktioneller Standard weiterhin sinnvoll, sollte aber nicht als technische SEO-Pflicht formuliert werden.

---

### 4. Fehlerhafte URL-Struktur bei englischen Seiten – sehr hohe Priorität

In `page-sitemap.xml` wurden englische URLs mit doppelten Slugs gefunden, beispielsweise:

- `https://www.bloecher.de/en/foundry//foundry`
- `https://www.bloecher.de/en/services/3d-print//3d-print`
- `https://www.bloecher.de/en/about-us/quality-management//quality-management`

Diese URLs liefern HTTP 200 statt auf eine eindeutige Ziel-URL weiterzuleiten oder einen Fehlerstatus zurückzugeben.

Dadurch können mehrere URLs inhaltlich dieselbe Seite repräsentieren und Duplicate-Content-Situationen entstehen.

Zusätzlich wurden in der Stichprobe keine sauberen `hreflang`-Verknüpfungen zwischen deutschen und englischen Seiten gefunden; `og:locale` ersetzt `hreflang` nicht.

### Empfehlung

- Ursache im Mehrsprachigkeits-/Routing-Setup ermitteln,
- doppelte URL-Strukturen entfernen,
- alte/falsche URLs permanent auf die kanonische URL umleiten,
- Sitemap bereinigen,
- Canonical-Tags aller betroffenen Seiten prüfen,
- DE-/EN-Seiten über korrekte `hreflang`-Tags miteinander verknüpfen.

---

### 5. Öffentlich sichtbare Platzhaltertexte – hohe Priorität

Auf `/leistungen/` wurden mehrfach offensichtlich nicht finalisierte Inhalte wie

> „Gib hier den Inhalt des Meilensteines“

gefunden.

### Bewertung

Dies ist weniger ein klassisches SEO-Problem als ein unmittelbares Qualitätsproblem. Solche Texte sollten vollständig entfernt oder durch fachliche Inhalte ersetzt werden.

Sie schwächen:

- Nutzervertrauen,
- Content-Qualität,
- semantische Eindeutigkeit,
- die Qualität maschineller Zusammenfassungen.

---

### 6. Bilder teilweise ohne sinnvolle Alt-Texte – mittlere Priorität

In einer Stichprobe auf der Startseite wurden mehrere leere `alt=""`-Attribute gefunden. Vereinzelt vorhandene Alt-Texte wirken eher wie Dateinamen, beispielsweise:

`giesserei-bloecher_gebäude_breit`

### Bewertung

Nicht jedes Bild benötigt zwingend einen beschreibenden Alt-Text: rein dekorative Bilder sollten bewusst ein leeres `alt=""` besitzen. Inhaltlich relevante Bilder sollten dagegen eine kurze, konkrete Beschreibung bekommen.

Alt-Texte dienen vor allem:

- Barrierefreiheit,
- semantischer Einordnung von Bildern,
- Bildersuche.

Empfehlung: Bilder zuerst in **dekorativ** und **inhaltstragend** klassifizieren und nur für letztere sinnvolle Beschreibungen pflegen.

---

### 7. Kein `llms.txt` – niedrige / experimentelle Priorität

`https://www.bloecher.de/llms.txt` liefert aktuell 404.

### Bewertung

`llms.txt` ist derzeit ein experimenteller Ansatz und kein etablierter SEO-Standard. Seine praktische Nutzung durch relevante KI-Anbieter ist uneinheitlich. Das Fehlen sollte deshalb **nicht als kritischer Fehler** gewertet werden.

Falls eine Datei angelegt wird, sollte sie als ergänzender maschinenlesbarer Einstieg dienen, z. B. mit:

- Kurzbeschreibung des Unternehmens,
- Kernkompetenzen,
- wichtigsten Leistungsseiten,
- Werkstoffen,
- Fertigungsgrenzen,
- Qualitäts-/Zertifizierungsinformationen,
- Ansprechpartner-/Kontaktseite.

Wichtiger als `llms.txt` bleiben jedoch sauberer HTML-Inhalt, eindeutige URLs, interne Verlinkung, strukturierte Daten und konsistente Unternehmensinformationen.

---

## Übergreifende Bewertung für KI-Suchsysteme

Für ChatGPT, Perplexity, Google AI Overviews und ähnliche Systeme existiert kein einzelner „KI-SEO“-Schalter.

Eine gute technische und redaktionelle Grundlage entsteht vor allem durch:

1. eindeutige Fakten im normalen HTML,
2. logisch gegliederte Seiten,
3. stabile und kanonische URLs,
4. maschinenlesbare strukturierte Daten,
5. präzise Seitentitel und Überschriften,
6. gute interne Verlinkung,
7. konsistente Unternehmensinformationen,
8. externe Erwähnungen und fachliche Autorität.

Für Blöcher ist besonders wertvoll, technische Aussagen möglichst konkret zu formulieren.

Statt nur:

> „Wir fertigen anspruchsvolle Gussteile.“

sind beispielsweise Aussagen wie

> „Aluminium-Sandguss für Einzelteile, Prototypen und Kleinserien bis ca. 2.500 kg Bauteilgewicht.“

für Menschen, Suchmaschinen und KI-Systeme wesentlich eindeutiger.

---

## Empfohlene Wissensstruktur

Die Website sollte zentrale Unternehmensfakten möglichst explizit und konsistent beantworten können:

### Unternehmen

- Wer ist Giesserei Blöcher?
- Wo befindet sich das Unternehmen?
- Seit wann besteht das Unternehmen?
- Welche Branchen werden beliefert?

### Verfahren

- Aluminium-Sandguss
- Modell-/Werkzeugbau
- 3D-gedruckte Formen und Kerne
- mechanische Bearbeitung bzw. verfügbare Folgeprozesse
- Wärmebehandlung / Temperierung, soweit angeboten

### Leistungsgrenzen

- mögliche Bauteilgewichte,
- maximale Abmessungen bzw. Volumen,
- typische Losgrößen,
- verfügbare Legierungen,
- erreichbare Toleranzen,
- Oberflächen,
- Lieferzustände.

### Qualität

- Zertifizierungen,
- Prüfverfahren,
- Messmöglichkeiten,
- Dokumentation / Rückverfolgbarkeit.

### Beschaffung / Anfrage

- Welche CAD-Daten werden akzeptiert?
- Welche Angaben werden für eine Anfrage benötigt?
- Wie läuft ein Projekt von CAD-Daten bis zum Gussteil ab?

Eine solche Struktur eignet sich gleichzeitig als Grundlage für Navigation, Landingpages, FAQ-Inhalte, strukturierte Daten und ggf. eine spätere `llms.txt`.

---

## Priorisierte Maßnahmen

### Priorität 1 – technische und sichtbare Fehler beseitigen

1. Fehlerhafte EN-URLs korrigieren.
2. Redirects, Canonicals und Sitemap danach bereinigen.
3. `hreflang` für DE/EN korrekt einrichten.
4. Öffentliche Platzhaltertexte entfernen.

### Priorität 2 – Seitenthemen und Snippets sauber definieren

5. Für jede Kernseite individuellen Title definieren.
6. Für jede Kernseite eine eigene Meta-Description schreiben.
7. Hauptthema und Suchintention jeder Seite eindeutig festlegen.

### Priorität 3 – semantische Inhaltsstruktur verbessern

8. Überschriftenhierarchie H1/H2/H3 bereinigen.
9. Kernaussagen und technische Leistungsdaten explizit ausformulieren.
10. Interne Verlinkung zwischen Verfahren, Anwendungen, Werkstoffen und Qualität verbessern.

### Priorität 4 – strukturierte Daten

11. `Organization` / geeigneten `LocalBusiness`-Typ als JSON-LD einführen.
12. Leistungen ggf. zusätzlich mit `Service`-Daten beschreiben.
13. Unternehmensdaten zwischen Website und externen Profilen konsistent halten.

### Priorität 5 – Medien und Barrierefreiheit

14. Bilder in dekorativ / inhaltstragend klassifizieren.
15. Für inhaltstragende Bilder aussagekräftige Alt-Texte pflegen.

### Priorität 6 – KI-spezifische Ergänzungen testen

16. Optional eine kompakte `llms.txt` bereitstellen.
17. Wirkung und tatsächlichen Nutzen beobachten, statt sie als zwingende Voraussetzung zu behandeln.

---

## Methodik

Geprüft wurden am 17.09.2026 unter anderem:

- Startseite,
- `robots.txt`,
- `sitemap.xml`,
- `page-sitemap.xml`,
- `llms.txt`,
- `/leistungen/`,
- eine englische Beispielseite.

Betrachtet wurden unter anderem:

- HTTP-Erreichbarkeit,
- Title,
- Meta-Description,
- `html lang`,
- Viewport,
- Canonical,
- Open-Graph-Daten,
- JSON-LD / strukturierte Daten,
- H1/H2/H3/H4-Struktur,
- Bild-Alt-Attribute,
- serverseitige bzw. JavaScript-basierte Content-Auslieferung,
- URL-Strukturen und Sitemap-Einträge.

Die Analyse ist eine technische und redaktionelle Stichprobe und ersetzt keinen vollständigen Crawl aller URLs sowie keine Auswertung aus Google Search Console, Bing Webmaster Tools oder Webserver-Logs.

---

## Nächste sinnvolle Vertiefung

Auf Basis dieser Analyse bietet sich als nächster Schritt eine **Soll-Struktur pro Kernseite** an. Für jede Seite können dabei definiert werden:

- Seitenthema / Suchintention,
- Ziel-URL,
- Title,
- Meta-Description,
- H1,
- H2-Struktur,
- zentrale Fakten,
- interne Links,
- Schema.org-Auszeichnung.

Damit entsteht aus der Analyse ein direkt umsetzbarer Arbeitsplan für WordPress und Redaktion.
