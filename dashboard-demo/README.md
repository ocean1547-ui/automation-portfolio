# dashboard-demo

Turn a raw sales spreadsheet into a polished, self-contained HTML sales
dashboard — no web server or internet connection needed.

![demo](demo.gif)

## What it does

1. **Cleans** the input CSV: strips whitespace, title-cases product names,
   parses mixed date formats (`2026-01-05`, `2026/01/05`, `Jun 01, 2026`),
   strips currency symbols from prices, removes duplicates, and fills
   missing regions with `"Unknown"`.
2. **Computes KPIs**: total revenue, order count, average order value,
   and top category.
3. **Renders 5 charts** (matplotlib) and embeds them as base64 PNGs in a
   single `index.html`:
   - Revenue by month (bar)
   - Revenue share by category (pie)
   - Top 5 products by revenue (horizontal bar)
   - Revenue by region (bar)
   - Daily revenue, 7-day average (line)
4. **Adds a Top-10 orders table** for quick inspection.

## Usage

```bash
pip install -r requirements.txt
python dashboard.py --input data/sample_sales.csv --output dashboard/index.html
```

Then open `dashboard/index.html` in any browser. The file is fully
self-contained — it works offline.

## Sample output

```
=== dashboard report ===
Rows before : 203
Rows after  : 200
Duplicates removed      : 3
Unparseable dates      : 0
Charts rendered         : 5
Total revenue           : $48,171.12
Saved dashboard -> dashboard/index.html
```

The sample data generator (`make_sample_data.py`) creates 203 rows of
realistic orders spanning Jan–Jun 2026, with a few duplicates and messy
formats so the cleaning step is visible.
