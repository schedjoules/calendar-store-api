## Countries

The supported countries, with their names in the requested language:

```
GET /countries?locale={ISO 639-1 code}

Optional GET parameters
- locale        (default: 'en')
```

`GET /countries?locale=de` returns an array of (shortened to one country):

```json
[
  {
    "country_id": 72,
    "name": "Netherlands",
    "iso_3166": "nl",
    "icon": "https://cdn-images.schedjoules.com/assets/0604f0ff.png",
    "icon_etag": null,
    "name_translation": "Niederlande",
    "translation_url": "https://api.schedjoules.com/countries?location=nl",
    "page_id": 115676
  }
]
```

| Field | |
|---|---|
| `country_id` | Use it as `country_id` in [Search](https://github.com/schedjoules/calendar-store-api/blob/master/details/search.md) |
| `name` | The name in English |
| `name_translation` | The name in the requested language, English where no translation exists |
| `iso_3166` | Lowercase ISO 3166-1 alpha-2 code. Use it as `location` on `/pages` |
| `page_id` | The country's home page in the calendar store: `GET /pages/{page_id}` |
| `translation_url` | Where to get the country's name in every language (below) |
| `icon_etag` | Always `null` |

### One country in every language

```
GET /countries?location={ISO 3166 code}
```

`GET /countries?location=nl` returns (shortened):

```json
{
  "country_id": 72,
  "name": "Netherlands",
  "icon": "https://cdn-images.schedjoules.com/assets/0604f0ff.png",
  "icon_etag": null,
  "iso_3166": "nl",
  "page_id": 115676,
  "locales": [
    {"locale": "de", "name_translation": "Niederlande"},
    {"locale": "fr", "name_translation": "Pays-Bas"}
  ]
}
```

Use the country list to let users switch to the calendar store of another country than the one their device's region setting points to.
