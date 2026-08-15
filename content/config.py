# -*- coding: utf-8 -*-
"""
Data for sr22carinsurancenashvilletn.com.

Every fact in CITIES / TN_FACTS is verified against a primary source; the
`source` fields say which. Anything unverified is omitted rather than guessed.

PLACEHOLDERS: the agency behind this site is not yet named. Business identity
fields below are deliberately bracketed tokens. validate.py counts them; it
does NOT fail on them, because shipping bracket tokens is the agreed plan
until the agency is signed. Never replace them with invented values --
insurance advertising is regulated by the TN Dept of Commerce & Insurance and
a producer license number is a checkable claim.
"""

# ---------------------------------------------------------------- business --

# PREVIEW mode: the site is deployed for review before an agency is named, so
# every page carries robots noindex and robots.txt disallows everything. A
# public, indexable insurance site with placeholder license numbers is not
# something to leave sitting in Google's index. Flip to False at real launch.
PREVIEW = True

SITE = {
    "domain": "sr22carinsurancenashvilletn.com",
    "base_url": "https://sr22carinsurancenashvilletn.com",
    "name": "[AGENCY NAME]",
    "short_name": "[AGENCY NAME]",
    "tagline": "SR-22 filings for Nashville and Middle Tennessee drivers",
    "phone_display": "[PHONE]",
    "phone_href": "[PHONE-E164]",          # e.g. +16155550123
    "text_display": "[TEXT NUMBER]",
    "email": "[EMAIL]",
    "street": "159 4th Ave N",
    "city": "Nashville",
    "region": "TN",
    "postal": "37219",
    "hours": "[HOURS]",
    "license": "[TN PRODUCER LICENSE #]",
    "agent_name": "[AGENT NAME]",
    "agent_title": "Licensed Tennessee Insurance Producer",
    "agent_bio": "[AGENT BIO]",   # 2-3 sentences: years licensed, what they
                                  # handle, why they do SR-22 work
    # Where the quote form posts. The template's PHP mailer was deleted -- it
    # was hardcoded to your@email.com and validated turf service categories,
    # so every submission from this form would have been rejected. Point this
    # at the real lead destination (GHL webhook, n8n, form service) before
    # launch; validate_site.py fails while it is still a placeholder.
    "form_endpoint": "/quote-not-connected.html",
    "last_updated": "2026-08-13",
    # Filled in only when the real Google Business Profile exists. Empty keys
    # are skipped by the schema builder -- do not invent coordinates, ratings,
    # or social URLs.
    "geo": {},
    "same_as": [],
}

# Bracketed tokens that are expected in output. Anything bracketed and NOT in
# this list is a generator bug, not a business placeholder.
KNOWN_PLACEHOLDERS = [
    "[AGENCY NAME]", "[PHONE]", "[PHONE-E164]", "[TEXT NUMBER]", "[EMAIL]",
    "[HOURS]", "[TN PRODUCER LICENSE #]",
    "[AGENT NAME]", "[AGENT BIO]", "[FORM ENDPOINT URL]",
]

# ------------------------------------------------------- verified TN facts --

SOURCES = {
    "fr": ("Tennessee Department of Safety and Homeland Security -- "
           "Do I need SR-22 Insurance?",
           "https://safetysupport.tn.gov/hc/en-us/articles/29263753232403-Do-I-need-SR-22-Insurance"),
    "reinstate": ("Tennessee Department of Safety and Homeland Security -- Reinstatements",
                  "https://www.tn.gov/safety/driver-services/reinstatements-and-moving-violations/reinstatements.html"),
    "installment": ("Tennessee Department of Safety and Homeland Security -- "
                    "Payment Plan for Reinstatement Fees",
                    "https://www.tn.gov/safety/driver-services/reinstatements-and-moving-violations/reinstatements/frinstallment.html"),
    "locations": ("Tennessee Department of Safety and Homeland Security -- "
                  "Driver Service Locations and Appointments",
                  "https://www.tn.gov/safety/driver-services/locations.html"),
    "statute_114": ("T.C.A. Sec. 55-12-114",
                    "https://law.justia.com/codes/tennessee/title-55/chapter-12/part-1/section-55-12-114/"),
    "eservices": ("Tennessee Department of Safety e-Services",
                  "https://tnpublicsafetyapp.tn.gov/eServices/"),
    "courts": ("Tennessee Administrative Office of the Courts -- court locator",
               "https://www.tncourts.gov/courts"),
    "interlock": ("Tennessee Department of Safety and Homeland Security -- "
                  "Ignition Interlock (Breath Alcohol Device)",
                  "https://www.tn.gov/safety/driver-services/reinstatements-and-moving-violations/ignition-interlock.html"),
    "restricted": ("Tennessee Department of Safety and Homeland Security -- "
                   "Restricted License Information",
                   "https://www.tn.gov/safety/driver-services/reinstatements-and-moving-violations/reinstatements/frrestricteddl.html"),
    "census": ("U.S. Census Bureau, 2020 Decennial Census", ""),
}

# Each entry: (label, claim, source key). These are the load-bearing GEO
# claims -- the whole strategy is that this site agrees with tn.gov. The label
# is what makes the block quotable: an assistant lifting "How long you need
# it" gets a self-contained answer.
TN_FACTS = [
    ("Who files it",
     "The policy must be filed electronically with the department by an "
     "insurance company licensed through the Tennessee Department of "
     "Commerce and Insurance to issue motor vehicle liability coverage in "
     "Tennessee. You cannot file it yourself.", "fr"),
    ("How long you need it",
     "Tennessee requires the SR-22 to be maintained for the length of your "
     "suspension or revocation period. A one-year revocation means a "
     "one-year SR-22 requirement -- Tennessee does not apply a flat "
     "three-year rule the way many other states do.", "fr"),
    ("When it starts",
     "The SR-22 can be maintained while you hold a restricted license, or "
     "beginning at reinstatement.", "fr"),
    ("What happens if it lapses",
     "If the policy is canceled or terminated before the requirement is "
     "complete, your driving privileges can be suspended again for Failure "
     "to Maintain Future Proof of Financial Responsibility. You would then "
     "have to refile the SR-22, pay reinstatement fees again, and reapply.",
     "fr"),
    ("How to check whether you still need one",
     "Open your reinstatement requirements in the Department of Safety "
     "e-Services portal. If SR22 is not listed among your requirements, you "
     "are no longer required to carry it.", "fr"),
]

# Tennessee minimum liability limits. 25/50/25 is long-standing and widely
# published, but we cite the statute rather than a rate-comparison site.
TN_MINIMUMS = {
    "bi_person": "$25,000",
    "bi_accident": "$50,000",
    "pd": "$25,000",
    "shorthand": "25/50/25",
    "cite": "T.C.A. Sec. 55-12-102",
}

# Verified on the Department of Safety installment page.
PAYMENT_PLAN = {
    "eligibility": "You must owe more than $75 in reinstatement fees and meet "
                   "all other reinstatement requirements.",
    "down": "$25 administrative fee due when you enter the plan",
    "installment": "$75 every quarter (every three months)",
    "term": "up to 60 months to clear the balance",
    "source": "installment",
}

