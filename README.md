## SchedJoules Calendar Service API

This API provides access to the SchedJoules Public Calendar Service: public calendars for holidays, sports, TV, weather, financial events and more, for desktop, web and mobile applications, in 18 languages.

**New here? Start with the [Integration Guide](https://github.com/schedjoules/calendar-store-api/blob/master/details/integration_guide.md).** Reading this with a coding agent? Give it [AGENTS.md](https://github.com/schedjoules/calendar-store-api/blob/master/AGENTS.md) and [llms-full.txt](https://github.com/schedjoules/calendar-store-api/blob/master/llms-full.txt), which holds every page in one file. Example responses and feeds are in [examples/](https://github.com/schedjoules/calendar-store-api/tree/master/examples).

## SDKs

The iOS and Android SDKs and the Swift client library are deprecated: integrate the REST API directly. See [SDKs](https://github.com/schedjoules/calendar-store-api/blob/master/details/sdks.md).

## Set Yourself Up

An API key is required. Request one at support@schedjoules.com.

You can explore the API with our test API key:
```
curl 'https://api.schedjoules.com/pages/115673' -H 'Authorization: Token token="0443a55244bb2b6224fd48e0416f0d9c"'
```
The test key gives access to the complete API, but every calendar URL it returns serves the same feed (Moon Phases). Your own key returns the real calendars.

## Request Basics

| | |
|---|---|
| Base URL | `https://api.schedjoules.com/` |
| Authentication | Header `Authorization: Token token="{YOUR_API_KEY}"` |
| Format | JSON. Appending `.json` to a URL is not required |
| Transport | HTTPS. A plain HTTP request is redirected to HTTPS |
| Redirects | `GET /pages` answers with a `302` to the page it resolves to. Follow redirects |

A missing or unknown API key returns `401`:
```json
{"errors": {"status": 401, "title": "Invalid API key", "detail": "https://github.com/schedjoules/calendar-store-api#set-yourself-up"}}
```

### Versioning
There is one version, `v1`. You may send `Accept: application/vnd.schedjoules; version=1`, but it is optional and currently every request is served by v1.

Fields may be added to responses without a version change, so make sure your client ignores fields it does not know.

### Language
The response language is taken from, in this order:
1. the `locale` parameter
2. the `x-locale` header
3. the `Accept-Language` header

Only the first two letters are used, so `de_DE` and `de-AT` both mean `de`. `nb` is read as `no`. A language the API does not support falls back to English. See [Languages](https://github.com/schedjoules/calendar-store-api/blob/master/details/languages.md) for the list.

## Pages
The API is built around pages. A page represents a view in your application: for example, a football page lists all teams in a league, so the user can pick a team and add its matches to their calendar.

Start from the user's location:
```
GET /pages?locale={ISO 639-1 code}&location={ISO 3166 code}

Optional GET parameters
- locale        language of the response (see Language above)
- location      ISO 3166-1 alpha-2 country code. Without it, or with an unknown one,
                you get the default catalogue of your API key, or the general
                "All Calendars" page
```

Or open a page by its id:
```
GET /pages/{page_id}?locale={ISO 639-1 code}
```

[ISO 639-1 language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) · [ISO 3166 country codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)

A page has a name and a list of `page_sections`. A section works as a header or grouping within the page, and holds items whose `item_class` is either `page` or `calendar`:
* A `page` item is a child page. For example, "English Football" is a child of "All Football", and "Premier League" is a child of "English Football".
* A `calendar` item is the calendar itself: its `url` is the feed your user subscribes to.

See [Pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md) for the full response format.

## Unique Anonymous User Identifier
Before presenting a calendar URL to your users, append a unique anonymous user identifier to it: `&u={unique_anonymous_user_identifier}`. It is used for statistics and to detect and prevent misuse of our content. Use the same identifier for the same user everywhere, including the [Accounts API](https://github.com/schedjoules/calendar-store-api/blob/master/details/accounts.md).

## Caching
Cache responses wherever possible.
* API responses carry an `ETag` and a `Last-Modified` header, and answer `304 Not Modified` to a matching `If-None-Match` or `If-Modified-Since`.
* They are sent with `Cache-Control: max-age=0, private, must-revalidate`: keep your copy, but revalidate it before using it again.

## More Information
* [Integration Guide](https://github.com/schedjoules/calendar-store-api/blob/master/details/integration_guide.md)
* [Android](https://github.com/schedjoules/calendar-store-api/blob/master/details/android.md)
* [iOS](https://github.com/schedjoules/calendar-store-api/blob/master/details/ios.md)
* [A Basic UI](https://github.com/schedjoules/calendar-store-api/blob/master/details/ui.md)
* [Embedding the Catalogue in an Existing App](https://github.com/schedjoules/calendar-store-api/blob/master/details/embedding.md)
* [Pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md)
* [In-app Purchases and Accounts](https://github.com/schedjoules/calendar-store-api/blob/master/details/accounts.md)
* [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md)
* [Pregnancy and Countdown Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/user_input_calendars.md)
* [Countries](https://github.com/schedjoules/calendar-store-api/blob/master/details/countries.md)
* [Languages](https://github.com/schedjoules/calendar-store-api/blob/master/details/languages.md)
* [Search](https://github.com/schedjoules/calendar-store-api/blob/master/details/search.md)
* [Top, New, Next](https://github.com/schedjoules/calendar-store-api/blob/master/details/top_new_next.md)
* [Weather](https://github.com/schedjoules/calendar-store-api/blob/master/details/weather.md)
* [Alarms](https://github.com/schedjoules/calendar-store-api/blob/master/details/alarms.md)
* [SDKs (deprecated)](https://github.com/schedjoules/calendar-store-api/blob/master/details/sdks.md)
* [Deprecations and Changes](https://github.com/schedjoules/calendar-store-api/blob/master/details/deprecation_and_changes.md)
* [FAQ](https://github.com/schedjoules/calendar-store-api/blob/master/details/faq.md)

## Rate Limits
There are currently no rate limits. Requests are monitored, and we may reach out if we see a way to make your integration more efficient.

## Data Usage and Restrictions
By using this API, you acknowledge that all accessed data is proprietary. The data and images may not be used for any purpose beyond what has been agreed upon. Data may not be stored in any database other than on a user's client device for performance purposes.

## Feedback and Support
If you have a feature request or have found a bug, open a GitHub issue or email support@schedjoules.com.
