"""Acquire US crude oil production from the EIA API (Q8 Hubbert). MEASURED, Tier A.

Reads EIA_API_KEY from .env and NEVER logs it: the fetch log and PROVENANCE store a
REDACTED url (api_key=REDACTED). Saves the raw JSON response. Idempotent; --force re-pulls.
Run: .venv/Scripts/python.exe src/acquire/eia.py
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _acquire_util as A  # noqa: E402

try:
    from dotenv import load_dotenv
    load_dotenv(A.ROOT / ".env")
except ModuleNotFoundError:
    pass

KEY = os.environ.get("EIA_API_KEY", "").strip()
BASE = "https://api.eia.gov/v2/petroleum/crd/crpdn/data/"
PARAMS = [
    ("frequency", "annual"), ("data[0]", "value"),
    ("facets[duoarea][]", "NUS"), ("facets[product][]", "EPC0"), ("facets[process][]", "FPF"),
    ("sort[0][column]", "period"), ("sort[0][direction]", "asc"), ("length", "5000"),
]
SRC_ID = "SRC-009"


def main(force: bool = False) -> int:
    if not KEY:
        print("!! EIA_API_KEY missing in .env. Stopping.")
        return 1
    dest = A.RAW / "eia" / "us_crude_production.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    safe_url = BASE + "?" + urllib.parse.urlencode(PARAMS + [("api_key", "REDACTED")])

    if dest.exists() and not force:
        data, status = dest.read_bytes(), "cached"
    else:
        url = BASE + "?" + urllib.parse.urlencode(PARAMS + [("api_key", KEY)])
        req = urllib.request.Request(url, headers={"User-Agent": A.UA})
        with urllib.request.urlopen(req, timeout=90) as r:  # noqa: S310
            data = r.read()
        # EIA echoes the request (incl. api_key) back in the JSON — redact it so the raw
        # file we persist/commit NEVER contains the secret. Data values are untouched.
        data = data.replace(KEY.encode("utf-8"), b"REDACTED")
        dest.write_bytes(data)
        status = "downloaded"

    sha = hashlib.sha256(data).hexdigest()
    rows = len(json.loads(data).get("response", {}).get("data", []))
    info = {"url": safe_url, "path": dest, "bytes": len(data), "sha256": sha, "status": status}
    A.log_fetch("eia", info, rows)
    print(f">> {status} us_crude_production.json rows={rows} bytes={len(data)} sha256={sha[:12]}")

    if not A.provenance_has(SRC_ID):
        block = f"""### {SRC_ID}  EIA US crude oil production
- name:           EIA U.S. Field Production of Crude Oil (annual, 1859- )
- url:            {safe_url}
- access_method:  api
- retrieved_at:   {A.utc_now()}
- raw_path:       data/raw/eia/us_crude_production.json
- sha256:         {sha}
- rows / size:    {rows} records (MBBL annual total + MBBL/D)
- license/terms:  US government public data; EIA API key from .env (REDACTED here, never committed)
- tier:           A
- caveats:        NUS = TOTAL US (incl. Alaska + offshore); Hubbert's 1956 forecast was
                  lower-48 only -> note that comparison caveat in the analysis."""
        A.provenance_append(block)
        print(f">> PROVENANCE: appended {SRC_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(force="--force" in sys.argv))