MAIL = {
    "usps": ["Tennessee Department of Safety and Homeland Security",
             "Financial Responsibility", "PO Box 945", "Nashville, TN 37202"],
    "courier": ["Tennessee Department of Safety and Homeland Security",
                "Financial Responsibility", "1150 Foster Ave.",
                "Nashville, TN 37210"],
    "note": "Courier deliveries (UPS, FedEx, DHL) go to the Foster Ave. "
            "address. Allow up to 5 business days for document review.",
    "source": "reinstate",
}

# Straight from the department's SR-22 article — their list, their wording.
#
# The GROUPING below is ours, not the department's, and the page says so. It
# exists because a flat list of fifteen items answers "what triggers an SR-22"
# but not "which one am I", which is the question a worried driver actually
# arrives with. Every item from the published list appears exactly once.
VIOLATION_GROUPS = [
    {
        "key": "impairment",
        "title": "Alcohol and impairment",
        "icon": "fa-wine-bottle",
        "note": "The most common route into the SR-22 system, and the one "
                "most likely to bring an ignition interlock requirement with "
                "it.",
        "items": [
            "DUI",
            "Implied consent violation or refusing testing",
            "Underage driving while impaired",
            "Driving while in possession of methamphetamine",
        ],
    },
    {
        "key": "record",
        "title": "Your driving record",
        "icon": "fa-list-ol",
        "note": "No single dramatic event — these build up, which is why the "
                "requirement often surprises people.",
        "items": [
            "Accumulation of points or convictions",
            "Two reckless driving violations within a 12-month period",
            "Speed contests or racing",
        ],
    },
    {
        "key": "financial",
        "title": "Money owed after a crash",
        "icon": "fa-scale-balanced",
        "note": "You may not have been convicted of anything. An uninsured "
                "accident or an unpaid judgment is enough on its own.",
        "items": [
            "Accident claims",
            "Unsatisfied judgments",
        ],
    },
    {
        "key": "serious",
        "title": "Serious and felony offences",
        "icon": "fa-triangle-exclamation",
        "note": "Longer revocations, and because Tennessee ties the filing to "
                "the revocation, longer SR-22 periods.",
        "items": [
            "Hit and run (all severity levels)",
            "Felony reckless endangerment by vehicle",
            "Vehicular assault or aggravated vehicular assault",
            "Vehicular homicide, manslaughter, or aggravated vehicular homicide",
            "Using a motor vehicle in the commission of a felony",
            "Theft of a vehicle",
        ],
    },
]

# Flat list kept for llms.txt and anywhere the grouping is not wanted.
VIOLATIONS = [i for g in VIOLATION_GROUPS for i in g["items"]]

# Claims we could NOT confirm on tn.gov. They stay on the site only in hedged
# form, flagged as "confirm with the department" -- never stated as fact.
UNVERIFIED = {
    "out_of_state_waiver":
        "Tennessee publishes an out-of-state waiver process for the ignition "
        "interlock requirement. We were not able to confirm an equivalent "
        "published SR-22 waiver form on tn.gov, so this site tells readers to "
        "confirm directly with the Financial Responsibility office rather "
        "than promising a waiver exists.",
    "filing_fee":
        "The $15-$25 SR-22 filing fee is an industry norm charged by the "
        "carrier, not a state-published figure. Described as 'typically' and "
        "attributed to carriers, never to the state.",
    "rate_ranges":
        "Monthly premium ranges are third-party rate-study estimates. Every "
        "page carrying them also carries RATE_DISCLAIMER.",
}

RATE_DISCLAIMER = ("Rate figures on this page are third-party estimates shown "
                   "for illustration and are not a quote. Your premium is "
                   "determined by the insurance carrier based on your "
                   "individual record. Tennessee does not set the price of "
                   "your insurance.")

COMPLIANCE_NOTE = ("[AGENCY NAME] is a licensed Tennessee insurance agency. "
                   "TN producer license [TN PRODUCER LICENSE #]. We do not "
                   "guarantee rates, approval, or reinstatement timelines.")

