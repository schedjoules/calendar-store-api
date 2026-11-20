## In-app Purchases and Accounts

You can configure the API to require end-users to pay for calendar content. In that case, you will likely want to integrate In-App Purchases. We offer several approaches for handling this.

Use the Account API to control calendar access per user, across multiple devices. (The former SDKs, which handled payments themselves, are [deprecated](https://github.com/schedjoules/calendar-store-api/blob/master/details/sdks.md).)

### Editing Subscriptions
An important consideration when developing on iOS or macOS is that calendar subscriptions are managed by the operating system, not your application. The only way to prevent end-users from accessing calendar subscriptions after their subscription has expired is to notify the Account API of the expiration. You can set or update the expiration date with the following request:

```
curl -X POST https://api.schedjoules.com/accounts/{UNIQUE_ANONYMOUS_USER_IDENTIFIER}/licenses -H "Content-Type: application/json" -H 'Authorization: Token token="{YOUR_API_KEY}"' -d '{"product_id": "{PRODUCT_ID}", "expiration_date": "{EXPIRATION_DATE}"}'
```

* `{UNIQUE_ANONYMOUS_USER_IDENTIFIER}` (in the path): Must be unique per user within your implementation and must match the identifier appended to the [calendar URI](https://github.com/schedjoules/calendar-store-api#unique-anonymous-user-identifier). The account is created on the first request.
* `product_id`: The identifier of the purchased product, such as its App Store or Google Play product ID. Posting the same `product_id` again for a user updates its expiration date.
* `expiration_date`: ISO 8601 format in UTC, e.g., `2018-06-05T18:47:05Z`.

The response lists all licenses of the user:

```
{"account_id": "{UNIQUE_ANONYMOUS_USER_IDENTIFIER}", "licenses": [{"license_id": "{PRODUCT_ID}", "expiration_date": "2018-06-05T18:47:05Z"}]}
```

`GET /accounts/{UNIQUE_ANONYMOUS_USER_IDENTIFIER}/licenses` returns the same response without changing anything. Your API key must be enabled for licenses; otherwise the POST returns `405`. Contact us to enable it.
