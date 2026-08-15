#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the blog card illustrations.

    python3 make_blog_art.py

Original artwork rather than stock or Places photos: nothing to license, no
attribution line to carry, exact brand palette, sharp at any density, and
each one is actually about its post instead of being a generic photo of a
car. Written as a generator so all eight share one frame and palette — change
FRAME once and every card updates.

Output: assets/images/blog/<slug>.svg  (16:9, ~2KB each)
"""

import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "images", "blog")

W, H = 640, 360

NAVY_1 = "#0B2545"
NAVY_2 = "#16324F"
NAVY_3 = "#1E4166"
AMBER = "#F2B441"
AMBER_D = "#D99A22"
BLUE = "#4E86C4"
PAPER = "#F4F7FB"
MUTED = "#8CA6C4"


def frame(inner, gid):
    """Shared card: navy gradient, faint grid, soft amber glow, hairline edge."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">
  <defs>
    <linearGradient id="bg{gid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{NAVY_2}"/>
      <stop offset="100%" stop-color="{NAVY_1}"/>
    </linearGradient>
    <radialGradient id="glow{gid}" cx="0.78" cy="0.18" r="0.75">
      <stop offset="0%" stop-color="{AMBER}" stop-opacity=".22"/>
      <stop offset="100%" stop-color="{AMBER}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid{gid}" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0v40" fill="none" stroke="#FFFFFF" stroke-opacity=".05" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg{gid})"/>
  <rect width="{W}" height="{H}" fill="url(#grid{gid})"/>
  <rect width="{W}" height="{H}" fill="url(#glow{gid})"/>
{inner}
  <rect x=".5" y=".5" width="{W-1}" height="{H-1}" fill="none" stroke="#FFFFFF" stroke-opacity=".10"/>
