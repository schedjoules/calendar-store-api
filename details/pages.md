##Pages

Pages are the foundation of the API. Pages are the scaffolds of the views your users will interact with. You need
to add the UX and UI for the pages.

Pages are localised so all items on the page that can be translated will be shown translated.
When requesting a page the response might look like:

```
{
    item_id: 115673,
    name: "United States calendar library",
    app_subscription_identifier: "xxx",
    page_sections: [
        {
        name: "Holidays",
        items: [
            {
                item_class: "page",
                item: {
                    item_id: 92047,
                    name: "United States",
                    icon: "http://images.schedjoules.com/images/9783d4f3.png",
                    icon_etag: "56648-2ea8-4ec94311ad680",
                    url: "https://api.schedjoules.com/pages/92047?locale=en",
                    country: "United States"
                }
            },
            ......
            {
                item_class: "calendar",
                item: {
                    item_id: 90734,
                    name: "Moon Phases",
                    identifier: "xxx_moonphases",
                    icon: "http://images.schedjoules.com/images/moonphases.png",
                    icon_etag: "562b4-2502-4ec94215e8480",
                    url: "http://xxx.schedjoules.com/calendars/moon_phases/calendar.ics?l=en&x=xxx"
                }
            },
            .......
            {
                item_class: "page",
                item: {
                    item_id: 108836,
                    name: "NBA",
                    icon: "http://images.schedjoules.com/images/9783d4f3.png",
                    icon_etag: "56648-2ea8-4ec94311ad680",
                    url: "https://api.schedjoules.com/pages/108836?locale=en",
                    sport: "Basketball",
                    country: "United States",
                    season: "2013-2014"
                }
            }
        }
}
```

###Elements
####Page
```
Required labels
- item_id                           integer
- name                              string
- page_sections                     array

Optional labels
- app_subscription_identifier       string

```

####Page Sections
```
Required labels
- name                              string (may be nil)
- items                             array

Optional labels
```

####Items
```
Required labels
- item_class                        string ('page' or 'calendar')
- item                              hash

Optional labels
```

####Page item
```
Required labels
- item_id                           integer
- name                              string
- icon                              string (url)
- icon_etag                         string
- url                               string (url to child page)

Optional labels
- sport                             string
- country                           string
- season                            string
```

####Calendar item
```
Required labels
- item_id                           integer
- name                              string
- url                               string (url to ics file)

Optional labels
- identifier                        string
- icon                              string (url)
- icon_etag                         string
- sport                             string
- country                           string
- season                            string
```
