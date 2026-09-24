#!/usr/bin/env python3
"""Turn a raw sales CSV into a self-contained HTML sales dashboard.

Cleans the data (whitespace, mixed date/price formats, duplicates, missing
regions), computes KPIs, and renders 5 charts into a single offline-ready
dashboard/index.html (charts are embedded as base64 PNGs).

Usage:
    pip install -r requirements.txt
    python dashboard.py --input data/sample_sales.csv --output dashboard/index.html
"""
import argparse
import base64
import io
import re
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATE_FMTS = ("%Y-%m-%d", "%Y/%m/%d", "%b %d, %Y")


def parse_date(raw):
    raw = str(raw).strip()
    for fmt in DATE_FMTS:
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return pd.NaT


def parse_price(raw):
    return float(re.sub(r"[$,]", "", str(raw).strip()))


def clean(df):
    report = {"rows_before": len(df)}
    df = df.drop_duplicates().copy()
    report["duplicates_removed"] = report["rows_before"] - len(df)
    for col in ("product", "category", "region"):
        df[col] = df[col].astype(str).str.strip()
    df["product"] = df["product"].str.title()
    df["date"] = df["date"].apply(parse_date)
    report["unparseable_dates"] = int(df["date"].isna().sum())
    df = df.dropna(subset=["date"])
    df["unit_price"] = df["unit_price"].apply(parse_price)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1).astype(int)
    df.loc[df["region"].isin(("", "nan", "None")), "region"] = "Unknown"
    df["revenue"] = df["unit_price"] * df["quantity"]
    df["month"] = df["date"].apply(lambda d: d.strftime("%Y-%m"))
    report["rows_after"] = len(df)
    return df, report


def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("ascii")


plt.rcParams.update({"font.size": 9, "figure.facecolor": "#ffffff"})


def chart_monthly(df):
    monthly = df.groupby("month")["revenue"].sum().sort_index()
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.bar(monthly.index, monthly.values, color="#2563eb")
    ax.set_title("Revenue by Month")
    ax.set_ylabel("USD")
    ax.tick_params(axis="x", rotation=30)
    for x, v in zip(monthly.index, monthly.values):
        ax.text(x, v, f"${v:,.0f}", ha="center", va="bottom", fontsize=8)
    return fig_to_base64(fig)


def chart_category(df):
    cat = df.groupby("category")["revenue"].sum()
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.pie(cat.values, labels=cat.index, autopct="%1.1f%%", startangle=90,
           colors=["#2563eb", "#16a34a", "#f59e0b", "#ef4444"])
    ax.set_title("Revenue Share by Category")
    return fig_to_base64(fig)


def chart_top_products(df):
    top = df.groupby("product")["revenue"].sum().nlargest(5).sort_values()
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.barh(top.index, top.values, color="#16a34a")
    ax.set_title("Top 5 Products by Revenue")
    for v, label in zip(top.values, top.index):
        ax.text(v, label, f"  ${v:,.0f}", va="center", fontsize=8)
    return fig_to_base64(fig)


def chart_region(df):
    reg = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.bar(reg.index, reg.values, color="#7c3aed")
    ax.set_title("Revenue by Region")
    ax.set_ylabel("USD")
    ax.tick_params(axis="x", rotation=30)
    return fig_to_base64(fig)


