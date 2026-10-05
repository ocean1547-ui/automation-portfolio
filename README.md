# Automation Portfolio

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ocean1547-ui/automation-portfolio)

Nine small, real-world automation projects. The six Python CLI tools clean,
monitor, send, sort, scrape, and rename — each one runs from the command
line, includes sample data, and has an animated demo. Plus two
self-contained HTML apps (no build step, no server) and one Jupyter
notebook on pandas data processing.

| Project | What it does |
|---|---|
| [excel-cleaner](./excel-cleaner/) | Cleans messy sales spreadsheets: dedupes, fixes dates/prices/casing, prints a report |
| [price-tracker](./price-tracker/) | Monitors a product page and alerts on price drops / target hits |
| [email-sender](./email-sender/) | Sends personalized bulk emails from CSV + template (dry-run by default) |
| [file-organizer](./file-organizer/) | Sorts a messy folder into subfolders by file type |
| [web-scraper](./web-scraper/) | Extracts structured data from any page into CSV via JSON config |
| [bulk-renamer](./bulk-renamer/) | Renames files in bulk with a clean date + sequence pattern |
| [dashboard-demo](./dashboard-demo/) | Builds a self-contained HTML sales dashboard (5 charts, KPI cards) from raw CSV |
| [ns-mortgage-hub](./ns-mortgage-hub/) | Single-file Nova Scotia home-buying app: B-20 stress-test mortgage calculator, DTT, listings, closing checklist |
| [tech-check-1-data-processing](./tech-check-1-data-processing/) | Jupyter notebook: pandas data processing from API + CSV sources, matplotlib visualization |
| [moneylog](./moneylog/) | Korean expense tracker web app (React+TS): receipt OCR, calendar view, monthly reports, budgets — KRW/CAD display |
| [household](./household/) | Personal finance dashboard demo (English, sample data): monthly income/expenses, per-card tracking, installment plans, receipts — single HTML reading data.json |
| [agent-skills](./agent-skills/) | Agent Skills demo (Korean): what SKILL.md packs are, google-gemini/gemini-skills library picks, my own shorts-pipeline skill with full SKILL.md |
| [tech-check-1-practice](./tech-check-1-practice/) | Practice notebook mirroring the Tech Check 1 exam format (CSV + API sources) |

## Live demos

The two HTML apps run right in the browser — no install needed:

- [NS Mortgage Hub](https://ocean1547-ui.github.io/automation-portfolio/ns-mortgage-hub/) — B-20 stress-test calculator, NS deed transfer tax, listings, closing checklist
- [Sales Dashboard demo](https://ocean1547-ui.github.io/automation-portfolio/dashboard-demo/dashboard/) — 5 charts + KPI cards generated from raw CSV
- [MoneyLog](https://ocean1547-ui.github.io/automation-portfolio/moneylog/) — smart household expense tracker: receipt OCR, calendar, reports, budgets (KRW/CAD)
- [Household Ledger](https://ocean1547-ui.github.io/automation-portfolio/household/) — personal finance dashboard demo (English, sample data): income/expenses, cards, installments, receipts

## Quick start

```bash
# excel-cleaner
cd excel-cleaner && pip install -r requirements.txt
python cleaner.py --input data/messy_sales.csv --output data/cleaned_sales.csv

# price-tracker
cd ../price-tracker && pip install -r requirements.txt
python tracker.py --config config.json

# email-sender (standard library only)
cd ../email-sender
python sender.py --dry-run

# file-organizer (dry-run first: moves nothing)
cd ../file-organizer
python organizer.py --folder demo/inbox --dry-run

# web-scraper
cd ../web-scraper && pip install -r requirements.txt
python scraper.py --config config.json

# bulk-renamer (dry-run first: changes nothing)
cd ../bulk-renamer
python renamer.py --folder demo/photos --prefix IMG --dry-run

# dashboard-demo -> generates a self-contained dashboard/index.html
cd ../dashboard-demo && pip install -r requirements.txt
python dashboard.py --input data/sample_sales.csv --output dashboard/index.html
```

The two HTML apps need no install — just open them in a browser:

```bash
# ns-mortgage-hub — Nova Scotia mortgage & home-buying app
open ns-mortgage-hub/index.html        # macOS
xdg-open ns-mortgage-hub/index.html    # Linux

# dashboard-demo — open the generated dashboard instead
open dashboard-demo/dashboard/index.html
```

The notebook:

```bash
# tech-check-1-data-processing
cd tech-check-1-data-processing
pip install pandas matplotlib requests jupyter
jupyter notebook Tech_check__1.ipynb
```

Built with Python 3.12, pandas, and requests. Demos generated from real runs
(see [tools/](./tools/) for the demo GIF scripts).

## License

MIT — see [LICENSE](./LICENSE).