</svg>
"""


# ---------------------------------------------------------------- artwork --

def art_how_long():
    """A timeline whose length is variable — the whole point of the post."""
    ticks = "".join(
        f'<line x1="{120 + i*68}" y1="196" x2="{120 + i*68}" y2="212" '
        f'stroke="{MUTED}" stroke-width="3" stroke-linecap="round" opacity=".6"/>'
        for i in range(6))
    return f"""  <text x="120" y="112" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="40">How long?</text>
  <rect x="118" y="150" width="404" height="14" rx="7" fill="#FFFFFF" fill-opacity=".13"/>
  <rect x="118" y="150" width="236" height="14" rx="7" fill="{AMBER}"/>
  <circle cx="354" cy="157" r="17" fill="{AMBER}"/>
  <circle cx="354" cy="157" r="7" fill="{NAVY_1}"/>
  {ticks}
  <text x="120" y="248" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="17">Your suspension</text>
  <text x="120" y="274" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="17">sets the length</text>
  <g opacity=".5">
    <line x1="404" y1="236" x2="512" y2="236" stroke="{MUTED}" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="416" y1="222" x2="500" y2="250" stroke="#E05B4B" stroke-width="3.5" stroke-linecap="round"/>
    <text x="404" y="274" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="17">not 3 years</text>
  </g>"""


def art_dui_reinstatement():
    """Four steps up to a licence card — the sequence the post lays out."""
    steps = ""
    for i in range(4):
        x, y = 96 + i * 58, 268 - i * 34
        steps += (f'<rect x="{x}" y="{y}" width="52" height="{268 - y + 34}" rx="5" '
                  f'fill="#FFFFFF" fill-opacity="{0.10 + i*0.06:.2f}"/>'
                  f'<text x="{x+26}" y="{y+24}" fill="{AMBER}" text-anchor="middle" '
                  f'font-family="system-ui,sans-serif" font-size="18" font-weight="700">{i+1}</text>')
    return f"""  <text x="96" y="86" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="36">Back on the road</text>
{steps}
  <g transform="translate(372,104)">
    <rect width="168" height="106" rx="12" fill="{PAPER}"/>
    <rect x="14" y="16" width="44" height="52" rx="6" fill="{BLUE}" fill-opacity=".45"/>
    <rect x="70" y="18" width="82" height="10" rx="5" fill="{NAVY_1}" fill-opacity=".55"/>
    <rect x="70" y="36" width="66" height="9" rx="4.5" fill="{NAVY_1}" fill-opacity=".3"/>
    <rect x="70" y="52" width="74" height="9" rx="4.5" fill="{NAVY_1}" fill-opacity=".3"/>
    <rect x="14" y="80" width="138" height="10" rx="5" fill="{AMBER}"/>
  </g>
  <path d="M356 246c46-14 84-38 112-70" fill="none" stroke="{AMBER}" stroke-width="3"
        stroke-linecap="round" stroke-dasharray="9 9" opacity=".75"/>"""


def art_restricted_10day():
    """A clock reading ten — the deadline the post is built around."""
    marks = "".join(
        f'<line x1="{460 + 62*__import__("math").cos(__import__("math").radians(a))}" '
        f'y1="{176 + 62*__import__("math").sin(__import__("math").radians(a))}" '
        f'x2="{460 + 72*__import__("math").cos(__import__("math").radians(a))}" '
        f'y2="{176 + 72*__import__("math").sin(__import__("math").radians(a))}" '
        f'stroke="{MUTED}" stroke-width="3" stroke-linecap="round" opacity=".55"/>'
        for a in range(0, 360, 30))
    return f"""  <text x="82" y="120" fill="{AMBER}" font-family="Georgia,serif" font-size="86" font-weight="400">10</text>
  <text x="82" y="164" fill="{PAPER}" font-family="system-ui,sans-serif" font-size="21" font-weight="700" letter-spacing="3">DAYS</text>
  <text x="82" y="212" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="17">from the judge&#8217;s</text>
  <text x="82" y="238" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="17">signature</text>
  <g transform="translate(0,0)">
    <circle cx="460" cy="176" r="86" fill="#FFFFFF" fill-opacity=".07"/>
    <circle cx="460" cy="176" r="86" fill="none" stroke="{AMBER}" stroke-width="4"
            stroke-dasharray="450 90" stroke-linecap="round" transform="rotate(-90 460 176)"/>
    {marks}
    <line x1="460" y1="176" x2="460" y2="122" stroke="{PAPER}" stroke-width="5" stroke-linecap="round"/>
    <line x1="460" y1="176" x2="502" y2="196" stroke="{AMBER}" stroke-width="5" stroke-linecap="round"/>
    <circle cx="460" cy="176" r="7" fill="{PAPER}"/>
  </g>"""


def art_owner_vs_nonowner():
    """Two panels: a car you own, and keys without one."""
    return f"""  <line x1="320" y1="58" x2="320" y2="302" stroke="#FFFFFF" stroke-opacity=".14" stroke-width="2"/>
  <text x="66" y="86" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="15" font-weight="700" letter-spacing="2.5">OWNER</text>
  <text x="368" y="86" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="15" font-weight="700" letter-spacing="2.5">NON-OWNER</text>
  <g transform="translate(60,140) scale(.52)">
    <path fill="{PAPER}" d="M40 128c-13 0-22-8-22-20v-14c0-11 7-19 18-22l52-13 41-32c11-9 24-13 38-13h51c17 0 32 7 43 20l30 34 55 12c15 3 24 13 24 27v1c0 12-9 20-22 20H40z"/>
    <path fill="{NAVY_3}" d="M152 24h47c12 0 22 5 30 14l24 27h-101z"/>
    <path fill="{NAVY_3}" d="M138 25l-11 40H86l32-25c6-5 13-9 20-15z"/>
    <circle cx="112" cy="124" r="31" fill="#101828"/><circle cx="112" cy="124" r="14" fill="{MUTED}"/>
    <circle cx="292" cy="124" r="31" fill="#101828"/><circle cx="292" cy="124" r="14" fill="{MUTED}"/>
  </g>
  <g transform="translate(430,150)">
    <circle cx="0" cy="0" r="26" fill="none" stroke="{AMBER}" stroke-width="9"/>
    <rect x="20" y="-7" width="76" height="14" rx="5" fill="{AMBER}"/>
    <rect x="72" y="5" width="11" height="20" rx="4" fill="{AMBER}"/>
    <rect x="90" y="5" width="11" height="15" rx="4" fill="{AMBER}"/>
  </g>
  <text x="368" y="238" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="27">no car needed</text>
  <text x="66" y="252" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="27">titled to you</text>"""


def art_costs():
    """Four quarterly instalments stepping down a balance."""
    bars = ""
    for i in range(4):
        x = 96 + i * 74
        bars += (f'<rect x="{x}" y="{300 - (58 + i*22)}" width="46" height="{58 + i*22}" rx="7" '
                 f'fill="{AMBER}" fill-opacity="{0.35 + i*0.2:.2f}"/>')
    return f"""  <text x="96" y="92" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="36">Two separate bills</text>
  <text x="96" y="128" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="17">Premium is one. State fees are another.</text>
{bars}
  <line x1="88" y1="302" x2="404" y2="302" stroke="{MUTED}" stroke-width="2.5" opacity=".55"/>
  <text x="96" y="330" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="14" letter-spacing="1.5">QUARTERLY</text>
  <g transform="translate(468,150)">
    <circle cx="0" cy="0" r="58" fill="#FFFFFF" fill-opacity=".08"/>
    <circle cx="0" cy="0" r="58" fill="none" stroke="{AMBER}" stroke-width="4" opacity=".8"/>
    <text x="0" y="14" fill="{AMBER}" text-anchor="middle" font-family="Georgia,serif" font-size="44">$75</text>
    <text x="0" y="86" fill="{MUTED}" text-anchor="middle" font-family="system-ui,sans-serif" font-size="15">per quarter</text>
  </g>"""


def art_lapse():
    """A continuous line that breaks — and the restart it forces."""
    return f"""  <text x="90" y="96" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="36">One missed payment</text>
  <path d="M90 186h146" stroke="{AMBER}" stroke-width="9" stroke-linecap="round"/>
  <path d="M300 186h250" stroke="{MUTED}" stroke-width="9" stroke-linecap="round" stroke-dasharray="4 20" opacity=".55"/>
  <g transform="translate(268,186)">
    <path d="M-24-30 4-6l-22 4 20 34" fill="none" stroke="#E05B4B" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <g transform="translate(90,232)">
    <rect width="212" height="42" rx="21" fill="{AMBER}" fill-opacity=".16"/>
    <text x="22" y="28" fill="{AMBER}" font-family="system-ui,sans-serif" font-size="16" font-weight="700">COVERED</text>
  </g>
  <g transform="translate(330,232)">
    <rect width="220" height="42" rx="21" fill="#E05B4B" fill-opacity=".16"/>
    <text x="22" y="28" fill="#F09A8E" font-family="system-ui,sans-serif" font-size="16" font-weight="700">SUSPENDED AGAIN</text>
  </g>"""


def art_fr44():
    """Three certificates, one of them Tennessee's."""
    docs = ""
    labels = ["SR-22", "FR-44", "SR-50"]
    for i, lab in enumerate(labels):
        x = 74 + i * 172
        on = i == 0
        fill = PAPER if on else "#FFFFFF"
        op = "1" if on else ".13"
        txt = NAVY_1 if on else PAPER
        docs += f"""  <g transform="translate({x},112)">
    <rect width="146" height="176" rx="12" fill="{fill}" fill-opacity="{op}"/>
    <rect x="20" y="26" width="106" height="11" rx="5.5" fill="{txt}" fill-opacity=".28"/>
    <rect x="20" y="48" width="80" height="9" rx="4.5" fill="{txt}" fill-opacity=".2"/>
    <text x="73" y="112" fill="{AMBER if on else MUTED}" text-anchor="middle"
          font-family="system-ui,sans-serif" font-size="26" font-weight="800">{lab}</text>
    <rect x="20" y="136" width="106" height="9" rx="4.5" fill="{txt}" fill-opacity=".18"/>
  </g>"""
    return f"""  <text x="74" y="76" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="34">Only one is Tennessee&#8217;s</text>
{docs}
  <path d="M147 306h0" stroke="{AMBER}" stroke-width="4"/>
  <rect x="74" y="300" width="146" height="5" rx="2.5" fill="{AMBER}"/>"""


