# -*- coding: utf-8 -*-
"""
Blog content for sr22carinsurancenashvilletn.com.

Kept out of config.py purely for size. Imported by config as `config.POSTS`.

Same accuracy rule as the rest of the site: every procedural claim about
Tennessee traces to a `SOURCES` key in config.py, and each post prints its
sources. Where tn.gov does not publish something, the post says so rather
than filling the gap from a competitor's page.

Body blocks are (kind, payload) tuples:
    ("h2",  "Heading")
    ("h3",  "Subheading")
    ("p",   "Paragraph. May contain inline HTML links.")
    ("ul",  ["item", "item"])
    ("ol",  ["step", "step"])
    ("note","Callout paragraph — the thing people get wrong.")
    ("quote","Pulled statement worth lifting verbatim.")
"""


# slug -> [(phrase that already appears in the body, destination), x3]
INTERNAL_LINKS = {
 "how-long-sr22-tennessee": [
   ("non-owner SR-22", "/non-owner-sr22-insurance.html"),
   ("restricted license", "/blog/restricted-license-tennessee-sr22/"),
   ("re-shop the whole market", "/sr22-removal.html"),
 ],
 "tennessee-license-reinstatement-after-dui": [
   ("Breath Alcohol Ignition Interlock Device", "/sr22-with-ignition-interlock.html"),
   ("restricted license", "/blog/restricted-license-tennessee-sr22/"),
   ("installment plan", "/blog/tennessee-reinstatement-fees-payment-plan/"),
 ],
 "restricted-license-tennessee-sr22": [
   ("ignition interlock device", "/sr22-with-ignition-interlock.html"),
   ("SR-22 liability insurance", "/owner-sr22-insurance.html"),
   ("full-service center", "/tennessee/nashville/"),
 ],
 "owner-vs-non-owner-sr22": [
   ("non-owner policy", "/non-owner-sr22-insurance.html"),
   ("non-owner option", "/non-owner-sr22-insurance.html"),
   ("restricted license", "/blog/restricted-license-tennessee-sr22/"),
 ],
 "tennessee-reinstatement-fees-payment-plan": [
   ("down payment on a policy", "/sr22-payment-plans.html"),
   ("standard-market pricing", "/sr22-removal.html"),
   ("restricted license", "/blog/restricted-license-tennessee-sr22/"),
 ],
 "sr22-lapse-tennessee": [
   ("switching carriers", "/sr22-removal.html"),
   ("Autopay", "/sr22-payment-plans.html"),
   ("restricted license", "/blog/restricted-license-tennessee-sr22/"),
 ],
 "sr22-fr44-sr50-difference": [
   ("carrier licensed to make the filing", "/out-of-state-sr22.html"),
   ("independent agency", "/out-of-state-sr22.html"),
   ("minimum liability limits", "/full-coverage-with-sr22.html"),
 ],
 "moving-with-sr22-tennessee": [
   ("independent agency", "/out-of-state-sr22.html"),
   ("ignition interlock", "/sr22-with-ignition-interlock.html"),
   ("Fort Campbell", "/tennessee/clarksville/"),
 ],
}

# A real Middle Tennessee photo for the third image on each post, chosen for
# relevance. Credits come from places_manifest.json at render time.
POST_PHOTO = {
 "how-long-sr22-tennessee": ("nashville", "Downtown Nashville. Your filing period is set by your own order, not by a rule of thumb."),
 "tennessee-license-reinstatement-after-dui": ("murfreesboro", "The Rutherford County courthouse in Murfreesboro. The court clears you before the state acts."),
 "restricted-license-tennessee-sr22": ("franklin", "The Williamson County courthouse in Franklin, where a restricted licence order is signed."),
 "owner-vs-non-owner-sr22": ("the-gulch", "The Gulch, Nashville. One of the few neighbourhoods where going car-free is realistic."),
 "tennessee-reinstatement-fees-payment-plan": ("columbia", "The Maury County courthouse in Columbia. Reinstatement fees are paid to the state, not to your carrier."),
 "sr22-lapse-tennessee": ("gallatin", "The Sumner County courthouse in Gallatin. A lapse sends you back through this process."),
 "sr22-fr44-sr50-difference": ("springfield", "The Robertson County courthouse in Springfield. Your requirements page is the tie-breaker."),
 "moving-with-sr22-tennessee": ("clarksville", "Downtown Clarksville, near Fort Campbell, where two states' rules often overlap."),
}

