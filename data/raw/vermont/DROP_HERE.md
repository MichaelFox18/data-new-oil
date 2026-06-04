# Vermont registry — manual bulk download goes here

GATE-2 decision: **you perform the official Bulk Database Download** (the portal 403s
automated requests; it is not scraped).

How:
1. Go to `https://bizfilings.vermont.gov` → Main Menu → "VT SEC OF STATE ONLINE
   SERVICES" → **Bulk Database Download**.
2. Select Business/Registration Type = **Data Broker** → Download.
3. Save the file into **this folder** as `vermont_data_brokers_<YYYY-MM-DD>.<csv|xlsx>`.

Then I log it (hash + provenance, `SRC-003`) with:
```
py src/acquire/ingest_local.py --source vermont --src-id SRC-003 \
   --name "Vermont SOS Data Broker registry (bulk download)" \
   --url "https://bizfilings.vermont.gov" --tier A --access portal \
   --notes "manual bulk download per GATE-2; portal blocks automated access" \
   data/raw/vermont/<your-file>
```
