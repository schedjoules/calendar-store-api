##Countries
A list of supported and localised country names can be retrieevd via:
```
GET /countries

Optional GET parameters
- locale (if omitted defaults to 'en')
- location

Required labels
- country_id					integer
- country_name					string
- iso_3166						string
- country_name_translation		string
- country_translation_url		string (url)
```

Countries can also be called to view all available translations by following the country_translation_url.
```
Required labels
- country_id					integer
- country_name					string
- iso_3166						string
- locales						array
	- locale					string
	- country_name_translation	string
```

You can use the coutrny list to let your users overwrite their default calendar store based on their device's regions setting and switch to a calendar store from a different country.

All country names are currently available in English. We are working on translation all country names to the the top 20 languages in the world. If you miss translation please let us know.