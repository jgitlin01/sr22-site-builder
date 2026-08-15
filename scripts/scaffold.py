#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a new location-page project from the skill's clean base.

    python3 scaffold.py \\
        --dir ~/projects/plumber-tulsa \\
        --company "Acme Plumbing" \\
        --niche "emergency plumbing" \\
        --city "Tulsa" --state OK \\
        --domain acmeplumbingtulsa.com \\
        [--palette navy|forest|slate|plum|clay]

Copies the base assets, writes a config.py stub, and drops in the generator,
art generators and validator. Nothing is cloned from a previous client's live
site, so there is no leakage to scrub -- that whole class of bug disappears.

WHAT THIS DOES NOT DO, and cannot:

  It does not write the content. Every niche has different authoritative facts
  (a state's SR-22 rules, a manufacturer's warranty terms, a licensing board's
  requirements) and the integrity of these pages rests entirely on researching
  them from primary sources before writing. The scaffold gives you the shell,
  the palette, the page architecture and a config with TODOs where the research
  goes. Phase 2 of SKILL.md is still real work.

  It also does not invent business identity. Anything unknown ships as a
  declared bracket placeholder -- see references/preview-and-placeholders.md.
"""

import argparse
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, "..", "base"))

# Dark brand colour + one accent used sparingly. Restrained on purpose: the
# vendored template signals value with size and colour, which reads as a promo
# sticker on a professional services site.
PALETTES = {
    "navy":   ("#0B2545", "#16324F", "#14508C", "#F2B441", "#D99A22"),
    "forest": ("#12332A", "#1B4A3C", "#2E7D6F", "#E0A458", "#C88C3C"),
    "slate":  ("#1B2430", "#2A3644", "#3E6B99", "#E3B23C", "#C79A2E"),
    "plum":   ("#2A1B33", "#3D2A48", "#7A4B8E", "#E8B44A", "#CB9834"),
    "clay":   ("#2E211C", "#43312A", "#A35A3C", "#E0B36A", "#C39751"),
}


def slugify(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


CONFIG_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
Data for {domain}.

RULE THAT MATTERS MOST: never fabricate. Everything on these pages is a
checkable claim about a real place or a real regulation. Cite the year on any
census figure, use real addresses, and omit a category rather than invent one.
Anything you could not confirm goes in UNVERIFIED and is surfaced on the page.
"""

# PREVIEW mode: noindex on every page, robots.txt Disallow, X-Robots-Tag
# header. Flip to False at launch -- a deliberate step, never a default.
PREVIEW = True

SITE = {{
    "domain": "{domain}",
    "base_url": "https://{domain}",
    "name": "{company}",
    "short_name": "{company}",
    "tagline": "{niche} in {city}, {state}",
    "niche": "{niche}",
    # Bracket tokens are deliberate. Fill from what the client supplies; never
    # invent a phone number, a licence number, or an address.
    "phone_display": "[PHONE]",
    "phone_href": "[PHONE-E164]",       # e.g. +19185550123
    "text_display": "[TEXT NUMBER]",
    "email": "[EMAIL]",
    "street": "[STREET ADDRESS]",
    "city": "{city}",
    "region": "{state}",
    "postal": "[ZIP]",
    "hours": "[HOURS]",
    "license": "[LICENSE #]",           # drop if the niche is unlicensed
    "agent_name": "[CONTACT NAME]",
    "agent_title": "[CONTACT TITLE]",
    "agent_bio": "[CONTACT BIO]",
    # Hard-fails the build until wired. A form posting to a dead URL 404s and
    # the visitor assumes it sent.
    "form_endpoint": "[FORM ENDPOINT URL]",
    "last_updated": "{today}",
    # Filled only when a real Google Business Profile exists. Never invent
    # coordinates, ratings or social URLs.
    "geo": {{}},
    "same_as": [],
}}

KNOWN_PLACEHOLDERS = [
    "[PHONE]", "[PHONE-E164]", "[TEXT NUMBER]", "[EMAIL]", "[STREET ADDRESS]",
    "[ZIP]", "[HOURS]", "[LICENSE #]", "[CONTACT NAME]", "[CONTACT TITLE]",
    "[CONTACT BIO]", "[FORM ENDPOINT URL]",
]

