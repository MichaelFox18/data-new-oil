"""Q6 exhaust premium — annualized revenue per user per platform.

Combines MEASURED FY2025 revenue (results/sec_revenue.json, SRC-006) with user counts
REPORTED in each FY2025 10-K (SRC-007; quoted below with source URLs + retrieval date,
re-derivable via src/acquire/sec_user_metrics.py). Computes annual revenue / reported
users. Google is revenue-only (reports no per-user metric).

COMPARABILITY: Meta DAP, Snap DAU, Reddit DAUq are DAILY actives; Pinterest MAU is
MONTHLY actives (a larger base -> lower per-user), so the per-user figures are not
strictly apples-to-apples across the daily/monthly split.

Run: .venv/Scripts/python.exe src/analyze/sec_arpu.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "acquire"))
import _acquire_util as A  # noqa: E402

ROOT = A.ROOT
REV = ROOT / "results" / "sec_revenue.json"
OUT = ROOT / "results" / "sec_arpu.json"
RETRIEVED = "2026-06-05"

# REPORTED user metrics, quoted from each FY2025 10-K (period 2025-12-31).
USERS = {
    "META": {"metric": "Family DAP (daily active people, avg Dec 2025)", "users": 3.58e9,
             "quote": "Family daily active people (DAP) was 3.58 billion on average for December 2025",
             "url": "https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm"},
    "SNAP": {"metric": "DAU (avg quarter ended Dec 31 2025)", "users": 474e6,
             "quote": "We had 474 million daily active users, or DAUs, on average in the quarter ended December 31, 2025; ARPU was $3.62 in Q4 2025",
             "url": "https://www.sec.gov/Archives/edgar/data/1564408/000156440826000013/snap-20251231.htm"},
    "RDDT": {"metric": "DAUq (avg three months ended Dec 31 2025)", "users": 121.4e6,
             "quote": "an average of 121.4 million daily active uniques (DAUq) ... three months ended December 31, 2025",
             "url": "https://www.sec.gov/Archives/edgar/data/1713445/000171344526000022/rddt-20251231.htm"},
    "PINS": {"metric": "global MAU (monthly active users, ~Q4 2025)", "users": 619e6,
             "quote": "619 million monthly active users from around the world come to Pinterest",
             "url": "https://www.sec.gov/Archives/edgar/data/1506293/000150629326000021/pins-20251231.htm"},
}


def main() -> int:
    rev = json.loads(REV.read_text(encoding="utf-8"))["companies"]
    out = {
        "reference_year": 2025,
        "note": "annual FY2025 revenue / reported users; DAP/DAU/DAUq are daily, PINS MAU monthly (not strictly comparable)",
        "companies": {},
    }
    print("Annualized revenue per user (FY2025 revenue / reported users):")
    for t, u in USERS.items():
        r = rev[t]["revenue_usd"]
        arpu = r / u["users"]
        out["companies"][t] = {
            "revenue_usd": r, "metric": u["metric"], "users": u["users"],
            "annual_rev_per_user_usd": round(arpu, 2), "source_url": u["url"],
        }
        print(f"  {t:6} ${r/1e9:6.1f}B / {u['users']/1e6:7.1f}M {u['metric'].split('(')[0].strip():28} = ${arpu:6.2f}/user/yr")
    g = rev["GOOGL"]["revenue_usd"]
    out["companies"]["GOOGL"] = {"revenue_usd": g, "metric": "no per-user metric reported", "annual_rev_per_user_usd": None}
    print(f"  GOOGL  ${g/1e9:6.1f}B  (no per-user metric reported)")

    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")

    if not A.provenance_has("SRC-007"):
        lines = "\n".join(
            f"  - {t}: {u['metric']} = {u['users']:.0f}  | \"{u['quote']}\"  [{u['url']}]"
            for t, u in USERS.items()
        )
        block = f"""### SRC-007  Platform user metrics (FY2025 10-K, REPORTED)
- name:           FY2025 10-K user metrics for ARPU (Meta / Snap / Reddit / Pinterest)
- url:            per-company below (SEC EDGAR 10-K documents, period 2025-12-31)
- access_method:  download (10-K HTML via SEC UA) — quoted text, not XBRL-tagged
- retrieved_at:   {RETRIEVED}
- raw_path:       N/A (REPORTED quotes; re-derive with src/acquire/sec_user_metrics.py)
{lines}
- tier:           A (company filings)
- caveats:        DAP/DAU/DAUq are DAILY actives; PINS MAU is MONTHLY (larger base) -> not
                  strictly comparable; user metrics are Q4-2025 point-in-time averages vs
                  full-year revenue, so the ratio is an approximate annual rev-per-user."""
        A.provenance_append(block)
        print(">> PROVENANCE: appended SRC-007")
    print(f">> wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
