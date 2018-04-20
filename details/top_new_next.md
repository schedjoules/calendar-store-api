## Top, new, next

There are three calls returning the in-app purchases that:
* are most populair
* are newly added
* will start next

All three calls return the [pages](https://github.com/schedjoules/calendar-store-api/blob/master/details/pages.md) JSON structure. For all three calls the maximum number of In App Purchases returned is 50.

### Top
The 'top' call will return the in-app purchases that were most popular. The in-app purchase that was most popular over the last week is at the top.

```
GET /pages?top={nr_of_items}

Required GET parameters
- nr_of_items				  	integer

Optional GET parameters
- locale 						string  (default: 'en')
- location 						string  (default: 'us')
```

### New
The 'new' call will return the in-app purchases that were added latest. The in-app purchase that was added latest is at the top. An extra label 'first_event' shows the date and time (UTC) of the first event of that in-app purchase.

```
GET /pages?new={nr_of_items}

Required GET parameters
- nr_of_items	  				integer

Optional GET parameters
- locale 						string  (default: 'en')
```

### Next
The 'next' call will return the in-app purchases that start next. The in-app purchase that starts first is at the top. An extra label 'first_event' shows the date and time (UTC) of the first event of that in-app purchase.

```
GET /pages?next={nr_of_items}

Required GET parameters
- nr_of_items		  			integer

Optional GET parameters
- locale 						string  (default: 'en')
```
