"""Q1/human-layer — California brokers' CCPA consumer-request volumes (SRC-002).

MEASURED. The CPPA registry makes every broker report, for calendar year 2024 (filed in
the 2026 cycle), the volume of consumer privacy requests it received across five request
types, how many it complied with / denied, and response times. We aggregate these into
the scale of consumer pushback and the concentration across brokers. Read-only on raw.

Writes results/ca_requests.json. Numbers with thousands separators are cleaned before
parsing; blanks are treated as missing (a broker that didn't report), not zero.

Run: .venv/Scripts/python.exe src/analyze/ca_requests.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "cppa" / "registry.csv"
OUT = ROOT / "results" / "ca_requests.json"
NAME_NEEDLE = "data broker name"

REQUEST_TYPES = {
    "delete": "Requests to delete",
    "know_collected": "Requests to know what personal information is being collected",
    "know_sold_shared": "Requests to know what personal information is sold or shared",
    "opt_out": "Requests to opt out of sale or sharing",
    "limit_sensitive": "Requests to limit the use and disclosure of sensitive personal information",
}


def num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.replace(",", "", regex=False).str.strip(), errors="coerce")


def pick(cols, prefix, *, endswith=None, contains=None):
    cand = [c for c in cols if c.startswith(prefix)]
    if endswith:
        cand = [c for c in cand if c.rstrip().endswith(endswith)]
    if contains:
        cand = [c for c in cand if contains in c]
    return cand[0] if cand else None


def main() -> int:
    df = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    n = len(df)
    cols = list(df.columns)
    name_col = next(c for c in cols if NAME_NEEDLE in c.lower())

    out = {"source": "SRC-002 CPPA registry", "reference_year": 2024, "n_brokers": int(n), "by_type": {}}
    per_broker_total = pd.Series(0.0, index=df.index)
    grand = {"received": 0, "complied": 0, "denied": 0}

    print(f"CA registry: {n} brokers — CCPA request volumes (CY2024)")
    for key, prefix in REQUEST_TYPES.items():
        c_total = pick(cols, prefix, endswith="Total requests received")
        c_whole = pick(cols, prefix, endswith="Complied in whole")
        c_part = pick(cols, prefix, endswith="Complied in part")
        c_denied = pick(cols, prefix, endswith="Denied")
        c_median = pick(cols, prefix, contains="Median")
        if not c_total:
            print(f"  !! {key}: total column not found"); continue

        total = num(df[c_total])
        whole = num(df[c_whole]) if c_whole else pd.Series(dtype=float)
        part = num(df[c_part]) if c_part else pd.Series(dtype=float)
        denied = num(df[c_denied]) if c_denied else pd.Series(dtype=float)
        median_days = num(df[c_median]) if c_median else pd.Series(dtype=float)

        received = int(total.fillna(0).sum())
        complied = int(whole.fillna(0).sum() + part.fillna(0).sum())
        den = int(denied.fillna(0).sum())
        reporting = int((total.fillna(0) > 0).sum())
        med_days = median_days[total.fillna(0) > 0].median()

        out["by_type"][key] = {
            "column": c_total, "received": received, "complied": complied, "denied": den,
            "compliance_rate": round(complied / received, 3) if received else None,
            "brokers_reporting_gt0": reporting,
            "median_response_days_across_brokers": (None if pd.isna(med_days) else round(float(med_days), 1)),
        }
        per_broker_total = per_broker_total.add(total.fillna(0), fill_value=0)
        grand["received"] += received; grand["complied"] += complied; grand["denied"] += den
        print(f"  {key:16} received={received:>10,}  complied={complied:>10,}  "
              f"rate={out['by_type'][key]['compliance_rate']}  brokers>0={reporting}  med_days={out['by_type'][key]['median_response_days_across_brokers']}")

    # concentration across all five types
    order = per_broker_total.sort_values(ascending=False)
    total_all = float(per_broker_total.sum())
    top10 = order.head(10)
    top1pct = order.head(max(1, n // 100))
    out["all_types"] = {
        "received": grand["received"], "complied": grand["complied"], "denied": grand["denied"],
        "compliance_rate": round(grand["complied"] / grand["received"], 3) if grand["received"] else None,
        "top10_share_of_requests": round(float(top10.sum()) / total_all, 3) if total_all else None,
        "top1pct_share_of_requests": round(float(top1pct.sum()) / total_all, 3) if total_all else None,
        "brokers_with_zero_requests": int((per_broker_total == 0).sum()),
        "top5_brokers": [
            {"name": str(df.loc[i, name_col]), "total_requests": int(per_broker_total.loc[i])}
            for i in top10.head(5).index
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")

    a = out["all_types"]
    print(f"\n  ALL TYPES: received={a['received']:,} complied={a['complied']:,} "
          f"(rate {a['compliance_rate']}) denied={a['denied']:,}")
    print(f"  concentration: top-10 brokers = {a['top10_share_of_requests']:.1%} of all requests; "
          f"{a['brokers_with_zero_requests']} of {n} brokers reported zero")
    print(f"  busiest: " + ", ".join(f"{b['name']} ({b['total_requests']:,})" for b in a["top5_brokers"]))
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
