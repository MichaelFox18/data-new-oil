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

### SRC-001  Epoch AI — model datasets
- name:           Epoch AI, Data on Notable AI Models (+ Frontier, Large-Scale subsets)
- url:            https://epoch.ai/data/ai-models  (per-file CSVs at epoch.ai/data/)
- access_method:  download
- retrieved_at:   2026-06-04 15:28 UTC
- raw_path:       data/raw/epoch/  (files below)
  - notable_ai_models.csv: rows=1026, sha256=338ebdc58e2fc1c1211b0584a0572a6c6fb6666a6869332876c2d48373596895
  - frontier_ai_models.csv: rows=137, sha256=b048276162ca6965b1281be661930af02c41c06be12f8d3c5e27c321d83c37d6
  - large_scale_ai_models.csv: rows=515, sha256=6f92b14a3613f16bc2bdbb8e02aebe266aa3d2cb42887c47fc0b0a0d44c2005b
- rows / size:    see per-file rows above
- license/terms:  CC-BY (free to use/redistribute with attribution to Epoch AI)
- tier:           A (originating research group's own published dataset)
- caveats:        training-dataset-size field coverage varies by model; verify exact
                  column names in Phase 4; Epoch updates these CSVs ~daily, so the
                  retrieved_at snapshot date matters for reproducibility.

### SRC-002  CPPA Data Broker Registry
- name:           California Privacy Protection Agency data broker registry
- url:            https://cppa.ca.gov/data_broker_registry/registry.csv
- access_method:  download
- retrieved_at:   2026-06-04 15:28 UTC
- raw_path:       data/raw/cppa/registry.csv
- sha256:         a58708e10006fa4897fcff1d563f2f99f9dac0dc4418ea68cfad90a825d17f1d
- rows / size:    581 rows / 319421 bytes
- license/terms:  public CA government registry; robots.txt allows the registry path (2026-06-04)
- tier:           A
- caveats:        self-registration only (non-registrants absent); collection-category
                  and recipient columns to be profiled in Phase 4; reflects the 2026
                  registration cycle.

### SRC-003  Vermont SOS Data Broker registry (bulk download)
- name:           Vermont SOS Data Broker registry (bulk download)
- url:            https://bizfilings.vermont.gov
- access_method:  portal
- retrieved_at:   2026-06-04 16:06 UTC
- raw_path:       data/raw/vermont/vermont_data_brokers_2026-06-04.xlsx
- sha256:         a5ad66420c2ef5c54f2cafced6cc3396eb61b71e694184c5e017803a7c0a429b
- rows / size:    714 rows / 258991 bytes
- license/terms:  public government registry; obtained manually (not scraped)
- tier:           A
- caveats:        manual bulk download per GATE-2; portal blocks automated access; xlsx; schema TBD in Phase 4

### SRC-004  Oregon DCBS/DFR Data Broker registry (manual export)
- name:           Oregon DCBS/DFR Data Broker registry (manual export)
- url:            https://ordcbs.mylicense.com/Verification/Search.aspx
- access_method:  manual
- retrieved_at:   2026-06-04 16:06 UTC
- raw_path:       data/raw/oregon/oregon_data_brokers_2026-06-04.csv
- sha256:         6593365f9ec6dd7987fb16a6024d4b4d94502e4e4b4e28177bd3f6747e69180b
- rows / size:    352 rows / 45306 bytes
- license/terms:  public government registry; obtained manually (not scraped)
- tier:           A
- caveats:        manual export per GATE-2; robots.txt disallows scraping; PIPE-delimited; name/address/status only, no sensitive-category fields

### SRC-005  Texas SOS Data Broker registry (official CSV export, manual download)
- name:           Texas SOS Data Broker registry (official CSV export, manual download)
- url:            https://www.sos.state.tx.us/statdoc/forms/registered-data-brokers.csv
- access_method:  download
- retrieved_at:   2026-06-04 16:23 UTC
- raw_path:       data/raw/texas/texas_data_brokers_2026-06-04.csv
- sha256:         ab108e52fd539bd82a56139eee586cb63df6ffe7bd1cbf906c158094237b1490
- rows / size:    400 rows / 438957 bytes
- license/terms:  public government registry; obtained manually (not scraped)
- tier:           A
- caveats:        official SOS export, downloaded manually (URL 403s to automated tools); 'Exported On: Jun 4 2026' = CURRENT; 2-row preamble (Record Name/Exported On) precedes the real header row (Registration Number, Full Legal Name, ...); ~398 data rows; includes 'Data of a Known Child' (minors Y/N) + free-text 'Categories of Data Processed and Transferred'; geolocation is inside free text, not a structured flag

### SRC-006  SEC EDGAR XBRL company facts
- name:           SEC EDGAR companyfacts (XBRL) for platform revenue/ARPU (Q6)
- url:            https://data.sec.gov/api/xbrl/companyfacts/CIK<cik>.json (+ company_tickers.json)
- access_method:  api
- retrieved_at:   2026-06-05 13:19 UTC
- raw_path:       data/raw/sec/  (files below)
  - META (Meta Platforms, Inc., CIK 0001326801): companyfacts_META.json sha256=ded9a9be1ed9c81cf94a4c1828a076438df6d43045a84f40ef392140ff638ccd
  - GOOGL (Alphabet Inc., CIK 0001652044): companyfacts_GOOGL.json sha256=f86ec6e788ad2e8fa5fb2832c0c4a508c3e109b60acb54d2344c5c24efcda5d3
  - SNAP (Snap Inc, CIK 0001564408): companyfacts_SNAP.json sha256=25f414946719805859e106ff1f39d234ef97c3302204e549556eab0fc3b69a3c
  - RDDT (Reddit, Inc., CIK 0001713445): companyfacts_RDDT.json sha256=3f7f0e5a99dd76493aea03778ea73d8f89cb674a79d2917617f69cbe2621fc05
  - PINS (PINTEREST, INC., CIK 0001506293): companyfacts_PINS.json sha256=77ce0a9ea6fc8fa90e49c6f707234bc9076a31f9bfa6be5a49c5bd3898ba087b
- sha256:         see per-file above; company_tickers.json sha256=9595b3e2ee7f36751ea2ed0b1d17746e3bd60dd4bffa7edb08c6de27fa33eed7
- rows / size:    JSON fact sets
- license/terms:  US government public filings; SEC fair-access UA sent (no key)
- tier:           A
- caveats:        revenue is in us-gaap XBRL; user counts (MAU/DAU/ARPU) are usually
                  company EXTENSION tags NOT returned by companyfacts -> may need filing text.
