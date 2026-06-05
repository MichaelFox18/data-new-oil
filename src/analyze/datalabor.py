"""F-10 — the rise of human-data-for-AI work, MEASURED via OpenAlex (SRC-011).

A PROXY (research-publication counts), NOT a job count. Loads the per-term year buckets,
keeps full years 2010-2025 (drops pre-2010 noise and the upstream future-dated errors like
2027/2036), reports the trajectory + growth multiples. Writes results/datalabor.json.

The market/company figures (Scale, Mercor, CAGR) are REPORTED context only and live in the
F-10 card, NOT here — this file holds only what we MEASURED. Read-only on raw.
Run: .venv/Scripts/python.exe src/analyze/datalabor.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "acquire"))
import _acquire_util as A  # noqa: E402

ROOT = A.ROOT
RAW = ROOT / "data" / "raw" / "openalex"
OUT = ROOT / "results" / "datalabor.json"

TERMS = {
    "rlhf": "reinforcement learning from human feedback",
    "human_feedback": "human feedback",
    "data_annotation": "data annotation",
    "data_labeling": "data labeling",
}


def load(slug: str) -> dict[int, int]:
    d = json.loads((RAW / f"{slug}.json").read_text(encoding="utf-8"))
    return {int(g["key"]): g["count"] for g in d["group_by"] if g["key"] and str(g["key"]).isdigit()}


def main() -> int:
    out = {
        "type": "MEASURED proxy: OpenAlex publication counts for human-data-for-AI terms; NOT a job count",
        "series": {}, "growth": {},
        "caveats": [
            "Counts works MENTIONING the phrase (full-text-ish) -> proxy for field growth, not jobs.",
            "2026 is a partial year (retrieved mid-2026); future-dated buckets (2027/2036) dropped as errors.",
            "The 2022->2023 jump is partly the real RLHF/ChatGPT boom and partly indexing lag.",
        ],
    }
    for slug, term in TERMS.items():
        c = load(slug)
        series = {y: c[y] for y in sorted(c) if 2010 <= y <= 2025}

        def g(a: int, b: int) -> float | None:
            return round(series[b] / series[a], 1) if series.get(a) and series.get(b) else None

        out["series"][slug] = {"term": term, "by_year": series, "2026_partial": c.get(2026)}
        out["growth"][slug] = {"2021_to_2024_x": g(2021, 2024), "2017_to_2024_x": g(2017, 2024),
                               "count_2024": series.get(2024)}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print("OpenAlex publications/year (MEASURED proxy; 2024 full year):")
    for slug in TERMS:
        s = out["series"][slug]["by_year"]
        gr = out["growth"][slug]
        print(f"  {slug:16} 2021={s.get(2021)!s:>5} 2024={s.get(2024)!s:>6}  "
              f"(2021->2024 = {gr['2021_to_2024_x']}x)")
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
