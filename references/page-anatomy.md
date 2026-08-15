# Page anatomy and schema

## City page sections

Order matters — conversion elements early, depth after, form before the sibling links.

### 1. Hero
- `<h1>`: `<Service> in <City>, <ST>` — the exact phrase people search
- Subhead naming the county and the core offer
- **CTA + click-to-call inside the hero.** Visitors from a "near me" search are often
  ready to call; making them scroll to find the number loses them. Reuse the homepage's
  existing hero CTA classes so it looks native.
- Breadcrumb: Home / Service Areas / City

### 2. Quick Answer box
The full offer in ~40 words: who, where, from what address, turnaround, warranty, phone.
This is the block that gets lifted into AI answers and featured snippets, so it should
stand alone without the rest of the page.

### 3. Intro
Why this service, in *this* place. Anchor to a real local condition — not "City is a
beautiful place to live." See "Substantive uniqueness" below.

### 4. Benefits + process
Standard across pages, but weave the city name in naturally and link to relevant blog
posts / service pages.

### 5. At a glance
Card grid: county (Maps link), population + census year, distance/direction from the
office, typical timeline, warranty, quote turnaround.

### 6. About the city
Geography and character paragraph, then **Local Landmarks & Things to Do** as photo
cards. Each card: real photo, name linking to Google Maps in a new tab
(`target="_blank" rel="noopener"`), one-line description, photo attribution.

### 7. Healthcare & civic
Hospitals with addresses, courthouse/government. Follow with a row of "Open in Maps"
buttons for each named facility.

### 8. Schools, dining, transit, events
Real school names + link to the district's official locator. Real restaurants with
descriptors. Transit authority + link. Events calendar link. See `research-sources.md`
for why the volatile ones are links rather than lists.

### 9. Weather & why it matters
Climate-normals stat cards (rainfall, wet season, summer/winter highs) labeled as
normals, then a paragraph connecting climate to the service.

### 10. Neighborhoods & areas served
Photo cards for real neighborhoods (linking to their pages), plain text + Maps links for
corridors. Use `align-items:start` on the grid so text-only entries don't stretch to
match photo-card height.

### 11. Services grid
Every service, each card carrying the image from that service's own page — visual
consistency across the site and no new assets needed.

### 12. Driving directions
Real turn-by-turn prose using actual road names, the office address linked to Maps, and
an embedded directions map.

### 13. Quote form
Include a hidden field identifying which page the lead came from — this is how you prove
the location pages are producing leads.

### 14. Sibling links
Other cities (and, on neighborhood pages, sibling neighborhoods). This is what makes the
fleet crawlable and distributes authority.

## Neighborhood page sections

Lighter, and honest about being part of a parent city:

1. Hero + CTA, 4-level breadcrumb (Home / Areas / City / Neighborhood)
2. Quick Answer
3. About — description + photo + embedded map, linking to the parent city page for the
   shared civic detail rather than duplicating it
4. What the work looks like here — **driven by neighborhood type**, see below
5. Things to do nearby — reuse the parent city's landmark cards (honest: they genuinely
   are nearby)
6. Schools/dining/transit framed as "nearest," pointing at the parent city
7. Weather, process, services grid, form, sibling neighborhoods

## Substantive uniqueness

The thing that makes 88 pages defensible. Classify each location by a **type** that
changes the actual job, and write real copy per type. For a home-services niche:

| Type | The real condition |
|---|---|
| waterfront / canal | salt exposure at seawalls, high water table |
| golf / HOA community | written landscape standards, year-round appearance rules |
| barrier island | salt spray, wind-driven sand, unobstructed UV |
| established / older | compacted soil, mature tree canopy and root competition |
| new construction | engineered fill, thin topsoil over compacted subgrade |
| rural acreage | well water, partial installs make more sense than whole-parcel |
| urban / downtown | small hard-edged lots, no irrigation access, rooftop/courtyard |

Adapt the axis to the niche. Roofing → wind zone, salt corrosion, tile vs shingle stock,
HOA color rules. Pest control → mangrove/wetland proximity, slab vs crawlspace, seasonal
swarm timing. Medical/legal → demographics, commute patterns, insurance networks.

The test: could a competitor copy your page, change the city name, and have it be equally
true? If yes, it isn't differentiated yet.

## JSON-LD

Four blocks per page. Cross-reference with `@id` so they form one graph rather than four
disconnected objects.

**LocalBusiness** (`@id: <site>/#localbusiness`) — name, description, url, telephone,
email, PostalAddress, GeoCoordinates, priceRange, image, ContactPoint. Use the most
specific type available (`["LocalBusiness","HomeAndConstructionBusiness"]`).

**Service** — `serviceType`, `provider: {"@id": <localbusiness>}`, and `areaServed`:

```json
"areaServed": {
  "@type": "City",
  "name": "Naples",
  "containedInPlace": {"@type": "AdministrativeArea", "name": "Collier County"}
}
```

For neighborhoods, nest one level deeper with `"@type": "Place"` containing the City
containing the AdministrativeArea.

**WebPage** — `@id`, `url`, `isPartOf: {"@id": <website>}`, `about: {"@id": <localbusiness>}`.

**BreadcrumbList** — matching the visible breadcrumb; 3 levels for cities, 4 for
neighborhoods. The final item has no `item` URL.

Hub page swaps WebPage for `CollectionPage` and adds an `ItemList` of every location.

**Never emit `AggregateRating` or `Review` without real reviews.** Fabricated review
schema is a manual-action risk, not just an accuracy problem.

## Build notes

- Use `string.Template` (`$var`) for the page shell — JSON-LD is full of `{}` and
  f-strings will choke. Substituted *values* aren't re-scanned, so a `$$` inside a
  substituted JSON string (like `"priceRange": "$$"`) survives fine.
- Read 2–3 of the client's existing pages first and reuse their actual CSS class names,
  so pages look native instead of bolted on.
- Root-relative paths (`/assets/...`) throughout, since these pages live in
  subdirectories.
- Cache-bust CSS/JS query strings if the client's site uses them.
