#!/usr/bin/env python3
"""Pre-deploy gates for a generated location-page fleet.

Usage:
    python validate.py <site-root> [geo-root=florida]

Checks every generated page for:
  1. leftover template variables ($var / {var}) that never got substituted
  2. invalid JSON-LD (one trailing comma silently kills the whole block)
  3. broken root-relative links and missing image assets
  4. missing structural tags (truncated writes)
  5. schema claiming a rating/hours/review with no matching VISIBLE element on the
     page -- a real Google guidelines issue, not just a style nit. Caught this
     manually twice in the same build (special pages that reuse a shared schema
     block but not its paired visible markup) before adding this check.
  6. template leakage -- the previous client's phone/address/domain surviving a
     clone, scanned across CSS and JS as well as HTML. See template-cloning.md;
     on one build the old number lived in a runtime-injected JS widget where no
     HTML grep would ever have found it. Set LEAK_PATTERNS per project.
  7. escaped HTML entities rendering as literal text (&amp;middot;) -- happens
     whenever an entity is written into a source string that later gets escaped
  8. bare landmark elements nested inside <main> -- templates style `header`,
     `footer` etc. directly, so a <header> inside a card gets captured by the
     fixed site-header rule and yanked out of the card
  9. grid tracks using `1fr` without a zero floor, which overflow their
     container when an item has wide min-content (a <select> with long options)
 10. CSS url() references pointing at files that do not exist -- a clone leaves
     the old client's background-image filenames behind, and an HTML-only asset
     check never sees them

Exit code 0 = safe to deploy. Nonzero = number of problems found.

Run this on the WHOLE site (generated pages + hand-authored root pages), not just
the generated fleet -- the visibility-mismatch check specifically targets pages that
share schema with the generator but aren't produced by it.
"""
import glob
import json
import os
import re
import sys

TEMPLATE_VAR = re.compile(r"\$[a-zA-Z_][a-zA-Z0-9_]*")
BRACE_VAR = re.compile(r"\{[a-zA-Z_][a-zA-Z0-9_\[\]\"']*\}")
LDJSON = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
ASSET_REF = re.compile(r'(?:href|src)="(/[^"#?]*)"')
REQUIRED_TAGS = ("</html>", "</body>", "</main>", "</footer>")

# schema key -> substring(s) that must appear somewhere in the visible body if that
# key is present in a LocalBusiness/Organization block. Customize the visible-text
# side to match your template's actual rendered markup (e.g. your rating badge's
# class name or your footer's hours string).
SCHEMA_VISIBILITY_PAIRS = {
    "aggregateRating": ["rating-badge"],              # rating badge class/marker
    "openingHoursSpecification": ["Mon"],             # visible hours string
}

# ---------------------------------------------------------------------------
# SET THIS PER PROJECT when the site was cloned from a previous client's build.
# Include every format of the old phone number, the old street/city/domain/
# email/social handles, the old Google place_id, the GSC verification filename,
# the old niche's vocabulary, and the template vendor's name.
# Empty list = no clone check. See references/template-cloning.md.
LEAK_PATTERNS = [
    # r"oldclientdomain\.com", r"Old Client Name",
    # r"\(239\) 320-2623", r"239-320-2623", r"\+12393202623",
    # r"ChIJ[0-9A-Za-z_-]{20,}", r"google[0-9a-f]{16}\.html",
]

# Files to scan for leaks beyond the HTML. The bug that motivated this lived in
# a JS widget that injected itself at runtime.
LEAK_EXTS = (".html", ".js", ".css", ".txt", ".json", ".xml", ".svg", ".php")

