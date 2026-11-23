#!/usr/bin/env python3
"""Crawl the legacy and Hugo websites and create a reproducible content comparison."""

from __future__ import annotations

import argparse
import concurrent.futures
import difflib
import html
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


DEFAULT_OLD = "https://www.bloecher.de"
DEFAULT_NEW = "https://cbloecher.github.io/www-bloecher-de-2026/pico-corp"

# Explicit mappings document renamed and translated routes. Unlisted routes are
# matched by their normalized path when possible.
PATH_MAP = {
    "/": "/",
    "/ersatzteile-nach-bedarf-de/": "/ersatzteile-nach-bedarf/",
    "/jobs/": "/jobs/",
    "/leistungen/": "/leistungen/",
    "/leistungen/technologie/": "/leistungen/",
    "/leistungen/aluminium-sandguss/": "/leistungen/aluminium-sandguss/",
    "/leistungen/3d-druck/": "/leistungen/3d-druck/",
    "/leistungen/modellbau/": "/leistungen/modellbau/",
    "/leistungen/temperierung/": "/leistungen/temperierung/",
    "/leistungen/3d-scannen/": "/leistungen/3d-scannen/",
    "/prototypen-ersatzteil/": "/prototypen-ersatzteil/",
    "/guss-fuer-werkzeuge-formen/": "/guss-fuer-werkzeuge-formen/",
    "/unternehmen/": "/unternehmen/",
    "/unternehmen/anfahrt/": "/unternehmen/anfahrt/",
    "/unternehmen/kontakt/": "/unternehmen/kontakt/",
    "/unternehmen/zertifizierung/": "/unternehmen/zertifizierung/",
    "/impressum/": "/impressum/",
    "/datenschutzerklaerung/": "/datenschutzerklaerung/",
    "/en/foundry/": "/en/",
    "/en/about-us/": "/en/about-us/",
    "/en/about-us/quality-management/": "/en/about-us/quality-management/",
    "/en/about-us/contact-us/": "/en/about-us/contact-us/",
    "/en/about-us/how-to-find-us/": "/en/about-us/how-to-find-us/",
    "/en/services/": "/en/services/",
    "/en/services/aluminium-sandcasting/": "/en/services/aluminium-sand-casting/",
    "/en/services/3d-print/": "/en/services/3d-print/",
    "/en/services/model-making/": "/en/services/model-making/",
    "/en/services/temperature-control/": "/en/services/temperature-control/",
    "/en/services/3d-scan/": "/en/services/3d-scan/",
    "/en/prototypes-and-spare-parts/": "/en/prototypes-and-spare-parts/",
    "/en/tools-and-molds/": "/en/tools-and-molds/",
}

SKIP_TAGS = {"script", "style", "svg", "nav", "header", "footer", "form", "noscript"}
TEXT_TAGS = {"title", "h1", "h2", "h3", "p", "li", "address"}
COOKIE_MARKERS = (
    "cookie and privacy", "how we use cookies", "essential website cookies",
    "google webfont settings", "google recaptcha settings", "vimeo and youtube",
    "this site uses cookies", "cookie- und datenschutzeinstellungen",
)


def fetch(url: str, attempts: int = 2) -> bytes:
    request = urllib.request.Request(url, headers={
        "User-Agent": "BloecherSiteCompare/1.0",
        "Accept-Language": "de-DE,de;q=0.9,en;q=0.5",
    })
    error = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                return response.read()
        except Exception as exc:
            error = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Abruf fehlgeschlagen: {url}: {error}")


def sitemap_urls(url: str) -> list[str]:
    root = ET.fromstring(fetch(url))
    local = root.tag.rsplit("}", 1)[-1]
    locations = [node.text.strip() for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "loc" and node.text]
    if local == "sitemapindex":
        urls: list[str] = []
        for child in locations:
            urls.extend(sitemap_urls(child))
        return urls
    return locations


class ContentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.active: str | None = None
        self.buffer: list[str] = []
        self.title = ""
        self.headings: list[str] = []
        self.blocks: list[str] = []
        self.cookie_started = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self.skip_depth += 1
        if not self.skip_depth and tag in TEXT_TAGS:
            self.active = tag
            self.buffer = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self.active == tag:
            text = clean_text(" ".join(self.buffer))
            if any(marker in text.lower() for marker in COOKIE_MARKERS):
                self.cookie_started = True
            if text and not self.cookie_started:
                if tag == "title":
                    self.title = text
                elif tag.startswith("h"):
                    self.headings.append(text)
                    self.blocks.append(text)
                else:
                    self.blocks.append(text)
            self.active = None
            self.buffer = []
        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.active and not self.skip_depth:
            self.buffer.append(data)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def canonical_path(url: str) -> str:
    path = urllib.parse.urlsplit(url).path
    parts = [part for part in path.split("/") if part]
    if len(parts) >= 2 and parts[-1] == parts[-2]:
        parts.pop()
    return "/" + "/".join(parts) + ("/" if parts else "")


