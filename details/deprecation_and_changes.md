## Deprecations and Breaking Changes

This document lists breaking changes and deprecated features in the API.

### Upcoming Changes
* **Weather URL** — The weather calendar URL structure will be updated.
* **Categories, sport, and gender** — These fields will be consolidated into a single hash.
* **Force SSL** — All requests will be required to use HTTPS.
* **Icon ETag removal** — The `icon_etag` field will be removed from responses.
* **Location by ID deprecated** — Looking up a location using a numeric ID is no longer supported. Use ISO 3166 country codes instead.
* **`country` renamed to `location`** — The `country` parameter has been renamed to `location` for consistency.
