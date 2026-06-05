"""Acquire OpenAlex publication-year counts for human-data-for-AI terms (Q12/F-10).

MEASURED proxy for the rise of paid human-data work (RLHF, annotation): counts of works
per publication year for each term, via OpenAlex group_by. Tier A/B. No key; uses the
polite pool with a contact email pulled from SEC_EDGAR_USER_AGENT in .env — the email is
REDACTED from the logged/provenance URL (not a secret, but we don't commit personal data).

Run: .venv/Scripts/python.exe src/acquire/openalex.py
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
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

m = re.search(r"[\w.+-]+@[\w.-]+", os.environ.get("SEC_EDGAR_USER_AGENT", ""))
CONTACT = m.group(0) if m else ""

TERMS = {
    "rlhf": "reinforcement learning from human feedback",
    "human_feedback": "human feedback",
    "data_annotation": "data annotation",
    "data_labeling": "data labeling",
}
BASE = "https://api.openalex.org/works"
SRC_ID = "SRC-011"


def main(force: bool = False) -> int:
    dest_dir = A.RAW / "openalex"
    results = []
    for slug, term in TERMS.items():
        dest = dest_dir / f"{slug}.json"
        q = [("search", f'"{term}"'), ("group_by", "publication_year")]  # quotes = phrase match
        safe_url = BASE + "?" + urllib.parse.urlencode(q + [("mailto", "REDACTED")])
        if dest.exists() and not force:
            data, status = dest.read_bytes(), "cached"
        else:
            url = BASE + "?" + urllib.parse.urlencode(q + ([("mailto", CONTACT)] if CONTACT else []))
            req = urllib.request.Request(url, headers={"User-Agent": f"MaxinomicsResearch/0.1 (mailto:{CONTACT})"})
            with urllib.request.urlopen(req, timeout=60) as r:  # noqa: S310
                data = r.read()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            status = "downloaded"
            time.sleep(1.0)  # polite
        sha = hashlib.sha256(data).hexdigest()
        n = len(json.loads(data).get("group_by", []))
        info = {"url": safe_url, "path": dest, "bytes": len(data), "sha256": sha, "status": status}
        A.log_fetch("openalex", info, n)
        results.append((slug, term, info))
        print(f"  {slug:16} {status:10} year-buckets={n} sha256={sha[:12]}")

    if results and not A.provenance_has(SRC_ID):
        lines = "\n".join(f"  - {slug} (\"{term}\"): {info['path'].relative_to(A.ROOT).as_posix()} sha256={info['sha256']}"
                          for slug, term, info in results)
        block = f"""### {SRC_ID}  OpenAlex publication-year counts (human-data-for-AI terms)
- name:           OpenAlex works counts by publication year for RLHF / annotation terms
- url:            https://api.openalex.org/works?search=<term>&group_by=publication_year
- access_method:  api
- retrieved_at:   {A.utc_now()}
- raw_path:       data/raw/openalex/  (files below)
{lines}
- license/terms:  OpenAlex CC0; polite pool (contact email REDACTED from logged URL)
- tier:           A/B (bibliometric aggregator over crossref/MAG/etc.)
- caveats:        'search' is full-text-ish (counts any work mentioning the phrase) -> a
                  PROXY for field growth, NOT job counts; 2026 is a partial year; a few
                  future-dated buckets (2027, 2036) are upstream date errors -> drop them."""
        A.provenance_append(block)
        print(f">> PROVENANCE: appended {SRC_ID}")
    return 0 if results else 1


if __name__ == "__main__":
    raise SystemExit(main(force="--force" in sys.argv))
