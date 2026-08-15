---
name: local-site-builder
description: Build a complete research-backed local service website for a business in any niche — homepage, service silo pages, city and neighbourhood location pages, a service-area hub, blog guides, sitemap, schema markup, real Google Places photos and original SVG artwork. Asks for company name, address, phone, email, niche and city, then scaffolds and builds. Use whenever someone wants a website, location pages, service-area pages, city landing pages, "a page for each city we serve", local SEO expansion, or wants to rank for "near me" and "service in city" searches. This is the generic engine — use sr22-site-builder or turf-site-builder instead when the niche is one of those.
---

# Local site builder

Builds the whole fleet: a homepage, one page per service, one per city, one per
real neighbourhood, a service-area hub, blog guides, and the schema/sitemap
plumbing — from a single `config.py`, on a template that already looks good.

This skill owns the **engine**: the clean base template in `base/`, the
generator, the validators and the reference docs. Two niche packs
(`sr22-site-builder`, `turf-site-builder`) reuse this same engine and only add
their content. Fix the template here and all three benefit.

---

## Start by asking

Do not scaffold until you have these. Ask in one message, accept partial
answers, and put a declared bracket placeholder in anything still unknown —
**never invent a phone number, an address or a licence number.**

| | Needed for |
|---|---|
| **Company name** | titles, schema, footer, logo |
| **Niche** | what the site is about, service list, artwork |
| **City + state** | the geography the fleet is built around |
| **Street address + ZIP** | `PostalAddress` schema, footer, contact page |
| **Phone** | every CTA on every page |
| **Email** | contact page, schema |
| **Domain** | canonicals, schema `@id`, sitemap |
| Hours, licence no., contact name | optional; bracket them if unknown |

Then confirm the scope before building — "that's 6 service pages, 14 city
pages and 22 neighbourhood pages, 45 total" — so they can redirect early.

## Then

```bash
python3 scripts/scaffold.py --dir ~/projects/<slug> \
  --company "Acme Plumbing" --niche "emergency plumbing" \
  --city Tulsa --state OK --domain acmeplumbingtulsa.com --palette slate
```

Palettes: `navy` `forest` `slate` `plum` `clay`. Each is a dark brand colour
plus one accent used sparingly — the vendored template signals value with size
and colour, which reads as a promo sticker on a professional services site.

`generate.py` runs immediately against the empty config. Then run
`validate_site.py` and **treat the failures as the to-do list**: broken links
to pages that do not exist yet, `[TODO: …]` and `[SOURCE NOT SET: …]` markers,
and the form-endpoint gate all point at exactly what still needs doing.
Generate, validate, fill, repeat.

---

## The rule that matters most: never fabricate

Everything on these pages is a checkable claim about a real place or a real
regulation. A wrong courthouse address or an invented statistic is worse than
omitting it — a local reader spots it instantly, quality raters are trained to
catch it, and it exposes the client.

- **Population, demographics** → cite the census year from an authoritative
  source. Aggregators disagree; prefer the primary figure and say which year.
- **Hospitals, courthouses, schools, offices** → real names, verified addresses.
- **Volatile data** (events, hours, schedules, zoning) → link to the official
  calendar or locator instead of hardcoding. Say so on the page: "we link out
  rather than list dates here since events change week to week" reads as
  competence.
- **Reviews, ratings, testimonials, years in business** → only with real
  supplied evidence. Never generate `AggregateRating`.
- **Nothing found for a category in a given place** → omit that category
  there. An honest gap beats a plausible invention.

In a **regulated niche** (insurance, legal, medical, financial), licence
numbers, "licensed in <state>", and years in business are checkable claims —
ship the bracket token. See `references/preview-and-placeholders.md`.

## Workflow

- **Phase 0 — Scaffold.** Above. Never clone a live client site; if you must,
  read `references/template-cloning.md` first.
- **Phase 1 — Tier the geography.** Incorporated places and CDPs get pages.
  Road corridors, highways and generic areas get **no page** — they become
  linked text on the parent city page. A page for "Winkler Road" has nothing
  true and specific to say, which is exactly the thin-content pattern that
  drags down the good pages around it.
- **Phase 2 — Research.** `references/research-sources.md`. Batch the lookups.
  County-level facts are shared by every city in that county — research once,
  reuse. This phase is the product; nothing substitutes for it.
- **Phase 3 — Fill config, run the generator.** Never hand-write pages.
  `references/page-anatomy.md` for the section spec,
  `references/frontend-gotchas.md` for the CSS and markup traps.
- **Phase 4 — Photos.** `references/photo-pipeline.md`. Expect to reject
  roughly half of what Places returns, and **look at every image**.
- **Phase 5 — Artwork** for pages with nothing to photograph.
  `references/original-artwork.md`.
- **Phase 5.5 — Placeholders and preview mode.**
  `references/preview-and-placeholders.md`.
- **Phase 6 — Validate, then deploy.** `references/deployment.md`. Run
  `scripts/responsive_audit.js` across phone, tablet and desktop widths.
- **Phase 7 — Entity consolidation** once live.
  `references/entity-consolidation.md`.

## Per-location uniqueness must be substantive

