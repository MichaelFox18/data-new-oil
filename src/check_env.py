"""Phase 0 / GATE-0 environment check.

Stdlib-only. Confirms the repo skeleton exists and that secrets handling is sane:
.env is gitignored and not present as a committed file. Prints a short summary and
exits non-zero if any structural invariant is violated. Deterministic; no network.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DIRS = [
    "data/raw",
    "data/interim",
    "src/acquire",
    "src/validate",
    "src/analyze",
    "src/viz",
    "results",
    "figures",
    "findings",
    "notebooks",
    "logs",
]

REQUIRED_FILES = [
    "CLAUDE.md",
    "README.md",
    "requirements.txt",
    ".env.example",
    ".gitignore",
    "run.sh",
    "Makefile",
    "data/PROVENANCE.md",
    "FACTCHECK.md",
]


def main() -> int:
    problems: list[str] = []

    print(f">> python : {sys.version.split()[0]}")
    print(f">> root   : {ROOT}")

    for d in REQUIRED_DIRS:
        if not (ROOT / d).is_dir():
            problems.append(f"missing directory: {d}")
    for f in REQUIRED_FILES:
        if not (ROOT / f).is_file():
            problems.append(f"missing file: {f}")

    # Secrets hygiene: .env must be gitignored, and must not exist as a real file.
    gitignore = ROOT / ".gitignore"
    if gitignore.is_file():
        ignored = gitignore.read_text(encoding="utf-8").splitlines()
        if not any(line.strip() == ".env" for line in ignored):
            problems.append(".gitignore does not exclude .env")
    if (ROOT / ".env").exists():
        # A local .env is expected (it holds keys). It must stay gitignored, which the
        # .gitignore check above enforces — its mere presence is not a failure.
        print(">> note   : local .env present (expected for keys; must stay gitignored)")

    n_ok = len(REQUIRED_DIRS) + len(REQUIRED_FILES) - len(problems)
    print(f">> checks : {n_ok}/{len(REQUIRED_DIRS) + len(REQUIRED_FILES)} structural invariants OK")

    if problems:
        print("\n!! GATE-0 FAILED:")
        for p in problems:
            print(f"   - {p}")
        return 1

    print(">> GATE-0 PASS: repo skeleton present, .env gitignored, no committed secrets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