def art_moving():
    """Two jurisdictions, an obligation that does not travel."""
    return f"""  <text x="74" y="84" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="34">It belongs to the state</text>
  <text x="74" y="120" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="34">that ordered it</text>
  <g transform="translate(96,170)">
    <path d="M0 20h150l18 34H0z" fill="#FFFFFF" fill-opacity=".16"/>
    <text x="10" y="90" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="16" font-weight="700" letter-spacing="2">HOME STATE</text>
  </g>
  <g transform="translate(388,170)">
    <path d="M0 20h150l18 34H0z" fill="{AMBER}" fill-opacity=".28"/>
    <text x="10" y="90" fill="{AMBER}" font-family="system-ui,sans-serif" font-size="16" font-weight="700" letter-spacing="2">TENNESSEE</text>
  </g>
  <path d="M270 202h96" fill="none" stroke="{AMBER}" stroke-width="4" stroke-linecap="round"/>
  <path d="M352 190l16 12-16 12" fill="none" stroke="{AMBER}" stroke-width="4"
        stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M366 236h-96" fill="none" stroke="{MUTED}" stroke-width="3" stroke-linecap="round"
        stroke-dasharray="7 8" opacity=".6"/>
  <path d="M284 224l-16 12 16 12" fill="none" stroke="{MUTED}" stroke-width="3"
        stroke-linecap="round" stroke-linejoin="round" opacity=".6"/>"""


