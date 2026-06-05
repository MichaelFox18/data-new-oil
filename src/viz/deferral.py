"""Q5 figure — the synthetic-data deferral overlay (MODELED). Reads results/crossover.json
+ results/deferral.json ONLY; writes figures/deferral.png. Shows the wall sliding right as
synthetic data multiplies the effective training pool (each 10x ~= +3 years).
Run: .venv/Scripts/python.exe src/viz/deferral.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CROSS = ROOT / "results" / "crossover.json"
DEF = ROOT / "results" / "deferral.json"
OUT = ROOT / "figures" / "deferral.png"

SHOW = {1: ("#d9534f", "human stock only"), 10: ("#e8902a", "+ synthetic 10x"),
        100: ("#3a9d4e", "+ synthetic 100x")}


def main() -> int:
    d = json.loads(CROSS.read_text(encoding="utf-8"))
    dz = json.loads(DEF.read_text(encoding="utf-8"))
    fit, stock = d["frontier_fit_2018plus"], d["stock_reported"]
    eff, g, t0 = stock["effective_tokens"], stock["growth_rate_per_year_central"], stock["anchor_year"]
    slope = fit["om_per_year"]
    yc = d["crossover_modeled"]["year_central"]
    lev = dz["years_deferred_per_10x_effective_data"]
    by_m = {sc["synthetic_multiplier"]: sc for sc in dz["scenarios"]}

    intercept = np.log10(eff * (1 + g) ** (yc - t0)) - slope * yc

    allpts, fr = d["all_language_points"], d["frontier_points"]
    xmax = 2040
    xline = np.linspace(2009, xmax, 240)

    fig, ax = plt.subplots(figsize=(11.2, 6.3))
    ax.scatter([p["year"] for p in allpts], [p["tokens"] for p in allpts],
               s=9, color="#9aa0a6", alpha=0.4, label="Notable language models")
    ax.scatter([p["year"] for p in fr], [p["tokens"] for p in fr],
               s=30, color="#1a73e8", edgecolor="white", lw=0.5, zorder=5, label="Frontier")
    ax.plot([2010, xmax], 10 ** (slope * np.array([2010, xmax]) + intercept),
            color="#1a73e8", lw=2, label=f"Frontier trend (~{fit['x_per_year']}x/yr)")

    # human stock + synthetic-augmented effective-stock lines, each with its crossover X
    for m, (color, lab) in SHOW.items():
        ax.plot(xline, eff * m * (1 + g) ** (xline - t0), color=color, lw=2,
                ls="--", alpha=0.9, label=f"{lab}" + (" (MODELED)" if m > 1 else " (REPORTED)"))
        yr = by_m[m]["crossover_year"]
        yv = eff * m * (1 + g) ** (yr - t0)
        ax.scatter([yr], [yv], s=110, marker="X", color=color, edgecolor="black", lw=0.6, zorder=6)
        ax.text(yr, yv * 1.7, f"~{yr:.0f}", color=color, fontsize=9, fontweight="bold", ha="center")

    ax.annotate(f"each 10x of (synthetic) data\nslides the wall only ~{lev:.0f} years\n"
                f"(1000x → ~{by_m[1000]['crossover_year']:.0f})",
                xy=(by_m[100]["crossover_year"], eff * 100), xytext=(2010.5, 8e15),
                fontsize=9, fontweight="bold", color="#333",
                bbox=dict(boxstyle="round", fc="#fff7e6", ec="#e8902a", alpha=0.9))

    ax.set_yscale("log")
    ax.set_xlim(2009, xmax)
    ax.set_ylim(min(p["tokens"] for p in allpts) * 0.5, 1e17)
    ax.set_xlabel("Year")
    ax.set_ylabel("Training data available / used (tokens, log scale)")
    ax.set_title("The deferral overlay: synthetic data slides the wall right ~3 yr per 10x (MODELED)")
    ax.legend(loc="lower right", fontsize=7.5, framealpha=0.92, ncol=2)
    ax.grid(True, which="major", ls=":", alpha=0.4)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
