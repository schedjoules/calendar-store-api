##Weather

In the JSON returned by the [pages resource](https://github.com/schedjoules/calendar-store-api/) you'll notice a url that looks like
```
http://{your_name}.schedjoules.com/cities/full/%TEMP%/%LANGUAGE%/%RAIN%/%WIND%/%TIME%/%CITY%.ics?x={your_app_code}
```

All parameters except for the %CITY% can be set by your users in your app.

These parameters can be accessed via:

```
GET /cities/weather_settings

Optional GET parameters
- locale (if omitted defaults to 'en')
```

Your app can access the %CITY% parameter by making a request to

```
GET /cities/cities_within_bounds?ne=4.363991,-1.150881&sw=-1.567068,8.39353

Required GET parameters
- ne
- sw
```
whereby the ne and sw parameters should be replaced by the north-east and south-west coordinates of the user's screen. 

Your request will be responded with the 30 most popular weather station in the users view. The response might look like:
```
{
fo = 101735161;
la = "3.17";
lo = "101.7";
to = "Kuala Lumpur";
ty = i;
}
```
This response provides the location_name (to), the location_coordinates(la,lo) and the location_id (fo). The ty label tells you if the returned marker is (c)lustered or (i)ndividual. Clustered markers can be zoomed into and will show more markers. 

We are working on API method that will return the closest location based on the user home or work address