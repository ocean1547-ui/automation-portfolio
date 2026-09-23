#!/usr/bin/env python3
"""
excel-cleaner: turn a messy sales spreadsheet into clean, analysis-ready data.

What it fixes:
  - fully empty rows
  - leading/trailing whitespace in text fields
  - inconsistent product-name casing ("  widget a " -> "Widget A")
  - mixed date formats ("2026/01/05", "Jan 6, 2026", "2026-01-07") -> YYYY-MM-DD
  - price strings with currency symbols ("$1,299.99") -> float
  - duplicate rows
  - missing regions -> "Unknown"

Usage:
    python cleaner.py --input data/messy_sales.csv --output data/cleaned_sales.csv
"""

import argparse
import sys

import pandas as pd


def clean(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    report: dict = {"rows_before": len(df)}

    # 1. Drop fully empty rows
    df = df.dropna(how="all").copy()

    # 1b. order_id back to clean integers (empty rows turn it into float)
    if "order_id" in df.columns:
        df["order_id"] = pd.to_numeric(df["order_id"], errors="coerce").astype("Int64")

    # 2. Strip whitespace from every text column
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip().replace({"nan": None, "None": None})

    # 3. Normalize product names
    if "product" in df.columns:
        df["product"] = df["product"].str.title()

    # 4. Standardize dates -> YYYY-MM-DD (handles mixed formats)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], format="mixed", errors="coerce")
        bad_dates = int(df["date"].isna().sum())
        report["unparseable_dates_dropped"] = bad_dates
        df = df.dropna(subset=["date"])
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # 5. Clean price: "$1,299.99" -> 1299.99
    if "price" in df.columns:
        df["price"] = (
            df["price"].astype(str).str.replace(r"[$,\s]", "", regex=True).astype(float)
        )

    # 6. Quantity must be a positive integer
    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        df = df.dropna(subset=["quantity"])
        df["quantity"] = df["quantity"].astype(int)

    # 7. Drop exact duplicates
    dupes = int(df.duplicated().sum())
    report["duplicates_removed"] = dupes
    df = df.drop_duplicates()

    # 8. Fill missing region and normalize casing
    if "region" in df.columns:
        missing = int(df["region"].isna().sum())
        report["regions_filled"] = missing
        df["region"] = df["region"].fillna("Unknown").str.title()

    # 9. Sort by date and reset the index
    if "date" in df.columns:
        df = df.sort_values("date").reset_index(drop=True)

    report["rows_after"] = len(df)
    return df, report


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean a messy sales CSV/Excel file.")
    parser.add_argument("--input", required=True, help="Path to the messy input file")
    parser.add_argument("--output", required=True, help="Path for the cleaned output file")
    args = parser.parse_args()

    try:
        if args.input.endswith((".xlsx", ".xls")):
            df = pd.read_excel(args.input)
        else:
            df = pd.read_csv(args.input)
    except FileNotFoundError:
        sys.exit(f"Error: input file not found: {args.input}")

    cleaned, report = clean(df)
    cleaned.to_csv(args.output, index=False)

    print("=== excel-cleaner report ===")
    print(f"Rows before : {report['rows_before']}")
    print(f"Rows after  : {report['rows_after']}")
    print(f"Duplicates removed      : {report.get('duplicates_removed', 0)}")
    print(f"Unparseable dates      : {report.get('unparseable_dates_dropped', 0)}")
    print(f"Missing regions filled : {report.get('regions_filled', 0)}")
    print(f"Saved cleaned file -> {args.output}")
    print(f"Total revenue in file  : ${(cleaned['price'] * cleaned['quantity']).sum():,.2f}")


if __name__ == "__main__":
    main()
