## Pages

Pages are the foundation of the API. They provide the structure for the views your users will interact with. Your application is responsible for providing the UX and UI for each page.

Pages are localised — all translatable items on a page will be returned in the requested language.

When requesting a page, the response will look similar to the following:

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
                    url: "http://xxx.schedjoules.com/calendars/moon_phases/calendar.ics?l=en&x=xxx&u=uuu"
                }
            },
            .......
            {
                item_class: "page",
                item: {
                    item_id: 108836,
                    name: "NBA",
                    icon: "http://images.schedjoules.com/images/9783d4f3.png",
                    url: "https://api.schedjoules.com/pages/108836?locale=en",
                    sport: "Basketball",
                    sport_id: 3
                    country: "United States",
                    season: "2019"
                }
            }
        }
}
```

### Elements
#### Page
```
Required labels
- item_id                           integer
- name                              string
- page_sections                     array

Optional labels
- app_subscription_identifier       string

```
The `item_id` is unique per page.
A page may contain one or more `page_sections`.
The `app_subscription_identifier` is unique per API key and can be used in applications that implement a subscription pricing model.


#### Page Sections
```
Required labels
- name                              string (may be nil)
- items                             array

Optional labels
```

#### Items
```
Required labels
- item_class                        string ('page' or 'calendar')
- item                              hash

Optional labels
```

#### Page item
```
Required labels
- item_id                           integer
- name                              string
- url                               string (url to child page)

Optional labels
- icon                              string (url)
- page_identifier                   string
- sport                             string
- sport_id                          string
- country                           string
- season                            string
- related_identifiers               array of strings
```

The calendar URL must be appended client-side with a unique anonymous user identifier: `&u={unique_anonymous_identifier}`.

The `page_identifier` indicates that all children of this page item share the specified identifier. An identifier is unique for a given combination of API key and page. If identifiers need to be shared across different API keys, they are listed under `related_identifiers`.

#### Calendar item
```
Required labels
- item_id                           integer
- name                              string
- url                               string (url to ics file)

Optional labels
- identifier                        string
- icon                              string (url)
- sport                             string
- sport_id                          integer
- country                           string
- season                            string
```