@dataclass
class Page:
    url: str
    path: str
    status: str
    title: str = ""
    headings: list[str] | None = None
    blocks: list[str] | None = None
    text: str = ""
    words: int = 0
    error: str | None = None


def crawl(url: str) -> Page:
    path = canonical_path(url)
    try:
        parser = ContentParser()
        parser.feed(fetch(url).decode("utf-8", errors="replace"))
        text = clean_text(" ".join(parser.blocks))
        return Page(url, path, "ok", parser.title, parser.headings, parser.blocks, text, len(text.split()))
    except Exception as exc:
        return Page(url, path, "error", error=str(exc), headings=[], blocks=[])


def content_similarity(left: str, right: str) -> float:
    """Estimate retained vocabulary while tolerating deliberately shorter copy."""
    words = lambda text: set(re.findall(r"[a-zäöüß0-9]{4,}", text.casefold()))
    a, b = words(left), words(right)
    return len(a & b) / min(len(a), len(b)) if a and b else 0.0


def meaningful_blocks(page: Page, other: Page) -> list[str]:
    other_normalized = {clean_text(x).casefold() for x in (other.blocks or [])}
    unique = []
    for block in page.blocks or []:
        normalized = clean_text(block).casefold()
        if len(normalized) < 25 or normalized in other_normalized:
            continue
        best = max((difflib.SequenceMatcher(None, normalized, candidate).ratio() for candidate in other_normalized), default=0)
        if best < 0.72:
            unique.append(block)
    return unique[:8]



def block_similarity(left: str, right: str) -> float:
    """Similarity for aligning editorial text blocks."""
    a = clean_text(left).casefold()
    b = clean_text(right).casefold()
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    char_ratio = difflib.SequenceMatcher(None, a, b).ratio()
    words = lambda text: set(re.findall(r"[a-zäöüß0-9]{3,}", text))
    wa, wb = words(a), words(b)
    vocabulary_ratio = len(wa & wb) / min(len(wa), len(wb)) if wa and wb else 0.0
    return max(char_ratio, vocabulary_ratio)