POSTS = [
    # ---------------------------------------------------------------- 1 ----
    {
        "slug": "how-long-sr22-tennessee",
        "title": "How Long Do You Need an SR-22 in Tennessee?",
        "dek": "Not three years. Tennessee ties your SR-22 to the length of "
               "your suspension or revocation — which means the answer is "
               "different for every driver.",
        "meta": "Tennessee ties your SR-22 period to the length of your "
                "suspension or revocation, not a flat three years. How to "
                "find your actual end date.",
        "date": "2026-08-13",
        "tags": ["Tennessee rules", "SR-22 basics"],
        "tldr": "Tennessee requires the SR-22 to be maintained for the length "
                "of your suspension or revocation period. A one-year "
                "revocation creates a one-year requirement. There is no flat "
                "three-year rule in Tennessee. Your actual end date is on "
                "your reinstatement requirements page in the Department of "
                "Safety e-Services portal — check there, not on a national "
                "insurance blog.",
        "sources": ["fr", "reinstate", "eservices"],
        "related": ["sr22-lapse-tennessee",
                    "tennessee-reinstatement-fees-payment-plan",
                    "sr22-fr44-sr50-difference"],
        "body": [
            ("p", "Search for how long an SR-22 lasts and almost every result "
                  "says three years. For most states that is roughly right. "
                  "For Tennessee it is wrong, and believing it will cost you "
                  "money in one direction or the other — either you carry "
                  "high-risk insurance longer than the state ever asked you "
                  "to, or you cancel early and get suspended again."),
            ("h2", "What Tennessee actually says"),
            ("p", "The Tennessee Department of Safety and Homeland Security "
                  "publishes the rule plainly: if you have a violation that "
                  "requires SR-22 insurance to be maintained with the "
                  "department, that proof must be maintained for the length "
                  "of your suspension or revocation period."),
            ("quote", "A one-year revocation creates a one-year SR-22 "
                      "requirement. A two-year revocation creates a two-year "
                      "requirement. The filing period follows the order — it "
                      "does not have a default length of its own."),
            ("p", "That is a meaningfully different design from the flat-term "
                  "states. In a three-year state, everyone with a filing "
                  "requirement carries it for three years regardless of what "
                  "they did. In Tennessee, the seriousness of the underlying "
                  "violation sets the revocation, and the revocation sets the "
                  "filing period."),
            ("h2", "Why this matters more than it sounds like it does"),
            ("p", "Two practical consequences follow from it."),
            ("p", "First, if your revocation is shorter than three years, "
                  "carrying an SR-22 for three years means paying high-risk "
                  "rates for months or years after the state stopped "
                  "requiring it. Nothing in the system moves you off that "
                  "pricing automatically. An agency that is not watching your "
                  "term has no reason to tell you."),
            ("p", "Second, if your revocation is longer, assuming three years "
                  "is how a completed requirement turns into a fresh "
                  "suspension. Cancelling before the requirement is finished "
                  "triggers a suspension for Failure to Maintain Future Proof "
                  "of Financial Responsibility, and you start over."),
            ("h2", "How to find your actual end date"),
            ("p", "Do not calculate it, and do not take a number from a "
                  "national comparison site. Pull your own requirements:"),
            ("ol", [
                "Open the Tennessee Department of Safety e-Services portal "
                "and go to your reinstatement requirements page.",
                "Look for SR22 in the list of requirements. If it is listed, "
                "you are still required to carry it.",
                "Read the rest of the list while you are there. Reinstatement "
                "usually involves more than the filing — fees, court "
                "clearances, and sometimes DUI school or an interlock device.",
                "When SR22 is no longer listed, the requirement is satisfied.",
            ]),
            ("note", "Verify before you cancel, not after. The requirements "
                     "page is the authoritative record of what the state "
                     "wants from you. A clerk's verbal answer from eight "
                     "months ago is not."),
            ("h2", "When the clock starts"),
            ("p", "The department states that the SR-22 can be maintained "
                  "while you hold a restricted license, or beginning at "
                  "reinstatement. If you are driving on a restricted license "
                  "during a revocation, you are already carrying the filing — "
                  "in fact you cannot get the restricted license without it."),
            ("p", "That is worth knowing because it changes the sequence. "
                  "Plenty of people assume they buy the SR-22 at the end of "
                  "the process, as the last box to tick before their license "
                  "comes back. If you want to drive during the revocation, "
                  "the filing comes near the beginning instead."),
            ("h2", "What can extend it"),
            ("p", "A new offense during the period is the obvious one. "
                  "Tennessee law contemplates the department releasing the "
                  "proof-of-financial-responsibility requirement after the "
                  "suspension or revocation period ends if the record shows "
                  "no additional offense that would authorize or require "
                  "another suspension during that time."),
            ("p", "The less obvious one is a lapse. If your policy cancels "
                  "mid-term and you have to refile, you are not picking up "
                  "where you left off — you are re-entering a process that "
                  "includes paying reinstatement fees again and reapplying "
                  "for the license."),
            ("h2", "What the filing certifies while it runs"),
            ("p", "For the whole period, the policy behind the certificate "
                  "has to meet at least Tennessee's minimum liability limits: "
                  "25/50/25, meaning $25,000 bodily injury per person, "
                  "$50,000 bodily injury per accident, and $25,000 property "
                  "damage per accident. You can carry more, and after a "
                  "serious at-fault loss there is a real argument for it, but "
                  "you cannot carry less and stay compliant."),
            ("p", "Dropping to a cheaper policy mid-term is a common way to "
                  "accidentally break compliance. If the replacement policy "
                  "does not meet the minimums, or does not carry the filing, "
                  "the certificate is not doing its job even though you are "
                  "insured."),
            ("h2", "Owner and non-owner filings run the same clock"),
            ("p", "The length of the requirement does not change based on "
                  "which certificate type you hold. A non-owner SR-22 is "
                  "cheaper because there is no vehicle to insure for physical "
                  "damage, not because it expires sooner. If you sell your "
                  "car partway through and switch to a non-owner policy, the "
                  "end date is unchanged — but the switch itself is a moment "
                  "where filings get dropped, so confirm the new one is on "
                  "record before cancelling the old one."),
            ("h2", "Three years is a real rule — somewhere else"),
            ("p", "It is worth understanding why the wrong answer is so "
                  "durable. Most SR-22 content online is written to rank in "
                  "every state at once, so it describes the most common "
                  "pattern and moves on. Three years genuinely is the term in "
                  "a number of states. It is simply not how Tennessee has "
                  "structured it."),
            ("p", "This is also why the question is worth getting right for "
                  "reasons beyond your own bill. When an AI assistant or a "
                  "search engine answers \"how long does an SR-22 last in "
                  "Tennessee,\" it is weighing sources against each other. "
                  "The pages that match what the Department of Safety "
                  "publishes are the ones that deserve to win, and the "
                  "state's own page is always the tiebreaker you can check "
                  "yourself."),
            ("h2", "A note on getting off it promptly"),
            ("p", "Because the end date varies, there is no calendar reminder "
                  "the industry sets for you. Most people discover their "
                  "requirement ended by accident, months later, after paying "
                  "high-risk premiums the whole time."),
            ("p", "Set your own reminder for the end of your revocation "
                  "period. Check e-Services that week. If SR22 is gone from "
                  "your requirements, that is the moment to re-shop the whole "
                  "market — your record still has the violation on it, but "
                  "you are no longer a driver with an active filing "
                  "obligation, and a number of carriers price those two "
                  "situations very differently."),
            ("h2", "The short version"),
            ("p", "Your SR-22 lasts exactly as long as your suspension or "
                  "revocation, and the only place that answer lives is your "
                  "own requirements page. Anyone who tells you three years "
                  "without looking at your record is quoting a different "
                  "state's rule."),
        ],
    },

    # ---------------------------------------------------------------- 2 ----
    {
        "slug": "tennessee-license-reinstatement-after-dui",
        "title": "Reinstating a Tennessee License After a DUI: the Whole "
                 "Sequence",
        "dek": "Court, interlock, SR-22, fees, and the Driver Services "
               "Center — in the order Tennessee actually wants them.",
        "meta": "The full order of operations for reinstating a Tennessee "
                "driver license after a DUI: court clearance, ignition "
                "interlock, SR-22 filing, fees, and which centers can help.",
        "date": "2026-08-13",
        "tags": ["DUI", "Reinstatement"],
        "tldr": "Reinstating after a Tennessee DUI runs roughly: get cleared "
                "by the court, install an ignition interlock device if one is "
                "required, have a licensed carrier file your SR-22 "
                "electronically, pay your reinstatement fees, and submit "
                "everything to the Department of Safety. Only full-service "
                "Driver Services Centers process reinstatements — in "
                "Davidson County that is Hart Lane or Hickory Hollow.",
        "sources": ["fr", "reinstate", "interlock", "restricted", "locations",
                    "eservices"],
        "related": ["restricted-license-tennessee-sr22",
                    "how-long-sr22-tennessee",
                    "tennessee-reinstatement-fees-payment-plan"],
        "body": [
            ("p", "A DUI reinstatement in Tennessee is not one transaction. "
                  "It is a sequence involving a court, an interlock vendor, "
                  "an insurance carrier, and a state agency, and each one is "
                  "waiting on a different piece. Most of the wasted time "
                  "people spend on this comes from doing the steps in the "
                  "wrong order, not from any single step being hard."),
            ("h2", "Step 0: find out what you are actually required to do"),
            ("p", "Before anything else, pull your reinstatement requirements "
                  "from the Department of Safety e-Services portal. It lists "
                  "what is outstanding and what you owe. Two people with the "
                  "same charge can have different lists, and the list is what "
                  "governs."),
            ("note", "Everything below is the common shape of a DUI "
                     "reinstatement. Your requirements page is the "
                     "authoritative version for you specifically."),
            ("h2", "Step 1: get cleared with the court"),
            ("p", "If the suspension came from a conviction, the court that "
                  "handled it has to clear you before the state will act. For "
                  "most Nashville cases that is Davidson County General "
                  "Sessions; elsewhere it is the General Sessions court in "
                  "the county that issued your citation."),
            ("p", "Court clearance is also where the restricted license "
                  "question gets decided, because a restricted license "
                  "requires a certified order signed by a judge."),
            ("h2", "Step 2: ignition interlock, if it applies"),
            ("p", "Tennessee requires a Breath Alcohol Ignition Interlock "
                  "Device for drivers convicted of or pleading guilty to a "
                  "DUI who want to keep driving during the revocation, unless "
                  "a waiver is granted. The department publishes minimum "
                  "installation periods by offense:"),
            ("ul", [
                "DUI 1st — 365 days",
                "DUI 2nd — 730 days",
                "DUI 3rd — 2,190 days",
                "DUI 4th or subsequent — 2,920 days",
            ]),
            ("p", "There is also a compliance requirement at the end. During "
                  "the final 120 days, certain violations — attempting to "
                  "start the vehicle above a .020% breath alcohol reading "
                  "without a verified passing retest within ten minutes, "
                  "skipping rolling retests, or failing them — restart that "
                  "120-day window. People lose months here, at the very end, "
                  "which is a demoralizing place to lose months."),
            ("p", "If a court has declared you indigent, Tennessee's "
                  "Electronic Monitoring Indigency Fund covers interlock "
                  "services within published fee caps. That is administered "
                  "by the Department of Treasury, not the Department of "
                  "Safety."),
            ("h2", "Step 3: the SR-22 filing"),
            ("p", "The certificate must be filed electronically with the "
                  "department by an insurance company licensed through the "
                  "Tennessee Department of Commerce and Insurance to issue "
                  "motor vehicle liability coverage in Tennessee. You cannot "
                  "file it yourself, and a standard policy without the filing "
                  "does not satisfy the requirement."),
            ("p", "Because the transmission is electronic, this is usually "
                  "the fastest step in the whole sequence — often the same "
                  "business day the policy binds. It is also the step people "
                  "leave until last, which is backwards if you want a "
                  "restricted license, since you cannot get one without proof "
                  "of an SR-22 currently in effect."),
            ("h2", "Step 4: pay reinstatement fees and submit documents"),
            ("p", "Fees vary by violation type and are shown on your "
                  "requirements page. You can pay and submit online, in "
                  "person at a full-service Driver Services Center, or by "
                  "mail to Financial Responsibility, PO Box 945, Nashville, "
                  "TN 37202. Courier deliveries go to 1150 Foster Ave., "
                  "Nashville, TN 37210. Allow up to five business days for "
                  "document review."),
            ("p", "If you owe more than $75, ask about the state's "
                  "installment plan rather than delaying the whole "
                  "reinstatement over the balance."),
            ("h2", "Step 5: keep it active, without a gap"),
            ("p", "The requirement runs for the length of your revocation. If "
                  "the policy cancels before that is complete, your driving "
                  "privileges can be suspended again for Failure to Maintain "
                  "Future Proof of Financial Responsibility, and you refile, "
                  "pay fees again, and reapply."),
            ("h2", "Where to go in person"),
            ("p", "Only full-service Driver Services Centers handle "
                  "reinstatement transactions — paying fees, setting up a "
                  "payment plan, and submitting documentation. Express "
                  "centers and self-service kiosks do not."),
            ("ul", [
                "Hart Lane — 624 Hart Lane, Nashville, TN 37216 "
                "(full-service, handles reinstatement)",
                "Hickory Hollow — 2460 Morris Gentry Blvd., Antioch, TN "
                "37013 (full-service)",
                "Nashville Downtown Express — 312 Rosa L. Parks Blvd, 3rd "
                "Floor (express; no testing)",
                "Metro Center — 220 French Landing Dr. (self-service kiosk)",
            ]),
            ("note", "Centers are open Monday through Friday, 8:30 a.m. to "
                     "5:00 p.m., and stop taking new applicants before the "
                     "posted closing time. Do not arrive at 4:45 expecting to "
                     "be seen."),
            ("h2", "If you live outside Davidson County"),
            ("p", "Most of the Middle Tennessee counties have their own "
                  "full-service center, which turns a half-day trip into an "
                  "errand. Rutherford County drivers use Samsonite Blvd. in "
                  "Murfreesboro — not the Blaze Drive express location. "
                  "Williamson County uses Carothers Parkway in Franklin; the "
                  "Mallory Lane location in Brentwood is a self-service kiosk "
                  "and cannot clear a hold."),
            ("p", "Sumner County uses Gallatin, Wilson County uses Lebanon, "
                  "Maury County uses Columbia, Robertson County uses "
                  "Springfield, and Dickson County has its own. Montgomery "
                  "County has two full-service centers in Clarksville, so "
                  "there is no wrong door there."),
            ("h2", "The interlock removal step people forget"),
            ("p", "Getting the device out is its own two-part approval, and "
                  "it does not happen automatically when your time is up. The "
                  "manufacturer produces a compliance determination form "
                  "showing your compliance status and any extensions from "
                  "violations. The state then reviews your license status "
                  "across the interlock period and, if satisfied, issues a "
                  "letter authorising removal."),
            ("p", "You take that to a Driver Services Center for an "
                  "unrestricted license, and provide it to the manufacturer "
                  "before they will schedule the removal. Budget time for it "
                  "rather than assuming the last day of the term is the day "
                  "the device comes out."),
            ("h2", "Common ways this goes sideways"),
            ("ul", [
                "Buying insurance without the filing. A standard policy is "
                "not an SR-22, and the Driver Services Center will not accept "
                "a declarations page in its place.",
                "Assuming the interlock vendor transmitted the installation "
                "record electronically. Ask them to confirm — the state needs "
                "it in their database, not on your receipt.",
                "Paying state fees before securing insurance, then not having "
                "the down payment for a policy. The filing gates more of the "
                "process than the fees do.",
                "Waiting on the mail. The certificate transmits "
                "electronically; there is no postal step for the SR-22 "
                "itself.",
                "Treating the requirements page as a one-time check. Pull it "
                "again after each step clears, so you find a problem while it "
                "is still small.",
            ]),
            ("h2", "Roughly how long the whole thing takes"),
            ("p", "The insurance step is usually same-day. Document review at "
                  "the department runs up to five business days. The court "
                  "step and the interlock step are the variable ones, and "
                  "they are the ones worth starting first for exactly that "
                  "reason."),
            ("p", "There is no way to compress a revocation period itself. "
                  "What you can compress is the administrative tail on either "
                  "end of it — and the difference between a driver who "
                  "sequences this well and one who does not is frequently "
                  "measured in weeks of not driving."),
        ],
    },

    # ---------------------------------------------------------------- 3 ----
    {
        "slug": "restricted-license-tennessee-sr22",
        "title": "Tennessee Restricted Licenses and the 10-Day Rule Nobody "
                 "Warns You About",
        "dek": "You have ten days from the judge's signature to get to a "
               "Driver Services Center — and you need the SR-22 already in "
               "force when you walk in.",
        "meta": "Tennessee gives you 10 days from a signed restricted license "
                "court order to apply at a Driver Services Center, with an "
                "SR-22 already in effect. What to have ready.",
        "date": "2026-08-13",
        "tags": ["Restricted license", "DUI"],
        "tldr": "Tennessee requires you to apply for a restricted license "
                "within ten days of the court order being signed, and the "
                "SR-22 must already be in effect when you apply — a standard "
                "insurance policy is not an acceptable substitute. You "
                "receive a 90-day temporary license while the application is "
                "reviewed.",
        "sources": ["restricted", "fr", "interlock", "locations"],
        "related": ["tennessee-license-reinstatement-after-dui",
                    "how-long-sr22-tennessee",
                    "owner-vs-non-owner-sr22"],
        "body": [
            ("p", "The restricted license is how a lot of Tennessee drivers "
                  "keep working through a revocation. It is also where the "
                  "tightest deadline in the whole process lives, and it is "
                  "not the deadline people expect."),
            ("h2", "The ten-day window"),
            ("p", "Tennessee's process starts with a certified Order for "
                  "Restricted Driver License, obtained from the court where "
                  "you were convicted or the court in your county of "
                  "residence, and signed by a judge. From the date of that "
                  "signature, you have ten days to appear at a Driver "
                  "Services Center and apply."),
            ("note", "The clock runs from the judge's signature, not from "
                     "when you picked the order up, and not from when you got "
                     "around to shopping for insurance. If you spend a week "
                     "comparing quotes, you have spent most of your window."),
            ("h2", "The SR-22 has to already be in force"),
            ("p", "This is the part that sends people home. The department is "
                  "explicit that you must obtain SR-22 liability insurance "
                  "showing the policy is currently in effect, and that a "
                  "standard insurance policy or other documentation is not "
                  "acceptable in its place."),
            ("p", "Proof of insurance is not proof of an SR-22. A declarations "
                  "page is not an SR-22. The certificate is a separate filing "
                  "that a licensed carrier transmits electronically to the "
                  "department, and it either exists in their system or it "
                  "does not."),
            ("p", "The good news is that this is fast. Because Tennessee "
                  "takes the filing electronically, a policy bound in the "
                  "morning can be filed the same business day. The bad news "
                  "is that it is only fast if you start it — a filing you "
                  "have not bought yet takes infinite time."),
            ("h2", "Interlock proof, if it applies"),
            ("p", "If your case requires an ignition interlock device, it "
                  "must be installed before you obtain the restricted "
                  "license, and the Driver Services Center will expect proof "
                  "of installation to have been submitted electronically into "
                  "the state's database by your interlock company. Ask your "
                  "vendor to confirm they have transmitted it. A paper "
                  "receipt in your hand is not the same as a record in the "
                  "state's system."),
            ("h2", "What you walk out with"),
            ("p", "On a successful application you receive a 90-day temporary "
                  "license and pay the applicable fees. A restricted license "
                  "case is then created for Central Office review to confirm "
                  "eligibility. If everything checks out, a hard-copy "
                  "restricted license is issued, valid for the duration of "
                  "the revocation period."),
            ("p", "The 90 days matter: the review has to complete inside that "
                  "window, or the application starts over. If something in "
                  "your file is wrong — a missing interlock record, a lapsed "
                  "filing — you want it found early, not on day 88."),
            ("h2", "A checklist to walk in with"),
            ("ol", [
                "Certified Order for Restricted Driver License, signed by a "
                "judge, dated within the last ten days.",
                "An SR-22 currently in effect, filed electronically by a "
                "carrier licensed in Tennessee.",
                "Proof of ignition interlock installation, transmitted "
                "electronically by your vendor, if required in your case.",
                "Your reinstatement requirements from e-Services, so you can "
                "see anything else outstanding.",
                "Payment for applicable fees.",
            ]),
            ("p", "And go to a full-service center. Express locations and "
                  "self-service kiosks do not handle this."),
            ("h2", "Why the order of operations matters so much here"),
            ("p", "Every other part of a reinstatement is forgiving about "
                  "sequence. This one is not, because two independent clocks "
                  "are running: the ten days from the judge's signature, and "
                  "however long it takes you to get an SR-22 in force."),
            ("p", "If you start shopping for insurance after the order is "
                  "signed, those clocks run in series and you are gambling. "
                  "If you have the filing in place before you go back to "
                  "court for the order, they run in parallel and the ten days "
                  "is comfortable. Same work, completely different stress "
                  "level."),
            ("note", "If you know a restricted license is likely — because "
                     "your attorney has raised it, or because you cannot keep "
                     "your job without driving — get the SR-22 quoted and "
                     "ready before the court date, not after."),
            ("h2", "What a restricted license does and does not give you"),
            ("p", "It is permission to drive during a revocation, not the "
                  "return of your ordinary license, and it remains valid only "
                  "for the duration of the revocation period. The specific "
                  "limitations come from the court's order — the scope is set "
                  "by the judge, not by the Department of Safety."),
            ("p", "It also does not shorten anything. Your revocation runs "
                  "its length, and your SR-22 obligation runs alongside it. "
                  "What the restricted license changes is whether you spend "
                  "that period able to get to work."),
            ("h2", "Where the order comes from"),
            ("p", "The certified order can come from the court where you were "
                  "convicted or the court in your county of residence. For "
                  "most Nashville-area cases that means the relevant county's "
                  "General Sessions court. Two things are worth asking the "
                  "clerk directly: that the copy is certified, and that the "
                  "judge's signature date is on it, since that date starts "
                  "your ten days."),
            ("h2", "If the ten days lapse"),
            ("p", "Talk to the court. You are generally looking at obtaining "
                  "a fresh order rather than talking your way past the "
                  "deadline at a Driver Services Center — the counter staff "
                  "are applying a rule, not exercising discretion."),
            ("p", "The more expensive version of this mistake is having the "
                  "order in hand and no SR-22, discovering it at the counter, "
                  "and burning three of your ten days getting insurance you "
                  "could have had a week earlier."),
        ],
    },

    # ---------------------------------------------------------------- 4 ----
    {
        "slug": "owner-vs-non-owner-sr22",
        "title": "Owner vs. Non-Owner SR-22: Which One Do You Actually Need?",
        "dek": "The wrong certificate type satisfies nothing. Here is how to "
               "tell which one your situation calls for.",
        "meta": "Owner and non-owner SR-22 policies both satisfy Tennessee's "
                "filing requirement, but they cover different things. How to "
                "pick the right one — and what non-owner does not cover.",
        "date": "2026-08-13",
        "tags": ["SR-22 basics", "Saving money"],
        "tldr": "If a vehicle is titled to you or regularly available to you, "
                "you need an owner's SR-22 attached to a liability policy on "
                "that vehicle. If you genuinely do not own or have regular "
                "access to a car, a non-owner SR-22 satisfies the same state "
                "filing for less money — but it is liability-only and covers "
                "no vehicle damage.",
        "sources": ["fr"],
        "related": ["how-long-sr22-tennessee",
                    "restricted-license-tennessee-sr22",
                    "sr22-lapse-tennessee"],
        "body": [
            ("p", "Both policy types produce a certificate the Tennessee "
                  "Department of Safety will accept. They are not "
                  "interchangeable, and buying the wrong one wastes money in "
                  "one direction or leaves you uncovered in the other."),
            ("h2", "The owner's SR-22"),
            ("p", "This is the default. If you have a vehicle titled in your "
                  "name, the filing attaches to a liability policy on that "
                  "vehicle, meeting at least Tennessee's 25/50/25 minimum: "
                  "$25,000 bodily injury per person, $50,000 per accident, "
                  "and $25,000 property damage."),
            ("p", "You can carry far more than the minimum, and if you "
                  "finance or lease the car you will also carry comprehensive "
                  "and collision because your lender requires it. The SR-22 "
                  "is indifferent to all of that — it certifies the liability "
                  "piece."),
            ("h2", "The non-owner SR-22"),
            ("p", "This is the option most drivers do not know exists. It "
                  "provides liability coverage when you drive vehicles you do "
                  "not own, and it satisfies the state filing. Because there "
                  "is no vehicle to insure for physical damage, it is "
                  "typically the least expensive path to reinstatement."),
            ("p", "It fits genuinely car-free situations: you sold the car, "
                  "you borrow one occasionally, you drive a company vehicle "
                  "covered by your employer, you use car-share, or you simply "
                  "want your license valid again while you rebuild."),
            ("h2", "What a non-owner policy does not do"),
            ("ul", [
                "It does not cover damage to the vehicle you are driving. "
                "Liability only.",
                "It does not cover a car titled to you.",
                "It generally does not cover a vehicle that lives at your "
                "address or is regularly available to you — including a "
                "household member's car.",
                "It is not a way to insure a car cheaply. If you have regular "
                "access to a vehicle, this is the wrong product and a claim "
                "is where you would find that out.",
            ]),
            ("note", "That third point is where people get into trouble. "
                     "Buying a non-owner policy while driving your partner's "
                     "car every day is not a clever savings move — it is a "
                     "coverage gap you discover at the worst possible "
                     "moment."),
            ("h2", "A quick way to decide"),
            ("ol", [
                "Is a vehicle titled in your name? Owner's policy.",
                "Is there a vehicle at your address you drive regularly, "
                "even if it is not yours? Talk to an agent — a non-owner "
                "policy is probably wrong, and there may be a better "
                "structure for the household.",
                "Do you genuinely drive only cars you borrow occasionally or "
                "rent, with no vehicle available to you day to day? "
                "Non-owner policy.",
                "Not sure? Describe the actual situation out loud to an "
                "agent, including whose cars are in the driveway. The right "
                "answer usually falls out in a minute.",
            ]),
            ("h2", "Why the price gap is worth asking about"),
            ("p", "Carriers disagree enormously about how to price drivers "
                  "with a violation on their record. That is true for both "
                  "policy types, and it is the reason to compare rather than "
                  "call one company. It is also why an agency that never "
                  "raises the non-owner option with a genuinely car-free "
                  "client is not doing the job — the cheaper product is "
                  "sometimes the correct product."),
            ("h2", "Both types satisfy the state identically"),
            ("p", "This is worth stating plainly, because people assume the "
                  "cheaper option must be a lesser one in the state's eyes. "
                  "It is not. Tennessee needs a certificate of financial "
                  "responsibility filed electronically by a licensed carrier, "
                  "proving liability coverage at or above 25/50/25. A "
                  "non-owner policy that meets those limits satisfies that "
                  "requirement exactly as an owner's policy does."),
            ("p", "The requirement also runs for the same length either way: "
                  "the length of your suspension or revocation period. "
                  "Choosing the non-owner route does not shorten your term."),
            ("h2", "The restricted-license wrinkle"),
            ("p", "If you are applying for a restricted license, the "
                  "department requires an SR-22 currently in effect, and will "
                  "not accept a standard policy in its place. Either "
                  "certificate type can satisfy that, but the practical "
                  "question is what you will actually be driving under the "
                  "court's order. If the restricted license exists so you can "
                  "drive to work in your own car, a non-owner policy is not "
                  "the right instrument."),
            ("h2", "Switching between them mid-term"),
            ("p", "People move in both directions during a filing period — "
                  "selling a car and going non-owner to save money, or buying "
                  "one and needing to convert. Both are normal. Both are also "
                  "the highest-risk moment for an accidental lapse, because "
                  "you are cancelling one policy and starting another."),
            ("ul", [
                "Have the new policy bound and the filing confirmed on record "
                "with the department before the old one cancels.",
                "Overlap by a day rather than timing it to the minute.",
                "Ask the new carrier explicitly to confirm the SR-22 was "
                "transmitted — not that it was requested.",
                "Re-pull your requirements page a few days later to see the "
                "state's view of it.",
            ]),
            ("note", "A gap of even a few days between filings can read as a "
                     "termination to the department and trigger a suspension "
                     "for Failure to Maintain Future Proof of Financial "
                     "Responsibility. The savings from a cheaper policy never "
                     "cover the cost of that."),
            ("h2", "What to tell an agent so they can get it right"),
            ("p", "Give the whole picture in one go: whose names are on which "
                  "titles, what is parked at your address, whether you drive "
                  "anything for work, and whether a court order is involved. "
                  "Those four answers determine the policy type, and getting "
                  "them wrong is the difference between a certificate that "
                  "works and one that leaves you exposed on a claim."),
        ],
    },

    # ---------------------------------------------------------------- 5 ----
    {
        "slug": "tennessee-reinstatement-fees-payment-plan",
        "title": "What Tennessee Reinstatement Actually Costs — and the "
                 "Payment Plan Most People Miss",
        "dek": "Your insurance premium is one bill. The state's fees are "
               "another, and Tennessee will let you pay them quarterly.",
        "meta": "Tennessee reinstatement fees are separate from your "
                "insurance premium. If you owe more than $75, the state "
                "offers a payment plan: $25 down, then $75 per quarter.",
        "date": "2026-08-13",
        "tags": ["Money", "Reinstatement"],
        "tldr": "Reinstatement fees are charged by the state and are separate "
                "from your insurance. If you owe more than $75 and meet all "
                "other reinstatement requirements, Tennessee offers an "
                "installment plan: a $25 administrative down payment, then "
                "$75 every quarter, over a term of up to 60 months.",
        "sources": ["installment", "reinstate", "eservices"],
        "related": ["tennessee-license-reinstatement-after-dui",
                    "how-long-sr22-tennessee", "sr22-lapse-tennessee"],
        "body": [
            ("p", "There are two separate bills in a Tennessee reinstatement, "
                  "and conflating them is why people give up partway "
                  "through. One goes to an insurance company. The other goes "
                  "to the state, and the state is more flexible about it than "
                  "most drivers realize."),
            ("h2", "Bill one: the insurance"),
            ("p", "The SR-22 filing fee itself is small — carriers typically "
                  "charge $15 to $25, usually once, though some charge it at "
                  "every renewal. Worth asking which kind you are buying."),
            ("p", "What actually costs money is the premium, and the premium "
                  "is driven by the violation behind the filing, not by the "
                  "filing. Tennessee is explicit that the cost of the "
                  "insurance is determined by the insurance company, not the "
                  "state. Two carriers looking at the same record on the same "
                  "day will not give you the same number, which is the entire "
                  "argument for comparing rather than accepting the first "
                  "quote."),
            ("h2", "Bill two: state reinstatement fees"),
            ("p", "These vary by violation type. Your exact amount is on your "
                  "reinstatement requirements page in the Department of "
                  "Safety e-Services portal — that is the only number worth "
                  "budgeting against, because a stacked record produces a "
                  "different total than a single violation."),
            ("p", "You can pay online, in person at a full-service Driver "
                  "Services Center, or by mail to Financial Responsibility, "
                  "PO Box 945, Nashville, TN 37202. Allow up to five business "
                  "days for document review."),
            ("h2", "The payment plan"),
            ("p", "This is the part that goes unmentioned on most SR-22 "
                  "sites. Tennessee offers an installment plan for "
                  "reinstatement fees:"),
            ("ul", [
                "Eligibility — you must owe more than $75 in reinstatement "
                "fees and meet all other reinstatement requirements.",
                "Down payment — $25, as an administrative fee, when you enter "
                "the plan.",
                "Installments — $75 each quarter, every three months, until "
                "the balance is paid.",
                "Term — up to 60 months.",
            ]),
            ("p", "You can set one up by mail request or in person at any "
                  "Tennessee Driver Services Center. If your license is "
                  "revoked or suspended again while a plan is active and in "
                  "good standing, you can request to modify the plan to "
                  "include the new fees rather than starting a second one. If "
                  "a plan defaults, you can request a new plan for the unpaid "
                  "balance."),
            ("note", "The eligibility floor is the total you owe, not your "
                     "ability to pay. Owing more than $75 is what qualifies "
                     "you — and most reinstatements clear that easily."),
            ("h2", "Sequencing the two bills"),
            ("p", "The insurance has to come first in practice, because the "
                  "SR-22 needs to be on file before several other things can "
                  "happen — a restricted license in particular requires a "
                  "policy currently in effect. The state fees can then be "
                  "handled on a plan while you are already driving legally."),
            ("p", "Doing it the other way around — draining savings on state "
                  "fees, then discovering you cannot afford the down payment "
                  "on a policy — is a common and avoidable trap."),
            ("h2", "One more cost worth naming"),
            ("p", "Staying on SR-22 pricing after your requirement ends is a "
                  "real expense, and an invisible one. Tennessee ties the "
                  "filing period to the length of your suspension or "
                  "revocation, so plenty of drivers are done sooner than "
                  "three years — but nothing moves you back to standard-market "
                  "pricing on its own. Check e-Services, confirm SR22 is gone "
                  "from your requirements, then re-shop."),
            ("h2", "What drives your premium, in rough order"),
            ("p", "If you want to predict where your number will land before "
                  "anyone quotes you, these are the levers carriers actually "
                  "pull:"),
            ("ul", [
                "The specific violation and how recently it happened. A DUI "
                "prices very differently from an accumulation of points, and "
                "both fade with time.",
                "Whether you choose an owner or non-owner policy. No vehicle "
                "to insure for physical damage is the single biggest "
                "structural saving available.",
                "Your ZIP code. Urban density and claim frequency mean "
                "Davidson County generally runs above the statewide average.",
                "Age and how long you have been licensed. Short licensing "
                "histories are priced most inconsistently between carriers.",
                "Any lapse in prior coverage, separate from the violation "
                "itself.",
                "Your limits and deductibles, and whether a lienholder "
                "requires comprehensive and collision.",
            ]),
            ("p", "Third-party rate studies put average SR-22 auto insurance "
                  "in Tennessee somewhere in the range of $130 to $215 per "
                  "month for minimum-limits coverage after a DUI, against "
                  "roughly $65 to $80 for a clean record. Treat those as "
                  "orientation, not a quote — they are estimates from outside "
                  "the state, and your actual number comes from a carrier "
                  "looking at your actual record."),
            ("h2", "Ways to genuinely lower the insurance bill"),
            ("ol", [
                "Compare carriers rather than accepting a renewal. The spread "
                "between the highest and lowest quote for the same driver is "
                "routinely the largest saving on the table.",
                "Ask whether a non-owner policy fits your real situation. If "
                "you genuinely have no vehicle, it usually costs "
                "substantially less.",
                "Ask whether the filing fee is charged once or at every "
                "renewal, and weigh that over the length of your term.",
                "Set up autopay so a failed payment never turns into a lapse "
                "and a second round of state fees.",
                "Diary your end date and re-shop the week your requirement "
                "clears.",
            ]),
            ("note", "Be skeptical of anyone promising a specific price or "
                     "the \"lowest rate\" before a carrier has underwritten "
                     "you. Insurance advertising is regulated in Tennessee, "
                     "and a number quoted without your record behind it is "
                     "not a number."),
            ("h2", "Budgeting the whole thing honestly"),
            ("p", "Add up three things: the insurance down payment and "
                  "monthly premium, your state reinstatement fees from "
                  "e-Services, and — if a DUI is involved — interlock costs. "
                  "For drivers a court has declared indigent, Tennessee's "
                  "Electronic Monitoring Indigency Fund covers interlock "
                  "services within published caps, administered by the "
                  "Department of Treasury rather than the Department of "
                  "Safety."),
            ("p", "Knowing the real total up front is what keeps people from "
                  "stalling out halfway through, which is by far the most "
                  "expensive outcome available."),
        ],
    },

    # ---------------------------------------------------------------- 6 ----
    {
        "slug": "sr22-lapse-tennessee",
        "title": "What Happens If Your SR-22 Lapses in Tennessee",
        "dek": "A missed payment does not just cancel a policy. It restarts "
               "a process you already paid to finish.",
        "meta": "If an SR-22 policy cancels before the requirement is "
                "complete, Tennessee can suspend your license again for "
                "Failure to Maintain Future Proof of Financial "
                "Responsibility. How to avoid it.",
        "date": "2026-08-13",
        "tags": ["Tennessee rules", "Staying compliant"],
        "tldr": "If your SR-22 policy is canceled or terminated before the "
                "requirement is complete, your driving privileges can be "
                "suspended again for Failure to Maintain Future Proof of "
                "Financial Responsibility. You would then have to refile the "
                "SR-22, pay reinstatement fees again, and reapply for your "
                "license.",
        "sources": ["fr", "reinstate", "eservices"],
        "related": ["how-long-sr22-tennessee",
                    "tennessee-reinstatement-fees-payment-plan",
                    "owner-vs-non-owner-sr22"],
        "body": [
            ("p", "The single most expensive mistake in the SR-22 system is "
                  "not choosing the wrong carrier. It is letting the policy "
                  "lapse two months before the requirement would have ended."),
            ("h2", "What the state does"),
            ("p", "The carrier that filed your certificate also notifies the "
                  "department when the policy terminates. The Department of "
                  "Safety is direct about the consequence: if the policy is "
                  "canceled or terminated prior to completing the "
                  "requirement, this can result in the driving privileges "
                  "being suspended for Failure to Maintain Future Proof of "
                  "Financial Responsibility."),
            ("quote", "To get the license back you refile the SR-22, pay "
                      "reinstatement fees again, and reapply. You do not "
                      "resume where you left off."),
            ("p", "That last point is the one worth sitting with. The lapse "
                  "does not pause the clock — it drops you back into a "
                  "process you had already paid to get through, with a new "
                  "round of fees attached."),
            ("h2", "How lapses actually happen"),
            ("p", "Almost never on purpose. In rough order of frequency:"),
            ("ul", [
                "A card on file expires or a bank account changes, and the "
                "auto-payment fails quietly.",
                "The policy renews at a higher premium and the payment fails "
                "for the difference.",
                "The driver assumes the requirement is over — usually because "
                "they read somewhere that SR-22s last three years — and "
                "cancels.",
                "A mid-term change (new vehicle, new address, a driver added "
                "or removed) is mishandled and the policy is rewritten "
                "without the filing carried over.",
                "The driver switches carriers to save money and the new "
                "policy is issued without an SR-22 attached.",
            ]),
            ("note", "That last one is worth naming clearly: switching "
                     "carriers is fine, but the new policy must carry the "
                     "filing, and the timing has to be clean. Ask the new "
                     "carrier to confirm the filing has been transmitted "
                     "before you cancel the old policy — not after."),
            ("h2", "How to not have this happen"),
            ("ol", [
                "Put the policy on autopay, and set a reminder to check the "
                "payment method annually before renewal.",
                "Never cancel based on assumption. Open e-Services, confirm "
                "SR22 is no longer listed among your requirements, then "
                "cancel.",
                "When switching carriers, overlap by a day and confirm the "
                "new filing is on record with the department first.",
                "Tell your agent about any change to the vehicle, address, or "
                "drivers on the policy, and ask explicitly whether the filing "
                "carries over.",
                "Know your actual end date. In Tennessee it matches your "
                "suspension or revocation period, and it is on your "
                "requirements page.",
            ]),
            ("h2", "If it already lapsed"),
            ("p", "Get a new policy with the filing in place as fast as "
                  "possible, then pull your requirements page to see exactly "
                  "what the state now wants — the list will have changed. "
                  "Expect fees, and expect to reapply. It is recoverable; it "
                  "is just more expensive than it needed to be."),
            ("h3", "In order"),
            ("ol", [
                "Bind a compliant policy today and have the carrier file the "
                "SR-22 electronically. Because the transmission is "
                "electronic, this part is usually same-day.",
                "Pull your reinstatement requirements from e-Services and "
                "read the new list, not the one you remember.",
                "Pay whatever reinstatement fees have been added. If the "
                "total is over $75, ask about the installment plan rather "
                "than delaying.",
                "Reapply for the license, and allow up to five business days "
                "for document review.",
                "If you were driving on a restricted license, check whether "
                "that order is affected — it required an SR-22 in effect to "
                "issue.",
            ]),
            ("h2", "The mechanism behind the suspension"),
            ("p", "It is not that the state is watching your bank account. "
                  "When a filed policy terminates, the carrier notifies the "
                  "department — that notice is the trigger. Which means two "
                  "useful things follow."),
            ("p", "First, it is automatic and reasonably fast, so there is no "
                  "quiet grace period to rely on. Second, it is tied to the "
                  "carrier's records, so a policy that was rewritten or "
                  "replaced without the filing carried over can look like a "
                  "termination even though you never intended to be "
                  "uninsured."),
            ("h2", "The one that catches careful people"),
            ("p", "Cancelling on assumption. Someone reads that SR-22s last "
                  "three years, counts three years from their conviction, and "
                  "cancels — while their Tennessee revocation, and therefore "
                  "their filing requirement, still has months to run."),
            ("p", "Tennessee ties the period to the length of the suspension "
                  "or revocation. There is no universal term to count from. "
                  "The requirements page in e-Services is the only place your "
                  "answer exists, and checking it takes less time than "
                  "reading this paragraph did."),
            ("h2", "What a lapse costs, roughly"),
            ("p", "Another round of reinstatement fees, the administrative "
                  "time of reapplying, however many days you are not driving "
                  "while it clears, and — if you were on a restricted license "
                  "for work — the risk to your job. Set against a failed $90 "
                  "auto-payment, the asymmetry is not close."),
            ("p", "Autopay, an annual check that the card on file has not "
                  "expired, and a diary note for your actual end date "
                  "eliminate nearly all of it."),
        ],
    },

    # ---------------------------------------------------------------- 7 ----
    {
        "slug": "sr22-fr44-sr50-difference",
        "title": "SR-22, FR-44, SR-50: Which One Does Tennessee Use?",
        "dek": "Three certificate names circulate online. Only one of them "
               "shows up in Tennessee's published requirements.",
        "meta": "SR-22 vs FR-44 vs SR-50 explained. What Tennessee's "
                "Department of Safety actually requires, and how to check "
                "what your own record says.",
        "date": "2026-08-13",
        "tags": ["SR-22 basics", "Tennessee rules"],
        "tldr": "Tennessee's Department of Safety publishes an SR-22 "
                "requirement — a certificate of financial responsibility "
                "filed electronically by a licensed carrier. FR-44 and SR-50 "
                "are certificate types used by other states. If anyone tells "
                "you Tennessee needs one of those, ask them to show you the "
                "tn.gov page, then check your own requirements in e-Services.",
        "sources": ["fr", "eservices"],
        "related": ["how-long-sr22-tennessee", "moving-with-sr22-tennessee",
                    "owner-vs-non-owner-sr22"],
        "body": [
            ("p", "Financial-responsibility certificates have confusingly "
                  "similar names, they vary by state, and national insurance "
                  "content tends to describe all of them at once without "
                  "saying which applies where. Here is the practical version "
                  "for a Tennessee driver."),
            ("h2", "SR-22 — the one Tennessee uses"),
            ("p", "An SR-22 is a certificate of financial responsibility. It "
                  "is not an insurance policy and not a type of coverage — it "
                  "is proof, filed with the state, that a policy exists "
                  "meeting at least the minimum liability limits."),
            ("p", "In Tennessee the certificate must be filed electronically "
                  "with the Department of Safety by an insurance company "
                  "licensed through the Tennessee Department of Commerce and "
                  "Insurance to issue motor vehicle liability coverage in "
                  "Tennessee. You cannot file it yourself. The state's "
                  "minimum liability limits are 25/50/25."),
            ("h2", "FR-44 — a higher-limit certificate, used elsewhere"),
            ("p", "An FR-44 works like an SR-22 but certifies liability "
                  "limits well above a state's ordinary minimum, and it is "
                  "typically tied to alcohol-related convictions. It is used "
                  "by a small number of states — Florida and Virginia are the "
                  "ones people encounter — not everywhere."),
            ("p", "Tennessee's published financial responsibility guidance "
                  "describes an SR-22 requirement. If a website or a "
                  "salesperson tells you that you need an FR-44 in Tennessee, "
                  "the right response is to ask them which tn.gov page says "
                  "so, and then go look at your own reinstatement "
                  "requirements yourself."),
            ("h2", "SR-50 and the other numbers"),
            ("p", "SR-50 generally refers to a proof-of-insurance form rather "
                  "than an ongoing filing obligation, and where it exists it "
                  "is a point-in-time verification. You will also see SR-21 "
                  "and SR-26 mentioned: broadly, these are the accident-report "
                  "and cancellation-notice forms in the same family — the "
                  "SR-26 in particular is the notice a carrier sends when a "
                  "filed policy terminates, which is the mechanism behind a "
                  "lapse suspension."),
            ("note", "You do not need to learn this taxonomy. You need to "
                     "know which requirement is on your record — and that is "
                     "a lookup, not a research project."),
            ("h2", "The only check that matters"),
            ("p", "Open the Tennessee Department of Safety e-Services portal "
                  "and read your reinstatement requirements page. It lists "
                  "what the state wants from you by name. If SR22 is listed, "
                  "you need an SR-22. If it is not listed, you do not."),
            ("p", "That single page settles every version of this question, "
                  "including the ones a national comparison site cannot "
                  "answer about you specifically."),
            ("h2", "Why the confusion persists"),
            ("p", "Most SR-22 content online is written to rank nationally, "
                  "so it describes a generic blend of every state's rules and "
                  "hedges the details. That is also why so many pages say "
                  "Tennessee SR-22s last three years — a real rule, in other "
                  "states. Tennessee ties the period to the length of your "
                  "suspension or revocation instead."),
            ("h2", "What an SR-22 is not"),
            ("p", "Clearing up the other half of the confusion is just as "
                  "useful:"),
            ("ul", [
                "It is not a type of insurance. There is no such product as "
                "\"SR-22 insurance\" separate from an auto policy — the "
                "certificate rides on top of an ordinary liability policy.",
                "It is not extra coverage. It certifies that coverage exists; "
                "it adds nothing to what you are protected against.",
                "It is not something you file. In Tennessee the carrier "
                "transmits it electronically, and it must be a carrier "
                "licensed through the Department of Commerce and Insurance to "
                "write motor vehicle liability coverage here.",
                "It is not proof of insurance for a traffic stop. Your "
                "insurance card is that. The SR-22 is a filing with the "
                "state.",
                "It is not a penalty in itself. The premium increase comes "
                "from the violation on your record, not from the certificate.",
            ]),
            ("h2", "Why the higher-limit version exists at all"),
            ("p", "The reasoning behind an FR-44 is that a driver with an "
                  "alcohol-related conviction represents enough additional "
                  "risk that the state's ordinary minimum limits are not "
                  "adequate protection for other people on the road. States "
                  "that use it typically require substantially higher bodily "
                  "injury and property damage limits than their standard "
                  "financial responsibility floor."),
            ("p", "Tennessee's published minimums for financial "
                  "responsibility are 25/50/25. Nothing stops you from "
                  "carrying more, and after a serious at-fault loss there is "
                  "a genuine argument for it — the minimums are a compliance "
                  "floor, not a recommendation."),
            ("h2", "If you have requirements in two states"),
            ("p", "This is where the naming actually starts to matter. "
                  "Someone who was convicted in Florida and now lives in "
                  "Nashville may owe Florida an FR-44 and owe Tennessee "
                  "nothing, or may owe both states something. The obligation "
                  "belongs to whichever state ordered it, and moving does not "
                  "clear it."),
            ("p", "That situation needs a carrier licensed to make the filing "
                  "in the originating state, which is not every carrier. It "
                  "is one of the few genuinely good reasons to work through "
                  "an independent agency rather than an online quote form."),
            ("note", "Whatever anyone tells you the requirement is called, "
                     "the tie-breaker is the same: your reinstatement "
                     "requirements page in the relevant state's system. Read "
                     "it before you buy."),
        ],
    },

    # ---------------------------------------------------------------- 8 ----
    {
        "slug": "moving-with-sr22-tennessee",
        "title": "Moving To or From Tennessee With an SR-22",
        "dek": "The obligation belongs to the state that ordered it. Crossing "
               "a state line does not clear it.",
        "meta": "Moving to Nashville with an out-of-state SR-22, or leaving "
                "Tennessee with one? Which state's filing you still owe, and "
                "what Tennessee actually publishes about waivers.",
        "date": "2026-08-13",
        "tags": ["Out of state", "Tennessee rules"],
        "tldr": "An SR-22 obligation belongs to the state that ordered it, "
                "and moving does not satisfy it. If you moved to Tennessee "
                "with an out-of-state requirement, that state still needs its "
                "filing. If you have a Tennessee requirement and moved away, "
                "get a written answer from the Department of Safety's "
                "Financial Responsibility office rather than assuming a "
                "waiver applies.",
        "sources": ["fr", "interlock", "statute_114", "eservices"],
        "related": ["sr22-fr44-sr50-difference", "how-long-sr22-tennessee",
                    "sr22-lapse-tennessee"],
        "body": [
            ("p", "Nashville absorbs a lot of new residents, and Clarksville "
                  "in particular sees constant movement through Fort Campbell. "
                  "So the two versions of this question come up all the time, "
                  "and both have the same underlying answer: the filing "
                  "belongs to whichever state ordered it."),
            ("h2", "You moved to Tennessee with an out-of-state SR-22"),
            ("p", "The state that suspended or revoked your license is the "
                  "one whose requirement you are satisfying. Getting a "
                  "Tennessee license does not clear it, and a Tennessee-only "
                  "policy without a filing to that state does not either."),
            ("p", "What you generally need is a policy that can produce the "
                  "filing the originating state expects, from a carrier "
                  "licensed to make that filing there. Not every carrier "
                  "writes in every state, which is a large part of why this "
                  "situation is worth handing to an independent agency rather "
                  "than solving with an online quote form."),
            ("p", "Two things to nail down before buying anything: which "
                  "state's filing you owe, and whether you also have a "
                  "Tennessee requirement now — those are separate questions "
                  "with separate answers."),
            ("h2", "You have a Tennessee SR-22 and moved away"),
            ("p", "Here is where we part company with most SR-22 sites, which "
                  "state confidently that Tennessee will waive the "
                  "requirement for out-of-state residents if your new state's "
                  "driver services office signs a form."),
            ("p", "What Tennessee clearly publishes is an out-of-state waiver "
                  "process for the <em>ignition interlock</em> requirement: "
                  "you submit a waiver request, your out-of-state licensing "
                  "authority completes the form, and it goes to the "
                  "department for approval — and if your home state will not "
                  "approve it, Tennessee's interlock requirements still "
                  "apply."),
            ("p", "We were not able to confirm an equivalent published SR-22 "
                  "waiver form on tn.gov. It may exist as an internal "
                  "process. But we are not going to tell you a requirement "
                  "will be waived on the strength of other websites saying "
                  "so, because if it is not, you find out via a suspension."),
            ("note", "Call the Department of Safety's Financial "
                     "Responsibility office and get the answer for your "
                     "record in writing. Then act on that. This is a "
                     "ten-minute call that protects a license."),
            ("h2", "What Tennessee law contemplates"),
            ("p", "Tennessee's financial responsibility statute does address "
                  "residents moving to or returning from another state, "
                  "alongside the registration consequences of a suspension "
                  "(T.C.A. Sec. 55-12-114). If your situation involves a move "
                  "in either direction, it is worth knowing the law "
                  "anticipates it rather than assuming you have fallen "
                  "through a crack."),
            ("h2", "Practical sequence for either direction"),
            ("ol", [
                "Pull your Tennessee reinstatement requirements from "
                "e-Services, so you know what this state wants.",
                "Contact the other state's driver services or financial "
                "responsibility office and ask what they still require of "
                "you, and get it in writing.",
                "Take both answers to an independent agency and ask for "
                "coverage that satisfies whichever filings are live.",
                "Do not cancel anything until both states' records show you "
                "clear. A lapse in either one restarts that state's process.",
            ]),
            ("h2", "The Clarksville case specifically"),
            ("p", "If you are stationed at Fort Campbell, you may hold a "
                  "license from a home-of-record state, live in Tennessee, "
                  "and have a citation from either side of the Kentucky line. "
                  "Sort out which state issued the order before you buy "
                  "insurance. It is the question that determines everything "
                  "else, and it is the one most often skipped."),
            ("h2", "Why a new license does not clear an old filing"),
            ("p", "States share driver records. Getting a Tennessee license "
                  "does not erase another state's requirement, and in "
                  "practice an unresolved out-of-state suspension tends to "
                  "surface at exactly the wrong moment — when you try to "
                  "convert your license, or after a traffic stop."),
            ("p", "The reverse is also true. Leaving Tennessee with an open "
                  "requirement does not close it. It sits on your record "
                  "until it is satisfied or the department releases it."),
            ("h2", "The interlock waiver, precisely"),
            ("p", "Since this is the one out-of-state process Tennessee "
                  "clearly documents, it is worth stating exactly how it "
                  "runs: you submit the waiver request through the "
                  "department's support portal, your out-of-state licensing "
                  "authority completes the waiver form, and the completed "
                  "form goes to the department for approval."),
            ("p", "The critical detail is the failure mode. If your home "
                  "state will not complete and approve the waiver, "
                  "Tennessee's interlock requirements still apply to you. The "
                  "waiver is a request, not an entitlement, and it depends on "
                  "another state's cooperation."),
            ("h2", "Why we hedge on the SR-22 waiver"),
            ("p", "It would be easier to write the confident version. Every "
                  "competing page does. But the cost of being wrong is "
                  "asymmetric: if you cancel a filing on the strength of a "
                  "waiver that does not apply to you, the consequence is a "
                  "suspension for Failure to Maintain Future Proof of "
                  "Financial Responsibility — refiling, fees again, "
                  "reapplying."),
            ("p", "So the recommendation is boring and correct. Ask the "
                  "department, get the answer for your record in writing, and "
                  "keep the filing running until you have it."),
            ("h2", "Buying coverage across two states"),
            ("ul", [
                "Not every carrier is licensed to make a filing in every "
                "state. The question to ask is not \"do you write SR-22s\" "
                "but \"can you file to this specific state.\"",
                "A non-owner policy is often the practical answer for someone "
                "satisfying another state's requirement while living here "
                "without a car titled to them.",
                "Keep documentation of both states' requirements. When one "
                "closes, you want to be able to prove it.",
                "Do not let either filing lapse while you sort the other out. "
                "Each state's clock runs independently.",
            ]),
            ("note", "If you are moving in either direction, start these "
                     "calls before the move, not after. Both departments are "
                     "easier to deal with while you still have a working "
                     "license and a stable address."),
        ],
    },
]
