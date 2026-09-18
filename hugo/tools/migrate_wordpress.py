#!/usr/bin/env python3
"""
Initial WordPress/Avia -> Hugo importer for bloecher.de.

Source:
  ../migration-source/export/wordpress-content.json

Output:
  content/de/
  content/en/
  assets/images/imported/

The importer is intentionally conservative:
- maps known WordPress pages to stable Hugo paths
- preserves migration provenance in front matter
- extracts readable text/headings from common Avia shortcodes
- emits REVIEW markers for content that still contains unsupported Avia structures
- copies original source images, not WordPress thumbnail derivatives

Run from hugo/:
  python3 tools/migrate_wordpress.py
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
DEFAULT_SOURCE = REPO / "migration-source" / "export" / "wordpress-content.json"
UPLOADS = REPO / "migration-source" / "wordpress" / "wp-content" / "uploads"

PAGE_MAP = {
    3529: ("de", "_index.md", "home"),
    3994: ("en", "_index.md", "home"),

    3476: ("de", "unternehmen/_index.md", "company"),
    3975: ("en", "about-us/_index.md", "company"),
    3604: ("de", "unternehmen/kontakt.md", "contact"),
    3989: ("en", "about-us/contact-us.md", "contact"),
    3728: ("de", "unternehmen/zertifizierung.md", "quality"),
    3985: ("en", "about-us/quality-management.md", "quality"),
    3526: ("de", "unternehmen/anfahrt.md", "directions"),
    4014: ("en", "about-us/how-to-find-us.md", "directions"),

    3501: ("de", "leistungen/_index.md", "services"),
    4017: ("en", "services/_index.md", "services"),
    3616: ("de", "leistungen/aluminium-sandguss.md", "aluminium-sand-casting"),
    4022: ("en", "services/aluminium-sand-casting.md", "aluminium-sand-casting"),
    3655: ("de", "leistungen/modellbau.md", "model-making"),
    4026: ("en", "services/model-making.md", "model-making"),
    3652: ("de", "leistungen/3d-druck.md", "3d-print"),
    4024: ("en", "services/3d-print.md", "3d-print"),
    3725: ("de", "leistungen/temperierung.md", "temperature-control"),
    4028: ("en", "services/temperature-control.md", "temperature-control"),
    3835: ("de", "leistungen/3d-scannen.md", "3d-scan"),
    4030: ("en", "services/3d-scan.md", "3d-scan"),
    3465: ("de", "leistungen/technologie.md", "technology"),

    3660: ("de", "prototypen-ersatzteil.md", "prototypes-spares"),
    4033: ("en", "prototypes-and-spare-parts.md", "prototypes-spares"),
    3664: ("de", "guss-fuer-werkzeuge-formen.md", "tools-molds"),
    4036: ("en", "tools-and-molds.md", "tools-molds"),

    3461: ("de", "jobs.md", "jobs"),
    3480: ("de", "impressum.md", "legal-notice"),
    3485: ("de", "datenschutzerklaerung.md", "privacy"),
}

SKIP_IDS = {
    3737,  # DEMO-CB: gb-Elemente
    3278,  # DEMO-CB: Mediaelemente
}

REVIEW_IDS = {
    3307, 3495,  # Ersatzteile nach Bedarf: redaktionelle Entscheidung offen
}

TITLE_OVERRIDES = {
    3529: "Giesserei Blöcher",
    3994: "Giesserei Blöcher",
}

DESCRIPTION_OVERRIDES = {
    3529: "Aluminium-Sandguss, Modellbau und 3D-gedruckte Formen und Kerne.",
    3994: "Aluminium sand casting, model making and 3D-printed molds and cores.",
}

EXTRA_ASSETS = [
    "2020/06/logo_gb_340x156_transparent.png",
    "2020/06/logo_giesserei-bloecher_340x156_white.png",
    "2020/06/favicon_32x32.png",
    "2023/11/giesserei-bloecher_gebaeude_breit.jpg",
]

SHORTCODE_TAG_RE = re.compile(r"\[/?av_[^\]]+\]", re.I | re.S)
WP_COMMENT_RE = re.compile(r"<!--\s*/?wp:[^>]*-->", re.I)
HTML_TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"[ \t]+")
BLANK_RE = re.compile(r"\n{3,}")

HEADING_RE = re.compile(
    r"\[av_heading\b(?P<attrs>[^\]]*)\](?P<body>.*?)\[/av_heading\]",
    re.I | re.S,
)
TEXTBLOCK_RE = re.compile(
    r"\[av_textblock\b[^\]]*\](?P<body>.*?)\[/av_textblock\]",
    re.I | re.S,
)
IMAGE_RE = re.compile(r"\[av_image\b(?P<attrs>[^\]]*)\]", re.I | re.S)
ATTR_RE = re.compile(r"([A-Za-z0-9_-]+)=(?:'([^']*)'|\"([^\"]*)\")")


def attrs(text: str) -> dict[str, str]:
    result = {}
    for m in ATTR_RE.finditer(text):
        result[m.group(1)] = m.group(2) if m.group(2) is not None else m.group(3)
    return result


def clean_inline(value: str) -> str:
    value = html.unescape(value or "")
    value = HTML_TAG_RE.sub("", value)
    value = value.replace("\r", "")
    value = SPACE_RE.sub(" ", value)
    return value.strip()


def html_to_markdownish(value: str) -> str:
    value = WP_COMMENT_RE.sub("", value or "")
    value = html.unescape(value)
    value = re.sub(r"<\s*br\s*/?\s*>", "\n", value, flags=re.I)
    value = re.sub(r"</p\s*>", "\n\n", value, flags=re.I)
    value = re.sub(r"<p\b[^>]*>", "", value, flags=re.I)
    value = re.sub(r"<strong\b[^>]*>(.*?)</strong>", r"**\1**", value, flags=re.I | re.S)
    value = re.sub(r"<b\b[^>]*>(.*?)</b>", r"**\1**", value, flags=re.I | re.S)
    value = re.sub(r"<em\b[^>]*>(.*?)</em>", r"*\1*", value, flags=re.I | re.S)
    value = re.sub(r"<i\b[^>]*>(.*?)</i>", r"*\1*", value, flags=re.I | re.S)
    value = re.sub(
        r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>",
        lambda m: f"[{clean_inline(m.group(2))}]({m.group(1)})",
        value,
        flags=re.I | re.S,
    )
    value = HTML_TAG_RE.sub("", value)
    value = value.replace("\r", "")
    value = BLANK_RE.sub("\n\n", value)
    return value.strip()


def extract_content(raw: str) -> tuple[str, list[str]]:
    review = []
    work = WP_COMMENT_RE.sub("", raw or "")

    # Preserve text blocks first.
    work = TEXTBLOCK_RE.sub(lambda m: "\n\n" + html_to_markdownish(m.group("body")) + "\n\n", work)

    # Convert headings using explicit tag when available.
    def heading_replace(m):
        a = attrs(m.group("attrs"))
        title = clean_inline(a.get("heading") or m.group("body"))
        tag = (a.get("tag") or "h2").lower()
        level = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}.get(tag, 2)
        return "\n\n" + ("#" * level) + " " + title + "\n\n"

    work = HEADING_RE.sub(heading_replace, work)

    # Images are mapped later; leave a visible migration marker for review.
    def image_replace(m):
        a = attrs(m.group("attrs"))
        attachment = a.get("attachment") or a.get("id") or ""
        src = a.get("src") or ""
        review.append(f"image:{attachment or src or 'unknown'}")
        return "\n\n<!-- MIGRATION-REVIEW image " + (attachment or src or "unknown") + " -->\n\n"

    work = IMAGE_RE.sub(image_replace, work)

    # Remove remaining Avia wrappers/tags but never silently claim full conversion.
    remaining = sorted(set(re.findall(r"\[/?(av_[A-Za-z0-9_:-]+)", work, flags=re.I)))
    if remaining:
        review.extend(f"shortcode:{x}" for x in remaining)

    work = SHORTCODE_TAG_RE.sub("\n", work)
    work = html_to_markdownish(work)
    work = BLANK_RE.sub("\n\n", work).strip()

    return work, sorted(set(review))


def yaml_quote(value) -> str:
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def front_matter(page: dict, translation_key: str, review: list[str]) -> str:
    meta = page.get("meta") or {}
    page_id = int(page["id"])
    title = TITLE_OVERRIDES.get(page_id, page.get("title", ""))
    desc = DESCRIPTION_OVERRIDES.get(page_id, meta.get("_yoast_wpseo_metadesc") or "")
    seo_title = meta.get("_yoast_wpseo_title") or ""

    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        f"description: {yaml_quote(desc)}",
        f"translationKey: {yaml_quote(translation_key)}",
        "draft: false",
        "migration:",
        f"  wordpress_id: {int(page['id'])}",
        f"  source_url: {yaml_quote(page.get('url', ''))}",
        f"  source_slug: {yaml_quote(page.get('slug', ''))}",
        f"  modified: {yaml_quote(page.get('modified', ''))}",
    ]

    if seo_title or desc:
        lines.extend([
            "seo:",
            f"  title: {yaml_quote(seo_title)}",
            f"  description: {yaml_quote(desc)}",
        ])

    if review:
        lines.append("migration_review:")
        for item in review:
            lines.append(f"  - {yaml_quote(item)}")

    lines.append("---")
    return "\n".join(lines) + "\n"


def copy_images(data: dict) -> int:
    dest_root = ROOT / "assets" / "images" / "imported"
    copied = 0
    for a in data.get("attachments", []):
        rel = a.get("relative_upload_path")
        if not rel:
            continue
        src = UPLOADS / rel
        if not src.is_file():
            continue
        dest = dest_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied += 1

    for rel in EXTRA_ASSETS:
        src = UPLOADS / rel
        if not src.is_file():
            continue
        dest = dest_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            shutil.copy2(src, dest)
            copied += 1

    return copied


def migrate(source: Path) -> None:
    data = json.loads(source.read_text(encoding="utf-8"))
    pages = {int(p["id"]): p for p in data.get("pages", [])}

    written = 0
    review_count = 0

    for page_id, page in pages.items():
        if page_id in SKIP_IDS:
            continue

        if page_id in REVIEW_IDS:
            print(f"[REVIEW] page {page_id}: {page.get('title')} – no target path assigned")
            review_count += 1
            continue

        mapping = PAGE_MAP.get(page_id)
        if not mapping:
            print(f"[REVIEW] unmapped page {page_id}: {page.get('title')} {page.get('url')}")
            review_count += 1
            continue

        lang, relpath, translation_key = mapping
        body, review = extract_content(page.get("content_raw") or "")

        target = ROOT / "content" / lang / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(front_matter(page, translation_key, review) + "\n" + body + "\n", encoding="utf-8")
        written += 1
        if review:
            review_count += 1

    copied = copy_images(data)

    print(f"[OK] Hugo content files written: {written}")
    print(f"[OK] Referenced original images copied: {copied}")
    print(f"[INFO] Pages/files requiring migration review: {review_count}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs="?", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()

    if not args.source.is_file():
        raise SystemExit(f"Source JSON not found: {args.source}")

    migrate(args.source)


if __name__ == "__main__":
    main()