def align_blocks(old_blocks: list[str], new_blocks: list[str]) -> list[dict]:
    """Order-preserving block alignment for the visual diff."""
    old_blocks = old_blocks or []
    new_blocks = new_blocks or []
    n, m = len(old_blocks), len(new_blocks)
    gap = -0.35
    threshold = 0.45

    dp = [[0.0] * (m + 1) for _ in range(n + 1)]
    back = [[""] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = i * gap
        back[i][0] = "old"
    for j in range(1, m + 1):
        dp[0][j] = j * gap
        back[0][j] = "new"

    similarities = [[block_similarity(old_blocks[i], new_blocks[j]) for j in range(m)] for i in range(n)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            similarity = similarities[i - 1][j - 1]
            match_score = similarity * 1.4 if similarity >= threshold else -0.8
            choices = (
                (dp[i - 1][j - 1] + match_score, "match"),
                (dp[i - 1][j] + gap, "old"),
                (dp[i][j - 1] + gap, "new"),
            )
            dp[i][j], back[i][j] = max(choices, key=lambda item: item[0])

    aligned: list[dict] = []
    i, j = n, m
    while i or j:
        step = back[i][j]
        if step == "match":
            similarity = similarities[i - 1][j - 1]
            kind = "unchanged" if similarity >= 0.88 else "changed"
            aligned.append({
                "kind": kind,
                "old": old_blocks[i - 1],
                "new": new_blocks[j - 1],
                "similarity": round(similarity, 3),
            })
            i -= 1
            j -= 1
        elif step == "old":
            aligned.append({"kind": "missing", "old": old_blocks[i - 1], "new": "", "similarity": 0})
            i -= 1
        else:
            aligned.append({"kind": "new", "old": "", "new": new_blocks[j - 1], "similarity": 0})
            j -= 1

    aligned.reverse()
    return aligned


def render_diff_html(result: dict) -> str:
    comparisons = result["comparisons"]
    page_sections = []
    toc_entries = []
    totals = {"missing": 0, "new": 0, "changed": 0, "unchanged": 0}

    for index, item in enumerate(comparisons, start=1):
        old = item.get("old")
        new = item.get("new")
        old_path = old["path"] if old else "–"
        new_path = new["path"] if new else "–"
        rows = align_blocks((old or {}).get("blocks") or [], (new or {}).get("blocks") or [])
        counts = {key: sum(row["kind"] == key for row in rows) for key in totals}
        for key in totals:
            totals[key] += counts[key]

        anchor = f"seite-{index}"
        label = old_path if old else new_path
        toc_entries.append(
            f'<li><a href="#{anchor}"><span>{html.escape(label)}</span>'
            f'<small>{counts["missing"]} fehlt · {counts["new"]} neu · {counts["changed"]} geändert</small></a></li>'
        )

        old_link = (
            f'<a href="{html.escape(old["url"], quote=True)}" target="_blank" rel="noopener">{html.escape(old_path)}</a>'
            if old else "–"
        )
        new_link = (
            f'<a href="{html.escape(new["url"], quote=True)}" target="_blank" rel="noopener">{html.escape(new_path)}</a>'
            if new else "–"
        )

        row_html = []
        for row in rows:
            kind = row["kind"]
            old_text = html.escape(row["old"])
            new_text = html.escape(row["new"])
            if kind == "missing":
                label_html = '<span class="diff-label">fehlt in Neu</span>'
            elif kind == "new":
                label_html = '<span class="diff-label">neu</span>'
            elif kind == "changed":
                label_html = f'<span class="diff-label">umformuliert · {row["similarity"]:.0%}</span>'
            else:
                label_html = '<span class="diff-label">inhaltlich gleich</span>'
            row_html.append(
                f'<tr class="{kind}"><td>{label_html}<div>{old_text or "—"}</div></td>'
                f'<td>{label_html}<div>{new_text or "—"}</div></td></tr>'
            )

        page_sections.append(f"""
<section class="page-diff" id="{anchor}">
  <div class="page-heading">
    <div>
      <p class="eyebrow">Seitenvergleich {index}</p>
      <h2>{html.escape(old_path)} <span>→</span> {html.escape(new_path)}</h2>
    </div>
    <div class="page-meta">
      <span class="status">{html.escape(item["status"])}</span>
      <span>Gesamtähnlichkeit {item.get("similarity", 0):.0%}</span>
    </div>
  </div>
  <div class="source-links"><strong>Alt:</strong> {old_link} <strong>Neu:</strong> {new_link}</div>
  <div class="mini-stats">
    <span class="missing">{counts["missing"]} fehlt</span>
    <span class="new">{counts["new"]} neu</span>
    <span class="changed">{counts["changed"]} umformuliert</span>
    <span class="unchanged">{counts["unchanged"]} gleich</span>
  </div>
  <div class="table-wrap">
    <table class="diff-table">
      <thead><tr><th>Alt</th><th>Neu / Hugo</th></tr></thead>
      <tbody>{''.join(row_html)}</tbody>
    </table>
  </div>
</section>
""")

    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Inhaltsvergleich Alt ↔ Neu · Giesserei Blöcher</title>
<style>
:root {{
  --bg:#f5f6f8; --surface:#fff; --text:#1b1f24; --muted:#667085; --line:#dfe3e8;
  --blue:#e8f1ff; --blue-border:#3b82f6; --red:#fff0f0; --red-border:#d92d20;
  --green:#edf9f0; --green-border:#179c52; --grey:#f6f7f8;
}}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
body {{ margin:0; font:15px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; background:var(--bg); color:var(--text); }}
a {{ color:#155eef; }}
.layout {{ display:grid; grid-template-columns:minmax(250px,320px) minmax(0,1fr); min-height:100vh; }}
aside {{ position:sticky; top:0; align-self:start; height:100vh; overflow:auto; padding:24px 20px; background:#111827; color:white; }}
aside h1 {{ margin:0 0 6px; font-size:20px; }}
aside p {{ margin:0 0 18px; color:#cbd5e1; font-size:13px; }}
aside ol {{ list-style:none; padding:0; margin:0; }}
aside li {{ margin:0 0 4px; }}
aside a {{ display:block; padding:8px 10px; border-radius:7px; color:white; text-decoration:none; }}
aside a:hover {{ background:#273449; }}
aside small {{ display:block; color:#94a3b8; font-size:11px; margin-top:2px; }}
main {{ padding:32px clamp(18px,3vw,48px) 80px; max-width:1500px; width:100%; }}
.intro,.page-diff {{ background:var(--surface); border:1px solid var(--line); border-radius:12px; box-shadow:0 1px 2px rgb(0 0 0 / 4%); }}
.intro {{ padding:24px; margin-bottom:28px; }}
.intro h1 {{ margin:0 0 8px; }}
.legend {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:18px; }}
.legend span,.mini-stats span {{ border-left:4px solid; padding:5px 8px; border-radius:4px; background:var(--grey); }}
.legend .missing,.mini-stats .missing {{ border-color:var(--red-border); background:var(--red); }}
.legend .new,.mini-stats .new {{ border-color:var(--green-border); background:var(--green); }}
.legend .changed,.mini-stats .changed {{ border-color:var(--blue-border); background:var(--blue); }}
.legend .unchanged,.mini-stats .unchanged {{ border-color:#98a2b3; }}
.controls {{ margin-top:18px; }}
.page-diff {{ padding:24px; margin:0 0 28px; scroll-margin-top:20px; }}
.page-heading {{ display:flex; gap:20px; justify-content:space-between; align-items:flex-start; }}
.page-heading h2 {{ margin:0; font-size:21px; overflow-wrap:anywhere; }}
.page-heading h2 span {{ color:var(--muted); }}
.eyebrow {{ margin:0 0 4px; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; font-size:11px; font-weight:700; }}
.page-meta {{ display:flex; flex-direction:column; align-items:flex-end; gap:5px; color:var(--muted); font-size:12px; white-space:nowrap; }}
.status {{ padding:2px 7px; background:var(--grey); border-radius:999px; }}
.source-links {{ margin:13px 0; display:flex; gap:8px; flex-wrap:wrap; align-items:center; color:var(--muted); }}
.mini-stats {{ display:flex; gap:8px; flex-wrap:wrap; margin:12px 0 18px; font-size:12px; }}
.table-wrap {{ overflow-x:auto; }}
.diff-table {{ width:100%; border-collapse:collapse; table-layout:fixed; }}
.diff-table th {{ text-align:left; padding:9px 12px; border-bottom:2px solid var(--line); }}
.diff-table td {{ vertical-align:top; width:50%; padding:10px 12px; border-bottom:1px solid var(--line); overflow-wrap:anywhere; }}
.diff-table tr.changed td {{ background:var(--blue); border-left:3px solid var(--blue-border); }}
.diff-table tr.missing td:first-child {{ background:var(--red); border-left:3px solid var(--red-border); }}
.diff-table tr.missing td:last-child {{ background:#fffafa; color:#98a2b3; }}
.diff-table tr.new td:last-child {{ background:var(--green); border-left:3px solid var(--green-border); }}
.diff-table tr.new td:first-child {{ background:#fbfffc; color:#98a2b3; }}
.diff-table tr.unchanged td {{ color:#667085; background:#fafafa; }}
.diff-label {{ display:inline-block; margin-bottom:5px; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:.04em; color:#475467; }}
body.hide-unchanged tr.unchanged {{ display:none; }}
@media (max-width:900px) {{
  .layout {{ display:block; }}
  aside {{ position:relative; height:auto; }}
  aside ol {{ columns:2; }}
  .page-heading {{ display:block; }}
  .page-meta {{ align-items:flex-start; margin-top:10px; }}
}}
@media (max-width:640px) {{
  aside ol {{ columns:1; }}
  main {{ padding:18px 10px 50px; }}
  .page-diff,.intro {{ padding:16px; }}
  .diff-table {{ table-layout:auto; min-width:760px; }}
}}
</style>
</head>
<body>
<div class="layout">
<aside>
  <h1>Alt ↔ Neu</h1>
  <p>Inhaltsverzeichnis · {html.escape(result["generated"])}</p>
  <ol>{''.join(toc_entries)}</ol>
</aside>
<main>
  <section class="intro">
    <h1>Inhaltsvergleich bisherige Website ↔ Hugo</h1>
    <p>Die Zuordnung erfolgt blockweise und reihenfolgetreu. Farben dienen der redaktionellen Prüfung und sind keine Qualitätsbewertung.</p>
    <div class="legend">
      <span class="missing"><strong>Rot:</strong> Altinhalt fehlt in Neu</span>
      <span class="new"><strong>Grün:</strong> neuer Inhalt in Hugo</span>
      <span class="changed"><strong>Blau:</strong> zugeordnete Passage wurde umformuliert</span>
      <span class="unchanged"><strong>Grau:</strong> weitgehend unverändert</span>
    </div>
    <div class="controls"><label><input type="checkbox" id="toggle-unchanged"> Unveränderte Passagen ausblenden</label></div>
    <p><strong>Gesamt:</strong> {totals["missing"]} fehlt · {totals["new"]} neu · {totals["changed"]} umformuliert · {totals["unchanged"]} weitgehend gleich.</p>
  </section>
  {''.join(page_sections)}
</main>
</div>
<script>
document.getElementById("toggle-unchanged").addEventListener("change", function () {{
  document.body.classList.toggle("hide-unchanged", this.checked);
}});
</script>
</body>
</html>
"""

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--old", default=DEFAULT_OLD)
    parser.add_argument("--new", default=DEFAULT_NEW)
    parser.add_argument("--new-display", default=None, help="Public base URL used in generated links when --new points to a local build.")
    parser.add_argument("--output", default="Analyse/site-vergleich")
    args = parser.parse_args()

    old_urls = sitemap_urls(args.old.rstrip("/") + "/sitemap.xml")
    new_urls = sitemap_urls(args.new.rstrip("/") + "/sitemap.xml")
    filtered_new_urls = [url for url in new_urls if "/categories/" not in url and "/tags/" not in url]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        old_pages = list(pool.map(crawl, old_urls))
        new_pages = list(pool.map(crawl, filtered_new_urls))
    old_by_path = {page.path: page for page in old_pages if page.path != "/sitemap.html/"}
    new_by_path = {}
    for page in new_pages:
        relative_path = canonical_path(page.url.replace(args.new.rstrip("/"), "", 1) or "/")
        page.path = relative_path
        if args.new_display:
            page.url = args.new_display.rstrip("/") + relative_path
        new_by_path[relative_path] = page

    comparisons = []
    mapped_new: set[str] = set()
    for old_path, old_page in sorted(old_by_path.items()):
        new_path = PATH_MAP.get(old_path, old_path if old_path in new_by_path else None)
        new_page = new_by_path.get(new_path) if new_path else None
        if new_path:
            mapped_new.add(new_path)
        if not new_page:
            comparisons.append({"status": "nur_alt", "old": asdict(old_page), "new": None, "similarity": 0})
            continue
        ratio = content_similarity(old_page.text, new_page.text)
        status = "vergleichbar" if ratio >= 0.55 else "abweichend"
        comparisons.append({
            "status": status,
            "old": asdict(old_page),
            "new": asdict(new_page),
            "similarity": round(ratio, 3),
            "only_old": meaningful_blocks(old_page, new_page),
            "only_new": meaningful_blocks(new_page, old_page),
        })
    for new_path, new_page in sorted(new_by_path.items()):
        if new_path not in mapped_new:
            comparisons.append({"status": "nur_hugo", "old": None, "new": asdict(new_page), "similarity": 0})

    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    result = {"generated": generated, "old_base": args.old, "new_base": args.new, "comparisons": comparisons}
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "vergleich.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "index.html").write_text(render_diff_html(result), encoding="utf-8")

    counts = {key: sum(item["status"] == key for item in comparisons) for key in ("vergleichbar", "abweichend", "nur_alt", "nur_hugo")}
    lines = [
        "# Seiten- und Inhaltsvergleich bloecher.de ↔ Hugo", "",
        f"Erzeugt: `{generated}`", "",
        "Dieser Bericht wird mit `python tools/compare_websites.py` reproduzierbar erzeugt. "
        "Der Ähnlichkeitswert ist ein Hinweis für die redaktionelle Prüfung, keine semantische Bewertung.", "",
        "## Übersicht", "",
        f"- Vergleichbar: **{counts['vergleichbar']}**",
        f"- Inhaltlich auffällig: **{counts['abweichend']}**",
        f"- Nur auf der alten Website: **{counts['nur_alt']}**",
        f"- Nur in Hugo: **{counts['nur_hugo']}**", "",
        "## Seitenzuordnung", "",
        "| Status | Alt | Hugo | Wörter alt/neu | Ähnlichkeit |", "|---|---|---|---:|---:|",
    ]
    for item in comparisons:
        old = item.get("old")
        new = item.get("new")
        old_link = f"[{old['path']}]({old['url']})" if old else "–"
        new_link = f"[{new['path']}]({new['url']})" if new else "–"
        words = f"{old['words'] if old else 0}/{new['words'] if new else 0}"
        lines.append(f"| {item['status']} | {old_link} | {new_link} | {words} | {item['similarity']:.0%} |")

    lines += ["", "## Auffällige Inhaltsunterschiede", ""]
    for item in comparisons:
        if item["status"] != "abweichend":
            continue
        old, new = item["old"], item["new"]
        lines += [f"### `{old['path']}` → `{new['path']}`", ""]
        if item.get("only_old"):
            lines.append("**Nur/anders auf Alt:** " + " · ".join(item["only_old"]))
            lines.append("")
        if item.get("only_new"):
            lines.append("**Nur/anders in Hugo:** " + " · ".join(item["only_new"]))
            lines.append("")
    (output / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
