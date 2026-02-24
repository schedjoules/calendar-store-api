## Search

The API supports two search endpoints: search by calendar name and search by identifier. Both return the [pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md) JSON structure.

### By Calendar Name
Use the search endpoint to allow users to find calendars via free-text search.

```
GET /pages/search?q={calendar_name}

e.g. /pages/search?q=Warriors

Required GET parameters
- calendar_name                 string

Optional GET parameters
- locale                        string  (default: 'en')
- country_id                    integer
- category_id                   integer
- nr_results                    integer (default: 20)
```

See [countries](https://github.com/schedjoules/calendar-store-api/blob/master/details/countries.md) for the `country_id`.
Available categories: 1. Holidays, 2. Sports, 3. Weather, 4. Finance, 5. Miscellaneous, 6. TV.
