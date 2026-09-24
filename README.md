# Automation Portfolio

Three small, real-world Python automation projects. Each one runs from the
command line, includes sample data, and has an animated demo.

| Project | What it does |
|---|---|
| [excel-cleaner](excel-cleaner/) | Cleans messy sales spreadsheets: dedupes, fixes dates/prices/casing, prints a report |
| [price-tracker](price-tracker/) | Monitors a product page and alerts on price drops / target hits |
| [email-sender](email-sender/) | Sends personalized bulk emails from CSV + template (dry-run by default) |
| [file-organizer](file-organizer/) | Sorts a messy folder into subfolders by file type |
| [web-scraper](web-scraper/) | Extracts structured data from any page into CSV via JSON config |
| [bulk-renamer](bulk-renamer/) | Renames files in bulk with a clean date + sequence pattern |

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
```

Built with Python 3.12, pandas, and requests. Demos generated from real runs.
