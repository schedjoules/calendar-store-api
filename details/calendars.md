## Calendars
The calendars are by default in the iCalendar data format ([RFC5545](https://tools.ietf.org/html/rfc5545)) but we also provide calendars in jCal ([RFC7265](https://tools.ietf.org/html/rfc7265)) and xCal ([RFC6321](https://tools.ietf.org/html/rfc6321)). Many OS's and calendar clients parse calendar files but, of course, you can also write your own parser.

As said the default calendar format is .ics. To get a calendar in either jCal or xCal format add extension .json or .xml:
* iCal: .../calendars/766e8a162f82
* jCal: .../calendars/766e8a162f82.json
* xCal: .../calendars/766e8a162f82.xml

### Remove results from calendar summary
Some users don't want to see the results of sport events in the calendar summary because they want to watch the game later without knowing the score. You can provide this by setting the show_result parameter.
```
GET /calendar/d2b1e319a12a?show_result=false

Optional GET parameters
- show_result (if omitted defaults to 'true')
```
