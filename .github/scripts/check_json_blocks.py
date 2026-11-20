#!/usr/bin/env python3
"""Fail when a ```json block in the docs does not parse.

Example responses are what readers, and coding agents above all, copy into
their code. Before this check the pages example had unquoted keys, a missing
comma and "......" in place of items, so anything modelled on it was wrong.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLOCK = re.compile(r"^```json\s*\n(.*?)^```", re.M | re.S)

errors = []
count = 0
for md in sorted(ROOT.rglob("*.md")):
    if ".git" in md.parts:
        continue
    text = md.read_text(encoding="utf-8")
    for m in BLOCK.finditer(text):
        count += 1
        line = text.count("\n", 0, m.start()) + 1
        try:
            json.loads(m.group(1))
        except json.JSONDecodeError as e:
            errors.append(f"{md.relative_to(ROOT)}:{line}: invalid JSON: {e}")

for e in errors:
    print(e)
print(f"{count} json block(s), {len(errors)} invalid")
sys.exit(1 if errors else 0)
