# excel-cleaner

Turn a messy sales spreadsheet into clean, analysis-ready data.

![demo](demo.gif)

## What it fixes

- Fully empty rows
- Leading/trailing whitespace (`"  widget a "` → `"Widget A"`)
- Mixed date formats (`2026/01/05`, `Jan 6, 2026`, `2026-01-07` → `2026-01-07`)
- Price strings with currency symbols (`"$1,299.99"` → `1299.99`)
- Duplicate rows
- Missing regions → `"Unknown"`

## Usage

```bash
pip install -r requirements.txt
python cleaner.py --input data/messy_sales.csv --output data/cleaned_sales.csv
```

Works with both CSV and Excel (`.xlsx`) input files. Prints a short report:
rows before/after, duplicates removed, unparseable dates, and total revenue.

## Sample output

```
=== excel-cleaner report ===
Rows before : 15
Rows after  : 12
Duplicates removed      : 2
Unparseable dates      : 0
Missing regions filled : 2
Saved cleaned file -> data/cleaned_sales.csv
Total revenue in file  : $5,922.74
```
