## Countries

You can retrieve the list of supported and localised country names via:
```
GET /countries

Optional GET parameters
- locale (default: 'en')
- location

Required labels
- country_id                    integer
- name                          string
- icon                          string (url)
- icon_etag                     string
- iso_3166                      string
- name_translation              string
- translation_url               string (url)
- page_id                       integer
```

You can also retrieve all available translations for a country by following the `country_translation_url`:
```
Required labels
- country_id                    integer
- name                          string
- icon                          string (url)
- icon_etag                     string
- iso_3166                      string
- page_id                       integer
- locales                       array
    - locale                    string
    - name_translation          string
```

The `page_id` refers to the home page of the country in the calendar store. You can navigate to it with `GET /pages/{page_id}`.

You can use the country list to allow users to override their default calendar store based on their device's region setting and switch to a calendar store from a different country.

All country names are currently available in English. We are working on translating all country names into the top 20 languages. If you require a translation that is missing, please let us know.
