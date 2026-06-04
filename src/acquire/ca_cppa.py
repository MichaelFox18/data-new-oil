"""Acquire the California Privacy Protection Agency (CPPA) Data Broker Registry CSV.

Feeds Q1 (broker census) and Q2 (registration growth). Official download; robots.txt
allows the registry path (checked 2026-06-04). Idempotent; --force re-pulls.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _acquire_util as A  # noqa: E402

URL = "https://cppa.ca.gov/data_broker_registry/registry.csv"
SRC_ID = "SRC-002"


def main(force: bool = False) -> int:
    dest = A.RAW / "cppa" / "registry.csv"
    try:
        info = A.download(URL, dest, force=force)
    except Exception as e:  # noqa: BLE001
        print(f"!! FAILED CA registry: {e}")
        return 1
    if info["looks_like_html"]:
        print("!! WARNING: response looks like HTML, not CSV — the CSV may now sit behind")
        print("   the DROP platform. Verify the real download URL before trusting this file.")
    rows = A.csv_rows(info["path"])
    A.log_fetch("cppa", info, rows)
    print(f">> {info['status']} registry.csv rows={rows} bytes={info['bytes']} sha256={info['sha256'][:12]}")

    if not A.provenance_has(SRC_ID):
        block = f"""### {SRC_ID}  CPPA Data Broker Registry
- name:           California Privacy Protection Agency data broker registry
- url:            {URL}
- access_method:  download
- retrieved_at:   {A.utc_now()}
- raw_path:       data/raw/cppa/registry.csv
- sha256:         {info['sha256']}
- rows / size:    {rows} rows / {info['bytes']} bytes
- license/terms:  public CA government registry; robots.txt allows the registry path (2026-06-04)
- tier:           A
- caveats:        self-registration only (non-registrants absent); collection-category
                  and recipient columns to be profiled in Phase 4; reflects the 2026
                  registration cycle."""
        A.provenance_append(block)
        print(f">> PROVENANCE: appended {SRC_ID}")
    else:
        print(f">> PROVENANCE: {SRC_ID} already present, not re-appending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(force="--force" in sys.argv))
