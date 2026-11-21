## Embedding the Catalogue in an Existing App

You do not need to show the whole catalogue. Most apps that already have users want SchedJoules content to appear as part of their own screens: a holidays switch in settings, a sports section next to their own content, an "Add calendar" option among the other sources. This page shows how to do that. For a separate catalogue screen instead, see [A Basic UI](https://github.com/schedjoules/calendar-store-api/blob/master/details/ui.md). The feed rules in the [Integration Guide](https://github.com/schedjoules/calendar-store-api/blob/master/details/integration_guide.md) apply either way.

Pick the pattern that fits where your users already are:

| Pattern | Looks like | Effort |
|---|---|---|
| [One switch](#pattern-1-one-switch) | "Show public holidays" in your settings | Smallest |
| [One branch](#pattern-2-one-branch) | A sports or TV section inside your app, showing one page of the catalogue | Small |
| [A source among sources](#pattern-3-a-source-among-sources) | "Add calendar > Holidays, sports and more" next to Google, iCloud or a URL | Medium |
| [Your own event view](#showing-the-events-in-your-own-views) | The events drawn in your app's own calendar or list, not through the system calendar | Depends on your app |

### Pattern 1: one switch

A single setting such as "Show public holidays for {country}". The user never sees the catalogue.

Find the country's national public holiday calendar with a filtered search:

```
GET /countries?locale={language}
  -> pick the user's country by iso_3166, take its country_id and name

GET /pages/search?q={country name}&country_id={country_id}&main_category_id=1&locale={language}
  -> take the calendar item with holiday_kind "public" and no region
```

For example `q=Germany&country_id=108&main_category_id=1` returns "Public Holidays" (`holiday_kind: "public"`, no `region`) together with the calendars of the 16 states, which carry a `region`. Use `holiday_kind: "observances"` for the variant that also includes observances (Mother's Day, Halloween), and the items with a `region` if you want to offer the user's state or province.

Then:
* Store the calendar's `item_id` and `url` once, and build the feed URL as usual (`url` + `&u=`).
* Do the lookup again when the user changes country, not on every start.
* Name the setting yourself ("Public holidays"); the item's `name` is generic ("Public Holidays") and does not mention the country.

The same lookup works for other single-calendar features: `holiday_kind: "school"` for school holidays, `main_category_id=2` with `sport_id` for a sport.

### Pattern 2: one branch

Show one page of the catalogue, and everything below it, inside your own screen: for example the sports of the user's country, a league, or the TV channels.

* Start from the country's home page (`page_id` from `GET /countries`, or `GET /pages?location={country}`) and pick the section you want by its items' `category_id` (see [Search](https://github.com/schedjoules/calendar-store-api/blob/master/details/search.md) for the ids). Section names are translated and can change; category ids do not.
* Or start from a fixed page id, for a branch that is the same for all your users (a league, Formula 1). Agree the ids with us, so we know they are in use. If one answers `404`, fall back to the country's home page rather than showing an error. `GET /pages/{page_id}/info` returns the pages that list a page, which helps you check where it sits.
* Render the pages with your own list components, in your own style. The rules from [A Basic UI](https://github.com/schedjoules/calendar-store-api/blob/master/details/ui.md#browse) still apply: icons can be `null`, show which calendars are subscribed, a page item opens the next page.
* Keep the user inside your app's navigation: a back action returns to your screen, not to a SchedJoules home page.

### Pattern 3: a source among sources

If your app already lets users add calendars (Google, iCloud, Exchange, a URL), add SchedJoules as one more source:

* The entry opens the user's home page (`GET /pages?locale=...&location=...`) with search on top, in a sheet or a pushed screen.
* Build the [Browse](https://github.com/schedjoules/calendar-store-api/blob/master/details/ui.md#browse) and [Calendar](https://github.com/schedjoules/calendar-store-api/blob/master/details/ui.md#calendar) screens from A Basic UI for this. Its My calendars and Settings screens are not needed: your calendar list and settings already do that job, and country and language become two of your settings.
* A subscribed calendar becomes a normal calendar in your app, with your app's controls: colour, visibility, notifications, remove. Do not build a separate "SchedJoules calendars" area.
* Show the calendar's name from the catalogue item (`original_name` from search), never from the feed's `X-WR-CALNAME`.
* SchedJoules calendars are read-only: hide editing on their events, and say so if the user tries.
* If your app already supports subscribing to a calendar by URL, you can reuse that path for the feed URL, as long as it follows the feed rules: body check, placeholder UIDs, sync by UID.

### Showing the events in your own views

Apps that draw their own calendar or agenda do not need the system calendar at all: fetch the feeds and store the events in your app's own local storage, then show them as a layer next to your own events.

* Store each event by its `UID`, linked to the subscription, so you can apply changes and remove the whole layer.
* All-day events (`DTSTART;VALUE=DATE`) are dates, not moments. Store and draw them as dates; converting them through a time zone moves them a day for some users.
* Timed events carry a `TZID`: convert to the user's time zone when drawing.
* Give each subscription its own colour and a visibility toggle, as you would for any other calendar.
* When the user opens an event, fetch it as [JSCalendar](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#one-event-as-jscalendar-rfc-8984), the recommended format for your own event view: the details users look for (scores, line-ups, results, holiday explanation) as structured JSON. Do not parse `DESCRIPTION` for them: its wording is not a contract. On any status other than `200` or `304`, show `DESCRIPTION` as plain text with line breaks.
* For a list screen that does not need the events stored (an agenda of one calendar, upcoming matches), read the [JSCalendar list](https://github.com/schedjoules/calendar-store-api/blob/master/details/calendars.md#a-calendar-as-a-jscalendar-list) instead of the feed: titles and times only, a fraction of the size. Keep the layer in your calendar views synced from the feeds, as above.
* The data stays on the device: see [Data Usage and Restrictions](https://github.com/schedjoules/calendar-store-api#data-usage-and-restrictions). If your app syncs calendars through your own servers, agree that with us first.

### Attribution

Wherever users choose SchedJoules content, show **Calendars by SchedJoules** (see [Attribution](https://github.com/schedjoules/calendar-store-api#attribution)):

| Pattern | Where |
|---|---|
| One switch | The setting's supporting text: "Public holidays for Germany" with "Calendars by SchedJoules" below it |
| One branch | One line at the end of the branch's list, on every page of it |
| A source among sources | On the entry ("Holidays, sports and more", with "Calendars by SchedJoules" as its subtitle) and in the catalogue sheet it opens |
| Your own event view | On the detail view of a SchedJoules event, next to the calendar's name |

### What not to do

* Do not copy catalogue data into your own build or backend. Fetch pages when the user opens them; they change (new seasons, new teams, translations).
* Do not rewrite feed URLs or build them from ids. Always take the `url` from the item.
* Do not hide that a calendar can end: when a feed answers with a placeholder (see [Integration Guide, step 5](https://github.com/schedjoules/calendar-store-api/blob/master/details/integration_guide.md#step-5-recognise-placeholder-events)), show the state in your own UI.