# ------------------------------------------------------------------ services --
# slug, title, nav label, icon, summary, body paragraphs
SERVICES = [
    {
        "slug": "owner-sr22-insurance",
        "h1": "Owner SR-22 Insurance in Nashville",
        "nav": "Owner SR-22 Policies",
        "icon": "fa-car",
        "summary": "If you own a vehicle registered in Tennessee, your SR-22 "
                   "attaches to a liability policy on that vehicle.",
        "body": [
            "An owner's SR-22 is the standard filing for a driver who has a "
            "car titled in their name. The certificate rides on top of a "
            "liability policy that meets Tennessee's 25/50/25 minimum, and "
            "the carrier transmits it to the Department of Safety "
            "electronically once the policy binds.",
            "The practical reason to move fast: coverage can start the same "
            "day. If you are trying to clear a reinstatement hold before a "
            "court date, or before a restricted license order expires, the "
            "gap between binding a policy and the state seeing the filing is "
            "the part you control.",
            "We shop carriers that specialize in high-risk drivers rather "
            "than defending one company's rate, and we tell you when a "
            "non-owner policy would be cheaper than what you are asking for.",
        ],
    },
    {
        "slug": "non-owner-sr22-insurance",
        "h1": "Non-Owner SR-22 Insurance in Nashville (No Car Required)",
        "nav": "Non-Owner SR-22",
        "icon": "fa-person-walking",
        "summary": "No vehicle? A non-owner policy still satisfies the state "
                   "filing, and it is usually the cheapest way to reinstate.",
        "body": [
            "This is the option most Nashville drivers do not know exists. If "
            "you do not own a vehicle but still need to satisfy an SR-22 "
            "requirement to reinstate your license, a non-owner policy "
            "provides liability coverage when you drive a car you do not own "
            "-- and it satisfies the Tennessee filing.",
            "It is typically the least expensive path to reinstatement "
            "because there is no vehicle to insure for physical damage. It "
            "fits if you are borrowing family vehicles, driving a company "
            "car, using a car-share, or simply want your license valid again "
            "while you rebuild.",
            "One limit worth stating plainly: a non-owner policy is "
            "liability-only. It does not cover damage to the vehicle you are "
            "driving, and it does not cover a car that is titled to you or "
            "regularly available to you.",
        ],
    },
    {
        "slug": "sr22-after-dui",
        "h1": "SR-22 After a DUI in Nashville",
        "nav": "SR-22 After a DUI",
        "icon": "fa-gavel",
        "summary": "A DUI conviction triggers a revocation, and your SR-22 "
                   "runs as long as that revocation does.",
        "body": [
            "DUI is the first violation the Department of Safety lists as a "
            "reason a Tennessee driver may be required to carry SR-22 "
            "insurance. Because Tennessee ties the filing period to the "
            "length of the revocation rather than a flat three years, the "
            "length of your requirement follows your specific order.",
            "Many carriers will not write a driver after a DUI at all, and "
            "the ones that will often quote very different prices for "
            "identical coverage. Shopping matters more after a DUI than at "
            "any other point in your driving life.",
            "We can coordinate the SR-22 filing with a restricted license "
            "order and an ignition interlock requirement so the pieces line "
            "up and nothing stalls the reinstatement.",
        ],
    },
    {
        "slug": "suspended-license-insurance",
        "h1": "Insurance While Your Tennessee License Is Suspended",
        "nav": "Suspended License Insurance",
        "icon": "fa-id-card",
        "summary": "You can buy a policy while your license is suspended — "
                   "and for most reinstatements, you have to.",
        "sources": ["fr", "restricted", "eservices"],
        "body": [
            "This is one of the most common misunderstandings we hear: that "
            "you cannot buy auto insurance without a valid license. You can, "
            "and in Tennessee the sequence usually requires it. The SR-22 "
            "certificate has to be on file before the state will restore "
            "your driving privileges, which means the policy exists before "
            "the license does.",
            "The same is true of a restricted license. The Department of "
            "Safety requires SR-22 insurance showing the policy is currently "
            "in effect, and is explicit that a standard policy or other "
            "documentation is not acceptable in its place. If you are "
            "planning to drive during your revocation, insurance is one of "
            "the first steps, not the last.",
            "What the policy looks like depends on your situation. If you "
            "still own a vehicle, an owner's policy with the filing attached "
            "keeps the car insured and satisfies the state. If you sold the "
            "car or never had one, a non-owner policy is usually cheaper and "
            "does the same job for the filing.",
            "One thing worth being straight about: a suspended license makes "
            "you a harder risk to place, and some carriers decline outright. "
            "That is exactly why the spread between quotes is widest for "
            "drivers in this position, and why calling one company tells you "
            "very little about what the market will actually do.",
            "If you are not sure whether your suspension even requires a "
            "filing, check before you buy anything. Your reinstatement "
            "requirements page in the Department of Safety e-Services portal "
            "lists what the state wants from you by name. Some suspensions "
            "require an SR-22 and some do not.",
        ],
    },
    {
        "slug": "sr22-with-ignition-interlock",
        "h1": "SR-22 and Ignition Interlock in Tennessee",
        "nav": "SR-22 + Ignition Interlock",
        "icon": "fa-car-battery",
        "summary": "Two separate requirements that have to line up. We handle "
                   "the filing side and help you sequence the rest.",
        "sources": ["interlock", "restricted", "fr"],
        "body": [
            "An ignition interlock device and an SR-22 are different "
            "obligations from different parts of the system, and they run on "
            "different clocks. We do not install interlocks — that is a "
            "certified vendor's job — but the filing has to be coordinated "
            "with the device, and getting the order wrong is what stalls "
            "reinstatements.",
            "Tennessee requires a Breath Alcohol Ignition Interlock Device "
            "for drivers convicted of or pleading guilty to a DUI who want to "
            "keep driving during the revocation, unless a waiver is granted. "
            "The department publishes minimum installation periods by "
            "offense: 365 days for a first DUI, 730 days for a second, 2,190 "
            "days for a third, and 2,920 days for a fourth or subsequent.",
            "Those numbers are the interlock term, not your SR-22 term. Your "
            "filing period matches the length of your suspension or "
            "revocation. The two frequently overlap, and they do not "
            "necessarily end on the same day.",
            "The sequencing that matters: the device has to be installed "
            "before you obtain a restricted license, and the Driver Services "
            "Center will expect proof of installation to have been submitted "
            "electronically into the state's database by your interlock "
            "company — not carried in on paper. The SR-22 has to be in force "
            "at the same time. Miss either and the trip is wasted.",
            "There is also a compliance requirement at the end that costs "
            "people months. During the final 120 days, attempting to start "
            "the vehicle above a .020% breath alcohol reading without a "
            "verified passing retest within ten minutes, skipping rolling "
            "retests, or failing them will restart that 120-day window.",
            "Removal is its own two-step approval. Your manufacturer produces "
            "a compliance determination form, the state reviews your license "
            "status across the interlock period, and if satisfied issues a "
            "letter authorising removal. You take that to a Driver Services "
            "Center for an unrestricted license and give it to the "
            "manufacturer before they will schedule the removal.",
            "If a court has declared you indigent, Tennessee's Electronic "
            "Monitoring Indigency Fund covers interlock services within "
            "published fee caps. That programme is administered by the "
            "Department of Treasury, not the Department of Safety, so it is "
            "a separate conversation from your reinstatement.",
        ],
    },
    {
        "slug": "underage-sr22-tennessee",
        "h1": "SR-22 for Drivers Under 21 in Tennessee",
        "nav": "Drivers Under 21",
        "icon": "fa-user-graduate",
        "summary": "Tennessee's threshold for drivers under 21 is .02, and "
                   "underage driving while impaired is on the state's SR-22 "
                   "list.",
        "sources": ["fr", "restricted", "eservices"],
        "body": [
            "Underage driving while impaired appears on the Department of "
            "Safety's list of violations that can require an SR-22. For "
            "drivers under 21, Tennessee applies a .02 percent alcohol "
            "concentration threshold rather than the .08 that applies to "
            "adults — a practical zero-tolerance standard, and one that "
            "catches young drivers who would not have registered as impaired "
            "under the adult rule.",
            "The insurance consequence is disproportionate, and it is worth "
            "understanding why. A driver at 19 has a short licensing history, "
            "which is already the profile carriers price most "
            "inconsistently. Add a filing requirement and the quotes stop "
            "resembling each other at all. It is routine to see the highest "
            "and lowest offer for the same 19-year-old differ by more than "
            "the annual premium a 40-year-old would pay outright.",
            "That variance is the whole opportunity. Shopping the market "
            "matters more for this driver than for almost anyone else, and a "
            "captive agent can only ever show one answer.",
            "A few situations come up constantly with this age group. If the "
            "driver is on a parent's policy, adding the filing raises the "
            "household premium and the family has a real decision to make "
            "about whether to keep them on it or write them separately. If "
            "the driver is at MTSU, Belmont, Vanderbilt, or TSU without a car "
            "on campus, a non-owner policy often satisfies the requirement "
            "for a fraction of the cost. And if a restricted license is "
            "needed to keep a job or get to class, the SR-22 has to be in "
            "force before the application, with only ten days from the "
            "judge's signature to file it.",
            "The other thing worth saying to a young driver directly: your "
            "requirement runs for the length of your revocation, not a flat "
            "three years, and it ends. Check e-Services the week your "
            "revocation is up, confirm SR22 is gone from your requirements, "
            "and re-shop immediately. Staying on high-risk pricing out of "
            "inertia is how a bad year at 19 turns into an expensive decade.",
        ],
    },
    {
        "slug": "sr22-driving-without-insurance",
        "h1": "SR-22 for Driving Without Insurance in Tennessee",
        "nav": "Driving Uninsured",
        "icon": "fa-file-circle-exclamation",
        "summary": "Tennessee's Financial Responsibility Law requires proof of "
                   "insurance. An uninsured accident claim can put you into "
                   "the SR-22 system.",
        "body": [
            "The Department of Safety lists accident claims among the reasons "
            "a driver may be required to carry SR-22 insurance. An accident "
            "you were involved in without coverage is the version of this "
            "that most often surprises people -- there was no conviction, but "
            "there is now a requirement.",
            "We can get you compliant and filed quickly, and then help you "
            "keep continuous coverage so it does not repeat. Continuity is "
            "the whole game here: a lapse restarts the process.",
        ],
    },
    {
        "slug": "sr22-points-and-repeat-violations",
        "h1": "SR-22 for Points or Repeat Violations in Tennessee",
        "nav": "Points & Repeat Violations",
        "icon": "fa-list-ol",
        "summary": "An accumulation of points or convictions can trigger a "
                   "suspension -- so can two reckless driving violations in "
                   "12 months.",
        "body": [
            "Accumulation of points or convictions appears on the Department "
            "of Safety's list, and so does two reckless driving violations "
            "within a 12-month period. Drivers in this category are usually "
            "shocked by the renewal quote from the carrier they already have.",
            "That reaction is rational, and it is also fixable. Carriers "
            "disagree enormously about how to price a driver with a record. "
            "Re-shopping the whole market is the single highest-value thing "
            "you can do at renewal.",
        ],
    },
    {
        "slug": "sr22-reckless-driving-racing-hit-and-run",
        "h1": "SR-22 for Reckless Driving, Racing, and Hit-and-Run",
        "nav": "Reckless, Racing, Hit-and-Run",
        "icon": "fa-triangle-exclamation",
        "summary": "Serious moving violations carry longer revocations -- "
                   "which, under Tennessee law, means longer SR-22 periods.",
        "body": [
            "Speed contests, leaving the scene, and felony reckless "
            "endangerment by vehicle all appear on the Department of Safety's "
            "SR-22 list. Because the filing period matches the revocation "
            "period, the more serious the order, the longer you carry it.",
            "We handle these filings routinely and will tell you honestly "
            "what a realistic price range looks like before you apply, rather "
            "than quoting you a number that evaporates at underwriting.",
        ],
    },
    {
        "slug": "sr22-unsatisfied-judgment",
        "h1": "SR-22 for an Unsatisfied Judgment in Tennessee",
        "nav": "Unsatisfied Judgment",
        "icon": "fa-scale-balanced",
        "summary": "An unpaid judgment from a motor vehicle accident can "
                   "suspend your license and require future proof of "
                   "financial responsibility.",
        "body": [
            "Unsatisfied judgments are on the department's list. Tennessee "
            "law also addresses the registration side: registrations can be "
            "suspended along with the license, and proof of financial "
            "responsibility is part of getting them back.",
            "We can put the SR-22 side of that in place while you resolve the "
            "judgment itself with the court. The two tracks run in parallel; "
            "neither one waits for the other.",
        ],
    },
    {
        "slug": "out-of-state-sr22",
        "h1": "Out-of-State SR-22 and New Nashville Residents",
        "nav": "Out-of-State Drivers",
        "icon": "fa-map-location-dot",
        "summary": "An SR-22 obligation follows you across state lines. Which "
                   "state needs what is the part worth getting right.",
        "body": [
            "If you moved to Nashville carrying an SR-22 requirement from "
            "another state, that obligation belongs to the state that ordered "
            "it. Satisfying Tennessee does not satisfy them. We can help you "
            "sort out which state needs which filing and place coverage that "
            "works for both.",
            "If you have a Tennessee requirement but now live elsewhere, ask "
            "the Department of Safety's Financial Responsibility office "
            "directly what your options are before you assume the requirement "
            "travels with you or disappears. Tennessee publishes an "
            "out-of-state waiver process for the ignition interlock "
            "requirement; we would rather point you at the department than "
            "promise you a waiver we cannot document.",
            "Tennessee law also addresses residents who move to or return "
            "from another state (T.C.A. Sec. 55-12-114). If that is your "
            "situation, get your requirements in writing from the department "
            "before buying anything.",
        ],
    },
    {
        "slug": "same-day-sr22-filing",
        "h1": "Same-Day SR-22 Filing in Nashville",
        "nav": "Same-Day Filing",
        "icon": "fa-bolt",
        "summary": "Tennessee takes the certificate electronically, so there "
                   "is no reason to wait on the mail.",
        "body": [
            "Because the department requires the filing to come from a "
            "licensed carrier electronically, the certificate can be "
            "transmitted as soon as your policy is issued and paid. Bind in "
            "the morning, filed the same business day, in most cases.",
            "A practical warning about timing: reinstatement work at a "
            "Driver Services Center takes counter time, and centers stop "
            "taking new applicants before their posted closing time. If you "
            "are sitting in the parking lot on Hart Lane trying to clear a "
            "hold today, call us and say so -- but do not cut it close.",
        ],
    },
    {
        "slug": "sr22-payment-plans",
        "h1": "SR-22 Payment Plans and Low Down Payments",
        "nav": "Payment Plans",
        "icon": "fa-credit-card",
        "summary": "SR-22 policies land at a bad financial moment. Low down "
                   "payments and monthly installments exist.",
        "body": [
            "This bill usually arrives right after court costs, fines, and "
            "reinstatement fees. We work with carriers that offer low down "
            "payments and monthly installments so you are not forced to pay "
            "six or twelve months up front.",
            "One detail that quietly costs people money: some carriers charge "
            "the SR-22 filing fee once, and some charge it at every renewal. "
            "We flag which is which before you buy.",
            "Separately, the state has its own installment option for "
            "reinstatement fees, which is not the same thing as a payment "
            "plan on your insurance -- details in the cost section on our "
            "homepage.",
        ],
    },
    {
        "slug": "full-coverage-with-sr22",
        "h1": "Full Coverage With an SR-22",
        "nav": "Full Coverage + SR-22",
        "icon": "fa-shield-halved",
        "summary": "An SR-22 certifies liability only. If you finance or "
                   "lease, your lender still wants comprehensive and "
                   "collision.",
        "body": [
            "The certificate proves liability coverage to the state. It says "
            "nothing about your own car. If there is a lienholder on the "
            "title, they still require comprehensive and collision, and an "
            "SR-22 does not change that.",
            "We build SR-22-compliant policies with full coverage, and we "
            "will raise uninsured motorist coverage with you rather than "
            "leaving it as a checkbox -- it is worth a real conversation in "
            "a state where you may be sharing the road with drivers who are "
            "in the same position you were.",
        ],
    },
    {
        "slug": "cdl-sr22-insurance",
        "h1": "SR-22 for CDL Holders and Commercial Drivers",
        "nav": "CDL & Commercial",
        "icon": "fa-truck",
        "summary": "If you drive for a living in Middle Tennessee, a "
                   "suspension is a livelihood problem, not an inconvenience.",
        "body": [
            "We handle SR-22 filings for CDL holders and for drivers who need "
            "coverage that satisfies both a state filing and an employer's "
            "insurability standard. Those are two different tests and they do "
            "not always have the same answer.",
            "Tell us who your employer is and what their insurability "
            "threshold looks like before we quote. It changes which carriers "
            "are worth approaching.",
        ],
    },
    {
        "slug": "rideshare-delivery-sr22",
        "h1": "SR-22 for Rideshare and Delivery Drivers in Nashville",
        "nav": "Rideshare & Delivery",
        "icon": "fa-taxi",
        "summary": "Uber, Lyft, DoorDash, and Amazon Flex drivers need a "
                   "rideshare endorsement on top of an SR-22-compliant policy.",
        "body": [
            "The platform's commercial coverage does not run continuously. "
            "There are periods -- app on, no passenger or order accepted -- "
            "where your personal policy is doing the work, and a standard "
            "personal policy may exclude exactly that.",
            "We build the rideshare endorsement and the SR-22 filing into one "
            "policy so there is no gap between what the state requires and "
            "what the platform assumes you have.",
        ],
    },
    {
        "slug": "sr22-removal",
        "h1": "SR-22 Removal and Getting Back to Standard Rates",
        "nav": "Getting Off SR-22",
        "icon": "fa-circle-check",
        "summary": "When the requirement clears, you should stop paying "
                   "high-risk rates. We watch for that date.",
        "body": [
            "This is where clients lose the most money, and almost nobody "
            "offers it as a service. When your suspension or revocation "
            "period ends and SR22 drops off your requirements page in "
            "e-Services, there is no longer a reason to carry high-risk "
            "pricing -- but nothing automatically moves you.",
            "We monitor your term, confirm with you that the requirement has "
            "actually cleared, and re-shop you into standard-market pricing "
            "the moment you qualify. Our goal is to stop being your SR-22 "
            "agency as fast as legally possible.",
            "Do not cancel on assumption. Verify in e-Services first, then "
            "cancel. Canceling early is how a completed requirement turns "
            "into a new suspension.",
        ],
    },
    {
        "slug": "motorcycle-and-household-sr22",
        "h1": "Motorcycle, Multi-Vehicle, and Household SR-22 Policies",
        "nav": "Motorcycle & Household",
        "icon": "fa-motorcycle",
        "summary": "Motorcycle liability with a filing, multi-vehicle "
                   "households, and excluded-driver arrangements.",
        "body": [
            "We handle motorcycle liability with SR-22 filings, and "
            "multi-vehicle households where only one driver actually needs "
            "the certificate.",
            "That last case is worth a conversation. Sometimes an excluded "
            "driver arrangement makes more financial sense for the family "
            "than rating everyone off one person's record -- and sometimes it "
            "is a trap, because an excluded driver who drives is uninsured. "
            "We will walk through both sides before you sign anything.",
        ],
    },
]

