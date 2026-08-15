# Generating original artwork

Clients ask for pictures. For a location fleet the honest answer is usually
"real photos of real places" (see `photo-pipeline.md`) — but service pages,
blog posts, and explainer sections have no place to photograph, and stock
imagery for these niches is all handshakes and car keys.

Drawing them as SVG from a generator solves it: nothing to license, no
attribution line cluttering the card, exact brand palette, sharp at any
density, and **42 pictures came to 136KB** — less than one stock JPEG.

---

## The pattern: shared frame + motif vocabulary

Do not author each image as a one-off. Write a generator so the whole set
shares a card and can be restyled in one edit.

```python
def frame(inner, gid, title=""):
    """Navy gradient, faint grid, soft accent glow, hairline edge."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" ...>
  <defs>
    <linearGradient id="bg{gid}" …>…</linearGradient>
    <radialGradient id="glow{gid}" …>…</radialGradient>
    <pattern id="grid{gid}" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0v40" fill="none" stroke="#FFF" stroke-opacity=".05"/>
    </pattern>
  </defs>
  …
{inner}
</svg>"""
```

**Give every gradient/pattern id a unique suffix.** SVG ids are document-global
once inlined; reuse silently cross-wires fills between images.

Then build a small parts kit and compose:

```python
def car(x, y, scale=1.0): ...
def cert(x, y, label, on=True): ...
def keys(x, y): ...
def shield(x, y, tick=True): ...
def clock(x, y, r=62): ...
def bars(x, y, values): ...

SERVICES = {
  "owner-policy":     ("Owner’s policy",  car(150,168,.78) + shield(516,196), "alt text"),
  "non-owner-policy": ("No car required", keys(190,200) + shield(470,196),    "alt text"),
  ...
}
```

Eighteen service illustrations that read as one set rather than eighteen
unrelated pictures, and a new one is three lines.

## Make the picture carry a fact

Decorative art is filler. The images that earn their place restate the page's
actual argument:

- a timeline bar whose **length varies**, with "not 3 years" struck through
- four numbered steps rising to a reinstated licence
- a clock beside a large **10** for a ten-day deadline
- an unbroken coverage line that **snaps** mid-run
- three certificates with only the relevant one lit

Each of those is the thesis of its article as a diagram. That is also what
makes them worth a `BlogPosting.image` entry.

## Alt text lives with the drawing

Store the description next to the code that draws it, and import it where the
markup is built. It cannot drift from the picture that way:

```python
ART = {"how-long": (draw_fn, "A timeline bar whose length varies, marked to "
                             "show the filing matches the suspension")}
```

## Decorative vs meaningful

Same image, two roles, two treatments:

```html
<!-- card thumbnail: the headline beside it already carries the meaning -->
<a class="card__art" href="…" tabindex="-1" aria-hidden="true">
  <img src="…" alt="" loading="lazy" width="640" height="360">
</a>

<!-- in-article figure: this one is content -->
<figure class="post__art">
  <img src="…" alt="A timeline bar whose length varies…" width="640" height="360">
</figure>
```

A screen reader announcing "a clock beside the number 10" before the headline
is noise. Announcing it for the figure inside the article is the point.

## Always set width/height and aspect-ratio

Prevents layout shift as the set loads:

```css
.card__art img { width:100%; height:auto; aspect-ratio:16/9; object-fit:cover; }
```

## Verify the set

```python
import config
missing = [s["slug"] for s in config.SERVICES if s["slug"] not in ART]
extra   = [k for k in ART if k not in {s["slug"] for s in config.SERVICES}]
```

Catches the drawing you forgot and the one whose slug you typo'd, at build time
rather than as a broken image on a client review call.
