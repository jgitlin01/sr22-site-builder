#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the service page illustrations.

    python3 make_service_art.py

Same approach and frame as make_blog_art.py: original artwork, brand palette,
nothing to license. Eighteen services is too many to hand-draw as one-offs and
keep coherent, so each is composed from a shared card plus one distinct motif
drawn from a small vocabulary of parts (vehicle, certificate, badge, keys,
gavel, clock, meter). The result reads as a set rather than eighteen unrelated
pictures.

Output: assets/images/services/<slug>.svg  (16:9)
"""

import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "images", "services")

W, H = 640, 360
NAVY_1, NAVY_2, NAVY_3 = "#0B2545", "#16324F", "#1E4166"
AMBER, BLUE, PAPER, MUTED = "#F2B441", "#4E86C4", "#F4F7FB", "#8CA6C4"
RED = "#E05B4B"


def frame(inner, gid, title):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">
  <defs>
    <linearGradient id="bg{gid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{NAVY_2}"/><stop offset="100%" stop-color="{NAVY_1}"/>
    </linearGradient>
    <radialGradient id="gl{gid}" cx="0.8" cy="0.2" r="0.8">
      <stop offset="0%" stop-color="{AMBER}" stop-opacity=".20"/>
      <stop offset="100%" stop-color="{AMBER}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="gr{gid}" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0v40" fill="none" stroke="#FFF" stroke-opacity=".05"/>
    </pattern>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg{gid})"/>
  <rect width="{W}" height="{H}" fill="url(#gr{gid})"/>
  <rect width="{W}" height="{H}" fill="url(#gl{gid})"/>
  <text x="52" y="80" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="32">{title}</text>
{inner}
  <rect x=".5" y=".5" width="{W-1}" height="{H-1}" fill="none" stroke="#FFF" stroke-opacity=".10"/>
</svg>
"""


# ------------------------------------------------------------ parts kit -- #

def car(x, y, scale=1.0, body=PAPER, glass=NAVY_3, wheel=MUTED):
    return f"""  <g transform="translate({x},{y}) scale({scale})">
    <path fill="{body}" d="M40 128c-13 0-22-8-22-20v-14c0-11 7-19 18-22l52-13 41-32c11-9 24-13 38-13h51c17 0 32 7 43 20l30 34 55 12c15 3 24 13 24 27v1c0 12-9 20-22 20H40z"/>
    <path fill="{glass}" d="M152 24h47c12 0 22 5 30 14l24 27h-101z"/>
    <path fill="{glass}" d="M138 25l-11 40H86l32-25c6-5 13-9 20-15z"/>
    <circle cx="112" cy="124" r="31" fill="#101828"/><circle cx="112" cy="124" r="14" fill="{wheel}"/>
    <circle cx="292" cy="124" r="31" fill="#101828"/><circle cx="292" cy="124" r="14" fill="{wheel}"/>
  </g>"""


def cert(x, y, label, w=150, h=182, on=True):
    fill = PAPER if on else "#FFFFFF"
    op = "1" if on else ".14"
    ink = NAVY_1 if on else PAPER
    return f"""  <g transform="translate({x},{y})">
    <rect width="{w}" height="{h}" rx="12" fill="{fill}" fill-opacity="{op}"/>
    <rect x="20" y="24" width="{w-52}" height="11" rx="5.5" fill="{ink}" fill-opacity=".26"/>
    <rect x="20" y="44" width="{w-78}" height="9" rx="4.5" fill="{ink}" fill-opacity=".18"/>
    <text x="{w/2}" y="{h/2+14}" fill="{AMBER if on else MUTED}" text-anchor="middle"
          font-family="system-ui,sans-serif" font-size="27" font-weight="800">{label}</text>
    <rect x="20" y="{h-40}" width="{w-52}" height="9" rx="4.5" fill="{ink}" fill-opacity=".16"/>
  </g>"""


def keys(x, y, colour=AMBER, scale=1.0):
    return f"""  <g transform="translate({x},{y}) scale({scale})">
    <circle cx="0" cy="0" r="26" fill="none" stroke="{colour}" stroke-width="9"/>
    <rect x="20" y="-7" width="76" height="14" rx="5" fill="{colour}"/>
    <rect x="72" y="5" width="11" height="20" rx="4" fill="{colour}"/>
    <rect x="90" y="5" width="11" height="15" rx="4" fill="{colour}"/>
  </g>"""