# --------------------------------------------------------------- research --
# TODO Phase 2. Every entry needs a primary source and the page prints it.
# See references/research-sources.md.
class _Todo(dict):
    """A dict whose missing keys report themselves instead of crashing.

    The shipped generator looks up config keys by name. Before the research is
    done none of them exist, so a plain dict raises KeyError and nothing
    renders at all. This yields a visible marker instead, which
    validate_site.py flags as an undeclared placeholder — an unfilled field is
    loud on the page but never fatal to the build, so you can generate and
    review the shell while the research is still in progress.
    """
    def __missing__(self, key):
        return "[TODO: %s]" % key


class _Sources(dict):
    """Same idea for SOURCES, whose values are (label, url) pairs."""
    def __missing__(self, key):
        return ("[SOURCE NOT SET: %s]" % key, "")


SOURCES = _Sources({{
    # "fr":       ("Name of the authority — page title", "https://..."),
    # "eservices":("Authority's self-service portal", "https://..."),
    # "census":   ("U.S. Census Bureau, 2020 Decennial Census", ""),
}})

# TODO The load-bearing claims for this niche, each (label, claim, source key).
# These are what an AI assistant lifts, so make each one self-contained. On one
# build the differentiator was a single rule nearly every competitor got wrong.
KEY_FACTS = []

# TODO Anything you could NOT confirm from a primary source. Surfaced on the
# page under "What we could not confirm" -- reads as credibility, not weakness.
UNVERIFIED = {{}}

DISCLAIMER = ("")   # required if the page quotes prices or rates

# --------------------------------------------------------------- services --
# One dedicated page each. `sources` is optional; add it when the copy asserts
# procedural detail rather than describing what the business does.
SERVICES = [
    # {{"slug": "emergency-callout", "h1": "...", "nav": "...",
    #   "icon": "fa-wrench", "summary": "...", "body": ["...", "..."],
    #   "sources": ["regulator"]}},
]

# ----------------------------------------------------------------- places --
# Tier the geography first (SKILL.md Phase 1). Incorporated places and CDPs get
# pages; road corridors and generic areas do NOT -- they become linked text.
COUNTIES = _Todo()

# `angle` is the local condition that actually changes the work here. This is
# the difference between a real fleet and 80 spun pages, and it is the part a
# competitor cannot copy.
CITIES = [
    # {{"slug": "{city_slug}", "name": "{city}", "county": "",
    #   "pop": 0, "places_query": "Downtown {city}, {state}",
    #   "intro": "", "angle": "", "commute": ""}},
]

NEIGHBORHOODS = []

# ------------------------------------------------------------------- copy --
FAQ = []      # (question, answer) — answer-first, 1-3 sentences then detail
STEPS = []    # (title, body) — the process, in the order it actually happens

CORE_PAGES = ["about", "contact", "faq", "services", "404"]

# --------------------------------------------------- optional page blocks --
# Every name below is referenced by generate.py and guarded by has(), so an
# empty value renders nothing and the page simply omits that section. Fill the
# ones your niche needs; delete the rest from the templates if a section will
# never apply.
#
# KEY_FACTS/TN_FACTS  the "what is this" answer block AI assistants lift
# VIOLATION_GROUPS    grouped triggers/eligibility, four labelled categories
# PAYMENT_PLAN        cost mechanics, if the niche has published fees
# TN_MINIMUMS         statutory minimums, if any
# DSC / DSC_HOURS     physical offices the reader may need to visit
# MAIL                where paperwork is sent
TN_FACTS = []          # rename freely; generate.py only checks emptiness
VIOLATION_GROUPS = []
PAYMENT_PLAN = _Todo()
TN_MINIMUMS = _Todo()
DSC = _Todo()
DSC_HOURS = ""
MAIL = _Todo(usps=[], courier=[], note="", source="")

# Shown wherever the page quotes a price, rate or estimate.
RATE_DISCLAIMER = ""

# Footer line. In a licensed trade this is where the licence number goes.
COMPLIANCE_NOTE = "{company}. [LICENSE #]"

