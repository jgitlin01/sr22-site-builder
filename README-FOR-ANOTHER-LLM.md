# Read this first

A complete website-building system for **SR-22 / high-risk auto insurance**. Everything needed is in this
folder — you do not need to invent the template.

## Start here, in order

1. **`RESEARCH-PROTOCOL.md`** — ten questions you must answer from the target
   state's own agency pages, plus the county and city layer. **SR-22 is state
   law and every state is different.** This is not optional and it is not a
   formality: on the reference build, nearly every competing page said an SR-22
   lasts three years, while the state's own page tied it to the length of the
   suspension. That one correction was the site's entire competitive position.
2. **`MASTER-PROMPT.md`** — the build method, architecture and every bug
   already hit.
3. **`NICHE-GUIDE.md`** — the 18-service architecture, the blog set, and the
   compliance rules for insurance advertising.
4. **`content/`** — a complete, working, deployed Tennessee config. Read it as
   the *shape* to fill. **Every fact in it is Tennessee-specific and must be
   re-researched for your state.**

## Why the research matters more here than almost anywhere

State law governs: how long the filing lasts, who may file it, minimum limits,
which violations trigger it, what a lapse does, reinstatement fees, restricted
licence deadlines, and interlock rules. **All of these differ by state.** Some
states do not use SR-22 at all — FR-44 is Florida and Virginia.

Then county and city decide *where the driver physically goes*, and that is the
local fact no national competitor has: many states run full-service offices,
express offices and self-service kiosks, and only full-service locations
process reinstatements.

## What is here

| Path | What it is | Skip it? |
|---|---|---|
| `RESEARCH-PROTOCOL.md` | The facts you must verify, and where they come from | **No. Do this first.** |
| `MASTER-PROMPT.md` | Architecture, rules, and every bug already hit | **No.** |
| `NICHE-GUIDE.md` | Service architecture and niche specifics | **No.** |
| `base/assets/` | The actual template — 4,227-line stylesheet, vendored Bootstrap/GSAP/Swiper, webfonts | **No.** This *is* the design; a description cannot reproduce it. |
| `base/lib/generate.py` | The 1,886-line page generator | **No.** Copy it, do not rewrite it. |
| `scripts/scaffold.py` | Creates a project from `base/` | Use it rather than copying by hand. |
| `scripts/validate.py`, `responsive_audit.js` | The gates | No — they catch what you will otherwise ship. |
| `references/*.md` | Deep detail per topic | Read the one you need. |
| `content/` | A complete working config from a deployed 66-page site | Read it — a working example beats any description. |

## Build

```bash
python3 scripts/scaffold.py --dir ./client-project \
  --company "…" --niche "SR-22 / high-risk auto insurance" --city … --state … --domain … --palette navy

cd client-project
python3 generate.py        # works immediately, from an empty config
python3 validate_site.py   # THE FAILURES ARE YOUR TO-DO LIST
```

Generate → validate → fill config → repeat until validation passes.
Palettes: `navy` `forest` `slate` `plum` `clay`.

## The rule you must not skip

**Research first. Write second.** Never fill `config.py` from memory, from a
competitor's site, or from a national comparison page — those are the sources
that are already wrong. Open the primary source, record the URL, put it in
`config.SOURCES`, and let the page print it.

Three categories, all mandatory where they apply:

1. **Regulator / authority pages.** Rules differ by state and often by county.
   Never assume a rule you learned for one state applies to another.
2. **Manufacturer specs and warranty terms.** Warranty length, material specs,
   drainage rates and certifications come from the manufacturer's published
   document for that product line — never from you.
3. **City, county and state facts** for every location page: county, population
   with the census year, the civic office that matters *and its service level*,
   climate, restrictions, permits, rebates, HOA rules.

If you cannot produce the URL for a claim, you cannot publish the claim.

**Never invent** phone numbers, licence numbers, addresses, ratings, review
counts, years in business or statistics. Ship a `[PLACEHOLDER]` and declare it
in `KNOWN_PLACEHOLDERS`.

**Publish what you could not confirm** in `config.UNVERIFIED`, rendered as a
"What we could not confirm" section. That reads as credibility, and it is the
difference between a page an AI assistant will cite and one it will not.

## Environment

Python 3 standard library only, no pip installs. A Google Places API key in
`.env` as `GOOGLE_PLACES_API_KEY=…` enables location photos; everything else
works without it.
