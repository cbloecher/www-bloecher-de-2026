#!/usr/bin/env python3
"""Crawl the legacy and Hugo websites and create a reproducible content comparison."""

from __future__ import annotations

import argparse
import concurrent.futures
import difflib
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
    "/leistungen/technologie/": None,
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--old", default=DEFAULT_OLD)
    parser.add_argument("--new", default=DEFAULT_NEW)
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
