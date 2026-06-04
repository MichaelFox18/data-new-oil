# Phase 4 — validation & data-quality notes

Per CLAUDE.md §9 (Phase 4). Machine profiles regenerate to `results/profiles/*.json`
(+ `SUMMARY.md`) via `src/validate/profile.py`; this file is the durable, hand-maintained
note: schema, known issues, cleaning decisions, and the read-correctness sanity checks.

All figures here are **MEASURED** this session by `src/validate/profile.py` reading
`data/raw/` (raw retrieved 2026-06-04). Raw is untouched (§2.6).

---

## Broker registries — schema is heterogeneous (decides what Q1 can compute)

| State | Source | Shape | Enc / delim | Full-dup rows | Collection-category fields? |
|---|---|---|---|---|---|
| CA | SRC-002 | 581 × 77 | utf-8 / `,` | 0 | **Yes — rich** |
| VT | SRC-003 | 714 × 39 | xlsx | **26** | No (identity + status + address) |
| OR | SRC-004 | 352 × 10 | cp1252 / `\|` | 0 | No (name + address + status) |
| TX | SRC-005 | pending manual download | — | — | reportedly has data-categories |

**Implication for Q1:** the cross-state work splits cleanly into two analyses —
- **Count + dedup** across all states (key = normalized broker name), and
- **Sensitive-category shares** (geolocation / minors / GenAI-sharing / biometric) which
  are a **California-only** computation; OR and VT do not carry those fields. TX may add a
  second category source once downloaded. State this scope honestly in the finding.

### California (SRC-002) — the category goldmine
- 77 columns. The four Q1-critical category flags are **0.0% blank**, values `Yes`/`No`:
  `precise geolocation`, `collects personal information of minors`, `shared/sold data to a
  GenAI developer in the past year`, `biometric data` (plus citizenship, reproductive
  health, union, sexual orientation, gender identity, and full CCPA request-volume metrics).
- Clean: 0 duplicate rows. Self-registration only (non-registrants absent) — a coverage
  floor, not a census of all brokers.

### Vermont (SRC-003) — dedup needs care
- Columns: `Name`, `Idregistration`, `DataBrokerStatus`, physical/mailing address fields.
- **26 full-duplicate rows** — must resolve in cleaning (multi-year re-registration vs.
  true dupes — investigate `Idregistration` + `DataBrokerStatus` before dropping).
- `DataBrokerStatus` likely includes inactive/terminated entries → filter to active for a
  current count; keep all for a historical/registration-trend view (Q2).

### Oregon (SRC-004) — encoding + parsing gotchas (now handled)
- **cp1252** (not UTF-8) and **pipe-delimited** — the auto-sniffer mis-parsed it into
  garbage columns; `profile.py` now picks the delimiter from the header and falls back
  utf-8 → cp1252 → latin-1. Cleaning must use the same.
- 9 real columns + 1 trailing-pipe empty column (`Unnamed: 9`, drop it).
- `addr_line_4` mashes city/state/zip into one field ("San Francisco CA  94104") → parse
  in cleaning. No category fields.

## Epoch model datasets (SRC-001) — Q3/Q4 feasibility
- `notable_ai_models.csv`: 1026 × 47. `Training dataset size (total)` is **35.5% blank**
  (~662 models populated) — enough to fit a growth trend and the training side of the
  crossover, with the missingness stated. `Publication date` 0.4% blank. `Training compute
  (FLOP)` 48.7% blank. `Frontier model` flag set on ~12% (88% blank).
- `frontier_ai_models.csv`: 137 × 61. `large_scale_ai_models.csv`: 515 × 34. No dup rows.

## Read-correctness sanity checks (GATE 4)
- Epoch notable **1026 rows ≈ Epoch's stated "900+ notable models"** → reader is correct. ✓
- OR/CA/VT parsed columns match each registry's expected schema (names, addresses,
  status; CA category form) → no silent truncation. ✓
- Re-running `profile.py` is deterministic and overwrites `results/profiles/` from raw. ✓

## Open cleaning decisions (carried into Phase 5)
1. Cross-state dedup key: normalized `name` (casefold, strip punctuation/suffixes like
   Inc/LLC). Validate overlap counts; expect some same-entity-different-spelling misses.
2. VT: resolve the 26 dup rows; decide active-only vs. all for each question.
3. OR: drop trailing empty col; split `addr_line_4` into city/state/zip.
4. Epoch: parse `Training dataset size (total)` units (notes column) before trending.
