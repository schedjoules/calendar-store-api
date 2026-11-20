## Deprecations and Changes

Breaking changes and deprecated features of the API.

### Done
* **HTTPS only.** Plain HTTP requests are redirected to HTTPS.
* **Location by country code.** `location` takes an ISO 3166 country code; looking a location up by numeric id is no longer supported.
* **`country` parameter renamed to `location`.** The request parameter is `location`. Responses still have a `country` field with the country's name.
* **`start_before` and the default of 500 results.** Calendar feeds no longer document a `start_before` parameter (it had no effect) or a default limit of 500 events: by default every event in the date range is returned. See [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md).

### Planned
* **`icon_etag` removal.** The field is still sent in Countries and in Top, New and Next, but its value is always `null`. Do not rely on it.
* **`events_updated_since` format.** National holiday calendars take Unix time, all others an ISO 8601 datetime. This will become one format; see [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#incremental-updates).