# ------------------------------------------------------------------- places --
# county-level facts are researched once and reused by every city in the county
COUNTIES = {
    "Davidson": {"court": "Davidson County General Sessions Court"},
    "Williamson": {"court": "Williamson County General Sessions Court"},
    "Rutherford": {"court": "Rutherford County General Sessions Court"},
    "Sumner": {"court": "Sumner County General Sessions Court"},
    "Wilson": {"court": "Wilson County General Sessions Court"},
    "Montgomery": {"court": "Montgomery County General Sessions Court"},
    "Maury": {"court": "Maury County General Sessions Court"},
    "Robertson": {"court": "Robertson County General Sessions Court"},
    "Dickson": {"court": "Dickson County General Sessions Court"},
}

# Driver Services Centers, verified on the department's locations page.
# type: full | express | kiosk. Only `full` centers handle reinstatement.
DSC = {
    "hart-lane": {"name": "Hart Lane Driver Services Center",
                  "addr": "624 Hart Lane, Nashville, TN 37216",
                  "phone": "(615) 532-9780", "type": "full"},
    "downtown-express": {"name": "Nashville Downtown Express Driver Services Center",
                         "addr": "312 Rosa L. Parks Blvd, 3rd Floor, Nashville, TN 37203",
                         "phone": "(615) 253-2061", "type": "express"},
    "hickory-hollow": {"name": "Hickory Hollow Driver Services Center",
                       "addr": "2460 Morris Gentry Blvd., Antioch, TN 37013",
                       "phone": "(615) 770-5701", "type": "full"},
    "metro-center": {"name": "Metro Center Self-Service Kiosk",
                     "addr": "220 French Landing Dr., Nashville, TN 37228",
                     "phone": "(615) 880-9374", "type": "kiosk"},
    "murfreesboro": {"name": "Murfreesboro Driver Services Center",
                     "addr": "1035 Samsonite Blvd., Murfreesboro, TN 37129",
                     "phone": "(615) 898-8036", "type": "full"},
    "murfreesboro-express": {"name": "Murfreesboro Express Driver Services Center",
                             "addr": "3906 Blaze Drive, Murfreesboro, TN 37129",
                             "phone": "(615) 907-4603", "type": "express"},
    "franklin": {"name": "Franklin Driver Services Center",
                 "addr": "3830 Carothers Parkway, Franklin, TN 37067",
                 "phone": "(615) 790-5515", "type": "full"},
    "cool-springs-kiosk": {"name": "AAA Cool Springs Self-Service Kiosk",
                           "addr": "1701 Mallory Lane, Brentwood, TN 37027",
                           "phone": "(629) 221-5786", "type": "kiosk"},
    "gallatin": {"name": "Gallatin Driver Services Center",
                 "addr": "855 N Bluejay Way, Gallatin, TN 37066",
                 "phone": "(615) 230-2995", "type": "full"},
    "lebanon": {"name": "Lebanon Driver Services Center",
                "addr": "204 Maddox Simpson Parkway, Lebanon, TN 37090",
                "phone": "(615) 443-2757", "type": "full"},
    "columbia": {"name": "Columbia Driver Services Center",
                 "addr": "1701 Hampshire Pike, Columbia, TN 38401",
                 "phone": "(931) 380-2548", "type": "full"},
    "dickson": {"name": "Dickson Driver Services Center",
                "addr": "114 West Christi Drive, Dickson, TN 37055",
                "phone": "(615) 441-6218", "type": "full"},
    "springfield": {"name": "Springfield Driver Services Center",
                    "addr": "4676 Highway 41 North, Suite C, Springfield, TN 37172",
                    "phone": "(615) 384-1885", "type": "full"},
    "clarksville-hornbuckle": {"name": "Clarksville (Hornbuckle) Driver Services Center",
                               "addr": "635 Hornbuckle Road, Clarksville, TN 37040",
                               "phone": "(931) 905-2940", "type": "full"},
    "clarksville-dunbar": {"name": "Clarksville (Dunbar Cave) Driver Services Center",
                           "addr": "220 West Dunbar Cave Road, Clarksville, TN 37040",
                           "phone": "(931) 648-5596", "type": "full"},
}

