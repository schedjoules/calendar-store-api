## SDKs (deprecated)

SchedJoules used to publish SDKs for iOS and Android. Both are deprecated and no longer maintained:

| SDK | Repository | Status |
|---|---|---|
| iOS | [ios-public-calendars-sdk](https://github.com/schedjoules/ios-public-calendars-sdk) | Deprecated, last updated March 2024 |
| Android | [android-public-calendars-sdk](https://github.com/schedjoules/android-public-calendars-sdk) | Deprecated and archived, last updated April 2023 |

Do not start a new integration on them. They do not follow later API changes and will not receive fixes.

Integrate the REST API directly instead: start with the [README](https://github.com/schedjoules/calendar-store-api#request-basics), then [Pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md) and [Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md).

If you use a coding agent, point it at [llms-full.txt](https://github.com/schedjoules/calendar-store-api/blob/master/llms-full.txt), which holds the whole API description in one file, and tell it not to use the SDKs.