def d_how_long():
    """Tennessee against the flat-term states, side by side."""
    return f"""  <text x="60" y="76" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="30">Two different designs</text>
  <text x="60" y="126" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="15" letter-spacing="2">FLAT-TERM STATES</text>
  <rect x="60" y="140" width="500" height="18" rx="9" fill="#FFFFFF" fill-opacity=".16"/>
  <text x="574" y="155" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="14" text-anchor="end">3 yrs</text>
  <text x="60" y="212" fill="{AMBER}" font-family="system-ui,sans-serif" font-size="15" letter-spacing="2">TENNESSEE</text>
  <rect x="60" y="226" width="500" height="18" rx="9" fill="#FFFFFF" fill-opacity=".10"/>
  <rect x="60" y="226" width="196" height="18" rx="9" fill="{AMBER}"/>
  <rect x="60" y="264" width="500" height="18" rx="9" fill="#FFFFFF" fill-opacity=".10"/>
  <rect x="60" y="264" width="342" height="18" rx="9" fill="{AMBER}" fill-opacity=".75"/>
  <text x="60" y="318" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="15">Each bar is one driver&#8217;s revocation</text>"""


def d_dui():
    """Who has to clear you, in order."""
    rows = [("COURT", "clears the conviction"), ("CARRIER", "files the SR-22"),
            ("STATE", "processes reinstatement")]
    out = ""
    for i, (a, b) in enumerate(rows):
        y = 122 + i * 74
        out += f"""  <circle cx="88" cy="{y}" r="20" fill="{AMBER}" fill-opacity=".22"/>
  <text x="88" y="{y+6}" fill="{AMBER}" text-anchor="middle" font-family="system-ui,sans-serif" font-size="16" font-weight="800">{i+1}</text>
  <text x="128" y="{y-2}" fill="{PAPER}" font-family="system-ui,sans-serif" font-size="17" font-weight="700" letter-spacing="1.5">{a}</text>
  <text x="128" y="{y+20}" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="15">{b}</text>"""
        if i < 2:
            out += f'  <line x1="88" y1="{y+22}" x2="88" y2="{y+52}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="4 5" opacity=".6"/>'
    return f'  <text x="60" y="72" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="30">Three gatekeepers, in order</text>' + out


def d_restricted():
    """What you must have in hand on the day."""
    items = ["Certified court order, signed", "SR-22 already in force",
             "Interlock record transmitted", "Fees"]
    out = ""
    for i, t in enumerate(items):
        y = 128 + i * 52
        out += f"""  <rect x="60" y="{y-24}" width="30" height="30" rx="8" fill="{AMBER}" fill-opacity=".2"/>
  <path d="M68 {y-10} l7 8 12-15" fill="none" stroke="{AMBER}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="106" y="{y-2}" fill="{PAPER}" font-family="system-ui,sans-serif" font-size="17">{t}</text>"""
    return (f'  <text x="60" y="76" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="30">Walk in with all four</text>'
            + out + f'  <text x="60" y="344" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="14">Full-service centre only</text>')


def d_owner():
    """A decision tree in three questions."""
    return f"""  <text x="60" y="72" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="30">Which one do you need?</text>
  <text x="60" y="126" fill="{PAPER}" font-family="system-ui,sans-serif" font-size="17">Is a vehicle titled to you?</text>
  <g transform="translate(60,146)">
    <rect width="150" height="44" rx="10" fill="{AMBER}" fill-opacity=".2"/>
    <text x="20" y="28" fill="{AMBER}" font-family="system-ui,sans-serif" font-size="15" font-weight="700">YES → OWNER</text>
  </g>
  <text x="60" y="236" fill="{PAPER}" font-family="system-ui,sans-serif" font-size="17">One at your address you drive?</text>
  <g transform="translate(60,256)">
    <rect width="216" height="44" rx="10" fill="#FFFFFF" fill-opacity=".12"/>
    <text x="20" y="28" fill="{PAPER}" font-family="system-ui,sans-serif" font-size="15" font-weight="700">PROBABLY OWNER — ASK</text>
  </g>
  <g transform="translate(340,146)">
    <rect width="240" height="154" rx="14" fill="{AMBER}" fill-opacity=".14"/>
    <text x="24" y="46" fill="{AMBER}" font-family="system-ui,sans-serif" font-size="15" font-weight="700">NEITHER?</text>
    <text x="24" y="84" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="26">Non-owner</text>
    <text x="24" y="118" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="14">Usually the cheapest</text>
    <text x="24" y="138" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="14">route to reinstatement</text>
  </g>"""


