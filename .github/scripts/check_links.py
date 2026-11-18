#!/usr/bin/env python3
"""Fail when a link into this repository points at a missing file or heading.

The docs link to each other with absolute GitHub URLs, so a renamed file or
heading breaks them silently. External links are not checked on purpose: they
fail on network hiccups and would make the required check flaky.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = "github.com/schedjoules/calendar-store-api"
LINK = re.compile(r"https?://" + re.escape(REPO) + r"(?:/(?:blob|edit|tree)/[^/\s)#]+)?/?([^\s)#'\"`]*)(?:#([^\s)'\"`]+))?")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")


def slug(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.strip().lower().replace("`", "")
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(path):
    seen, result = {}, set()
    in_code = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        m = None if in_code else HEADING.match(line)
        if not m:
            continue
        base = slug(m.group(1))
        n = seen.get(base, 0)
        seen[base] = n + 1
        result.add(base if n == 0 else f"{base}-{n}")
    result.update(re.findall(r'<a\s+(?:name|id)="([^"]+)"', path.read_text(encoding="utf-8")))
    return result


errors = []
for md in sorted(ROOT.rglob("*.md")):
    if ".git" in md.parts:
        continue
    for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
        for m in LINK.finditer(line):
            target_rel, fragment = m.group(1).rstrip("/"), m.group(2)
            target = ROOT / target_rel if target_rel else ROOT / "README.md"
            where = f"{md.relative_to(ROOT)}:{lineno}"
            if not target.exists():
                errors.append(f"{where}: {m.group(0)} -> missing file {target_rel}")
            elif fragment and target.is_file() and fragment.lower() not in anchors(target):
                errors.append(f"{where}: {m.group(0)} -> no heading #{fragment} in {target.relative_to(ROOT)}")

for e in errors:
    print(e)
print(f"{len(errors)} broken internal link(s)")
sys.exit(1 if errors else 0)
