# Phase 1 — Research questions & hypotheses

Per CLAUDE.md §9 (Phase 1). Each question is **specific, falsifiable, and
data-answerable**. For each: the claim, what would confirm vs. refute it, the data
it needs, candidate primary source(s) with tier, a tag
(`EXPECTED-BUT-WORTH-QUANTIFYING` vs. `GENUINELY-OPEN`), the chapter it serves, a
priority, and the main feasibility risk.

**Nothing here is a finding or a fact.** Every number named below — including those
carried over from the pitch — is an *unverified lead* to confirm against a freshly
fetched primary source, or to drop (CLAUDE.md §2). This list governs **what is worth
investigating**; it does not pre-commit any answer.

**This list requires GATE 1 sign-off before any data is acquired.**

Priority key: **P0** = load-bearing spine of the film · **P1** = strong original cut ·
**P2** = supporting / context, attempt if P0–P1 land.

---

## P0 — The spine (the two original analyses the film leans on hardest)

### Q1 — The broker census: how many, collecting what?
- **CLAIM:** After merging and deduping the four public state data-broker registries
  (California/CPPA, Vermont, Texas, Oregon), there are **N** unique brokers, of which
  **X%** self-report collecting precise geolocation and **Y%** collecting minors' data.
- **CONFIRM:** the four registries are downloadable, share enough identity fields to
  dedupe defensibly, and at least some expose geolocation/minors flags → a single
  deduped count + categorized shares.
- **REFUTE / DOWNGRADE:** registries are not machine-retrievable, lack common
  identifiers (dedupe intractable), or carry no collection-category fields → report
  what *is* available and mark the rest `NEEDS-DATA`.
- **DATA NEEDED:** current registry exports from all four states.
- **SOURCES:** CA CPPA registry; VT, TX, OR registries (Tier A; confirm each state's
  current download/registry mechanism at fetch time).
- **TAG:** registries existing is expected; the *merged national count* and the
  *geolocation/minors shares* are a **GENUINELY-OPEN** computation nobody publishes.
- **CHAPTER:** 2–3 · **RISK:** entity resolution across states (same broker, different
  spellings) is the hard part; field availability varies by state.

