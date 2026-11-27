# XSS and CSRF: break it, then fix it

## `label_span`

The browser keeps both values as data in these two HTML contexts. Time and output space are O(n) for n total characters.

## `form_cookie`

SameSite supports the browser-side check. Time and result space are O(n) for n token characters.

## `save_theme`

Failed requests leave settings intact. With bounded input and average dictionary lookups, time and extra space are O(1).

## Next practice

Add a second setting to the toy handler. Reuse the same form-token check and test both outcomes.
