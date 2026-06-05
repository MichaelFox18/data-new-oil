#!/usr/bin/env bash
# Rebuild results/ and figures/ from data/raw/ with no manual steps (CLAUDE.md §6).
# On Windows, run through Git Bash. The pipeline stages are added as each phase lands.
set -euo pipefail
cd "$(dirname "$0")"

# Locate a Python interpreter — prefer the project venv (has pandas/openpyxl/etc.).
if [ -x ".venv/Scripts/python.exe" ]; then PY=".venv/Scripts/python.exe"
elif [ -x ".venv/bin/python" ]; then PY=".venv/bin/python"
elif command -v python >/dev/null 2>&1; then PY=python
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
"$PY" src/acquire/sec_edgar.py         # cached; needs SEC_EDGAR_USER_AGENT in .env
# VT/OR/TX registries are committed raw (manual per GATE-2); ingest_local.py logs new ones.
# "$PY" src/acquire/eia.py             # pending: needs EIA_API_KEY (Q8 Hubbert)

# ---- Phase 4: validation & cleaning (raw -> data/interim) ----
"$PY" src/validate/profile.py

# ---- Phase 5: analysis (one script per question -> results/) ----
"$PY" src/analyze/ca_categories.py
"$PY" src/analyze/ca_requests.py
"$PY" src/analyze/broker_census.py
"$PY" src/analyze/tx_ai_mentions.py
"$PY" src/analyze/epoch_growth.py
"$PY" src/analyze/sec_revenue.py
"$PY" src/analyze/sec_arpu.py
"$PY" src/analyze/crossover.py
"$PY" src/analyze/deferral.py

# ---- Phase 7: figures (results/ -> figures/, labels injected from data) ----
"$PY" src/viz/crossover.py
"$PY" src/viz/deferral.py

echo ">> run.sh complete."
