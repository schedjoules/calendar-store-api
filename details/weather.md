## Weather

### Calendar Requests

We provide weather data for 150.000 locations worldwide, always 14 days ahead. Since the data is presented within a calendar, all information is returned as plain text. In the JSON returned by the [pages resource](https://github.com/schedjoules/calendar-store-api/), you will find a URL in the following format:

```
GET /calendars/weather/calendar.ics?l={locale}&loc={location}&d={temp}&p={rain}&w={wind}&t={time}

Required GET parameters
- loc   location        location_id returned by GET /cities/cities_within_bounds (see below)

Optional GET parameters
- l     locale          ISO 639-1 language code (default: 'en')
- d     temperature     c, f (default: 'c')
- p     precipitation   mm, in (default: 'mm')
- w     wind speed      kmh, kts, ms, mph (default: 'kmh')
- t     time format     12, 24 (default: 24)
```

You can retrieve the available (and localised) parameter options via:

```
GET /cities/weather_settings

Optional GET parameters
- locale            (default: 'en')
```

When the `location` parameter is provided, the defaults for that location are returned. For example, requesting `location=us` will return Fahrenheit as the default temperature unit.

The weather information included in the calendar is:
* Daily maximum/minimum temperature
* Daily rainfall amount and probability
* Daily sunrise and sunset times
* Daily UV index
* Per 6-hour interval: temperature, wind speed, and wind direction

### Plotting Locations Based on the User's Location
Your app can retrieve available weather station locations by making the following request:

```
GET /cities/cities_within_bounds?ne=4.363991,-1.150881&sw=-1.567068,8.39353

Required GET parameters
- ne
- sw
```

The `ne` and `sw` parameters represent the north-east and south-west coordinates of the user's visible map area. The response will contain the 30 most popular weather stations within that area. Example response:

```
...
{
    la: -1.4,
    lo: 31.73,
    fo: 100158179,
    ty: "c",
    to: "Katerero"
},
{
    la: 2.57,
    lo: -72.64,
    fo: 103828545,
    ty: "i",
    to: "San Jose del Guaviare"
}
...
```

Each entry includes the location name (`to`), coordinates (`la`, `lo`), and location ID (`fo`). The `ty` label indicates whether the marker is (c)lustered or (i)ndividual. Clustered markers can be expanded by zooming in to reveal additional individual markers.
