#!/usr/bin/env python3
"""Generate realistic sample sales data for the dashboard demo.

Writes data/sample_sales.csv with ~200 orders spanning 2026-01 to 2026-06,
including a few duplicates, messy dates/prices, and missing regions so the
dashboard script shows its cleaning step too.
"""
import csv
import random
from datetime import date, timedelta

random.seed(42)

PRODUCTS = {
    "Electronics": [("Wireless Mouse", 29.99), ("USB-C Hub", 49.99),
                    ("Mechanical Keyboard", 89.99), ("Webcam HD", 59.99),
                    ("Bluetooth Speaker", 79.99)],
    "Furniture": [("Standing Desk", 299.99), ("Ergonomic Chair", 199.99),
                  ("Bookshelf", 129.99), ("Monitor Arm", 69.99)],
    "Office Supplies": [("Notebook Pack", 12.99), ("Pen Set", 8.99),
                        ("Desk Organizer", 24.99), ("Sticky Notes", 5.99)],
    "Kitchen": [("Coffee Maker", 89.99), ("Electric Kettle", 39.99),
                ("Knife Set", 59.99), ("Blender", 69.99)],
}
REGIONS = ["Halifax", "Toronto", "Vancouver", "Montreal", "Calgary"]
DATE_FMTS = ["%Y-%m-%d", "%Y/%m/%d", "%b %d, %Y"]  # mixed formats on purpose

start = date(2026, 1, 1)
rows = []
order_id = 1000
for i in range(200):
    d = start + timedelta(days=random.randint(0, 170))
    category = random.choice(list(PRODUCTS))
    product, price = random.choice(PRODUCTS[category])
    qty = random.randint(1, 5)
    region = random.choice(REGIONS + [None])  # occasional missing region
    # messy variants
    messy_product = product if i % 3 else f"  {product.lower()} "
    messy_date = d.strftime(DATE_FMTS[i % 3])
    messy_price = f"${price:,.2f}" if i % 2 else f"{price}"
    rows.append([f"ORD-{order_id}", messy_date, messy_product,
                 category, qty, messy_price, region or ""])
    order_id += 1

# inject a few exact duplicates
rows += [rows[10], rows[55], rows[120]]

with open("data/sample_sales.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["order_id", "date", "product", "category",
                "quantity", "unit_price", "region"])
    w.writerows(rows)
print(f"wrote data/sample_sales.csv ({len(rows)} rows)")
