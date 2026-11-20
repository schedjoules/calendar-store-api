## Calendars Filled In by the User

Most calendar URLs in a pages response can be subscribed to as they are. A few calendars are built from something the user enters in your app before subscribing, the way the [weather calendar](https://github.com/schedjoules/calendar-store-api/blob/master/details/weather.md) needs a location. Their URL is a template with placeholders in curly braces, and your app replaces each placeholder with the user's input.

There are two such calendars:

| Calendar | Placeholders | What it shows |
|---|---|---|
| Pregnancy | `{due_date}` | One event per week of pregnancy, counted back from the due date, plus the due date itself |
| Countdown | `{countdown_name}`, `{countdown_date}`, `{countdown_yearly}` | One all-day event per day up to a date the user picks, for example "12 days to Holiday" |

SchedJoules stores none of this input. Everything the calendar needs is in the URL, and every request computes the events from it. Keep the filled URL as the subscription: changing the input means subscribing to a new URL (or replacing the old one).

### Availability: announce the input step

These pages only appear in API responses for apps that can fill the template. An app announces that with the `features` parameter on its API requests:

```
GET /pages/115673?locale=en&location=us&features=due_date,countdown

Optional GET parameters
- features      comma separated list of input steps the app supports
                due_date    shows the pregnancy calendar
                countdown   shows the countdown calendar
```

The parameter applies to every request that returns pages: `/pages`, `/pages/{page_id}`, search, and the top, new and next lists. A request without it never sees these pages, so an app that cannot fill the template does not show its users a calendar they cannot use.

At the moment these pages are served to the SchedJoules apps only, whatever the `features` parameter says. Contact support@schedjoules.com if you would like to offer them in your app.

### Recognising a template

Check the calendar item's `url` for a placeholder before you present a subscribe action. A URL that still contains `{` and `}` (or their encoded form `%7B` and `%7D`) must never be subscribed to as it is: an unfilled template serves an empty calendar.

Do not add these calendars through a one-tap path that skips the input step, such as a suggestion or onboarding list.

### Pregnancy

The calendar item's URL looks like this:

```
https://xxx.schedjoules.com/calendars/xxxxxxxxxxxx?l=en&due={due_date}&x=xxx
```

Replace `{due_date}` with the due date as `YYYY-MM-DD`, then append `&u={unique_anonymous_user_identifier}` as for any other calendar.

| Parameter | Format | Notes |
|---|---|---|
| `due` | `YYYY-MM-DD` | Accepted from 365 days in the past up to 294 days (42 weeks) ahead |

The calendar contains:
* One all-day event per week, from week 4 to week 42. Weeks are completed weeks as midwives count them: week 12 runs from 12+0 to 12+6, and week 40 starts on the due date.
* One all-day event on the due date itself.

Each event has a title ("Week 12: ...") and a description of the baby's development in that week, written from the NHS week-by-week guide and translated into every API language. The descriptions are general information, not medical advice, and each ends with a disclaimer saying so.

The due date is health data. Do not log the filled URL or send it to analytics.

### Countdown

The calendar item's URL looks like this:

```
https://xxx.schedjoules.com/calendars/xxxxxxxxxxxx?l=en&countdown_name={countdown_name}&countdown_date={countdown_date}&countdown_yearly={countdown_yearly}&x=xxx
```

Fill in the placeholders, append `countdown_repeat` (below) and `&u={unique_anonymous_user_identifier}`.

| Parameter | Format | Notes |
|---|---|---|
| `countdown_name` | text, URL-encoded | What the user counts down to. Whitespace is collapsed and the name is cut at 60 characters |
| `countdown_date` | `YYYY-MM-DD` | The day counted down to. Up to 10 years ahead |
| `countdown_repeat` | `none`, `yearly`, `monthly`, `weekly` | How the countdown repeats. Not in the template yet: append it. Any other value means `none` |
| `countdown_yearly` | `1` or `0` | The older form of `countdown_repeat`: `1` means yearly. Used only when `countdown_repeat` is missing. Fill it as well, so the URL works the same either way |

The calendar is named after the countdown, so a user with several countdowns can tell them apart in their calendar app. Each event is an all-day event:

* Every day before the date: "12 days to Holiday"
* On the date itself: "Holiday is today"

Which days get an event depends on the repeat:

| Repeat | Events | After the date |
|---|---|---|
| `none` | The 365 days before the date, and the date | Nothing. A date more than 365 days in the past gives an empty calendar |
| `yearly` | The 365 days before the next anniversary, and the anniversary | Rolls on to next year's anniversary |
| `monthly` | From the day after the previous occurrence up to the next one | Rolls on to the next month. A 31st falls on the last day of a shorter month |
| `weekly` | The 6 days before the next occurrence of that weekday, and the day itself | Rolls on to the next week |

For a repeating countdown the date is the first occurrence and may lie in the past, so a birthday can be entered with the year of birth.

The texts are available in en, ar, da, de, es, fi, fr, it, ja, ko, nl, no, pl, pt, ru, sv, tr and zh. Other languages get English.

The name is text the user typed. Do not log the filled URL or send it to analytics.

### Free and Premium Users

Both calendars follow the same [date range](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#date-range) as every other calendar: a free user sees the events of the next 60 days, a Premium user all of them. The `start_at_or_after` and `results` parameters work as usual.

### Unusable Input

A missing, malformed or out-of-range value never causes an error. The request succeeds with an empty calendar. Validate the input in your app before subscribing, using the ranges above, so the user is not left with a calendar that never shows anything.
