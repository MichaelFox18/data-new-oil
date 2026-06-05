"""Q8 — Hubbert's 1956 forecast vs. actual US crude production.

Actual production = MEASURED (EIA SRC-009). Hubbert's curve = a reconstruction (MODELED) of
his REPORTED 1956 parameters (SRC-010): logistic-derivative P(t)=Pmax*sech^2((t-tm)/tau),
tau=Q/(2*Pmax), for ultimate recoverable Q=150 Gb (peak ~1965) and Q=200 Gb (peak ~1970),
lower-48. Finds the actual peak, the shale trough, and how far actual now exceeds Hubbert.
Writes results/hubbert.json. Run: .venv/Scripts/python.exe src/analyze/hubbert.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "acquire"))
import _acquire_util as A  # noqa: E402

ROOT = A.ROOT
RAW = ROOT / "data" / "raw" / "eia" / "us_crude_production.json"
OUT = ROOT / "results" / "hubbert.json"

# Hubbert 1956 parameters (REPORTED, lower-48): ultimate Q (Gb), peak year, peak rate (Gb/yr)
HUBBERT = {
    "Q200": {"Q_gb": 200, "t_peak": 1970, "peak_gb_yr": 3.0, "label": "Hubbert 200 Gb (upper bound)"},
    "Q150": {"Q_gb": 150, "t_peak": 1965, "peak_gb_yr": 2.5, "label": "Hubbert 150 Gb (most likely)"},
}
HUBBERT_SOURCES = [
    {"quote": "Hubbert (1956, 'Nuclear Energy and the Fossil Fuels') used 150-200 Gb ultimate "
              "recoverable for the lower-48 and predicted a US peak ~1965 (150 Gb) to 1970 "
              "(200 Gb); his 200-Gb curve peaked ~1970 and the actual peak was ~17% higher",
     "url": "https://en.wikipedia.org/wiki/Hubbert_peak_theory"},
]


def hubbert_rate(t: float, p: dict) -> float:
    tau = p["Q_gb"] / (2 * p["peak_gb_yr"])
    return p["peak_gb_yr"] / math.cosh((t - p["t_peak"]) / tau) ** 2


def main() -> int:
    rows = json.loads(RAW.read_text(encoding="utf-8"))["response"]["data"]
    actual = {int(r["period"]): float(r["value"]) / 1e6 for r in rows if r.get("units") == "MBBL"}  # Gb/yr
    years = sorted(actual)
    y_recent = max(years)

    pre2000 = {y: actual[y] for y in years if y <= 2000}
    peak_year = max(pre2000, key=pre2000.get)
    trough_year = min((y for y in years if 1990 <= y <= 2012), key=lambda y: actual[y])
    h200_recent = hubbert_rate(y_recent, HUBBERT["Q200"])

    out = {
        "type": "actual=MEASURED (EIA SRC-009); Hubbert curve=MODELED reconstruction of his "
                "REPORTED 1956 parameters (SRC-010)",
        "actual_gb_per_year": {str(y): round(actual[y], 3) for y in years},
        "actual_conventional_peak": {"year": peak_year, "gb_per_year": round(pre2000[peak_year], 3)},
        "shale_trough": {"year": trough_year, "gb_per_year": round(actual[trough_year], 3)},
        "recent": {"year": y_recent, "gb_per_year": round(actual[y_recent], 3)},
        "hubbert_params": HUBBERT,
        "hubbert_curves_gb_per_year": {
            k: {str(y): round(hubbert_rate(y, p), 3) for y in range(1900, y_recent + 1)}
            for k, p in HUBBERT.items()
        },
        "divergence": {
            "hubbert200_at_recent_gb_yr": round(h200_recent, 3),
            "actual_vs_hubbert200_x": round(actual[y_recent] / h200_recent, 1),
        },
        "sources_reported": HUBBERT_SOURCES,
        "caveat": "EIA NUS = total US (incl. Alaska/offshore); Hubbert forecast lower-48 only.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"actual conventional peak: {peak_year} = {pre2000[peak_year]:.2f} Gb/yr")
    print(f"shale trough: {trough_year} = {actual[trough_year]:.2f} Gb/yr")
    print(f"recent: {y_recent} = {actual[y_recent]:.2f} Gb/yr (all-time record: {actual[y_recent] == max(actual.values())})")
    print(f"Hubbert-200 at {y_recent}: {h200_recent:.2f} Gb/yr  ->  actual is {out['divergence']['actual_vs_hubbert200_x']}x his forecast")

    if not A.provenance_has("SRC-010"):
        q = "\n".join(f"  - \"{s['quote']}\" [{s['url']}]" for s in HUBBERT_SOURCES)
        block = f"""### SRC-010  Hubbert 1956 forecast parameters (REPORTED)
- name:           M. King Hubbert (1956) US oil peak forecast parameters
- url:            https://en.wikipedia.org/wiki/Hubbert_peak_theory (primary: Hubbert 1956 API paper)
- access_method:  download (secondary descriptions of the 1956 paper) — REPORTED
- retrieved_at:   2026-06-05
- raw_path:       N/A (REPORTED parameters)
{q}
- tier:           B (secondary descriptions of a Tier-A primary paper)
- caveats:        We reconstruct his curve as a logistic-derivative from Q=150/200 Gb +
                  peak 1965/1970 (lower-48); peak rates ~2.5/3.0 Gb/yr are his curve's
                  stated peaks. The reconstruction is MODELED, faithful to his stated form."""
        A.provenance_append(block)
        print(">> PROVENANCE: appended SRC-010")
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
