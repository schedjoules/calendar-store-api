#SchedJoules Calendar Store API

With this API you can get access to the SchedJoules Public Calendar Library. SchedJoules delivers the most comprehensive public desktop, web and mobile calendar store in the world. We currently deliver over 180.000 complete, accurate and timely public calendars for holidays, sports, weather and financial events. We do so in 40 languages.

##Set yourself up
1. Mail us at info@schedjoules.com for an API key
2. Try curl -L 'https://api.schedjoules.com/pages/115676?locale=en&location=ar' -v -H 'Authorization: Token token="{API_KEY}"' from your terminal. If you get data you are good to go. Else contact us so we can help you out.

##Requests
* All URLs start with https://api.schedjoules.com/
* You can append URLs can be by .json but that is not mandatory
* We use REST methodology for the API
* All output  is in JSON format
* The API only accepts HTTPS requests

###Headers
####Versioning
The API version needs to be set in de request header. Current version is: v1. If you don't set headers and the default version is bumped your application might not function. If we change the API in backward-incompatible ways, we'll bump the version marker and maintain stable support for the old URLs. Labels can be added without version change so make your client flexible enough to handle that. Follow our [twitter feed](http://twitter.com/schedjoules) for latest SchedJoules' news also on the API. We'll email you with API changes as well once you are set up.

####Authentication
You will need an API key to use this API. You can get your API key by contacting us at info@schedjoules.com. You need to set the API key in the header

##Here we go
Those were the basics ... now the fun:

###Pages
The API is mainly build around the concept of pages. Visualise a page in your application for eg football.That page would have all the name of all the temas in a league from which users can select the calendar they want to add to their calendar.

A page has a name has some meta data like it name and page_section. Think of page sections as headers or paragraphes. A page section has name. Within the page section there the items wich have an item class. And item class is either a 'calendar' or a (sub) 'page'.

A (sub)page is, not very surprisingly, a child page of the page the user is looking at. Think of English Football being a (sub)page of all football and Premier League being a (sub)page of English Football.

A item class calendar is where the magic happens. This is where the users get to see the actual data in calendar file and can add that calendar to his calendar.

GET /pages/{PAGE_ID}&locale={[ISO 639-1 code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)}&location={[ISO_3166 code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)}

Required GET parameters
* page_id

Optional GET paramaters
* locale - Default is 'en'
* location - Default is 'us'

If you use the locale and location parameter you will redirected to the correct page_id. So have you application detect the users locale and location and the API will return the page with the calendars that are most relevant to the user in his preferred language ;-)

##Just to make sure there is no misunderstandig ... 
By using our API it is clear to you that all the data you access is proprietary. The data and images can not be used for any other purpose then agreed on. Data can't be stored in any database other than on a users client for speed purposes.

##Caching
Do your clients, yourself and us a favor and cache where you can. It will speed up you app and save bandwidth.
* All json responses support Etag and last modified so use If-Modified-Since and If-None-Matched.
* Icons are are in the JSON have their etag mentioned in de response.

##Rate limits
There are no rate limits. We do count requests. If we think we can help you improve we will contact you.

##Help Us
Please tell us how we can make the API better. If you have a specific feature request or if you found a bug, please use GitHub issues or send us an email.