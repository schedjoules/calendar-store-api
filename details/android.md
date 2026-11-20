## Android

Android has no built-in way to subscribe to an iCalendar feed. Your app fetches the feeds itself and writes the events into the system calendar through `CalendarContract`, so they show up in Google Calendar and every other calendar app on the device. This page lists what that takes, from the SchedJoules Android app's own implementation. Read the [Integration Guide](https://github.com/schedjoules/calendar-store-api/blob/master/details/integration_guide.md) first.

### Architecture

* **Fetching:** a `WorkManager` periodic job (with a network constraint) fetches every subscribed feed. Send `If-None-Match` and do nothing more on a `304`.
* **Parsing:** an iCalendar library such as [biweekly](https://github.com/mangstadt/biweekly).
* **Storage:** one local calendar per subscription in `CalendarContract.Calendars`, under your own account type, with events in `CalendarContract.Events`.

You need the `READ_CALENDAR` and `WRITE_CALENDAR` permissions. Ask for them when the user subscribes to their first calendar, after explaining why, not at app start.

### Writing calendars and events

* Write as a sync adapter: append `CALLER_IS_SYNCADAPTER=true`, `ACCOUNT_NAME` and `ACCOUNT_TYPE` (your own, for example your package name) to the content URI. Use `ACCOUNT_TYPE_LOCAL` only if you accept that it behaves differently on some devices.
* One calendar row per subscription. Put your subscription id in `Calendars._SYNC_ID`, and the feed's name in `CALENDAR_DISPLAY_NAME`.
* Put the event `UID` in `Events._SYNC_ID`. On each sync, compare by `_SYNC_ID`: insert new UIDs, update changed ones, delete the ones a complete feed no longer has.
* Apply the changes with `applyBatch`, in chunks of a few hundred operations: one Binder transaction is limited to about 1 MB, and a large sport or TV calendar can exceed it in one go.

### Dates and times

* **All-day events** (`DTSTART;VALUE=DATE`): set `ALL_DAY=1`, `EVENT_TIMEZONE=UTC`, and `DTSTART` at **UTC midnight** of the date. Many parsers, biweekly among them, read a date as midnight in the device's time zone; east of UTC that is the previous day in UTC, and every all-day event lands a day early. Convert to UTC midnight of the same calendar date.
* **Timed events:** use the event's `TZID` for `EVENT_TIMEZONE`. If the feed has no matching `VTIMEZONE`, the TZID is usually an Olson name Android knows; fall back to UTC only if it is not.
* **Recurring events** (`RRULE`): Android requires `DURATION` and forbids `DTEND` on them. Compute `DURATION` from the event's start and end.
* `RECURRENCE-ID` overrides need a separate row with `ORIGINAL_SYNC_ID` and `ORIGINAL_INSTANCE_TIME`. Few SchedJoules feeds use them; skipping them keeps the main series intact.

### Alarms

A `VALARM` in the feed becomes a row in `CalendarContract.Reminders` (`MINUTES` before, `METHOD_ALERT`). See [Alarms](https://github.com/schedjoules/calendar-store-api/blob/master/details/alarms.md) for the defaults and the `al` parameter.

### Google Calendar and other devices

Events in a calendar under your own account type stay on the device. They show up in Google Calendar on that phone, but are not uploaded to the user's Google account, so they do not appear on the web or on other devices. That is how Android works for any calendar app that is not a Google account; tell your users rather than trying to work around it.

### Refreshing

* A periodic `WorkManager` job every few hours is enough. Android may delay it on low battery or in Doze; that is expected.
* Run a sync right after a subscription is added, so the user sees events at once.
* Keep the last `ETag` per feed and send it as `If-None-Match`.
