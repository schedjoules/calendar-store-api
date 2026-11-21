## Examples

Real responses from the API, for building and testing a client without a key of your own. Use them as fixtures in your tests.

### responses/

Captured on 2026-11-20 with the public test key; long lists are shortened.

| File | Request |
|---|---|
| `page.json` | `GET /pages/115673?locale=en&location=us` (2 sections, 2 items each) |
| `search.json` | `GET /pages/search?q=Warriors&nr_results=2` |
| `info.json` | `GET /pages/50084/info?locale=en` |
| `ultimate_successor.json` | `GET /pages/766e8a162f82/ultimate_successor` |
| `cities_search.json` | `GET /cities/search?q=Amsterdam` (3 cities) |
| `weather_settings.json` | `GET /cities/weather_settings?locale=en&location=us` |
| `error_401.json` | Any request without an API key |
| `event.jscalendar.json` | One event as JSCalendar: `GET {feed url}.jscalendar?...&event=20260531_` (captured 2026-11-21). The test key serves Moon Phases, so it has only the standard properties; a holiday with vendor properties is shown in [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#one-event-as-jscalendar-rfc-8984) |

### feeds/

| File | What it is | Source |
|---|---|---|
| `moon_phases.ics` | A normal feed (3 events) | Live capture |
| `no_access.ics` | Placeholder: the feed URL is wrong | Live capture (invalid `x`) |
| `expired_subscription.ics` | Placeholder: the user's access ended | Rebuilt from the server template |
| `expired_calendar.ics` | Placeholder: the calendar was retired | Rebuilt from the server template |
| `empty.ics` | Placeholder: no events in the date range | Rebuilt from the server template |

The texts of the rebuilt placeholders can differ from what the server sends, and are translated. Recognise placeholders by `UID` only, never by text. See the [Integration Guide](https://github.com/schedjoules/calendar-store-api/blob/master/details/integration_guide.md#step-5-recognise-placeholder-events).
