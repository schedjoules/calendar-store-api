## Weather

### Calendar Requests

The weather calendar is a forecast for one location, 16 days ahead, with one all-day event per day. Its `url` in a pages response is a template your app fills in:

```
GET /calendars/weather/calendar.ics?l={locale}&loc={location}&d={temp}&p={rain}&w={wind}&t={time}

Required GET parameters
- loc   location        location_id from GET /cities/search or GET /cities/cities_within_bounds (below)

Optional GET parameters
- l     locale          ISO 639-1 language code (default: 'en')
- d     temperature     c, f (default: 'c')
- w     wind speed      kmh, kts, ms, mph (default: 'kmh')
- t     time format     12, 24 (default: 24)
- p     precipitation   mm, in. Accepted, but has no effect: the calendar shows no precipitation
- h     hourly          1 = one detail line per hour for the first 96 hours instead of one per 3 hours
```

Each day's event contains:
* in the title: the day's minimum and maximum temperature and a short description of the weather;
* in the description: a line every 3 hours (or every hour with `h=1`) with temperature, wind speed and conditions, followed by the day's temperature, humidity and wind range.

### Weather Settings

The units to offer, with localised names and the default for a country:

```
GET /cities/weather_settings?locale={locale}&location={ISO 3166 code}

Optional GET parameters
- locale        (default: 'en')
- location      country whose defaults to return. Only 'us' and 'gb' have their own defaults
```

`GET /cities/weather_settings?locale=en&location=us` returns:

```json
{
  "temp": {"title": "Temperature", "options": {"c": "ºC", "f": "ºF"}, "default": "f"},
  "rain": {"title": "Precipitation", "options": {"mm": "mm", "in": "po"}, "default": "in"},
  "wind": {"title": "Wind Speed", "options": {"kmh": "km/h", "kts": "Knots", "ms": "m/s", "mph": "mph"}, "default": "mph"},
  "time": {"title": "Time format", "options": {"12": "12-hour", "24": "24-hour"}, "default": "12"}
}
```

### Searching Locations by City Name

```
GET /cities/search?q={query}

Required GET parameters
- q         search query, at least 2 characters

Optional GET parameters
- locale    returns city names in this language where available
```

Every word of the query must match the start of a word in the city's name or one of its local names. At most 10 results, ordered by exact name match first, then names that start with the query, then popularity. A query shorter than 2 characters returns an empty array `[]`.

`GET /cities/search?q=Amsterdam` returns (shortened):

```json
{
  "cities": [
    {"country": "nl", "latitude": 52.37, "longitude": 4.9, "name": "Amsterdam", "location_id": 102759794},
    {"country": "ca", "latitude": 51.75, "longitude": -102.47, "name": "Amsterdam", "location_id": 105884628}
  ]
}
```

Use the `location_id` as the `loc` parameter of the calendar URL. `country` is a lowercase ISO 3166 code.

### Locations on a Map

To show weather locations on a map of the area the user is looking at:

```
GET /cities/cities_within_bounds?ne={lat},{lng}&sw={lat},{lng}

Required GET parameters
- ne    north-east corner of the visible map, latitude first
- sw    south-west corner of the visible map, latitude first
```

The API takes the 100 most popular locations in the area and groups nearby ones, so you get at most 30 markers. A north-east longitude smaller than the south-west one is read as an area that crosses the 180° meridian.

`GET /cities/cities_within_bounds?ne=52.5,5.1&sw=52.2,4.7` returns (shortened):

```json
[
  {"la": 52.37, "lo": 4.9, "fo": 102759794, "ty": "i", "to": "Amsterdam"},
  {"la": 52.3, "lo": 4.86, "fo": 102759798, "ty": "i", "to": "Amstelveen"}
]
```

| Field | |
|---|---|
| `la`, `lo` | Latitude and longitude |
| `fo` | The `location_id` |
| `to` | Location name |
| `ty` | `i` for a single location, `c` for a cluster of several. A cluster carries the name and id of one of its locations; zoom in to split it |
