"""Q1/Q3 — California data brokers' self-reported collection & sharing categories.

MEASURED from the CPPA registry (SRC-002). Every category flag profiled at 0% blank
(pure Yes/No), so shares are computed over all registered brokers with no imputation.
Columns are matched by case-insensitive substring (robust to curly apostrophes in the
official headers). Writes results/ca_categories.json. Read-only on raw.

Run: .venv/Scripts/python.exe src/analyze/ca_categories.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "cppa" / "registry.csv"
OUT = ROOT / "results" / "ca_categories.json"

# label -> case-insensitive substring uniquely identifying the column
PATTERNS = {
    "precise_geolocation": "precise geolocation",
    "minors": "personal information of minors",
    "biometric": "biometric data",
    "reproductive_health": "reproductive health",
    "citizenship_immigration": "citizenship",
    "sexual_orientation": "sexual orientation",
    "gender_identity": "gender identity",
    "union_membership": "union membership",
    "sold_to_genai_developer": "developer of a genai",
    "sold_to_federal_govt": "to the federal government",
    "sold_to_law_enforcement": "to law enforcement",
    "sold_to_state_govts": "other state governments",
    "sold_to_foreign_actor": "to a foreign actor",
}


def find_cols(cols, needle):
    return [c for c in cols if needle.lower() in c.lower()]


def main() -> int:
    df = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    n = len(df)
    out = {"source": "SRC-002 CPPA registry", "n_brokers": int(n), "categories": {}}
    print(f"CA registry: {n} registered brokers\n  share self-reporting YES (of all brokers):")

    summary = []
    for label, needle in PATTERNS.items():
        hits = find_cols(df.columns, needle)
        if not hits:
            out["categories"][label] = {"column": None, "status": "COLUMN_NOT_FOUND"}
            print(f"    !! {label}: column not found ({needle!r})")
            continue
        if len(hits) > 1:
            print(f"    !! {label}: {len(hits)} columns match {needle!r}, using first")
        col = hits[0]
        vals = df[col].str.strip().str.casefold()
        yes, no, blank = int((vals == "yes").sum()), int((vals == "no").sum()), int((vals == "").sum())
        other = n - yes - no - blank
        pct = round(100 * yes / n, 1) if n else None
        out["categories"][label] = {
            "column": col, "yes": yes, "no": no, "blank": blank, "other": other, "pct_yes": pct,
        }
        summary.append((label, yes, pct))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    for label, yes, pct in sorted(summary, key=lambda r: -(r[2] or 0)):
        print(f"    {label:26} {yes:4}/{n} = {pct:5}%")
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
