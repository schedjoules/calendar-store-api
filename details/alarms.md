## Alarms

Events in the iCalendar feed carry a default alarm that depends on the type of calendar:

| Calendar | Default alarm |
|---|---|
| Sports | 30 minutes before |
| TV | 30 minutes before |
| Moon phases, name days, week numbers, day numbers | 30 minutes before |
| Finance | 720 minutes (12 hours) before |
| Public holidays | none |
| School holidays | 720 minutes before for most countries, 30 minutes before in the UK |
| Weather, pregnancy, countdown | none |

You can override the default, or let your users do so, with the `al` parameter on the calendar URL:

| Value | Effect |
|---|---|
| `al=48` | Alarm 48 minutes before the start of each event |
| `al=-15` | Alarm 15 minutes after the start |
| `al=0` | Alarm at the start. Any value that is not a number has the same effect |
| `al=none` | No alarms |

`al` also adds alarms to calendars that have none by default. It only applies to the iCalendar format: jCal and xCal responses contain no alarms.
