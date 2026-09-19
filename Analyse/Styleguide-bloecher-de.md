# Web-Styleguide – Giesserei Blöcher

**Stand:** 19.09.2026  
**Basis:** aktueller Webauftritt `www.bloecher.de`, Live-Snapshot im Repository und daraus abgeleitete Gestaltung für den Hugo-Neuaufbau.

> Dieser Styleguide ist aus dem bestehenden Webauftritt abgeleitet. Er ist kein formales Corporate-Design-Handbuch. Wo der Live-Auftritt keine eindeutige Vorgabe liefert, sind Empfehlungen für den Neuaufbau ausdrücklich als solche formuliert.

---

## 1. Gestaltungscharakter

Die visuelle Sprache von Blöcher ist zurückhaltend, technisch und sachlich.

Kennzeichnend sind:

- viel Weißraum
- überwiegend weiße Flächen
- sehr zurückhaltende Grautöne
- Orange nur als gezielter Akzent
- zentriertes Logo im Header
- horizontale, leichte Navigation
- klare typografische Hierarchie ohne dekorative Schrift
- dünne Linien statt kräftiger Rahmen
- technische Fotografien aus Produktion, Werkzeugbau und Gießerei
- wenig visuelle Effekte
- keine ausgeprägte „App“- oder Dashboard-Anmutung

Der Neuaufbau darf moderner und großzügiger sein, soll aber diese Ruhe beibehalten.

---

## 2. Farben

### 2.1 Direkt aus dem bestehenden Auftritt belegbar

| Rolle | Wert | Verwendung |
| --- | --- | --- |
| Weiß | `#ffffff` | Hauptflächen, Header, Inhalte |
| Hellgrau | `#f8f8f8` | alternative Flächen, dezente Hintergründe |
| Liniengrau | `#f2f2f2` | Trennlinien, dezente Begrenzungen |
| UI-Grau | `#e1e1e1` | Formfelder, Linien, neutrale UI-Elemente |
| Dunkel | `#222222` | Überschriften |
| Text dunkel | `#444444` | Fließtext-Grundton |
| Meta-Grau | `#919191` | sekundäre Information |
| Navigationsgrau | `#c9c9c9` | Header-/Navigationselemente |
| Orange Akzent | `#ed9c10` | explizit im aktuellen Leistungsbereich als Icon-Akzent gesetzt |

Weitere Farbcodes wie `#ffa133` und `#f76700` sind im Enfold-CSS vorhanden, dort aber teilweise für generische Theme-/Social-Komponenten. Sie sollten deshalb nicht automatisch als verbindliche Markenfarben interpretiert werden.

### 2.2 Empfohlenes Hugo-Farbsystem

Für den Neuaufbau wird das bestehende Farbsystem auf wenige semantische Tokens reduziert:

```css
:root {
  --color-brand: #ed9c10;
  --color-text: #444444;
  --color-heading: #222222;
  --color-muted: #919191;
  --color-nav: #c9c9c9;
  --color-line: #e1e1e1;
  --color-line-soft: #f2f2f2;
  --color-surface: #f8f8f8;
  --color-white: #ffffff;
}
```

### Grundregel

**Orange nie als dominante Flächenfarbe einsetzen.**

Orange funktioniert am besten für:

- kleine Marker
- Icons
- Hover-Zustände
- aktive Navigation
- Eyebrows/Kicker
- einzelne Buttons
- technische Kennzahlen oder Akzentlinien

Große orange Flächen sollten die Ausnahme bleiben.

---

## 3. Typografie

### 3.1 Bestehender Auftritt

Der Enfold-Auftritt definiert:

```css
font-family:
  "HelveticaNeue",
  "Helvetica Neue",
  Helvetica,
  Arial,
  sans-serif;
```

Belegte Grundgrößen:

| Element | Live-Wert |
| --- | ---: |
| Fließtext | 13 px |
| H1 | 34 px |
| H2 | 28 px |
| H3 | 20 px |
| H4 | 18 px |
| H5 | 16 px |
| H6 | 14 px |

Der bestehende Auftritt arbeitet damit typografisch eher kompakt.

### 3.2 Empfehlung für Hugo

Die Schriftfamilie bleibt bewusst systemnah:

```css
font-family:
  Arial,
  Helvetica,
  "Helvetica Neue",
  sans-serif;
```

Für heutige Displays und bessere Lesbarkeit darf die Skalierung moderat größer werden:

| Element | Empfehlung |
| --- | --- |
| Fließtext | 16 px |
| kleiner Text | 13–14 px |
| H1 Unterseite | 34–48 px responsiv |
| H2 | 26–36 px responsiv |
| H3 | 20–24 px |
| Navigation | 14–15 px |

### Typografische Regeln

