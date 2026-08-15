# Photo pipeline (Google Places)

Real photos of real places. This is what makes location pages look locally credible
instead of stock-photo generic.

## Getting a key

The user has to do this — it needs their Google account and a card on file:

1. console.cloud.google.com → create/select a project
2. Enable billing (required to activate the API; usage at this scale is minimal)
3. Enable **Places API (New)** — not the legacy "Places API"
4. Credentials → Create Credentials → API Key
5. Restrict the key to Places API (New)
6. Set a budget alert (~$10/mo) as a safety net

Store it in `.env` in the project root, never in a script or a committed file, and never
in a generated page. One-time lookups for ~150 places is a small number of calls.

## Fetching

`scripts/fetch_photos.py`. Two calls per place:

1. `POST https://places.googleapis.com/v1/places:searchText` with
   `{"textQuery": "<Place>, <City>, <ST>"}` and header
   `X-Goog-FieldMask: places.id,places.displayName,places.photos,places.formattedAddress`
2. `GET https://places.googleapis.com/v1/<photo.name>/media?maxWidthPx=1000&key=...`

Write a manifest keyed by a stable id, recording file path, contributor credit, matched
place name, and the address. Keep the manifest **resumable** — skip anything already
marked ok so a rerun doesn't re-bill or re-download.

Expect roughly 20% of lookups to return no photo, concentrated in small HOA-only
subdivisions with no distinct Google Place. That's a normal outcome, not a bug — those
locations fall back to text + map.

## The QA pass — do not skip this

**Places returns photos in an uncurated order.** The first photo is whatever the algorithm
surfaces, which for quiet residential places is frequently:

- someone's fish catch (real case, on a canal-front neighborhood)
- a parked car, a parking garage
- a restaurant or home interior
- a close-up of fabric or a random object

Shipping those unreviewed puts a confidently wrong image on a page about a real,
identifiable place. Worse than a stock photo, because it looks like the site is broken or
automated.

**Process:**

1. `scripts/contact_sheet.py` renders all photos into labeled grids (~20 per sheet), so
   reviewing 120 photos is ~6 glances instead of 120 file opens.
2. Look at every sheet. Flag anything that isn't recognizably the place or at least a
   neutral, on-brand scene of it.
3. For each flagged place, re-fetch candidates 2–5 for that place and build a candidate
   sheet.
4. Swap in the best alternative. **If none of the candidates are good, drop the photo**
   and let the page fall back to text + map. A missing photo is invisible; a wrong one
   isn't.
5. Update the manifest (`ok: false` for drops) and regenerate.

Budget real time for this. In a 151-place build, 7 needed intervention — 5 had a usable
alternative, 2 had nothing good in their entire photo pool.

## Attribution

Google's terms require crediting the contributor. Render under each photo:

```html
<p style="font-size:.75rem;opacity:.6">Photo: {credit} via Google Maps</p>
```

The credit comes from `photo.authorAttributions[0].displayName`.

## Maps links and embeds — no key needed

Separate from photos, and free:

- **Place link:** `https://www.google.com/maps/search/?api=1&query=<urlencoded place>`
  Opens the place's Google listing. Use `target="_blank" rel="noopener"`.
- **Place embed:** `https://maps.google.com/maps?q=<query>&output=embed`
  Renders the place with its info card.
- **Directions embed:** `https://maps.google.com/maps?saddr=<from>&daddr=<to>&output=embed`

These work without an API key, which makes them the right choice for the many map
elements on these pages.

## What the QA pass actually rejects

On a 29-location build, **11 of the first 25 photos were unusable** — Places'
first result is genuinely unreliable, not occasionally wrong. Real rejections:

| Location | What came back |
|---|---|
| Germantown | a storm-damaged / derelict building |
| Madison | a shed being framed |
| Mount Juliet | a road construction crew |
| Springfield | Santa in a bucket truck |
| Whites Creek | shot through a car windshield, roof in frame |
| Brentwood | the interior of an office showroom |
| Dickson | an empty field |
| Antioch | a snowy parking lot |
| Green Hills | a mall car park at night |
| Inglewood | **an identifiable private individual walking a path** |

That last one matters beyond aesthetics: do not publish a stranger's likeness
as a page hero.

## Re-query with named landmarks, not place names

The fix that worked: for anything rejected, re-query a **specific named
landmark** rather than the settlement.

```
"Gallatin, Tennessee"          -> a house under construction
"Sumner County Courthouse, Gallatin, Tennessee"  -> the courthouse
```

Courthouses, city halls, named parks and civic buildings return civic-looking
photographs almost every time. Budget three passes: initial fetch, landmark
re-query for the rejects, then a final small pass. Two locations still ended
with no usable photo, which is the correct outcome — fall back to a credited
regional photo rather than shipping the wrong place.

## Caption what is actually pictured

Once you re-query by landmark, the image is no longer a generic streetscape.
Say what it is, so the caption is true:

```
"Williamson County Courthouse. Photo: Tim B via Google Maps"
```

Take the longer of the API's `displayName` and your query's first segment —
Places sometimes clips the name to "Downtown" and sometimes returns a fuller
one than you asked for.

## Approval is a separate flag from success

`fetch_photos.py` writes `ok: true` when a download succeeds. That is not the
same as "a human looked at it". Add `approved` yourself during the contact-sheet
pass and have the generator ship **only approved photos**, so an un-reviewed
fetch can never reach production.