def chart_daily_trend(df):
    daily = df.groupby("date")["revenue"].sum().sort_index()
    rolling = daily.rolling(7, min_periods=1).mean()
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.plot(daily.index, rolling.values, color="#ef4444", linewidth=2)
    ax.set_title("Daily Revenue (7-day average)")
    ax.set_ylabel("USD")
    ax.tick_params(axis="x", rotation=30)
    return fig_to_base64(fig)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sales Dashboard</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif;
          background: #f1f5f9; color: #0f172a; margin: 0; padding: 24px; }}
  h1 {{ margin: 0 0 4px; }} .sub {{ color: #64748b; margin-bottom: 20px; }}
  .kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
           margin-bottom: 20px; }}
  .kpi {{ background: #fff; border-radius: 12px; padding: 16px;
          box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  .kpi .label {{ color: #64748b; font-size: 13px; }}
  .kpi .value {{ font-size: 26px; font-weight: 700; margin-top: 4px; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
  .card {{ background: #fff; border-radius: 12px; padding: 12px;
           box-shadow: 0 1px 3px rgba(0,0,0,.08); text-align: center; }}
  .card img {{ max-width: 100%; height: auto; }}
  table {{ width: 100%; border-collapse: collapse; background: #fff;
           border-radius: 12px; overflow: hidden; margin-top: 20px;
           box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  th, td {{ padding: 10px 14px; text-align: left; font-size: 14px; }}
  th {{ background: #2563eb; color: #fff; }}
  tr:nth-child(even) td {{ background: #f8fafc; }}
  .footer {{ color: #94a3b8; font-size: 12px; margin-top: 16px; }}
</style>
</head>
<body>
<h1>Sales Dashboard</h1>
<div class="sub">{orders} orders · {date_range} · generated from {input_name}</div>
<div class="kpis">
  <div class="kpi"><div class="label">Total Revenue</div><div class="value">${revenue:,.2f}</div></div>
  <div class="kpi"><div class="label">Orders</div><div class="value">{orders}</div></div>
  <div class="kpi"><div class="label">Avg. Order Value</div><div class="value">${aov:,.2f}</div></div>
  <div class="kpi"><div class="label">Top Category</div><div class="value">{top_cat}</div></div>
</div>
<div class="grid">
  <div class="card"><img src="data:image/png;base64,{ch1}" alt="Monthly revenue"></div>
  <div class="card"><img src="data:image/png;base64,{ch2}" alt="Revenue by category"></div>
  <div class="card"><img src="data:image/png;base64,{ch3}" alt="Top products"></div>
  <div class="card"><img src="data:image/png;base64,{ch4}" alt="Revenue by region"></div>
</div>
<div class="card" style="margin-top:12px"><img src="data:image/png;base64,{ch5}" alt="Daily trend"></div>
<h2>Top 10 Orders</h2>
<table>
<tr><th>Order</th><th>Date</th><th>Product</th><th>Qty</th><th>Revenue</th><th>Region</th></tr>
{top_rows}
</table>
<div class="footer">Built with dashboard.py — a personal demo project.</div>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/sample_sales.csv")
    ap.add_argument("--output", default="dashboard/index.html")
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    df, report = clean(df)

    total = df["revenue"].sum()
    top_cat = df.groupby("category")["revenue"].sum().idxmax()
    top10 = df.nlargest(10, "revenue")
    top_rows = "\n".join(
        "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>${:,.2f}</td><td>{}</td></tr>".format(
            r.order_id, r.date, r.product, r.quantity, r.revenue, r.region)
        for r in top10.itertuples())

    html = HTML_TEMPLATE.format(
        orders=len(df),
        date_range=f"{df['date'].min()} to {df['date'].max()}",
        input_name=args.input,
        revenue=total, aov=total / len(df), top_cat=top_cat,
        ch1=chart_monthly(df), ch2=chart_category(df),
        ch3=chart_top_products(df), ch4=chart_region(df),
        ch5=chart_daily_trend(df), top_rows=top_rows)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print("=== dashboard report ===")
    print(f"Rows before : {report['rows_before']}")
    print(f"Rows after  : {report['rows_after']}")
    print(f"Duplicates removed      : {report['duplicates_removed']}")
    print(f"Unparseable dates      : {report['unparseable_dates']}")
    print(f"Charts rendered         : 5")
    print(f"Total revenue           : ${total:,.2f}")
    print(f"Saved dashboard -> {args.output}")


if __name__ == "__main__":
    main()
