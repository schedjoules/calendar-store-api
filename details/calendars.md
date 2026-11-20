## Calendars

The `url` of a calendar item is the calendar feed. Calendars are served in iCalendar format ([RFC 5545](https://tools.ietf.org/html/rfc5545)) by default, which every major operating system and calendar client can subscribe to. jCal ([RFC 7265](https://tools.ietf.org/html/rfc7265)) and xCal ([RFC 6321](https://tools.ietf.org/html/rfc6321)) are also available: add the extension to the path.

* iCalendar: `.../calendars/766e8a162f82`
* jCal: `.../calendars/766e8a162f82.json`
* xCal: `.../calendars/766e8a162f82.xml`

Differences from the iCalendar feed:
* jCal and xCal responses contain no alarms.
* jCal property names use underscores where the RFC uses hyphens, for example `x_wr_calname` instead of `x-wr-calname`.

Remember to append `&u={unique_anonymous_user_identifier}` to every calendar URL (see the [README](https://github.com/schedjoules/calendar-store-api#unique-anonymous-user-identifier)).

### Date Range

By default, the date range of events returned depends on your agreement with SchedJoules. You can move the start of the window:

```
GET /calendars/766e8a162f82?start_at_or_after={datetime}

Optional GET parameters
- start_at_or_after     datetime    ISO 8601 (e.g. 2026-01-01T00:00:00Z). Only events
                                    starting at or after this moment are returned.
```

The end of the window cannot be changed per request.

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
