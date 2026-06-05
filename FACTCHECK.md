# FACTCHECK — every on-screen number, traced

Phase 8 deliverable (CLAUDE.md §14). Every number that may appear in the video, paired
with its claim type, value, source/script, tier, reproduce command, confidence, and
chapter. Built from `VERIFIED` findings only.

- Reproduce ALL results + figures from raw: `bash run.sh` (uses `.venv`; on Windows run
  in Git Bash). Individual reproduce commands below use the venv interpreter:
  `.venv/Scripts/python.exe <script>` (shown as `py <script>` for brevity).
- TYPE = `MEASURED` (we computed it from raw) | `REPORTED` (we quote a source) |
  `MODELED` (we estimated it; assumptions shown in the finding).
- Sources are logged in `data/PROVENANCE.md` (SRC-001 … SRC-011).

---

## Chapter 2-3 — The exhaust economy (brokers)

- CLAIM: "803 unique data brokers are registered across the four public state registries" |
  TYPE: MEASURED | VALUE: 803 | SOURCE: SRC-002/003/004/005 (Tier A) |
  REPRODUCE: `py src/analyze/broker_census.py` | CONFIDENCE: Medium-High | CHAPTER: 2-3 | F-02
- CLAIM: "166 brokers (20.7%) are registered in all four states" |
  TYPE: MEASURED | VALUE: 166 (20.7%) | SOURCE: SRC-002/003/004/005 (Tier A) |
  REPRODUCE: `py src/analyze/broker_census.py` | CONFIDENCE: Medium-High | CHAPTER: 2-3 | F-02
  NOTE: name-based dedup -> 803 is a near-ceiling, 166 a floor. Triangulates PRC/EFF's ~750 (Apr 2025, REPORTED).
- CLAIM: "Of 581 California-registered brokers, 18.9% collect precise geolocation" |
  TYPE: MEASURED | VALUE: 110/581 = 18.9% | SOURCE: SRC-002 (Tier A) |
  REPRODUCE: `py src/analyze/ca_categories.py` | CONFIDENCE: High | CHAPTER: 3 | F-01
- CLAIM: "5.3% of CA brokers sold/shared data with a GenAI developer in the past year" |
  TYPE: MEASURED | VALUE: 31/581 = 5.3% | SOURCE: SRC-002 (Tier A) |
  REPRODUCE: `py src/analyze/ca_categories.py` | CONFIDENCE: High | CHAPTER: 3-7 | F-01
  NOTE: self-report -> lower bound ("at least").
- CLAIM: "3.1% of CA brokers collect minors' personal information" |
  TYPE: MEASURED | VALUE: 18/581 = 3.1% | SOURCE: SRC-002 (Tier A) |
  REPRODUCE: `py src/analyze/ca_categories.py` | CONFIDENCE: High | CHAPTER: 3 | F-01
- CLAIM (supporting context): "The 10 busiest CA brokers account for 67.7% of all reported
  consumer-request events; ~99% are fulfilled" | TYPE: MEASURED | VALUE: 67.7%; ~98.7% |
  SOURCE: SRC-002 (Tier A) | REPRODUCE: `py src/analyze/ca_requests.py` |
  CONFIDENCE: Medium (self-report, automated signals) | CHAPTER: 3 | F-04
  NOTE: triangulates Bloomberg Law; the cross-type request sum double-counts automated (GPC) signals.

## Chapter 3 — The exhaust premium (ARPU)

- CLAIM: "Alphabet earned $402.8B and Meta $201.0B in FY2025" |
  TYPE: MEASURED | VALUE: $402.8B; $201.0B | SOURCE: SRC-006 SEC XBRL (Tier A) |
  REPRODUCE: `py src/analyze/sec_revenue.py` | CONFIDENCE: High | CHAPTER: 3 | F-06
- CLAIM: "Meta earns ~$56/yr per daily user; Reddit ~$18; Snap ~$13; Pinterest ~$7/monthly user" |
  TYPE: MEASURED (revenue) + REPORTED (user counts) | VALUE: $56.14 / $18.14 / $12.51 / $6.82 |
  SOURCE: SRC-006 (Tier A) + SRC-007 10-K user metrics (Tier A) |
  REPRODUCE: `py src/analyze/sec_arpu.py` | CONFIDENCE: High | CHAPTER: 3 | F-06
  NOTE: DAP/DAU/DAUq are DAILY actives; Pinterest MAU is MONTHLY (not directly comparable).
- CLAIM: "A person's raw data sells for a fraction of a dollar" |
  TYPE: REPORTED | VALUE: <$1/person (basic demographics ~$0.0005) | SOURCE: FT 2013 calculator (Tier B) |
  REPRODUCE: cite FT; cross-ref NIH PMC8562626 | CONFIDENCE: Medium | CHAPTER: 1,3 | F-06
  NOTE: the pitch's "$0.36" is UNVERIFIED — DO NOT USE (see below).

## Chapter 4-5 — The machines that eat data / the wall

