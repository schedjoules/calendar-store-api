##Weather

In the JSON returned by the [pages resource](https://github.com/schedjoules/calendar-store-api/) you'll notice a url that looks like: *

```
http://{your_name}.schedjoules.com/calendars/weather/calendar.ics?l={language}&loc={location}&d={temp}&p={rain}&w={wind}&t={time}&x={your_app_code} 
```
This is the base URI for adding weather information to a calendar. All parameters except for the {location} can be set by your users in your app.

These parameters can be accessed via:

```
GET /cities/weather_settings

Optional GET parameters
- locale (if omitted defaults to 'en')
```

Your app can access the {location} parameter by making a request to

```
GET /cities/cities_within_bounds?ne=4.363991,-1.150881&sw=-1.567068,8.39353

Required GET parameters
- ne
- sw
```
whereby the ne and sw parameters should be replaced by the north-east and south-west coordinates of the user's screen. 

Your request will be responded with the 30 most popular weather station in the users view. The response might contain:
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

We are working on API method that will return the closest location based on the user home or work address

\* For older versions of our API this is:
```
http://{your_name}.schedjoules.com/cities/full/%TEMP%/%LANGUAGE%/%RAIN%/%WIND%/%TIME%/%CITY%.ics?x={your_app_code}
```