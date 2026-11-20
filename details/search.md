## Search

Free-text search over calendars and pages:

```
GET /pages/search?q={query}

e.g. /pages/search?q=Warriors

Required GET parameters
- q                     string   at least 3 characters. A shorter query returns no items

Optional GET parameters
- locale                string   (default: 'en')
- nr_results            integer  number of results (default: 50)
- country_id            integer  filter by country, see Countries
- main_category_id      integer  filter by main category
- sport_id              integer  filter by sport
- gender_id             integer  filter by gender
```

Every filter takes one id or a comma-separated list, e.g. `main_category_id=1,2`. An unknown id returns no items, not an error.

`main_category_id` values:

| ID | Category |
|---|---|
| 1 | Holidays |
| 2 | Sports |
| 3 | Weather |
| 4 | Finance |
| 5 | Miscellaneous |
| 6 | TV |

`gender_id` values: 1 Men, 2 Women, 3 Unspecified, 4 Mixed.

See [Countries](https://github.com/schedjoules/calendar-store-api/blob/master/details/countries.md) for `country_id`. To open a page whose id you already know, use `GET /pages/{page_id}`; there is no separate lookup endpoint.

### Response

The response has the [pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md) structure, with `item_id` set to `null` and the query as `name`. Results are grouped into one section per main category. Search items carry one extra field, `original_name`: `name` may include a gender sign and a flag to tell similar teams apart, `original_name` does not.

`GET /pages/search?q=Warriors&nr_results=1` returns:

```json
{
  "item_id": null,
  "name": "Warriors",
  "page_sections": [
    {
      "name": "Sports",
      "items": [
        {
          "item_class": "calendar",
          "item": {
            "item_id": 29139585,
            "name": "Golden State Warriors ♂ 🇺🇸",
            "original_name": "Golden State Warriors",
            "url": "https://holidays.schedjoules.com/calendars/766e8a162f82?l=en",
            "category": "Sports",
            "category_id": 2,
            "icon": "https://cdn-images.schedjoules.com/assets/basketball.png",
            "country": "United States",
            "country_id": 79,
            "sport": "Basketball",
            "sport_id": 2,
            "gender": "Men",
            "gender_id": 1
          }
        }
      ]
    }
  ]
}
```
