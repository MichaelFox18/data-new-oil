# FACTCHECK — every on-screen number, traced

Final Phase 8 deliverable (CLAUDE.md §14). Every number intended for the video is
listed here with its claim type, source/script, tier, and the exact command to
reproduce it. Built only after findings reach `VERIFIED` (GATE 6) and approved at
GATE 8.

## Line format

```
- CLAIM: "<one line>" | TYPE: MEASURED | VALUE: <n> | SOURCE: SRC-007 (Tier A) |
  REPRODUCE: `py src/analyze/broker_census.py` | CONFIDENCE: High | CHAPTER: 3
```

`TYPE` is one of `MEASURED` | `REPORTED` | `MODELED` (CLAUDE.md §3).

---

<!-- No verified, video-bound numbers yet. -->
