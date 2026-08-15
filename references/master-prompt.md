# Local Service Website Builder — Master Prompt

**Portable specification. Hand this whole document to any capable LLM with file
and shell access and it can rebuild this system from nothing.**

Everything here was learned building a 66-page SR-22 insurance site for
Nashville, itself derived from a turf-installation site for Fort Myers. Every
warning is a bug that actually happened, not a hypothetical.

---

## 0. What you are building

A generated static website for a local service business:

```
/                          homepage
/<service>.html            one page per service (6–18)
/<geo>/                    service-area hub
/<geo>/<city>/             one page per city (10–20)
/<geo>/<city>/<hood>/      one page per real neighbourhood (0–30)
/blog/  /blog/<post>/      researched guides (6–8)
about, contact, faq, services, privacy, terms, 404
sitemap.xml  robots.txt  llms.txt
```

Typical output: 45–70 pages from one `config.py`.

**Non-negotiable architecture: a generator, not hand-written pages.**

```
config.py      per-client data: business, services, cities, facts, copy
blog.py        long-form content (split out purely for file size)
generate.py    templates + build_home/build_city/build_service/…
validate_site.py  pre-deploy gates
assets/        CSS, JS, fonts, images
```

With 66 pages, any later change ("add a weather block", "kill the yellow
button") is a data or template edit and one re-run instead of 66 manual edits.
This is the single biggest time saver in the whole workflow and it is what
makes the client's inevitable round-two requests cheap instead of painful.

Use `string.Template` (`$var`) for the page shell, **not** f-strings — JSON-LD
is full of `{}` braces that f-strings choke on.

---

### The copy layer

**No reader-facing string belongs in the generator.** `generate.py` holds a
`DEFAULT_COPY` dict of niche-neutral fallbacks and a `copy()` helper; every
override lives in `config.COPY`:

```python
def copy(key, **fmt):
    tpl = getattr(C, "COPY", {}).get(key, DEFAULT_COPY.get(key, ""))
    base = {"niche": …, "company": …, "city": …, "region": …, "phone": …}
    base.update(fmt)
    try:    return tpl.format(**base)
    except (KeyError, IndexError):
        return tpl          # a half-filled COPY still builds
```

Titles, meta descriptions, hero eyebrow/H1/subhead, quick answers, section
headings, footer blurbs, the 404 link list, legal drafts and form dropdowns
all live in config. Retro-fitting this to a niche-specific generator took a
day and cut cross-niche leakage from 59 stray phrases to 7 — do it from the
start instead.

Structural things that also belong in config, not the template: `GEO_ROOT`
and `HUB_CITY_SLUG`. Derive them and a rebuild silently rewrites every
location URL on a live site.

## 1. The rule that overrides everything: never fabricate

Every claim on these pages is checkable. A wrong courthouse address or an
invented statistic is worse than omitting it — a local reader spots it
instantly, quality raters are trained to catch it, and it exposes the client.

| Category | Rule |
|---|---|
| Population, demographics | Cite the census year. Aggregators disagree; prefer the primary figure and label the year on the page. |
| Hospitals, courthouses, offices | Real names, verified street addresses. |
| Volatile data (events, hours, schedules) | Link to the official calendar/locator. Do not hardcode. Say so on the page — it reads as competence. |
| Reviews, ratings, testimonials, years in business | Only with real supplied evidence. **Never generate `AggregateRating`.** |
| Nothing found for a category in a place | Omit that category there. An honest gap beats a plausible invention. |
| Regulated niches (insurance, legal, medical, financial) | Licence numbers, "licensed in <state>", years in business are checkable claims. Ship a bracket placeholder. |

**Publish what you could not confirm.** Keep an `UNVERIFIED` dict and render it
as a "What we could not confirm" section. On the SR-22 build the out-of-state
waiver could not be verified on the state's site, so the page says so and tells
readers to get a written answer. That reads as credibility, and it is the
difference between a page a model will cite and one it will not.

---

## 2. Phase 0 — Never clone a live client site

Cloning is how you publish someone else's phone number under a new brand.
Build from a clean, niche-neutral base instead. If you must clone, this is what
actually leaked on a real build:

**The phone number survived every HTML grep** because it lived in a widget that
injected itself at runtime:

```js
// assets/js/corner-call.js
var a = document.createElement('a');
a.href = 'tel:+12393202623';        // invisible to any HTML search
a.innerHTML = '… Call Here for Turf Discounts! …';
document.body.appendChild(a);
```

**So scan every text file, not just HTML:** `.js .css .txt .json .xml .svg .php`

**The header stayed green** because templates hardcode their palette *outside*
the CSS variables:

```css
header { background:#0e2b12; }     /* not a variable */
```

Find colour literals by hue, and **also search URL-encoded hex** — inline SVG
data URIs escape the `#` as `%23`, so `#2e7d32` hides as `%232e7d32`.

**The bundled form backend was a demo:**

```php
$to = "your@email.com";                              // never changed
$valid_services = ["Lawn Care", "Hardscaping", …];   // old niche's categories
```

It would have rejected 100% of the new site's submissions. Its companion JS was
worse — intercepted submit, showed a success message, sent nothing. **Delete
both; never adapt them.**

**Also strip:** `aggregateRating`, `openingHoursSpecification`, `geo`, `hasMap`,
`sameAs`, the Search Console verification file, the template vendor's name, and
dead `url()` references to the old client's photo filenames (27 of those
survived two careful passes on a real build, invisible because HTML-only asset
checks never look inside CSS).

