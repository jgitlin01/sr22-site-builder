# Shipping before the client is signed

These fleets are usually built and deployed for review before the business
identity exists — no confirmed phone number, no licence number, no lead
destination. That is fine, as long as the unfinished parts are impossible to
miss and impossible to index.

---

## Declared placeholders, gated by the validator

Put every unknown in one place and declare it, so the validator can tell a
deliberate gap from a substitution bug:

```python
SITE = {"name": "[AGENCY NAME]", "phone_display": "[PHONE]", ...}

KNOWN_PLACEHOLDERS = ["[AGENCY NAME]", "[PHONE]", "[EMAIL]", "[HOURS]", ...]
```

```python
# any bracket token NOT declared is a generator bug, not a business placeholder
for tok in set(re.findall(r"\[[A-Za-z][^\[\]]{2,}?\]", src)):
    if tok not in KNOWN_PLACEHOLDERS:
        problems.append("undeclared placeholder %s" % tok)
```

Two things that made this actually work:

- **No upper bound on the token length.** A first pass used `{2,80}` and an
  86-character `[AGENT BIO — 2-3 sentences: …]` token slipped straight past the
  gate. Keep tokens short (`[AGENT BIO]`) and put the instructions in a comment.
- **Escaping changes the token.** If the escaper rewrites ` -- ` to `&mdash;`,
  the rendered token no longer string-matches the declared one. Another reason
  to keep tokens plain.

## The form endpoint is not an ordinary placeholder

An unfilled phone number is obviously unfinished on screen. A form `action`
pointing at a dead URL is invisible — the visitor fills it in, hits submit,
gets a 404, and reasonably assumes their details went somewhere.

Make it the one placeholder that **hard-fails** the build, and give it a stub
so a real enquiry is never silently swallowed on a public preview:

```python
if site["form_endpoint"].startswith("["):
    hard_fail("quote form still posts to %s" % site["form_endpoint"])
elif site["form_endpoint"] == "/form-not-connected.html":
    warn_loudly("FORM IS NOT COLLECTING LEADS — stub in place")
```

The stub page says plainly that nothing was submitted, and gives the phone
number instead. Delete it once a real endpoint is wired.

## PREVIEW mode

A publicly reachable site carrying `[LICENCE #]` should not be in anyone's
index. One flag drives three mechanisms:

```python
PREVIEW = True   # flip to False at launch — a deliberate step, not a default
```

1. `<meta name="robots" content="noindex, nofollow">` on every page
2. `robots.txt` → `User-agent: *` / `Disallow: /`
3. an `X-Robots-Tag: noindex, nofollow` response header (`vercel.json`,
   `_headers`, or host config) — belt and braces, since the meta tag only helps
   if the page is parsed

Have the validator print a loud note while `PREVIEW` is on, so it can never be
forgotten at launch.

## Regulated industries: never invent a credential

Insurance, legal, medical, and financial sites are YMYL, and several of the
fields a template wants are **checkable claims**:

- producer / bar / licence numbers
- "licensed in <state>"
- years in business, number of clients served
- ratings and testimonials

If the client has not supplied it, ship the bracket token. Do not generate a
plausible-looking number. Also:

- Avoid superlatives the regulator cares about — "guaranteed lowest rates",
  "cheapest in <city>".
- Any figure from a third-party rate study gets a visible disclaimer on the
  same page saying it is an estimate, not a quote.
- Put a `[REVIEW REQUIRED]` note in the privacy and terms drafts and tell the
  client in writing that a licensed compliance reviewer needs to sign off.

## Verify primary sources, and publish what you could not confirm

The whole GEO position on a regulated build is *this page agrees with the
regulator's own page*. That means reading the government source, not a
competitor.

On the SR-22 build this produced the site's single biggest differentiator —
Tennessee ties the filing period to the length of the suspension, while nearly
every competing page says a flat three years — and it caught two errors in the
brief the client supplied.

When a claim cannot be confirmed, **say so on the page** rather than repeating
what other sites assert:

```python
UNVERIFIED = {
  "out_of_state_waiver":
    "The state publishes an out-of-state waiver for the interlock requirement. "
    "We could not confirm an equivalent published SR-22 waiver, so this site "
    "tells readers to get a written answer from the department.",
}
```

Rendered as a "What we could not confirm" section, this reads as credibility,
not weakness — and it is the difference between a page a model will cite and
one it will not.