def shield(x, y, colour=AMBER, tick=True, scale=1.0):
    t = (f'<path d="M-22 4 L-6 20 L24-16" fill="none" stroke="{NAVY_1}" '
         f'stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>') if tick else ""
    return f"""  <g transform="translate({x},{y}) scale({scale})">
    <path d="M0-72 62-48v46C62 36 34 66 0 80-34 66-62 36-62-2v-46z" fill="{colour}" fill-opacity=".92"/>
    {t}
  </g>"""


def gavel(x, y, scale=1.0):
    return f"""  <g transform="translate({x},{y}) scale({scale})">
    <rect x="-70" y="52" width="140" height="16" rx="8" fill="{MUTED}" fill-opacity=".7"/>
    <g transform="rotate(-32)">
      <rect x="-16" y="-64" width="86" height="40" rx="10" fill="{PAPER}"/>
      <rect x="16" y="-30" width="16" height="76" rx="7" fill="{MUTED}"/>
    </g>"""+"</g>"


def clock(x, y, r=62, hand=AMBER):
    return f"""  <g transform="translate({x},{y})">
    <circle r="{r}" fill="#FFF" fill-opacity=".08"/>
    <circle r="{r}" fill="none" stroke="{MUTED}" stroke-width="4" stroke-opacity=".55"/>
    <line x1="0" y1="0" x2="0" y2="{-r+22}" stroke="{PAPER}" stroke-width="5" stroke-linecap="round"/>
    <line x1="0" y1="0" x2="{r-26}" y2="16" stroke="{hand}" stroke-width="5" stroke-linecap="round"/>
    <circle r="6" fill="{PAPER}"/>
  </g>"""


def bars(x, y, vals, colour=AMBER, bw=42, gap=20):
    out = ""
    for i, v in enumerate(vals):
        out += (f'<rect x="{x + i*(bw+gap)}" y="{y - v}" width="{bw}" height="{v}" rx="7" '
                f'fill="{colour}" fill-opacity="{0.3 + i*0.18:.2f}"/>')
    return "  " + out


