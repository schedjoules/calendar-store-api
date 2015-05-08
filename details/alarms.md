##Alarms

The events in the calendars in the different categories have different default alarms:
* holidays - 720m (12h)
* sports - 30m
* tv - 30m
* finance - 720m (12h)
* moon phases/name days - no alarm

These defaults are based on our experience and user feedback. You can overwrite these defaults or let your end user overwrite them. To do so append the calendar url with &al={alarm_in_minutes} eg &al=48 to have an alarm go off 48 minutes before DTSTART. You can use negative values if you choose the alarm to sound after DTSTART or use &al=none to remove alarms.
