## SchedJoules Calendar Service API

This API provides access to the SchedJoules Public Calendar Service. SchedJoules delivers the most comprehensive public calendar service in the world for desktop, web, and mobile applications. We currently deliver over 560.000 complete, accurate, and up-to-date public calendars covering holidays, sports, weather, and financial events in 16 languages.


## SDKs

We provide SDKs for iOS and Android:
* [iOS](https://github.com/schedjoules/ios-public-calendars-sdk)
* [Android](https://github.com/schedjoules/Android-SDK)

Follow the links above for the 5-minute installation documentation.

## Getting Started

You can explore the API using our test user API key:
```
curl 'https://api.schedjoules.com/pages/115673' -v -H 'Authorization: Token token="0443a55244bb2b6224fd48e0416f0d9c"'
```
The test API key grants access to the complete API, but calendar URLs will contain placeholder data. To obtain full access to calendar content, contact us at support@schedjoules.com and we will provide you with a dedicated API key.

## Making a Request
* All requests start with `https://api.schedjoules.com/`
* The API follows REST principles
* All responses are in JSON format
* Appending `.json` to URLs is not required
* The API only accepts HTTPS requests

Use the user's current location as an entry point:
```
GET /pages?locale={ISO 639-1 code}&location={ISO_3166 code}

Optional GET parameters
- locale (if omitted, defaults to 'en')
- location (if omitted, defaults to 'us' unless page_id is used)
```

Or navigate directly to a page using its page_id:
```
GET /pages/{page_id}&locale={ISO 639-1 code}

Required GET parameters
- page_id

Optional GET parameters
- locale                    string (if omitted, defaults to 'en')
```

[ISO 639-1 language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
[ISO 3166 country codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)

When using a region setting for the locale (e.g., `de_DE`), only the language portion (`de`) is used to determine the response language.

### Headers
#### Versioning
The API version must be specified in the request header. The current version is `v1`. If no version header is provided, the API defaults to version 1.
```
curl 'https://api.schedjoules.com/pages/115673' -v -H 'Authorization: Token token="0443a55244bb2b6224fd48e0416f0d9c"' -H "Accept: application/vnd.schedjoules; version=1"
```
Labels may be added without a version change, so ensure your client is flexible enough to handle new labels gracefully. Follow our [Twitter feed](http://twitter.com/schedjoules) for the latest SchedJoules news, including API updates. You will also be notified by email of API changes once your account is set up.

#### Authentication
An API key is required to use this API. You can obtain your API key by contacting us at support@schedjoules.com. The API key must be included in the request header.

### Pages
The API is primarily built around the concept of pages. A page represents a view in your application — for example, a football page would list all teams in a league, allowing users to select their favourite team and add its matches to their calendar.

A page has a name and metadata including a `page_section`. Page sections function as headers or groupings within a page. Each page section contains items with an `item_class` of either `calendar` or `page`.

A `page` item is a child page of the current page. For example, "English Football" is a sub-page of "All Football", and "Premier League" is a sub-page of "English Football".

A `calendar` item represents the actual calendar content. This is where users can view event data and subscribe to a calendar in their calendar application.

## Caching
We strongly recommend caching responses wherever possible. This will improve your application's performance and reduce unnecessary bandwidth usage.
* All responses include an `ETag` or `Last-Modified` header. Use `If-Modified-Since` and `If-None-Match` in your requests accordingly.
* Icon URLs in the JSON response include their ETag in the response.

## Unique Anonymous User Identifier
Before presenting a calendar to your users, you must append the calendar URL client-side with a unique anonymous user identifier: `&u={unique_anonymous_user_identifier}`. This is used for statistical purposes and to detect and prevent misuse of our content.

## More Information
* [Pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md)
* [In-app Purchases and Accounts](https://github.com/schedjoules/calendar-store-api/edit/master/details/accounts.md)
* [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md)
* [Countries](https://github.com/schedjoules/calendar-store-api/blob/master/details/countries.md)
* [Languages/Locales](https://github.com/schedjoules/calendar-store-api/blob/master/details/languages.md)
* [Search](https://github.com/schedjoules/calendar-store-api/blob/master/details/search.md)
* [Top, New, Next](https://github.com/schedjoules/calendar-store-api/blob/master/details/top_new_next.md)
* [Weather](https://github.com/schedjoules/calendar-store-api/blob/master/details/weather.md)
* [Alarms](https://github.com/schedjoules/calendar-store-api/blob/master/details/alarms.md)
* [FAQ](https://github.com/schedjoules/calendar-store-api/blob/master/details/faq.md)

## Rate Limits
There are currently no rate limits. Requests are monitored, and we may reach out if we identify opportunities to help you optimize your integration.

## Data Usage and Restrictions
By using this API, you acknowledge that all accessed data is proprietary. The data and images may not be used for any purpose beyond what has been agreed upon. Data may not be stored in any database other than on a user's client device for performance purposes.

## Feedback and Support
If you have a feature request or have found a bug, please open a GitHub issue or send us an email at support@schedjoules.com.
