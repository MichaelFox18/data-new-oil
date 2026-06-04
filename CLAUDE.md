# CLAUDE.md — "Data Was Never the New Oil" Data Analysis

This file is the operating manual for the data-analysis phase of a Maxinomics-style
documentary video. Read it fully at the start of every session and follow it. When this
file and a casual instruction conflict, follow this file unless the human explicitly
overrides it in writing.

---

## 1. Mission

We are sourcing and analyzing real data to find **legitimately novel, meaningful,
evidence-backed insights** for a ~20-minute documentary on the data economy.

Working thesis the film argues (this frames *what is worth investigating*, it is **not**
a conclusion to confirm — we follow the data even if it kills the thesis):

> "Data is the new oil" gets the metaphor backwards. Oil is *consumed*; data is *copied*,
> so it should be impossible to run out of. Yet AI is hitting a wall — not a depleted
> stock but an exhausted *flow* of new human text. We have heard "we're running out"
> before, about oil, for a century, and new extraction tech deferred it every time.
> Data's "fracking" is synthetic data. Open question: does it defer the wall forever, or
> trigger model collapse — the one failure mode oil never had?

**The bar.** This is for a channel whose reputation rests on rigor and original analysis.
Every number that could appear on screen must survive a fact-check that traces it to a
primary source or to our own reproducible computation. A single fabricated or
misremembered statistic is a project-level failure. We would rather ship three
bulletproof insights than ten shaky ones.

---

## 2. THE PRIME DIRECTIVE — no hallucinations

These rules are absolute. They override speed, helpfulness, and narrative convenience.

1. **Every number traces to one of two things, never a third.**
   - (a) Code in `src/` that computes it from a file in `data/raw/`, **or**
   - (b) A direct quote from a source logged in `data/PROVENANCE.md` with exact URL and
     retrieval date.
   There is no third source. "I recall that the figure is ~X" is **not** a source.

2. **Never state a statistic, date, name, or quote from memory.** If you recall one
   (including any number in this file or in the pitch/stat-bank docs), treat it as an
   *unverified hypothesis* to confirm against a freshly fetched source — or drop it. The
   numbers in our own pitch documents are starting leads, not facts.

3. **Missing data is reported, never filled.** If you don't have the data to answer
   something, write `NO DATA` or `UNVERIFIED` and stop. Do not estimate, interpolate,
   extrapolate, or substitute a "plausible" value unless the human explicitly asks for an
   estimate — and then it must be labeled `MODELED` with the method shown.

4. **No invented anything.** Never fabricate a URL, dataset, DOI, author, institution,
   quote, table, or row. If you cannot fetch it, you cannot cite it. Do not guess URL
   structures or API endpoints — verify them live before relying on them.

5. **Label every claim by type** (see §3): `MEASURED`, `REPORTED`, or `MODELED`.

6. **Raw data is immutable.** Files in `data/raw/` are never edited. Every transformation
   happens in code and writes to a new location. Any result must be reproducible by
   re-running the pipeline from raw.

7. **Single-source claims are flagged as such.** Prefer triangulation across two
   independent sources. Never launder a Tier-C aggregator (§4) into a citation.

8. **Surprising results get more scrutiny, not less.** A startling finding is first
   assumed to be a bug, a data artifact, or a confound until the pipeline is re-verified
   and an alternative explanation is ruled out.

9. **When uncertain, stop and ask the human.** Flagging uncertainty is success. Guessing
   to seem complete is the failure mode this whole document exists to prevent.

10. **Do not present known facts as discoveries.** A finding is only an "insight" after it
    passes the novelty test (§11).

If you are ever tempted to write a number you did not compute or fetch in this session,
that impulse is the exact moment to stop and run the verification path instead.

---

## 3. Claim taxonomy — how to write every quantitative statement

Tag each claim in findings, results, and the final fact-check with its type:

- `MEASURED` — we computed it from raw data we hold. Must reference the script and the
  raw source. Example: "MEASURED: 1,287 unique data brokers across the four state
  registries after dedupe (`src/analyze/broker_census.py`, raw: CA/VT/TX/OR registries,
  retrieved 2026-06-xx)."
- `REPORTED` — a source states it; we are quoting, not measuring. Must reference the
  PROVENANCE id. Example: "REPORTED (Epoch AI, 2024): 80% CI for full use of human text
  stock is 2026–2032."
- `MODELED` — we estimated/projected it. Must show the method, inputs, and assumptions,
  and give a range, not a false-precision point.

