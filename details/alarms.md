## Alarms

Calendar events in different categories have the following default alarm offsets:

* Holidays — 720 minutes (12 hours)
* Sports — 30 minutes
* TV — 30 minutes
* Finance — 720 minutes (12 hours)
* Moon phases / name days — no alarm

These defaults are based on user feedback and usage data. You can override these defaults, or allow your end-users to do so. To override, append the calendar URL with `&al={alarm_in_minutes}` — for example, `&al=48` will trigger an alarm 48 minutes before `DTSTART`. Negative values will trigger the alarm after `DTSTART`. To disable alarms entirely, append `&al=none`.
