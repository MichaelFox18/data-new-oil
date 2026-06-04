"""Shared helpers for Phase 3 acquisition fetchers (stdlib only).

Each fetcher downloads a raw artifact to data/raw/<source>/, hashes it, writes a
fetch-log line, and appends a PROVENANCE entry (idempotently). Raw is immutable
(CLAUDE.md §2.6): a fetcher caches and will not re-download an existing file unless
--force is passed. No transformation happens here — we store exactly what was returned.
"""

from __future__ import annotations

import csv
import datetime
import hashlib
import re
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROVENANCE = ROOT / "data" / "PROVENANCE.md"
LOG = ROOT / "logs" / "acquire.log"

# Polite, identifying User-Agent (no personal data); points at the project repo.
UA = "MaxinomicsDataResearch/0.1 (+https://github.com/MichaelFox18/data-new-oil)"

HTML_SNIFF = (b"<!doctype html", b"<html", b"<!DOCTYPE HTML")


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def download(url: str, dest: Path, *, ua: str = UA, force: bool = False) -> dict:
    """Fetch url -> dest (cached unless force). Returns metadata incl. sha256 + a
    `looks_like_html` flag so a fetcher can warn when a CSV endpoint returned a page."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not force:
        data = dest.read_bytes()
        status = "cached"
    else:
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        with urllib.request.urlopen(req, timeout=90) as r:  # noqa: S310 (trusted gov/research hosts)
            data = r.read()
        dest.write_bytes(data)
        status = "downloaded"
    head = data[:512].lower()
    return {
        "url": url,
        "path": dest,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "status": status,
        "looks_like_html": any(s in head for s in (b"<!doctype html", b"<html")),
    }


def csv_rows(path: Path) -> int | None:
    """Data-row count (excluding header). None if it can't be parsed as CSV."""
    try:
        with path.open(newline="", encoding="utf-8", errors="replace") as f:
            n = sum(1 for _ in csv.reader(f))
        return max(n - 1, 0)
    except Exception:
        return None


def xlsx_rows(path: Path) -> int | None:
    """Best-effort data-row count for an .xlsx (first worksheet, minus header) via
    stdlib zip/xml — avoids a dependency just to log provenance. None if unreadable.
    Full column profiling happens in Phase 4 with a proper reader."""
    try:
        with zipfile.ZipFile(path) as z:
            sheets = sorted(
                n for n in z.namelist()
                if n.startswith("xl/worksheets/sheet") and n.endswith(".xml")
            )
            if not sheets:
                return None
            xml = z.read(sheets[0]).decode("utf-8", "replace")
        n = len(re.findall(r"<row[ >]", xml))
        return max(n - 1, 0)
    except Exception:
        return None


def log_fetch(source: str, info: dict, rows) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    rel = info["path"].relative_to(ROOT).as_posix()
    line = (
        f"{utc_now()}\t{source}\t{info['status']}\t{info['url']}\t{rel}"
        f"\tbytes={info['bytes']}\trows={rows}\tsha256={info['sha256']}\n"
    )
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line)


def provenance_has(src_id: str) -> bool:
    if not PROVENANCE.exists():
        return False
    txt = PROVENANCE.read_text(encoding="utf-8")
    return f"### {src_id} " in txt or f"### {src_id}\n" in txt


def provenance_append(block: str) -> None:
    with PROVENANCE.open("a", encoding="utf-8") as f:
        f.write("\n" + block.rstrip() + "\n")
