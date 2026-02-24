## In-app Purchases and Accounts

You can configure the API to require end-users to pay for calendar content. In that case, you will likely want to integrate In-App Purchases. We offer several approaches for handling this.

The easiest approach is to use one of our [SDKs](https://github.com/schedjoules/calendar-store-api/blob/master/README.md#sdks). Payment processing and calendar management are handled entirely within the SDK, allowing you to get up and running quickly. If you choose not to use one of the SDKs, you gain more flexibility through the Account API. The Account API allows you to control calendar behaviour and user access across multiple devices.

### Editing Subscriptions
An important consideration when developing on iOS or macOS is that calendar subscriptions are managed by the operating system, not your application. The only way to prevent end-users from accessing calendar subscriptions after their subscription has expired is to notify the Account API of the expiration. You can set or update the expiration date with the following request:

```
curl -X POST https://api.schedjoules.com/accounts/{UUID}/licenses -H "Content-Type: application/json" -H 'Authorization: Token token="{YOUR_API_KEY}"' -d '{"{NAME_SPACE}:{UUID}": {"expiration_date": "{EXPIRATION_DATE}"}}'
```

* `unique_anonymous_user_identifier`: Must be unique per user within your implementation and must match the identifier appended to the [calendar URI](https://github.com/schedjoules/calendar-store-api#unique-anonymous-user-identifier).
* `namespace`: Can be any string, such as your company name.
* `expiration_date`: ISO 8601 format in UTC, e.g., `2018-06-05T18:47:05Z`.

### Upcoming Features
* Freemium offerings
* Set the number of calendars accessible within a user's purchased tier
* Sync calendars and settings (colour, alarms) across multiple devices
