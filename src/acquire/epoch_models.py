"""Acquire Epoch AI model datasets (CC-BY).

Feeds Q4 (training-set-size growth) and the training side of the Q3 crossover.
Downloads the Notable / Frontier / Large-Scale model CSVs. Idempotent; --force re-pulls.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _acquire_util as A  # noqa: E402

FILES = {
    "notable_ai_models.csv": "https://epoch.ai/data/notable_ai_models.csv",
    "frontier_ai_models.csv": "https://epoch.ai/data/frontier_ai_models.csv",
    "large_scale_ai_models.csv": "https://epoch.ai/data/large_scale_ai_models.csv",
}
SRC_ID = "SRC-001"


def main(force: bool = False) -> int:
    dest_dir = A.RAW / "epoch"
    results = []
    for name, url in FILES.items():
        try:
            info = A.download(url, dest_dir / name, force=force)
        except Exception as e:  # noqa: BLE001
            print(f"!! FAILED {name}: {e}")
            continue
        if info["looks_like_html"]:
            print(f"!! WARNING {name}: response looks like HTML, not CSV — verify endpoint")
        rows = A.csv_rows(info["path"])
        A.log_fetch("epoch", info, rows)
        results.append((name, info, rows))
        print(f">> {info['status']:10} {name:28} rows={rows} bytes={info['bytes']} sha256={info['sha256'][:12]}")

    if not results:
        return 1
    if not A.provenance_has(SRC_ID):
        files_md = "\n".join(
            f"  - {name}: rows={rows}, sha256={info['sha256']}" for name, info, rows in results
        )
        block = f"""### {SRC_ID}  Epoch AI — model datasets
- name:           Epoch AI, Data on Notable AI Models (+ Frontier, Large-Scale subsets)
- url:            https://epoch.ai/data/ai-models  (per-file CSVs at epoch.ai/data/)
- access_method:  download
- retrieved_at:   {A.utc_now()}
- raw_path:       data/raw/epoch/  (files below)
{files_md}
- rows / size:    see per-file rows above
- license/terms:  CC-BY (free to use/redistribute with attribution to Epoch AI)
- tier:           A (originating research group's own published dataset)
- caveats:        training-dataset-size field coverage varies by model; verify exact
                  column names in Phase 4; Epoch updates these CSVs ~daily, so the
                  retrieved_at snapshot date matters for reproducibility."""
        A.provenance_append(block)
        print(f">> PROVENANCE: appended {SRC_ID}")
    else:
        print(f">> PROVENANCE: {SRC_ID} already present, not re-appending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(force="--force" in sys.argv))
