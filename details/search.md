## Search

The API supports two search endpoints: search by calendar name and search by identifier. Both return the [pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md) JSON structure.

### By Calendar Name
Use the search endpoint to allow users to find calendars via free-text search.

```
GET /pages/search?q={calendar_name}

e.g. /pages/search?q=Warriors

Required GET parameters
- calendar_name                 string (minimum 3 characters)

Optional GET parameters
- locale                        string   (default: 'en')
- nr_results                    integer  (default: 50, maximum: 50)
- country_id                    integer  filter by country — see countries endpoint
- main_category_id              integer  filter by category (comma-separated for multiple)
- sport_id                      integer  filter by sport (comma-separated for multiple)
- gender_id                     integer  filter by gender (comma-separated for multiple)
```

Available `main_category_id` values:

| ID | Category |
|---|---|
| 1 | Holidays |
| 2 | Sports |
| 3 | Weather |
| 4 | Finance |
| 5 | Miscellaneous |
| 6 | TV |

Multiple values can be passed as a comma-separated list, e.g. `main_category_id=1,2`.

See [countries](https://github.com/schedjoules/calendar-store-api/blob/master/details/countries.md) for the `country_id`.
