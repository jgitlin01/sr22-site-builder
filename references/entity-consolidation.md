# Entity consolidation: tying the site to the real business

Location pages get the *content* right. This phase gets the *entity* right — making
sure Google (and AI answer engines) resolve your site, your Google Business Profile,
your socials, and your legacy web presence as the same business, not four unrelated
things. This is usually a short, high-leverage pass done once the page fleet is live.

## Pull real data from the GBP, don't estimate it

Ask the user to open their Google Business Profile (or share a screenshot / the GBP
edit panel) and pull:

- **Exact coordinates** — more authoritative than geocoding the address yourself
- **Place ID** — visible in a "share"/"embed" panel, or via a browser extension; used to build `hasMap`
- **Rating + review count** — real numbers only, never estimated
- **Hours** — the actual weekly schedule, including "closed" days
- **Social profile URLs** — Website tab / Contact tab often lists them directly, sometimes more completely than the user remembers having
- **Primary + secondary categories** — see below

Update `LocalBusiness`:

```json
{
  "geo": {"@type": "GeoCoordinates", "latitude": 26.6440025, "longitude": -81.8692654},
  "sameAs": ["<facebook>", "<instagram>", "<youtube>", "<tiktok>",
             "https://www.google.com/maps/place/?q=place_id:<PLACE_ID>"],
  "hasMap": "https://www.google.com/maps/place/?q=place_id:<PLACE_ID>",
  "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0",
                       "reviewCount": "8", "bestRating": "5", "worstRating": "1"},
  "openingHoursSpecification": [
    {"@type": "OpeningHoursSpecification",
     "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
     "opens": "09:00", "closes": "18:00"}
  ]
}
```

`sameAs` is what actually consolidates the entity — it's the explicit signal that these
profiles and this website describe the same business. Also add the profiles to the site
footer (`rel="noopener me"` — the `me` rel-value is the microformats convention for
"this link is also me," which some tools read alongside `sameAs`), replacing whatever
`href="#"` placeholders were there before.

## The rule that bit us twice: schema must match what's on the page

Google requires that structured data reflect **visible page content** — you cannot mark
up a 5-star rating or business hours that a visitor can't also see and verify by reading
the page. Two ways this fails silently:

1. You add `aggregateRating` to the shared `LocalBusiness` block used across every page
   type, but the special pages (a 404, a legal page) that reuse that block have nowhere
   for a rating to be visible.
2. You update the schema on 89 generated pages via the generator, but the 20-odd
   hand-authored root pages (`about.html`, `services.html`, blog posts) use a different
   template and don't get the matching visible element.

Both happened in this exact build. The fix is structural, not manual: whenever you add
`aggregateRating` or `openingHoursSpecification`, add the paired visible element
(a star badge, an hours line) in the *same* function/template pass, and run
`scripts/validate.py`, which checks the pairing on every page and fails loud if one side
is missing without the other. Don't ship a fix to only the generated pages and assume the
hand-authored ones inherited it — they didn't, because they're not generated.

## Legacy web presence: consolidate, don't abandon

Businesses migrating to a new site often have an old one sitting somewhere quiet — an S3
static site, an old Wix/Squarespace export, a legacy WordPress install left running.
That old URL may still be what's listed in the GBP, in directory citations, or in old
backlinks. Two options, in order of preference:

**Server-side 301 redirect** if you control the old host. Passes link equity forward and
is invisible to the user. Watch for **dual endpoints** — S3 in particular has a REST
endpoint (`bucket.s3.amazonaws.com`, ignores website-hosting config, serves raw objects)
and a website endpoint (`bucket.s3-website-<region>.amazonaws.com`, honors redirect
rules). External links and GBP fields point at whichever URL was originally used —
usually the REST one. Configuring "redirect requests" in bucket properties only affects
the website endpoint. If the REST endpoint is what's actually referenced, replace the
individual objects with redirect stub files instead (or in addition):

```html
<!DOCTYPE html><html><head>
<link rel="canonical" href="https://newdomain.com/">
<meta name="robots" content="noindex,follow">
<meta http-equiv="refresh" content="0; url=https://newdomain.com/">
<script>location.replace("https://newdomain.com/");</script>
</head><body><p>Moved to <a href="https://newdomain.com/">newdomain.com</a>.</p></body></html>
```

`noindex,follow` tells Google to drop the old URL from its index while still crediting
the link signal to the destination. Check whether the bucket/host is public-read — if
the old site was reachable, it already is, and the upload UI's "public access" warning
is the platform's standard caution, not a new risk being introduced.

**If you don't control the old host** (an old vendor's account, an expired platform),
skip the redirect and instead update every place that *points at* the old URL — GBP
website field, directory citations, social bios.

## Order of operations matters: verify Search Console before you redirect anything

If a Search Console property was verified via an HTML file hosted on the *old* site (a
`google<hash>.html` file is the tell), redirecting or deleting that host breaks
verification and orphans the property along with its search-performance history.

Sequence:
1. Verify the **new** domain in Search Console first — HTML-file upload if you control
   FTP/hosting and want it done in seconds, or a DNS TXT record at whichever provider
   actually controls the live DNS zone. Domain-property (DNS) verification is more
   durable than URL-prefix (file) verification since it survives future hosting moves.
2. Confirm the new property shows verified.
3. *Then* set up the redirect / replace the old files.
4. Submit the sitemap on the new property; check that the old property (if it still
   exists) isn't fighting it with conflicting signals.

**Check which DNS actually governs the domain before adding a TXT record.** A domain
registered at one registrar (Namecheap, GoDaddy) but pointed at a host's nameservers
(Hostinger, Cloudflare) has its DNS zone at the host, not the registrar — records added
in the registrar's "Advanced DNS" panel are silently ignored. If the nameservers aren't
the registrar's own defaults, add DNS records at the host instead.

## Google Business Profile category

Primary category is one of the strongest local-pack ranking factors, and it's tempting to
guess or reuse a category from memory — don't. Google's category taxonomy is a live,
searchable list, not something to recall from training data or infer from a marketing
blog. Have the user open the category field in GBP and type the core service term (e.g.
"turf," "roofing," "hvac") — Google surfaces every matching category it actually has, and
that's the only reliable source. Prefer the most specific match available as primary;
generic adjacent categories (e.g. "Landscaper" for a pure turf installer) work better as
secondaries. Drop any listed category that doesn't reflect real services offered — an
unrelated secondary category dilutes relevance rather than adding reach.

## Reviews unlock more than they used to

If the business has zero reviews, this whole phase's `aggregateRating` step is
unavailable — don't fabricate one. Flag it as the highest-leverage thing missing, and
revisit this phase once real reviews exist.
