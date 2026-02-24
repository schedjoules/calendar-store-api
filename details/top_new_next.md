## Top, New, Next

There are three endpoints that return in-app purchases based on the following criteria:
* Most popular
* Most recently added
* Starting soonest

All three endpoints return the [pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md) JSON structure. A maximum of 50 in-app purchases are returned per call.

### Top
Returns the most popular in-app purchases, with the most popular item from the past week listed first.

```
GET /pages?top={nr_of_items}

Required GET parameters
- nr_of_items             integer

Optional GET parameters
- locale                  string  (default: 'en')
- location                string  (default: 'us')
```

### New
Returns the most recently added in-app purchases, with the latest addition listed first. An additional `first_event` label indicates the date and time (UTC) of the first event for each in-app purchase.

```
GET /pages?new={nr_of_items}

Required GET parameters
- nr_of_items             integer

Optional GET parameters
- locale                  string  (default: 'en')
```

### Next
Returns in-app purchases with the earliest upcoming start date, listed in ascending order. An additional `first_event` label indicates the date and time (UTC) of the first event for each in-app purchase.

```
GET /pages?next={nr_of_items}

Required GET parameters
- nr_of_items             integer

Optional GET parameters
- locale                  string  (default: 'en')
```
