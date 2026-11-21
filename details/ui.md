## A Basic UI

A standalone v0.1 needs four screens. This is the structure the SchedJoules apps use on iOS and Android, reduced to what a first version needs. Build it with your platform's standard components (lists, tab or navigation bars, switches, sheets); nothing here needs a custom control. Read the [Integration Guide](https://github.com/schedjoules/calendar-store-api/blob/master/details/integration_guide.md) first for the API side.

**Which screens to build:**

| Your app | Build |
|---|---|
| Already shows calendars or events (a calendar, agenda or planner app) | Browse and Calendar from this page, opened from your existing "add calendar" entry, as in [Embedding, pattern 3](https://github.com/schedjoules/calendar-store-api/blob/master/details/embedding.md#pattern-3-a-source-among-sources). No My calendars or Settings screen: your own calendar list and settings do that job |
| Has no calendar views of its own, or is a standalone catalogue | All four screens below |
| Needs only one kind of content (public holidays, one sport) | No catalogue screens: [Embedding, pattern 1 or 2](https://github.com/schedjoules/calendar-store-api/blob/master/details/embedding.md) |

The wireframes below show structure only: which elements, in which order. Draw them with your platform's own components and spacing.

| Screen | Shows | API |
|---|---|---|
| Browse | The catalogue, one page at a time, with search on top | `GET /pages`, `GET /pages/{id}`, `GET /pages/search` |
| Calendar | One calendar: its name, the next events, a subscribe control | The item from the page, and its feed |
| My calendars | What the user subscribed to | Your own storage |
| Settings | Country and language | `GET /countries`, `GET /languages` |

Put Browse and My calendars in a tab or navigation bar; Settings can be a third tab or sit behind an icon.

### Browse

```
+--------------------------------------+
| United States              (title)   |
| [ Search calendars               ]   |
|--------------------------------------|
| [icon] Holidays                  >   |   first section: no header
| [icon] Sports                    >   |
| POPULAR                   (header)   |
| [icon] Golden State Warriors  [on]   |   calendar row, subscribed
| [    ] Moon Phases            [  ]   |   icon null: empty space kept
|        Calendars by SchedJoules      |   attribution, end of the list
|--------------------------------------|
|  Browse  |  My calendars  |  Settings|
+--------------------------------------+
```

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

```
+--------------------------------------+
| <  Golden State Warriors             |
|--------------------------------------|
|          [ Subscribe ]               |   becomes "Subscribed"
|--------------------------------------|
| SAT 21 NOV                           |
|   19:30  Warriors - Lakers           |
| MON 23 NOV                           |
|   04:00  Celtics - Warriors          |
| ...                                  |   next 10 to 20 events
|        Calendars by SchedJoules      |   attribution
+--------------------------------------+
```

* Title: the item's `name` (`original_name` when it came from search).
* A subscribe control at the top: a switch or a button that turns into "Subscribed". Subscribing must give feedback at once; on Android, start the first sync immediately so events appear in the calendar app within seconds.
* Below it, the next events: fetch the [JSCalendar list](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#a-calendar-as-a-jscalendar-list) with `start_at_or_after` set to now and `results=20`, and list date, time and `title` of the entries, grouped by day. This lets users check that they picked the right team or region before they subscribe. An empty calendar gives `"entries": []`: show "No upcoming events". If you read the iCalendar feed here instead, never show its placeholder event (see [Integration Guide, step B2](https://github.com/schedjoules/calendar-store-api/blob/master/details/integration_guide.md#step-b2-recognise-placeholder-events)).
* Tapping an event opens its detail screen. Fetch the event as [JSCalendar](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#one-event-as-jscalendar-rfc-8984), the recommended format: line-ups, results and holiday details as structured JSON. On any status other than `200` or `304`, show the feed's `DESCRIPTION`, `LOCATION` and `URL` instead.
* A calendar that needs input from the user asks for it here, before it can be subscribed:
  * weather: a city (with search) and units, see [Weather](https://github.com/schedjoules/calendar-store-api/blob/master/details/weather.md)
  * pregnancy: the due date; countdown: a name and a date, see [Pregnancy and Countdown Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/user_input_calendars.md)

  Use the platform's date picker and a sheet or a separate screen. Never subscribe to the template URL with its `{placeholders}` still in it.

**With the test key** every calendar serves its real events, but only the next 5, so a Calendar screen previews at most 5 events and a synced calendar holds 5. That is expected and not a sync bug; your own key returns the whole calendar. To test the empty and placeholder states, load the files in [examples/feeds](https://github.com/schedjoules/calendar-store-api/tree/master/examples/feeds) instead of a live feed.

### My calendars

```
+--------------------------------------+
| My calendars                         |
|--------------------------------------|
| [icon] Golden State Warriors     (o) |   (o): colour in the system calendar
| [icon] Public Holidays           (o) |
| [icon] Moon Phases  Not syncing  (o) |   permission refused
|--------------------------------------|
|  Browse  |  My calendars  |  Settings|
+--------------------------------------+
```

* One row per subscription: icon, name, and on Android the colour of the calendar in the system calendar.
* Tapping a row opens the Calendar screen for that subscription.
* Unsubscribe from the Calendar screen or with a swipe on the row, after a confirmation. On Android, delete the local calendar and its events; with an iOS webcal subscription, tell the user to remove it under Calendar accounts in the iOS Settings app, because your app cannot.
* Empty state: one sentence and a button that opens Browse.

### Settings

```
+--------------------------------------+
| Settings                             |
|--------------------------------------|
| Country                United States |
| Language                     English |
| Contact support                    > |
+--------------------------------------+
```

* Country and language, both defaulting to the device. A change reloads the home page in Browse.
* Changing the language does not change existing subscriptions: their feeds stay in the language they were added in. Say so, or offer to re-add them.
* A link to your support channel.

### Attribution

Show **Calendars by SchedJoules** on Browse (every page and the search results) and on the Calendar screen: one line in your secondary text style, at the end of the list or under the title. My calendars and Settings do not need it. See [Attribution](https://github.com/schedjoules/calendar-store-api#attribution) for the rules.

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

### A v0.1 UI checklist

Check each item in the running app, not only in code. Leave out the My calendars and Settings items when your app's own screens do that job (see the table at the top).

- [ ] Browse opens on the home page for the device's language and country, with the page `name` as title
- [ ] Sections show their `name` as header; a section with an empty name shows none
- [ ] Page rows open the child page with a working back action; calendar rows open the Calendar screen
- [ ] Rows with `icon: null` or no icon keep the names aligned
- [ ] Subscribed calendars are marked on their rows, matched by `item_id`, in Browse and in search results
- [ ] Search starts at 3 characters after a short pause; results use `original_name` once opened
- [ ] The Calendar screen title comes from the catalogue item, never from the feed's `X-WR-CALNAME`
- [ ] The Calendar screen lists the next events grouped by day, and shows "No upcoming events" for an empty list (or `empty.ics` when it reads the feed)
- [ ] No placeholder event is ever shown as an event (try every file in `examples/feeds/`)
- [ ] Tapping an event shows its JSCalendar document (try `examples/responses/event.jscalendar.json`), and the feed's `DESCRIPTION` when that request fails
- [ ] Subscribing gives feedback at once; on Android the first sync starts immediately
- [ ] Calendar access is asked at the first subscribe, not at app start; refusing it leaves the subscription visible as not syncing, with a link to the system settings
- [ ] Weather, pregnancy and countdown calendars ask for their input before subscribing
- [ ] Unsubscribing asks for confirmation and removes the events (Android) or explains the iOS Settings step (webcal)
- [ ] My calendars has an empty state with a button to Browse
- [ ] Changing country or language reloads Browse
- [ ] Loading, offline, `5xx`, empty search and empty calendar each show their state from the table above
- [ ] "Calendars by SchedJoules" shows on every Browse page, the search results and the Calendar screen
- [ ] Dark mode and the largest system text size both work on every screen