### Q3 — The recomputed crossover (hero visual)
- **CLAIM:** From Epoch AI's *own published data*, projected frontier-model training-set
  size meets the estimated stock of usable public human text within a datable window
  (the pitch's lead is ~2026–2032, central ~2028 — **to be reproduced, not assumed**).
- **CONFIRM:** Epoch's data-stock estimates and model-training-size series are
  retrievable as data (not just a chart image) and recombine into a crossover with an
  explicit uncertainty band.
- **REFUTE / DOWNGRADE:** the crossover exists only as a published figure we cannot
  rebuild from underlying numbers → cite it `REPORTED` and drop the "recomputed" claim.
- **DATA NEEDED:** Epoch's human-text-stock dataset + notable-models training-size data.
- **SOURCES:** Epoch AI published datasets / replication data (Tier A for their own data).
- **TAG:** **EXPECTED-BUT-WORTH-RECOMPUTING** — the published claim is known; the value
  is rebuilding it from first-party numbers rather than screenshotting it.
- **CHAPTER:** 5 · **RISK:** their projection involves modeling assumptions; we must
  separate what we *measure* from their data vs. what remains their `MODELED` estimate.

---

## P1 — Strong original cuts

### Q4 — How fast the appetite grew
- **CLAIM:** Notable-model training-set size has grown at **R** (doublings/year) over
  period **[t0, t1]**.
- **CONFIRM:** Epoch's notable-models dataset has dataset-size + date columns for enough
  models to fit a defensible rate.
- **REFUTE:** dataset-size is too sparsely populated → report coverage and widen error.
- **DATA:** Epoch AI notable-models dataset (Tier A).
- **TAG:** EXPECTED-BUT-WORTH-QUANTIFYING · **CHAPTER:** 4 · **RISK:** missing/uneven
  dataset-size reporting across models.

### Q5 — The deferral overlay (synthetic "fracking" line) — MODELED
- **CLAIM:** Adding a synthetic-data generation term to the human-text stock pushes the
  Q3 crossover right by **Δ years** under stated assumptions.
- **CONFIRM:** we can specify principled, sourced inputs (synthetic-volume growth,
  usable fraction) and produce a labeled `MODELED` line with a sensitivity range.
- **REFUTE / DECLINE:** no defensible inputs exist → say so honestly and present only
  the human-text crossover (the pitch's Gartner "synthetic overtakes real by 2030" is
  `REPORTED` context to attribute, not data we measure).
- **DATA:** Q3 base + explicit assumptions; Gartner projection as attributed context only.
- **TAG:** **GENUINELY-OPEN**, `MODELED` · **CHAPTER:** 7 · **RISK:** easy to overclaim;
  must stay explicitly modeled with shown inputs.

### Q6 — The exhaust premium: ARPU vs. the price of you
- **CLAIM:** Annual revenue-per-user for the major data-driven platforms (Meta,
  Alphabet, Snap, Reddit, Pinterest) is **$A–$Z**, vs. the reported **~$0.36** a
  person's raw data sells for — an **M×** gap.
- **CONFIRM:** filings disclose revenue + a user metric (MAU/DAU or stated ARPU) to
  compute per-user revenue directly; the $0.36 lead resolves to a citable primary.
- **REFUTE / DOWNGRADE:** the $0.36 has no traceable primary → keep ARPU as the
  `MEASURED` result and present the contrast only if/when the price figure is sourced
  (`REPORTED`), else mark `NEEDS-DATA`.
- **DATA:** SEC EDGAR filings (Tier A) for ARPU; a primary for the $0.36 data price.
- **TAG:** ARPU is EXPECTED-BUT-WORTH-COMPUTING; the *contrast* is the original cut.
- **CHAPTER:** 3 · **RISK:** the $0.36 figure's provenance; ARPU definitions vary by
  filer (regional ARPU, ad vs. total revenue) — must standardize.

### Q8 — Hubbert vs. actual: the forecast that shale broke
- **CLAIM:** Hubbert's 1956 logistic forecast for US crude production diverges from
  actual EIA production beginning ~**year**, by **magnitude**, at the shale inflection.
- **CONFIRM:** EIA long-run US production series is retrievable; Hubbert's original
  curve/parameters are sourced from the primary (digitized), not reconstructed.
- **REFUTE:** can't source Hubbert's actual stated curve → present actual production
  alone and treat the forecast qualitatively.
- **DATA:** EIA production data (Tier A); Hubbert 1956 original for the prediction curve.
- **TAG:** EXPECTED-BUT-WORTH-REBUILDING · **CHAPTER:** 6 · **RISK:** faithfully
  reproducing the *original* forecast (not a later idealized version) is the crux.

---

## P2 — Supporting / context (attempt after P0–P1)

### Q2 — Broker registration growth over time
- **CLAIM:** Registered-broker counts have grown **G%** by first-registration year.
- **CONFIRM/REFUTE:** registries expose a registration/first-year field. If absent →
  `NEEDS-DATA`. **SOURCES:** the four registries (Tier A). **TAG:** GENUINELY-OPEN ·
  **CHAPTER:** 3 · **RISK:** date fields often absent or reset annually.

### Q7 — The licensing scramble: documented deal scale
- **CLAIM:** Disclosed AI training-data licensing deals total/observably trend at
  **scale S** (pitch leads: News Corp $250M+, Reddit ~$60M/yr — **to verify**).
- **CONFIRM/REFUTE:** deals appear in filings / official statements (Tier A/B). Many
  are private → coverage is partial; flag it. **SOURCES:** SEC EDGAR (Reddit, News
  Corp), official press releases. **TAG:** GENUINELY-OPEN, partial-coverage ·
  **CHAPTER:** 6–7 · **RISK:** selection bias toward disclosed deals.

### Q9 — Panic-frequency: the recurring scarcity narrative
- **CLAIM:** The frequency of scarcity phrases ("peak oil" historically; "data
  wall"/"synthetic data" recently) rises and falls in measurable waves.
- **CONFIRM/REFUTE:** Google Books Ngram + arXiv metadata return phrase-frequency
  series. **SOURCES:** Google Books Ngram (Tier A raw); arXiv/OpenAlex (Tier A/B).
  **TAG:** GENUINELY-OPEN · **CHAPTER:** 6–7 · **RISK:** phrase choice and corpus
  end-dates (Ngram lags); normalize by total volume.

### Q10 — Recommendation & ad-economy scale (context)
- **CLAIM:** Recommenders drive a large share of engagement/sales and the ad economy is
  ~$1T scale (pitch leads: ~35% Amazon, ~80% Netflix, ~70% YouTube — **mostly
  aggregator-sourced; verify or demote**).
- **CONFIRM/REFUTE:** can we find first-party or peer-reviewed primaries? Expect several
  to be Tier-C-only → those become `REPORTED`-with-caveat or are dropped. **SOURCES:**
  company statements, IAB/eMarketer primary releases (attribute), academic papers.
  **TAG:** EXPECTED-BUT-FRAGILE · **CHAPTER:** 3 · **RISK:** these stats are heavily
  recycled without primaries; honesty about which survive matters more than keeping them.

### Q11 — The flow, not the stock: human text production rate
- **CLAIM:** New high-quality public human text is produced far slower than model data
  appetite grows — substantiating the "exhausted flow" framing.
- **CONFIRM/REFUTE:** a defensible proxy (Common Crawl growth, Wikipedia volume, arXiv
  output) can bound the production rate; likely `MODELED`/partial. **SOURCES:** Common
  Crawl stats, Wikipedia dumps, arXiv (Tier A for documented stats). **TAG:**
  GENUINELY-OPEN, possibly `NEEDS-DATA` · **CHAPTER:** 5 · **RISK:** "high-quality" is
  hard to operationalize; risk of an apples-to-oranges rate.

---

## Carried as REPORTED context only (not original analysis)
- **Model collapse** as a failure mode (Chapter 7) is a research-literature claim we
  would *cite* (`REPORTED`, from the primary papers), not something we measure. Logged
  here so it isn't mistaken for a data question.

## Notes for GATE 1
- Recommended build order: **Q3 + Q1 first** (the spine), then **Q4, Q6, Q8, Q5**,
  then P2 as time allows.
- Q5, Q10, Q11 carry the highest risk of `NEEDS-DATA`/`MODELED` outcomes — that is an
  acceptable result under the manual (negative results are results), not a failure.
- No data will be fetched for any question not approved here (CLAUDE.md §9, GATE 1).