---

## 3. Phase 1 — Tier the geography before writing anything

| Tier | Page? | Example |
|---|---|---|
| Incorporated cities/towns | Yes, full page | Naples, Franklin |
| Census-designated places | Yes, but say "unincorporated community" | Lehigh Acres |
| Named neighbourhoods/districts | Yes, under their city | Old Naples, The Gulch |
| **Road corridors, highways, generic areas** | **No page** — linked text only | "US-41 corridor" |

That last row is what people get wrong. A page for "Winkler Road" has nothing
true and specific to say, so it becomes filler — exactly the thin-content
pattern that drags down the good pages around it.

Confirm the count with the client before building: "that's 21 city pages and 67
neighbourhood pages, 88 total" lets them redirect early.

---

## 4. Phase 2 — Research (this phase *is* the product)

Batch lookups. County-level facts (courts, transit, school district) are shared
by every city in that county — research once, reuse. That collapses a lot of
work.

**Per city:** county, population + census year, geography/character, 3–4 real
landmarks, hospital(s) with address, the civic office that matters for this
niche, real neighbourhoods, schools, a few real restaurants, transit authority.

### Sources that changed recently

- `api.census.gov` now returns **"Missing Key"** — needs a free API key.
- `census.gov/quickfacts` returns **403** to automated fetches.
- **What works:** the Wikipedia "List of municipalities in <state>" article —
  2020 decennial figure and county for every place in one table, one fetch.

Named neighbourhoods are usually not census places and have **no population**.
Omit it; give the page a different real anchor (ZIP codes, nearest civic
office, what changes about the job there).

### Research is a phase, not a step. Do it before you write anything.

The most common way this system produces a bad site is writing copy from
memory and back-filling sources afterwards. Do it the other way round: open
the authority's own pages, record the URLs, fill `config.SOURCES`, and only
then write.

**Three categories, all mandatory where they apply:**

**1. Regulator / authority pages — for any regulated or licensed trade.**
Insurance, legal, medical, financial, contracting, pest control, real estate.
Search for the *agency*, not the topic:

```
site:<state>.gov <topic> requirements
site:dmv.<state>.gov <topic>
site:<state>.gov licensing board <trade>
```

Rules differ by state, and often by county. **Never assume a rule you learned
for one state applies to another** — that is precisely the error that makes
most national content wrong, and it is the opening the client is paying you to
exploit. On one build, nearly every competing page said an SR-22 lasts three
years; the state's own page tied it to the length of the suspension. That
single correction was the site's whole position.

**2. Manufacturer specs and warranty terms — for any product-based trade.**
Warranty length, drainage rates, material specs, certifications, load ratings,
coverage rates. These come from the manufacturer's published document for the
specific product line, per client. Never from you, never from a competitor's
marketing, never rounded for convenience.