DSC_HOURS = "Monday-Friday, 8:30 a.m. to 5:00 p.m."

# pop = 2020 Decennial Census. `angle` is the local condition that actually
# changes the SR-22 job in that place -- this is what keeps 16 city pages from
# reading as one page with the name swapped.
CITIES = [
    {
        "slug": "nashville", "name": "Nashville", "county": "Davidson",
        "pop": 689447, "places_query": "Downtown Nashville, Tennessee",
        "dsc": ["hart-lane", "downtown-express", "hickory-hollow", "metro-center"],
        "intro": "Nashville is where Tennessee's Financial Responsibility "
                 "office physically sits, which cuts both ways: the "
                 "paperwork path is short, and the Driver Services Centers "
                 "that handle reinstatement are the busiest in the state.",
        "angle": "Davidson County drivers have the most reinstatement "
                 "counter options in Tennessee -- Hart Lane, Hickory Hollow "
                 "in Antioch, and the Downtown Express center -- but only "
                 "the full-service centers process reinstatements, and the "
                 "express location does no testing. Knowing which door to "
                 "walk through saves an afternoon.",
        "commute": "Everything in this metro funnels through I-40, I-24, and "
                   "I-65, and a suspended license in Nashville is not a "
                   "problem you can solve with transit for most work "
                   "schedules. That is usually why the SR-22 becomes urgent.",
    },
    {
        "slug": "franklin", "name": "Franklin", "county": "Williamson",
        "pop": 83454, "places_query": "Downtown Franklin, Tennessee",
        "dsc": ["franklin", "cool-springs-kiosk"],
        "intro": "Franklin drivers file the same certificate as everyone "
                 "else in Tennessee, but they clear their court side in "
                 "Williamson County and their counter side on Carothers "
                 "Parkway.",
        "angle": "The Franklin Driver Services Center on Carothers Parkway "
                 "is full-service, so reinstatement work can be done there "
                 "rather than driving into Davidson County. The Cool Springs "
                 "location at 1701 Mallory Lane is a self-service kiosk -- "
                 "convenient for renewals, not for clearing a hold.",
        "commute": "Williamson County commutes run long and almost entirely "
                   "by car. A suspension here typically means a 30-plus mile "
                   "problem, which is why non-owner policies get "
                   "under-considered locally -- plenty of Franklin drivers "
                   "genuinely do need an owner's filing.",
    },
    {
        "slug": "brentwood", "name": "Brentwood", "county": "Williamson",
        "pop": 45373, "places_query": "Brentwood, Tennessee",
        "dsc": ["cool-springs-kiosk", "franklin"],
        "intro": "Brentwood sits on the Davidson County line, so its drivers "
                 "often have a court matter in one county and a driver "
                 "services trip in another.",
        "angle": "The kiosk at 1701 Mallory Lane in Brentwood is "
                 "self-service. Reinstatements are not processed there -- "
                 "the nearest full-service center is Franklin on Carothers "
                 "Parkway. Assuming the closest location can clear your hold "
                 "is the most common wasted trip in this part of the metro.",
        "commute": "Brentwood households frequently insure several vehicles "
                   "and several drivers on one policy, which makes the "
                   "excluded-driver question live here more often than in "
                   "most of the metro.",
    },
    {
        "slug": "murfreesboro", "name": "Murfreesboro", "county": "Rutherford",
        "pop": 152769, "places_query": "Downtown Murfreesboro, Tennessee",
        "dsc": ["murfreesboro", "murfreesboro-express"],
        "intro": "Murfreesboro is the largest city in Middle Tennessee "
                 "outside Nashville and has its own full-service Driver "
                 "Services Center, so most of a Rutherford County "
                 "reinstatement can be handled locally.",
        "angle": "Two centers, two different jobs: Samsonite Blvd. is "
                 "full-service and handles reinstatement, while the Blaze "
                 "Drive express center does no testing. Rutherford County "
                 "drivers who show up at the wrong one lose a morning.",
        "commute": "A large student population at MTSU means a lot of young "
                   "drivers with short licensing histories, which is exactly "
                   "the profile carriers price most inconsistently. The "
                   "spread between quotes tends to be widest here.",
    },
    {
        "slug": "smyrna", "name": "Smyrna", "county": "Rutherford",
        "pop": 53070, "places_query": "Smyrna, Tennessee",
        "dsc": ["murfreesboro", "murfreesboro-express"],
        "intro": "Smyrna drivers handle their court side in Rutherford "
                 "County and their counter side in Murfreesboro.",
        "angle": "There is no Driver Services Center in Smyrna. The nearest "
                 "full-service option is Murfreesboro on Samsonite Blvd. "
                 "Plan the trip -- and do the insurance filing first, so the "
                 "SR-22 is already showing when you arrive.",
        "commute": "Shift work at the large manufacturing employers here "
                   "makes a suspension an immediate job risk, and it makes "
                   "same-day filing worth more than a slightly lower rate.",
    },
    {
        "slug": "la-vergne", "name": "La Vergne", "county": "Rutherford",
        "pop": 38719, "places_query": "La Vergne, Tennessee",
        "dsc": ["murfreesboro", "hickory-hollow"],
        "intro": "La Vergne sits at the Davidson-Rutherford seam on I-24, "
                 "close enough to Antioch that either county's driver "
                 "services center can be the practical choice.",
        "angle": "La Vergne drivers are roughly equidistant from Hickory "
                 "Hollow in Antioch and the Murfreesboro center on Samsonite "
                 "Blvd. Both are full-service. Your court clearance, though, "
                 "goes through Rutherford County regardless of which counter "
                 "you use.",
        "commute": "This is a heavy I-24 commuter corridor. Uninsured-motorist "
                   "coverage deserves a real look here rather than a reflexive "
                   "decline.",
    },
    {
        "slug": "hendersonville", "name": "Hendersonville", "county": "Sumner",
        "pop": 61753, "places_query": "Hendersonville, Tennessee",
        "dsc": ["gallatin", "hart-lane"],
        "intro": "Hendersonville is Sumner County's largest city, and its "
                 "drivers usually split the difference between the Gallatin "
                 "center and Hart Lane in Nashville.",
        "angle": "The nearest full-service Driver Services Center is "
                 "Gallatin at 855 N Bluejay Way. Sumner County handles the "
                 "court side. Hart Lane in Nashville is the fallback when "
                 "Gallatin's wait is long, but it is a different county's "
                 "counter, not a different set of requirements.",
        "commute": "Long lake-shore commutes into Davidson County make this "
                   "a car-dependent market where non-owner policies rarely "
                   "fit -- most Hendersonville drivers genuinely own the "
                   "vehicle they need to insure.",
    },
    {
        "slug": "gallatin", "name": "Gallatin", "county": "Sumner",
        "pop": 44431, "places_query": "Downtown Gallatin, Tennessee",
        "dsc": ["gallatin"],
        "intro": "Gallatin is the Sumner County seat and has the county's "
                 "full-service Driver Services Center, so court and counter "
                 "are both local.",
        "angle": "855 N Bluejay Way is full-service, which means "
                 "reinstatement fees, payment plans, and document submission "
                 "can all happen in Gallatin. That is genuinely convenient "
                 "and unusual outside the big metro counties.",
        "commute": "Gallatin has grown quickly, and a lot of newer residents "
                   "carry insurance histories from other states. If yours "
                   "does, the out-of-state question is worth resolving "
                   "before you buy anything.",
    },
    {
        "slug": "mount-juliet", "name": "Mount Juliet", "county": "Wilson",
        "pop": 39289, "places_query": "Mount Juliet, Tennessee",
        "dsc": ["lebanon", "hart-lane"],
        "intro": "Mount Juliet sits on the Davidson County line in Wilson "
                 "County, which routinely splits people's court and counter "
                 "trips between two directions.",
        "angle": "The nearest full-service center is Lebanon at 204 Maddox "
                 "Simpson Parkway; Hart Lane in Nashville is the other "
                 "realistic option. Wilson County handles the court side "
                 "either way.",
        "commute": "Mount Juliet is one of the few Middle Tennessee suburbs "
                   "with WeGo Star commuter rail service, which occasionally "
                   "makes a non-owner policy viable for a Nashville "
                   "commuter -- a genuinely rare situation in this metro, "
                   "and worth asking about.",
    },
    {
        "slug": "lebanon", "name": "Lebanon", "county": "Wilson",
        "pop": 38431, "places_query": "Downtown Lebanon, Tennessee",
        "dsc": ["lebanon"],
        "intro": "Lebanon is the Wilson County seat, with the county's "
                 "full-service Driver Services Center on Maddox Simpson "
                 "Parkway.",
        "angle": "Reinstatement work -- paying fees, setting up the state's "
                 "installment plan, submitting documents -- can be done at "
                 "204 Maddox Simpson Parkway rather than driving into "
                 "Davidson County.",
        "commute": "Wilson County's I-40 corridor carries heavy truck "
                   "traffic, and CDL holders here feel a suspension as an "
                   "immediate income problem rather than an inconvenience.",
    },
    {
        "slug": "spring-hill", "name": "Spring Hill", "county": "Maury",
        "pop": 50005, "places_query": "Spring Hill, Tennessee",
        "dsc": ["columbia", "franklin"],
        "intro": "Spring Hill straddles the Maury and Williamson county "
                 "line, which means the answer to 'which county handles my "
                 "case' depends on your address, not your mailing city.",
        "angle": "The city sits in two counties. That matters for the court "
                 "side of a reinstatement, and it changes which Driver "
                 "Services Center is closer -- Columbia on Hampshire Pike or "
                 "Franklin on Carothers Parkway. Confirm which county your "
                 "citation actually came from before you drive anywhere.",
        "commute": "Large-employer shift schedules here make same-day "
                   "filing and evening availability worth more than a small "
                   "premium difference.",
    },
    {
        "slug": "columbia", "name": "Columbia", "county": "Maury",
        "pop": 41690, "places_query": "Downtown Columbia, Tennessee",
        "dsc": ["columbia"],
        "intro": "Columbia is the Maury County seat and has the county's "
                 "full-service Driver Services Center on Hampshire Pike.",
        "angle": "1701 Hampshire Pike is full-service, so Maury County "
                 "drivers can pay reinstatement fees and submit documents "
                 "without leaving the county.",
        "commute": "Columbia sits far enough south that a Nashville-area "
                   "agency without local knowledge tends to treat it as an "
                   "afterthought. The requirements are identical; the "
                   "logistics are not.",
    },
    {
        "slug": "dickson", "name": "Dickson", "county": "Dickson",
        "pop": 16058, "places_query": "Downtown Dickson, Tennessee",
        "dsc": ["dickson"],
        "intro": "Dickson has its own full-service Driver Services Center, "
                 "which is not something every county this size can say.",
        "angle": "114 West Christi Drive is full-service and handles "
                 "reinstatement. Given the distance to Nashville, that is "
                 "the difference between a local errand and a half-day trip.",
        "commute": "Rural mileage means more time on the road per driver and "
                   "a real case for looking hard at liability limits rather "
                   "than defaulting to state minimums.",
    },
    {
        "slug": "springfield", "name": "Springfield", "county": "Robertson",
        "pop": 18782, "places_query": "Downtown Springfield, Tennessee",
        "dsc": ["springfield"],
        "intro": "Springfield is the Robertson County seat, with a "
                 "full-service Driver Services Center on Highway 41 North.",
        "angle": "4676 Highway 41 North, Suite C is full-service. Robertson "
                 "County drivers do not need to drive to Davidson County to "
                 "clear a reinstatement hold.",
        "commute": "Springfield is close enough to the Kentucky line that "
                   "out-of-state filing questions come up regularly. If your "
                   "requirement originated in another state, that state "
                   "still needs its filing.",
    },
    {
        "slug": "clarksville", "name": "Clarksville", "county": "Montgomery",
        "pop": 166722, "places_query": "Downtown Clarksville, Tennessee",
        "dsc": ["clarksville-hornbuckle", "clarksville-dunbar"],
        "intro": "Clarksville is the largest city on this list after "
                 "Nashville, with two full-service Driver Services Centers "
                 "of its own.",
        "angle": "Both Clarksville centers -- Hornbuckle Road and West "
                 "Dunbar Cave Road -- are full-service, so there is no wrong "
                 "door for a reinstatement here. Montgomery County handles "
                 "the court side.",
        "commute": "Fort Campbell means a steady population of drivers "
                   "carrying licenses and insurance histories from other "
                   "states, plus frequent moves. Which state ordered your "
                   "filing is the first question to answer in Clarksville, "
                   "and it is not always Tennessee.",
    },
    {
        "slug": "goodlettsville", "name": "Goodlettsville", "county": "Davidson",
        "pop": 17789, "places_query": "Goodlettsville, Tennessee",
        "dsc": ["hart-lane", "gallatin"],
        "intro": "Goodlettsville is split between Davidson and Sumner "
                 "counties, so which court handles your case depends on "
                 "where in the city you are.",
        "angle": "The city sits in two counties. Hart Lane in Nashville and "
                 "the Gallatin center are both full-service and both "
                 "realistic. The county on your citation, not your mailing "
                 "address, decides the court side.",
        "commute": "This is a heavy I-65 corridor with a lot of "
                   "cross-county driving, which is exactly the pattern that "
                   "produces accumulated-points suspensions.",
    },
]

