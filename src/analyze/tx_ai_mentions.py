"""Q1/Q3 bridge — Texas brokers self-describing AI/ML use in free text (SRC-005).

MEASURED. The Texas registry's free-text "Categories of Data Processed and Transferred"
and "Additional Information or Explanation" fields sometimes describe AI/ML use — a second
state's AI signal beyond California's structured GenAI-sharing flag (F-01). Counts brokers
whose free text matches AI/ML terms and keeps examples + per-term counts for human review
(so false positives, e.g. standalone "ai", can be discounted). Read-only on raw.

Writes results/tx_ai_mentions.json.
Run: .venv/Scripts/python.exe src/analyze/tx_ai_mentions.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "texas" / "texas_data_brokers_2026-06-04.csv"
OUT = ROOT / "results" / "tx_ai_mentions.json"

TERMS = {
    "artificial intelligence": r"artificial intelligence",
    "machine learning": r"machine learning",
    "generative / genai": r"generative|genai",
    "llm / language model": r"\bllm\b|large language model",
    "ai (standalone)": r"\bai\b",
    "model training": r"model training|train(?:ed|ing)?\s+(?:a |an |our |the )?(?:model|ai)",
    "neural / deep learning": r"neural network|deep learning",
}


def load_tx() -> pd.DataFrame:
    df = pd.read_csv(RAW, header=None, dtype=str, keep_default_na=False)
    i = (df[0].str.strip() == "Registration Number").idxmax()
    df.columns = [str(c).strip() for c in df.loc[i]]
    return df.loc[i + 1:].reset_index(drop=True)


def main() -> int:
    df = load_tx()
    name_col = "Full Legal Name"
    text_cols = [c for c in df.columns if "Categories" in c or "Additional Information" in c]
    text = df[text_cols].astype(str).agg(" ".join, axis=1).str.lower()

    per_term, any_hit = {}, pd.Series(False, index=df.index)
    compiled = {lab: re.compile(pat) for lab, pat in TERMS.items()}
    for lab, rx in compiled.items():
        m = text.str.contains(rx, na=False)
        per_term[lab] = int(m.sum())
        any_hit = any_hit | m

    examples = []
    for i in df.index[any_hit][:15]:
        t = text.loc[i]
        examples.append({
            "name": str(df.loc[i, name_col]),
            "terms": [lab for lab, rx in compiled.items() if rx.search(t)],
            "snippet": re.sub(r"\s+", " ", t)[:200],
        })

    out = {
        "source": "SRC-005 TX registry free text",
        "n_brokers": int(len(df)),
        "brokers_with_any_ai_term": int(any_hit.sum()),
        "by_term": per_term,
        "examples": examples,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"TX brokers: {len(df)}; with any AI/ML term: {int(any_hit.sum())}")
    for lab, c in sorted(per_term.items(), key=lambda x: -x[1]):
        print(f"  {lab:24} {c}")
    print("examples:")
    for e in examples[:6]:
        print(f"  - {e['name'][:34]:34} {e['terms']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
