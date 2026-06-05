"""Q3 hero crossover — frontier LLM training-set size vs Epoch's human-text stock.

Combines our MEASURED frontier training-size trend (Epoch language models, SRC-001) with
Epoch's REPORTED stock of human public text (SRC-008, quoted from arXiv:2211.04325v2 and
Epoch's "Can AI scaling continue through 2030"). Fits the frontier (running-max) trend and
projects when it reaches the stock -> a MODELED crossover, alongside Epoch's own REPORTED
2026-2032 exhaustion window. Writes results/crossover.json. Read-only on raw.

Run: .venv/Scripts/python.exe src/analyze/crossover.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "acquire"))
import _acquire_util as A  # noqa: E402

ROOT = A.ROOT
RAW = ROOT / "data" / "raw" / "epoch" / "notable_ai_models.csv"
OUT = ROOT / "results" / "crossover.json"
RETRIEVED = "2026-06-05"

# REPORTED Epoch stock figures (tokens). Sourced from primaries, not memory:
STOCK_EFFECTIVE = 4e14            # quality+repetition-adjusted effective stock of public text
STOCK_CI = (1.3e14, 2.1e15)      # 95% CI on indexed-web stock (130T - 2100T)
EPOCH_WINDOW = (2026, 2032)      # reported exhaustion window
STOCK_SOURCES = [
    {"quote": "models will be trained on dataset sizes approaching the total effective stock "
              "of text in the indexed web: around 4e14 tokens",
     "url": "https://arxiv.org/html/2211.04325v2"},
    {"quote": "indexed web ~510T tokens after dedup [95% CI 130T-2100T]; models reach the stock "
              "between 2026 and 2032",
     "url": "https://arxiv.org/abs/2211.04325"},
]


def frontier(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("date").copy()
    df["runmax"] = df["tokens"].cummax()
    return df[df["tokens"] >= df["runmax"]].copy()  # record-setting (frontier) models


def main() -> int:
    df = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    df = df[df["Domain"].str.strip() == "Language"].copy()
    df["tokens"] = pd.to_numeric(df["Training dataset size (total)"], errors="coerce")
    df["date"] = pd.to_datetime(df["Publication date"], errors="coerce")
    df = df.dropna(subset=["tokens", "date"])
    df = df[df["tokens"] > 0].copy()
    df["year"] = df["date"].dt.year + (df["date"].dt.dayofyear - 1) / 365.25

    fr = frontier(df)
    fr_modern = fr[fr["year"] >= 2018]
    slope, intercept = np.polyfit(fr_modern["year"].to_numpy(float), np.log10(fr_modern["tokens"].to_numpy(float)), 1)

    def cross_year(stock: float) -> float:
        return (np.log10(stock) - intercept) / slope

    latest = df.loc[df["tokens"].idxmax()]
    out = {
        "frontier_fit_2018plus": {
            "n_frontier_models": int(len(fr_modern)),
            "om_per_year": round(float(slope), 3),
            "x_per_year": round(float(10 ** slope), 2),
            "doublings_per_year": round(float(slope / np.log10(2)), 2),
        },
        "latest_frontier": {
            "model": str(latest["Model"]), "date": latest["date"].strftime("%Y-%m-%d"),
            "tokens": float(latest["tokens"]),
            "orders_of_magnitude_below_effective_stock": round(float(np.log10(STOCK_EFFECTIVE / latest["tokens"])), 2),
        },
        "stock_reported": {
            "effective_tokens": STOCK_EFFECTIVE, "ci_tokens": list(STOCK_CI),
            "epoch_exhaustion_window": list(EPOCH_WINDOW), "type": "REPORTED (Epoch)",
            "sources": STOCK_SOURCES, "retrieved": RETRIEVED,
        },
        "crossover_modeled": {
            "type": "MODELED — our frontier trend extrapolated to the stock level",
            "year_at_effective_stock": round(float(cross_year(STOCK_EFFECTIVE)), 1),
            "year_at_ci_low": round(float(cross_year(STOCK_CI[0])), 1),
            "year_at_ci_high": round(float(cross_year(STOCK_CI[1])), 1),
        },
        "frontier_points": [
            {"model": str(r.Model), "year": round(float(r.year), 2), "tokens": float(r.tokens)}
            for r in fr.itertuples()
        ],
        "all_language_points": [
            {"year": round(float(y), 2), "tokens": float(tk)}
            for y, tk in zip(df["year"], df["tokens"])
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")

    f = out["frontier_fit_2018plus"]; c = out["crossover_modeled"]; l = out["latest_frontier"]
    print(f"frontier (2018+): n={f['n_frontier_models']}, {f['x_per_year']}x/yr ({f['doublings_per_year']} doublings/yr)")
    print(f"latest frontier: {l['model']} = {l['tokens']:.2e} tokens ({l['orders_of_magnitude_below_effective_stock']} OM below 4e14 stock)")
    print(f"MODELED crossover at 4e14 effective stock: ~{c['year_at_effective_stock']}  (CI {c['year_at_ci_low']}..{c['year_at_ci_high']})")
    print(f"Epoch REPORTED window: {EPOCH_WINDOW[0]}-{EPOCH_WINDOW[1]}")

    if not A.provenance_has("SRC-008"):
        q = "\n".join(f"  - \"{s['quote']}\" [{s['url']}]" for s in STOCK_SOURCES)
        block = f"""### SRC-008  Epoch human-text data stock (REPORTED)
- name:           Epoch AI estimate of the stock of human-generated public text
- url:            https://arxiv.org/abs/2211.04325 ; https://arxiv.org/html/2211.04325v2
- access_method:  download (paper text) — REPORTED quotes
- retrieved_at:   {RETRIEVED}
- raw_path:       N/A (REPORTED quotes)
{q}
- tier:           A (originating research group's own paper)
- caveats:        ~4e14 effective (quality/repetition-adjusted) vs ~510T raw indexed web
                  [95% 130T-2100T]; exhaustion window 2026-2032 is Epoch's own projection
                  (their MODELED). Earlier '~300T' lead was a search summary, NOT used."""
        A.provenance_append(block)
        print(">> PROVENANCE: appended SRC-008")
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