The difference between a real fleet and 80 spun pages is one field: what
actually changes about the work in *this* place. Coastal salt exposure,
canal-front water tables, engineered fill in new construction, compacted soil
under decades-old lawns, HOA landscape standards, which county courthouse
clears you, which office is full-service and which is a kiosk. That is the part
a competitor cannot copy, and it is the only thing that makes the page worth
existing.

## What ships here

`base/` — clean, niche-neutral copy of the template (CSS, JS, fonts, generator,
validators) with every trace of previous clients removed and the palette reduced
to tokens. Do not edit it per project; edit the copy the scaffold makes.


## Geography tiering

| Tier | Gets a page? | Examples |
|---|---|---|
| Incorporated cities / towns | Yes — full page | Naples, Cape Coral |
| Census-designated places (CDPs) | Yes — full page, but say "unincorporated community," don't imply it's a city | Lehigh Acres, Iona |
| Named neighborhoods / subdivisions / districts | Yes — neighborhood page under its city | Old Naples, Punta Gorda Isles |
| Road corridors, highways, generic areas | **No page** — plain text + Maps link | "US-41 corridor", "Rural acreage parcels" |


## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Pages read as spun | Only the city name varies | Tie content to a real local condition that changes the work |
| Thin/doorway pages | Built pages for road corridors | Only real named places get pages |
| Wrong photo on a real place | Trusted Places' first photo | Contact-sheet QA pass |
| Schema silently absent | One malformed JSON-LD block | `validate.py` before deploy |
| Blank page after deploy | CDN cached a bad response | Purge cache before touching HTML |
| Client asks for a change, it costs hours | Pages hand-written | Generator with data/template split |
| Rating/hours schema present, nothing visible on page | Hand-authored pages (404, legal, blog) reused the schema block but not the paired visible element | `validate.py` catches this; add the visible element in the same pass as the schema |
| Redirect "works" but GBP traffic still hits the old site | Old host has two endpoints (e.g. S3 REST vs website) and only one honors redirects | Check both; replace objects with redirect stubs if the non-redirecting endpoint is what's actually referenced |
| Search Console property breaks after site migration | It was verified via a file hosted on the old site | Verify the new domain *before* redirecting/retiring the old one |
| Old client's phone number still on the live site | It was in a JS widget that injects itself at runtime, not in the HTML | Scan `.js .css .txt .json .xml .svg .php` too, and make the widget read the number off the page |
| Header/buttons keep the old brand colour after a recolour | Template hardcodes its palette outside the CSS variables, including `%23`-encoded hex inside SVG data URIs | Audit colour literals by hue; search the URL-encoded form as well |
| Form silently collects nothing | Template's PHP mailer hardcoded to `your@email.com`, and its JS faked a success message without sending | Delete both; gate the real endpoint as a hard build failure |
| Card titles vanish, one stray header at the top of the page | Nested `<header>` captured by the template's bare `header { position: fixed }` rule | Use a div; grep for bare landmark rules before nesting |
| Form clipped on phones, no scrollbar anywhere | `1fr` has a min-content floor, so a `<select>` with long options forced a 395px track into a 335px container | `minmax(min(Npx,100%), 1fr)` + `min-width: 0` on items |
| `&middot;` rendering as literal text on every card | An HTML entity written into a source string then passed through the escaper | Use literal Unicode (`·` `—` `’`) in source strings |
| Sections permanently blank after an anchor jump | Scroll-reveal put `opacity: 0` on whole `<section>`s and the observer never fired for them | Animate card groups, never prose sections; never above the fold; add a `.js` guard and a reveal failsafe |
| "The CSS isn't applying" | Stylesheet edited but the `?v=` cache-buster never changed | Derive the version from file mtime |
| Client says the spacing looks broken | 120px section padding from a photo-led template, on a text-dense page stacking a dozen short sections | ~72px desktop / ~44px phone, separate with background tints |
| Looks fine on desktop, unusable on a phone | "Responsive" template kept desktop type sizes to 320px — eyebrow wrapped to 81px tall, city hero ran 1061px on an 812px screen | Explicit phone block; `input {font-size: max(16px,1rem)}` to stop iOS zoom |
| Screenshot shows a layout gutter that isn't in the DOM | Preview pane under-painted the right edge | Trust `getBoundingClientRect` / `elementFromPoint`; run `responsive_audit.js` |

## Reference files

- `references/research-sources.md` — where each fact category comes from
- `references/page-anatomy.md` — section spec + JSON-LD patterns
- `references/photo-pipeline.md` — Places API, fetching, the QA pass
- `references/original-artwork.md` — generating original SVG imagery
- `references/frontend-gotchas.md` — grid overflow, entity escaping, animations that hide content, phone type scale, why screenshots lie
- `references/preview-and-placeholders.md` — placeholders, form gating, PREVIEW noindex, regulated niches
- `references/template-cloning.md` — only if cloning a live site
- `references/deployment.md` — validation gates, FTP/CDN gotchas
- `references/entity-consolidation.md` — GBP tie-in, sameAs, ratings/hours
- `references/master-prompt.md` — the whole system as one portable document, for handing to another LLM or onboarding someone

## Scripts

- `scripts/scaffold.py` — new project from the clean base
- `scripts/fetch_photos.py` — Places photos + attribution into a manifest
- `scripts/contact_sheet.py` — review grids for the photo QA pass
- `scripts/validate.py` — pre-deploy gates
- `scripts/responsive_audit.js` — console sweep across widths
