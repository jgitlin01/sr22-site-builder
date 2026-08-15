#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pre-deploy gates for sr22carinsurancenashvilletn.com.

    python3 validate_site.py

Runs on top of the generic location-page validator. What it adds:

1. TEMPLATE LEAKAGE. This site was cloned from a turf installer's build. Their
   phone number, street address, Google place_id, review count, and Search
   Console verification file must not survive the clone. A fabricated
   aggregateRating on a YMYL insurance page is a manual-action risk, not a
   cosmetic bug, so any hit here is a hard failure.

2. SCHEMA/CONTENT AGREEMENT. Structured data must describe what a visitor can
   actually see. Ratings, hours, and addresses may only appear in JSON-LD if
   the same value is rendered on the page.

3. PLACEHOLDER AUDIT. Bracket tokens are expected until the agency is named,
   but only the ones declared in config.KNOWN_PLACEHOLDERS. An undeclared
   bracket token means the generator failed to substitute something.

Exit code is non-zero if any hard failure is found.
"""

import json
import os
import re
import sys

import config as C

ROOT = os.path.dirname(os.path.abspath(__file__))

# Strings that prove the turf template leaked through.
LEAKS = [
    r"turfinstallationgurus", r"Turf Installation Gurus", r"239-320-2623",
    r"\(239\) 320-2623", r"\+12393202623", r"Hendry St", r"Fort Myers",
    r"ChIJvdwFNYpB24gRHOC8Sg5xOVo", r"fortmyersfl@", r"TurfGurus",
    r"google99ce5de2cc93a18f", r"\bartificial turf\b", r"putting green",
    r"Mowix",
]

# Schema properties that require a matching visible element on the page.
NEEDS_VISIBLE = {
    "aggregateRating": None,          # never allowed without real reviews
    "openingHoursSpecification": "hours",
    "priceRange": None,
}


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in ("assets", "__pycache__", "_contact_sheets")]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def text_assets():
    """CSS/JS/text carried over from the template. Scanning only the HTML is
    not enough -- the previous client's phone number survived the clone inside
    a JS widget that injects itself at runtime, where no HTML grep would see
    it."""
    exts = (".js", ".css", ".txt", ".json", ".xml", ".php", ".svg")
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in ("__pycache__", "_contact_sheets", ".git")]
        for fn in filenames:
            if fn.endswith(exts):
                yield os.path.join(dirpath, fn)


def rel(p):
    return os.path.relpath(p, ROOT)


def main():
    hard, soft = [], []
    pages = list(html_files())
    internal_targets = set()
    link_uses = []

    # 1 -- template leakage, across every text file in the tree
    for path in list(pages) + list(text_assets()):
        try:
            src = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for pat in LEAKS:
            if re.search(pat, src, re.I):
                hard.append("%s: turf template leak matching /%s/"
                            % (rel(path), pat))

    for path in pages:
        src = open(path, encoding="utf-8").read()
        r = rel(path)

        # 2 -- JSON-LD parses, and does not overclaim
        for block in re.findall(
                r'<script type="application/ld\+json">(.*?)</script>',
                src, re.S):
            try:
                obj = json.loads(block)
            except json.JSONDecodeError as e:
                hard.append("%s: invalid JSON-LD (%s)" % (r, e))
                continue
            flat = json.dumps(obj)
            for prop, visible_key in NEEDS_VISIBLE.items():
                if '"%s"' % prop not in flat:
                    continue
                if visible_key is None:
                    hard.append("%s: schema claims %s with nothing to back it"
                                % (r, prop))
                else:
                    val = C.SITE.get(visible_key, "")
                    body = src.split("</head>", 1)[-1]
                    if val and val not in body:
                        hard.append("%s: schema has %s but the page never "
                                    "shows it" % (r, prop))

        # 3 -- undeclared bracket tokens
        # No upper bound on token length: a long token that the regex silently
        # skipped would let an unfilled field ship looking validated.
        for tok in set(re.findall(r"\[[A-Za-z][^\[\]]{2,}?\]", src)):
            if tok not in C.KNOWN_PLACEHOLDERS and "REVIEW REQUIRED" not in tok:
                hard.append("%s: undeclared placeholder %s" % (r, tok))

        # collect links for the internal-link check
        for href in re.findall(r'href="(/[^"#?]*)"', src):
            link_uses.append((r, href))
        for src_attr in re.findall(r'(?:src|background-image:url\()[\'"]?(/[^\'")]+)', src):
            link_uses.append((r, src_attr))

        # every page must be structurally complete
        for tag in ("</html>", "</footer>", "</main>", "<h1"):
            if tag not in src:
                hard.append("%s: missing %s" % (r, tag))

    # build the set of things that exist
    for path in pages:
        p = "/" + rel(path).replace(os.sep, "/")
        internal_targets.add(p)
        if p.endswith("/index.html"):
            internal_targets.add(p[:-len("index.html")])
    for dirpath, _, filenames in os.walk(os.path.join(ROOT, "assets")):
        for fn in filenames:
            internal_targets.add(
                "/" + os.path.relpath(os.path.join(dirpath, fn), ROOT)
                .replace(os.sep, "/"))

    for page, href in link_uses:
        target = href.split("?")[0]
        if target in internal_targets:
            continue
        if target.rstrip("/") + "/index.html" in internal_targets:
            continue
        hard.append("%s: broken internal link -> %s" % (page, target))

    # The quote form is the whole conversion path, and an unwired form action
    # is invisible on screen in a way an unfilled phone number is not. This is
    # the one placeholder that blocks rather than warns.
    ep = C.SITE["form_endpoint"]
    if ep.startswith("["):
        hard.append("quote form still posts to %s -- point it at the real "
                    "lead destination or the preview stub" % ep)
    elif ep == "/quote-not-connected.html":
        soft.append("QUOTE FORM IS NOT COLLECTING LEADS. It posts to the "
                    "preview stub, which tells the visitor nothing was "
                    "submitted and gives them the phone number. Point "
                    "SITE['form_endpoint'] at the real destination before "
                    "this site takes real traffic.")

    if C.PREVIEW:
        soft.append("PREVIEW MODE: every page carries robots noindex and "
                    "robots.txt disallows all crawlers. Set PREVIEW = False "
                    "in config.py at launch.")

    # sitemap sanity
    sm = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(sm):
        hard.append("sitemap.xml missing")
    else:
        locs = re.findall(r"<loc>(.*?)</loc>", open(sm, encoding="utf-8").read())
        if len(locs) != len(set(locs)):
            hard.append("sitemap.xml has duplicate <loc> entries")
        for loc in locs:
            p = loc.replace(C.SITE["base_url"], "") or "/"
            if p not in internal_targets and p + "index.html" not in internal_targets:
                hard.append("sitemap.xml lists a URL with no page: %s" % loc)

    # informational: how much is still placeholder
    ph = sum(1 for p in pages
             if any(t in open(p, encoding="utf-8").read()
                    for t in C.KNOWN_PLACEHOLDERS))
    soft.append("%d of %d pages still contain business placeholders "
                "(expected until the agency is named)" % (ph, len(pages)))
    missing = [c["slug"] for c in C.CITIES
               if not os.path.exists(os.path.join(
                   ROOT, "assets", "images", "places", c["slug"] + ".jpg"))]
    missing += [n["slug"] for n in C.NEIGHBORHOODS
                if not os.path.exists(os.path.join(
                    ROOT, "assets", "images", "places", n["slug"] + ".jpg"))]
    if missing:
        soft.append("no location-specific photo (falls back to the Nashville "
                    "photo, credited): " + ", ".join(missing))

    print("checked %d pages" % len(pages))
    for s in soft:
        print("  note: " + s)
    if hard:
        print("\n%d FAILURE(S):" % len(hard))
        for h in sorted(set(hard)):
            print("  " + h)
        return 1
    print("\nPASS - no failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