# Neighborhoods and small communities inside Davidson County. These are not
# census places, so they carry no population figure -- an honest gap. What
# they do carry is a real ZIP, a real nearest center, and a real local angle.
NEIGHBORHOODS = [
    {"slug": "east-nashville", "name": "East Nashville", "zips": "37206, 37216",
     "dsc": "hart-lane", "places_query": "East Nashville, Nashville, Tennessee",
     "angle": "Hart Lane is the closest full-service reinstatement center to "
              "East Nashville, which makes this one of the few parts of the "
              "county where the counter is genuinely a short trip."},
    {"slug": "antioch", "name": "Antioch", "zips": "37013",
     "dsc": "hickory-hollow", "places_query": "Antioch, Nashville, Tennessee",
     "angle": "The Hickory Hollow Driver Services Center at 2460 Morris "
              "Gentry Blvd. is in Antioch itself and is full-service, so "
              "reinstatement work does not require crossing the county."},
    {"slug": "donelson", "name": "Donelson", "zips": "37214",
     "dsc": "hart-lane", "places_query": "Donelson, Nashville, Tennessee",
     "angle": "Donelson's airport-adjacent employment base runs on shift "
              "schedules, which is where a same-day electronic filing is "
              "worth more than a marginally cheaper premium."},
    {"slug": "hermitage", "name": "Hermitage", "zips": "37076",
     "dsc": "hickory-hollow", "places_query": "Hermitage, Nashville, Tennessee",
     "angle": "Hermitage sits near the Wilson County line, so drivers here "
              "sometimes have a Davidson County counter trip and a Wilson "
              "County court matter at the same time."},
    {"slug": "madison", "name": "Madison", "zips": "37115",
     "dsc": "hart-lane", "places_query": "Madison, Nashville, Tennessee",
     "angle": "Madison is close to both Hart Lane and the Goodlettsville "
              "line, and it is one of the easier parts of the county from "
              "which to reach a full-service reinstatement counter."},
    {"slug": "bellevue", "name": "Bellevue", "zips": "37221",
     "dsc": "hart-lane", "places_query": "Bellevue, Nashville, Tennessee",
     "angle": "Bellevue is on the far west side of Davidson County. Hart "
              "Lane is a real drive from here, and the Dickson center is "
              "sometimes closer -- worth checking before you commit an "
              "afternoon."},
    {"slug": "green-hills", "name": "Green Hills", "zips": "37215",
     "dsc": "downtown-express", "places_query": "Green Hills, Nashville, Tennessee",
     "angle": "The Downtown Express center is the nearest driver services "
              "location, but it is express -- no testing, and not the place "
              "to clear a reinstatement hold. Hart Lane is the full-service "
              "option."},
    {"slug": "berry-hill", "name": "Berry Hill", "zips": "37204",
     "dsc": "downtown-express", "places_query": "Berry Hill, Tennessee",
     "angle": "Berry Hill is its own incorporated city inside Davidson "
              "County, with a 2020 census population of 2,112. Small as it "
              "is, its drivers use the same Davidson County courts and "
              "centers as the rest of the county."},
    {"slug": "old-hickory", "name": "Old Hickory", "zips": "37138",
     "dsc": "hickory-hollow", "places_query": "Old Hickory, Tennessee",
     "angle": "Old Hickory sits at the Davidson-Wilson-Sumner junction, "
              "which is the most common place in the metro to be genuinely "
              "unsure which county issued your citation."},
    {"slug": "whites-creek", "name": "Whites Creek", "zips": "37189",
     "dsc": "hart-lane", "places_query": "Whites Creek, Tennessee",
     "angle": "Whites Creek is rural north Davidson County. Hart Lane is the "
              "nearest full-service center, and there is no realistic "
              "transit alternative while a license is suspended."},
    {"slug": "inglewood", "name": "Inglewood", "zips": "37216",
     "dsc": "hart-lane", "places_query": "Inglewood, Nashville, Tennessee",
     "angle": "Inglewood shares the 37216 ZIP with the Hart Lane center "
              "itself -- about as close as a Nashville driver gets to the "
              "reinstatement counter."},
    {"slug": "germantown", "name": "Germantown", "zips": "37208",
     "dsc": "downtown-express", "places_query": "Germantown, Nashville, Tennessee",
     "angle": "Germantown is walkable in a way most of this metro is not, "
              "which makes it one of the few neighborhoods where a "
              "non-owner SR-22 policy is a realistic long-term answer "
              "rather than a stopgap."},
    {"slug": "the-gulch", "name": "The Gulch", "zips": "37203",
     "dsc": "downtown-express", "places_query": "The Gulch, Nashville, Tennessee",
     "angle": "The Gulch shares the 37203 ZIP with the Downtown Express "
              "center on Rosa L. Parks Blvd. That center handles renewals "
              "and updates but not testing -- reinstatement means Hart Lane."},
]

