## In-app Purchases and Accounts

You can choose to have your end-users pay for using the content of the API. In that case you probably want to work with In App Purchases. We offer different flavours of handling this.

By far the easiest way is to use on of our [SDKs](https://github.com/schedjoules/calendar-store-api/blob/master/README.md#sdks). Payment and operational handling of calendars is handled in the SDK. Another advantages is that you are up and running quickly. In case you do not use one of the SDKs you gain flexibility. For those case we have developed the account API. With the account API you can influence the behaviour of calendars and users over multiple device.

### Editing Subscriptions
Important to remember when you are developing on iOS or MacOS is that the actual calendar subscription is handled by the OS; not your application. The only way to stop end-users from using calendar subscriptions after their subscription has ended is by telling the account API the subscription has expired. You can set and change the expiration date by this request

```
curl -X POST https://api.schedjoules.com/accounts/{UUID}/licenses -H "Content-Type: application/json" -H 'Authorization: Token token="{YOUR_API_KEY}"' -d '{"{NAME_SPACE}:{UUID}": {"expiration_date": "{EXPIRATION_DATE}"}}'
```

* unique_anonymous_user_identifier: needs to be unique per user for your implementation and is the same as is appended to the [calendar URI](https://github.com/schedjoules/calendar-store-api#unique-anonymous-user-identifier)
* namespace: can be anything eg your company name
* expiration_date: ISO8601 format UTC eg 2018-06-05T18:47:05Z

### Other upcoming features
* freemium offerings
* set number of calendars that user has access to within his purchased tier
* sync calendars and settings (color, alarms) over multiple devices
