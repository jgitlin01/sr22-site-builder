# Frontend gotchas

Bugs from real builds that are invisible until someone looks at the right
screen size, and that a human reviewer will notice before you do.

---

## `1fr` overflows its container

The single worst CSS bug in the SR-22 build, present on every page carrying a
quote form and invisible until measured.

`1fr` means `minmax(auto, 1fr)`, and that `auto` floor is **min-content**. A
grid item containing something unbreakable — a `<select>` whose longest option
reads "Driving without insurance / accident claim" — forces its track wider
than the container:

```
container 335px  →  grid-template-columns computed to 395px
```

No horizontal scrollbar on `<html>` (an ancestor had `overflow:hidden`), so
nothing looked wrong. The form was just clipped.

```css
/* wrong */ grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
/* right */ grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr));

/* and let the items themselves shrink */
.grid > * , .grid input, .grid select, .grid textarea { min-width: 0; max-width: 100%; }
```

Rule of thumb: **any grid that can contain a `select`, a long word, an image,
or a `pre` needs `minmax(0, …)` or `minmax(min(Npx,100%), …)`.**

## HTML entities inside strings that get escaped

If your generator escapes output — and it should — then an entity written into
a Python string is escaped along with everything else:

```python
blurb = "Davidson County &middot; SR-22 filing"
esc(blurb)   # -> "Davidson County &amp;middot; SR-22 filing"
```

Which renders on the page, in front of the client, as literal
`&middot;`. It shipped on 16 city cards.

**Use literal Unicode in source strings.** `·` `—` `–` `’` `“` `”` `•` `…`
survive both escaped and raw contexts untouched, because `html.escape` only
touches `& < >` and quotes. Convert once:

```python
ENT = {'&middot;':'·', '&mdash;':'—', '&ndash;':'–', '&rsquo;':'’',
       '&ldquo;':'“', '&rdquo;':'”', '&bull;':'•', '&hellip;':'…'}
# leave &amp; &nbsp; &lt; &gt; alone — those are structural
```

Add a validation check for `&amp;[a-z]{2,8};` in output.

## Entrance animations that hide content

Scroll-reveal patterns set `opacity: 0` and restore it when an
IntersectionObserver fires. Three ways that goes wrong, all seen:

**1. It hides whole sections permanently.** Put `data-animation` on a
`<section>` and the observer may never fire for it — restored scroll positions,
anchor jumps, and fast scrolling all skip it. Three sections of body copy sat
invisible after a jump-scroll, with no way back except scrolling away and
returning. Animate *card groups and images*, never a section wrapping prose.

**2. It hides above-the-fold copy.** The hero faded in, so first paint was a
photograph with no words on it — bad for the reader and bad for LCP. **Never
animate anything above the fold.**

**3. It hides everything if the script fails.** `opacity:0` in a stylesheet
applies whether or not the JS ever runs, so a 404 on one script blanks the page
for readers and crawlers. Gate it:

```html
<script>document.documentElement.classList.add('js')</script>
```
```css
.js [data-animation] { opacity: 0; }
@media (prefers-reduced-motion: reduce) {
  .js [data-animation] { opacity: 1 !important; animation: none !important; }
}
```

And ship a failsafe that reveals anything still hidden after a grace period.
Motion should be a bonus, never a precondition for reading the page.

## Cache-busting, or "my CSS isn't applying"

Editing a stylesheet and re-running the generator changes nothing if the link
still says `?v=1`. Lost real time to this — the rules were correct and the
browser was serving the old file. Derive the version from the file:

```python
CSS_FILES = [os.path.join(ROOT, "assets/css", f) for f in ("site.css", "extra.css")]
CSS_VER = str(int(max(os.path.getmtime(f) for f in CSS_FILES if os.path.exists(f))))
```

## Section rhythm from a photo-led template

Templates built for image-heavy marketing sites use 100–120px section padding.
On a text-dense local page that stacks a dozen short sections, it reads as
broken layout — the client asked "why is the spacing messed up". Drop to
~72px desktop / ~44px phone and let background tints do the separating.

## The phone type scale is not automatic

A "responsive" template can still keep desktop sizes down to 320px. Measured on
an untouched clone at 375px:

| Element | Rendered | Effect |
|---|---|---|
| Eyebrow | 16px uppercase, 0.25em tracking | wrapped to 2 lines, 81px tall |
| Licence line | 16.8px | 151px tall |
| City hero | — | **1061px on an 812px screen** |

Add an explicit phone block. Also set `input, select, textarea { font-size: max(16px, 1rem) }`
at every width — iOS zooms the whole page when a focused field is under 16px.

## Verify by measuring, not by screenshot

Preview panes lie. In this environment screenshots came back blank after
programmatic scrolls, showed stale paints, and under-painted the right edge of
wide viewports — which reads as a layout gutter that does not exist. At an
800px viewport `header`, `.hero` and `body` all measured exactly 800 right-edge
with no scrollbar gap, while the screenshot showed 80px of white.

When a screenshot looks wrong, confirm with geometry before you "fix" anything:

```js
document.elementFromPoint(400, 300)            // what is actually painted there
el.getBoundingClientRect()                     // real position and size
document.documentElement.scrollWidth > clientWidth   // real horizontal overflow
getComputedStyle(el).opacity                   // is it hidden or just not drawn
```

`scripts/responsive_audit.js` automates the sweep — run it instead of eyeballing.
