# Tech Check 1 — Practice Notebook

A practice Jupyter notebook mirroring the Tech Check 1 exam format, so the
same code patterns can be rehearsed on different data.

## What it does

1. **File source (Part A)** — loads `practice_products_2020-2025.csv`
   (Product / 2020–2025, revenue in $ millions), prints `info()` and
   `describe()`, and draws a bar chart of the top 5 products by revenue
   in 2025.
2. **Web source (Part B)** — fetches 200 todo items from the
   [JSONPlaceholder API](https://jsonplaceholder.typicode.com/todos),
   loads the JSON into a DataFrame, and charts completed vs pending
   counts with `value_counts()`.

## Run

```bash
pip install pandas matplotlib requests jupyter
jupyter notebook tc1_practice.ipynb
```

Practice/exam-prep project. Sample data only.
