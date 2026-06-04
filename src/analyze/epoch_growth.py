"""Q4 / Q3 — growth of language-model training-set size (Epoch, SRC-001).

MEASURED. Filters Epoch notable models to Domain == "Language" (where training size is
in TOKENS, per the dataset-size notes), parses tokens + publication date, and fits
log10(tokens) vs decimal year to get the growth rate. Also reports the current frontier
scale. Writes results/epoch_growth.json. Read-only on raw.

The crossover (Q3) also needs Epoch's REPORTED human-text-stock estimate (order ~1e14
tokens) — that is NOT computed here and must be sourced from their paper before use.

Run: .venv/Scripts/python.exe src/analyze/epoch_growth.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "epoch" / "notable_ai_models.csv"
OUT = ROOT / "results" / "epoch_growth.json"


def fit_loglinear(years: np.ndarray, log10tokens: np.ndarray) -> tuple[float, float, float]:
    slope, intercept = np.polyfit(years, log10tokens, 1)
    pred = slope * years + intercept
    ss_res = float(((log10tokens - pred) ** 2).sum())
    ss_tot = float(((log10tokens - log10tokens.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot else float("nan")
    return float(slope), float(intercept), float(r2)


def summarize(df: pd.DataFrame, label: str) -> dict:
    years = df["year"].to_numpy(dtype=float)
    logt = np.log10(df["tokens"].to_numpy(dtype=float))
    slope, _intercept, r2 = fit_loglinear(years, logt)
    return {
        "label": label, "n": int(len(df)),
        "date_min": df["date"].min().strftime("%Y-%m-%d"),
        "date_max": df["date"].max().strftime("%Y-%m-%d"),
        "om_per_year": round(slope, 3),
        "x_per_year": round(10 ** slope, 2),
        "doublings_per_year": round(slope / np.log10(2), 2),
        "years_per_10x": round(1 / slope, 2) if slope else None,
        "r2": round(r2, 3),
    }


def main() -> int:
    df = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    df = df[df["Domain"].str.strip() == "Language"].copy()
    df["tokens"] = pd.to_numeric(df["Training dataset size (total)"], errors="coerce")
    df["date"] = pd.to_datetime(df["Publication date"], errors="coerce")
    df = df.dropna(subset=["tokens", "date"])
    df = df[df["tokens"] > 0].copy()
    df["year"] = df["date"].dt.year + (df["date"].dt.dayofyear - 1) / 365.25

    full = summarize(df, "all language models w/ tokens+date")
    modern = summarize(df[df["year"] >= 2018], "2018+ (modern scaling era)")

    recent = df[df["year"] >= 2025].sort_values("tokens", ascending=False).head(5)
    imax = df["tokens"].idxmax()
    out = {
        "source": "SRC-001 Epoch notable_ai_models.csv, Domain=Language (tokens)",
        "fit_all": full,
        "fit_2018plus": modern,
        "max_tokens": float(df["tokens"].max()),
        "max_tokens_model": str(df.loc[imax, "Model"]),
        "max_tokens_date": df.loc[imax, "date"].strftime("%Y-%m-%d"),
        "top5_recent_2025plus": [
            {"model": str(r.Model), "date": r.date.strftime("%Y-%m-%d"), "tokens": float(r.tokens)}
            for r in recent.itertuples()
        ],
        "human_text_stock_context": (
            "CROSSOVER needs Epoch's REPORTED usable human-text stock (order ~1e14 tokens); "
            "NOT measured here — source from arXiv:2211.04325 / Epoch data paper before use."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"language models with tokens+date: {full['n']}")
    for f in (full, modern):
        print(f"  [{f['label']:32}] n={f['n']:3}  {f['x_per_year']}x/yr  "
              f"{f['doublings_per_year']} doublings/yr  {f['years_per_10x']} yr/10x  "
              f"R2={f['r2']}  ({f['date_min']}..{f['date_max']})")
    print(f"  max training set: {out['max_tokens']:.3g} tokens  ({out['max_tokens_model']}, {out['max_tokens_date']})")
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
