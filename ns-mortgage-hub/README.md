# NS Mortgage Hub — Nova Scotia Home Buying & Mortgage Intelligence Platform

A self-contained, single-file HTML web app for Nova Scotia homebuyers.
No build step, no dependencies — open `index.html` in a browser.

## Features

- **Mortgage & stress-test calculator** — OSFI B-20 compliant: qualifies at
  contract rate + 2.0% or 5.25% (whichever is higher), with 39% GDS / 44% TDS limits
- **Canadian semi-annual compounding** mortgage math (`(1 + i/2)^(2/12) - 1`)
- **Nova Scotia deed transfer tax (DTT)** by municipality (HRM 1.5%, Colchester 1.0%)
- **Property listings** with budget filter tied to the calculated max purchase price
- **Document checklist** for mortgage underwriting & closing (9 items, progress tracker)
- **Professional team directory** (broker / realtor / lawyer) with consultation modal
- **Printable buyer's approval summary** (Print / Save as PDF)

## Run

```bash
open index.html        # macOS
xdg-open index.html    # Linux
```

Personal demo project. Sample data only — rates and listings are illustrative.
