#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static site generator for sr22carinsurancenashvilletn.com.

Data lives in config.py; markup lives here. Nothing is hand-written into the
output directory -- re-run this file after any content change.

    python3 generate.py

Markup reuses the class names from the Turf Installation Gurus build so the
existing CSS applies unchanged. All internal links are root-absolute, so no
per-depth path juggling is needed.

string.Template ($var) is used rather than f-strings because the JSON-LD
blocks are full of braces.
"""

import html
import json
import os
import re
from string import Template

import config as C
from make_blog_art import ART as BLOG_ART, DIAGRAM as BLOG_DIAGRAM
from make_service_art import SERVICES as SERVICE_ART

def slugify_state(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", str(s).lower())).strip("-")


ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = C.SITE["base_url"]

# URL segments for the location fleet. Structural, so they live here rather
# than in COPY: /GEO/ is the hub, /GEO/HUB/ is the primary city that owns the
# neighbourhood pages.
GEO = getattr(C, "GEO_ROOT", None) or slugify_state(C.SITE.get("region", "area"))
HUB = getattr(C, "HUB_CITY_SLUG", None) or (C.CITIES[0]["slug"] if getattr(C, "CITIES", None) else "city")
HUB_NAME = getattr(C, "HUB_CITY_NAME", None) or (C.CITIES[0]["name"] if getattr(C, "CITIES", None) else "City")

# Cache-bust the override stylesheet on content change. Without this, editing
# sr22.css and re-running the generator leaves browsers (and CDN edges) on the
# old file at the same ?v= string, which looks exactly like a CSS rule that
# "isn't applying".
# While PREVIEW is on, every page tells crawlers to stay away. Removing this
# is a deliberate launch step, not something to leave to chance.
ROBOTS_META = ('    <meta name="robots" content="noindex, nofollow">'
               if C.PREVIEW else
               '    <meta name="robots" content="index, follow, max-image-preview:large">')

_css = os.path.join(ROOT, "assets", "css", "sr22.css")
CSS_VER = (str(int(os.path.getmtime(_css))) if os.path.exists(_css) else "1")


# ----------------------------------------------------------------- helpers --

def esc(s):
    # config.py keeps prose ASCII-safe; render the typographic characters here
    # so "--" does not reach the page as two hyphens.
    out = html.escape(str(s), quote=False)
    return (out.replace(" -- ", " — ")
               .replace("'", "’"))


def write(relpath, content):
    path = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return relpath


def jsonld(obj):
    # Keep schema text identical to what a visitor reads, including the dash.
    body = json.dumps(obj, ensure_ascii=False).replace(" -- ", " — ")
    return '<script type="application/ld+json">%s</script>' % body


# ---------------------------------------------------------------- copy --
# Niche-neutral defaults. config.COPY overrides any key; everything the client
# actually reads lives in config, so this generator is pure structure.
# {niche} {city} {region} {company} {phone} are always available.
DEFAULT_COPY = {
    "home_title":        "{niche} in {city}, {region} | {company}",
    "home_desc":         "{niche} in {city}, {region}. Call {phone} for a free quote.",
    "home_eyebrow":      "{city} &bull; {region}",
    "home_h1":           "{niche} in {city}, {region}",
    "home_sub":          "Local {niche} for {city} and the surrounding area.",
    "home_quick":        "We provide {niche} across {city} and the surrounding area. "
                         "Call <a href=\"tel:{phone_href}\">{phone}</a> for a free quote.",
    "hero_cta":          "Get My Free Quote",
    "hero_license":      "Serving {city} and the surrounding area",
    "answer_h2":         "What is {niche}?",
    "answer_lede":       "",
    "answer_intro":      "Here is what applies:",
    "violations_h2":     "Why you may need {niche}",
    "violations_lede":   "",
    "violations_help":   "Not sure which applies to you? Call us at "
                         "<a href=\"tel:{phone_href}\">{phone}</a> and we will walk "
                         "through it with you at no charge.",
    "services_h2":       "Our services",
    "cost_h2":           "How much does {niche} cost in {city}?",
    "steps_h2":          "How it works",
    "faq_h2":            "Frequently Asked Questions",
    "form_h2":           "Get a free quote",
    "form_sub":          "Tell us what you need and we will get straight back to you.",
    "form_foot":         "Or call <a href=\"tel:{phone_href}\">{phone}</a>. No obligation.",
    "author_h2":         "Reviewed by {agent_name}",
    "author_foot":       "Page last updated {updated}.",
    "cta_band_h2":       "Ready to get started?",
    "cta_band_sub":      "Most people get a quote in under 10 minutes.",
    "hub_title":         "{niche} service areas | {region}",
    "hub_desc":          "Cities and neighbourhoods where we provide {niche}.",
    "hub_h1":            "{niche} across {region}",
    "hub_sub":           "Every page below carries that area's own local detail.",
    "city_title":        "{niche} in {name}, {region}",
    "city_desc":         "{niche} for {name}, {region}. Call {phone}.",
    "city_h1":           "{niche} in {name}, {region}",
    "city_glance_h2":    "{name} at a glance",
    "city_diff_h2":      "What is different about {niche} in {name}",
    "hood_title":        "{niche} in {name}, {hub} {region}",
    "hood_desc":         "{niche} for {name}. Call {phone}.",
    "hood_h1":           "{niche} in {name}",
    "services_idx_title":"{niche} services in {city}, {region}",
    "services_idx_desc": "Everything we handle.",
    "services_idx_h1":   "Our services",
    "about_title":       "About {company} | {niche} in {city}",
    "about_desc":        "About {company}.",
    "contact_title":     "Contact | {niche} quotes in {city}, {region}",
    "contact_desc":      "Get a quote for {niche} in {city}. Call {phone}.",
    "contact_h1":        "Get your quote",
    "faq_title":         "{niche} FAQ",
    "faq_desc":          "Answers to the questions people actually ask.",
    "faq_h1":            "Questions, answered",
    "blog_title":        "{niche} guides",
    "blog_desc":         "Plain explanations of how this works locally.",
    "blog_h1":           "{niche} guides",
    "blog_sub":          "Written for {region}, and sourced.",
    "cta_short":         "Free Quote",
    "footer_h":          "{niche} in {city}, {region}",
    "footer_p":          "",
    "footer_services_h": "Services",
    "schema_description":"{company} provides {niche} in {city}, {region} and the surrounding area.",
    "hub_eyebrow":       "Service Areas",
    "hood_eyebrow":      "{hub}",
    "hood_h1":           "{niche} in {name}",
    "contact_eyebrow":   "Contact",
    "contact_sub":       "Tell us what you need and we will get straight back to you.",
    "faq_eyebrow":       "FAQ",
    "faq_sub":           "",
    "blog_eyebrow":      "Guides",
    "services_idx_eyebrow": "Services",
    "services_idx_sub":  "",
    "about_eyebrow":     "About",
    "about_h1":          "About {company}",
    "about_sub":         "",
    "llms_summary":      "{company} provides {niche} in {city}, {region}. "
                         "Office: {street}, {city}, {region} {postal}. Phone: {phone}.",
}


def copy(key, **fmt):
    """Page copy, from config.COPY with a niche-neutral fallback.

    Every string a reader sees lives in config so the generator stays pure
    structure and works for any niche. Unknown placeholders are left alone
    rather than raising, so a half-filled COPY still builds.
    """
    tpl = getattr(C, "COPY", {}).get(key, DEFAULT_COPY.get(key, ""))
    base = {
        "niche": C.SITE.get("niche", "our services"),
        "company": C.SITE.get("name", ""),
        "city": C.SITE.get("city", ""),
        "region": C.SITE.get("region", ""),
        "phone": C.SITE.get("phone_display", ""),
        "phone_href": C.SITE.get("phone_href", ""),
        "street": C.SITE.get("street", ""),
        "postal": C.SITE.get("postal", ""),
        "agent_name": C.SITE.get("agent_name", ""),
        "license": C.SITE.get("license", ""),
        "updated": C.SITE.get("last_updated", ""),
        "hub": HUB_NAME,
    }
    base.update(fmt)
    try:
        return tpl.format(**base)
    except (KeyError, IndexError):
        return tpl


def has(name):
    """True when config declares non-empty data for an optional section.

    Lets the generator run against a fresh scaffold whose research is not in
    yet: sections with no data render as nothing rather than crashing, and
    appear as the config fills up.
    """
    return bool(getattr(C, name, None))


def source_link(key):
    label, url = C.SOURCES[key]
    if not url:
        return esc(label)
    return ('<a href="%s" target="_blank" rel="noopener nofollow">%s</a>'
            % (url, esc(label)))


def photo_for(slug):
    """Return (src, credit) for a location, or (None, None) if QA dropped it.

    places_manifest.json is written by fetch_photos.py; `approved` is set by
    hand during the contact-sheet review. Only approved photos ship. Missing
    entries are a normal, expected state -- those pages fall back to the
    default hero rather than showing an image of the wrong place.
    """
    return PHOTOS.get(slug, (None, None))


PHOTOS = {}
RAW_CREDITS = {}
_manifest = os.path.join(ROOT, "places_manifest.json")
if os.path.exists(_manifest):
    with open(_manifest, encoding="utf-8") as fh:
        for slug, rec in json.load(fh).items():
            if rec.get("approved"):
                RAW_CREDITS[slug] = rec.get("credit", "Google Maps contributor")
            if rec.get("approved") and rec.get("file"):
                # Credit the contributor (required by Google's terms) and name
                # what is actually pictured -- several of these are landmarks,
                # not generic streetscapes, and the caption should say so.
                credit = rec.get("credit", "Google Maps contributor")
                # Places sometimes returns a clipped display name ("Downtown")
                # and sometimes a fuller one than we asked for; take whichever
                # names the subject more completely.
                subject = max(rec.get("matched_name", ""),
                              rec.get("query", "").split(",")[0],
                              key=len)
                PHOTOS[slug] = ("/" + rec["file"].lstrip("/"),
                                ("%s. Photo: %s via Google Maps" % (subject, credit))
                                if subject else
                                ("Photo: %s via Google Maps" % credit))


# ------------------------------------------------------------------- chrome --

def nav_services():
    out = ['<li><a class="dropdown-item" href="/services.html">'
           '<i class="fa-solid fa-list"></i> All Services</a></li>']
    for s in C.SERVICES:
        out.append('<li><a class="dropdown-item" href="/%s.html">'
                   '<i class="fa-solid %s"></i> %s</a></li>'
                   % (s["slug"], s["icon"], esc(s["nav"])))
    return "\n".join(out)


def nav_areas():
    out = ['<li><a class="dropdown-item" href="/%s/">' % GEO +
           '<i class="fa-solid fa-list"></i> All Service Areas</a></li>']
    for c in C.CITIES:
        out.append('<li><a class="dropdown-item" href="/%s/%s/">'
                   '<i class="fa-solid fa-location-dot"></i> %s</a></li>'
                   % (GEO, c["slug"], esc(c["name"])))
    return "\n".join(out)


HEADER = Template("""    <header>
        <div class="header-container">
            <nav class="navbar navbar-expand-xl">
                <div class="navbar-container">
                    <div class="navbar-brand-container">
                        <div class="image-container navbar-logo-container">
                            <a class="navbar-brand fw-bold" href="/index.html">
                                <img src="/assets/images/logo-light.svg" alt="$name" class="img-fluid">
                            </a>
                        </div>
                        <div class="navbar-logo-corner-box"></div>
                        <div class="navbar-logo-corner-box"></div>
                    </div>
                    <div class="nav-link-container">
                        <div class="navbar-link-corner-box"></div>
                        <div class="navbar-action-container">
                            <div class="collapse navbar-collapse" id="navbarNav">
                                <ul class="navbar-nav">
                                    <li class="nav-item"><a class="nav-link" href="/index.html">Home</a></li>
                                    <li class="nav-item"><a class="nav-link" href="/about.html">About</a></li>
                                    <li class="nav-item dropdown">
                                        <a class="nav-link dropdown-toggle" href="/services.html" role="button" data-bs-toggle="dropdown" aria-expanded="false">Services</a>
                                        <ul class="dropdown-menu" style="max-height:64vh;overflow-y:auto">