Always attach, for any quantitative claim: the **n / coverage**, the **time window**, the
**source or script**, and a one-line **caveat** if the figure is soft.

---

## 4. Source reliability tiers + named source map

**Tiers (a citation-quality control):**
- **Tier A — primary / authoritative, machine-verifiable.** Government data, regulator
  registries, company filings, the originating research group's own published dataset,
  official statistical agencies. On-screen claims should rest here wherever possible.
- **Tier B — reputable secondary.** Peer-reviewed papers, established outlets reporting
  first-hand, named analysts. Usable, ideally corroborated by a Tier-A source.
- **Tier C — aggregators / SEO stat round-ups / blogs.** **Never cited.** Use only as a
  lead to find the underlying Tier-A/B primary, then cite the primary.

**Candidate primary sources (verify exact access at fetch time — do not assume
endpoints).** Mapped to where each is most useful:

- **Epoch AI** — published datasets on AI model training (dataset sizes, compute, dates)
  and their data-stock work. *Chapters 4–7, the hero crossover.* Tier A for their own data.
- **SEC EDGAR** — 10-K/10-Q filings and structured company-facts data for Meta, Alphabet,
  Reddit, Snap, etc.: revenue, ARPU, user counts, data-licensing line items. *Chapter 3,
  the "exhaust premium."* Tier A.
