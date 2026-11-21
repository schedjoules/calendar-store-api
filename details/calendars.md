## Calendars

The `url` of a calendar item is the calendar feed. Calendars are served in iCalendar format ([RFC 5545](https://tools.ietf.org/html/rfc5545)) by default, which every major operating system and calendar client can subscribe to. jCal ([RFC 7265](https://tools.ietf.org/html/rfc7265)) and xCal ([RFC 6321](https://tools.ietf.org/html/rfc6321)) are also available: add the extension to the path.

* iCalendar: `.../calendars/766e8a162f82`
* jCal: `.../calendars/766e8a162f82.json`
* xCal: `.../calendars/766e8a162f82.xml`

Differences from the iCalendar feed:
* jCal and xCal responses contain no alarms.
* jCal property names use underscores where the RFC uses hyphens, for example `x_wr_calname` instead of `x-wr-calname`.

For a single event, for example the detail screen a user opens from an event, there is also a JSON document in JSCalendar format ([RFC 8984](https://www.rfc-editor.org/rfc/rfc8984)). See [One Event as JSCalendar](#one-event-as-jscalendar-rfc-8984).

Remember to append `&u={unique_anonymous_user_identifier}` to every calendar URL (see the [README](https://github.com/schedjoules/calendar-store-api#unique-anonymous-user-identifier)).

### Which Format to Use

| You want to | Use |
|---|---|
| Subscribe a user, or sync the events into the device calendar | iCalendar. Every client reads it, and it is the format the sync rules in the [Integration Guide](https://github.com/schedjoules/calendar-store-api/blob/master/details/integration_guide.md) are written for |
| Read a whole calendar as JSON or XML | jCal or xCal. Same content as the iCalendar feed, one to one |
| Show a list of a calendar's events in your own app: an agenda, upcoming matches | JSCalendar list: the whole calendar, titles and times only |
| Show one event in detail: a match with its line-ups, a race classification, a holiday's background | JSCalendar, one event per request |

JSCalendar does not replace the feed. Keep syncing with iCalendar, show your own lists from the JSCalendar list, and fetch the event's JSCalendar document when the user opens an event.

### One Event as JSCalendar (RFC 8984)

```
GET /calendars/766e8a162f82.jscalendar?{the feed's own parameters}&event={event part}
Accept: application/jscalendar+json
```

Take the calendar item's `url` exactly as you use it for the feed, including `&u=`, add `.jscalendar` to the path and append `&event=`. The request passes the same access checks and returns events from the same window as the feed.

The **event part** comes from the event's `UID` in the feed. A UID has the form `{page id}_{language id}_{event part}@schedjoules.com`: drop the domain and the first two fields. The event part can itself contain underscores.

* UID `49733_1_28_1__20261205@schedjoules.com` → `event=28_1__20261205`
* UID `36254089_1_5781805@schedjoules.com` → `event=5781805`

Calendars whose UIDs do not start with the page id, such as weather, have no event documents.

#### Responses

| Status | Body | When |
|---|---|---|
| 200 | JSCalendar `Event`, `application/jscalendar+json` | The event is in the feed this URL serves |
| 304 | none | `If-None-Match` matches. The ETag is per event |
| 403 | `{"error":"no_access"}` or `{"error":"expired_subscription"}` | Where the feed would serve a placeholder event |
| 404 | `{"error":"event_not_found"}` | The event is not in this feed: outside the window, removed, or unknown |
| 404 | `{"error":"expired_calendar"}` | The calendar is retired |

On any status other than 200 or 304, show what you already have from the feed (title, time, `DESCRIPTION`).

Unlike the feed, access problems come back as HTTP errors, not as a `200` with a placeholder event.

#### The Document

Standard JSCalendar properties are written by the same code that writes the iCalendar feed, so for the same `UID` they always agree with it:

| iCalendar | JSCalendar |
|---|---|
| `UID` | `uid` |
| `SUMMARY` | `title` |
| `DTSTART`, `DTEND` with a time (UTC) | `start` (local date-time), `timeZone: "Etc/UTC"`, `duration` |
| `DTSTART`, `DTEND` as dates (all-day) | `start` at `T00:00:00`, `showWithoutTime: true`, `duration` in days, no `timeZone` |
| `LOCATION`, `GEO` | `locations."1"` with `name` and `coordinates` (`geo:lat,lon`) |
| `URL` | `links."1"` with `href`, `rel: "alternate"` |
| `LAST-MODIFIED` | `updated` |
| `STATUS` | `status`: `confirmed`, `tentative` or `cancelled` |
| `DESCRIPTION` | `description`, with real line breaks |

Empty properties are left out.

Structured data is in vendor properties, named under our domain as RFC 8984 section 3.3 prescribes:

| Property | Calendars | Content |
|---|---|---|
| `schedjoules.com:version` | all | `1`. Within a version, changes are additive only |
| `schedjoules.com:match` | football | `status`, `competition`, score, `home` and `away` with team, formation, starters and bench, and a timeline of goals, cards and substitutions |
| `schedjoules.com:raceResults` | motorsport, cycling | rows of `position`, `name`, `points`, `time`, `status` (`DNF`, `DNS`, `DSQ`, ...) |
| `schedjoules.com:holiday` | national and regional holidays | `observedIn` (list), `estimated` (bool), `text` |
| `schedjoules.com:finance` | company calendars | `company`, `bank`, `extraInfo`, `extraInfoUrl`, `speaker`, `webcast`, `irContact` (`name`, `email`, `phone`) |

Other calendars (TV, school holidays, moon phases, week numbers, name days and more) have the standard properties only: show their `description`. More vendor properties will be added over time. Ignore the ones you do not know, as RFC 8984 requires, and fall back to `description` for any event you have no layout for.

Football:

```json
{
  "@type": "Event",
  "uid": "36254089_1_5781805@schedjoules.com",
  "updated": "2026-11-20T10:00:00Z",
  "title": "NEC Nijmegen - PSV Eindhoven",
  "start": "2026-11-21T19:00:00",
  "timeZone": "Etc/UTC",
  "duration": "PT1H45M",
  "status": "confirmed",
  "description": "Tournament: Eredivisie\n\n...",
  "locations": { "1": { "@type": "Location", "name": "Goffertstadion, Nijmegen", "coordinates": "geo:51.8231,5.83813" } },
  "links": { "1": { "@type": "Link", "href": "https://www.schedjoules.com/calendar/36254089?event=5781805&c=event", "rel": "alternate" } },
  "schedjoules.com:version": 1,
  "schedjoules.com:match": { "id": 5781805, "status": "scheduled", "competition": "Eredivisie", "home": { "team": "NEC Nijmegen", "formation": "3-4-3", "starters": [], "bench": [] }, "away": { "team": "PSV Eindhoven", "starters": [], "bench": [] }, "events": [] }
}
```

Holiday:

```json
{
  "@type": "Event",
  "uid": "49733_1_28_1__20261205@schedjoules.com",
  "title": "Saint Nicholas",
  "start": "2026-12-05T00:00:00",
  "showWithoutTime": true,
  "duration": "P1D",
  "status": "confirmed",
  "description": "Saint Nicholas Day, celebrated on December 6th, ...",
  "locations": { "1": { "@type": "Location", "name": "Netherlands" } },
  "schedjoules.com:version": 1,
  "schedjoules.com:holiday": { "estimated": false, "text": "Saint Nicholas Day, celebrated on December 6th, ..." }
}
```

### A Calendar as a JSCalendar List

Leave out `event` and the same request returns the whole calendar as a JSCalendar `Group` ([RFC 8984 section 5.3](https://www.rfc-editor.org/rfc/rfc8984#section-5.3)), for an event list in your app:

```
GET /calendars/766e8a162f82.jscalendar?{the feed's own parameters}
Accept: application/jscalendar+json
```

```json
{
  "@type": "Group",
  "uid": "36254089_1@schedjoules.com",
  "title": "Eredivisie (Netherlands)",
  "entries": [
    {
      "@type": "Event",
      "uid": "36254089_1_5781805@schedjoules.com",
      "updated": "2026-11-20T10:00:00Z",
      "title": "NEC Nijmegen - PSV Eindhoven",
      "start": "2026-11-21T19:00:00",
      "timeZone": "Etc/UTC",
      "duration": "PT1H45M",
      "status": "confirmed",
      "locations": { "1": { "@type": "Location", "name": "Goffertstadion, Nijmegen", "coordinates": "geo:51.8231,5.83813" } }
    }
  ],
  "schedjoules.com:version": 1
}
```

* Each entry has the list properties only: `uid`, `updated`, `title`, `start`, `timeZone` or `showWithoutTime`, `duration`, `status`, `locations`. They have the same values as in the [event's own document](#the-document). For the description, links and structured data, fetch that document with the entry's event part when the user opens it.
* The entries are the events of the iCalendar feed, in the same order. [`start_at_or_after`, `start_before`](#date-range), [`results`](#number-of-events) and [`events_updated_since`](#incremental-updates) work as they do for the feed. A called-off match in an `events_updated_since` answer has `status: "cancelled"`.
* A calendar without events gives `"entries": []`, never a placeholder event.
* Errors, `ETag` and `304` work as for one event. The list has an `ETag` of its own.
* It is much smaller than the feed. Measured on 2026-11-21: Eredivisie (500 events) 165 KB against 590 KB for the iCalendar feed, 9 KB against 70 KB gzipped.

Do not sync the device calendar from the list. It has no descriptions, so events would show up there without their details, and iOS and other calendar apps read iCalendar only.

#### Why JSCalendar for the Detail Screen

* **No parsing of description text.** In iCalendar, a match's line-ups, a race classification or a holiday's background only exist as free text in `DESCRIPTION`, and the wording of that text is not a contract: it can change at any time. The vendor properties are a contract, versioned and changed additively only.
* **Plain JSON.** No iCalendar parser, line folding, escaping or `VTIMEZONE` handling for a screen that shows one event. Any JSON library reads it.
* **Agrees with the user's calendar.** The standard properties come from the same code as the feed, so the detail screen never shows a different time or title than the event the user synced.
* **A published standard, not a SchedJoules format.** JSCalendar is an IETF standard (RFC 8984), designed as a JSON alternative to iCalendar and the event format of JMAP for Calendars. jCal maps iCalendar one to one, so its `DESCRIPTION` is still text; JSCalendar is built to carry structured data.
* **Safe to build on.** Unknown vendor properties are ignored and `description` is always there, so a new kind of data or a new field never breaks your app.
* **Small and cacheable.** One event per request, with a per-event `ETag` for `If-None-Match`, instead of downloading the whole feed to show one event. For a list screen, the [JSCalendar list](#a-calendar-as-a-jscalendar-list) is a fraction of the feed's size.
* **Clear errors.** Access problems are HTTP statuses, so there are no placeholder events to recognise.

### Date Range

By default, the date range of events returned depends on your agreement with SchedJoules. You can narrow it:

```
GET /calendars/766e8a162f82?start_at_or_after={datetime}&start_before={datetime}

Optional GET parameters
- start_at_or_after     datetime    ISO 8601 (e.g. 2026-01-01T00:00:00Z). Only events
                                    starting at or after this moment are returned.
- start_before          datetime    ISO 8601. Only events starting before this moment
                                    are returned.
```

`start_before` can only shorten the window: a value later than the end of the window your agreement gives has no effect. A value that cannot be parsed is ignored. The weather calendar ignores both parameters.

### Number of Events

By default, every event in the date range is returned. To limit the response to the first N events:

```
GET /calendars/766e8a162f82?results={nr_of_events}

Optional GET parameters
- results               integer     Maximum number of events to return.
```

### Incremental Updates

To fetch only the events that changed since a given moment:

```
GET /calendars/766e8a162f82?events_updated_since={timestamp}

Optional GET parameters
- events_updated_since  Returns only events updated after this moment.
```

The format currently depends on the calendar type:
* **National holiday calendars:** Unix time in seconds, for example `1767225600`.
* **Regional holiday calendars and most sport calendars:** an ISO 8601 datetime, for example `2026-01-01T00:00:00Z`.
* **All other calendars:** the parameter is ignored, and you get the full calendar.

When you ask a sport calendar for updates, events that were called off are included, so you can remove them on your side.

### Hiding Sport Event Results
Some users prefer not to see results in a sport event's title, for example because they will watch the match later. Use `show_result=false` to leave results out:

```
GET /calendars/d2b1e319a12a?show_result=false

Optional GET parameters
- show_result           Only the value 'false' has an effect. Results are shown by default.
```

### Alarms
See [Alarms](https://github.com/schedjoules/calendar-store-api/blob/master/details/alarms.md).

### Calendars Filled In by the User
The weather, pregnancy and countdown calendars have a URL template that your app fills in with what the user enters (a location, a due date, or a name and a date). See [Weather](https://github.com/schedjoules/calendar-store-api/blob/master/details/weather.md) and [Pregnancy and Countdown Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/user_input_calendars.md).
