"""Ingest a manually-placed raw file (e.g. Vermont/Oregon registries).

Per the GATE-2 decisions, VT (portal bulk download) and OR (manual export) are NOT
scraped — the human places the file under data/raw/<source>/. This script hashes the
file in place, logs a fetch line, and appends a PROVENANCE entry. It never modifies
the raw file.

Example:
  py src/acquire/ingest_local.py --source vermont --src-id SRC-003 \
     --name "Vermont SOS Data Broker registry (bulk download)" \
     --url "https://bizfilings.vermont.gov" --tier A --access portal \
     --notes "manual bulk download per GATE-2" data/raw/vermont/<file>
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _acquire_util as A  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Hash + log a manually-placed raw file.")
    ap.add_argument("file", help="path to the placed raw file (under data/raw/<source>/)")
    ap.add_argument("--source", required=True)
    ap.add_argument("--src-id", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--tier", default="A")
    ap.add_argument("--access", default="manual", help="manual | portal | download")
    ap.add_argument("--notes", default="")
    a = ap.parse_args()

    path = Path(a.file).resolve()
    if not path.exists():
        print(f"!! file not found: {path}")
        return 1

    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    rows = A.csv_rows(path)
    rel = path.relative_to(A.ROOT).as_posix() if A.ROOT in path.parents else path.name
    info = {"url": a.url, "path": path, "bytes": len(data), "sha256": sha, "status": "ingested"}
    A.log_fetch(a.source, info, rows)
    print(f">> ingested {rel} rows={rows} bytes={len(data)} sha256={sha[:12]}")

    if not A.provenance_has(a.src_id):
        block = f"""### {a.src_id}  {a.name}
- name:           {a.name}
- url:            {a.url}
- access_method:  {a.access}
- retrieved_at:   {A.utc_now()}
- raw_path:       {rel}
- sha256:         {sha}
- rows / size:    {rows} rows / {len(data)} bytes
- license/terms:  public government registry; obtained manually (not scraped)
- tier:           {a.tier}
- caveats:        {a.notes}"""
        A.provenance_append(block)
        print(f">> PROVENANCE: appended {a.src_id}")
    else:
        print(f">> PROVENANCE: {a.src_id} already present, not re-appending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
