# Instructions for coding agents

You are integrating the SchedJoules Calendar API into an app.

1. Read `llms-full.txt` in this repository: it is the whole API description in one file. Start with the Integration Guide section, then the Android or iOS section, then the UI section that fits the app:
   - **The app already shows calendars or events** (a calendar, agenda or planner app): follow Embedding the Catalogue, pattern 3 "A source among sources", even when you were asked for a "calendar store". Build the Browse and Calendar screens from A Basic UI and open them from the app's existing "add calendar" entry. Do not build A Basic UI's My calendars or Settings screens: subscribed calendars appear in the app's own calendar list, and country and language go in the app's own settings.
   - **The app has no calendar views of its own**, or you were asked for a standalone catalogue: build all four screens of A Basic UI.
   - **Only one kind of content is wanted** (public holidays, one sport): Embedding the Catalogue, pattern 1 or 2.
   If none of these clearly applies, ask the person you work for before building screens.
2. Do not use the SchedJoules SDKs or the Swift client library. They are deprecated. Call the REST API directly.
3. Use `examples/` as test fixtures: real API responses and feeds, including the placeholder feeds.
4. The rules that break integrations most often:
   - Every API request sends `Authorization: Token token="<key>"`. Parse responses leniently: new fields appear without notice.
   - Feed URL = the calendar item's `url` + `&u=<random id of 20+ characters, stable per user>`. Never remove or rebuild other parameters. Never fetch a URL that still contains `{placeholders}`.
   - Accept a feed body only if it starts with `BEGIN:VCALENDAR` and ends with `END:VCALENDAR`.
   - Feeds answer access problems with `200` and a placeholder event. Recognise them by `UID` (`no_access@`, `expired_subscription@`, `expired_<lang>@`, `empty_<id>@schedjoules.com`), never show them as events, and never copy a placeholder feed's `X-WR-CALNAME` over the calendar's name.
   - Sync by `UID`; delete events only based on a complete feed; refresh with `If-None-Match`.
   - Never log feed URLs.
   - Show "Calendars by SchedJoules" on every screen where users browse, search or pick calendars (README, Attribution). It is required.
5. The public test key returns the real catalogue, but every calendar URL serves the same feed: "Moon Phases", a normal feed with upcoming events. So with the test key every calendar previews the same events and every feed's `X-WR-CALNAME` is "Moon Phases". That is expected, not a parsing bug; it is also why the shown name must come from the catalogue item. Test the other feed states with `examples/feeds/`. Real content needs a key from support@schedjoules.com.
6. Check your screens against the UI checklist at the end of A Basic UI before you report the work as done.
