## Pages

Pages are the foundation of the API. They provide the structure for the views your users interact with; your application provides the UX and UI for each page.

Pages are localised: every translatable field is returned in the requested language.

`GET /pages/115673?locale=en` returns (shortened to one item per section):

```json
{
  "item_id": 115673,
  "name": "United States",
  "country": "United States",
  "country_id": 79,
  "icon": null,
  "page_sections": [
    {
      "name": "Holidays",
      "id": 2,
      "items": [
        {
          "item_class": "calendar",
          "item": {
            "item_id": 50084,
            "name": "Public Holidays",
            "url": "https://holidays.schedjoules.com/calendars/766e8a162f82?l=en",
            "category": "Holidays",
            "category_id": 1,
            "country": "United States",
            "country_id": 79,
            "holiday_kind": "public",
            "icon": "https://cdn-images.schedjoules.com/assets/9783d4f3.png"
          }
        }
      ]
    },
    {
      "name": "Sports",
      "id": 28,
      "items": [
        {
          "item_class": "page",
          "item": {
            "item_id": 29230902,
            "name": "NBA",
            "url": "https://api.schedjoules.com/pages/29230902?locale=en",
            "category": "Sports",
            "category_id": 2,
            "country": "United States",
            "country_id": 79,
            "sport": "Basketball",
            "sport_id": 2,
            "gender": "Men",
            "gender_id": 1,
            "icon": "https://cdn-images.schedjoules.com/assets/basketball.png"
          }
        }
      ]
    }
  ]
}
```

An optional field without a value is usually left out rather than sent as `null`; `icon` is the exception and can be `null`.

### Page

| Field | Type | |
|---|---|---|
| `item_id` | integer | Always. Unique per page |
| `name` | string | Always |
| `page_sections` | array | Always. One or more sections |
| `icon` | string (URL) or null | |
| `description` | string | |
| `url` | string (URL) | Only on a page that has no sections of its own |
| `app_subscription_identifier` | string | Only for API keys on a subscription pricing model. The product identifier to offer this user. It can differ per user: it is chosen from the `u` parameter (or the `x-user-id` header) |

A page also carries the same tag fields as an item (`category`, `country`, `sport` and so on, see below) when they apply.

### Page Section

| Field | Type | |
|---|---|---|
| `name` | string | Always. An empty string for the first, unnamed section |
| `id` | integer | Not on the first, unnamed section |
| `items` | array | The section's items |

### Item

| Field | Type | |
|---|---|---|
| `item_class` | string | `page` or `calendar` |
| `item` | object | The page item or calendar item |

### Page item and calendar item

Both have the same fields. The difference is the `url`: a page item's `url` is the API URL of the child page, a calendar item's `url` is the calendar feed.

| Field | Type | |
|---|---|---|
| `item_id` | integer | Always |
| `name` | string | Always |
| `url` | string (URL) | Always |
| `icon` | string (URL) or null | |
| `category`, `category_id` | string, integer | Main category, see [Search](https://github.com/schedjoules/calendar-store-api/blob/master/details/search.md) for the ids |
| `country`, `country_id` | string, integer | The country the item belongs to, see [Countries](https://github.com/schedjoules/calendar-store-api/blob/master/details/countries.md) |
| `region`, `region_id` | string, integer | Regional holiday calendars only |
| `sport`, `sport_id` | string, integer | Sports only |
| `gender`, `gender_id` | string, integer | Sports only: 1 Men, 2 Women, 3 Unspecified, 4 Mixed |
| `holiday_kind` | string | Holiday calendars only, for example `public` |

`region` is set on regional holiday calendars only: the state, province or other region the calendar covers, in the requested locale (falling back to English). `country` is the country it belongs to; a national calendar has no `region`. Outside its parent page a regional calendar is named like its national one ("Public Holidays and Observances"), so show `region` with it, for example as a subtitle: "California, United States".

Before presenting a calendar item's `url` to your users, append the unique anonymous user identifier: `&u={unique_anonymous_user_identifier}` (see the [README](https://github.com/schedjoules/calendar-store-api#unique-anonymous-user-identifier)).

A calendar `url` can be a template that your app must fill in first, such as the weather calendar's `{location}`. See [Weather](https://github.com/schedjoules/calendar-store-api/blob/master/details/weather.md) and [Pregnancy and Countdown Calendars](https://github.com/schedjoules/calendar-store-api/blob/master/details/user_input_calendars.md).