# ------------------------------------------------------------------- blog --
# Add blog.py and uncomment when you write guides. See SKILL.md Phase 3.
POSTS = []
INTERNAL_LINKS = {{}}
POST_PHOTO = {{}}
# from blog import POSTS, INTERNAL_LINKS, POST_PHOTO
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--company", required=True)
    ap.add_argument("--niche", required=True)
    ap.add_argument("--city", required=True)
    ap.add_argument("--state", required=True)
    ap.add_argument("--domain", required=True)
    ap.add_argument("--palette", default="navy", choices=sorted(PALETTES))
    ap.add_argument("--geo-root", default=None,
                    help="URL segment for location pages (default: state slug)")
    a = ap.parse_args()

    dest = os.path.expanduser(a.dir)
    if os.path.exists(dest) and os.listdir(dest):
        sys.exit("refusing to scaffold into a non-empty directory: %s" % dest)
    if not os.path.isdir(BASE):
        sys.exit("base/ not found at %s -- is the skill installed completely?" % BASE)

    os.makedirs(dest, exist_ok=True)
    shutil.copytree(os.path.join(BASE, "assets"), os.path.join(dest, "assets"),
                    dirs_exist_ok=True)
    for f in os.listdir(os.path.join(BASE, "lib")):
        shutil.copy(os.path.join(BASE, "lib", f), os.path.join(dest, f))

    # palette
    dark, mid, link, accent, accent_hover = PALETTES[a.palette]
    css = os.path.join(dest, "assets", "css", "site.css")
    s = open(css, encoding="utf-8").read()
    s = re.sub(r"--accent-color:\s*#[0-9A-Fa-f]{6};", "--accent-color: %s;" % accent, s, 1)
    s = re.sub(r"--accent-color-2:\s*#[0-9A-Fa-f]{6};", "--accent-color-2: %s;" % dark, s, 1)
    s = re.sub(r"--accent-color-5:\s*#[0-9A-Fa-f]{6};", "--accent-color-5: %s;" % link, s, 1)
    s = re.sub(r"--accent-color-8:\s*#[0-9A-Fa-f]{6};", "--accent-color-8: %s;" % accent_hover, s, 1)
    open(css, "w", encoding="utf-8").write(s)

    # config stub
    from datetime import date
    open(os.path.join(dest, "config.py"), "w", encoding="utf-8").write(
        CONFIG_TEMPLATE.format(
            domain=a.domain, company=a.company, niche=a.niche,
            city=a.city, state=a.state, city_slug=slugify(a.city),
            today=date.today().isoformat()))

    geo_root = a.geo_root or slugify(a.state)
    open(os.path.join(dest, ".gitignore"), "w", encoding="utf-8").write(
        ".env\n__pycache__/\n*.pyc\n.vercel\n_preview*.html\n")
    open(os.path.join(dest, "README.md"), "w", encoding="utf-8").write(f"""# {a.domain}

{a.niche} in {a.city}, {a.state} — location-page fleet for {a.company}.

```bash
python3 generate.py        # rebuild every page from config.py
python3 validate_site.py   # pre-deploy gates — must PASS before uploading
```

Never hand-edit the generated HTML. Edit `config.py` and re-run.

## How this actually goes

Run `python3 generate.py` right now — it works, and produces a small site from
an empty config. Then run `python3 validate_site.py`: **the failures are your
to-do list.** Broken links to pages that do not exist yet, `[TODO: ...]` and
`[SOURCE NOT SET: ...]` markers, and the form-endpoint gate all point at
exactly what still needs filling. Generate, validate, fill, repeat.

The generator ships with the previous build's niche-specific copy in a few
places (the homepage quick-answer paragraph, some inline links). The validator
flags every one as a broken link or an undeclared placeholder, so none of it
can survive to launch unnoticed. Rewrite those strings for your niche as they
come up.

## Next steps

1. **Research (SKILL.md Phase 2).** Fill `SOURCES`, `KEY_FACTS`, `CITIES`,
   `SERVICES` in `config.py` from primary sources. This is the work that makes
   the fleet worth publishing; nothing else substitutes for it.
2. **Tier the geography (Phase 1)** before writing any of it. Incorporated
   places and CDPs get pages. Road corridors do not.
3. **Photos (Phase 4).** `fetch_photos.py . places.json`, then
   `contact_sheet.py .`, then **look at every image** and set
   `"approved": true` on the ones you keep. Expect to reject roughly half.
4. **Artwork** for pages with nothing to photograph — see
   `references/original-artwork.md`.
5. **Wire the form endpoint.** The build hard-fails until you do.
6. **Set `PREVIEW = False`** only at launch.

Geo root: `/{geo_root}/`
""")

    print("scaffolded %s" % dest)
    print("  assets    base template, %s palette" % a.palette)
    print("  config.py stub with research TODOs")
    print("  lib       generate.py, validate_site.py, art generators")
    print("""
next:
  python3 generate.py        # works now, from an empty config
  python3 validate_site.py   # the failures ARE your to-do list

The scaffold gives you the shell, the palette and the page architecture.
The facts are still yours to research and verify -- SKILL.md Phase 1 (tier the
geography) then Phase 2 (research from primary sources).""")


if __name__ == "__main__":
    main()