# --------------------------------------------------------------------- FAQ --
FAQ = [
    ("How long do I need SR-22 insurance in Tennessee?",
     "For the length of your suspension or revocation period. The Tennessee "
     "Department of Safety states this directly: a one-year revocation "
     "creates a one-year SR-22 requirement. Tennessee does not apply a "
     "universal three-year rule the way many other states do."),
    ("Can I file an SR-22 myself?",
     "No. The policy must be filed electronically with the department by an "
     "insurance company licensed through the Tennessee Department of "
     "Commerce and Insurance to issue motor vehicle liability coverage in "
     "Tennessee."),
    ("Do I need an SR-22 if I don't own a car?",
     "Often yes -- and a non-owner SR-22 policy is the answer. It satisfies "
     "the state filing and covers your liability when you drive vehicles you "
     "do not own. It is typically the least expensive way to reinstate, "
     "because there is no vehicle to insure for physical damage."),
    ("How fast can I get an SR-22 filed in Nashville?",
     "Usually the same business day. Because Tennessee requires the "
     "certificate to be transmitted electronically by the carrier, it can go "
     "out as soon as your policy is issued and paid."),
    ("What happens if my SR-22 policy cancels?",
     "Your driving privileges can be suspended again for Failure to Maintain "
     "Future Proof of Financial Responsibility. To get your license back you "
     "would have to refile the SR-22, pay reinstatement fees again, and "
     "reapply."),
    ("How do I know when I no longer need an SR-22?",
     "Check your reinstatement requirements in the Tennessee Department of "
     "Safety e-Services portal. If SR22 is not listed, the requirement is "
     "satisfied. Verify there first, then cancel -- never cancel on "
     "assumption."),
    ("What are Tennessee's minimum insurance requirements?",
     "25/50/25: $25,000 bodily injury per person, $50,000 bodily injury per "
     "accident, and $25,000 property damage per accident (T.C.A. Sec. "
     "55-12-102)."),
    ("Will an SR-22 make my insurance go up?",
     "The filing fee itself is minor. The violation behind the filing is what "
     "raises your premium, often substantially, and how much depends heavily "
     "on which carrier you choose. Tennessee does not set the price -- the "
     "insurance company does."),
    ("Is there a payment plan for Tennessee reinstatement fees?",
     "Yes, and it is separate from your insurance payments. If you owe more "
     "than $75 in reinstatement fees and meet all other requirements, the "
     "Department of Safety offers a plan with a $25 administrative down "
     "payment and $75 due each quarter, over a term of up to 60 months."),
    ("I have an SR-22 from another state but moved to Nashville. What now?",
     "The state that ordered the filing still needs it satisfied. Moving does "
     "not clear it. We can help you determine what each state requires and "
     "place coverage that works for both."),
    ("I have a Tennessee SR-22 but moved out of state. Can I get out of it?",
     "Ask the Department of Safety's Financial Responsibility office "
     "directly. Tennessee publishes an out-of-state waiver process for the "
     "ignition interlock requirement, but we would rather send you to the "
     "department for a written answer on SR-22 than promise you a waiver we "
     "cannot document."),
    ("Does an SR-22 cover any car I drive?",
     "It depends on the certificate type. An owner's policy covers listed "
     "vehicles; a non-owner policy covers you as a driver of vehicles you do "
     "not own. Tell us your exact situation so the right one gets filed."),
    ("Do you work with drivers who have multiple DUIs or a long violation "
     "history?",
     "Yes. We work with carriers that write drivers other agencies decline, "
     "and we will give you a realistic price range before you apply."),
    ("Where do I go in person to handle a reinstatement?",
     "A full-service Driver Services Center -- not an express location or a "
     "self-service kiosk. In Davidson County that means Hart Lane at 624 "
     "Hart Lane or Hickory Hollow at 2460 Morris Gentry Blvd. in Antioch. "
     "Centers are open Monday through Friday, 8:30 a.m. to 5:00 p.m., and "
     "stop taking new applicants before closing."),
]

