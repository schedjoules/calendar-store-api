## Deprecations and Changes

Breaking changes and deprecated features of the API.

### Done
* **JSCalendar recommended; jCal and xCal not recommended.** Since 2026-11-21 JSCalendar (RFC 8984) is the recommended format for new integrations: the list for event lists in your app, one event for detail screens. iCalendar remains the format for subscribing and syncing. jCal and xCal keep working but are not recommended: they carry no more than the iCalendar feed. See [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#formats).
* **jCal and xCal follow their RFCs.** Since 2026-11-21:
  * the calendar name property is `x-wr-calname`, not `x_wr_calname`;
  * date-times are UTC with `Z` (`2026-05-31T08:45:00Z`), not `+00:00`;
  * the responses are `application/calendar+json` and `application/calendar+xml` instead of `application/json` and `application/xml`;
  * xCal text is XML-escaped only, without iCalendar backslash escapes (`\,`). Feeds with `&` or `<` in an event text used to be invalid XML;
  * in xCal, `url` is a `<uri>` and is left out when empty.
* **A calendar as a JSCalendar list.** Since 2026-11-21 a `.jscalendar` request without `event` returns the whole calendar as a JSCalendar `Group` with titles and times, instead of `400`. See [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#a-calendar-as-a-jscalendar-list).
* **One event as JSCalendar.** Since 2026-11-21 a single event is available as a JSCalendar document (RFC 8984, see [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#one-event-as-jscalendar-rfc-8984)), with structured match, race, holiday and finance data. The iCalendar, jCal and xCal feeds were unchanged by it.
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
