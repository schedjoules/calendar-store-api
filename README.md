##SchedJoules Calendar Store API
With this API you can get access to the SchedJoules Public Calendar Library. SchedJoules delivers the most comprehensive public desktop, web and mobile calendar store in the world. We currently deliver over 180.000 complete, accurate and timely public calendars for holidays, sports, weather and financial events. We do so in 40 languages.

For iOS we have a **SDK** that uses all the API goodies. For the 5 minute SDK install [check out](http://schedjoules.com/resources/developer-resources/ios/CalendarStoreDocumentation/index.html) the documentation. Of course you are more than welcome to implement the API without using the SDK. If so please read on.

##Set yourself up
You can take a peek at the API by using our test user API key:
```
curl -L 'https://api.schedjoules.com/pages/115673' -v -H 'Authorization: Token token="0443a55244bb2b6224fd48e0416f0d9c"'
```
The test API key gives you access to the complete API but the calendar urls will contain dummy data. If you like what you see and want full access to the calendar content as well mail us at support@schedjoules.com and we'll provide you with your API key.

##Making a request
* All requests start with https://api.schedjoules.com/
* We use REST methodology for the API
* All output  is in JSON format
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
- locale (if omitted defaults to 'en')
```

[ISO 639-1 language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)  
[ISO_3166 country codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)

Using the user's region setting for setting the locale is accepted but only the language part (for 'de_DE' => 'de') is used to return the correct language.  

###Headers
####Versioning
The API version needs to be set in the request header. Current version is: `v1`. If you don't set headers and the default version is bumped your application might not function. Labels can be added without version change so make your client flexible enough to handle that. Follow our [twitter feed](http://twitter.com/schedjoules) for latest SchedJoules' news, also on the API. We'll email you with API changes as well once you are set up.

####Authentication
You will need an API key to use this API. You can get your API key by contacting us at support@schedjoules.com. You need to set the API key in the header.

###Pages
The API is mainly build around the concept of pages. Visualise a page in your application for eg football.That page would have all the names of all the teams in a league from which users can select their favourite team of which to want to add all matches to their calendar.

A page has a name and meta data like its name and page_section. Think of page sections as headers or paragraphes. A page section has a name. Within the page_section are the items wich have an item_class. And item_class is either a 'calendar' or a 'page'.

A page is, not very surprisingly, a child page of the page the user is looking at. Think of English Football being a (sub)page of All Football and Premier League being a (sub)page of English Football.

An item_class calendar is where the magic happens. This is where the user gets to see the actual data in the calendar file and can add that calendar to his of her calendar application.

##Caching
Do your clients, yourself and us a favor and cache where you can. It will speed up your app and save bandwidth.
* All requests we return will include an `ETag` or `Last-Modified` header so use `If-Modified-Since` and `If-None-Matched` in you requests.
* Icon urls that are in the JSON have their ETag mentioned in de response.

##More Information
Check out the following pages for more information:
* [Pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md)
* [In App Purchases and Subscriptions](https://github.com/schedjoules/calendar-store-api/blob/master/details/in_app_purchases.md)
* [Countries](https://github.com/schedjoules/calendar-store-api/blob/master/details/countries.md)
* [Search](https://github.com/schedjoules/calendar-store-api/blob/master/details/search.md)
* [Top, next, new](https://github.com/schedjoules/calendar-store-api/blob/master/details/top_next_new.md)
* [Weather](https://github.com/schedjoules/calendar-store-api/blob/master/details/weather.md)
* [Questions and Answers](https://github.com/schedjoules/calendar-store-api/blob/master/details/faq.md)

##Rate limits
There are no rate limits. We do count requests. If we think we can help you improve we will contact you.

##Just to make sure there is no misunderstanding ...
By using our API it is clear to you that all the data you access is proprietary. The data and images can not be used for any other purpose then agreed upon. Data can't be stored in any database other than on a users client for performance purposes.

##Help Us
Please tell us how we can make the API better. If you have a specific feature request or if you find a bug, please use GitHub issues or send us an email at info@schedjoules.com.
