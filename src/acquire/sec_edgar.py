"""Acquire SEC EDGAR XBRL company facts for the 'exhaust premium' analysis (Q6).

Resolves tickers -> CIK via SEC's official company_tickers.json, then downloads each
company's companyfacts JSON (all standard-taxonomy XBRL facts). Reads
SEC_EDGAR_USER_AGENT from .env (SEC requires a descriptive UA incl. a contact email).
Saves raw + appends provenance. Stdlib + python-dotenv only.

NOTE: revenue lives in us-gaap XBRL; per-user metrics (MAU/DAU/ARPU) are usually company
EXTENSION tags that the companyfacts API does NOT return — so the analysis step checks
what's actually present before promising an ARPU.

Run: .venv/Scripts/python.exe src/acquire/sec_edgar.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _acquire_util as A  # noqa: E402

try:
    from dotenv import load_dotenv
    load_dotenv(A.ROOT / ".env")
except ModuleNotFoundError:
    pass

UA = os.environ.get("SEC_EDGAR_USER_AGENT", "").strip()
TICKERS = ["META", "GOOGL", "SNAP", "RDDT", "PINS"]
TICKER_MAP_URL = "https://www.sec.gov/files/company_tickers.json"


def main(force: bool = False) -> int:
    if not UA or "@" not in UA:
        print("!! SEC_EDGAR_USER_AGENT missing/invalid in .env (need 'Name email@x.com'). Stopping.")
        return 1
    dest = A.RAW / "sec"

    info = A.download(TICKER_MAP_URL, dest / "company_tickers.json", ua=UA, force=force)
    A.log_fetch("sec", info, None)
    tmap = json.loads(info["path"].read_text(encoding="utf-8"))
    by_ticker = {v["ticker"].upper(): v for v in tmap.values()}

    results = []
    for t in TICKERS:
        rec = by_ticker.get(t)
        if not rec:
            print(f"  !! {t}: not in ticker map")
            continue
        cik10 = str(rec["cik_str"]).zfill(10)
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json"
        time.sleep(0.3)  # SEC politeness
        try:
            fi = A.download(url, dest / f"companyfacts_{t}.json", ua=UA, force=force)
        except Exception as e:  # noqa: BLE001
            print(f"  !! {t} (CIK {cik10}): {e}")
            continue
        A.log_fetch("sec", fi, None)
        results.append((t, rec["title"], cik10, fi))
        print(f"  {t:6} {rec['title'][:32]:32} CIK {cik10}  {fi['status']:10} {fi['bytes']:>10,} b")

    if results and not A.provenance_has("SRC-006"):
        lines = "\n".join(
            f"  - {t} ({title}, CIK {cik}): companyfacts_{t}.json sha256={fi['sha256']}"
            for t, title, cik, fi in results
        )
        block = f"""### SRC-006  SEC EDGAR XBRL company facts
- name:           SEC EDGAR companyfacts (XBRL) for platform revenue/ARPU (Q6)
- url:            https://data.sec.gov/api/xbrl/companyfacts/CIK<cik>.json (+ company_tickers.json)
- access_method:  api
- retrieved_at:   {A.utc_now()}
- raw_path:       data/raw/sec/  (files below)
{lines}
- sha256:         see per-file above; company_tickers.json sha256={info['sha256']}
- rows / size:    JSON fact sets
- license/terms:  US government public filings; SEC fair-access UA sent (no key)
- tier:           A
- caveats:        revenue is in us-gaap XBRL; user counts (MAU/DAU/ARPU) are usually
                  company EXTENSION tags NOT returned by companyfacts -> may need filing text."""
        A.provenance_append(block)
        print(">> PROVENANCE: appended SRC-006")
    return 0 if results else 1


if __name__ == "__main__":
    raise SystemExit(main(force="--force" in sys.argv))
