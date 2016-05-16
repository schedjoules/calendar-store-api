##Weather

### Calendar requests

We provide data for 150.000 locations worldwide; 14 days ahead. Since the information is used in the calendar the information is all flat text. In the JSON returned by the [pages resource](https://github.com/schedjoules/calendar-store-api/) you'll notice a url that looks like:

```
GET /calendars/weather/calendar.ics?l={locale}&loc={location}&d={temp}&p={rain}&w={wind}&t={time}

Required GET parameters
- loc	location		location_id returned by GET /cities/cities_within_bounds (see below)

Optional GET parameters
- l 	locale			ISO 639-1 language code (default: 'en')
- d		temperature		c, f (default: 'c')
- p 	precipitation	mm, in (default: 'mm')	
- w		wind speed		kmh, kts, ms, mph (default: 'kmh')
- t		time format		12, 24 (default: 24)
```

You can access these (and localised) parameters via:

```
GET /cities/weather_settings

Optional GET parameters
- locale 				(default: 'en')
```

By using the location parameter the defaults for that location are returned. For example when requesting location=us the default temperature setting will be returned as Fahrenheit.

The weather information returned in the user's calendar is:
* Daily max/min temperature for the day
* Daily rainfall + chance
* Daily sunrise & sunset times
* Daily UV index
* Per 6 hours: temperature, wind speed, wind direction

###Plot locations based on the user's location
Your app can access the {location} parameter by making a request to

```
GET /cities/cities_within_bounds?ne=4.363991,-1.150881&sw=-1.567068,8.39353

Required GET parameters
- ne
- sw
```
The ne and sw parameters should be replaced by the north-east and south-west coordinates of the user's screen. The response will contain the 30 most popular weather stations in the users view. An example response:
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
This response provides the location_name (to), the location_coordinates(la,lo) and the location_id (fo). The ty label tells you if the returned marker is (c)lustered or (i)ndividual. Clustered markers can be zoomed into and will show more markers.