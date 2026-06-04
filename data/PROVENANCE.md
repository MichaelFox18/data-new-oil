# PROVENANCE ledger (append-only)

One block per fetched source, filled in **at acquisition time, before any analysis
uses it** (CLAUDE.md §7). If a field can't be filled (e.g. no hash for a live API),
say so explicitly — never leave a blank that looks complete.

## Entry template

```
### SRC-000  <short name>
- name:           <full name>
- url:            <exact URL fetched>
- access_method:  download | api | scrape
- retrieved_at:   YYYY-MM-DD HH:MM UTC
- raw_path:       data/raw/<source>/<file>
- sha256:         <hash of the raw file>  (or: N/A — live API, see fetch log)
- rows / size:    <count> rows / <bytes>
- license/terms:  <note; for scraping, robots.txt + ToS status + human-approval ref>
- tier:           A | B | C
- caveats:        <known gaps, e.g. self-registration only; some brokers missing>
```

---

<!-- No sources fetched yet. First entries land in Phase 3, after GATE 2 sign-off. -->
