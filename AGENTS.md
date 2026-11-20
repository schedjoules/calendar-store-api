# Instructions for coding agents

You are integrating the SchedJoules Calendar API into an app.

1. Read `llms-full.txt` in this repository: it is the whole API description in one file. Start with the Integration Guide section, then the Android or iOS section, then A Basic UI for a separate catalogue, or Embedding the Catalogue when the app already has its own screens.
2. Do not use the SchedJoules SDKs or the Swift client library. They are deprecated. Call the REST API directly.
3. Use `examples/` as test fixtures: real API responses and feeds, including the placeholder feeds.
4. The rules that break integrations most often:
   - Every API request sends `Authorization: Token token="<key>"`. Parse responses leniently: new fields appear without notice.
   - Feed URL = the calendar item's `url` + `&u=<random id of 20+ characters, stable per user>`. Never remove or rebuild other parameters. Never fetch a URL that still contains `{placeholders}`.
   - Accept a feed body only if it starts with `BEGIN:VCALENDAR` and ends with `END:VCALENDAR`.
   - Feeds answer access problems with `200` and a placeholder event. Recognise them by `UID` (`no_access@`, `expired_subscription@`, `expired_<lang>@`, `empty_<id>@schedjoules.com`), never show them as events, and never copy a placeholder feed's `X-WR-CALNAME` over the calendar's name.
   - Sync by `UID`; delete events only based on a complete feed; refresh with `If-None-Match`.
   - Never log feed URLs.
5. The public test key returns the same placeholder calendar for every calendar URL. Real content needs a key from support@schedjoules.com.
