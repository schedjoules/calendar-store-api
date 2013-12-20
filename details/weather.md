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
whereby the ne and sw parameters should be replaced by the north-east and south-west coordinates of the user's screen. Your request will be responded with the 30 most popular weather station in the users view. This response provides the location_name, the location_coordinates and a location_id.

We are working on API method that will return the closest location based on the user home or work address