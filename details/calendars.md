## Calendars

Calendars are provided in iCalendar format ([RFC 5545](https://tools.ietf.org/html/rfc5545)) by default. We also support jCal ([RFC 7265](https://tools.ietf.org/html/rfc7265)) and xCal ([RFC 6321](https://tools.ietf.org/html/rfc6321)). Most operating systems and calendar clients can parse calendar files natively, though you may also implement your own parser.

The default calendar format is `.ics`. To request a calendar in jCal or xCal format, append the appropriate file extension:
* iCal: `.../calendars/766e8a162f82`
* jCal: `.../calendars/766e8a162f82.json`
* xCal: `.../calendars/766e8a162f82.xml`

### Hiding Sport Event Results
Some users prefer not to see sport event results in their calendar summary — for example, if they intend to watch the event later and want to avoid spoilers. This behaviour can be controlled via the `show_result` parameter.

```
GET /calendar/d2b1e319a12a?show_result=false

Optional GET parameters
- show_result (if omitted, defaults to 'true')
```
