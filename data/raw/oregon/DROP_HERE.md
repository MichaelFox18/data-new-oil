# Oregon registry — manual export goes here

GATE-2 decision: **manual export only — no scraping** (Oregon's robots.txt is
`Disallow: /` and explicitly blocks the license-search path).

How:
1. Open the verification search `https://ordcbs.mylicense.com/Verification/Search.aspx`
   (or the DFR license search). Set Profession = **DFT-Data Broker**, License Type =
   **Data Broker**, leave other fields blank, search.
2. Export / save the full results into **this folder** as
   `oregon_data_brokers_<YYYY-MM-DD>.<csv|xlsx>` (copy to CSV by hand if no export).

Then I log it (hash + provenance, `SRC-004`) with:
```
py src/acquire/ingest_local.py --source oregon --src-id SRC-004 \
   --name "Oregon DCBS/DFR Data Broker registry (manual export)" \
   --url "https://ordcbs.mylicense.com/Verification/Search.aspx" --tier A --access manual \
   --notes "manual export per GATE-2; robots.txt disallows scraping" \
   data/raw/oregon/<your-file>
```

If a clean export isn't feasible, we mark Oregon `NEEDS-DATA` and report the other states.
