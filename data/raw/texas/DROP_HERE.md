# Texas registry — official SOS CSV export (manual download)

GATE-2 decision was "official export first." Texas SOS **does** publish an official CSV
export, but it returns **HTTP 403 to automated tools** (server-side WAF blocks both our
fetcher and browser-like fetches). So grab it in your real browser — this is still an
official download, **not** scraping.

Try in order:
1. **Direct:** open `https://www.sos.state.tx.us/statdoc/forms/registered-data-brokers.csv`
   in your browser — it should download.
2. If that 403s too, open `https://www.sos.state.tx.us/statdoc/data-brokers.shtml` and use
   the registry/export link, or the Appian portal
   `https://texas-sos.appianportals.com/data-broker-registry` and use its export-to-CSV.
3. Save into **this folder** as `texas_data_brokers_2026-06-04.csv`.
   **Note the "generated on" date** if the file shows one — if it's 2024 it may undercount
   the current registry, and we'll flag that.

Then I log it (`SRC-005`):
```
py src/acquire/ingest_local.py --source texas --src-id SRC-005 \
   --name "Texas SOS Data Broker registry (official CSV export)" \
   --url "https://www.sos.state.tx.us/statdoc/forms/registered-data-brokers.csv" \
   --tier A --access download \
   --notes "official SOS export; 403 to automated tools so downloaded manually; verify generation date" \
   data/raw/texas/<your-file>
```