$nav_services
                                        </ul>
                                    </li>
                                    <li class="nav-item dropdown">
                                        <a class="nav-link dropdown-toggle" href="/$geo/" role="button" data-bs-toggle="dropdown" aria-expanded="false">Service Areas</a>
                                        <ul class="dropdown-menu" style="max-height:64vh;overflow-y:auto">
$nav_areas
                                        </ul>
                                    </li>
                                    <li class="nav-item"><a class="nav-link" href="/blog/">Blog</a></li>
                                    <li class="nav-item"><a class="nav-link" href="/faq.html">FAQ</a></li>
                                    <li class="nav-item"><a class="nav-link" href="/contact.html">Contact</a></li>
                                </ul>
                            </div>
                            <button class="nav-btn" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                                <i class="fa-solid fa-bars"></i>
                            </button>
                            <div class="navbar-cta-container">
                                <a href="tel:$phone_href" class="tig-nav-phone">
                                    <i class="fa-solid fa-phone"></i>
                                    <span>$phone</span>
                                </a>
                                <a href="/contact.html" class="btn btn-accent">
                                    <span>$cta_short</span>
                                    <i class="fa-solid fa-circle-arrow-right"></i>
                                </a>
                            </div>
                        </div>
                        <div class="navbar-link-corner-box"></div>
                    </div>
                </div>
            </nav>
        </div>
    </header>

    <aside>
        <div class="navbar-popup" id="navbarPopup">
            <ul class="navbar-popup-menu">
                <li><a href="/index.html">Home</a></li>
                <li><a href="/about.html">About</a></li>
                <li><a href="/services.html">Services</a></li>
                <li><a href="/$geo/">Service Areas</a></li>
                <li><a href="/blog/">Blog</a></li>
                <li><a href="/faq.html">FAQ</a></li>
                <li><a href="/contact.html">Contact</a></li>
            </ul>
        </div>
    </aside>
""")


FOOTER = Template("""    <footer>
        <div class="footer-container">
            <div class="footer-bg">
                <div class="hero-container">
                    <div class="footer-wrapper">
                        <div class="footer__intro-container">
                            <div class="footer-intro">
                                <div class="image-container footer-logo">
                                    <img src="/assets/images/logo-light.svg" alt="$name">
                                </div>
                                <h4 class="secondary-color">$footer_h</h4>
                                <p class="secondary-color">$footer_p</p>
                                <p class="secondary-color" style="font-size:.85rem;opacity:.85">$compliance</p>
                            </div>
                            <div class="footer-link footer-service">
                                <h4 class="secondary-color">$footer_services_h</h4>
                                <ul class="footer-list">
$footer_services
                                </ul>
                            </div>
                            <div class="footer-link footer-company">
                                <h4 class="secondary-color">Company</h4>
                                <ul class="footer-list">
                                    <li><a href="/about.html">About Us</a></li>
                                    <li><a href="/services.html">All Services</a></li>
                                    <li><a href="/blog/">Blog</a></li>
                                    <li><a href="/faq.html">FAQ</a></li>
                                    <li><a href="/contact.html">Contact Us</a></li>
                                    <li><a href="/$geo/">Service Areas</a></li>
                                </ul>
                                $footer_sources
                            </div>
                            <div class="footer-link footer-cta">
                                <h4 class="secondary-color">Get In Touch</h4>
                                <ul class="footer-list zero-icon">
                                    <li><a href="tel:$phone_href">$phone</a></li>
                                    <li><a href="mailto:$email">$email</a></li>
                                    <li>$street, $city, $region $postal</li>
                                    <li>$hours</li>
                                </ul>
                            </div>
                        </div>
                        <div class="footer-copyright__container">
                            <p class="copyright-text">&copy; 2026 $name. All Rights Reserved. Page last updated $updated.</p>
                            <div class="footer-legallink__container">
                                <a href="/privacy.html" class="footer-legalink-text">Privacy Policy</a>
                                <a href="/terms.html" class="footer-legalink-text">Terms &amp; Conditions</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </footer>
""")


SHELL = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$title</title>
    <meta name="description" content="$desc">
    <link rel="canonical" href="$canonical">
$robots
    <meta property="og:title" content="$title">
    <meta property="og:description" content="$desc">
    <meta property="og:url" content="$canonical">
    <meta property="og:type" content="website">
    <link rel="stylesheet" href="/assets/css/main.css?v=30">
    <link rel="stylesheet" href="/assets/css/responsive.css?v=3">
    <link rel="stylesheet" href="/assets/css/sr22.css?v=$cssver">
    <link rel="shortcut icon" href="/assets/images/favicon.svg">
    <script>document.documentElement.classList.add('js')</script>
$schema
</head>
<body>
$header
    <main>
$body
    </main>
$footer
    <script src="/assets/js/vendor/bootstrap.bundle.min.js"></script>
    <script src="/assets/js/vendor/gsap.min.js"></script>
    <script src="/assets/js/vendor/ScrollTrigger.min.js"></script>
    <script src="/assets/js/vendor/swiper-bundle.min.js"></script>
    <script src="/assets/js/script.js"></script>
    <script src="/assets/js/gsap-script.js"></script>
    <script src="/assets/js/swiper-script.js"></script>
    <script src="/assets/js/tig-sticky-header.js?v=2"></script>
    <script src="/assets/js/tig-corner-call.js?v=2"></script>
    <script src="/assets/js/tig-scrolltop.js?v=2"></script>
    <script src="/assets/js/sr22-reveal-failsafe.js?v=1"></script>
</body>
</html>
""")


def page(title, desc, canonical, body, schema_blocks):
    s = C.SITE
    footer_services = "\n".join(
        '                                    <li><a href="/%s.html">%s</a></li>'
        % (x["slug"], esc(x["nav"])) for x in C.SERVICES[:8])
    return SHELL.substitute(
        title=esc(title), desc=esc(desc), canonical=canonical, cssver=CSS_VER,
        robots=ROBOTS_META,
        schema="\n".join(schema_blocks),
        header=HEADER.substitute(name=esc(s["name"]), phone=esc(s["phone_display"]),
                                 phone_href=s["phone_href"],
                                 nav_services=nav_services(), nav_areas=nav_areas(), geo=GEO,
                                 cta_short=copy("cta_short")),
        body=body,
        footer=FOOTER.substitute(
            name=esc(s["name"]), phone=esc(s["phone_display"]),
            phone_href=s["phone_href"], email=esc(s["email"]),
            street=esc(s["street"]), city=esc(s["city"]), region=s["region"],
            postal=esc(s["postal"]), hours=esc(s["hours"]),
            updated=s["last_updated"], compliance=esc(C.COMPLIANCE_NOTE),
            footer_services=footer_services,
            src_fr=C.SOURCES["fr"][1], src_reinstate=C.SOURCES["reinstate"][1],
            src_eservices=C.SOURCES["eservices"][1], geo=GEO,
            footer_h=copy("footer_h"), footer_p=copy("footer_p"),
            footer_services_h=copy("footer_services_h"),
            footer_sources=footer_sources()),
    )


# ------------------------------------------------------------------- schema --

def schema_agency():
    """InsuranceAgency. Address/geo/rating/hours are emitted ONLY when real
    values exist -- schema must match visible page content, and a fabricated
    aggregateRating on a YMYL insurance site is a manual-action risk."""
    s = C.SITE
    obj = {
        "@context": "https://schema.org",
        "@type": "InsuranceAgency",
        "@id": BASE + "/#agency",
        "name": s["name"],
        "url": BASE + "/",
        "description": copy("schema_description"),
        "areaServed": [{"@type": "City", "name": c["name"] + ", TN"}
                       for c in C.CITIES],
        "knowsAbout": getattr(C, "KNOWS_ABOUT", []),
    }
    if not s["phone_display"].startswith("["):
        obj["telephone"] = s["phone_href"]
    if not s["street"].startswith("["):
        obj["address"] = {"@type": "PostalAddress",
                          "streetAddress": s["street"],
                          "addressLocality": s["city"],
                          "addressRegion": s["region"],
                          "postalCode": s["postal"],
                          "addressCountry": "US"}
    if s["geo"]:
        obj["geo"] = dict({"@type": "GeoCoordinates"}, **s["geo"])
    if s["same_as"]:
        obj["sameAs"] = s["same_as"]
    return jsonld(obj)


