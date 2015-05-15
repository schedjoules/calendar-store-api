##Search

Our API supports two search calls: by calendar name and by identifier. Both calls return the [pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md) JSON structure.

###By calendar name
You can use the search funtion to let users find calendars via free text search

```
GET /pages/search?q={calendar_name}

eg /pages/search?q=Warriors

Required GET parameters
- calendar_name					string

Optional GET parameters
- locale 						string  (default: 'en')
- country_id 					integer 
- category_id 					integer
- nr_results 					integer (default: 20)
```

See [countries](https://github.com/schedjoules/calendar-store-api/blob/master/details/countries.md) for the country_id.
The categories to choose from are: 1. Holidays, 2. Sports, 3. Weather, 4. Finance, 5. Miscellaneous, 6. TV

###By product identifier
You can use this search call to combine calendars with the same identifier or find a page based on the identifier.

```
GET /pages/search?i={identifier}

eg /pages/search?i=xxxxxxx_92047_united_states_holidays

Required GET parameters
- identifier					string

Optional GET parameters
- locale						string  (default: 'en')
```