"""Q1 — the broker census: cross-state count + overlap (CA / VT / OR / TX).

MEASURED. Cleans each registry's broker-name column (per-state encoding/delimiter/preamble
handled), drops exact-duplicate rows, normalizes names (casefold, strip punctuation +
legal-form suffixes), and dedups across states to a single national count with overlap.

Writes data/interim/brokers_normalized.csv (one row per registration: state, raw_name,
norm_name) and results/broker_census.json. Read-only on raw.

CAVEAT (stated in the finding): name-based entity resolution is imperfect — the same
company spelled differently across states will be under-merged; this is a conservative
floor on overlap and a near-ceiling on the unique count.

Run: .venv/Scripts/python.exe src/analyze/broker_census.py
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim"
OUT = ROOT / "results" / "broker_census.json"

# Conservative legal-form suffixes only (NOT group/holdings/company/the — too merge-happy).
SUFFIXES = {
    "inc", "incorporated", "llc", "llp", "llp", "lp", "ltd", "limited", "corp",
    "corporation", "co", "plc", "pllc", "pc", "gmbh", "sa", "ag", "nv", "bv",
}

# Per-state config. file is globbed from the dir; reader kwargs per source.
STATES = {
    "CA": dict(src="SRC-002", dir="cppa", name="data broker name",
               read=dict(dtype=str, keep_default_na=False)),
    "VT": dict(src="SRC-003", dir="vermont", name="Name", excel=True,
               read=dict(dtype=str)),
    "OR": dict(src="SRC-004", dir="oregon", name="full_name",
               read=dict(dtype=str, sep="|", encoding="cp1252", keep_default_na=False)),
    # TX export has a metadata preamble + a blank line before the real header, so we
    # locate the header row dynamically rather than skip a fixed count.
    "TX": dict(src="SRC-005", dir="texas", name="full legal name", header_marker="Registration Number",
               read=dict(dtype=str, header=None, keep_default_na=False)),
}


def normalize(name: str) -> str:
    s = re.sub(r"[^a-z0-9 ]+", " ", str(name).casefold())
    toks = [t for t in s.split() if t not in SUFFIXES]
    return " ".join(toks).strip()


def data_file(dirname: str) -> Path:
    cands = [p for p in (RAW / dirname).iterdir()
             if p.is_file() and p.suffix.lower() in (".csv", ".xlsx", ".xls")
             and p.name not in ("DROP_HERE.md", ".gitkeep")]
    if len(cands) != 1:
        raise SystemExit(f"expected exactly 1 data file in {dirname}/, found {len(cands)}: {cands}")
    return cands[0]


def find_name_col(cols, target: str) -> str:
    exact = [c for c in cols if c.strip().casefold() == target.casefold()]
    if exact:
        return exact[0]
    sub = [c for c in cols if target.casefold() in c.casefold()]
    if not sub:
        raise SystemExit(f"name column matching {target!r} not found in {list(cols)[:20]}")
    return sub[0]


def main() -> int:
    INTERIM.mkdir(parents=True, exist_ok=True)
    long_rows = []          # (state, raw_name, norm_name)
    per_state = {}
    name_to_states: dict[str, set] = {}

    for st, cfg in STATES.items():
        path = data_file(cfg["dir"])
        if cfg.get("excel"):
            df = pd.read_excel(path, **cfg["read"])
        else:
            df = pd.read_csv(path, **cfg["read"])
        if cfg.get("header_marker"):
            first = df.iloc[:, 0].astype(str).str.strip()
            mask = first == cfg["header_marker"]
            if not mask.any():
                raise SystemExit(f"{st}: header marker {cfg['header_marker']!r} not found")
            hidx = mask.idxmax()
            df.columns = [str(c).strip() for c in df.loc[hidx].tolist()]
            df = df.loc[hidx + 1:].reset_index(drop=True)
        raw_rows = len(df)
        df = df.drop_duplicates()
        dropped = raw_rows - len(df)
        col = find_name_col(df.columns, cfg["name"])

        names = df[col].fillna("").astype(str)
        norms = names.map(normalize)
        keep = norms.str.len() > 0
        uniq = sorted(set(norms[keep]))
        for raw, nm in zip(names[keep], norms[keep]):
            long_rows.append((st, raw.strip(), nm))
            name_to_states.setdefault(nm, set()).add(st)

        per_state[st] = {
            "src": cfg["src"], "file": path.relative_to(ROOT).as_posix(),
            "name_col": col, "raw_rows": int(raw_rows), "exact_dup_rows_dropped": int(dropped),
            "rows_with_name": int(keep.sum()), "unique_norm_names": len(uniq),
        }
        print(f"  {st}: raw={raw_rows} dup_dropped={dropped} unique_names={len(uniq)} (col={col!r})")

    # national dedup + overlap
    naive_sum = sum(v["unique_norm_names"] for v in per_state.values())
    national_unique = len(name_to_states)
    overlap = Counter(len(s) for s in name_to_states.values())
    in_all_four = sorted(nm for nm, s in name_to_states.items() if len(s) == len(STATES))

    out = {
        "states": per_state,
        "naive_sum_of_state_uniques": naive_sum,
        "national_unique_brokers": national_unique,
        "duplicates_removed_by_cross_state_dedup": naive_sum - national_unique,
        "overlap_by_state_count": {str(k): int(v) for k, v in sorted(overlap.items())},
        "brokers_in_all_4_states": {"count": len(in_all_four), "names": in_all_four},
        "method_caveat": "name-based dedup; same-entity-different-spelling under-merges",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")

    interim_path = INTERIM / "brokers_normalized.csv"
    pd.DataFrame(long_rows, columns=["state", "raw_name", "norm_name"]).to_csv(interim_path, index=False)

    print(f"\n  naive sum of per-state uniques : {naive_sum}")
    print(f"  NATIONAL UNIQUE brokers (dedup): {national_unique}")
    print(f"  removed by cross-state dedup   : {naive_sum - national_unique}")
    print(f"  overlap (states -> #brokers)   : {dict(sorted(overlap.items()))}")
    print(f"  registered in all 4 states     : {len(in_all_four)}")
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()} + {interim_path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
