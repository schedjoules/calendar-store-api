## Integration Guide

The shortest path from nothing to a calendar app that shows SchedJoules calendars. It ties the reference pages together and adds the rules that only show up once real users sync real feeds. Screens: [A Basic UI](https://github.com/schedjoules/calendar-store-api/blob/master/details/ui.md) for a separate catalogue, [Embedding](https://github.com/schedjoules/calendar-store-api/blob/master/details/embedding.md) to put it inside an existing app. Platform specifics: [Android](https://github.com/schedjoules/calendar-store-api/blob/master/details/android.md) and [iOS](https://github.com/schedjoules/calendar-store-api/blob/master/details/ios.md). Example responses and feeds: [examples/](https://github.com/schedjoules/calendar-store-api/tree/master/examples).

### The model in one paragraph

The API is a catalogue: pages of calendars, in the user's language and country. Your app shows the catalogue, the user picks a calendar, and from then on your app fetches that calendar's events regularly. A calendar item has a `url` that serves the events in two formats, and steps 1 to 3 are the same for both:

* **JSCalendar** ([RFC 8984](https://www.rfc-editor.org/rfc/rfc8984)), the recommended format: plain JSON with structured data, a slim list of the calendar's events, and the full details of one event when the user opens it.
* **iCalendar** ([RFC 5545](https://tools.ietf.org/html/rfc5545)), the most widely used format, and what the `url` returns as it is.

JSCalendar can be used for subscribing and syncing too, but most calendar clients (the iOS and Android calendars, Google Calendar, Outlook) read only iCalendar. That is why this guide syncs into a device calendar from iCalendar. After step 3 it splits into two tracks, and many apps follow both. See [Which Format to Use](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#which-format-to-use).

### Step 1: a key and the request basics

Use the test key from the [README](https://github.com/schedjoules/calendar-store-api#set-yourself-up) to build everything; request your own key before you ship. Every API request needs:

```
Authorization: Token token="{YOUR_API_KEY}"
```

Send `locale` (the user's language) and `location` (the user's country) on page requests. Follow redirects. Ignore response fields you do not know.

### Step 2: show the catalogue

1. `GET /pages?locale=de&location=de` gives the home page for that user. It redirects to `/pages/{id}`.
2. Render each section of `page_sections` as a header with its `items`.
3. An item with `item_class: "page"` opens another page: `GET` its `url`.
4. An item with `item_class: "calendar"` is subscribable.

Add search with `GET /pages/search?q=...` (3 characters or more). For the screens around it, see [A Basic UI](https://github.com/schedjoules/calendar-store-api/blob/master/details/ui.md). See [Pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md) and [Search](https://github.com/schedjoules/calendar-store-api/blob/master/details/search.md).

Store the `item_id` of each calendar the user subscribes to: you need it later (step 5).

### Step 3: build the feed URL

Take the calendar item's `url` as it is, and append the user identifier:

```
{url}&u={unique_anonymous_user_identifier}
```

Rules:
* `u` is a random identifier you create once per user (or install), at least 20 characters. A UUID works. Use the same value for every feed of that user, and as the account id in the [Accounts API](https://github.com/schedjoules/calendar-store-api/blob/master/details/accounts.md) if you use it.
* Never remove or change the other parameters, `x` in particular: it identifies your API key on the feed.
* A `url` that contains `{placeholders}` is a template. Fill every placeholder first (the weather calendar's `{location}` and units, see [Weather](https://github.com/schedjoules/calendar-store-api/blob/master/details/weather.md)). Never fetch or subscribe to a URL that still contains `{` or `%7B`.
* The feed URL is per user. Do not log it or send it to analytics.

### Step 4: choose a track

| Your app | Track | Format |
|---|---|---|
| Shows events in its own screens: an agenda, upcoming matches, an event page | [A: show events in your app](#track-a-show-events-in-your-app) | JSCalendar |
| Puts events in the device calendar, or in a calendar client that reads iCalendar | [B: sync into a calendar](#track-b-sync-into-a-calendar) | iCalendar |

An app that does both, for example one that syncs into the device calendar and opens an event page of its own, follows both tracks with the same feed URL from step 3.

### Track A: show events in your app

#### Step A1: list a calendar's events

Add `.jscalendar` to the path of the feed URL from step 3 and `GET` it with `Accept: application/jscalendar+json`. Keep every parameter, `u` included. The answer is the whole calendar as a JSCalendar `Group`: each event with its `uid`, `updated`, `title`, `start`, `timeZone` (or `showWithoutTime`), `duration`, `status` and `locations`, a fraction of the iCalendar feed's size. See [A Calendar as a JSCalendar List](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#a-calendar-as-a-jscalendar-list).

* A calendar without events gives `"entries": []`. There are no placeholder events in JSCalendar.
* Access problems are HTTP statuses: `403` with `{"error":"no_access"}` (a bug in your URL, fix it) or `{"error":"expired_subscription"}` (offer renewal).
* Refresh with `If-None-Match` and the last `ETag`, as in step B3: an unchanged list answers `304` with no body.

#### Step A2: show one event

When the user opens an event, fetch it as JSCalendar instead of parsing `DESCRIPTION`: take the same `.jscalendar` URL and append `&event={event part}`, the part of the `uid` after `{item_id}_{language_id}_` (drop `@schedjoules.com`). The document has the same title and time as the list, plus the description, links and structured data such as a match's line-ups, a race classification or a holiday's background. A `404` means the event is no longer in the calendar. On anything other than `200` or `304`, show what you already have. See [One Event as JSCalendar](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#one-event-as-jscalendar-rfc-8984).

### Track B: sync into a calendar

#### Step B1: fetch the feed

`GET` the feed URL. It returns `text/calendar` (iCalendar, [RFC 5545](https://tools.ietf.org/html/rfc5545)). Use it for subscribing and syncing: most calendar clients read only iCalendar, and the rules in this track are written for it. Do not sync from jCal or xCal; they work but are not recommended. When your app also opens events in its own screens, fetch those as JSCalendar (step A2).

What a feed contains:
* `X-WR-CALNAME`: the calendar's name. In your UI you can use the catalogue item's `name` instead (from search results, use `original_name`: search names can end in a gender sign and a flag to tell teams apart).
* One `VEVENT` per event, with `UID`, `DTSTART`, `DTEND`, `SUMMARY`, `DESCRIPTION`, `LOCATION`, `URL`, `LAST-MODIFIED`, `CATEGORIES`, `STATUS`, `TRANSP:TRANSPARENT` and often a `VALARM` (see [Alarms](https://github.com/schedjoules/calendar-store-api/blob/master/details/alarms.md)).
* All-day events use `DTSTART;VALUE=DATE` with an exclusive `DTEND`, as the RFC says. Some feeds, the placeholder events among them, send `DTEND` equal to `DTSTART`: treat that as a one-day event.
* `UID` looks like `{item_id}_{language_id}_{rest}@schedjoules.com` and is stable: the same event keeps its UID across fetches. The language is part of it, so the same event in another language has another UID.

**Check the body before you use it.** Only accept a response that starts with `BEGIN:VCALENDAR` and ends with `END:VCALENDAR`. A proxy error page or a cut-off download otherwise looks like a calendar with no events, and your sync deletes everything.

#### Step B2: recognise placeholder events

A feed never answers an access problem with an HTTP error. It answers `200` with one placeholder event that explains the problem to the user. Recognise them by `UID`:

| UID | Meaning | What your app should do |
|---|---|---|
| `no_access@schedjoules.com` | The URL is wrong: missing or invalid `x`, missing `u`, inactive key | A bug on your side. Do not show it as an event; log it and fix the URL |
| `expired_subscription@schedjoules.com` | The user's access ended (for example an expired license in the [Accounts API](https://github.com/schedjoules/calendar-store-api/blob/master/details/accounts.md)) | Offer renewal; keep or hide the calendar |
| `expired_{language}@schedjoules.com` | The calendar itself was retired | Remove the subscription, or offer a replacement (step 5) |
| `empty_{item_id}@schedjoules.com` | The calendar has no events in the date range right now | A normal state. Show "no upcoming events" rather than the event |

The placeholder events also carry `CATEGORIES:Expired` or `CATEGORIES:No access`. A placeholder feed also changes `X-WR-CALNAME` (for example to "You have no access to this calendar"): never copy it over the name you show for the calendar. Example feeds: [examples/feeds](https://github.com/schedjoules/calendar-store-api/tree/master/examples/feeds).

#### Step B3: keep it in sync

**Refresh.** Fetch each feed every few hours. Send `If-None-Match` with the last `ETag`: an unchanged feed answers `304 Not Modified` with no body, which costs almost nothing. More often than hourly gains nothing for most calendars; live sport scores change during matches only.

**Apply changes by UID.** Compare the new feed with what you stored:
* a UID you do not have: add the event
* a UID you have: update it if anything changed (`LAST-MODIFIED` helps)
* a UID that is gone from a complete feed: delete the event

**Incremental updates** with `events_updated_since` are optional (see [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#incremental-updates)). They never tell you what was deleted, so still fetch the complete feed regularly, for example once a day, and delete only based on complete feeds.

### Both tracks

#### Step 5: replaced calendars

A calendar can be replaced by a newer one, for example a sport season by the next. The old feed URL keeps working and serves the new content, so nothing breaks. To update what you store and show:

```
GET /pages/{item_id}/info
```

returns the calendar's current `item` (name, `url`, icon) and the pages it is listed on, and

```
GET /pages/{calendar_id}/ultimate_successor
```

returns `{"requested_id": "...", "successor_id": "...", "in_api": true}` for the `calendar_id` in a feed URL (`/calendars/{calendar_id}`).

#### Step 6: errors

API errors (not feeds or JSCalendar documents) answer with an HTTP status and:

```json
{"errors": {"status": 401, "title": "Invalid API key", "detail": "https://github.com/schedjoules/calendar-store-api#set-yourself-up"}}
```

| Status | Title | Cause |
|---|---|---|
| 401 | Invalid API key | Missing or unknown key |
| 403 | This API key is inactive | The key was switched off; contact us |
| 404 | Nothing here | Unknown page or route |
| 405 | This request is not allowed with this API key | The endpoint is not enabled for your key, for example licenses |
| 500 | Something went wrong | On our side; retry later |

### A v0.1 checklist

- [ ] Every request sends the `Authorization` header; responses are parsed leniently
- [ ] Catalogue browsing with `locale` and `location` from the device, following redirects
- [ ] Feed URL = item `url` + `&u=`, templates filled, nothing else changed
- [ ] Feed URLs never logged

Track A, events in your app:
- [ ] Event lists read the JSCalendar list; an empty calendar shows "no upcoming events"
- [ ] Event detail screens read the event as JSCalendar, falling back to what you have on any non-200
- [ ] `403` answers handled: `no_access` logged as a bug, `expired_subscription` offers renewal

Track B, sync into a calendar:
- [ ] Feed body checked for `BEGIN:VCALENDAR` ... `END:VCALENDAR` before use
- [ ] Placeholder UIDs handled, not shown as events
- [ ] Refresh with `If-None-Match`; changes applied by UID; deletions only from complete feeds
