# Importing this builder into Genspark (or any other LLM workspace)

This package is tool-agnostic. It does not depend on Kimi. Any AI coding
environment that can (a) read uploaded files and (b) run `python3` commands
can operate it. Python 3 standard library only — no pip installs, ever.

## How to get the files in

**Option A — GitHub (preferred).** The builder lives in a private repo.
Paste the repo URL into your Genspark chat and tell the agent to clone it
into the workspace:

    https://github.com/jgitlin01/sr22-site-builder

or run `git clone https://github.com/jgitlin01/sr22-site-builder` if the
environment gives you a terminal.

**Option B — zip upload.** If the platform accepts zip uploads, use
`sr22-site-builder-portable-v2.zip` and unzip it in the workspace. (Genspark
rejected this format at last attempt — use Option A.)

Then paste the contents of **`KIMI-PROMPT-SR22.md`** as your kickoff
instruction, filling in the target city/state/domain.

## First message to paste (adapt the bracketed parts)

> Read `sr22-site-builder/README-FOR-ANOTHER-LLM.md` first, then
> `RESEARCH-PROTOCOL.md`, then `MASTER-PROMPT.md` (same folder). Follow them strictly.
> The target is [CITY], [STATE] — domain [DOMAIN]. Research the state, county,
> and city SR-22 rules from primary sources before writing any content.
> Business address: [ADDRESS]. Hours: [HOURS]. Leave the phone number and
> email as placeholders. Scaffold the project, generate, and validate until
> the validator passes with no failures.

## The Google Places API key (location photos)

Location photos need a Google Places API key. The key is **not** in this
package on purpose — never upload a live key to a third-party platform
inside a zip.

1. Copy `.env.example` to `.env` in the project root.
2. Paste your key: `GOOGLE_PLACES_API_KEY=AIza...`
3. Run `python3 fetch_photos.py` from the project root, then review the
   contact sheets per `references/photo-pipeline.md`, approve, and re-run
   `python3 generate.py`.

Everything else works with no key — the site just ships gradient heroes.

## Build loop

```bash
python3 scripts/scaffold.py --dir ./client-project --company "…" \
  --niche "SR-22 / high-risk auto insurance" --city … --state … --domain … --palette navy
cd client-project
python3 generate.py        # builds every page
python3 validate_site.py   # THE FAILURES ARE YOUR TO-DO LIST
```

Generate → validate → fix → repeat until PASS.

## Deploying to Vercel

- The project is plain static HTML/CSS/JS. Import the folder into Vercel,
  no build command, no framework preset.
- While the site is in preview, copy `scripts/vercel.json.example` to the
  project root as `vercel.json` — it sends `X-Robots-Tag: noindex` on every
  response so Google never indexes the placeholder build.
- At launch: set `PREVIEW = False` in `config.py`, regenerate, and delete
  `vercel.json` (or remove the header block).

## Fixes folded into v2 (vs the original zip)

- **`base/assets/css/sr22.css` added.** The original zip referenced this
  stylesheet but did not include it — pages rendered unstyled. This is the
  real file from the deployed Austin build (navy `#0B2545` / amber `#F2B441`,
  all `sr22-*` components and the default hero gradient).
- **`.env.example` added** so the photo step is discoverable.
- **`scripts/vercel.json.example` added** for noindex preview deploys.

Everything else is byte-identical to the original package.
