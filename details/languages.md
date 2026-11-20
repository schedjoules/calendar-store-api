## Languages

The API and most calendar content are available in 18 languages:

| Code | Language | Code | Language |
|---|---|---|---|
| `ar` | Arabic | `ko` | Korean |
| `da` | Danish | `nl` | Dutch |
| `de` | German | `no` | Norwegian |
| `en` | English | `pl` | Polish |
| `es` | Spanish | `pt` | Portuguese |
| `fi` | Finnish | `ru` | Russian |
| `fr` | French | `sv` | Swedish |
| `it` | Italian | `tr` | Turkish |
| `ja` | Japanese | `zh` | Chinese |

The current list:

```
GET /languages
```

returns an array of (shortened):

```json
[
  {"language_id": 1, "name": "Français", "iso_639_1": "fr"},
  {"language_id": 15, "name": "Norsk bokmål", "iso_639_1": "no"}
]
```

`name` is the language's own name, not its English name. How the API picks the response language is described in the [README](https://github.com/schedjoules/calendar-store-api#language).

If a language that matters to you or your users is missing, please contact us.
