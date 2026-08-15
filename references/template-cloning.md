# Cloning a previous client's site

The fastest way to start a new fleet is to copy a build that already works.
It is also the fastest way to publish another client's phone number under your
new client's brand. Everything here came from doing exactly that.

Treat the clone as **hostile input you happen to own**. The old client's
identity is hiding in more places than you will guess, and the places that
matter most are the ones a grep of the HTML will not find.

---

## 1. The leakage gate must scan more than HTML

This is the one that bites. On the SR-22 build the previous client's phone
number survived every HTML grep because it lived here:

```js
// assets/js/corner-call.js  — a widget that injects itself at runtime
var a = document.createElement('a');
a.href = 'tel:+12393202623';                      // <- invisible to HTML grep
a.innerHTML = '... Call Here for Turf Discounts! ...';
document.body.appendChild(a);
```

It rendered as a floating call button on all 66 pages.

**Scan every text file in the tree**, not just `*.html`: `.js`, `.css`, `.txt`,
`.json`, `.xml`, `.svg`, `.php`. Build the pattern list from the old client's
real data and make it a hard failure:

```python
LEAKS = [
    r"oldclientdomain\.com", r"Old Client Name",
    r"239-320-2623", r"\(239\) 320-2623", r"\+12393202623",   # every format
    r"Hendry St", r"Fort Myers",                              # street, city
    r"ChIJvdwFNYpB24gRHOC8Sg5xOVo",                           # Google place_id
    r"oldclient@", r"OldClientSocialHandle",
    r"google[0-9a-f]{16}\.html",                              # GSC verification
    r"\bartificial turf\b", r"putting green",                 # old niche terms
    r"Mowix",                                                 # template vendor
]
```

Then make the widget read its data from the page instead of carrying its own
copy, so it can never drift again:

```js
var navPhone = document.querySelector('.nav-phone');   // single source of truth
a.href = navPhone.getAttribute('href');
```

## 2. Hardcoded colours live outside the CSS variables

Recolouring by redefining `:root` variables gets you 80% of the way and then
leaves a green header on a navy site. Templates commonly hardcode their palette
inside their own custom section:

```css
header { background:#0e2b12; }                    /* fixed site header */
.hero__eyebrow { color:#c9e265; }
.phone-flash { background:#aadb4e; }
```

Find every colour literal and judge it by hue, not by hoping:

```python
import re, sys
hexes = set(re.findall(r'#[0-9a-fA-F]{6}', open('main.css').read()))
for h in hexes:
    r, g, b = (int(h[i:i+2], 16) for i in (1, 3, 5))
    if g > r and g > b and g - max(r, b) > 8:      # green-ish; adapt to old palette
        print(h)
```

**Also search URL-encoded hex.** Inline SVG data URIs escape the `#`:

```css
background-image: url("data:image/svg+xml;utf8,<svg ...
    stroke='%232e7d32' ...");                      /* %23 == # */
```

A plain `#2e7d32` search will never see it.

## 3. Delete the template's form handling — do not adapt it

Bundled contact backends are demos, not working code. The one on this build:

```php
$to = "your@email.com";                            // never changed by anyone
$valid_services = ["Lawn Care", "Hardscaping", ...];   // old niche's categories
if (!in_array($service, $valid_services)) { http_response_code(400); exit; }
```

It would have rejected 100% of the new site's submissions while looking
installed. Its companion JS was worse — it intercepted submit, showed a success
message, and sent nothing anywhere:

```js
contactForm.addEventListener("submit", function (e) {
  e.preventDefault();
  showAlert(successMsg, errorMsg, allFilled);      // no network call at all
});
```

Delete both. Point the form at a real endpoint, and until there is one, see
`preview-and-placeholders.md` for the stub pattern.

## 4. Never carry over `aggregateRating`

The old build's schema had a real 5.0 / 8 reviews. Copied forward, that is
fabricated review data on the new client's domain — a manual-action risk, not
a style nit, and worse on a YMYL site. Same for `openingHoursSpecification`,
`geo`, `hasMap`, `sameAs`, and the Search Console verification file.

Emit these **only** when real values exist:

```python
if not site["street"].startswith("["):
    obj["address"] = {...}
if site["geo"]:
    obj["geo"] = {...}
# aggregateRating: omitted entirely until real reviews exist
```

## 5. Bare element rules will capture your new markup

Templates style landmark elements directly:

```css
header { position: fixed; top: 0; z-index: 1000; background: #0e2b12; }
```

So the moment you write a perfectly reasonable card:

```html
<article class="violation-group">
  <header class="violation-group__head">…</header>   <!-- yanked to viewport top -->
</article>
```

…all four card headers get pinned to the top of the page, stacked on each
other, and the card titles vanish. Took a screenshot to notice.

**Before nesting `<header>`, `<footer>`, `<nav>`, `<aside>`, `<section>` or
`<main>` inside a component, grep the stylesheet for a bare rule on that tag.**
If one exists, use a `div`. Add the check to validation:

```python
main_html = re.search(r'<main>(.*?)</main>', src, re.S).group(1)
for tag in ("header", "footer"):
    if re.search(r'<%s[ >]' % tag, main_html):
        problems.append("bare <%s> inside <main> — check for a bare element rule" % tag)
```

## 6. Strip the old vendor's identity from the CSS too

`main.css` opened with the template vendor's name, project description and a
masking image called `Mowix-Masking-1.png`. Rename the asset, rewrite the
header comment. It shows up in view-source and in the client's asset folder.

---

## Clone checklist

- [ ] Leak patterns cover phone (all formats), address, city, domain, email,
      social handles, place_id, GSC file, old-niche vocabulary, vendor name
- [ ] Leak scan runs over HTML **and** `.js .css .txt .json .xml .svg .php`
- [ ] Colour literals audited by hue, including `%23`-encoded hex
- [ ] Template form backend and fake form JS deleted, not adapted
- [ ] `aggregateRating` / hours / geo / sameAs / GSC file all removed
- [ ] Any runtime-injected widget reads its data from the page
- [ ] No bare landmark elements nested inside components
- [ ] Vendor name and asset filenames renamed
- [ ] Leak gate wired into `validate.py` as a **hard** failure before first deploy