def d_costs():
    """The state's plan, stated plainly."""
    return f"""  <text x="60" y="76" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="30">The state&#8217;s instalment plan</text>
  <g transform="translate(60,116)">
    <rect width="240" height="92" rx="14" fill="#FFFFFF" fill-opacity=".10"/>
    <text x="22" y="40" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="14" letter-spacing="1.5">ELIGIBLE IF YOU OWE</text>
    <text x="22" y="74" fill="{PAPER}" font-family="Georgia,serif" font-size="28">more than $75</text>
  </g>
  <g transform="translate(320,116)">
    <rect width="240" height="92" rx="14" fill="{AMBER}" fill-opacity=".16"/>
    <text x="22" y="40" fill="{AMBER}" font-family="system-ui,sans-serif" font-size="14" letter-spacing="1.5">DOWN PAYMENT</text>
    <text x="22" y="74" fill="{PAPER}" font-family="Georgia,serif" font-size="28">$25</text>
  </g>
  <g transform="translate(60,228)">
    <rect width="240" height="92" rx="14" fill="{AMBER}" fill-opacity=".16"/>
    <text x="22" y="40" fill="{AMBER}" font-family="system-ui,sans-serif" font-size="14" letter-spacing="1.5">THEN EACH QUARTER</text>
    <text x="22" y="74" fill="{PAPER}" font-family="Georgia,serif" font-size="28">$75</text>
  </g>
  <g transform="translate(320,228)">
    <rect width="240" height="92" rx="14" fill="#FFFFFF" fill-opacity=".10"/>
    <text x="22" y="40" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="14" letter-spacing="1.5">OVER A TERM OF</text>
    <text x="22" y="74" fill="{PAPER}" font-family="Georgia,serif" font-size="28">up to 60 months</text>
  </g>"""


def d_lapse():
    """How lapses actually happen, ranked."""
    causes = [("Card on file expires", 100), ("Renewal price rises", 78),
              ("Cancelled on assumption", 60), ("Switched carrier, no filing", 44)]
    out = ""
    for i, (t, w) in enumerate(causes):
        y = 122 + i * 56
        out += f"""  <rect x="60" y="{y}" width="{w*4.4:.0f}" height="26" rx="13" fill="{AMBER}" fill-opacity="{0.5 - i*0.09:.2f}"/>
  <text x="72" y="{y+18}" fill="{PAPER}" font-family="system-ui,sans-serif" font-size="15">{t}</text>"""
    return (f'  <text x="60" y="76" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="30">How lapses actually happen</text>'
            + out + f'  <text x="60" y="348" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="14">Almost never on purpose</text>')


def d_fr44():
    """Which state uses what."""
    return f"""  <text x="60" y="76" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="30">Who uses which</text>
  <g transform="translate(60,116)">
    <rect width="230" height="118" rx="14" fill="{AMBER}" fill-opacity=".16"/>
    <text x="22" y="42" fill="{AMBER}" font-family="system-ui,sans-serif" font-size="22" font-weight="800">SR-22</text>
    <text x="22" y="74" fill="{PAPER}" font-family="system-ui,sans-serif" font-size="15">Tennessee, and most</text>
    <text x="22" y="96" fill="{PAPER}" font-family="system-ui,sans-serif" font-size="15">other states</text>
  </g>
  <g transform="translate(320,116)">
    <rect width="240" height="118" rx="14" fill="#FFFFFF" fill-opacity=".10"/>
    <text x="22" y="42" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="22" font-weight="800">FR-44</text>
    <text x="22" y="74" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="15">Higher limits — Florida</text>
    <text x="22" y="96" fill="{MUTED}" font-family="system-ui,sans-serif" font-size="15">and Virginia</text>
  </g>
  <g transform="translate(60,254)">
    <rect width="500" height="76" rx="14" fill="#FFFFFF" fill-opacity=".06"/>
    <text x="22" y="34" fill="{PAPER}" font-family="system-ui,sans-serif" font-size="15">The only check that settles it for you:</text>
    <text x="22" y="58" fill="{AMBER}" font-family="system-ui,sans-serif" font-size="15" font-weight="700">your reinstatement requirements in e-Services</text>
  </g>"""


