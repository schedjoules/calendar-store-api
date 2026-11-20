## A Basic UI

A v0.1 needs four screens. This is the structure the SchedJoules apps use on iOS and Android, reduced to what a first version needs. Build it with your platform's standard components (lists, tab or navigation bars, switches, sheets); nothing here needs a custom control. Read the [Integration Guide](https://github.com/schedjoules/calendar-store-api/blob/master/details/integration_guide.md) first for the API side.

| Screen | Shows | API |
|---|---|---|
| Browse | The catalogue, one page at a time, with search on top | `GET /pages`, `GET /pages/{id}`, `GET /pages/search` |
| Calendar | One calendar: its name, the next events, a subscribe control | The item from the page, and its feed |
| My calendars | What the user subscribed to | Your own storage |
| Settings | Country and language | `GET /countries`, `GET /languages` |

Put Browse and My calendars in a tab or navigation bar; Settings can be a third tab or sit behind an icon.

### Browse

* Open on the user's home page: `GET /pages?locale={device language}&location={device country}`. Use the page's `name` as the screen title.
* Render each entry of `page_sections` as a list section with its `name` as the header. The first section can have an empty name: show it without a header.
* One row per item: the `icon` on the left, the `name` as the text.
  * `item_class: "page"`: a row with a chevron (or your platform's equivalent) that opens the child page as a new screen, with a back action to the parent.
  * `item_class: "calendar"`: a row that opens the Calendar screen. You may also put a subscribe switch on the row itself, so users can subscribe to several teams without leaving the list.
* `icon` can be `null` or missing. Reserve the space anyway and show a neutral placeholder, so the names stay aligned.
* Show which calendars the user already subscribed to, on the row (a filled switch, a check mark). Match by `item_id`.
* Search at the top of the home page. Send the query after the user typed 3 characters and paused briefly; show the results as one flat list, grouped by category if you like (see [Search](https://github.com/schedjoules/calendar-store-api/blob/master/details/search.md)). Search names can end in a gender sign and a flag to tell teams apart: keep them in the result list, and use `original_name` everywhere else.

Optional for a later version: a "Top" tab with `GET /pages?top=20&location={country}` (see [Top, New, Next](https://github.com/schedjoules/calendar-store-api/blob/master/details/top_new_next.md)), filter chips for the home page's sections.

### Calendar

What the user sees before and after subscribing to one calendar.

* Title: the item's `name` (`original_name` when it came from search).
* A subscribe control at the top: a switch or a button that turns into "Subscribed". Subscribing must give feedback at once; on Android, start the first sync immediately so events appear in the calendar app within seconds.
* Below it, the next events of the feed: fetch it, and list date, time and `SUMMARY` of the next 10 to 20 events, grouped by day. This lets users check that they picked the right team or region before they subscribe, and it is the place where an empty calendar shows "No upcoming events" instead of the placeholder event (see [Integration Guide, step 5](https://github.com/schedjoules/calendar-store-api/blob/master/details/integration_guide.md#step-5-recognise-placeholder-events)).
* Tapping an event can show its `DESCRIPTION`, `LOCATION` and `URL`; for sport this holds the scores and line-ups.
* A calendar that needs input from the user asks for it here, before it can be subscribed:
  * weather: a city (with search) and units, see [Weather](https://github.com/schedjoules/calendar-store-api/blob/master/details/weather.md)
  * pregnancy: the due date; countdown: a name and a date, see [Pregnancy and Countdown Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/user_input_calendars.md)

  Use the platform's date picker and a sheet or a separate screen. Never subscribe to the template URL with its `{placeholders}` still in it.

### My calendars

* One row per subscription: icon, name, and on Android the colour of the calendar in the system calendar.
* Tapping a row opens the Calendar screen for that subscription.
* Unsubscribe from the Calendar screen or with a swipe on the row, after a confirmation. On Android, delete the local calendar and its events; with an iOS webcal subscription, tell the user to remove it under Calendar accounts in the iOS Settings app, because your app cannot.
* Empty state: one sentence and a button that opens Browse.

### Settings

* Country and language, both defaulting to the device. A change reloads the home page in Browse.
* Changing the language does not change existing subscriptions: their feeds stay in the language they were added in. Say so, or offer to re-add them.
* A link to your support channel.

### Permissions and first run

* Do not ask for calendar access at app start. Ask when the user subscribes to the first calendar, after one line explaining why (Android: `READ_CALENDAR` and `WRITE_CALENDAR`; iOS with EventKit: full access; iOS with webcal: nothing).
* If the user refuses, keep the subscription in My calendars, show that it is not syncing, and link to the system settings.
* No onboarding is needed for a v0.1: the home page is the onboarding.

### States every screen needs

| State | Show |
|---|---|
| Loading | A progress indicator in the list area; keep the title and search visible |
| No network or `5xx` | A short message and a Retry button. Keep showing cached content if you have it |
| Empty page or search | "No calendars found" with the query |
| Calendar with no upcoming events | "No upcoming events"; the subscription itself is fine |

### Platform look

Use the native look of each platform instead of one shared design: system fonts, system colours and dark mode, the standard back behaviour, standard switches. Users recognise those, and they keep working with accessibility settings (larger text, screen readers) without extra effort. The iOS and Android SchedJoules apps share the same screens and grouping, but each looks like its own platform.