- Überschriften eher **Regular/Normal** als extrem fett.
- Großbuchstaben nur punktuell für Seitentitel/Kicker.
- Keine dekorativen Fonts.
- Keine extrem engen oder stark negativen Laufweiten.
- Fließtextbreite ca. **45–55 rem**.
- Zeilenhöhe Fließtext ca. **1.55–1.7**.

---

## 4. Layout und Breiten

Im bestehenden Theme finden sich Containerbreiten von etwa **1.010 px**; für einzelne Layoutzustände existieren weitere Werte.

Für den Hugo-Neuaufbau:

```css
--content-width: 1130px;
--text-width: 800px;
```

### Grundstruktur

- Seitenrahmen großzügig
- Inhalt nicht über die ganze Viewportbreite ziehen
- Textspalten deutlich schmaler als Bild-/Gridbereiche
- horizontale Trennlinien sparsam einsetzen
- keine dicken Box-Rahmen

### Empfohlene vertikale Abstände

| Kontext | Abstand |
| --- | --- |
| Header → Inhalt | 48–80 px |
| H1 → Lead | 24–32 px |
| Abschnitt → Abschnitt | 56–96 px |
| H2 → Text | 16–24 px |
| Absatz → Absatz | 16–24 px |

---

## 5. Header

Der bestehende Auftritt nutzt:

- Logo zentriert
- Hauptnavigation darunter
- helle/weiße Fläche
- leichte Grautöne
- sehr dezente Trennlinien
- geringe visuelle Schwere

### Empfehlung

Desktop:

```text
              LOGO

Werkzeuge | Prototypen | Leistungen | Jobs | Unternehmen       DE EN
──────────────────────────────────────────────────────────────────
```

Regeln:

- Logo optisch im Mittelpunkt
- Navigation leicht und zurückhaltend
- kein massiver farbiger Header
- Navigation in Grau, Hover/Aktiv in Orange
- maximal eine feine horizontale Linie

Mobile:

- Logo kleiner
- Navigation kompakt bzw. über Menü
- Sprachwahl sichtbar lassen

---

## 6. Seitentitel und Hierarchie

### H1

- genau ein H1 pro Seite
- Seitenthema, keine dekorative Wiederholung
- auf Unterseiten zentriert
- viel Weißraum
- optional kleiner Kicker darüber
- darunter feine Linie statt farbiger Balken

Beispiel:

```text
LEISTUNGEN

ALUMINIUM-SANDGUSS
──────────────────
```

### H2

H2 gliedern fachliche Hauptblöcke, z. B.:

- Leistungsumfang
- Verfahren
- Anwendungen
- Technische Grenzen
- Qualität
- Vorteile

### H3

Nur für echte Untergliederungen, z. B.:

- Prozessschritte
- Varianten
- einzelne Verfahrensstufen

**Keine Überschrift nur aus Layoutgründen.**

---

## 7. Navigation innerhalb eines Themenbereichs

Der bestehende Auftritt kennt horizontale Subnavigationen.

Für Hugo wird dieses Muster beibehalten:

```text
Aluminium-Sandguss · Temperierung · Modellbau · 3D-Sanddruck · 3D-Scannen
```

Regeln:

- eine Zeile, wenn möglich
- horizontal scrollbar auf kleinen Displays
- Schrift kleiner als Hauptnavigation
- Grau im Normalzustand
- Orange bei Hover/Aktiv
- keine großen Tabs oder gefüllten Buttons

---

## 8. Buttons und Links

### Textlinks

- normal im Textfluss
- Akzentfarbe Orange oder dunkles Grau
- Hover sichtbar, aber nicht aufdringlich
- Unterstreichung bei längeren Textlinks bevorzugt

### Primärer Button

Empfehlung:

- orange Fläche
- weiße Schrift
- keine starke Rundung
- eher rechteckig
- kompakte Höhe

### Sekundärer Button

- transparenter Hintergrund
- dünne Linie
- dezenter Hover

### Nicht verwenden

- starke Schatten
- Pill-Buttons
- Neonfarben
- übertriebene Gradients
- viele konkurrierende CTA-Farben

---

## 9. Karten und Übersichten

Der bestehende Blöcher-Stil ist **nicht card-lastig**.

Für Übersichtsseiten daher:

- Karten nur, wenn sie Informationsstruktur verbessern
- viel Weißraum
- dünne obere oder untere Linie
- keine schweren Rahmen
- keine starken Schatten
- keine großen Radien
- Icons/Bilder klein und funktional einsetzen

Geeignet:

```text
01
ALUMINIUM-SANDGUSS
Einzelteile, Prototypen und Kleinserien …
─────────────────────────────────────
```

Nicht passend:

- Dashboard-Kacheln
- Glas-/Blur-Effekte
- große farbige Flächen pro Karte

---

## 10. Bilder

