## Calendars

Calendars are provided in iCalendar format ([RFC 5545](https://tools.ietf.org/html/rfc5545)) by default. We also support jCal ([RFC 7265](https://tools.ietf.org/html/rfc7265)) and xCal ([RFC 6321](https://tools.ietf.org/html/rfc6321)). Most operating systems and calendar clients can parse calendar files natively, though you may also implement your own parser.

The default calendar format is `.ics`. To request a calendar in jCal or xCal format, append the appropriate file extension:
* iCal: `.../calendars/766e8a162f82`
* jCal: `.../calendars/766e8a162f82.json`
* xCal: `.../calendars/766e8a162f82.xml`

### Date Range

By default, the date range of events returned depends on the subscription status of the user:

| Subscription | Events from | Events until |
|---|---|---|
| Premium | 1 year ago | 10 years from now |
| Free | Now | 60 days from now |

You can override the date range using the following parameters:

```
GET /calendars/766e8a162f82?start_at_or_after={datetime}&start_before={datetime}

Optional GET parameters
- start_at_or_after     datetime    ISO 8601 (e.g. 2026-01-01T00:00:00Z). Overrides the default start of the event window.
- start_before          datetime    ISO 8601. Overrides the default end of the event window.
```

### Incremental Updates

To fetch only events that have been updated since a given point in time — useful for syncing changes without re-fetching the full calendar — use the `events_updated_since` parameter:

```
GET /calendars/766e8a162f82?events_updated_since={datetime}

Optional GET parameters
- events_updated_since  datetime    ISO 8601. Returns only events with an updated_at timestamp after this value.
```

### Number of Events

By default, up to 500 events are returned per calendar request. You can request a different number using the `results` parameter:

```
GET /calendars/766e8a162f82?results={nr_of_events}

Optional GET parameters
- results               integer     Maximum number of events to return (default: 500).
```

### Hiding Sport Event Results
Some users prefer not to see sport event results in their calendar summary — for example, if they intend to watch the event later and want to avoid spoilers. This behaviour can be controlled via the `show_result` parameter.

```
GET /calendar/d2b1e319a12a?show_result=false

Optional GET parameters
- show_result (if omitted, defaults to 'true')
```
