##Search

Our API supports two search calls: by calendar name and by identifier. Both calls return the [pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md) JSON structure.

###By calendar name
You can use this search call to have users find calendars not only by going through the API tree structure but also throught free text search.

```
GET /pages/search?q={calendar_name}

eg /pages/search?q=Warriors

Required GET parameters
- calendar_name					string
```

###By product identifier
You can use this search call to combine calendars with the same identifier or find a page based on the identifier.

```
GET /pages/search?i={identifier}

eg /pages/search?i=xxxxxxx_92047_united_states_holidays

Required GET parameters
- identifier					string
```