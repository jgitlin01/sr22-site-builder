#!/usr/bin/env python3
"""The data shape a generator consumes. Copy, fill in per client, keep separate
from the template — that split is what makes later changes cheap.

Everything here is a checkable claim about a real place. Leave a field out rather
than guessing it. Comments mark where each value should come from.
"""

# ---------------------------------------------------------------- business
BUSINESS = dict(
    name="Example Turf Co",
    site="https://example.com",
    geo_root="florida",              # URL segment: /florida/<city>/
    office="123 Main St, Springfield, FL 33901",
    phone_display="(555) 123-4567",
    phone_tel="+15551234567",
    email="hello@example.com",
    lat=26.644007, lng=-81.869651,
    price_range="$$",
    schema_types=["LocalBusiness", "HomeAndConstructionBusiness"],  # most specific available
)

# services: (url, fontawesome_icon, title, blurb, image)
# image should come from that service's own page so the fleet looks native
SERVICES = [
    ("/residential.html", "fa-house", "Residential Installation",
     "Full replacement for front and back yards.", "svc-residential.jpg"),
    ("/commercial.html", "fa-building", "Commercial Installation",
     "Offices, storefronts, HOAs and multi-building properties.", "svc-commercial.jpg"),
]

# --------------------------------------------------------- shared climate
# Climate NORMALS, not a forecast. Source: NWS climate normals.
# Label as normals on the page so it doesn't read as broken live data.
CLIMATE_BASE = (
    "The region averages roughly 54 inches of rain a year, concentrated in a rainy "
    "season from June through October, with August the wettest month. Summer highs "
    "sit near 90&deg;F and January highs near 71&deg;F."
)
CLIMATE_STATS = [
    ("fa-cloud-showers-heavy", "54 in/yr", "Average annual rainfall"),
    ("fa-calendar-days", "Jun&ndash;Oct", "Rainy season"),
    ("fa-temperature-high", "~90&deg;F", "Summer highs (Aug)"),
    ("fa-temperature-low", "~71&deg;F", "Winter highs (Jan)"),
]

# ------------------------------------------------- county-level (shared)
# Research once per county, reuse across every city in it.
COUNTY_INFO = {
    "Example County": dict(
        transit_name="ExampleTransit",
        transit_url="https://example.gov/transit",
        transit_note="Describe the system and span. Do NOT enumerate stops or route "
                     "numbers — they change and you can't verify them.",
        schools_name="Example County Public Schools",
        schools_url="https://exampleschools.net/locator",  # official zoning locator
        events_name="Example County events calendar",
        events_url="https://example.gov/events",           # link, never hardcode dates
        events_url2=None,
    ),
}

# ------------------------------------------------------------- cities
# pop: primary census count + year. If sources disagree, prefer the primary count.
CITIES = [
    dict(
        slug="springfield", name="Springfield", county="Example County",
        pop="86,395", pop_year="2020",
        distance="about 10 miles", direction="west",
        img="hero-springfield.jpg",

        # Why this service, in THIS place — anchor to a real local condition.
        intro="...",
        # Geography/character + census detail.
        geo="...",
        # What about local conditions changes the actual job here.
        climate="...",
        # Real turn-by-turn using actual road names.
        directions="...",

        # 3-4 real landmarks that will resolve to a Google Place.
        attractions=[("Riverside Park", "A 40-acre park along the river.")],

        # Real facility names + street addresses.
        hospital="Example Regional Medical Center, 500 Health Way.",
        civic="Example County Courthouse, 100 Justice Dr.",
        # (label, maps query) for the "Open in Maps" buttons
        places=[("Example Regional Medical Center",
                 "Example Regional Medical Center, 500 Health Way, Springfield FL")],

        # Real schools; page also links the district locator for zoning.
        schools=[("Springfield High School", "High School")],
        # Real, established restaurants.
        dining=[("The Riverside Grill", "Waterfront American")],

        # Optional verified demographics
        median_age="44.9", pct_65=None, income="$83,583", pct_rural=None,

        # Mix of named neighborhoods (get pages) and corridors (text + Maps link only).
        areas=["Old Town", "Riverside", "Main Street corridor", "US-1 corridor"],
    ),
]

# -------------------------------------------------------- neighborhoods
# Only real named places. Road corridors do NOT belong here — a page for
# "Main Street corridor" has nothing true and specific to say and reads as thin content.
#
# kind drives the substantive copy so pages differ by what actually changes the job,
# not just by name. Adapt these types to the niche.
KINDS = {
    "waterfront": ("Salt drifting off the water and a high water table...",
                   "We spec salt-rated materials and build deeper drainage..."),
    "golf": ("Written landscape standards that don't pause for watering restrictions...",
             "Holds the manicured look year-round with no irrigation..."),
    "island": ("Constant salt spray, wind-driven sand, unobstructed UV...",
               "UV-stabilized and salt-tolerant spec, bases that drain through..."),
    "established": ("Soil compacted by decades of traffic, mature canopy shading...",
                    "We excavate and rebuild the base rather than laying over old..."),
    "new": ("Engineered fill with thin topsoil over compacted subgrade...",
            "That subgrade is close to ideal for a properly built base..."),
    "rural": ("Well water rather than city, and whole-parcel work rarely pencils...",
              "Targeted installs — a defined area near the house, a run, a green..."),
    "urban": ("Small hard-edged lots, shifting shade, nowhere to run irrigation...",
              "Works on courtyards, terraces and rooftops where a lawn can't..."),
}

# (name, city_slug, kind, blurb)
NEIGHBORHOODS = [
    ("Old Town", "springfield", "established",
     "The historic core, centered on the courthouse square."),
]
