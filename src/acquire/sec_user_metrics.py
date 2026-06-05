"""Pull platform user metrics from the FY2025 10-Ks (REPORTED, Tier A) for Q6 ARPU.

SEC does not XBRL-tag user counts, so we fetch each 10-K HTML with the declared
SEC_EDGAR_USER_AGENT, strip tags, and print short context windows around the key-metric
phrases. Read the exact reported figures from the output, then cite them (URL + retrieval
date) in PROVENANCE/F-06. Run: .venv/Scripts/python.exe src/acquire/sec_user_metrics.py
"""

from __future__ import annotations

import os
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _acquire_util as A  # noqa: E402

try:
    from dotenv import load_dotenv
    load_dotenv(A.ROOT / ".env")
except ModuleNotFoundError:
    pass

UA = os.environ.get("SEC_EDGAR_USER_AGENT", "").strip()

TENK = {
    "META": "https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm",
    "SNAP": "https://www.sec.gov/Archives/edgar/data/1564408/000156440826000013/snap-20251231.htm",
    "RDDT": "https://www.sec.gov/Archives/edgar/data/1713445/000171344526000022/rddt-20251231.htm",
    "PINS": "https://www.sec.gov/Archives/edgar/data/1506293/000150629326000021/pins-20251231.htm",
}
KEYWORDS = ["daily active", "monthly active", "average revenue per", "ARPU", "DAUq", "DAP)"]


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:  # noqa: S310
        html = r.read().decode("utf-8", "replace")
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&#160;|&nbsp;|&#8217;|&#8220;|&#8221;", " ", text)
    return re.sub(r"\s+", " ", text)


def main() -> int:
    if not UA or "@" not in UA:
        print("!! SEC_EDGAR_USER_AGENT missing/invalid in .env. Stopping.")
        return 1
    for t, url in TENK.items():
        try:
            text = fetch_text(url)
        except Exception as e:  # noqa: BLE001
            print(f"!! {t}: {e}")
            continue
        print(f"\n===== {t}  ({len(text):,} chars) =====")
        for kw in KEYWORDS:
            hits = [m.start() for m in re.finditer(re.escape(kw), text, re.I)][:3]
            for pos in hits:
                snippet = text[max(0, pos - 70): pos + 90]
                print(f"  [{kw}] …{snippet.strip()}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
