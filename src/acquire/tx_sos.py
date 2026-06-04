"""Acquire the Texas SOS Data Broker Registry official CSV export.

Per GATE-2 (Texas: official export / API first, scrape only as fallback), this uses the
Secretary of State's own published CSV export — an official government download, NOT a
scrape of the Appian portal. Idempotent; --force re-pulls.

Freshness caveat: the published export may carry an older generation date than the live
Appian registry; we record row count + retrieval date and flag staleness for Phase 4.

NOTE (2026-06-04): this official URL returns HTTP 403 to both our fetcher and a
browser-like fetch (server-side WAF), so automated download fails from here. The working
path is a manual browser download into data/raw/texas/ followed by ingest_local.py — see
data/raw/texas/DROP_HERE.md. This script is kept for documentation / in case the block lifts.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _acquire_util as A  # noqa: E402

URL = "https://www.sos.state.tx.us/statdoc/forms/registered-data-brokers.csv"
SRC_ID = "SRC-005"


def main(force: bool = False) -> int:
    dest = A.RAW / "texas" / "registered-data-brokers.csv"
    try:
        info = A.download(URL, dest, force=force)
    except Exception as e:  # noqa: BLE001
        print(f"!! FAILED TX registry CSV: {e}")
        return 1
    if info["looks_like_html"]:
        print("!! WARNING: response looks like HTML, not CSV — verify the export URL")
    rows = A.csv_rows(info["path"])
    A.log_fetch("texas", info, rows)
    print(f">> {info['status']} registered-data-brokers.csv rows={rows} bytes={info['bytes']} sha256={info['sha256'][:12]}")

    if not A.provenance_has(SRC_ID):
        block = f"""### {SRC_ID}  Texas SOS Data Broker Registry (official CSV export)
- name:           Texas Secretary of State data broker registry — published CSV export
- url:            {URL}
- access_method:  download (official SOS export; not the Appian portal, not scraped)
- retrieved_at:   {A.utc_now()}
- raw_path:       data/raw/texas/registered-data-brokers.csv
- sha256:         {info['sha256']}
- rows / size:    {rows} rows / {info['bytes']} bytes
- license/terms:  public TX government export; www.sos.state.tx.us robots.txt empty/none (2026-06-04)
- tier:           A
- caveats:        VERIFY freshness — this published export may carry an older generation
                  date than the live Appian registry; if stale, flag undercount in Phase 4.
                  Reportedly includes a data-categories field (richer than the OR export)."""
        A.provenance_append(block)
        print(f">> PROVENANCE: appended {SRC_ID}")
    else:
        print(f">> PROVENANCE: {SRC_ID} already present, not re-appending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(force="--force" in sys.argv))
