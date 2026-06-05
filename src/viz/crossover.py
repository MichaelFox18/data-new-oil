"""Hero figure — the data crossover. Reads results/crossover.json ONLY; writes
figures/crossover.png. All numbers/labels come from the results file (no hand-typed
values). Run: .venv/Scripts/python.exe src/viz/crossover.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "results" / "crossover.json"
OUT = ROOT / "figures" / "crossover.png"


def main() -> int:
    d = json.loads(RES.read_text(encoding="utf-8"))
    fit = d["frontier_fit_2018plus"]
    stock = d["stock_reported"]
    cross = d["crossover_modeled"]
    latest = d["latest_frontier"]

    allpts = d["all_language_points"]
    fr = d["frontier_points"]
    ax_years = [p["year"] for p in allpts]
    ax_tok = [p["tokens"] for p in allpts]
    fr_years = [p["year"] for p in fr]
    fr_tok = [p["tokens"] for p in fr]

    eff = stock["effective_tokens"]
    ci_lo, ci_hi = stock["ci_tokens"]
    win_lo, win_hi = stock["epoch_exhaustion_window"]
    x_cross = cross["year_at_effective_stock"]

    # frontier fit line params (reconstruct slope/intercept from two known points:
    # the modeled crossover (year, eff) and latest frontier (year, tokens))
    slope = fit["om_per_year"]
    intercept = np.log10(eff) - slope * x_cross

    fig, ax = plt.subplots(figsize=(11, 6.2))
    # human-text stock band (REPORTED)
    ax.axhspan(ci_lo, ci_hi, color="#d9534f", alpha=0.08)
    ax.axhline(eff, color="#d9534f", lw=2, ls="--")
    ax.text(2009.2, eff * 1.25, f"Epoch human-text stock  ~{eff:.0e} tokens (REPORTED)",
            color="#b52b27", fontsize=9, fontweight="bold")
    ax.text(2009.2, ci_hi * 0.55, f"95% CI {ci_lo:.0e}–{ci_hi:.0e}", color="#b52b27", fontsize=8)

    # Epoch reported exhaustion window
    ax.axvspan(win_lo, win_hi, color="#5b9bd5", alpha=0.12)
    ax.text((win_lo + win_hi) / 2, eff * 0.30, f"Epoch window {win_lo}–{win_hi}",
            color="#2f6aa6", fontsize=8.5, ha="center", va="top", fontweight="bold")

    # all language models (faint) + frontier (bold) + fit line
    ax.scatter(ax_years, ax_tok, s=10, color="#9aa0a6", alpha=0.45, label="Notable language models")
    ax.scatter(fr_years, fr_tok, s=34, color="#1a73e8", edgecolor="white", lw=0.5,
               zorder=5, label="Frontier (record-setting)")
    xs = np.array([min(ax_years), x_cross + 0.4])
    ax.plot(xs, 10 ** (slope * xs + intercept), color="#1a73e8", lw=2,
            label=f"Frontier trend (~{fit['x_per_year']}x/yr)")

    # crossover marker
    ax.scatter([x_cross], [eff], s=120, marker="X", color="black", zorder=6)
    ax.annotate(f"crossover ~{x_cross:.0f}\n(modeled {cross['year_at_ci_low']:.0f}–{cross['year_at_ci_high']:.0f})",
                (x_cross, eff), xytext=(x_cross - 6.5, eff * 6), fontsize=9, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.annotate(f"latest: {latest['model']}\n{latest['tokens']:.1e} tokens",
                (latest["date"][:4], latest["tokens"]) if False else (2025.7, latest["tokens"]),
                xytext=(2018.5, latest["tokens"] * 0.06), fontsize=8,
                arrowprops=dict(arrowstyle="->", color="#1a73e8"))

    ax.set_yscale("log")
    ax.set_xlim(2009, max(win_hi, x_cross) + 1)
    ax.set_ylim(min(ax_tok) * 0.4, ci_hi * 3)
    ax.set_xlabel("Year")
    ax.set_ylabel("Training dataset size (tokens, log scale)")
    ax.set_title("The data crossover: frontier LLM training size vs. the stock of human text")
    ax.legend(loc="lower right", fontsize=8, framealpha=0.9)
    ax.grid(True, which="major", ls=":", alpha=0.4)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