ENTITY_LEAK = re.compile(r"&amp;(?:[a-z]{2,8}|#\d{2,5});")
BARE_LANDMARK = re.compile(r"<(header|footer)[ >]")
MAIN_BLOCK = re.compile(r"<main[^>]*>(.*?)</main>", re.S)
BAD_GRID = re.compile(r"grid-template-columns:[^;]*minmax\(\s*\d+px\s*,\s*1fr\s*\)")
CSS_URL = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = sys.argv[1]
    geo = sys.argv[2] if len(sys.argv) > 2 else "florida"
    os.chdir(root)

    fleet_files = glob.glob(f"{geo}/**/index.html", recursive=True)
    if not fleet_files:
        sys.exit(f"No pages found under {geo}/")

    # Hand-authored root pages (about.html, services.html, blog posts, 404, etc.) --
    # these share LocalBusiness schema with the generated fleet but are edited by
    # hand, which is exactly where the schema/visibility pairing tends to drift.
    root_files = [f for f in glob.glob("*.html")
                  if not f.startswith("google") and "verification" not in f.lower()]

    files = fleet_files + root_files
    problems = 0

    for f in files:
        c = open(f, encoding="utf-8").read()

        body = c.split("<body>", 1)[-1]
        for m in set(TEMPLATE_VAR.findall(body)):
            # $$ is a legitimate escaped dollar (e.g. priceRange "$$")
            if m != "$" and f"{m}{m}" not in body:
                print(f"LEFTOVER VAR  {f}: {m}")
                problems += 1
        for m in set(BRACE_VAR.findall(body)):
            print(f"LEFTOVER BRACE {f}: {m}")
            problems += 1

        for m in set(ENTITY_LEAK.findall(c)):
            print(f"ENTITY LEAK   {f}: {m} rendering as literal text "
                  f"(use literal Unicode in source strings)")
            problems += 1

        mb = MAIN_BLOCK.search(c)
        if mb:
            for tag in set(BARE_LANDMARK.findall(mb.group(1))):
                print(f"BARE LANDMARK {f}: <{tag}> inside <main> -- templates often "
                      f"style this element directly; use a div")
                problems += 1

        blocks = LDJSON.findall(c)
        if not blocks:
            print(f"NO SCHEMA     {f}")
            problems += 1
        for b in blocks:
            try:
                d = json.loads(b)
            except Exception as e:
                print(f"BAD JSON-LD   {f}: {e}")
                problems += 1
                continue
            if str(d.get("@type")).find("LocalBusiness") != -1 or d.get("@type") == "Organization":
                for key, visible_markers in SCHEMA_VISIBILITY_PAIRS.items():
                    if key in d and not any(marker in c for marker in visible_markers):
                        print(f"SCHEMA W/O VISIBLE MATCH  {f}: has '{key}' in schema "
                              f"but none of {visible_markers} found in page body")
                        problems += 1

        # Structural-tag check only applies to the generated fleet -- hand-authored
        # pages may legitimately use a different shell and this would false-positive.
        if f in fleet_files:
            for tag in REQUIRED_TAGS:
                if tag not in c:
                    print(f"MISSING TAG   {f}: {tag}")
                    problems += 1

    if LEAK_PATTERNS:
        scanned = 0
        for dirpath, dirnames, filenames in os.walk("."):
            dirnames[:] = [d for d in dirnames
                           if d not in ("__pycache__", ".git", "node_modules")]
            for fn in filenames:
                if not fn.endswith(LEAK_EXTS):
                    continue
                path = os.path.join(dirpath, fn)
                try:
                    text = open(path, encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                scanned += 1
                for pat in LEAK_PATTERNS:
                    if re.search(pat, text, re.I):
                        print(f"TEMPLATE LEAK {path}: matches /{pat}/")
                        problems += 1
        print(f"(leak scan: {scanned} text files)")

    for css in glob.glob("assets/css/*.css") + glob.glob("css/*.css"):
        text = open(css, encoding="utf-8", errors="ignore").read()
        for m in set(BAD_GRID.findall(text)):
            print(f"GRID OVERFLOW {css}: {m.strip()} -- `1fr` has a min-content "
                  f"floor; use minmax(min(Npx,100%), 1fr)")
            problems += 1
        # url() targets, resolved relative to the stylesheet. Skips data: and
        # remote URLs. Catches the previous client's photo filenames surviving
        # a clone inside background-image rules, which an HTML-only asset scan
        # cannot see -- found 27 of them on a real build.
        for ref in set(CSS_URL.findall(text)):
            if ref.startswith(("data:", "http:", "https:", "//", "#")):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(css), ref.split("?")[0]))
            if not os.path.isfile(target):
                print(f"DEAD CSS URL  {css}: url({ref}) -> no such file")
                problems += 1

    missing = set()
    for f in files:
        for ref in ASSET_REF.findall(open(f, encoding="utf-8").read()):
            p = ref.lstrip("/")
            cand = p if os.path.isfile(p) else os.path.join(p, "index.html")
            if not os.path.isfile(cand):
                missing.add(ref)
    for ref in sorted(missing):
        print(f"BROKEN REF    {ref}")
        problems += 1

    print(f"\nchecked {len(files)} pages — {problems} problem(s)")
    if problems:
        print("Fix these before uploading.")
    sys.exit(min(problems, 250))


if __name__ == "__main__":
    main()
