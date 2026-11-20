## iOS

On iOS there are two ways to get a SchedJoules calendar into the user's calendar. Pick one before you write code: they lead to different apps. Read the [Integration Guide](https://github.com/schedjoules/calendar-store-api/blob/master/details/integration_guide.md) first.

| | Subscribed calendar (webcal) | Your app writes events (EventKit) |
|---|---|---|
| How | Open the feed URL with the `webcal://` scheme; iOS asks the user to confirm and then owns the calendar | Your app fetches the feed and writes events into a calendar it created with EventKit |
| Who refreshes | iOS, on its own schedule, without your app running | Your app, only when iOS lets it run |
| Effort for a v0.1 | Very small | Substantial |
| Freshness | Steady, independent of how often your app is opened | Depends on app opens, background refresh and pushes; can lag for users who rarely open your app |
| Personalisation (hide events, own alarms, combine sources) | Not possible | Possible |
| Removing the calendar | The user removes it in Settings or Calendar; your app cannot | Your app can |
| Calendar permission | Not needed | Needed (full access) |

For a v0.1, start with webcal: it works in an afternoon. Move to EventKit when you need personalisation.

### Webcal subscription

1. Build the feed URL as in the [Integration Guide](https://github.com/schedjoules/calendar-store-api/blob/master/details/integration_guide.md#step-3-build-the-feed-url) (item `url` plus `&u=`).
2. Replace the scheme: `https://` becomes `webcal://`.
3. Open it with `UIApplication.shared.open(url)`. iOS shows its subscribe dialog.

Your app does not learn whether the user confirmed. To show "subscribed" in your UI, look for a calendar of type `.subscription` with the same title through EventKit afterwards, or simply keep your own list.

### EventKit

* Ask for calendar access (`requestFullAccessToEvents`) when the user subscribes to their first calendar, after explaining why; never at app start.
* Create one `EKCalendar` per subscription, on a writable source (iCloud or local), and keep its `calendarIdentifier` with the subscription.
* Map each feed event to an `EKEvent` and keep a map from the feed `UID` to the event's identifier. Apply changes by UID as the guide describes: add, update, delete only from complete feeds.
* All-day events: set `isAllDay` and use the date as given; do not shift it through a time zone.

**Refreshing.** iOS decides when your app may run in the background:
* Sync when the app starts and when it comes to the foreground.
* Schedule a `BGAppRefreshTask`. iOS runs it at its own discretion; do not count on a time.
* Silent pushes (`content-available`, priority 5) can wake your app, but Apple does not guarantee their delivery and asks for no more than two or three per hour.
* Nothing wakes your app when the user opens the Calendar app.

So freshness for EventKit users depends on how often they open your app. Plan for that: it is the main reason to start with webcal.
