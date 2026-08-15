# Research sources

Batch these — several lookups per turn, not one at a time. County-level facts are shared
by every city in that county, so research once and reuse.

## Population, demographics, geography

**Source:** Wikipedia's article for the city/CDP is the fastest reliable route to the
census figure, and it states the census year explicitly.

**Watch out:** aggregator sites (worldpopulationreview, city-data, etc.) report wildly
different numbers for the same place — often because they're mixing the CDP, the CCD,
and the metro area, or projecting estimates. In one build, two sources gave 114,287 and
124,523 for the same 2020 CDP. Always cite the census year, prefer the primary census
count over an estimate, and if two sources disagree, use the one that names its
methodology.

**Useful beyond raw population:** median age and percent 65+ (tells you whether to
lead with low-maintenance/retirement angles), median household income, and urban vs
rural split. Wikipedia CDP articles usually carry all of these.

## Landmarks / things to do

Wikipedia's article for the place usually lists the real ones. Prefer specific named
places with a Google presence (parks, museums, piers, preserves, stadiums) over vague
categories, because those are the ones that will resolve to a real Google Place with a
photo in the photo pipeline.

## Hospitals

Search the regional health system by name (e.g. "<Health System> locations addresses").
You want the facility name + street address, and it's worth noting trauma level or
"nearest ER" when a place has no hospital of its own — that's genuinely useful to a
resident and shows real local knowledge.

## Courthouses / civic

Search "<County> County courthouse address" and the county clerk's site. Note when a
community has no courthouse of its own and routes to the county seat — saying that
plainly is more useful than implying every small CDP has its own court.

## Schools

Two-part approach, and the second part matters:

1. Name real schools that serve the area (search "<city> public schools list names").
2. **Link to the district's official school locator** for zoning.

Attendance boundaries change, and a page that asserts a specific address is zoned to a
specific school will eventually be wrong and can genuinely mislead a family. Naming real
schools plus linking the locator is both more accurate and more useful.

District locator examples: `leeschools.net`, `collierschools.com/schools`,
`yourcharlotteschools.net`.

## Transit

Find the county/regional transit authority (LeeTran, Collier Area Transit, etc.). Capture
the authority name, official URL, rough service span, and coverage.

**Do not enumerate specific bus stops or route numbers.** Route structures and stop
locations change, you usually can't verify street-level accuracy from a search, and a
wrong stop is a genuinely bad user experience. Describe the system and link the trip
planner.

## Events

Link the official city/county/chamber events calendar. Never hardcode dated event
listings — they're stale within days and make the whole site look abandoned. Naming a
few genuinely annual, long-running events ("the air show," "the weekly farmers market")
is fine because those are stable; specific dates are not.

## Dining

Local press and city magazines (Gulfshore Life-type publications), plus "best restaurants
<city>" searches. Prefer long-established, well-known places over new openings — a
restaurant that closed six months after you published makes the page look neglected.
Include a short descriptor ("waterfront seafood", "steakhouse") so it reads as local
knowledge rather than a scraped list.

## Climate / weather

Climate **normals**, not a forecast. Annual rainfall, wet/dry season months, summer and
winter average highs. Sources: NWS climate normals, weather-and-climate.com, usclimatedata.

Label it as normals on the page. A "weather" section that looks like live data but is
static reads as broken; one that's clearly framed as typical climate is genuinely useful
— especially when you tie it to why it affects the service being sold.

**No weather API needed** for this. Only add one if the user specifically wants live
current conditions, which is a different feature with an ongoing key + cost.

## Neighborhoods

Local knowledge plus map inspection. The test for "does this deserve a page" is whether
you can say something true and specific about it beyond its name. Named
communities/subdivisions/districts pass; road corridors fail.

Be conservative on subdivision names — a confidently-wrong neighborhood name is an
instant credibility hit with exactly the local audience you're targeting. When unsure,
describe by adjacency instead ("bordered by X to the west"), which Wikipedia CDP articles
often state directly.

## Population, as of this build

The obvious routes both fail now:

- `api.census.gov` returns **"Missing Key"** — it requires a free API key even
  for the decennial datasets that used to be open.
- `census.gov/quickfacts/...` returns **403** to automated fetches.

What works without a key: the Wikipedia "List of municipalities in <state>"
article, which carries the 2020 decennial figure and the county for every
incorporated place in one table — one fetch for a whole state, and the numbers
matched the official figures on spot-check.

Whatever the source, **label the year on the page** ("pop. 152,769 (2020
Census)"). Aggregators disagree, and an unlabelled number is the kind of claim
a local reader notices is stale.

Named neighbourhoods are usually not census places and have no population at
all. Omit it rather than substituting a city-wide figure — and give the page a
real local anchor instead (ZIP codes, the nearest civic office, what changes
about the job there).
