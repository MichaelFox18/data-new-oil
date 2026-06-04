# NEXT SESSION — resume here

_Last updated: 2026-06-04. Read this first, then `CLAUDE.md` (operating manual),
then `QUESTIONS.md`, `SOURCES.md`, `VALIDATION.md`, and `findings/`._

## Where we are
- Repo: private GitHub `MichaelFox18/data-new-oil`, branch `main`, clean + pushed.
- Last commit: `1fed30b` (GATE 6: F-01/F-02/F-03 → VERIFIED).
- **Phases 0–4 complete** (setup, questions, sources, acquisition, validation).
  **Phase 5 in progress** (3 findings done). **Phase 6 GATE 6 passed** for those 3.
- Reproduce everything: `bash run.sh` (uses `.venv`; rebuilds results/profiles from raw).

## Findings — all VERIFIED (human sign-off 2026-06-04)
- **F-01** CA broker categories: 18.9% precise geolocation, **5.3% sold/shared to a GenAI
  developer**, 3.1% minors (n=581, 0% blank). Self-report = lower bounds. `results/ca_categories.json`.
- **F-02** Four-state census: **803 unique brokers; 166 (20.7%) in all four states**;
  437 (54%) in 2+. Triangulates PRC/EFF's ~750 groups (Apr 2025) — NOT a "first count";
  the original cut is the all-four core. `results/broker_census.json`, `data/interim/brokers_normalized.csv`.
- **F-03** LLM training-size growth: ~5×/yr (2.35 doublings/yr, R²=0.46, n=212), max 36T
  tokens (Qwen3-Max). Population trend. `results/epoch_growth.json`.

## Sources acquired (PROVENANCE SRC-001..005, all Tier A)
Epoch CSVs (CC-BY) · CA CPPA (581) · VT xlsx (714, 26 dup rows) · OR cp1252+pipe (352) ·
TX official export (398; 2-row preamble + blank line before header; has minors flag +
free-text categories). Keys for EIA + FRED are filled in the gitignored `.env`; SEC needs
only the User-Agent (set).

## OPEN DECISION (the user was choosing this when we stopped)
Which broker-data expansion to pursue next — pick any, I'll sequence:
1. **Path 2 — mine in-hand data (my recommended first):** CA request-volume metrics
   (deletion/know/opt-out counts + response times across 581 brokers — untapped, a whole
   new finding); **TX free-text AI/ML scan** (a 2nd state's AI signal — see note below);
   VT registration trend (Q2) via `DataBrokerStatus`.
2. **Path 1+3 — broaden + time axis:** add the *second* California registry (CA Attorney
   General, `oag.ca.gov/data-brokers`); use PRC/EFF's downloadable cleaned+parent-grouped
   750-broker DB for an Apr-2025 → Jun-2026 comparison. ⚠️ PRC is **CC-BY-NC-SA
   (NonCommercial)** — use as REPORTED cross-check ONLY; keep on-screen numbers from our
   own Tier-A registry pulls.
3. **Path 4 — AI money trail (SEC):** ARPU for public brokers (Equifax/Experian/TransUnion/
   LiveRamp) + training-data licensing deals (Reddit/News Corp). Uses `.env` keys (Q6/Q7).
4. **Source Epoch's stock figure** (arXiv:2211.04325 / Epoch data paper, ~1e14 tokens,
   REPORTED) to complete the F-03 hero crossover.

## Backlog (remaining Phase-5 questions, see QUESTIONS.md)
Q6 SEC ARPU vs ~$0.36 (find a primary for $0.36) · Q7 licensing deals · Q8 EIA Hubbert-vs-
actual (+ source Hubbert 1956 curve) · Q9 Ngram/arXiv panic-frequency · Q11 text "flow"
rate. Then Phase 7 (figures from results/ only) and Phase 8 (FACTCHECK.md + GATE 8).

## Environment gotchas (important)
- Python: use `py` (Windows launcher) or `.venv/Scripts/python.exe`. **Git Bash cannot see
  `python`/`python3`** — only `py`. Scripts run fine via the venv interpreter.
- **Memory is tight on this box**: running several pandas processes at once caused a
  Windows "paging file too small" error and made commands auto-background with no output.
  **Run one pandas process at a time**; prefer committed scripts over inline `-c` one-liners.
- `.venv/` and `.env` are gitignored. `data/raw/** -text` keeps raw byte-exact (hashes).
- Per-state parsing: OR = cp1252 + `|`; TX = find header row "Registration Number"
  (preamble + blank line); VT = drop 26 exact-dup rows; category Yes/No flags are CA-only
  (TX has a minors flag + free text).

## In-flight note
A quick **Texas free-text AI/ML mention count** was being computed but kept getting
auto-backgrounded (memory). To run it cleanly: load TX with dynamic header detection
(as in `src/analyze/broker_census.py`), join the `Categories of Data Processed and
Transferred` + `Additional Information` columns, and count AI/ML/generative/LLM regex
hits. Make it a committed script (`src/analyze/tx_ai_mentions.py`) if it becomes a finding.