def road(x, y, w=380, colour=MUTED):
    dashes = "".join(
        f'<rect x="{x + i*68}" y="{y}" width="40" height="6" rx="3" fill="{colour}" fill-opacity=".45"/>'
        for i in range(w // 68 + 1))
    return "  " + dashes


def label(x, y, text, colour=MUTED, size=17):
    return (f'  <text x="{x}" y="{y}" fill="{colour}" font-family="system-ui,sans-serif" '
            f'font-size="{size}">{text}</text>')


def chip(x, y, text, colour=AMBER, w=210):
    return f"""  <g transform="translate({x},{y})">
    <rect width="{w}" height="42" rx="21" fill="{colour}" fill-opacity=".18"/>
    <text x="20" y="28" fill="{colour}" font-family="system-ui,sans-serif" font-size="15" font-weight="700">{text}</text>
  </g>"""


# ------------------------------------------------------------- services -- #
# slug: (title on the card, artwork, alt text)

SERVICES = {
 "owner-sr22-insurance": ("Owner&#8217;s policy",
    car(150, 168, .78) + shield(516, 196, AMBER, True, .58) + road(120, 316),
    "A car with a shield and tick, for an owner's SR-22 policy"),

 "non-owner-sr22-insurance": ("No car required",
    keys(190, 200, AMBER, 1.5) + shield(470, 196, AMBER, True, .58)
    + label(52, 296, "Liability cover when you drive a car you do not own"),
    "A set of keys without a car, for a non-owner SR-22 policy"),

 "sr22-after-dui": ("After a DUI",
    gavel(180, 176, 1.1) + cert(400, 118, "SR-22", 150, 182)
    + label(52, 320, "Filing period follows the revocation"),
    "A gavel beside an SR-22 certificate, for filings after a DUI"),

 "suspended-license-insurance": ("Licence suspended",
    cert(96, 122, "LICENCE", 176, 176, False)
    + f'  <path d="M112 292 L256 148" stroke="{RED}" stroke-width="9" stroke-linecap="round"/>'
    + cert(400, 122, "SR-22", 150, 176) + label(52, 330, "You can insure before you are licensed again"),
    "A struck-through licence beside an active SR-22 certificate"),

 "sr22-with-ignition-interlock": ("Interlock + filing",
    f'''  <g transform="translate(150,196)">
    <rect x="-72" y="-52" width="144" height="104" rx="16" fill="{PAPER}"/>
    <rect x="-50" y="-30" width="100" height="34" rx="8" fill="{NAVY_3}" fill-opacity=".55"/>
    <circle cx="-24" cy="26" r="10" fill="{AMBER}"/><circle cx="4" cy="26" r="10" fill="{MUTED}" fill-opacity=".6"/>
    <circle cx="32" cy="26" r="10" fill="{MUTED}" fill-opacity=".6"/>
  </g>''' + cert(400, 122, "SR-22", 150, 176)
    + label(52, 330, "Two requirements, two clocks"),
    "A breath-test device beside an SR-22 certificate"),

 "underage-sr22-tennessee": ("Under 21",
    f'  <text x="60" y="212" fill="{AMBER}" font-family="Georgia,serif" font-size="96">.02</text>'
    + label(60, 254, "Tennessee threshold under 21", MUTED)
    + car(330, 186, .62, PAPER) + road(330, 312),
    "The figure .02 beside a car, for Tennessee's under-21 alcohol threshold"),

 "sr22-driving-without-insurance": ("Driving uninsured",
    cert(96, 122, "NONE", 168, 176, False)
    + shield(460, 196, AMBER, True, .6)
    + label(52, 330, "Get compliant, then keep it continuous"),
    "An empty certificate beside a shield, for driving without insurance"),

 "sr22-points-and-repeat-violations": ("Points add up",
    bars(96, 292, [46, 78, 112, 148, 186]) + clock(486, 190, 56)
    + label(96, 322, "Accumulation triggers a suspension"),
    "Rising bars beside a clock, for accumulated points and violations"),

 "sr22-reckless-driving-racing-hit-and-run": ("Serious violations",
    f'  <path d="M96 250 L196 122 L296 250 Z" fill="none" stroke="{RED}" stroke-width="9" stroke-linejoin="round"/>'
    f'  <line x1="196" y1="168" x2="196" y2="206" stroke="{RED}" stroke-width="9" stroke-linecap="round"/>'
    f'  <circle cx="196" cy="228" r="6" fill="{RED}"/>'
    + cert(400, 122, "SR-22", 150, 176)
    + label(52, 330, "Longer revocation, longer filing"),
    "A warning triangle beside an SR-22 certificate"),

 "sr22-unsatisfied-judgment": ("Unpaid judgment",
    gavel(170, 172, 1.0)
    + f'  <g transform="translate(392,140)"><rect width="164" height="112" rx="12" fill="{PAPER}"/>'
    f'<rect x="20" y="24" width="120" height="11" rx="5.5" fill="{NAVY_1}" fill-opacity=".26"/>'
    f'<rect x="20" y="46" width="86" height="9" rx="4.5" fill="{NAVY_1}" fill-opacity=".18"/>'
    f'<text x="20" y="90" fill="{RED}" font-family="system-ui,sans-serif" font-size="22" font-weight="800">UNPAID</text></g>'
    + label(52, 330, "Registration and licence both affected"),
    "A gavel beside an unpaid judgment document"),

 "out-of-state-sr22": ("Across state lines",
    f'  <path d="M96 190h132l16 30H96z" fill="#FFF" fill-opacity=".16"/>'
    f'  <path d="M392 190h132l16 30H392z" fill="{AMBER}" fill-opacity=".28"/>'
    + label(96, 262, "HOME STATE", MUTED, 15) + label(392, 262, "TENNESSEE", AMBER, 15)
    + f'  <path d="M268 176h84" stroke="{AMBER}" stroke-width="4" stroke-linecap="round"/>'
    f'  <path d="M338 164l16 12-16 12" fill="none" stroke="{AMBER}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
    "Two states with an arrow between them, for out-of-state filings"),

 "same-day-sr22-filing": ("Filed today",
    clock(160, 196, 68) + cert(392, 120, "SENT", 150, 176)
    + f'  <path d="M252 196h96" stroke="{AMBER}" stroke-width="4" stroke-dasharray="10 8" stroke-linecap="round"/>'
    + label(52, 330, "Transmitted electronically, usually same business day"),
    "A clock with an arrow to a transmitted certificate"),

 "sr22-payment-plans": ("Pay monthly",
    bars(96, 292, [64, 64, 64, 64, 64]) + clock(486, 186, 54)
    + label(96, 322, "Low down payment, monthly instalments"),
    "Even monthly instalment bars beside a clock"),

 "full-coverage-with-sr22": ("Full coverage",
    car(140, 168, .74) + shield(506, 190, AMBER, True, .62)
    + chip(52, 292, "COMPREHENSIVE", AMBER, 220) + chip(292, 292, "COLLISION", BLUE, 180),
    "A car and shield with comprehensive and collision labels"),

 "cdl-sr22-insurance": ("CDL holders",
    f'''  <g transform="translate(120,150)">
    <rect x="0" y="20" width="180" height="92" rx="10" fill="{PAPER}"/>
    <path d="M180 48h58l38 40v24h-96z" fill="{PAPER}" fill-opacity=".8"/>
    <circle cx="60" cy="126" r="26" fill="#101828"/><circle cx="60" cy="126" r="11" fill="{MUTED}"/>
    <circle cx="222" cy="126" r="26" fill="#101828"/><circle cx="222" cy="126" r="11" fill="{MUTED}"/>
  </g>''' + shield(516, 190, AMBER, True, .56)
    + label(52, 330, "A suspension is a livelihood problem"),
    "A commercial truck with a shield, for CDL holders"),

 "rideshare-delivery-sr22": ("Rideshare &amp; delivery",
    car(130, 168, .7)
    + f'  <g transform="translate(444,150)"><rect width="120" height="120" rx="26" fill="{PAPER}"/>'
    f'<circle cx="60" cy="46" r="17" fill="{NAVY_3}"/>'
    f'<path d="M28 96c0-19 14-30 32-30s32 11 32 30z" fill="{NAVY_3}"/></g>'
    + label(52, 330, "Platform cover has gaps your policy must fill"),
    "A car beside a passenger icon, for rideshare and delivery drivers"),

 "sr22-removal": ("Getting off SR-22",
    cert(96, 118, "SR-22", 150, 182)
    + f'  <path d="M272 208h96" stroke="{AMBER}" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/>'
    f'  <path d="M354 196l16 12-16 12" fill="none" stroke="{AMBER}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    + shield(486, 200, AMBER, True, .62)
    + label(52, 330, "Verify in e-Services, then re-shop"),
    "A certificate with an arrow to a clear shield, for ending the filing"),

 "motorcycle-and-household-sr22": ("Motorcycle &amp; household",
    f'''  <g transform="translate(120,196)">
    <circle cx="0" cy="40" r="34" fill="none" stroke="{PAPER}" stroke-width="9"/>
    <circle cx="150" cy="40" r="34" fill="none" stroke="{PAPER}" stroke-width="9"/>
    <path d="M0 40l40-52h48l24 32-37 60" fill="none" stroke="{AMBER}" stroke-width="9"
          stroke-linecap="round" stroke-linejoin="round"/>
  </g>''' + car(356, 186, .55, PAPER) + label(52, 330, "One filing, several vehicles"),
    "A motorcycle beside a car, for motorcycle and household policies"),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for i, (slug, (title, art, _alt)) in enumerate(sorted(SERVICES.items())):
        svg = frame(art, i, title)
        with open(os.path.join(OUT, slug + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(svg)
    print("%d service illustrations -> assets/images/services/" % len(SERVICES))
    import config
    missing = [s["slug"] for s in config.SERVICES if s["slug"] not in SERVICES]
    if missing:
        print("NO ARTWORK for:", ", ".join(missing))
    extra = [k for k in SERVICES if k not in {s["slug"] for s in config.SERVICES}]
    if extra:
        print("artwork with no service:", ", ".join(extra))


if __name__ == "__main__":
    main()
