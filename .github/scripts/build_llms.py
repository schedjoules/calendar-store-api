#!/usr/bin/env python3
"""Build llms.txt and llms-full.txt from the docs, or check they are current.

    python3 .github/scripts/build_llms.py           # write both files
    python3 .github/scripts/build_llms.py --check   # fail if either is stale

llms.txt is a short index (https://llmstxt.org) linking to the raw markdown of
every page. llms-full.txt is every page joined into one file, so a coding agent
can read the whole API in one fetch. Both are generated from PAGES below, so a
new page under details/ fails the check until it is listed here.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = "https://raw.githubusercontent.com/schedjoules/calendar-store-api/master/"

# (path, title, one-line description), in reading order.
PAGES = [
    ("README.md", "Overview", "Authentication, request basics, language, pages, the user identifier, caching"),
    ("details/pages.md", "Pages", "The page response: sections, page items and calendar items, every field"),
    ("details/calendars.md", "Calendars", "Calendar feeds: formats, date range, results, incremental updates, sport results"),
    ("details/user_input_calendars.md", "Pregnancy and Countdown Calendars", "Calendar URLs your app fills in with a due date or a countdown"),
    ("details/weather.md", "Weather", "The weather calendar template, units, city search and map locations"),
    ("details/alarms.md", "Alarms", "Default alarms per calendar type and the al parameter"),
    ("details/search.md", "Search", "Free-text search with country, category, sport and gender filters"),
    ("details/top_new_next.md", "Top, New, Next", "Popular, recently updated and starting-soon lists"),
    ("details/countries.md", "Countries", "Supported countries, their ids, codes, home pages and translations"),
    ("details/languages.md", "Languages", "The 18 supported languages"),
    ("details/accounts.md", "In-app Purchases and Accounts", "Registering a user's license expiration"),
    ("details/sdks.md", "SDKs (deprecated)", "The iOS and Android SDKs and the Swift client are deprecated; integrate the REST API directly"),
    ("details/deprecation_and_changes.md", "Deprecations and Changes", "What changed and what is planned"),
    ("details/faq.md", "FAQ", "Content coverage, languages, data usage"),
]

SUMMARY = (
    "REST API (JSON over HTTPS) for public calendars: holidays, sports, TV, weather, finance "
    "and more. Clients browse pages of calendars and subscribe users to calendar feed URLs "
    "(iCalendar, jCal or xCal). Every request needs an `Authorization: Token token=\"...\"` header."
)


def index():
    lines = ["# SchedJoules Calendar Service API", "", f"> {SUMMARY}", "", "## Docs", ""]
    lines += [f"- [{title}]({RAW}{path}): {desc}" for path, title, desc in PAGES]
    lines += ["", "## Optional", "", f"- [All docs in one file]({RAW}llms-full.txt)", ""]
    return "\n".join(lines)


def full():
    parts = [f"# SchedJoules Calendar Service API\n\n> {SUMMARY}\n\n"
             "Generated from the markdown files in this repository by .github/scripts/build_llms.py. "
             "Do not edit by hand.\n"]
    for path, title, _ in PAGES:
        text = (ROOT / path).read_text(encoding="utf-8").strip()
        parts.append(f"\n\n<!-- source: {path} -->\n\n{text}\n")
    return "".join(parts)


def main():
    errors = []
    listed = {p for p, _, _ in PAGES}
    for md in sorted((ROOT / "details").glob("*.md")):
        rel = md.relative_to(ROOT).as_posix()
        if rel not in listed:
            errors.append(f"{rel} is not listed in PAGES in .github/scripts/build_llms.py")
    for path in listed:
        if not (ROOT / path).exists():
            errors.append(f"{path} is listed in PAGES but does not exist")
    if errors:
        print("\n".join(errors))
        return 1

    wanted = {"llms.txt": index(), "llms-full.txt": full()}
    if "--check" in sys.argv:
        stale = [name for name, text in wanted.items()
                 if not (ROOT / name).exists() or (ROOT / name).read_text(encoding="utf-8") != text]
        for name in stale:
            print(f"{name} is out of date: run python3 .github/scripts/build_llms.py and commit it")
        return 1 if stale else 0
    for name, text in wanted.items():
        (ROOT / name).write_text(text, encoding="utf-8")
    return 0


sys.exit(main())
