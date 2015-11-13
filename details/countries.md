##Countries
You can retreive the list of supported and localised country names via:
```
GET /countries

Optional GET parameters
- locale (default: 'en')
- location

Required labels
- country_id					integer
- name							string
- icon							string (url)
- icon_etag						string
- iso_3166						string
- name_translation				string
- translation_url				string (url)
- page_id						integer
```

Countries can also be called to view all available translations by following the country_translation_url.
```
Required labels
- country_id					integer
- name							string
- icon							string (url)
- icon_etag						string
- iso_3166						string
- page_id						integer
- locales						array
	- locale					string
	- name_translation			string
```

The page\_id refers to the home page of the country in the calendar store. So you can do a GET /pages/{page_id}

You can use the country list to let your users overwrite their default calendar store based on their device's region setting and switch to a calendar store from a different country.

All country names are currently available in English. We are working on translation all country names to the the top 20 languages in the world. If you miss translations please let us know.