"""Q5 deferral overlay — how far does synthetic data slide the data wall? (MODELED)

We do NOT predict how much synthetic data will exist (unknowable). Instead we model the
DEFERRAL LEVERAGE: treat synthetic data as multiplying the effective training-data pool by
a factor M, and compute where the crossover moves for a sweep of M. Because frontier
training grows exponentially (~2.2x/yr, MEASURED), each 10x of effective data buys only a
few fixed years — that leverage is the robust, honest result; M itself is an assumption.

Inputs: results/crossover.json (frontier slope + stock, from SRC-001 MEASURED + SRC-008
REPORTED). Output: results/deferral.json. No raw read, no pandas.
Run: .venv/Scripts/python.exe src/analyze/deferral.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CROSS = ROOT / "results" / "crossover.json"
OUT = ROOT / "results" / "deferral.json"

MULTIPLIERS = [1, 3, 10, 30, 100, 1000]  # synthetic makes effective data M x the human stock


def main() -> int:
    d = json.loads(CROSS.read_text(encoding="utf-8"))
    slope = d["frontier_fit_2018plus"]["om_per_year"]      # OM/year (MEASURED frontier trend)
    s = d["stock_reported"]
    eff, g, t0 = s["effective_tokens"], s["growth_rate_per_year_central"], s["anchor_year"]
    yc = d["crossover_modeled"]["year_central"]

    a = math.log10(1 + g)
    # reconstruct the frontier line from the known central crossover point
    y_at_yc = eff * (1 + g) ** (yc - t0)
    intercept = math.log10(y_at_yc) - slope * yc

    def cross(d0: float) -> float:
        return (math.log10(d0) - intercept - t0 * a) / (slope - a)

    leverage = 1.0 / (slope - a)  # years of deferral per 10x of effective data
    scenarios = [
        {"synthetic_multiplier": M, "effective_stock_tokens": eff * M,
         "crossover_year": round(cross(eff * M), 1)}
        for M in MULTIPLIERS
    ]

    out = {
        "type": "MODELED — synthetic data assumed to multiply effective training data by M",
        "assumptions": [
            "effective stock = human stock (~4e14, growing 0-10%/yr) x M",
            "M (synthetic multiplier) is a SWEEP, not a prediction — we do not estimate real synthetic volume",
            "frontier trend (~2.2x/yr) assumed unchanged",
            "synthetic data assumed as useful as human data (1:1) — an UPPER bound on its effect",
            "model collapse / quality degradation NOT modeled (see counterforce)",
        ],
        "frontier_om_per_year": slope,
        "years_deferred_per_10x_effective_data": round(leverage, 2),
        "baseline_crossover_year": yc,
        "scenarios": scenarios,
        "counterforce": "Model collapse (REPORTED, research literature): models trained on their "
                        "own synthetic output can degrade in quality. This caps synthetic data's "
                        "effective multiplier and is Chapter 7's open question — NOT quantified here.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"frontier {10**slope:.2f}x/yr  ->  deferral leverage = {leverage:.2f} years per 10x of data")
    print("MODELED crossover under a synthetic multiplier M:")
    for sc in scenarios:
        print(f"  M={sc['synthetic_multiplier']:>5}x  effective={sc['effective_stock_tokens']:.1e}  ->  wall ~{sc['crossover_year']}")
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
