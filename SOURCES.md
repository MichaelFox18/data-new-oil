# Phase 2 — Source map & acquisition plan

Per CLAUDE.md §9 (Phase 2) and §10. Maps each GATE-1-approved question to candidate
primary sources, with access mode, tier, and — for any web source we'd fetch — the
**robots.txt / ToS status recorded before acquisition**. Prefer official
download/API over scraping.

**Status: planning only.** No data has been fetched into `data/raw/`; no PROVENANCE
entries written. That is Phase 3, and only after **GATE 2** sign-off — especially for
any scraping (CLAUDE.md §9/§10: legality approval is the human's, per source).

URLs below are *candidate* endpoints observed during recon; each is re-verified at
fetch time (CLAUDE.md §4 — do not assume endpoints). Every external number named here
is an **unverified lead**, not a fact.

Legend — **access:** `download` · `api` · `portal` (interactive, may need account) ·
`scrape` · `manual` (human pulls it). **tier:** A/B/C (§4).

---

## A. The broker census (Q1, Q2) — four state registries

The four states expose their registries very differently. This materially changes
what a "complete four-state census" can be: **2 clean, 1 conditional, 1 blocked.**

### CA — California Privacy Protection Agency (CPPA) Data Broker Registry
- access: **download** · tier: **A**
- candidate URL: `https://cppa.ca.gov/data_broker_registry/registry.csv`
  (registry page: `https://cppa.ca.gov/data_broker_registry/`)
- robots.txt (cppa.ca.gov, retrieved 2026-06-04): `Disallow: /images /js /ssi /css`
  only — the `data_broker_registry` path and the CSV are **allowed**.
- notes: CSV reportedly includes data-collection-category and recipient columns →
  directly supports the geolocation/minors shares in Q1. **No scraping needed.**

### VT — Vermont Secretary of State Data Broker registry
- access: **portal → manual** · tier: **A**
- candidate path: `bizfilings.vermont.gov` → Main Menu → "VT SEC OF STATE ONLINE
  SERVICES" → "Bulk Database Download" → Business/Registration Type = "Data Broker".
  Public registry search: `https://sos.vermont.gov/business-services/other-filings/data-broker`
- robots.txt (bizfilings.vermont.gov, 2026-06-04): **HTTP 403** to our automated
  request — the portal blocks non-browser access. Bulk download is real but
  interactive; **treat as a human/manual download**, not an automated fetch.
- notes: an official bulk export exists → high-quality once obtained; the open
  question is whether it requires an account.

### TX — Texas Secretary of State Data Broker Registry
- access: **scrape OR portal-api** (no bulk download) · tier: **A**
- candidate URL: `https://texas-sos.appianportalsgov.com/data-broker-registry`
  (info page: `https://www.sos.state.tx.us/statdoc/data-brokers.shtml`)
- robots.txt (texas-sos.appianportalsgov.com, 2026-06-04): **HTTP 404** — no
  robots.txt present (absence ≠ blanket permission; ToS still governs).
- notes: SOS page confirms **search-only, no bulk download**. The registry runs on
  Appian; Appian portals typically back the UI with a JSON data endpoint. **Preferred
  path: find that official data endpoint/export first; HTML scrape only as fallback,
  rate-limited + cached. Requires GATE 2 approval + a ToS check before any fetch.**

### OR — Oregon DCBS / Division of Financial Regulation Data Broker registry
- access: **BLOCKED for automated collection → manual / agency request** · tier: **A**
- candidate paths: license search `https://www4.cbs.state.or.us/exs/all/mylicsearch/`
  (Profession = "DFT-Data Broker"); verification `https://ordcbs.mylicense.com/Verification/Search.aspx`;
  registry info `https://dfr.oregon.gov/business/licensing/data-broker-registry/`
- robots.txt (www4.cbs.state.or.us, 2026-06-04): `User-agent: *` → **`Disallow: /`**;
  the `exs/all/mylicsearch` path is **explicitly disallowed**. PetalBot fully blocked;
  only whitelisted agents (e.g. `dcbs-google`) allowed.
- notes: **Scraping is disallowed by robots.txt — we will not scrape it (§10).** Options:
  (a) request the list from DFR (published contact: dfr.ndp.licensing@dcbs.oregon.gov /
  503-947-7300); (b) human manual export from the verification site; (c) mark OR
  `NEEDS-DATA` and report the other states. No bulk download is advertised.

**Honest implication for Q1:** the "most complete public picture" is, realistically,
**CA (full download) + VT (manual bulk) + TX (conditional, pending approval) + OR
(manual/agency or NEEDS-DATA)**. Cross-state entity resolution (same broker, different
spellings) remains the hard analytical step regardless of access.

---

## B. The crossover & the appetite (Q3, Q4, Q5) — Epoch AI

### Epoch AI — Data on Notable AI Models (training-set size trend) — Q4, part of Q3
- access: **download** · tier: **A** (their own data)
- candidate URLs: `https://epoch.ai/data/notable_ai_models.csv`,
  `.../frontier_ai_models.csv`, `.../large_scale_ai_models.csv`, `.../all_ai_models.csv`
- license: **CC-BY** (free to use with attribution). **No scraping.** Updated ~daily.
- notes: `MEASURED` training-dataset-size growth comes straight from these columns
  (coverage of the dataset-size field is the risk — verify at fetch).

### Epoch AI — human-text data-stock estimate (the crossover's other half) — Q3, Q5
- access: **download/paper** · tier: **A/B**
- candidate sources: paper "Will we run out of data? Limits of LLM scaling based on
  human-generated data" (`arxiv.org/abs/2211.04325`); blog "Can AI scaling continue
  through 2030"; any published replication notebook (locate at fetch).
- notes: Epoch's stock figure and end-of-data window (their reported ~300T tokens /
  100–1000T 90% CI / ~2026–2032, central revised ~2028 — **all leads to verify**) are
  their `REPORTED`/`MODELED` estimates. Unless they publish the underlying series, the
  crossover is: training trend `MEASURED` from the CSV × stock `REPORTED` from the
  paper. Q5's synthetic "fracking" overlay is `MODELED` on top, with shown assumptions.