- **State data-broker registries** — California (CPPA), Vermont, Texas, Oregon. Public
  lists of registered brokers, some with consumer-request reporting. *Chapters 2–3, the
  broker census.* Tier A. (Confirm each state's current download/registry mechanism.)
- **EIA** (US Energy Information Administration) — historical oil production and reserves;
  open data API and downloads. *Chapter 6, the Hubbert-vs-actual overlay.* Tier A.
- **Google Books Ngram** — downloadable n-gram frequency corpora. *Chapter 6, empirical
  "panic frequency" of phrases like "peak oil" over time.* Tier A as raw corpus.
- **arXiv / Semantic Scholar / OpenAlex** — paper metadata APIs. *Chapters 5–7,
  bibliometric trends (e.g., rise of "synthetic data" / "data licensing" in the
  literature).* Tier A/B.
- **Common Crawl / Hugging Face Datasets** — to characterize the actual scale of public
  web/training corpora. *Chapter 4.* Tier A for documented dataset stats.
- **FRED** (St. Louis Fed) and **Our World in Data** — macro series and clean long-run
  series (GDP to size the ad economy, internet adoption). Tier A/B; OWID restates sources,
  so cite OWID's underlying source where it matters.
- **Pew Research Center** — public attitudes/usage microdata (downloadable). *Human layer.*
  Tier A/B.

Reports such as IDC, Statista, Gartner, DataReportal, WARC are **REPORTED** context, often
behind paywalls and frequently restated by Tier-C sites. Treat their numbers as quotes to
attribute, never as data we measured, and find the primary release where possible.

---

## 5. Repository structure

```
project/
  CLAUDE.md                 # this file
  README.md                 # how to reproduce end-to-end
  run.sh | Makefile         # one command rebuilds results/ and figures/ from raw
  requirements.txt          # pinned deps
  .env.example              # NAMES of required API keys only — never real values
  .gitignore                # .env, large raw blobs if needed, secrets, caches
  data/
    raw/                    # IMMUTABLE. one subdir per source. never edited.
    interim/                # cleaned/derived datasets (produced by code only)
    PROVENANCE.md           # the source ledger (§7) — append-only
  src/
    acquire/                # one fetcher per source; writes to data/raw + logs provenance
    validate/               # profiling + integrity checks
    analyze/                # one script per research question; writes to results/
    viz/                    # one script per figure; reads results/, writes figures/
  results/                  # computed outputs (JSON/CSV) that feed claims AND charts
  figures/                  # regenerable charts (no hand-edited numbers)
  findings/                 # one finding card per insight (§8)
  notebooks/                # exploration ONLY; never the source of truth
  logs/                     # fetch logs, run logs (timestamps, row counts, hashes)
  FACTCHECK.md              # final: every on-screen number -> source + script (§14)
```

Rule of separation: **raw → interim → results → figures/findings**, one direction only.
Numbers flow forward through code; they never flow backward by hand.

---

## 6. Conventions & tooling

- Python 3.x with `pandas` or `polars`; `requests`/`httpx` for fetching; `matplotlib` for
  figures. Pin versions in `requirements.txt`.
- **Determinism:** set and record random seeds; sort before sampling; no nondeterministic
  outputs in results.
- **Scripts are the source of truth, notebooks are not.** Anything that produces a number
  used in a finding lives in `src/` and is re-runnable headless. Notebooks are scratch.
- **Idempotent + summarized:** each script reads from declared inputs, writes declared
  outputs, prints a short summary (rows in, rows out, key stats), and can run twice with
  the same result.
- **No hand-typed numbers in outputs.** Final claims and chart labels are injected from
  `results/*.json`. If a number isn't in `results/`, it cannot appear in a finding.
- **Reproducibility:** `run.sh`/`Makefile` regenerates `results/` and `figures/` from
  `data/raw/` with no manual steps. Commit per phase. Commit the PROVENANCE ledger.

---

## 7. Provenance ledger format (`data/PROVENANCE.md`, append-only)

One block per fetched source. Filled in at acquisition time, before any analysis uses it.

```
### SRC-007  CPPA Data Broker Registry
- name:           California data broker registry
- url:            <exact URL fetched>
- access_method:  download | api | scrape
- retrieved_at:   2026-06-xx HH:MM UTC
- raw_path:       data/raw/cppa/registry_2026-06-xx.csv
- sha256:         <hash of the raw file>
- rows / size:    <count> rows
- license/terms:  <note; for scraping, robots.txt + ToS status and human approval ref>
- tier:           A
- caveats:        <known gaps, e.g., self-registration only; some brokers missing>
```

If any field can't be filled (e.g., no hash because the source is a live API), say so
explicitly; never leave a blank that looks complete.

---

## 8. Finding card template (`findings/F-XX.md`)

No insight is "done" until its card is complete and status is `VERIFIED`.

```
# F-03  Title of the finding

CLAIM (one sentence, specific, falsifiable):
  e.g. "After dedupe, the four public state registries list N unique data brokers,
  Z% of which self-report collecting precise geolocation."

TYPE:        MEASURED | REPORTED | MODELED
NUMBERS:     the exact figure(s), with units
SOURCES:     PROVENANCE ids (+ tier). Triangulated? (Y/N — if N, flag.)
METHOD:      script path; one-paragraph plain-English description of how it's computed
COVERAGE:    n / rows / time window / what's excluded
CONFIDENCE:  High | Medium | Low  — and the single biggest reason for that rating
NOVELTY:     prior-art check result (§11): is this already widely stated? what's new here?
ALTERNATIVES: alternative explanations / confounders considered and how addressed
ROBUSTNESS:  checks run (re-run from raw, leave-one-source-out, sanity anchors, etc.)
VISUAL:      proposed chart + the results/ file that feeds it
CHAPTER:     which of the 7 chapters it serves
STATUS:      DRAFT | VERIFIED | REJECTED | NEEDS-DATA
```

A `REJECTED` card stays in the repo. Negative results are results and protect us from
re-chasing dead ends.

---

## 9. The phases

Work strictly in order. Each phase ends with a **GATE** — a checklist that must pass
before the next phase starts. Do not skip ahead to analysis because a dataset looks
promising; the gates are what keep numbers honest.

### Phase 0 — Setup
- Create the repo structure (§5), `requirements.txt`, `.env.example`, `.gitignore`,
  `run.sh`/`Makefile` skeleton, empty `PROVENANCE.md` and `FACTCHECK.md`.
- Confirm secrets handling: keys read from environment only; `.env` gitignored; no key
  ever printed to logs or committed.
- **GATE 0:** repo builds; `.gitignore` confirmed to exclude `.env`; a dummy script runs
  via `run.sh`.

### Phase 1 — Questions & hypotheses
- Translate the thesis into a numbered list of **specific, falsifiable, data-answerable
  questions** (e.g., "How many unique data brokers exist across the four public
  registries, and how has that count grown by registration year?").
- For each: state what would confirm vs. refute it, what data it needs, and which
  candidate source(s) could supply it. Mark expected-but-worth-quantifying vs.
  genuinely-open.
- **GATE 1:** human reviews and approves the question list and priorities. Do not acquire
  data for questions not on the approved list without flagging it.

### Phase 2 — Source mapping & acquisition plan
- For each approved question, identify candidate sources, tier them (§4), and pick the
  access mode (prefer official download/API over scraping — see §10).
- For any scraping: record the robots.txt/ToS status and **get explicit human approval per
  source** before fetching (§10). Booking responsibility for legality sits with the human.
- **GATE 2:** human approves the source list and any scraping. No fetch without this.

### Phase 3 — Acquisition & raw archival
- Write one fetcher per source in `src/acquire/`. Each: pulls the data, writes the raw
  artifact to `data/raw/<source>/`, computes its hash, and **appends a PROVENANCE entry**
  (§7) plus a line in `logs/`.
- Respect rate limits; cache; never re-hammer a source. API keys from env only.
- Do not transform during acquisition — store exactly what was returned.
- **GATE 3:** every fetched source has a complete PROVENANCE entry with hash, row count,
  and retrieval time. Raw row/record counts spot-checked against the source's own stated
  totals where available (catch silent truncation/pagination loss).

### Phase 4 — Validation & cleaning
- Profile each raw dataset: schema, types, ranges, null rates, duplicates, encoding,
  obvious anomalies. Write a short data-quality note per source.
- Build cleaned `data/interim/` datasets **only via scripts**, with a logged cleaning
  decision list (what was dropped/normalized and why). Keep raw untouched.
- Sanity-check against known anchors (a figure the source itself publishes) to confirm the
  pipeline reads the data correctly — without treating the anchor as a target to hit.
- **GATE 4:** for each dataset, schema documented, known issues listed, cleaned output
  reproducible from raw, and at least one read-correctness sanity check passes.

### Phase 5 — Analysis & discovery
- One script per question in `src/analyze/`, each writing its outputs to `results/` as
  JSON/CSV. Start with honest EDA; let the data speak before forcing the narrative.
- Pursue the original computations (§11 backlog) — these are where real novelty lives.
- Triangulate where possible; note where you can't.
- Draft a finding card (§8) for each candidate insight, status `DRAFT`.
- **GATE 5:** every `DRAFT` finding has a runnable script, a `results/` artifact, and a
  filled card. No finding rests on a number not in `results/`.

### Phase 6 — Verification & red-team
- For each `DRAFT` finding, independently re-derive the number (re-run from raw; where
  feasible, a second method or second source).
- Adversarial pass: alternative explanations, confounders, base rates, selection bias,
  survivorship, definitional drift, data-quality artifacts. Write these into the card's
  ALTERNATIVES/ROBUSTNESS fields.
- Promote to `VERIFIED` only if it survives. Otherwise `REJECTED` or `NEEDS-DATA` with a
  note.
- **GATE 6:** human reviews every card moving to `VERIFIED`. Surprising findings get an
  explicit "is this a bug?" review before acceptance.

### Phase 7 — Synthesis & narrative mapping
- Rank `VERIFIED` findings by strength x novelty x visual potential. Map each to a chapter.
- Produce the consolidated `results/` files that feed the figures and the script (e.g.,
  the crossover data + the synthetic-data "deferral overlay" series, if the data supports
  one; the broker-census tables; the ARPU-vs-data-price comparison).
- Generate figures from `results/` only (`src/viz/`), labels injected from data.
- **GATE 7:** every figure regenerates from `run.sh`; every label/number on every figure
  is present in a `results/` file.

### Phase 8 — Handoff to production
- Write `FACTCHECK.md` (§14): every number intended for the video, paired with its claim
  type, source/script, and the command to reproduce it.
- Ensure `run.sh` rebuilds the world from `data/raw/`. Commit everything including raw
  manifests.
- **GATE 8:** a clean checkout + `run.sh` reproduces all `results/` and `figures/`; every
  `FACTCHECK` line resolves to a source or a script.

---

## 10. Data acquisition discipline (API keys, downloads, scraping)

**Order of preference:** official bulk download > official API > scraping. Scrape only
when no download/API exists.

**API keys & secrets:**
- Read from environment variables / a gitignored `.env`. List required key *names* (never
  values) in `.env.example`.
- Never hardcode, never commit, never print keys (including in error messages or logs).
- If a required key is missing, stop and ask — do not proceed with fabricated or empty
  auth.

**Downloads:** save the exact file to `data/raw/`, hash it, log provenance. Note the file
version/date the source assigns.

**Scraping (only with per-source human approval):**
- Check and respect `robots.txt` and the site's Terms of Service. If disallowed or
  ambiguous, stop and ask the human; do not proceed on assumption.
- Rate-limit, set a descriptive User-Agent, cache every response into `data/raw/`, and
  never re-request what you already have.
- Prefer public, factual records (e.g., government registries) over anything behind a
  login or paywall. Do not attempt to bypass access controls.
- Record the robots/ToS status in the PROVENANCE entry.

---

## 11. The novelty bar — what counts as a "legitimately new insight"

A `DRAFT` finding becomes a real candidate insight only if it clears all three:

1. **Specific & falsifiable.** A precise claim with a number, a comparison, or a trend —
   not a vibe.
2. **Grounded.** `MEASURED` from data we hold, or `REPORTED` and triangulated. Not a
   memory, not a guess.
3. **Prior-art checked.** Before calling something an insight, check whether it's already
   widely stated in this exact form (quick literature/news/search pass, logged in the
   card). If it's common knowledge, either find the sharper original cut (a number nobody
   has computed, a comparison nobody has drawn) or demote it to "supporting context."

Avoid **insight theater**: a well-known fact restated confidently is not a discovery. The
value is in computations others haven't bothered to do.

**Candidate original analyses to test (hypotheses, not promises — expect some to fail):**
- **Broker census.** Merge + dedupe the four state registries into the most complete public
  count; categorize by type; quantify how many self-report collecting geolocation or
  minors' data; trend registrations by year; map HQ geography.
- **The recomputed crossover.** From Epoch AI's dataset, recompute the historical growth
  rate of training-set size and the human-text-stock comparison with the latest models;
  build the hero chart from first-party numbers rather than a screenshot.
- **The deferral overlay.** If the data supports it, add a "fracking" line (effective data
  including synthetic generation) to show the wall sliding right — and state honestly where
  that line is `MODELED`.
- **Exhaust premium.** From SEC filings, compute revenue-per-user / ARPU for the big
  data-driven platforms and contrast with the ~$0.36 a person's raw data reportedly sells
  for. ("Your data sells for cents; your attention earns platform X $N/year.")
- **Panic-frequency bibliometric.** From Google Books Ngram and/or arXiv metadata, chart how
  often "peak oil" (historically) and "data wall"/"synthetic data" (recently) appear over
  time — an empirical picture of recurring scarcity narratives.
- **Hubbert vs actual.** From EIA data, recreate the 1956 prediction against actual US
  production, annotating where shale broke the forecast — the visual spine of Chapter 6.

---

## 12. Verification & red-team protocol (applied in Phase 6, and to anything surprising)

For each candidate insight, before it can be `VERIFIED`:
- Re-derive the number from `data/raw/` by re-running the pipeline. Numbers must match.
- Where possible, reproduce by a second method or a second independent source.
- Ask: could this be a definitional artifact (units, what's counted), a coverage gap, a
  duplicate-inflation, a base-rate illusion, a time-window cherry-pick, or a parsing bug?
- State the strongest alternative explanation and why the data still supports the claim.
- For any `MODELED` number: show inputs, assumptions, and a sensitivity range.

---

## 13. Human checkpoints (do not pass without sign-off)

- **GATE 1:** approval of the question list.
- **GATE 2:** approval of sources and any scraping (legality).
- **GATE 6:** approval of each finding promoted to `VERIFIED`.
- **GATE 8:** approval of `FACTCHECK.md` before anything goes into the script.

At each, present a concise summary and wait. When unsure between checkpoints, ask.

---

## 14. Definition of done & final deliverables

The analysis is done when:
- `results/` holds every number any finding or figure uses, each regenerable from raw.
- `findings/` holds a complete card per insight, each `VERIFIED` or explicitly `REJECTED`.
- `figures/` regenerate from `run.sh` with all labels sourced from `results/`.
- `FACTCHECK.md` lists every video-bound number with: the claim, its type
  (`MEASURED`/`REPORTED`/`MODELED`), source/PROVENANCE id or script path, tier, and the
  exact command to reproduce it.
- A fresh checkout + `run.sh` reproduces `results/` and `figures/` end-to-end.

`FACTCHECK.md` line format:
```
- CLAIM: "<one line>"  | TYPE: MEASURED | VALUE: <n> | SOURCE: SRC-007 (Tier A) |
  REPRODUCE: `python src/analyze/broker_census.py` | CONFIDENCE: High | CHAPTER: 3
```

---

## 15. Anti-patterns — quick do-not list

- Do **not** write a number you did not compute or fetch this session.
- Do **not** fill a data gap with a "reasonable" value (unless asked, and then label
  `MODELED`).
- Do **not** cite a source you have not actually retrieved, or guess a URL/DOI/endpoint.
- Do **not** cite Tier-C aggregators; chase the primary.
- Do **not** edit `data/raw/`. Do **not** hand-edit numbers in `results/` or figures.
- Do **not** treat the channel's own pitch/stat-bank numbers as verified — re-verify them.
- Do **not** let a surprising result skip scrutiny; assume bug-until-proven.
- Do **not** present common knowledge as a discovery.
- Do **not** proceed past a gate without its sign-off.
- When in doubt, **stop and ask.** That is the correct outcome, not a failure.