**3. City, county and state facts — for every location page.**
County (and whether the city straddles two), population with the census year,
the civic office that matters for this niche *and its service level*, climate
normals, local restrictions, permits, rebates, HOA rules, soil, pests. This is
the layer that makes a city page real rather than spun.

**Record the URL for every fact.** Each becomes a `SOURCES` entry printed on
the page that relies on it. If you cannot produce the URL, you cannot publish
the claim.

### Find the fact the competition gets wrong

This is the highest-leverage research you can do. Read the **primary regulator
or authority's own page** and note where it disagrees with the national
consensus. On the SR-22 build:

> Nearly every competing page says an SR-22 lasts three years. Tennessee ties
> the filing period to the **length of the suspension or revocation**.

That single correction is the whole GEO position — when a model cross-checks
against the state's site, your page is the one that matches.

---

## 5. Per-location uniqueness must be substantive

The difference between a real fleet and 80 spun pages is one field: **what
actually changes about the work in this place.**

Good: coastal salt exposure, canal-front water tables, engineered fill in new
construction, compacted clay under decades-old lawns, HOA landscape standards,
which county courthouse clears you, which government office is full-service
versus a self-service kiosk.

Bad: "We proudly serve Murfreesboro!" with the city name swapped.

On the SR-22 build the strongest per-city differentiator turned out to be
**which driver services office actually processes reinstatements** — only
full-service locations do, and sending someone to a kiosk wastes their
afternoon. No national competitor had that.

---

## 6. Page anatomy

1. Hero — H1 `<Service> in <City>, <ST>`, subhead, **CTA + click-to-call in the hero itself**
2. Quick Answer box — the whole offer in ~40 words (wins AI/featured snippets)
3. Intro tied to a real local condition
4. At a glance — county, population, the civic facts, timeline
5. The authoritative answer block — labelled facts, each with a source link
6. Services grid
7. Cost section, with a disclaimer if any figure is an estimate
8. Process steps
9. Local civic detail (offices, courts) with maps links
10. Neighbourhoods — cards for real ones, text links for corridors
11. FAQ (FAQPage schema)
12. Author/reviewer block with a named human
13. Quote form
14. Sibling links

**Make the answer block quotable.** Label each fact so an assistant lifting
"How long you need it" gets a self-contained answer:

```python
KEY_FACTS = [
  ("How long you need it",
   "Tennessee requires the SR-22 to be maintained for the length of your "
   "suspension or revocation period…", "source_key"),
]
```

### Schema

`LocalBusiness` (or a subtype — `InsuranceAgency`, `HomeAndConstructionBusiness`),
`Service`, `WebPage`, `BreadcrumbList`, `FAQPage`, `ItemList`, `BlogPosting`.

**Schema must match visible page content.** Emitting a rating or hours that
does not appear on the page is a real guidelines violation. Emit conditionally:

```python
if not site["street"].startswith("["):
    obj["address"] = {...}
if site["geo"]:
    obj["geo"] = {...}
# aggregateRating: omitted entirely until real reviews exist
```

---

## 7. Frontend gotchas — every one of these actually happened

### `1fr` overflows its container

The worst bug of the build, on every page with a form, invisible until measured.

`1fr` means `minmax(auto, 1fr)` and that `auto` floor is **min-content**. A
`<select>` whose longest option reads "Driving without insurance / accident
claim" forced a **395px track inside a 335px container**. No horizontal
scrollbar appeared because an ancestor had `overflow:hidden`.

```css
/* wrong */ grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
/* right */ grid-template-columns: repeat(auto-fit, minmax(min(280px,100%), 1fr));
.grid > *, .grid input, .grid select { min-width: 0; max-width: 100%; }
```

### HTML entities inside strings that get escaped

```python
blurb = "Davidson County &middot; SR-22 filing"
esc(blurb)   # -> "Davidson County &amp;middot; SR-22 filing"
```

Shipped on 16 city cards, rendering as literal `&middot;`. **Use literal
Unicode** (`·` `—` `–` `’` `“` `”` `•` `…`) in source strings — `html.escape`
only touches `& < >` and quotes. Leave `&amp; &nbsp; &lt; &gt;` alone.

