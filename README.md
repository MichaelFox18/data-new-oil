# Data Was Never "The New Oil" — Data Analysis

Reproducible data-analysis repo for the Maxinomics longform documentary
*"Data Was Never 'The New Oil' — Until Now."*

The creative brief is in [`Maxinomics_Data_Pitch.md`](Maxinomics_Data_Pitch.md).
The operating manual that governs **all** work in this repo is
[`CLAUDE.md`](CLAUDE.md) — read it before doing anything. Its prime directive:

> Every number that could appear on screen traces to either (a) code in `src/`
> that computes it from a file in `data/raw/`, or (b) a primary source logged in
> `data/PROVENANCE.md`. Nothing comes from memory. Numbers flow forward through
> code (raw → interim → results → figures); they never flow backward by hand.

## Layout

```
data/raw/        IMMUTABLE source archives, one subdir per source
data/interim/    cleaned/derived datasets (produced by code only)
data/PROVENANCE.md  append-only source ledger
src/acquire/     one fetcher per source -> writes raw + logs provenance
src/validate/    profiling + integrity checks
src/analyze/     one script per research question -> writes results/
src/viz/         one script per figure -> reads results/, writes figures/
results/         computed JSON/CSV that feed BOTH claims and charts
figures/         regenerable charts (no hand-edited numbers)
findings/        one finding card per insight (F-XX.md)
notebooks/       exploration ONLY, never the source of truth
logs/            fetch logs, run logs (timestamps, row counts, hashes)
FACTCHECK.md     final: every on-screen number -> source + reproduce command
```

## Toolchain (this machine)

Python is available via the Windows `py` launcher (Python 3.14). The Git Bash
provided by the Bash tool does not see `python`/`python3` on PATH; use `py`.

```powershell
# one-time: create an isolated environment and install pinned deps (Phase 3)
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

## Reproduce

`run.sh` (POSIX shell) / `Makefile` rebuild `results/` and `figures/` from
`data/raw/` with no manual steps. On Windows run it through Git Bash, or call the
stages directly with `py`:

```bash
bash run.sh          # detects an interpreter, runs the env check + pipeline stages
```

```powershell
py src/check_env.py  # the Phase 0 / GATE-0 environment check
```

## Status

- **Phase 0 — Setup:** scaffold in place; GATE-0 env check runnable.
- **Phase 1 — Questions & hypotheses:** drafting the falsifiable question list
  (awaiting **GATE 1** human approval before any data is acquired).

Phases and gates are defined in [`CLAUDE.md`](CLAUDE.md) §9. Do not pass a gate
without its sign-off.