def d_moving():
    """The sequence for either direction."""
    steps = ["Pull your Tennessee requirements",
             "Ask the other state, in writing",
             "Place cover that satisfies both",
             "Cancel nothing until both are clear"]
    out = ""
    for i, t in enumerate(steps):
        y = 126 + i * 56
        out += f"""  <circle cx="82" cy="{y-6}" r="17" fill="{AMBER}" fill-opacity=".2"/>
  <text x="82" y="{y}" fill="{AMBER}" text-anchor="middle" font-family="system-ui,sans-serif" font-size="15" font-weight="800">{i+1}</text>
  <text x="118" y="{y}" fill="{PAPER}" font-family="system-ui,sans-serif" font-size="17">{t}</text>"""
    return (f'  <text x="60" y="76" fill="{PAPER}" font-family="Georgia,serif" font-style="italic" font-size="30">Either direction, same order</text>' + out)


DIAGRAM = {
    "how-long-sr22-tennessee": (d_how_long,
        "Bar comparison showing flat three-year states against Tennessee, "
        "where each driver's filing matches their own revocation"),
    "tennessee-license-reinstatement-after-dui": (d_dui,
        "Three numbered gatekeepers: the court clears the conviction, the "
        "carrier files the SR-22, the state processes reinstatement"),
    "restricted-license-tennessee-sr22": (d_restricted,
        "Checklist of the four things to bring: signed court order, SR-22 in "
        "force, transmitted interlock record, and fees"),
    "owner-vs-non-owner-sr22": (d_owner,
        "Decision tree: a vehicle titled to you means an owner's policy, "
        "neither means a non-owner policy"),
    "tennessee-reinstatement-fees-payment-plan": (d_costs,
        "The state instalment plan: eligible over $75, $25 down, $75 each "
        "quarter, up to 60 months"),
    "sr22-lapse-tennessee": (d_lapse,
        "Ranked causes of a lapse, led by an expired card on file"),
    "sr22-fr44-sr50-difference": (d_fr44,
        "SR-22 used by Tennessee against FR-44 used by Florida and Virginia"),
    "moving-with-sr22-tennessee": (d_moving,
        "Four ordered steps for moving into or out of Tennessee with a filing"),
}


ART = {
    "how-long-sr22-tennessee": (art_how_long,
        "A timeline bar whose length varies, marked to show a Tennessee SR-22 "
        "runs as long as the suspension rather than a flat three years"),
    "tennessee-license-reinstatement-after-dui": (art_dui_reinstatement,
        "Four numbered steps rising toward a reinstated driver licence"),
    "restricted-license-tennessee-sr22": (art_restricted_10day,
        "A clock beside the number 10, for the ten-day restricted licence "
        "deadline"),
    "owner-vs-non-owner-sr22": (art_owner_vs_nonowner,
        "A split panel: a car on the owner side, keys alone on the non-owner "
        "side"),
    "tennessee-reinstatement-fees-payment-plan": (art_costs,
        "Quarterly instalment bars beside a $75 per-quarter marker"),
    "sr22-lapse-tennessee": (art_lapse,
        "An unbroken coverage line that snaps, turning into a suspension"),
    "sr22-fr44-sr50-difference": (art_fr44,
        "Three certificate cards with SR-22 highlighted as the Tennessee one"),
    "moving-with-sr22-tennessee": (art_moving,
        "Two states with an arrow between them, showing the filing obligation "
        "stays with the ordering state"),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for i, (slug, (fn, _alt)) in enumerate(sorted(ART.items())):
        with open(os.path.join(OUT, slug + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(frame(fn(), i))
        n += 1
    for i, (slug, (fn, _alt)) in enumerate(sorted(DIAGRAM.items())):
        with open(os.path.join(OUT, slug + "-fig.svg"), "w", encoding="utf-8") as fh:
            fh.write(frame(fn(), 100 + i))
        n += 1
    print("%d blog images (%d headers + %d diagrams) -> assets/images/blog/"
          % (n, len(ART), len(DIAGRAM)))


if __name__ == "__main__":
    main()