### Scroll-reveal animations that hide content

Three failures, all seen:

1. **Whole sections stayed invisible.** `data-animation` on a `<section>` and
   the IntersectionObserver never fires — restored scroll positions, anchor
   jumps, fast scrolling all skip it. Three sections of body copy sat blank.
   **Animate card groups and images, never a section wrapping prose.**
2. **Above-the-fold copy faded in**, so first paint was a photo with no words —
   bad for the reader and for LCP. **Never animate above the fold.**
3. **A script failure blanked the page**, because `opacity:0` applies whether
   or not the JS runs. Gate it:

```html
<script>document.documentElement.classList.add('js')</script>
```
```css
.js [data-animation] { opacity: 0; }
@media (prefers-reduced-motion: reduce) {
  .js [data-animation] { opacity: 1 !important; animation: none !important; }
}
```

Plus a failsafe that reveals anything still hidden after ~1.2s. Motion is a
bonus, never a precondition for reading.

### Bare element rules capture nested markup

Templates style landmark elements directly:

```css
header { position: fixed; top: 0; z-index: 1000; }
```

So a perfectly reasonable `<header class="card__head">` inside a card gets
yanked out and pinned to the top of the viewport — all four card headers
stacked, titles vanished. **Grep for bare rules on `header footer nav aside
section main` before nesting them.** Use a `div`.

### Cache-busting

Editing CSS changes nothing if the link still says `?v=1`. Lost real time to
"my CSS isn't applying" when the rules were correct and the browser was serving
the old file:

```python
CSS_VER = str(int(max(os.path.getmtime(f) for f in CSS_FILES)))
```

### Section rhythm

Templates built for image-heavy marketing use 100–120px section padding. On a
text-dense page stacking a dozen short sections it reads as broken layout — the
client said "the spacing is messed up". Use ~72px desktop / ~44px phone and let
background tints separate.

### The phone type scale is not automatic

A "responsive" template can keep desktop sizes to 320px. Measured at 375px on
an untouched clone:

| Element | Rendered | Effect |
|---|---|---|
| Eyebrow | 16px uppercase, 0.25em tracking | wrapped to 2 lines, 81px tall |
| City hero | — | **1061px on an 812px screen** |

Add an explicit phone block. And set `input, select, textarea { font-size: max(16px, 1rem) }`
at **every** width — iOS zooms the page when a focused field is under 16px.

### Verify by measuring, not by screenshot

Preview panes lie. In this environment they returned blank captures after
programmatic scrolls, stale paints, and an unpainted right edge that looked
exactly like a layout gutter — while `header`, `.hero` and `body` all measured
exactly the viewport width with no scrollbar gap.

```js
document.elementFromPoint(400, 300)                 // what is actually painted
el.getBoundingClientRect()                          // real position and size
document.documentElement.scrollWidth > clientWidth  // real overflow
getComputedStyle(el).opacity                        // hidden, or just not drawn
```

**Automate it.** Load each page in an offscreen iframe at 320/360/375/390/414/
700/768/820/834/1024/1180/1440/1920 and report elements extending past the
viewport, skipping anything inside a deliberately clipping ancestor.

---

## 8. Photos

Real photos of real places via the Google Places API, credited as their terms
require ("Photo: <name> via Google Maps").

**Places returns photos in an uncurated order, and it is genuinely unreliable.**
On a 29-location build, **11 of the first 25 were unusable**:

| Location | What came back |
|---|---|
| Germantown | a storm-damaged building |
| Madison | a shed being framed |
| Springfield | Santa in a bucket truck |
| Whites Creek | shot through a car windshield, roof in frame |
| Inglewood | **an identifiable private individual** |

That last one matters beyond aesthetics — do not publish a stranger's likeness
as a page hero.

**The fix:** re-query rejects with a **named landmark** rather than the
settlement.

```
"Gallatin, Tennessee"                            -> a house under construction
"Sumner County Courthouse, Gallatin, Tennessee"  -> the courthouse
```