---

## C. The exhaust economy (Q6, Q7, Q10)

### SEC EDGAR — platform revenue / users / licensing line items — Q6, Q7
- access: **api + download** · tier: **A**
- candidate: `data.sec.gov` company-facts/submissions APIs; EDGAR full-text search;
  bulk filings. Requires a descriptive `User-Agent` w/ contact email (env var). **No key.**
- notes: ARPU computed from disclosed revenue ÷ a stated user metric. Standardize
  definitions across filers (regional vs. global ARPU, ad vs. total revenue). Reddit /
  News Corp filings for licensing-deal disclosures (Q7). Confirm exact endpoints at fetch.

### The "~$0.36 per person" data price — Q6
- access: **needs primary** · tier: **? (currently UNVERIFIED)**
- notes: carried from the pitch as a lead with **no traceable primary yet**. Until one
  is found and tiered, the ARPU contrast is presented ARPU-only; the price is
  `NEEDS-DATA`. Do not put $0.36 on screen without a sourced primary.

### Recommender / ad-economy shares — Q10 (context)
- access: **needs primary** · tier: **mixed, many C**
- notes: the ~35% / ~80% / ~70% / ~$1T leads are aggregator-prone. Hunt first-party
  (company statements, IAB/eMarketer primary releases, peer-reviewed) → keep only what
  resolves to A/B; demote or drop the rest. Expect attrition here.

---

## D. The oil parallel (Q8, Q9)

### EIA — historical US crude production — Q8
- access: **api + download** · tier: **A**
- candidate: EIA Open Data API (key required, env var) + bulk CSVs. Confirm series id
  for US field production of crude oil at fetch.

### Hubbert 1956 original forecast curve — Q8
- access: **download (locate primary)** · tier: **A/B**
- notes: source Hubbert's *actual* 1956 curve/parameters from the original
  ("Nuclear Energy and the Fossil Fuels"), not a later idealized redraw. Locate a
  primary PDF at fetch; if unobtainable, present actual EIA production alone.

### Google Books Ngram + arXiv/OpenAlex — panic-frequency — Q9
- access: **download (Ngram) + api (arXiv/OpenAlex)** · tier: **A / A-B**
- notes: Ngram bulk n-gram files are official downloads; normalize by total volume and
  mind the corpus end-date. arXiv/OpenAlex APIs for recent "data wall"/"synthetic data"
  frequency. No keys for arXiv; OpenAlex polite-pool email.

---

## E. The flow question (Q11)
- access: **api + download** · tier: **A** (for documented stats)
- candidate: Common Crawl published crawl-size stats; Wikipedia dumps; arXiv output
  counts. Likely yields a `MODELED`/partial bound; "high-quality text" is hard to
  operationalize — flag the proxy explicitly. May land `NEEDS-DATA`.

---

## Robots/ToS recon log (retrieved 2026-06-04)
| host | robots.txt result | bearing on us |
|------|-------------------|---------------|
| cppa.ca.gov | Disallow /images,/js,/ssi,/css; registry allowed | CA download OK |
| www4.cbs.state.or.us | `User-agent: *  Disallow: /`; mylicsearch disallowed | **OR: no scrape** |
| texas-sos.appianportalsgov.com | 404 (no robots.txt) | TX: ToS check before any fetch |
| bizfilings.vermont.gov | 403 to automated request | VT: manual download |

---

## GATE 2 — decisions required before any fetch
1. **Texas:** approve "try official Appian export/API first, polite rate-limited scrape
   only as fallback" — or manual-only / exclude?
2. **Oregon:** robots.txt disallows scraping. Choose: agency data request, manual
   export, or mark `NEEDS-DATA`. (No scrape either way.)
3. **Vermont:** confirm a human performs the portal bulk download (preferred), vs. I
   attempt an automated download.
4. **Approve the official-download/API sources** (CA, Epoch, SEC EDGAR, EIA, Ngram,
   arXiv/OpenAlex, Common Crawl) for Phase 3 acquisition.
No source is fetched until these are signed off (CLAUDE.md §9, GATE 2).