- CLAIM: "Frontier LLM training sets grew ~2.2x/year (record-setters), reaching 36 trillion tokens" |
  TYPE: MEASURED | VALUE: 2.19x/yr; 3.6e13 tokens (Qwen3-Max) | SOURCE: SRC-001 Epoch (Tier A) |
  REPRODUCE: `py src/analyze/crossover.py` | CONFIDENCE: Medium-High | CHAPTER: 4-5 | F-07/F-03
  NOTE: population-wide fit is ~5x/yr (`epoch_growth.py`); the crossover uses the FRONTIER fit (~2.2x/yr).
- CLAIM: "The latest frontier model is already only ~1 order of magnitude below the entire usable human-text stock" |
  TYPE: MEASURED vs REPORTED | VALUE: 36T vs ~4e14 (1.05 OM) | SOURCE: SRC-001 + SRC-008 |
  REPRODUCE: `py src/analyze/crossover.py` | CONFIDENCE: High | CHAPTER: 5 | F-07
- CLAIM: "Epoch estimates the usable human-text stock at ~4e14 tokens, growing 0-10%/yr,
  with full use 2026-2032" | TYPE: REPORTED | VALUE: ~4e14 tokens; 0-10%/yr; 2026-2032 |
  SOURCE: SRC-008 Epoch arXiv:2211.04325v2 (Tier A) | REPRODUCE: cite paper |
  CONFIDENCE: High (their estimate) | CHAPTER: 5 | F-07
- CLAIM: "Our independent frontier trend crosses the stock ~2029 (modeled 2027-2032) —
  inside Epoch's window" | TYPE: MODELED | VALUE: ~2029.1 (2027.3-2031.8) |
  SOURCE: SRC-001 (MEASURED) + SRC-008 (REPORTED) | REPRODUCE: `py src/analyze/crossover.py` |
  CONFIDENCE: Medium-High | CHAPTER: 5,7 | F-07

## Chapter 6 — We've seen this movie (oil)

- CLAIM: "US oil production peaked in 1970 (3.52 Gb/yr), as Hubbert's 1956 curve predicted" |
  TYPE: MEASURED (actual) + REPORTED (Hubbert params) | VALUE: 3.52 Gb/yr, 1970 |
  SOURCE: SRC-009 EIA (Tier A) + SRC-010 Hubbert (Tier B) | REPRODUCE: `py src/analyze/hubbert.py` |
  CONFIDENCE: High | CHAPTER: 6 | F-09
- CLAIM: "Then fracking broke the forecast: 2025 production hit an all-time record 4.96 Gb/yr,
  ~12x Hubbert's curve for that year" | TYPE: MEASURED + MODELED | VALUE: 4.96 Gb/yr; 12x |
  SOURCE: SRC-009 EIA (Tier A) | REPRODUCE: `py src/analyze/hubbert.py` |
  CONFIDENCE: High | CHAPTER: 6 | F-09
  NOTE: EIA NUS = total US; Hubbert forecast lower-48 (Alaska adds the 1980s bump).

## Chapter 7 — Does the streak break? (synthetic + human data)

- CLAIM: "Synthetic data defers the wall only ~3 years per 10x of data (frontier grows ~120%/yr)" |
  TYPE: MODELED | VALUE: 3.1 yr per 10x; 10x->2032, 100x->2035, 1000x->2038 |
  SOURCE: SRC-001 (MEASURED) + SRC-008 (REPORTED), assumptions shown | REPRODUCE: `py src/analyze/deferral.py` |
  CONFIDENCE: Leverage robust; M is a sweep, not a forecast | CHAPTER: 7 | F-08
- CLAIM: "Research on RLHF (paying humans to train models) exploded ~728x — from ~6 papers
  in 2021 to ~4,370 in 2024" | TYPE: MEASURED (research proxy) | VALUE: 6 -> 4,370 (~728x) |
  SOURCE: SRC-011 OpenAlex (Tier A/B) | REPRODUCE: `py src/analyze/datalabor.py` |
  CONFIDENCE: High for the trend (it is a PROXY, not jobs) | CHAPTER: 7 | F-10

---

## DO NOT USE (UNVERIFIED) / NEEDS-DATA

- "$0.36 per person" raw-data price — UNVERIFIED (no clean primary; does not match the FT
  calculator). Use the FT "<$1/person" framing (REPORTED) instead. (F-06)
- A specific "AI-training jobs +X%" count — NEEDS-DATA (no BLS code; key firms private;
  job-board analytics paywalled). Use the OpenAlex RLHF research proxy + REPORTED industry
  figures instead. (F-10)
- Data-labeling MARKET-SIZE figures (Scale/Mercor ARR, CAGR) — REPORTED only (Tier B-C,
  many private); attribute on screen, never present as our measurement. (F-10)

## Status
- VERIFIED & on-screen-ready: F-01, F-02, F-03, F-04 (context), F-06, F-07, F-08, F-09, F-10.
- REJECTED (negative result, not on screen): F-05 (Texas free-text AI scan).
- GATE 8: `bash run.sh` reproduces all `results/` + `figures/` from `data/raw/`.
- **GATE 8 APPROVED 2026-06-05** — FACTCHECK.md is the source of truth for the video script.