def schema_webpage(url, name, desc):
    return jsonld({"@context": "https://schema.org", "@type": "WebPage",
                   "@id": url + "#webpage", "url": url, "name": name,
                   "description": desc, "inLanguage": "en-US",
                   "isPartOf": {"@id": BASE + "/#website"},
                   "about": {"@id": BASE + "/#agency"},
                   "dateModified": C.SITE["last_updated"]})


def schema_website():
    return jsonld({"@context": "https://schema.org", "@type": "WebSite",
                   "@id": BASE + "/#website", "url": BASE + "/",
                   "name": C.SITE["name"], "inLanguage": "en-US",
                   "publisher": {"@id": BASE + "/#agency"}})


def schema_breadcrumb(items):
    return jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList",
                   "itemListElement": [
                       {"@type": "ListItem", "position": i + 1,
                        "name": n, "item": u}
                       for i, (n, u) in enumerate(items)]})


def schema_faq(pairs):
    return jsonld({"@context": "https://schema.org", "@type": "FAQPage",
                   "mainEntity": [
                       {"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in pairs]})


def schema_service(svc, area="Nashville, TN"):
    obj = {"@context": "https://schema.org", "@type": "Service",
           "name": svc["h1"], "serviceType": svc["nav"],
           "description": svc["summary"],
           "provider": {"@id": BASE + "/#agency"},
           "areaServed": {"@type": "City", "name": area},
           "url": "%s/%s.html" % (BASE, svc["slug"])}
    art = service_art(svc["slug"])[0]
    if art:
        obj["image"] = BASE + art
    return jsonld(obj)


# ---------------------------------------------------------------- fragments --

def hero_form_card():
    """The quote card that sits in the top-right of the homepage hero, the
    same slot the turf build used. Above the fold, so the primary conversion
    path is visible without scrolling."""
    return """                <div class="tig-hero__form-card" data-animation="fade-left">
                    <h3>%s</h3>
                    <form class="tig-cta__form" action="%s" method="post">
                        <input type="hidden" name="page_context" value="hero">
                        <div class="tig-cta__row">
                            <input type="text" name="first_name" placeholder="First Name*" required autocomplete="given-name">
                            <input type="text" name="last_name" placeholder="Last Name*" required autocomplete="family-name">
                        </div>
                        <div class="tig-cta__row">
                            <input type="tel" name="phone" placeholder="Phone*" required autocomplete="tel">
                            <input type="text" name="zip" placeholder="ZIP Code*" required inputmode="numeric" autocomplete="postal-code">
                        </div>
                        <input type="email" name="email" placeholder="Email" autocomplete="email">
%s                        <button type="submit" class="btn btn-accent tig-cta__submit">
                            <span>Get My Free Quote</span>
                            <i class="fa-solid fa-circle-arrow-right"></i>
                        </button>
                        <p class="tig-hero__form-note">No obligation, no credit card. Most quotes take under 10 minutes.</p>
                    </form>
                </div>
""" % (copy("cta_short"), C.SITE["form_endpoint"], form_selects("tig-select", labelled=False))


def service_marquee_section():
    """Scrolling service strip under the homepage hero, same as turf's."""
    if not has("SERVICES"):
        return ""
    links = "".join(
        '<a href="/%s.html"><i class="fa-solid %s"></i> %s</a>'
        % (s["slug"], s["icon"], esc(s["nav"])) for s in C.SERVICES)
    # The link set is emitted twice so the infinite scroll has no visible seam.
    return """        <div class="tig-marquee" aria-label="SR-22 services">
            <div class="tig-marquee__track">%s%s</div>
        </div>
""" % (links, links)


def hero(eyebrow, h1, sub, crumbs, photo=None, inner=True, aside=""):
    bg = ""
    credit = ""
    if photo and photo[0]:
        bg = ' style="background-image:url(\'%s\')"' % photo[0]
        if photo[1]:
            credit = ('<p class="sr22-photo-credit">%s</p>' % esc(photo[1]))
    crumb_html = ""
    if crumbs:
        parts = []
        for name, url in crumbs[:-1]:
            parts.append('<a href="%s">%s</a><span class="divider">/</span>'
                         % (url, esc(name)))
        parts.append('<a href="#" class="current">%s</a>' % esc(crumbs[-1][0]))
        crumb_html = ('<div class="banner-inner__breadcrumb-wrapper">'
                      '<div class="banner-inner-corner-box left-box"></div>'
                      '<nav class="breadcrumb">%s</nav>'
                      '<div class="banner-inner-corner-box right-box"></div>'
                      '</div>' % "".join(parts))
    # With no aside the grid collapses to a single full-width column; with one
    # it splits like the turf homepage (text left, quote card top-right).
    grid_mod = "" if aside else " tig-hero__grid--single"
    return """        <section class="tig-hero%s">
            <div class="tig-hero__bg"%s></div>
            <div class="tig-hero__overlay"></div>
            <div class="tig-hero__content tig-hero__grid%s">
                <div class="tig-hero__text" data-animation="fade-right">
                    <span class="tig-hero__eyebrow">%s</span>
                    <h1>%s</h1>
                    <p>%s</p>
                    <div class="tig-hero__cta">
                        <a href="/contact.html" class="btn btn-accent">
                            <span>%s</span>
                            <i class="fa-solid fa-circle-arrow-right"></i>
                        </a>
                        <a href="tel:%s" class="tig-hero__phone tig-phone-flash">
                            <i class="fa-solid fa-phone"></i>
                            <span>%s</span>
                        </a>
                    </div>
                    <p class="sr22-hero__license">%s</p>
                    %s
                </div>
                %s
            </div>
            %s
        </section>
""" % (" tig-hero--inner" if inner else "", bg, grid_mod, eyebrow, h1, sub,
       copy("hero_cta"),
       C.SITE["phone_href"], esc(C.SITE["phone_display"]),
       copy("hero_license"), credit,
       aside if aside else crumb_html,
       crumb_html if aside else "")


def quick_answer(text):
    return """        <section class="section">
            <div class="hero-container">
                <div class="tig-tldr" data-animation="fade-up">
                    <span class="tig-tldr__label"><i class="fa-solid fa-bolt"></i> Quick Answer</span>
                    <p>%s</p>
                </div>
            </div>
        </section>
""" % text


def answer_block():
    """The block AI assistants lift verbatim. Self-contained and sourced."""
    if not has("TN_FACTS"):
        return ""
    facts = "\n".join(
        '                        <li><strong>%s</strong>%s</li>'
        % (esc(label), esc(claim))
        for label, claim, _ in C.TN_FACTS)
    m = C.TN_MINIMUMS
    return """        <section class="section sr22-answer">
            <div class="hero-container">
                <h2>What Is SR-22 Insurance in Tennessee?</h2>
                <p class="sr22-lede">An SR-22 is not an insurance policy. It is a certificate of financial responsibility that your insurance company files electronically with the Tennessee Department of Safety and Homeland Security to prove you carry at least the state’s minimum liability coverage. Tennessee requires this filing from drivers whose licenses were suspended or revoked for certain violations.</p>
                <p>Here is what Tennessee specifically requires:</p>
                <ul class="sr22-facts" data-animation="fade-up">
%s
                </ul>
                <p><strong>Minimum coverage required:</strong> Tennessee’s minimum liability limits are %s — %s bodily injury per person, %s bodily injury per accident, and %s property damage per accident (%s).</p>
                <p class="sr22-source">Source: %s. See also %s.</p>
            </div>
        </section>
""" % (facts, m["shorthand"], m["bi_person"], m["bi_accident"], m["pd"],
       esc(m["cite"]), source_link("fr"), source_link("reinstate"))


def violations_block():
    """The department's fifteen triggers, grouped so a reader can find
    themselves in it. Wording of each item is theirs; the four categories are
    ours, and the page says so rather than implying the state groups them."""
    if not has("VIOLATION_GROUPS"):
        return ""
    groups = []
    for g in C.VIOLATION_GROUPS:
        items = "".join(
            '<li>%s</li>' % esc(i) for i in g["items"])
        groups.append("""                    <article class="sr22-vgroup sr22-vgroup--%s">
                        <div class="sr22-vgroup__head">
                            <span class="sr22-vgroup__icon"><i class="fa-solid %s"></i></span>
                            <div>
                                <h3>%s</h3>
                                <p class="sr22-vgroup__count">%d of the 15 listed</p>
                            </div>
                        </div>
                        <ul class="sr22-vgroup__list">%s</ul>
                        <p class="sr22-vgroup__note">%s</p>
                    </article>""" % (g["key"], g["icon"], esc(g["title"]),
                                     len(g["items"]), items, esc(g["note"])))

    return """        <section class="section sr22-violations">
            <div class="hero-container">
                <h2>Why Tennessee Drivers Need an SR-22</h2>
                <p class="sr22-lede">The Department of Safety lists fifteen reasons a driver may be required to carry SR-22 insurance. They fall into four broad situations &mdash; find yours below.</p>
                <div class="sr22-vgrid" data-animation="fade-up">
%s
                </div>
                <p>Not sure which applies to you? Pull your official requirements from the <a href="%s" target="_blank" rel="noopener nofollow">Department of Safety e-Services portal</a>, or call us at <a href="tel:%s">%s</a> and we will walk through it with you at no charge.</p>
                <p class="sr22-source">The fifteen items and their wording come from %s. Grouping them into four categories is ours, to make the list easier to scan &mdash; the department publishes them as a single list.</p>
            </div>
        </section>
""" % ("\n".join(groups), C.SOURCES["eservices"][1], C.SITE["phone_href"],
       esc(C.SITE["phone_display"]), source_link("fr"))


def services_grid(heading="SR-22 Services We File in Nashville"):
    if not has("SERVICES"):
        return ""
    # Own class names throughout. The base template's `card-service--slide__*`
    # classes absolutely-position the body to the bottom of a full-bleed slide,
    # so reusing them for a simple card grid stacked every card's text on top
    # of its neighbour. Styling for these lives in sr22.css.
    cards = []
    for s in C.SERVICES:
        art = service_art(s["slug"])[0]
        art_html = ("""<span class="sr22-svc__art"><img src="%s" alt="" loading="lazy" width="640" height="360"></span>"""
                    % art) if art else ""
        cards.append("""                    <a class="sr22-svc" href="/%s.html">
                        %s
                        <span class="sr22-svc__body">
                            <span class="sr22-svc__icon"><i class="fa-solid %s"></i></span>
                            <h3 class="sr22-svc__title">%s</h3>
                            <p class="sr22-svc__text">%s</p>
                            <span class="sr22-more">Learn more <i class="fa-solid fa-chevron-right"></i></span>
                        </span>
                    </a>""" % (s["slug"], art_html, s["icon"], esc(s["nav"]),
                               esc(s["summary"])))
    return """        <section class="section">
            <div class="hero-container">
                <h2>%s</h2>
                <div class="sr22-service-grid" data-animation="fade-up">
%s
                </div>
            </div>
        </section>
""" % (esc(heading), "\n".join(cards))


def cost_block():
    if not has("PAYMENT_PLAN"):
        return ""
    p = C.PAYMENT_PLAN
    return """        <section class="section sr22-cost">
            <div class="hero-container">
                <h2>How Much Does SR-22 Insurance Cost in Nashville?</h2>
                <p>The filing fee itself is small — carriers typically charge $15 to $25, usually once. Tennessee is explicit that the cost of the insurance is determined by the insurance company, not the state.</p>
                <p>What actually raises your price is the violation behind the filing. Third-party rate studies put average SR-22 auto insurance in Tennessee in the range of roughly $130 to $215 per month for minimum-limits coverage after a DUI, against roughly $65 to $80 per month for a driver with a clean record. Nashville rates tend to run above the statewide average because of urban traffic density and claim frequency in Davidson County.</p>
                <p>Your actual quote depends on the specific violation and its date, your age and how long you have been licensed, your ZIP code, whether you choose an owner or non-owner policy, your vehicle, your limits and deductibles, and any lapse in prior coverage.</p>
                <p><strong>The single most useful thing to understand:</strong> carriers disagree enormously about high-risk drivers. It is routine to see a wide spread between the highest and lowest quote for the same driver and the same coverage. That spread is the entire reason to use an independent agency instead of calling one carrier.</p>
                <h3>Reinstatement fees are separate from your premium</h3>
                <p>Tennessee charges reinstatement fees that vary by violation type, on top of whatever your insurance costs. The Department of Safety offers an installment plan: %s There is %s, then %s, %s.</p>
                <p>Confirm your exact amount on your official reinstatement requirements page in <a href="%s" target="_blank" rel="noopener nofollow">e-Services</a>.</p>
                <p class="sr22-disclaimer">%s</p>
                <p class="sr22-source">Source: %s.</p>
            </div>
        </section>
""" % (esc(p["eligibility"]), esc(p["down"]), esc(p["installment"]),
       esc(p["term"]), C.SOURCES["eservices"][1], esc(C.RATE_DISCLAIMER),
       source_link("installment"))


def steps_block():
    if not has("STEPS"):
        return ""
    items = []
    # Same reason as services_grid: the base `why-choose-us__features-item` is
    # a horizontal flex row with a 72%-wide title column, which threw the
    # heading and the body text side by side and overlapping.
    for i, (h, b) in enumerate(C.STEPS, 1):
        items.append("""                    <li class="sr22-step">
                        <span class="sr22-step__num">%d</span>
                        <h3 class="sr22-step__title">%s</h3>
                        <p class="sr22-step__text">%s</p>
                    </li>""" % (i, esc(h), esc(b)))
    return """        <section class="section sr22-steps">
            <div class="hero-container">
                <h2>How to Get SR-22 Insurance in Nashville: 5 Steps</h2>
                <ol class="sr22-steps__grid" data-animation="fade-up">
%s
                </ol>
                <p>Mail goes to %s. %s</p>
                <p class="sr22-source">Source: %s.</p>
            </div>
        </section>
""" % ("\n".join(items), esc(", ".join(C.MAIL["usps"])), esc(C.MAIL["note"]),
       source_link("reinstate"))


def faq_block(pairs, heading="Frequently Asked Questions"):
    if not pairs:
        return ""
    items = []
    for i, (q, a) in enumerate(pairs):
        items.append("""                    <details class="sr22-faq__item"%s>
                        <summary><h3>%s</h3></summary>
                        <p>%s</p>
                    </details>""" % (" open" if i == 0 else "", esc(q), esc(a)))
    return """        <section class="section sr22-faq">
            <div class="hero-container">
                <h2>%s</h2>
                <div class="sr22-faq__list">
%s
                </div>
            </div>
        </section>
""" % (esc(heading), "\n".join(items))


def quote_form(context=""):
    ctx = (' <input type="hidden" name="page_context" value="%s">' % esc(context)) if context else ""
    return """        <section class="section sr22-form" id="quote">
            <div class="hero-container">
                <h2>%s</h2>
                <p>%s</p>
                <form class="sr22-form__grid" data-animation="fade-up" action="%s" method="post">%s
                    <label>Full name<input type="text" name="name" required autocomplete="name"></label>
                    <label>Phone<input type="tel" name="phone" required autocomplete="tel"></label>
                    <label>Email<input type="email" name="email" autocomplete="email"></label>
                    <label>ZIP code<input type="text" name="zip" required inputmode="numeric" autocomplete="postal-code"></label>
%s                    <label class="sr22-form__wide">Anything else we should know?<textarea name="message" rows="4"></textarea></label>
                    <button type="submit" class="btn btn-accent"><span>Get My Free Quote</span> <i class="fa-solid fa-circle-arrow-right"></i></button>
                </form>
                <p>Or call <a href="tel:%s">%s</a> · Text %s · Open %s. Se habla español. No obligation, no credit card to get a quote.</p>
                <p class="sr22-disclaimer">Submitting this form does not bind coverage and is not an application. Coverage begins only when a carrier issues a policy.</p>
            </div>
        </section>
""" % (copy("form_h2"), copy("form_sub"), C.SITE["form_endpoint"], ctx,
       form_selects(), C.SITE["phone_href"],
       esc(C.SITE["phone_display"]), esc(C.SITE["text_display"]),
       esc(C.SITE["hours"]))


def author_block():
    s = C.SITE
    return """        <section class="section sr22-author">
            <div class="hero-container">
                <div class="sr22-author__card">
                    <h2>%s</h2>
                    <p><strong>%s</strong> — %s, TN license %s.</p>
                    <p>%s</p>
                    <p class="sr22-source">Page last updated %s. We update these pages when the Department of Safety changes its published guidance.</p>
                </div>
            </div>
        </section>
""" % (copy("author_h2"), esc(s["agent_name"]), esc(s["agent_title"]), esc(s["license"]),
       esc(s["agent_bio"]), s["last_updated"])


def dsc_block(keys, heading="Where to handle this in person"):
    if not has("DSC") or not keys:
        return ""
    rows = []
    for k in keys:
        d = C.DSC[k]
        badge = {"full": "Full-service — handles reinstatement",
                 "express": "Express — no testing, not for reinstatement",
                 "kiosk": "Self-service kiosk — not for reinstatement"}[d["type"]]
        maps = ("https://www.google.com/maps/search/?api=1&query="
                + d["addr"].replace(" ", "+").replace(",", "%2C"))
        rows.append("""                    <li class="sr22-dsc__item sr22-dsc--%s">
                        <h3>%s</h3>
                        <p><a href="%s" target="_blank" rel="noopener">%s</a><br>%s · %s</p>
                        <p class="sr22-dsc__badge">%s</p>
                    </li>""" % (d["type"], esc(d["name"]), maps, esc(d["addr"]),
                                esc(d["phone"]), C.DSC_HOURS, badge))
    return """        <section class="section sr22-dsc">
            <div class="hero-container">
                <h2>%s</h2>
                <ul class="sr22-dsc__list" data-animation="fade-left">
%s
                </ul>
                <p>Only full-service Driver Services Centers process reinstatements — paying fees, setting up the state’s installment plan, and submitting documents. Express locations and self-service kiosks do not. Centers stop taking new applicants before their posted closing time, so do not arrive at 4:45.</p>
                <p class="sr22-source">Addresses and hours from %s. Hours change — confirm before you drive.</p>
            </div>
        </section>
""" % (esc(heading), "\n".join(rows), source_link("locations"))


def form_selects(cls="", labelled=True):
    """Dropdowns from config.FORM_FIELDS: [(name, placeholder, [(value,label)])].

    `labelled` wraps each select in its <label> (the main quote form, where the
    placeholder doubles as the visible label); the compact hero card uses the
    placeholder option alone. Empty config renders no selects, which is correct
    for a simple quote form.
    """
    out = []
    for name, placeholder, options in getattr(C, "FORM_FIELDS", []):
        opts = "".join("\n                            "
                       '<option value="%s">%s</option>' % (v, esc(l))
                       for v, l in options)
        # the labelled variant shows the placeholder as the visible <label>,
        # so repeating it as a disabled option would be redundant
        ph = ("" if labelled else
              '\n                            <option value="" selected disabled>%s</option>'
              % esc(placeholder))
        sel = ('<select name="%s"%s>%s%s\n                        </select>'
               % (name, (' class="%s"' % cls) if cls else "", ph, opts))
        if labelled:
            out.append("                    <label>%s\n                        %s\n                    </label>\n"
                       % (esc(placeholder), sel))
        else:
            out.append("                        " + sel)
    return "\n".join(out)


def footer_sources():
    """Optional 'Official Sources' footer block from config.FOOTER_SOURCES:
    [(label, source_key)]. Omitted entirely when the niche has no authority
    worth linking."""
    rows = getattr(C, "FOOTER_SOURCES", [])
    if not rows:
        return ""
    items = "".join(
        '<li><a href="%s" target="_blank" rel="noopener nofollow">%s</a></li>'
        % (C.SOURCES[k][1], esc(label)) for label, k in rows)
    return ('<h4 class="secondary-color">Official Sources</h4>'
            '<ul class="footer-list">%s</ul>' % items)


def prose_sections(sections):
    """Render (h2, [paragraphs]) pairs. Body copy lives in config so the
    generator carries no niche voice of its own."""
    if not sections:
        return ""
    out = []
    for h2, paras in sections:
        out.append("                <h2>%s</h2>" % esc(h2))
        for para in paras:
            out.append("                <p>%s</p>" % para)
    return """        <section class="section sr22-prose">
            <div class="hero-container">
%s
            </div>
        </section>
""" % "\n".join(out)


def cta_band(text="Ready to get filed?"):
    return """        <section class="section sr22-cta-band">
            <div class="hero-container">
                <h2>%s</h2>
                <p>%s</p>
                <div class="tig-hero__cta">
                    <a href="/contact.html" class="btn btn-accent"><span>%s</span> <i class="fa-solid fa-circle-arrow-right"></i></a>
                    <a href="tel:%s" class="tig-hero__phone"><i class="fa-solid fa-phone"></i> <span>%s</span></a>
                </div>
            </div>
        </section>
""" % (esc(text), copy("cta_band_sub"), copy("hero_cta"), C.SITE["phone_href"], esc(C.SITE["phone_display"]))


def links_grid(heading, items, note=""):
    """items: (label, url, blurb) or (label, url, blurb, image_src).

    Cities pass their real Google Places photo; text-only entries render the
    same card without the image band.
    """
    def card(item):
        l, u, b = item[0], item[1], item[2]
        img = item[3] if len(item) > 3 else None
        art = ("""<span class="sr22-link-card__art"><img src="%s" alt="" loading="lazy"></span>"""
               % img) if img else ""
        return """                    <a class="sr22-link-card%s" href="%s">
                        %s
                        <span class="sr22-link-card__body">
                            <h3>%s</h3>
                            <p>%s</p>
                            <span class="sr22-more">View <i class="fa-solid fa-chevron-right"></i></span>
                        </span>
                    </a>""" % (" has-art" if img else "", u, art, esc(l), esc(b))

    cards = "\n".join(card(i) for i in items)
    note_html = "<p>%s</p>" % note if note else ""
    return """        <section class="section">
            <div class="hero-container">
                <h2>%s</h2>
                %s
                <div class="sr22-link-grid" data-animation="fade-up">
%s
                </div>
            </div>
        </section>
""" % (esc(heading), note_html, cards)


# -------------------------------------------------------------------- pages --

def build_home():
    url = BASE + "/"
    title = copy("home_title")
    desc = copy("home_desc")
    body = "".join([
        hero(copy("home_eyebrow"), copy("home_h1"), copy("home_sub"),
             [], photo_for("nashville"), inner=False,
             aside=hero_form_card()),
        service_marquee_section(),
        quick_answer(copy("home_quick")),
        answer_block(),
        violations_block(),
        services_grid(),
        cost_block(),
        steps_block(),
        dsc_block(["hart-lane", "hickory-hollow", "downtown-express", "metro-center"],
                  "Davidson County Driver Services Centers"),
        links_grid(copy("areas_h2"),
                   [(c["name"],
                     "/%s/%s/" % (GEO, c["slug"]),
                     "%s County · SR-22 filing and reinstatement help"
                     % c["county"],
                     photo_for(c["slug"])[0] or photo_for("nashville")[0])
                    for c in C.CITIES],
                   copy("areas_note")),
        faq_block(C.FAQ),
        author_block(),
        quote_form("homepage"),
    ])
    schema = [schema_website(), schema_agency(),
              schema_webpage(url, title, desc), schema_faq(C.FAQ),
              schema_breadcrumb([("Home", url)])]
    return write("index.html", page(title, desc, url, body, schema))


def build_service(svc):
    url = "%s/%s.html" % (BASE, svc["slug"])
    title = "%s | %s" % (svc["h1"], C.SITE["name"])
    desc = svc["summary"][:158]
    paras = "\n".join("                <p>%s</p>" % esc(p) for p in svc["body"])
    # Pages that assert procedural detail cite it. Services without a
    # `sources` key are describing what we do, not what the state requires,
    # and need no citation block.
    svc_sources = ""
    if svc.get("sources"):
        svc_sources = ('                <p class="sr22-source">Sources: %s.</p>'
                       % "; ".join(source_link(k) for k in svc["sources"]))
    others = [(s["nav"], "/%s.html" % s["slug"], s["summary"])
              for s in C.SERVICES if s["slug"] != svc["slug"]]

    a_src, a_alt = service_art(svc["slug"])
    svc_art_html = ""
    if a_src:
        svc_art_html = ("""        <section class="section sr22-artband">
            <div class="hero-container">
                <figure class="sr22-figure"><img src="%s" alt="%s" width="640" height="360"></figure>
            </div>
        </section>
""" % (a_src, esc(a_alt)))
    body = "".join([
        hero("SR-22 Services", esc(svc["h1"]), esc(svc["summary"]),
             [("Home", "/index.html"), ("Services", "/services.html"),
              (svc["nav"], url)], photo_for("nashville")),
        svc_art_html,
        quick_answer(esc(svc["summary"]) +
                     ' Call <a href="tel:%s">%s</a> or '
                     '<a href="/contact.html">request a quote</a>.'
                     % (C.SITE["phone_href"], esc(C.SITE["phone_display"]))),
        """        <section class="section">
            <div class="hero-container sr22-prose">
%s
%s
            </div>
        </section>
""" % (paras, svc_sources),
        answer_block(),
        cta_band(),
        links_grid("Other SR-22 situations we handle", others),
        author_block(),
        quote_form(svc["slug"]),
    ])
    schema = [schema_agency(), schema_webpage(url, title, desc),
              schema_service(svc),
              schema_breadcrumb([("Home", BASE + "/"),
                                 ("Services", BASE + "/services.html"),
                                 (svc["nav"], url)])]
    return write("%s.html" % svc["slug"], page(title, desc, url, body, schema))


def build_city(city):
    slug, name, county = city["slug"], city["name"], city["county"]
    url = "%s/%s/%s/" % (BASE, GEO, slug)
    title = copy("city_title", name=name)
    desc = copy("city_desc", name=name)
    pop = ("{:,}".format(city["pop"]) if city.get("pop") else None)
    hoods = ""
    if slug == "nashville":
        hoods = links_grid(
            "Nashville neighborhoods we serve",
            [(n["name"], "/%s/%s/%s/" % (GEO, HUB, n["slug"]),
              "ZIP %s · nearest center: %s"
              % (n["zips"], C.DSC[n["dsc"]]["name"]),
              photo_for(n["slug"])[0] or photo_for("nashville")[0])
             for n in C.NEIGHBORHOODS])

    siblings = [(c["name"], "/%s/%s/" % (GEO, c["slug"]),
                 "%s County" % c["county"])
                for c in C.CITIES if c["slug"] != slug]

    glance = """        <section class="section sr22-glance">
            <div class="hero-container">
                <h2>%s at a glance</h2>
                <dl class="sr22-glance__grid" data-animation="fade-right">
                    <div><dt>County</dt><dd>%s</dd></div>
                    %s
                    <div><dt>Court that clears your suspension</dt><dd>%s</dd></div>
                    <div><dt>Nearest full-service reinstatement center</dt><dd>%s</dd></div>
                    <div><dt>How long you carry the SR-22</dt><dd>The length of your suspension or revocation period</dd></div>
                    <div><dt>Minimum liability</dt><dd>%s</dd></div>
                </dl>
                <p class="sr22-source">Court locations: %s. Center details: %s.%s</p>
            </div>
        </section>
""" % (esc(name), esc(county + " County"),
       ("<div><dt>Population</dt><dd>%s (2020 Census)</dd></div>" % pop) if pop else "",
       esc(C.COUNTIES[county]["court"]),
       esc(next(C.DSC[k]["name"] for k in city["dsc"] if C.DSC[k]["type"] == "full")),
       C.TN_MINIMUMS["shorthand"],
       source_link("courts"), source_link("locations"),
       " Population: U.S. Census Bureau, 2020 Decennial Census." if pop else "")

    body = "".join([
        hero("%s County, Tennessee" % county,
             "SR22 Insurance in %s, TN" % esc(name),
             esc(city["intro"]),
             [("Home", "/index.html"), ("Service Areas", "/%s/" % GEO),
              (name, url)], photo_for(slug)),
        quick_answer(copy("home_quick")),
        glance,
        """        <section class="section sr22-prose">
            <div class="hero-container">
                <h2>What is different about an SR-22 in %s</h2>
                <p>%s</p>
                <p>%s</p>
            </div>
        </section>
""" % (esc(name), esc(city["angle"]), esc(city["commute"])),
        dsc_block(city["dsc"], "Driver Services Centers near %s" % name),
        answer_block(),
        services_grid("SR-22 services for %s drivers" % name),
        hoods,
        cost_block(),
        steps_block(),
        faq_block(C.FAQ[:8], "SR-22 questions from %s drivers" % name),
        links_grid("Other Middle Tennessee cities we serve", siblings),
        author_block(),
        quote_form("city:" + slug),
    ])
    schema = [schema_agency(), schema_webpage(url, title, desc),
              schema_faq(C.FAQ[:8]),
              jsonld({"@context": "https://schema.org", "@type": "Service",
                      "name": "SR-22 insurance filing in %s, TN" % name,
                      "serviceType": "SR-22 filing",
                      "provider": {"@id": BASE + "/#agency"},
                      "areaServed": {"@type": "City", "name": "%s, TN" % name},
                      "url": url}),
              schema_breadcrumb([("Home", BASE + "/"),
                                 ("Service Areas", BASE + "/%s/" % GEO),
                                 (name, url)])]
    return write("%s/%s/index.html" % (GEO, slug),
                 page(title, desc, url, body, schema))


def build_hood(hood):
    slug, name = hood["slug"], hood["name"]
    url = "%s/%s/%s/%s/" % (BASE, GEO, HUB, slug)
    title = copy("hood_title", name=name)
    desc = copy("hood_desc", name=name)
    d = C.DSC[hood["dsc"]]
    hub_url = "/%s/%s/" % (GEO, HUB)
    siblings = [(n["name"], "/%s/%s/%s/" % (GEO, HUB, n["slug"]),
                 "ZIP %s" % n["zips"])
                for n in C.NEIGHBORHOODS if n["slug"] != slug]
    body = "".join([
        hero(copy("hood_eyebrow"), copy("hood_h1", name=esc(name)),
             esc(hood["angle"]),
             [("Home", "/index.html"), ("Service Areas", "/%s/" % GEO),
              (HUB_NAME, "/%s/%s/" % (GEO, HUB)), (name, url)],
             # Fall back to the Nashville photo (with its credit) rather than
             # the CSS default, which would show the same image with no
             # attribution.
             photo_for(slug) if photo_for(slug)[0] else photo_for("nashville")),
        quick_answer(
            'We file SR-22 certificates for %s drivers (ZIP %s) electronically with the '
            '<a href="%s" target="_blank" rel="noopener nofollow">Tennessee Department of Safety</a>, usually the same business day. '
            'Nearest driver services location: %s at %s. '
            'Call <a href="tel:%s">%s</a>.'
            % (esc(name), esc(hood["zips"]), C.SOURCES["fr"][1],
               esc(d["name"]), esc(d["addr"]),
               C.SITE["phone_href"], esc(C.SITE["phone_display"]))),
        """        <section class="section sr22-prose">
            <div class="hero-container">
                <h2>SR-22 filing for %s</h2>
                <p>%s</p>
                <p>%s is inside Davidson County, so the court side of a reinstatement runs through %s and the state side runs through the Department of Safety. The requirements are identical to the rest of Tennessee — what changes locally is which counter is worth your afternoon.</p>
                <p>For the full explanation of what an SR-22 is, how long Tennessee makes you carry one, and what happens if the policy lapses, see <a href="%s">SR-22 insurance in Nashville</a> or our <a href="/faq.html">SR-22 FAQ</a>.</p>
            </div>
        </section>
""" % (esc(name), esc(hood["angle"]), esc(name),
       esc(C.COUNTIES["Davidson"]["court"]), hub_url),
        dsc_block([hood["dsc"]] + (["hart-lane"] if hood["dsc"] != "hart-lane" else []),
                  "Driver services near %s" % name),
        # No answer_block here on purpose. Neighborhood pages are the thinnest
        # in the fleet, and repeating the same 400-word explainer across 13 of
        # them is the doorway-page pattern. The parent Nashville page carries
        # it, one click away, and is linked from the Quick Answer above.
        services_grid("SR-22 services for %s drivers" % name),
        faq_block(C.FAQ[:6], "Common questions in %s" % name),
        links_grid("Other Nashville neighborhoods", siblings),
        links_grid("Nearby cities",
                   [(c["name"], "/%s/%s/" % (GEO, c["slug"]),
                     "%s County" % c["county"]) for c in C.CITIES[:8]]),
        author_block(),
        quote_form("hood:" + slug),
    ])
    schema = [schema_agency(), schema_webpage(url, title, desc),
              schema_faq(C.FAQ[:6]),
              schema_breadcrumb([("Home", BASE + "/"),
                                 ("Service Areas", BASE + "/%s/" % GEO),
                                 (HUB_NAME, BASE + "/%s/%s/" % (GEO, HUB)),
                                 (name, url)])]
    return write("%s/%s/%s/index.html" % (GEO, HUB, slug),
                 page(title, desc, url, body, schema))


def linkify(html_text, pairs, used):
    """Turn the first unused occurrence of each phrase into an internal link.

    Only touches text outside existing tags, so a phrase inside an <a> or an
    attribute is never double-wrapped.
    """
    for phrase, url in pairs:
        if phrase in used:
            continue
        # split on tags; only substitute inside text runs
        parts = re.split(r"(<[^>]+>)", html_text)
        for i, part in enumerate(parts):
            if part.startswith("<"):
                continue
            idx = part.find(phrase)
            if idx == -1:
                continue
            parts[i] = (part[:idx] + '<a href="%s">%s</a>' % (url, phrase)
                        + part[idx + len(phrase):])
            html_text = "".join(parts)
            used.add(phrase)
            break
    return html_text


def render_blocks(blocks, links=None, figure_after=None, figure_html=""):
    """Turn blog.py's (kind, payload) tuples into markup.

    Paragraph text may contain inline HTML (links, <em>), so `p`/`note`/
    `quote` are trusted and not escaped -- they come from blog.py, which we
    author, not from user input. List items are escaped.
    """
    out = []
    used = set()
    pairs = list(links or [])
    for n, (kind, payload) in enumerate(blocks):
        if figure_after is not None and n == figure_after:
            out.append(figure_html)
        if kind == "h2":
            out.append("                <h2>%s</h2>" % esc(payload))
        elif kind == "h3":
            out.append("                <h3>%s</h3>" % esc(payload))
        elif kind == "p":
            out.append("                <p>%s</p>"
                       % linkify(payload, pairs, used))
        elif kind == "ul":
            out.append('                <ul class="sr22-post__list">%s</ul>'
                       % "".join("<li>%s</li>" % esc(i) for i in payload))
        elif kind == "ol":
            out.append('                <ol class="sr22-post__list">%s</ol>'
                       % "".join("<li>%s</li>" % esc(i) for i in payload))
        elif kind == "note":
            out.append('                <aside class="sr22-post__note">'
                       '<strong>Worth knowing</strong><p>%s</p></aside>'
                       % linkify(payload, pairs, used))
        elif kind == "quote":
            out.append('                <blockquote class="sr22-post__quote">'
                       '<p>%s</p></blockquote>' % payload)
        else:
            raise ValueError("unknown block kind: %r" % kind)
    if figure_after is not None and figure_after >= len(blocks):
        out.append(figure_html)
    missing = [p for p, _ in pairs if p not in used]
    if missing:
        raise ValueError("internal-link phrase not found in body: %r" % missing)
    return "\n".join(out)


def read_time(post):
    """Derive read time from the actual body rather than a hand-set number,
    so edits to a post cannot leave a stale '9 min read' behind."""
    words = 0
    for kind, payload in post["body"]:
        if isinstance(payload, list):
            words += sum(len(str(i).split()) for i in payload)
        else:
            words += len(re.sub(r"<[^>]+>", " ", str(payload)).split())
    return "%d min read" % max(1, round(words / 225))


def post_art(slug):
    """(src, alt) for a guide's illustration, or (None, None).

    Alt text comes from make_blog_art.py so the description of the picture
    lives next to the code that draws it and cannot drift.
    """
    entry = BLOG_ART.get(slug)
    if not entry or not os.path.exists(
            os.path.join(ROOT, "assets", "images", "blog", slug + ".svg")):
        return None, None
    return "/assets/images/blog/%s.svg" % slug, entry[1]


def service_art(slug):
    """(src, alt) for a service illustration, or (None, None)."""
    entry = SERVICE_ART.get(slug)
    if not entry or not os.path.exists(
            os.path.join(ROOT, "assets", "images", "services", slug + ".svg")):
        return None, None
    return "/assets/images/services/%s.svg" % slug, entry[2]


def post_by_slug(slug):
    for p in C.POSTS:
        if p["slug"] == slug:
            return p
    raise KeyError("no such post: %s" % slug)


def build_post(post):
    slug = post["slug"]
    url = "%s/blog/%s/" % (BASE, slug)
    title = "%s | %s" % (post["title"], C.SITE["name"])
    desc = post["meta"]

    sources = "".join(
        "<li>%s</li>" % source_link(k) for k in post["sources"])
    tags = "".join('<span class="sr22-post__tag">%s</span>' % esc(t)
                   for t in post["tags"])
    related = [(post_by_slug(s)["title"], "/blog/%s/" % s,
                post_by_slug(s)["dek"]) for s in post["related"]]

    # Image 1 — header illustration
    art_src, art_alt = post_art(slug)
    art_html = ""
    if art_src:
        art_html = ('                <figure class="sr22-post__art">'
                    '<img src="%s" alt="%s" width="640" height="360"></figure>'
                    % (art_src, esc(art_alt)))

    # Image 2 — a diagram carrying a specific fact, dropped in around a third
    # of the way down so it lands inside the argument rather than after it
    fig_html = ""
    fig_after = None
    dia = BLOG_DIAGRAM.get(slug)
    dia_path = os.path.join(ROOT, "assets", "images", "blog", slug + "-fig.svg")
    if dia and os.path.exists(dia_path):
        fig_after = max(2, len(post["body"]) // 3)
        fig_html = ('                <figure class="sr22-post__fig">'
                    '<img src="/assets/images/blog/%s-fig.svg" alt="%s" '
                    'loading="lazy" width="640" height="360"></figure>'
                    % (slug, esc(dia[1])))

    # Image 3 — a real, credited Middle Tennessee photo near the end
    photo_html = ""
    photo_json = None
    pinfo = C.POST_PHOTO.get(slug)
    if pinfo:
        psrc, _ = photo_for(pinfo[0])
        pcredit = RAW_CREDITS.get(pinfo[0])
        if psrc:
            photo_json = psrc
            photo_html = ('                <figure class="sr22-post__photo">'
                          '<img src="%s" alt="%s" loading="lazy">'
                          '<figcaption>%s<span>Photo: %s via Google Maps</span>'
                          '</figcaption></figure>'
                          % (psrc, esc(pinfo[1]), esc(pinfo[1]), esc(pcredit)))

    body = "".join([
        hero("SR-22 Guide", esc(post["title"]), esc(post["dek"]),
             [("Home", "/index.html"), ("Blog", "/blog/"),
              (post["title"], url)],
             photo_for("nashville")),
        """        <section class="section sr22-post">
            <div class="hero-container">
                <p class="sr22-post__meta">%s · %s · Updated %s</p>
                <div class="tig-tldr" data-animation="fade-up">
                    <span class="tig-tldr__label"><i class="fa-solid fa-bolt"></i> The short answer</span>
                    <p>%s</p>
                </div>
%s
                <div class="sr22-post__body">
%s
                </div>
%s
                <div class="sr22-post__sources">
                    <h3>Sources</h3>
                    <ul>%s</ul>
                    <p class="sr22-source">This article summarises publicly published Tennessee Department of Safety guidance as of %s. It is general information, not legal advice, and not a quote. Your own reinstatement requirements page in e-Services is the authoritative record for your situation.</p>
                </div>
            </div>
        </section>
""" % (tags, read_time(post), post["date"], esc(post["tldr"]),
       art_html,
       render_blocks(post["body"], C.INTERNAL_LINKS.get(slug), fig_after, fig_html),
       photo_html, sources, post["date"]),
        author_block(),
        cta_band("Need this handled rather than explained?"),
        links_grid("Keep reading", related),
        quote_form("blog:" + slug),
    ])

    article = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "@id": url + "#article",
        "headline": post["title"],
        "description": post["meta"],
        "url": url,
        "datePublished": post["date"],
        "dateModified": C.SITE["last_updated"],
        "inLanguage": "en-US",
        "keywords": ", ".join(post["tags"]),
        "articleSection": post["tags"][0],
        "publisher": {"@id": BASE + "/#agency"},
        "isPartOf": {"@id": BASE + "/blog/#blog"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url + "#webpage"},
        "image": [BASE + u for u in
                  [art_src,
                   ("/assets/images/blog/%s-fig.svg" % slug) if fig_html else None,
                   photo_json] if u] or None,
        "citation": [{"@type": "CreativeWork", "name": C.SOURCES[k][0],
                      "url": C.SOURCES[k][1]}
                     for k in post["sources"] if C.SOURCES[k][1]],
    }
    article = {k: v for k, v in article.items() if v is not None}
    # Only claim authorship once there is a real person to name -- an author
    # of "[AGENT NAME]" is worse than no author property at all.
    if not C.SITE["agent_name"].startswith("["):
        article["author"] = {"@type": "Person", "name": C.SITE["agent_name"],
                             "jobTitle": C.SITE["agent_title"]}
    else:
        article["author"] = {"@id": BASE + "/#agency"}

    schema = [schema_agency(), schema_webpage(url, post["title"], desc),
              jsonld(article),
              schema_breadcrumb([("Home", BASE + "/"),
                                 ("Blog", BASE + "/blog/"),
                                 (post["title"], url)])]
    return write("blog/%s/index.html" % slug, page(title, desc, url, body, schema))


def build_blog_index():
    url = BASE + "/blog/"
    title = copy("blog_title")
    desc = copy("blog_desc")
    cards = "\n".join(
        """                    <article class="sr22-post-card">
                        <a class="sr22-post-card__art" href="/blog/%s/" tabindex="-1" aria-hidden="true">
                            <img src="%s" alt="" loading="lazy" width="640" height="360">
                        </a>
                        <div class="sr22-post-card__body">
                            <p class="sr22-post__meta">%s<span class="sr22-post__read">%s</span></p>
                            <h3><a href="/blog/%s/">%s</a></h3>
                            <p>%s</p>
                            <a href="/blog/%s/" class="sr22-more">Read the guide <i class="fa-solid fa-chevron-right"></i></a>
                        </div>
                    </article>"""
        % (p["slug"], post_art(p["slug"])[0] or "",
           "".join('<span class="sr22-post__tag">%s</span>' % esc(t)
                   for t in p["tags"]),
           read_time(p), p["slug"], esc(p["title"]), esc(p["dek"]), p["slug"])
        for p in C.POSTS)

    body = "".join([
        hero(copy("blog_eyebrow"), copy("blog_h1"), copy("blog_sub"),
             [("Home", "/index.html"), ("Blog", url)],
             photo_for("nashville")),
        """        <section class="section">
            <div class="hero-container">
                <div class="sr22-post-grid" data-animation="fade-up">
%s
                </div>
            </div>
        </section>
""" % cards,
        cta_band(),
        quote_form("blog-index"),
    ])
    schema = [schema_agency(), schema_webpage(url, title, desc),
              jsonld({"@context": "https://schema.org", "@type": "Blog",
                      "@id": url + "#blog", "url": url, "name": title,
                      "description": desc, "inLanguage": "en-US",
                      "publisher": {"@id": BASE + "/#agency"},
                      "blogPost": [
                          {"@type": "BlogPosting", "headline": p["title"],
                           "url": "%s/blog/%s/" % (BASE, p["slug"]),
                           "image": BASE + (post_art(p["slug"])[0] or ""),
                           "datePublished": p["date"]}
                          for p in C.POSTS]}),
              schema_breadcrumb([("Home", BASE + "/"), ("Blog", url)])]
    return write("blog/index.html", page(title, desc, url, body, schema))


def build_hub():
    url = BASE + "/%s/" % GEO
    title = copy("hub_title")
    desc = copy("hub_desc")
    body = "".join([
        hero(copy("hub_eyebrow"), copy("hub_h1"), copy("hub_sub"),
             [("Home", "/index.html"), ("Service Areas", url)],
             photo_for("nashville")),
        links_grid("Cities we serve",
                   [(c["name"], "/%s/%s/" % (GEO, c["slug"]),
                     "%s County · pop. %s (2020 Census)"
                     % (c["county"], "{:,}".format(c["pop"])),
                     photo_for(c["slug"])[0] or photo_for("nashville")[0])
                    for c in C.CITIES]),
        links_grid("Nashville neighborhoods",
                   [(n["name"], "/%s/%s/%s/" % (GEO, HUB, n["slug"]),
                     "ZIP %s" % n["zips"],
                     photo_for(n["slug"])[0] or photo_for("nashville")[0])
                    for n in C.NEIGHBORHOODS]),
        """        <section class="section sr22-prose">
            <div class="hero-container">
                <h2>Areas we cover without a dedicated page</h2>
                <p>We also write SR-22 policies for drivers along the I-24, I-40 and I-65 corridors and in the smaller communities between these cities. If your town is not listed, the requirements are the same statewide — call us and we will tell you which county court and which Driver Services Center apply to you.</p>
                <p>Populations shown are from the U.S. Census Bureau’s 2020 Decennial Census. Driver Services Center addresses and hours come from %s and change from time to time; confirm before you drive.</p>
            </div>
        </section>
""" % source_link("locations"),
        cta_band(),
        quote_form("hub"),
    ])
    items = [{"@type": "ListItem", "position": i + 1,
              "name": c["name"] + ", TN",
              "url": "%s/%s/%s/" % (BASE, GEO, c["slug"])}
             for i, c in enumerate(C.CITIES)]
    schema = [schema_agency(), schema_webpage(url, title, desc),
              jsonld({"@context": "https://schema.org", "@type": "ItemList",
                      "name": "SR-22 insurance service areas in Middle Tennessee",
                      "itemListElement": items}),
              schema_breadcrumb([("Home", BASE + "/"), ("Service Areas", url)])]
    return write("%s/index.html" % GEO, page(title, desc, url, body, schema))


def build_services_index():
    url = BASE + "/services.html"
    title = copy("services_idx_title")
    desc = copy("services_idx_desc")
    body = "".join([
        hero(copy("services_idx_eyebrow"), copy("services_idx_h1"), copy("services_idx_sub"),
             [("Home", "/index.html"), ("Services", url)],
             photo_for("nashville")),
        services_grid("What we file"),
        answer_block(),
        cost_block(),
        cta_band(),
        quote_form("services"),
    ])
    schema = [schema_agency(), schema_webpage(url, title, desc),
              jsonld({"@context": "https://schema.org", "@type": "ItemList",
                      "name": "SR-22 insurance services",
                      "itemListElement": [
                          {"@type": "ListItem", "position": i + 1,
                           "name": s["h1"],
                           "url": "%s/%s.html" % (BASE, s["slug"])}
                          for i, s in enumerate(C.SERVICES)]}),
              schema_breadcrumb([("Home", BASE + "/"), ("Services", url)])]
    return write("services.html", page(title, desc, url, body, schema))


def build_about():
    url = BASE + "/about.html"
    title = copy("about_title")
    desc = copy("about_desc")
    body = "".join([
        hero(copy("about_eyebrow"), copy("about_h1"), copy("about_sub"),
             [("Home", "/index.html"), ("About", url)], photo_for("nashville")),
        prose_sections(getattr(C, "ABOUT_SECTIONS", [])),
        author_block(),
        cta_band(),
        quote_form("about"),
    ])
    schema = [schema_agency(), schema_webpage(url, title, desc),
              schema_breadcrumb([("Home", BASE + "/"), ("About", url)])]
    return write("about.html", page(title, desc, url, body, schema))


def build_contact():
    url = BASE + "/contact.html"
    title = copy("contact_title")
    desc = copy("contact_desc")
    s = C.SITE
    body = "".join([
        hero(copy("contact_eyebrow"), copy("contact_h1"), copy("contact_sub"),
             [("Home", "/index.html"), ("Contact", url)], photo_for("nashville")),
        quote_form("contact"),
        """        <section class="section sr22-prose">
            <div class="hero-container">
                <h2>Reach us directly</h2>
                <ul class="footer-list zero-icon">
                    <li>Phone: <a href="tel:%s">%s</a></li>
                    <li>Text: %s</li>
                    <li>Email: <a href="mailto:%s">%s</a></li>
                    <li>Office: %s, %s, %s %s</li>
                    <li>Hours: %s</li>
                </ul>
                <h2>Where the state wants your paperwork</h2>
                <p>Reinstatement documents go to the Department of Safety, not to us. By mail: %s. By courier: %s. %s</p>
                <p class="sr22-source">Source: %s.</p>
            </div>
        </section>
""" % (s["phone_href"], esc(s["phone_display"]), esc(s["text_display"]),
       esc(s["email"]), esc(s["email"]), esc(s["street"]), esc(s["city"]),
       s["region"], esc(s["postal"]), esc(s["hours"]),
       esc(", ".join(C.MAIL["usps"])), esc(", ".join(C.MAIL["courier"])),
       esc(C.MAIL["note"]), source_link("reinstate")),
        dsc_block(["hart-lane", "hickory-hollow"],
                  "Nashville reinstatement counters"),
    ])
    schema = [schema_agency(), schema_webpage(url, title, desc),
              jsonld({"@context": "https://schema.org", "@type": "ContactPage",
                      "@id": url + "#contactpage", "url": url,
                      "about": {"@id": BASE + "/#agency"}}),
              schema_breadcrumb([("Home", BASE + "/"), ("Contact", url)])]
    return write("contact.html", page(title, desc, url, body, schema))


def build_faq():
    url = BASE + "/faq.html"
    title = copy("faq_title")
    desc = copy("faq_desc")
    body = "".join([
        hero(copy("faq_eyebrow"), copy("faq_h1"), copy("faq_sub"),
             [("Home", "/index.html"), ("FAQ", url)], photo_for("nashville")),
        answer_block(),
        faq_block(C.FAQ),
        violations_block(),
        """        <section class="section sr22-prose">
            <div class="hero-container">
                <h2>What we could not confirm</h2>
                <p>Most SR-22 sites state everything with equal confidence. These are the points where the published record is thinner than the internet suggests:</p>
                <ul>
%s
                </ul>
            </div>
        </section>
""" % "\n".join("                    <li>%s</li>" % esc(v)
                for v in C.UNVERIFIED.values()),
        cta_band(),
        quote_form("faq"),
    ])
    schema = [schema_agency(), schema_webpage(url, title, desc),
              schema_faq(C.FAQ),
              schema_breadcrumb([("Home", BASE + "/"), ("FAQ", url)])]
    return write("faq.html", page(title, desc, url, body, schema))


def build_form_stub():
    """Landing page for the quote form while no CRM endpoint is wired.

    A form posting to a dead URL 404s and a visitor assumes their details were
    received. On a publicly reachable preview that is worse than an obviously
    unfinished page, so this says plainly that nothing was submitted and gives
    the phone number instead. Delete this page once form_endpoint points at a
    real destination.
    """
    url = BASE + "/quote-not-connected.html"
    guides = "".join(
        '                    <li><a href="/blog/%s/">%s</a></li>\n'
        % (p["slug"], esc(p["title"])) for p in C.POSTS[:3])
    body = """        <section class="section sr22-prose" style="padding-top:180px">
            <div class="hero-container">
                <h1>Nothing was submitted</h1>
                <div class="sr22-disclaimer" style="font-size:1rem">
                    <p><strong>This is a preview build.</strong> The quote form is not yet connected to a system that can receive it, so your details were <strong>not</strong> sent to anyone and were not stored.</p>
                </div>
                <p>If you actually need an SR-22 filed, please call <a href="tel:%s">%s</a> rather than using the form.</p>
                <p>In the meantime, these pages answer most of what people ask before they call:</p>
                <ul>
%s                    <li><a href="/faq.html">SR-22 questions, answered</a></li>
                </ul>
                <p>You can also pull your own official reinstatement requirements from the <a href="%s" target="_blank" rel="noopener nofollow">Tennessee Department of Safety e-Services portal</a> at any time, free.</p>
            </div>
        </section>
""" % (C.SITE["phone_href"], esc(C.SITE["phone_display"]), guides,
       C.SOURCES["eservices"][1])
    return write("quote-not-connected.html",
                 page("Form Not Connected | " + C.SITE["name"],
                      "This preview build's quote form is not connected. "
                      "Nothing was submitted.",
                      url, body, [schema_agency()]))


def build_404():
    body = """        <section class="section sr22-prose" style="padding-top:180px">
            <div class="hero-container">
                <h1>Page not found</h1>
                <p>That page does not exist. Here is where most people are headed:</p>
                <ul>%s</ul>
            </div>
        </section>
""" % "".join(
        '<li><a href="%s">%s</a></li>' % (u, esc(l))
        for l, u in getattr(C, "NOT_FOUND_LINKS",
                            [("Home", "/"), ("Services", "/services.html"),
                             ("Service areas", "/%s/" % GEO),
                             ("Questions, answered", "/faq.html"),
                             ("Get a quote", "/contact.html")]))
    return write("404.html", page("Page Not Found | " + C.SITE["name"],
                                  "The page you were looking for does not exist.",
                                  BASE + "/404.html", body, [schema_agency()]))


DEFAULT_LEGAL = [
    ("privacy", "Privacy Policy", [
        "We collect the information you submit through the form on this site "
        "in order to respond to your enquiry and provide the service you asked "
        "about. We do not sell your information.",
        "[REVIEW REQUIRED: this is a starting draft. Have counsel review it "
        "and confirm any sector-specific privacy obligations before launch.]",
    ]),
    ("terms", "Terms & Conditions", [
        "This site is informational. Nothing on it is a contract, a quote, or "
        "a guarantee of price, availability or outcome.",
        "[REVIEW REQUIRED: have a qualified reviewer approve this site before "
        "launch, including any advertising rules that apply to this trade.]",
    ]),
]


def build_legal():
    """Minimal privacy/terms so footer links are not broken. Deliberately
    plain -- these need a lawyer's pass before launch, and say so."""
    out = []
    for slug, h1, paras in getattr(C, "LEGAL_PAGES", DEFAULT_LEGAL):
        url = "%s/%s.html" % (BASE, slug)
        body = """        <section class="section sr22-prose" style="padding-top:180px">
            <div class="hero-container">
                <h1>%s</h1>
%s
                <p class="sr22-source">Last updated %s.</p>
            </div>
        </section>
""" % (h1, "\n".join("                <p>%s</p>" % esc(p) for p in paras),
       C.SITE["last_updated"])
        out.append(write("%s.html" % slug,
                         page("%s | %s" % (h1, C.SITE["name"]),
                              "%s for %s." % (h1, C.SITE["name"]),
                              url, body, [schema_agency(),
                                          schema_webpage(url, h1, h1)])))
    return out


# ---------------------------------------------------------------- ancillary --

def build_sitemap(urls):
    rows = "\n".join(
        "  <url><loc>%s</loc><lastmod>%s</lastmod></url>"
        % (u, C.SITE["last_updated"]) for u in urls)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + rows + "\n</urlset>\n")
    return write("sitemap.xml", xml)


def build_robots():
    if C.PREVIEW:
        return write("robots.txt",
                     "# PREVIEW BUILD -- not for indexing.\n"
                     "# Set PREVIEW = False in config.py at launch.\n"
                     "User-agent: *\nDisallow: /\n")
    return write("robots.txt",
                 "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE)


def build_llms():
    lines = [
        "# %s" % C.SITE["name"],
        "> Independent Tennessee insurance agency placing SR-22 auto "
        "insurance for drivers in Nashville and Middle Tennessee. The "
        "certificate is filed electronically with the Tennessee Department "
        "of Safety and Homeland Security by a licensed carrier, usually the "
        "same business day. Office: %s, %s, %s %s. Phone: %s."
        % (C.SITE["street"], C.SITE["city"], C.SITE["region"],
           C.SITE["postal"], C.SITE["phone_display"]),
        "",
        "## Key Tennessee facts (verified against tn.gov)",
    ]
    for label, claim, key in C.TN_FACTS:
        lines.append("- %s: %s (Source: %s)"
                     % (label, claim, C.SOURCES[key][1]))
    lines += [
        "- Tennessee minimum liability limits are %s: %s bodily injury per "
        "person, %s per accident, %s property damage (%s)."
        % (C.TN_MINIMUMS["shorthand"], C.TN_MINIMUMS["bi_person"],
           C.TN_MINIMUMS["bi_accident"], C.TN_MINIMUMS["pd"],
           C.TN_MINIMUMS["cite"]),
        "- Reinstatement fee installment plan: %s $25 administrative down "
        "payment, then $75 per quarter, up to 60 months. (Source: %s)"
        % (C.PAYMENT_PLAN["eligibility"], C.SOURCES["installment"][1]),
        "",
        "## Services",
    ]
    for s in C.SERVICES:
        lines.append("- [%s](%s/%s.html): %s"
                     % (s["h1"], BASE, s["slug"], s["summary"]))
    lines += ["", "## Service areas"]
    for c in C.CITIES:
        lines.append("- [%s, %s](%s/%s/%s/): %s County%s"
                     % (c["name"], C.SITE["region"], BASE, GEO, c["slug"], c["county"],
                        ", pop. {:,} (2020 Census)".format(c["pop"])
                        if c.get("pop") else ""))
    lines += ["", "## Guides"]
    for p in C.POSTS:
        lines.append("- [%s](%s/blog/%s/): %s"
                     % (p["title"], BASE, p["slug"], p["tldr"]))
    lines += ["", "## Resources",
              "- [FAQ](%s/faq.html)" % BASE,
              "- [All guides](%s/blog/)" % BASE,
              "- [All services](%s/services.html)" % BASE,
              "- [Contact](%s/contact.html)" % BASE,
              "", "Last updated %s." % C.SITE["last_updated"]]
    return write("llms.txt", "\n".join(lines) + "\n")


# --------------------------------------------------------------------- main --

def main():
    built = [build_home(), build_services_index(), build_about(),
             build_contact(), build_faq(), build_404(),
             build_form_stub()]
    built += build_legal()
    for s in C.SERVICES:
        built.append(build_service(s))
    built.append(build_hub())
    for c in C.CITIES:
        built.append(build_city(c))
    for n in C.NEIGHBORHOODS:
        built.append(build_hood(n))
    built.append(build_blog_index())
    for p in C.POSTS:
        built.append(build_post(p))

    urls = []
    for rel in built:
        if rel in ("404.html", "quote-not-connected.html"):
            continue
        if rel.endswith("index.html"):
            urls.append(BASE + "/" + rel[:-len("index.html")])
        else:
            urls.append(BASE + "/" + rel)
    build_sitemap(sorted(set(urls)))
    build_robots()
    build_llms()
    print("Generated %d pages (+ sitemap, robots, llms.txt)" % len(built))
    if not PHOTOS:
        print("NOTE: places_manifest.json missing or empty -- pages are using "
              "the default hero background. Run fetch_photos.py, review the "
              "contact sheets, then re-run this generator.")


if __name__ == "__main__":
    main()