# ------------------------------------------------------------------- steps --
STEPS = [
    ("Confirm what the state actually requires",
     "Pull your reinstatement requirements from the Tennessee Department of "
     "Safety e-Services portal. It tells you whether SR-22 is required, what "
     "else is outstanding, and what you owe. Do not guess, and do not rely "
     "on what a clerk told you months ago."),
    ("Get cleared with the court",
     "If the suspension came from a conviction, the county court that handled "
     "it has to clear you before the state will act. That is Davidson County "
     "General Sessions for most Nashville cases, and the corresponding "
     "General Sessions court in whichever county issued your citation."),
    ("Buy a compliant policy and have it filed",
     "Call or use the form on this site. We compare carriers, quote you, and "
     "once you bind, the carrier transmits the SR-22 to the Department of "
     "Safety electronically -- usually the same business day."),
    ("Pay your reinstatement fees and submit documents",
     "You can pay and submit online, in person at a full-service Driver "
     "Services Center, or by mail. Allow up to five business days for "
     "document review. If you owe more than $75, ask about the state's "
     "installment plan."),
    ("Keep it active without a single lapse",
     "This is the step that costs people the most. Set up autopay. A "
     "cancellation before your term is complete restarts the entire process "
     "and costs far more than whatever premium you were trying to save."),
]

# -------------------------------------------------------------------- blog --
# Post bodies live in blog.py purely to keep this file readable.
from blog import POSTS, INTERNAL_LINKS, POST_PHOTO  # noqa: E402

# ------------------------------------------------------------------- pages --
CORE_PAGES = ["about", "contact", "faq", "services", "404"]
