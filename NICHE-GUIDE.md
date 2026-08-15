---
name: sr22-site-builder
description: Build a complete SR-22 / high-risk auto insurance website for an agency in any US state — homepage, 18 service silo pages (owner, non-owner, after a DUI, suspended licence, ignition interlock, under-21, CDL, rideshare, getting off SR-22), city and neighbourhood location pages, 8 researched blog guides, schema and sitemap. Use whenever someone wants an SR-22 site, SR22 insurance pages, high-risk auto insurance marketing, DUI insurance pages, licence reinstatement content, or a filing-agency website for a city or state.
---

# SR-22 site builder

A content pack for the `local-site-builder` engine. That skill owns the
template, generator, validators and reference docs; this one supplies the
SR-22 service architecture, the researched page structure, the blog set and
the artwork.

**Read `local-site-builder/SKILL.md` first** — every rule there applies here,
especially *never fabricate*. Insurance is regulated and YMYL.

---

**Before writing anything, work through `RESEARCH-PROTOCOL.md`.** SR-22 is state law and every state differs — the ten questions in that file decide the whole site, and county-level facts decide the local pages.

## Start by asking

Same intake as the engine — company name, address, phone, email, city, state,
domain — plus two that matter for this niche:

- **State**, because SR-22 rules are state law and differ substantially
- **Producer licence number**, or a `[TN PRODUCER LICENSE #]`-style placeholder

## Build

```bash
python3 ../local-site-builder/scripts/scaffold.py --dir ~/projects/<slug> \
  --company "…" --niche "SR-22 insurance" --city … --state … \
  --domain … --palette navy
cp content/{config.py,blog.py,make_blog_art.py,make_service_art.py} ~/projects/<slug>/
```

`content/config.py` is the Tennessee build, complete and working. Treat it as
the shape to fill, not the answer: **every fact in it is Tennessee-specific and
must be re-researched for the target state.**

---

## The research that makes this niche worth publishing

SR-22 content online is saturated with thin, near-identical national pages.
The moat is state-specific accuracy, and there is a reliable way to find it:
**read the state's own Department of Motor Vehicles / Department of Safety
pages and note where they disagree with the national consensus.**

On the Tennessee build that produced the single biggest differentiator:

> Nearly every competing page says an SR-22 lasts three years. Tennessee ties
> the filing period to the **length of the suspension or revocation**. A
> one-year revocation is a one-year requirement.

That one correction is why an AI assistant cross-checking against tn.gov would
cite that page over ValuePenguin. Find the equivalent for your state.

### Facts to verify from the state's own pages, every time

| | Why it matters |
|---|---|
| **How long the filing lasts** | The most-got-wrong fact in the niche |
| Who may file it, and how | Most states require electronic filing by a licensed carrier — the driver cannot self-file |
| Minimum liability limits | e.g. 25/50/25, cite the statute |
| The list of triggering violations | Use the state's own wording; group them for scannability but say the grouping is yours |
| What happens on a lapse | Usually re-suspension under a named rule |
| Reinstatement fees and any instalment plan | TN: owe over $75 → $25 down, $75/quarter, up to 60 months |
| Restricted / hardship licence process | TN: **10 days** from the judge's signature, SR-22 must already be in force |
| Ignition interlock rules | Minimum periods by offence, the compliance window, removal process |
| Where to physically go | Which offices are full-service vs express vs kiosk — only some process reinstatement |

**Publish what you could not confirm.** On the TN build the out-of-state SR-22
waiver could not be verified on tn.gov (only the interlock waiver is
published), so the site says so and tells readers to get a written answer.
That reads as credibility, not weakness.

## Service architecture (18 pages)

Owner · non-owner · after a DUI · driving uninsured · points and repeat
violations · reckless/racing/hit-and-run · unsatisfied judgment · out-of-state
· same-day filing · payment plans · full coverage with a filing · CDL ·
rideshare and delivery · **getting off SR-22** · motorcycle and household ·
suspended-licence insurance · SR-22 with ignition interlock · drivers under 21.

Two of those are differentiators almost nobody offers:

- **Getting off SR-22** — monitoring the term and re-shopping the moment the
  requirement clears. Clients lose the most money here.
- **Suspended-licence insurance** — kills the "you can't buy insurance without
  a licence" myth, which is false and drives real search volume.

## Blog set (8 guides, ~1,000 words each)

How long you need one · reinstating after a DUI · the restricted-licence
deadline · owner vs non-owner · what reinstatement actually costs · what
happens if it lapses · SR-22 vs FR-44 vs SR-50 · moving between states.

Each carries three images and three contextual internal links — see the engine's
`references/original-artwork.md` and the `INTERNAL_LINKS` pattern in
`content/blog.py`, which fails the build if a declared phrase is not present in
the prose.

## Local angle for a filing agency

The strongest per-city differentiator is **which office handles reinstatement**.
States publish office lists with service levels; only full-service locations
process reinstatements, and sending someone to a kiosk wastes their afternoon.
Pair that with the county court that clears the conviction, and each city page
has something true, specific and useful that no national competitor has.

## Compliance

- Avoid "guaranteed lowest rates" / "cheapest in <city>"
- Any rate figure gets a visible disclaimer that it is an estimate, not a quote
- Display the agency licence number
- Tell the client in writing that a licensed compliance reviewer must sign off
