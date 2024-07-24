## Search

Our API supports two search calls: by calendar name and by identifier. Both calls return the [pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md) JSON structure.

### By calendar name
You can use the search funtion to let users find calendars via free text search

```
GET /pages/search?q={calendar_name}

eg /pages/search?q=Warriors

Required GET parameters
- calendar_name					string

Optional GET parameters
- locale 					string  (default: 'en')
- country_id 					integer 
- category_id 					integer
- nr_results 					integer (default: 20)
```

See [countries](https://github.com/schedjoules/calendar-store-api/blob/master/details/countries.md) for the country_id.
The categories to choose from are: 1. Holidays, 2. Sports, 3. Weather, 4. Finance, 5. Miscellaneous, 6. TV
