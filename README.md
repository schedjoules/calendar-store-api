## SchedJoules Calendar Service API
With this API you can get access to the SchedJoules Public Calendar Service. SchedJoules delivers the most comprehensive public calendar service in the world for desktop, web and mobile applications. We currently deliver over 560.000 complete, accurate and timely public calendars for holidays, sports, weather and financial events. We do so in 16 languages.


## SDKs
We provide SDK's for iOS and Android:
* [iOS](https://github.com/schedjoules/ios-public-calendars-sdk)
* [Android](https://github.com/schedjoules/Android-SDK)

Follow the links above for the 5-minute-install documentation.

## Set yourself up
You can take a peek at the API by using our test user API key:
```
curl 'https://api.schedjoules.com/pages/115673' -v -H 'Authorization: Token token="0443a55244bb2b6224fd48e0416f0d9c"'
```
The test API key gives you access to the complete API but the calendar urls will contain dummy data. If you like what you see and want full access to the calendar content as well you can send us an email at support@schedjoules.com and we'll provide you with your own dedicated API key.

## Making a request
* All requests start with https://api.schedjoules.com/
* We use REST methodology for the API
* All output is in JSON format
* Appending URLs with .json is not mandatory
* The API only accepts HTTPS requests

Use the user's current location as an entry point:
```
GET /pages?locale={ISO 639-1 code}&location={ISO_3166 code}

Optional GET parameters
- locale (if omitted defaults to 'en')
- location (if omitted defaults to 'us' unless page_id is used)
```

Or if you know the page_id go directly to that page
```
GET /pages/{page_id}&locale={ISO 639-1 code}

Required GET parameters
- page_id

Optional GET parameters
- locale 					string (if omitted defaults to 'en')
```

[ISO 639-1 language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) 
[ISO_3166 country codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)

Using the user's region setting for setting the locale is accepted but only the language part (for 'de_DE' => 'de') is used to return the correct language.

### Headers
#### Versioning
The API version needs to be set in the request header. Current version is: `v1`. If you don't set headers the API will presume that you use version 1. 
```
curl 'https://api.schedjoules.com/pages/115673' -v -H 'Authorization: Token token="0443a55244bb2b6224fd48e0416f0d9c"' -H "Accept: application/vnd.schedjoules; version=1"
```
Labels can be added without version change so make your client flexible enough to handle that. Follow our [twitter feed](http://twitter.com/schedjoules) for latest SchedJoules' news, also on the API. We'll email you with API changes as well once you are set up.

#### Authentication
You will need an API key to use this API. You can get your API key by contacting us at support@schedjoules.com. You need to set the API key in the header.

### Pages
The API is mainly build around the concept of pages. Visualise a page in your application for eg football.That page would have all the names of all the teams in a league from which users can select their favourite team of which to want to add all matches to their calendar.

A page has a name and meta data like its name and page_section. Think of page sections as headers or paragraphes. A page section has a name. Within the page_section are the items wich have an item_class. And item_class is either a 'calendar' or a 'page'.

A page is, not very surprisingly, a child page of the page the user is looking at. Think of English Football being a (sub)page of All Football and Premier League being a (sub)page of English Football.

An item_class calendar is where the magic happens. This is where the user gets to see the actual data in the calendar file and can add that calendar to his of her calendar application.

## Caching
Do your clients, yourself and us a favor and cache where you can. It will speed up your app and save bandwidth.
* All requests we return will include an `ETag` or `Last-Modified` header so use `If-Modified-Since` and `If-None-Match` in you requests.
* Icon urls that are in the JSON have their ETag mentioned in de response.

## Calendars
The calendars are by default in the iCalendar data format ([RFC5545](https://tools.ietf.org/html/rfc5545)) but we also provide calendars in jCal ([RFC7265](https://tools.ietf.org/html/rfc7265)) and xCal ([RFC6321](https://tools.ietf.org/html/rfc6321)). Many OS's and calendar clients parse calendar files but, of course, you can also write your own parser.

As said the default calendar format is .ics. To get a calendar in either jCal or xCal format add extension .json or .xml:
* iCal: .../calendars/766e8a162f82
* jCal: .../calendars/766e8a162f82.json
* xCal: .../calendars/766e8a162f82.xml

## Unique anonymous user identifier
Before you can offer calendar to your users you need to append the calendar url client side with a unique anonymous user identifier: &u={unique_anonymous_user_identifier}. We use this for statistical purposes and for detecting and preventing of misuse of our content.

## More Information
Check out the following pages for more information:
* [Pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md)
* [In-app Purchases and Accounts](https://github.com/schedjoules/calendar-store-api/edit/master/details/accounts.md)
* [Countries](https://github.com/schedjoules/calendar-store-api/blob/master/details/countries.md)
* [Languages/locales](https://github.com/schedjoules/calendar-store-api/blob/master/details/languages.md)
* [Search](https://github.com/schedjoules/calendar-store-api/blob/master/details/search.md)
* [Top, new, next](https://github.com/schedjoules/calendar-store-api/blob/master/details/top_new_next.md)
* [Weather](https://github.com/schedjoules/calendar-store-api/blob/master/details/weather.md)
* [Alarms](https://github.com/schedjoules/calendar-store-api/blob/master/details/alarms.md)
* [FAQ](https://github.com/schedjoules/calendar-store-api/blob/master/details/faq.md)

## Rate limits
There are no rate limits. We do count requests. If we think we can help you improve we will contact you.

## Just to make sure there is no misunderstanding ...
By using our API it is clear to you that all the data you access is proprietary. The data and images can not be used for any other purpose then agreed upon. Data can't be stored in any database other than on a users client for performance purposes.

## Help Us
Please tell us how we can make the API better. If you have a specific feature request or if you find a bug, please use GitHub issues or send us an email at support@schedjoules.com.
