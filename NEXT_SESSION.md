# NEXT SESSION — resume here

_Last updated: 2026-06-05. The data-analysis phase is COMPLETE through GATE 8._

## Status: DONE (analysis phase)
- Repo: private GitHub `MichaelFox18/data-new-oil`, branch `main`, clean + pushed.
- **All 8 phases complete; GATE 8 APPROVED 2026-06-05.** `FACTCHECK.md` is the source of
  truth for the video; `bash run.sh` reproduces every result + figure from `data/raw/`.
- Read `FACTCHECK.md` first, then `findings/`, `data/PROVENANCE.md`, `CLAUDE.md`.

## Findings (findings/F-XX.md) — 9 VERIFIED + 1 REJECTED
- F-01 CA categories: 18.9% geolocation, **5.3% sold to a GenAI developer**, 3.1% minors (Ch 3)
- F-02 census: **803 unique brokers; 166 in all four states** (Ch 2-3)
- F-03 training-size growth; F-07 crossover: **frontier meets the stock ~2029** (Ch 4-5)
- F-04 CCPA request concentration (VERIFIED as supporting context, Ch 3)
- F-05 Texas free-text AI scan = **REJECTED** negative result
- F-06 exhaust premium: **Meta ~$56/user/yr vs data worth <$1** (Ch 3)
- F-08 deferral overlay: synthetic buys **~3 yr per 10x** (MODELED, Ch 7)
- F-09 Hubbert: **nailed 1970, fracking broke it 12x** (Ch 6)
- F-10 data-labor: **RLHF research ~728x** 2021->2024 (proxy, Ch 7)

## Sources: SRC-001..011 (all tiered in PROVENANCE.md)
Epoch (001), CA/VT/OR/TX registries (002-005), SEC XBRL (006) + 10-K user metrics (007),
Epoch stock paper (008), EIA oil (009), Hubbert params (010), OpenAlex (011).

## OPTIONAL follow-ups (none required; the phase is done)
- Chase REPORTED -> primary: Appen revenue from its annual report; the "$1B/lab/yr" lead;
  a clean FT-2013 primary for the data price (the "$0.36" stays UNVERIFIED / DO-NOT-USE).
- Tighter Hubbert: swap EIA total-US for the lower-48 series (apples-to-apples pre-shale).
- More broker cuts: 3-state minors share (CA+TX+VT); VT/TX breach data; CA AG (2nd) registry;
  PRC time-comparison (CC-BY-NC -> REPORTED only).
- Remaining approved questions not yet built: Q9 panic-frequency bibliometric; Q7 licensing deals.

## Environment gotchas (still apply)
- Python via `py` or `.venv/Scripts/python.exe`; Git Bash cannot see `python`/`python3`.
- Memory-tight: run ONE pandas process at a time (concurrent runs caused a paging error).
- `.venv/` + `.env` gitignored; `data/raw/** -text` keeps raw byte-exact. EIA echoes its
  API key and OpenAlex takes a mailto -> both are REDACTED from saved files/logs; a commit
  security-gate (`git grep --cached` for the key/email) guards every push.
