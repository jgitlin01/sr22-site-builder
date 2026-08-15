/* Responsive audit — paste into the browser console on the running site.
 *
 *   Usage:  audit()                          // default pages + widths
 *           audit(['/','/services.html'])    // your own page list
 *           audit(null, [375, 768, 1440])    // your own widths
 *
 * Loads each page in an offscreen iframe at each width and reports:
 *   - elements extending past the viewport (ignoring anything inside a
 *     deliberately scrolling/clipping ancestor, so marquees don't false-positive)
 *   - real horizontal document overflow
 *   - broken images
 *   - card grids that failed to fill their container
 *
 * Why a script and not screenshots: preview panes lie. In one environment they
 * returned blank captures after programmatic scrolls, stale paints, and an
 * unpainted right edge that read as a layout gutter which did not exist in the
 * DOM. Measure; do not eyeball.
 */
async function audit(pages, widths) {
  pages = pages || [
    '/', '/services.html', '/faq.html', '/contact.html', '/about.html',
    // add one of each generated page type:
    // '/<geo>/', '/<geo>/<city>/', '/<geo>/<city>/<hood>/', '/blog/', '/blog/<post>/'
  ];
  // 320 catches the smallest phone still in use; 700-1024 is the tablet band
  // that falls between a phone breakpoint and a desktop layout; 1920 catches
  // containers that fail to cap.
  widths = widths || [320, 360, 375, 390, 414, 700, 768, 820, 834, 1024, 1180, 1440, 1920];

  const bad = [];
  for (const w of widths) {
    for (const p of pages) {
      const f = document.createElement('iframe');
      f.style.cssText =
        `position:fixed;left:-9999px;top:0;width:${w}px;height:900px;border:0`;
      f.src = p;
      document.body.appendChild(f);
      await new Promise(r => { f.onload = r; setTimeout(r, 1200); });

      try {
        const d = f.contentDocument, win = f.contentWindow;
        const vw = d.documentElement.clientWidth;

        let over = 0, example = null;
        d.querySelectorAll('main *, header *, footer *').forEach(el => {
          const r = el.getBoundingClientRect();
          if (!r.width) return;
          // skip anything inside a scrolling/clipping ancestor — those are
          // intentionally wider than the viewport (marquees, overflow-auto rows)
          let par = el.parentElement, clipped = false;
          while (par && par !== d.body) {
            const ox = win.getComputedStyle(par).overflowX;
            if (ox === 'auto' || ox === 'scroll' || ox === 'hidden') { clipped = true; break; }
            par = par.parentElement;
          }
          if (!clipped && r.right > vw + 1) {
            over++;
            if (!example) {
              example = el.tagName + '.' + String(el.className || '').slice(0, 30);
            }
          }
        });

        const brokenImg = Array.from(d.images)
          .filter(i => i.complete && i.naturalWidth === 0).length;

        // a grid should fill its container; allow for a max-width cap on wide screens
        let gridShort = false;
        const grid = d.querySelector('[class*="-grid"]');
        if (grid) {
          const cont = grid.parentElement.getBoundingClientRect().width;
          gridShort = grid.getBoundingClientRect().width < cont - 2;
        }

        const hScroll = d.documentElement.scrollWidth > vw + 1;
        if (over || brokenImg || gridShort || hScroll) {
          bad.push({ w, page: p, overflow: over, example, brokenImg, gridShort, hScroll });
        }
      } catch (e) {
        bad.push({ w, page: p, error: String(e).slice(0, 60) });
      }
      f.remove();
    }
  }

  if (!bad.length) {
    return `CLEAN — ${pages.length} pages x ${widths.length} widths = ` +
           `${pages.length * widths.length} combinations, no problems`;
  }
  console.table(bad);
  return bad;
}

/* Sanity helpers for when a screenshot disagrees with the DOM.
 * If elementFromPoint returns real content and the rects are correct, believe
 * them — the capture is wrong, not the layout. */
function whatIsAt(x, y) {
  const el = document.elementFromPoint(x, y);
  return el && {
    el: el.tagName + '.' + String(el.className || '').slice(0, 40),
    text: (el.textContent || '').trim().slice(0, 60),
    opacity: getComputedStyle(el).opacity,
    rect: el.getBoundingClientRect().toJSON()
  };
}

function edges() {
  const r = s => {
    const el = document.querySelector(s);
    return el ? Math.round(el.getBoundingClientRect().right) : null;
  };
  return {
    innerWidth: window.innerWidth,
    clientWidth: document.documentElement.clientWidth,
    visualViewport: window.visualViewport && Math.round(window.visualViewport.width),
    scrollbarGap: window.innerWidth - document.documentElement.clientWidth,
    headerRight: r('header'),
    bodyRight: Math.round(document.body.getBoundingClientRect().right),
    hasHorizontalScroll:
      document.documentElement.scrollWidth > document.documentElement.clientWidth
  };
}

/* Anything still hidden by a scroll-reveal that never fired. Should be []
 * after the page settles; anything listed is content a reader cannot see. */
function stillHidden() {
  return Array.from(document.querySelectorAll('[data-animation]'))
    .filter(el => getComputedStyle(el).opacity === '0')
    .map(el => el.tagName + '.' + String(el.className || '').slice(0, 40));
}
