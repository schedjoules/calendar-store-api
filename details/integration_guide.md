## Integration Guide

The shortest path from nothing to a calendar app that shows SchedJoules calendars. It ties the reference pages together and adds the rules that only show up once real users sync real feeds. Screens: [A Basic UI](https://github.com/schedjoules/calendar-store-api/blob/master/details/ui.md). Platform specifics: [Android](https://github.com/schedjoules/calendar-store-api/blob/master/details/android.md) and [iOS](https://github.com/schedjoules/calendar-store-api/blob/master/details/ios.md). Example responses and feeds: [examples/](https://github.com/schedjoules/calendar-store-api/tree/master/examples).

### The model in one paragraph

The API is a catalogue: pages of calendars, in the user's language and country. A calendar item has a `url`, which is an iCalendar feed. Your app shows the catalogue, the user picks a calendar, and from then on your app (or the operating system) fetches that feed regularly. All content lives in the feed; the API is only needed to browse.

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

Store the `item_id` of each calendar the user subscribes to: you need it later (step 6).

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

### Step 4: fetch the feed

`GET` the feed URL. It returns `text/calendar` (iCalendar, [RFC 5545](https://tools.ietf.org/html/rfc5545)).

What a feed contains:
* `X-WR-CALNAME`: the calendar's name. In your UI you can use the catalogue item's `name` instead (from search results, use `original_name`: search names can end in a gender sign and a flag to tell teams apart).
* One `VEVENT` per event, with `UID`, `DTSTART`, `DTEND`, `SUMMARY`, `DESCRIPTION`, `LOCATION`, `URL`, `LAST-MODIFIED`, `CATEGORIES`, `STATUS`, `TRANSP:TRANSPARENT` and often a `VALARM` (see [Alarms](https://github.com/schedjoules/calendar-store-api/blob/master/details/alarms.md)).
* All-day events use `DTSTART;VALUE=DATE` with an exclusive `DTEND`, as the RFC says. Some feeds, the placeholder events among them, send `DTEND` equal to `DTSTART`: treat that as a one-day event.
* `UID` looks like `{item_id}_{language_id}_{rest}@schedjoules.com` and is stable: the same event keeps its UID across fetches. The language is part of it, so the same event in another language has another UID.

**Check the body before you use it.** Only accept a response that starts with `BEGIN:VCALENDAR` and ends with `END:VCALENDAR`. A proxy error page or a cut-off download otherwise looks like a calendar with no events, and your sync deletes everything.

### Step 5: recognise placeholder events

A feed never answers an access problem with an HTTP error. It answers `200` with one placeholder event that explains the problem to the user. Recognise them by `UID`:

| UID | Meaning | What your app should do |
|---|---|---|
| `no_access@schedjoules.com` | The URL is wrong: missing or invalid `x`, missing `u`, inactive key | A bug on your side. Do not show it as an event; log it and fix the URL |
| `expired_subscription@schedjoules.com` | The user's access ended (for example an expired license in the [Accounts API](https://github.com/schedjoules/calendar-store-api/blob/master/details/accounts.md)) | Offer renewal; keep or hide the calendar |
| `expired_{language}@schedjoules.com` | The calendar itself was retired | Remove the subscription, or offer a replacement (step 6) |
| `empty_{item_id}@schedjoules.com` | The calendar has no events in the date range right now | A normal state. Show "no upcoming events" rather than the event |

The placeholder events also carry `CATEGORIES:Expired` or `CATEGORIES:No access`. A placeholder feed also changes `X-WR-CALNAME` (for example to "You have no access to this calendar"): never copy it over the name you show for the calendar. Example feeds: [examples/feeds](https://github.com/schedjoules/calendar-store-api/tree/master/examples/feeds).

### Step 6: keep it in sync

**Refresh.** Fetch each feed every few hours. Send `If-None-Match` with the last `ETag`: an unchanged feed answers `304 Not Modified` with no body, which costs almost nothing. More often than hourly gains nothing for most calendars; live sport scores change during matches only.

**Apply changes by UID.** Compare the new feed with what you stored:
* a UID you do not have: add the event
* a UID you have: update it if anything changed (`LAST-MODIFIED` helps)
* a UID that is gone from a complete feed: delete the event

**Incremental updates** with `events_updated_since` are optional (see [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#incremental-updates)). They never tell you what was deleted, so still fetch the complete feed regularly, for example once a day, and delete only based on complete feeds.

**Replaced calendars.** A calendar can be replaced by a newer one, for example a sport season by the next. The old feed URL keeps working and serves the new content, so nothing breaks. To update what you store and show:

```
GET /pages/{item_id}/info
```

returns the calendar's current `item` (name, `url`, icon) and the pages it is listed on, and

```
GET /pages/{calendar_id}/ultimate_successor
```

returns `{"requested_id": "...", "successor_id": "...", "in_api": true}` for the `calendar_id` in a feed URL (`/calendars/{calendar_id}`).

### Step 7: errors

API errors (not feeds) answer with an HTTP status and:

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
- [ ] Feed body checked for `BEGIN:VCALENDAR` ... `END:VCALENDAR` before use
- [ ] Placeholder UIDs handled, not shown as events
- [ ] Refresh with `If-None-Match`; changes applied by UID; deletions only from complete feeds
- [ ] Feed URLs never logged
