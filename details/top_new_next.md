## Top, New, Next

Three lists for discovery screens:
* **Top:** the most popular items, most popular in the past week first
* **New:** folders updated most recently, latest first
* **Next:** folders whose first event is today or later, soonest first

All three return the [pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md) structure with a single section. At most 50 items are returned, and a list can hold fewer items than you ask for, or none.

### Top

```
GET /pages?top={nr_of_items}&location={ISO 3166 code}

Required GET parameters
- top           integer     number of items (maximum 50)

Optional GET parameters
- locale        string      (default: 'en')
- location      string      the country to rank for. Without it only items that are
                            popular worldwide are returned, so the list is shorter
```

### New

```
GET /pages?new={nr_of_items}

Required GET parameters
- new           integer     number of items (maximum 50)

Optional GET parameters
- locale        string      (default: 'en')
```

The list is the same worldwide: `location` has no effect.

### Next

```
GET /pages?next={nr_of_items}

Required GET parameters
- next          integer     number of items (maximum 50)

Optional GET parameters
- locale        string      (default: 'en')
```

The list is the same worldwide: `location` has no effect.

### Extra fields

Items in New and Next have a `first_event` field: the start of the folder's first event, in UTC, formatted as `"2026-11-20 00:30:00 UTC"` (not ISO 8601).

Items in these lists also carry `icon_etag`, which is always `null`.
