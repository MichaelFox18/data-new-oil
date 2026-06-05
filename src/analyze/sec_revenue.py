"""Q6 (exhaust premium), numerator — platform annual revenue from SEC XBRL (SRC-006).

MEASURED. Reads each companyfacts JSON and extracts full-fiscal-year revenue using SEC's
calendar-year annual frames (frame == 'CY####', which dedupes to one clean annual value).
Prefers us-gaap:Revenues, else RevenueFromContractWithCustomerExcludingAssessedTax.
Writes results/sec_revenue.json. Read-only on raw.

The per-user denominator (MAU/DAU/ARPU) is NOT in XBRL and is sourced separately from the
10-Ks as REPORTED — see the F-06 card. Run: .venv/Scripts/python.exe src/analyze/sec_revenue.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "sec"
OUT = ROOT / "results" / "sec_revenue.json"

TICKERS = ["META", "GOOGL", "SNAP", "RDDT", "PINS"]
PREF = [
    "Revenues",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
]
CY = re.compile(r"^CY(\d{4})$")


def annual_series(facts: dict) -> tuple[list[str], dict]:
    """Merge CY-annual revenue across concepts (companies switched tags at ASC 606 in
    2018). Iterate PREF in order so the post-606 contract-revenue tag overrides the legacy
    'Revenues' tag on any overlapping year; union covers the full history to the latest FY."""
    merged: dict[int, int] = {}
    used: list[str] = []
    for concept in PREF:
        node = facts.get("us-gaap", {}).get(concept)
        if not node:
            continue
        got = False
        for e in node.get("units", {}).get("USD", []):
            m = CY.match(e.get("frame", ""))
            if m:
                merged[int(m.group(1))] = e["val"]
                got = True
        if got:
            used.append(concept)
    return used, dict(sorted(merged.items()))


def main() -> int:
    out = {"source": "SRC-006 SEC EDGAR companyfacts (XBRL)", "companies": {}}
    print("Annual revenue (full FY, from SEC XBRL CY frames):")
    for t in TICKERS:
        d = json.loads((RAW / f"companyfacts_{t}.json").read_text(encoding="utf-8"))
        concepts, series = annual_series(d.get("facts", {}))
        if not series:
            out["companies"][t] = {"status": "NO_ANNUAL_REVENUE_FRAME"}
            print(f"  {t:6} no annual revenue frame found")
            continue
        years = sorted(series)
        fy = years[-1]
        rev = series[fy]
        prior = series.get(fy - 1)
        yoy = round((rev / prior - 1) * 100, 1) if prior else None
        out["companies"][t] = {
            "entity": d.get("entityName"),
            "concepts": concepts,
            "fy": fy,
            "revenue_usd": rev,
            "prior_fy": fy - 1 if prior else None,
            "prior_revenue_usd": prior,
            "yoy_growth_pct": yoy,
            "all_years": series,
        }
        print(f"  {t:6} FY{fy}: ${rev/1e9:8.1f}B  (YoY {yoy}%)  [{'+'.join(concepts)}]")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
