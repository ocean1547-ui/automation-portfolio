# Tech Check 1 — Practice Notebook

A practice Jupyter notebook mirroring the Tech Check 1 exam format, so the
same code patterns can be rehearsed on different data.

## What it does

1. **File source (Part A)** — loads `practice_population_2020-2025.csv`
   (Country / 2020–2025, population in millions), prints `info()` and
   `describe()`, and draws a bar chart of the top 5 countries in 2025.
2. **Web source (Part B)** — fetches Colorado breweries from the
   [Open Brewery DB API](https://www.openbrewerydb.org/documentation),
   loads the JSON into a DataFrame, and charts `brewery_type` counts
   with `value_counts()`.

## Run

```bash
pip install pandas matplotlib requests jupyter
jupyter notebook tc1_practice.ipynb
```

Practice/exam-prep project. Sample data only.