Courthouses, city halls and named parks return civic-looking photographs almost
every time. Budget three passes. Two locations still ended with no usable photo
— that is the correct outcome; fall back to a credited regional photo.

**Approval is a separate flag from success.** `ok: true` means the download
worked, not that a human looked. Add `approved` during a contact-sheet review
and ship only approved photos.

---

## 9. Original artwork where there is nothing to photograph

Service pages, explainers and blog posts have no place to photograph, and stock
imagery for these niches is all handshakes and car keys. Generate SVG instead:
nothing to license, no attribution line, exact brand palette, sharp at any
density. **42 pictures came to 136KB** — less than one stock JPEG.

**Pattern: shared frame + motif vocabulary.** Do not author one-offs.

```python
def frame(inner, gid, title=""):
    """Gradient, faint grid, accent glow, hairline edge."""
    # NOTE: unique id suffix per image — SVG ids are document-global once
    # inlined, and reuse silently cross-wires fills between images.

def car(x, y, scale): ...
def cert(x, y, label): ...
def shield(x, y): ...
def clock(x, y, r): ...

SERVICES = {"owner-policy": ("Owner's policy", car(...) + shield(...), "alt")}
```

**Make the picture carry a fact.** A timeline bar whose length *varies* with
"not 3 years" struck through. A clock beside a large **10** for a ten-day
deadline. An unbroken coverage line that *snaps*. Each is the thesis of its
page as a diagram.

**Alt text lives with the drawing** so it cannot drift. **Decorative vs
meaningful:** card thumbnails get `aria-hidden="true"` and `alt=""` (the
headline beside them carries the meaning); in-article figures get real alt text.

Verify the set at build time — `missing = [s for s in SERVICES if s not in ART]`.

---

## 10. Internal linking, enforced

Three contextual links per blog post, in real sentences, not a link dump.
Data-driven with a build-time guard:

```python
INTERNAL_LINKS = {
  "post-slug": [("phrase that already exists in the body", "/target.html"), …x3],
}

def linkify(html_text, pairs, used):
    """Link the first unused occurrence of each phrase, only in text runs
    outside existing tags so nothing is double-wrapped."""
    ...

# and then, non-negotiably:
missing = [p for p, _ in pairs if p not in used]
if missing:
    raise ValueError("internal-link phrase not found in body: %r" % missing)
```

That guard earned its keep immediately — it rejected five phrases assumed to be
in the copy and were not, caught a link pointing at a URL that did not exist,
and flagged two phrases living inside `<ul>` blocks (which are escaped and
cannot take injected HTML). Without it, posts silently ship with two links.

---

## 11. Placeholders, preview mode, regulated niches

**Declare every unknown** so the validator can tell a deliberate gap from a
substitution bug:

```python
SITE = {"name": "[AGENCY NAME]", "phone_display": "[PHONE]", …}
KNOWN_PLACEHOLDERS = ["[AGENCY NAME]", "[PHONE]", …]
```

```python
for tok in set(re.findall(r"\[[A-Za-z][^\[\]]{2,}?\]", src)):
    if tok not in KNOWN_PLACEHOLDERS:
        problems.append("undeclared placeholder %s" % tok)
```

Two things that made it work: **no upper bound on token length** (a first pass
used `{2,80}` and an 86-character token slipped past), and **keep tokens plain**
(if the escaper rewrites ` -- ` to `&mdash;`, the rendered token no longer
matches the declared one).

**The form endpoint is not an ordinary placeholder.** An unfilled phone number
is obviously unfinished; a form `action` pointing at a dead URL is invisible —
the visitor submits, gets a 404, and assumes it sent. Make it the one
placeholder that **hard-fails the build**, and ship a stub page that says
plainly nothing was submitted and gives the phone number.

**PREVIEW mode.** A public site carrying `[LICENCE #]` must not be indexed. One
flag drives three mechanisms:

```python
PREVIEW = True   # flip to False at launch — a deliberate step, never a default
```

1. `<meta name="robots" content="noindex, nofollow">` on every page
2. `robots.txt` → `Disallow: /`
3. `X-Robots-Tag: noindex, nofollow` response header (`vercel.json` / `_headers`)

