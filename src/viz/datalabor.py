"""F-10 figure — the rise of human-data-for-AI research (OpenAlex MEASURED proxy). Reads
results/datalabor.json ONLY; writes figures/datalabor.png. Labels from the results file.
Run: .venv/Scripts/python.exe src/viz/datalabor.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "results" / "datalabor.json"
OUT = ROOT / "figures" / "datalabor.png"

STYLE = {
    "rlhf": ("#1a73e8", "RLHF (reinforcement learning from human feedback)", 2.6),
    "human_feedback": ("#e8902a", "human feedback", 1.8),
    "data_annotation": ("#3a9d4e", "data annotation", 1.8),
    "data_labeling": ("#9aa0a6", "data labeling", 1.8),
}


def main() -> int:
    d = json.loads(RES.read_text(encoding="utf-8"))
    fig, ax = plt.subplots(figsize=(11, 6.2))

    for slug, (color, label, lw) in STYLE.items():
        by_year = d["series"][slug]["by_year"]
        xs = sorted(int(y) for y in by_year if 2015 <= int(y) <= 2025)
        ys = [by_year[str(y)] for y in xs]
        ax.plot(xs, ys, color=color, lw=lw, marker="o", ms=3.5, label=label)

    rlhf = d["series"]["rlhf"]["by_year"]
    g = d["growth"]["rlhf"]["2021_to_2024_x"]
    ax.annotate(f"RLHF papers: ~{rlhf.get('2021')}/yr in 2021 → ~{rlhf.get('2024')}/yr in 2024\n(~{g:.0f}x — the post-ChatGPT human-feedback boom)",
                xy=(2024, rlhf["2024"]), xytext=(2015.4, 1600), fontsize=9, fontweight="bold",
                color="#1a73e8", bbox=dict(boxstyle="round", fc="#eaf1fc", ec="#1a73e8", alpha=0.9),
                arrowprops=dict(arrowstyle="->", color="#1a73e8"))

    ax.set_yscale("log")
    ax.set_xlim(2015, 2025.4)
    ax.set_xlabel("Publication year")
    ax.set_ylabel("OpenAlex works mentioning the phrase (log scale)")
    ax.set_title("The data-labor signal: human-feedback AI research exploded (OpenAlex — a PROXY, not job counts)")
    ax.legend(loc="upper left", fontsize=8.5, framealpha=0.9)
    ax.grid(True, which="major", ls=":", alpha=0.4)
    ax.text(0.99, 0.02, "Proxy for the field; true job counts are NEEDS-DATA", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=7.5, color="#777", style="italic")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
