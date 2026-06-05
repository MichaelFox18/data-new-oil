"""Chapter-6 figure — Hubbert's 1956 forecast vs. actual US crude production. Reads
results/hubbert.json ONLY; writes figures/hubbert.png. All labels from the results file.
Run: .venv/Scripts/python.exe src/viz/hubbert.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "results" / "hubbert.json"
OUT = ROOT / "figures" / "hubbert.png"


def series(dct):
    xs = sorted(int(y) for y in dct)
    return xs, [dct[str(y)] for y in xs]


def main() -> int:
    d = json.loads(RES.read_text(encoding="utf-8"))
    ax_actual = {y: v for y, v in d["actual_gb_per_year"].items() if int(y) >= 1900}
    peak, trough, recent = d["actual_conventional_peak"], d["shale_trough"], d["recent"]
    div = d["divergence"]

    ax_x, ax_y = series(ax_actual)
    h2_x, h2_y = series(d["hubbert_curves_gb_per_year"]["Q200"])
    h1_x, h1_y = series(d["hubbert_curves_gb_per_year"]["Q150"])

    fig, ax = plt.subplots(figsize=(11, 6.2))
    # shale era shading (post-trough divergence)
    ax.axvspan(trough["year"], recent["year"], color="#1a73e8", alpha=0.06)

    ax.plot(ax_x, ax_y, color="#111", lw=2.4, label="Actual US crude production (EIA)", zorder=5)
    ax.plot(h2_x, h2_y, color="#d9534f", lw=2, ls="--", label="Hubbert 1956: 200 Gb (peak 1970)")
    ax.plot(h1_x, h1_y, color="#e8902a", lw=1.6, ls=":", label="Hubbert 1956: 150 Gb (peak 1965)")

    ax.scatter([peak["year"]], [peak["gb_per_year"]], s=60, color="#111", zorder=6)
    ax.annotate(f"1970 peak ({peak['gb_per_year']:.1f} Gb/yr)\nHubbert nailed the year",
                (peak["year"], peak["gb_per_year"]), xytext=(1935, 4.3), fontsize=9, fontweight="bold",
                arrowprops=dict(arrowstyle="->"))
    ax.scatter([trough["year"]], [trough["gb_per_year"]], s=45, color="#111", zorder=6)
    ax.annotate(f"{trough['year']} trough\n({trough['gb_per_year']:.1f} Gb/yr)",
                (trough["year"], trough["gb_per_year"]), xytext=(trough["year"] - 26, 0.7), fontsize=8,
                arrowprops=dict(arrowstyle="->"))
    ax.scatter([recent["year"]], [recent["gb_per_year"]], s=70, marker="*", color="#1a73e8", zorder=7)
    ax.annotate(f"{recent['year']}: {recent['gb_per_year']:.2f} Gb/yr — all-time record\n"
                f"= {div['actual_vs_hubbert200_x']:.0f}x Hubbert's forecast (fracking)",
                (recent["year"], recent["gb_per_year"]), xytext=(1972, 4.6), fontsize=9, fontweight="bold",
                color="#1a73e8", arrowprops=dict(arrowstyle="->", color="#1a73e8"))

    ax.set_xlim(1900, recent["year"] + 2)
    ax.set_ylim(0, max(ax_y) * 1.18)
    ax.set_xlabel("Year")
    ax.set_ylabel("US crude oil production (billion barrels / year)")
    ax.set_title("Hubbert vs. actual: the 1956 forecast nailed the 1970 US peak — then fracking broke it")
    ax.legend(loc="upper left", fontsize=8.5, framealpha=0.9)
    ax.grid(True, ls=":", alpha=0.4)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