---

## 12. Validation gates — run before every deploy

```
 1. leftover template variables ($var / {var})
 2. invalid JSON-LD (one trailing comma silently kills the block)
 3. broken root-relative links and missing image assets
 4. missing structural tags (truncated writes)
 5. schema claiming rating/hours with no matching VISIBLE element
 6. template leakage across HTML *and* .js .css .txt .json .xml .svg .php
 7. escaped entities rendering as literal text (&amp;middot;)
 8. bare <header>/<footer> nested inside <main>
 9. grid tracks using `1fr` without a zero floor
10. CSS url() references pointing at files that do not exist
11. undeclared bracket placeholders
12. form endpoint still a placeholder  → HARD FAIL
```

Checks 6–10 were each added *after* the corresponding bug shipped. Check 10
found two more latent bugs the moment it existed.

---

## 13. Deployment

- Sequential FTP of ~90 files hangs past most timeouts. Parallelise, but create
  remote directories **serially first** to avoid a race.
- CDN edge caches can serve a stale or truncated page indefinitely. If a page
  renders blank while its source is fine, **purge the cache before debugging
  the HTML**.
- Verify live: fetch every sitemap URL, confirm 200s.
- Search Console: verify the new domain **before** redirecting or retiring the
  old one — the old property is often verified via a file on the old host.
- A redirect can "work" while GBP traffic still hits the old site if the old
  host has two endpoints and only one honours redirects. Check both.

---

## 14. Intake — what to ask before building

| | Needed for |
|---|---|
| Company name | titles, schema, footer, logo |
| Niche | service list, artwork, copy |
| City + state | the geography |
| Street address + ZIP | `PostalAddress` schema, footer, contact |
| Phone | every CTA on every page |
| Email | contact page, schema |
| Domain | canonicals, schema `@id`, sitemap |
| Hours, licence no., contact name | optional — bracket if unknown |

Accept partial answers. Bracket the rest. **Never invent.**

---

## 15. Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Pages read as spun | Only the city name varies | Tie content to a real local condition |
| Thin/doorway pages | Built pages for road corridors | Only real named places get pages |
| Wrong photo on a real place | Trusted Places' first photo | Contact-sheet QA pass |
| Schema silently absent | One malformed JSON-LD block | Validate before deploy |
| Old client's phone still live | It was in a runtime-injected JS widget | Scan JS/CSS too |
| Header keeps old brand colour | Palette hardcoded outside the variables, incl. `%23` hex | Audit literals by hue |
| Form collects nothing | Template's PHP hardcoded to `your@email.com`; its JS faked success | Delete both; gate the endpoint |
| Card titles vanish | Nested `<header>` captured by `header{position:fixed}` | Use a div |
| Form clipped on phones | `1fr` min-content floor | `minmax(min(Npx,100%),1fr)` |
| `&middot;` as literal text | Entity in a source string, then escaped | Literal Unicode |
| Sections blank after anchor jump | Scroll-reveal on whole sections | Animate groups; add `.js` guard + failsafe |
| "CSS isn't applying" | Cache-buster never changed | Derive `?v=` from mtime |
| Spacing looks broken | 120px section padding on text-dense pages | ~72px / ~44px |
| Unusable on a phone | Desktop type scale down to 320px | Explicit phone block; 16px inputs |
| Screenshot shows a gutter that isn't in the DOM | Preview pane under-painted | Trust `getBoundingClientRect` |
| Client change costs hours | Pages hand-written | Generator with data/template split |

---

## 16. Working style that made this go well

- **Read before you build.** Trace what a change touches; the smallest diff in
  the wrong place is a second bug.
- **Fix the root cause, once, where all callers route through.**
- **Automate the check the moment a bug is found**, so it cannot recur.
- **Blocking questions only when proceeding would be unsafe or useless.**
  Everything else: state the assumption and keep building.
- **Report faithfully.** If a screenshot disagrees with the measurement, say
  which you trusted and why. If you broke something and reverted, say so.
- **Scope discipline.** "Change one page, then when I approve, do the rest" is
  a gift — the generator makes the rollout a one-line change afterwards.
