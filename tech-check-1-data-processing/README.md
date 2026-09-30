# Tech Check #1 — Data Processing and Visualization

A Jupyter notebook demonstrating data import from multiple sources, manipulation
with pandas, and visualization with matplotlib.

## What it does

1. **API source** — fetches cat facts from `https://catfact.ninja/facts`,
   parses the JSON, and loads the results into a pandas DataFrame.
2. **File source** — loads `student_scores.csv` (name / age / score) from disk.
3. **Basic calculations** — computes max, min, and mean of the fact lengths
   from the API data.
4. **Visualization** — renders a bar chart of cat-fact lengths with matplotlib.

## Run

```bash
pip install pandas matplotlib requests jupyter
jupyter notebook Tech_check__1.ipynb
```

Coursework-style demo project. Sample data only.
