#!/usr/bin/env bash
# Rebuild results/ and figures/ from data/raw/ with no manual steps (CLAUDE.md §6).
# On Windows, run through Git Bash. The pipeline stages are added as each phase lands.
set -euo pipefail
cd "$(dirname "$0")"

# Locate a Python interpreter (Windows 'py' launcher included).
if command -v python >/dev/null 2>&1; then PY=python
elif command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v py >/dev/null 2>&1; then PY=py
else
  echo "ERROR: no Python interpreter found on PATH (tried python, python3, py)." >&2
  echo "On this machine, run the stages with the 'py' launcher in PowerShell instead." >&2
  exit 1
fi
echo ">> interpreter: $PY ($("$PY" --version 2>&1))"

# ---- Phase 0: environment / GATE-0 check ----
"$PY" src/check_env.py

# ---- Phase 3: acquisition (one fetcher per source; writes data/raw + provenance) ----
# Fetchers are idempotent + cached: with raw already present they re-hash, not re-download.
"$PY" src/acquire/epoch_models.py
"$PY" src/acquire/ca_cppa.py
# "$PY" src/acquire/tx_sos.py          # pending: Appian API recon (GATE-2: API-first)
# src/acquire/ingest_local.py          # VT/OR: run manually once the placed file exists
# "$PY" src/acquire/sec_edgar.py       # pending: needs SEC_EDGAR_USER_AGENT (contact email)
# "$PY" src/acquire/eia.py             # pending: needs EIA_API_KEY

# ---- Phase 4: validation & cleaning (raw -> data/interim) ----
# "$PY" src/validate/<source>.py

# ---- Phase 5: analysis (one script per question -> results/) ----
# "$PY" src/analyze/<question>.py

# ---- Phase 7: figures (results/ -> figures/, labels injected from data) ----
# "$PY" src/viz/<figure>.py

echo ">> run.sh complete."