Die bestehende Website nutzt überwiegend echte technische Fotos:

- Gießerei
- Modellbau
- Sanddruck
- Werkzeuge
- Gussteile
- 3D-Scanning
- Gebäude

### Bildsprache

- reale Fertigung statt Stockfotografie
- technisch, glaubwürdig, sachlich
- Werkstück oder Prozess im Mittelpunkt
- möglichst wenig dekorative Inszenierung

### Darstellung

- große Bilder dürfen 16:9 oder breitformatig sein
- technische Detailbilder auch quadratisch möglich
- kein übermäßiger Radius
- keine starken Schatten
- Alt-Texte beschreiben Motiv/Funktion, nicht „Bild von …“

Hugo soll responsive Varianten und WebP erzeugen.

---

## 11. Startseite

Die Startseite darf moderner sein als die historischen Unterseiten.

Beibehalten:

- großes reales Produktions-/Gebäudebild
- klare Hauptaussage
- Aluminium-Sandguss sofort erkennbar
- wenige technische Kennzahlen
- drei bis fünf Kernkompetenzen
- direkter Kontakt

Nicht überladen:

- keine langen Textblöcke
- keine zehn verschiedenen Module
- keine Animation als Selbstzweck

### Hero

```text
ALUMINIUM-SANDGUSS

Wir formen Zukunft.
Stück für Stück.

Anspruchsvolle Gussteile, Prototypen und Kleinserien …
```

Hero-Text weiß auf Foto mit dunkler, ruhiger Überlagerung.

Orange kann als Kicker und CTA eingesetzt werden.

---

## 12. Tabellen und technische Daten

Technische Daten sollen funktional wirken.

- keine Vollflächen-Raster
- horizontale Linien
- linksbündige Inhalte
- Header leicht hervorgehoben
- Einheiten immer mit Wert zusammen darstellen

Beispiel:

| Kurzbezeichnung | Norm | Hinweis |
| --- | --- | --- |
| 226 | EN-AC46200 | Universallegierung |
| UFO90 | G-Al Zn10 Si8 Mg | selbstaushärtend |

---

## 13. Tonalität im Inhalt

Die bestehende Marke kommuniziert eher technisch als werblich.

### Bevorzugt

- konkrete technische Aussagen
- Maße, Gewichte und Verfahren
- verständliche Beschreibung von Prozess und Nutzen
- kurze, sachliche Sätze
- „wir“ dort, wo eigene Leistung beschrieben wird

### Vermeiden

- Superlative ohne Nachweis
- Marketingfloskeln
- künstlich emotionale Sprache
- generische KI-Texte
- lange Erklärungen ohne Bezug zur eigenen Leistung

---

## 14. Responsive Verhalten

Grundprinzip:

**Desktop-Identität erhalten, mobil vereinfachen.**

- Header vertikal kompakter
- horizontale Navigationslisten scrollbar oder als Menü
- Inhalte einspaltig
- Bilder volle Text-/Inhaltsbreite
- Tabellen bei Bedarf horizontal scrollbar
- Buttons auf kleinen Displays ggf. volle Breite

Breakpoint als Ausgangspunkt:

```css
@media (max-width: 52rem) { ... }
```

---

## 15. Design-Tokens für Hugo

Empfohlener kompakter Ausgangspunkt:

```css
:root {
  --content-width: 70.625rem;
  --text-width: 50rem;

  --brand: #ed9c10;

  --heading: #222222;
  --text: #444444;
  --muted: #919191;
  --nav: #c9c9c9;

  --line: #e1e1e1;
  --line-soft: #f2f2f2;
  --surface: #f8f8f8;
  --white: #ffffff;

  --space-xs: .5rem;
  --space-sm: 1rem;
  --space-md: 2rem;
  --space-lg: 4rem;
  --space-xl: 6rem;
}
```

---

## 16. Entscheidungsregeln

Bei neuen Komponenten gilt:

1. **Ist sie notwendig?**
2. **Kann sie mit Weißraum und Typografie statt Boxen gelöst werden?**
3. **Ist Orange nur Akzent und nicht Selbstzweck?**
4. **Bleibt die technische Information im Vordergrund?**
5. **Passt die Komponente zu Logo, Navigation und bestehender Bildsprache?**
6. **Funktioniert sie ohne Animation und JavaScript?**
7. **Ist die semantische HTML-Struktur auch ohne CSS verständlich?**

---

## 17. Kurzform

Die Blöcher-Websprache lässt sich auf folgende Formel reduzieren:

> **Weißraum + technische Klarheit + Grau + gezieltes Orange + echte Fertigungsbilder.**

Der Hugo-Neuaufbau soll diese Identität bewahren, dabei aber Typografie, Responsive Design, semantische Struktur und technische Umsetzung modernisieren.
