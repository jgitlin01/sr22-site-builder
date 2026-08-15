# SR-22 research protocol — do this before writing a single page

**SR-22 is state law. Every state is different, and most published content is
wrong about at least one state.** The value of this site is that it agrees with
the state's own agency. That only happens if you read the state's own pages.

Do not write copy from memory, from a competitor, or from a national
comparison site. Those are the sources that got it wrong in the first place.

---

## Step 1 — Find the state's own authority pages

Search for the agency, not the topic. Depending on the state it is a
Department of Motor Vehicles, Department of Safety, Department of Public
Safety, Department of Revenue, Secretary of State, or Department of
Transportation.

```
site:<state>.gov SR-22 financial responsibility
site:<state>.gov reinstatement requirements
site:dmv.<state>.gov certificate of financial responsibility
```

Record the exact URL of every page you use. Each one becomes an entry in
`config.SOURCES` and gets printed on the page that relies on it.

## Step 2 — Answer these, from the state's own pages only

| # | Question | Why it decides the whole site |
|---|---|---|
| 1 | **How long must the filing be maintained?** | The most-got-wrong fact in the niche. Some states are a flat 3 years. Tennessee ties it to the length of the suspension or revocation. Get this right and you beat every national page. |
| 2 | Who may file it, and how? | Most states require electronic filing by a carrier licensed in that state. The driver usually cannot self-file. |
| 3 | What are the minimum liability limits? | e.g. 25/50/25. Cite the statute number. |
| 4 | Which violations trigger it? | Use the state's own list and wording. |
| 5 | What happens if the policy lapses? | Usually re-suspension under a named rule. Get the rule's name. |
| 6 | What are the reinstatement fees? | And is there an instalment plan? TN: owe over $75 → $25 down, $75/quarter, up to 60 months. |
| 7 | Is there a restricted / hardship / occupational licence? | And what is the deadline? TN gives **10 days** from the judge's signature, with the SR-22 already in force. |
| 8 | Are ignition interlocks required, and for how long? | Minimum periods by offence number, any compliance window near the end, and the removal process. |
| 9 | Does the state use SR-22, FR-44, or something else? | FR-44 is Florida and Virginia. Do not assume. |
| 10 | What happens to drivers moving in or out of state? | Is there a published waiver? If you cannot confirm one, say so. |

## Step 3 — County and city layer

State law sets the rules; **counties and cities decide where you physically go**,
and that is the local differentiator no national competitor has.

For every city in the fleet, find:

- **The county** it sits in. Some cities straddle two — say so, because it
  changes which court has the case.
- **Which court clears the conviction.** Usually a General Sessions, District,
  Municipal or County Court. Link to the state court locator rather than
  hardcoding a schedule.
- **The nearest driver-services office**, with street address, phone and
  **service level**. This is the highest-value local fact on the whole site:
  many states run full-service offices, express offices and self-service
  kiosks, and **only full-service locations process reinstatements**. Sending
  someone to a kiosk wastes their afternoon.
- **Population**, with the census year labelled.
- **Any local condition that changes the job** — a military base nearby means
  constant out-of-state filings; a university means young drivers with short
  licensing histories; a commuter corridor means a suspension is a job risk.

## Step 4 — Write down what you could not confirm

Put it in `config.UNVERIFIED` and render it on the FAQ page under "What we
could not confirm". On the Tennessee build, the out-of-state SR-22 waiver could
not be verified on the state's site — only the interlock waiver is published —
so the page says exactly that and tells readers to get a written answer.

That section reads as credibility, not weakness, and it is precisely the kind
of honesty that makes an AI assistant cite you over a page that asserts
everything with equal confidence.

## Step 5 — Never invent

- Producer licence numbers, "licensed in <state>", years in business, ratings
- Any figure you did not read on the authority's page or a rate study you can
  name

Ship `[LICENSE #]`-style bracket placeholders instead, and tell the client in
writing that a licensed compliance reviewer must sign off before launch.
Insurance advertising is regulated by the state's insurance department.

---

## The output of this phase

A filled `config.SOURCES`, `KEY_FACTS`, `UNVERIFIED`, `CITIES` and `COUNTIES`,
where every claim traces to a URL you actually opened. Only then start writing.
