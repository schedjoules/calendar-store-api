## Deprecations and Changes

Breaking changes and deprecated features of the API.

### Done
* **One event as JSCalendar.** Since 2026-11-21 a single event is available as a JSCalendar document (RFC 8984, see [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#one-event-as-jscalendar-rfc-8984)), with structured match, race, holiday and finance data. The iCalendar, jCal and xCal feeds are unchanged.
* **SDKs deprecated.** The iOS and Android SDKs and the Swift client library are no longer maintained. See [SDKs](https://github.com/schedjoules/calendar-store-api/blob/master/details/sdks.md).
* **HTTPS only.** Plain HTTP requests are redirected to HTTPS.
* **Location by country code.** `location` takes an ISO 3166 country code; looking a location up by numeric id is no longer supported.
* **`country` parameter renamed to `location`.** The request parameter is `location`. Responses still have a `country` field with the country's name.
* **No default of 500 results.** By default every event in the date range is returned; `results` still limits it. See [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md).
* **`start_before` works.** It was documented for years but had no effect. It now ends the event window, within the window your agreement gives.
* **Search returns at most 50 results.** Larger `nr_results` values used to be honoured; they now return 50.

### Planned
* **`icon_etag` removal.** The field is still sent in Countries and in Top, New and Next, but its value is always `null`. Do not rely on it.
* **`events_updated_since` format.** National holiday calendars take Unix time, all others an ISO 8601 datetime. This will become one format; see [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#incremental-updates).
