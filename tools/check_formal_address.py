#!/usr/bin/env python3
"""Fail when informal German direct address appears in public Hugo copy."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "hugo")

TARGETS = [
    *ROOT.glob("content/de/**/*.md"),
    ROOT / "i18n/de.toml",
]

PATTERNS = [
    re.compile(r"\bdu\b", re.IGNORECASE),
    re.compile(r"\bdich\b", re.IGNORECASE),
    re.compile(r"\bdir\b", re.IGNORECASE),
    re.compile(r"\bdein(?:e|er|em|en|es)?\b", re.IGNORECASE),
    re.compile(r"\beuch\b", re.IGNORECASE),
    re.compile(r"\beuer(?:e|er|em|en|es)?\b", re.IGNORECASE),
    re.compile(r"\b(?:kannst|findest|erfährst|erreichst|möchtest|willst|hast|bist)\b", re.IGNORECASE),
]

violations: list[str] = []

for path in TARGETS:
    if not path.exists():
        continue
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if any(pattern.search(line) for pattern in PATTERNS):
            violations.append(f"{path}:{number}: {line.strip()}")

if violations:
    print("Informelle Du-Ansprache in deutscher Website gefunden:")
    print("\n".join(violations))
    print("\nVorgabe: deutsche Website durchgängig in der Sie-Form.")
    raise SystemExit(1)

print("OK: keine informelle Du-Ansprache in deutschem Hugo-Content gefunden.")
