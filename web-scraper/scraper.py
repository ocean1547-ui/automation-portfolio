#!/usr/bin/env python3
"""
web-scraper: extract structured data from a web page into a CSV file.

Uses simple CSS class selectors defined in a JSON config:
  - "item": selector for each repeating block (e.g. ".product")
  - "fields": mapping of column name -> selector inside each block

Works with http(s) URLs and local file:// URLs (handy for demos/tests).

Usage:
    python scraper.py --config config.json
"""

import argparse
import csv
import json
import sys
from html.parser import HTMLParser

import requests


class _ItemParser(HTMLParser):
    """Collect text for each field inside every element matching item_class."""

    def __init__(self, item_class: str, fields: dict):
        super().__init__()
        self.item_class = item_class
        self.fields = fields  # {column: "classname"}
        self.items: list[dict] = []
        self._in_item = False
        self._depth = 0
        self._current: dict = {}
        self._capture_field = None
        self._capture_depth = 0

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class", "")
        if not self._in_item and cls == self.item_class:
            self._in_item = True
            self._depth = 1
            self._current = {}
            return
        if self._in_item:
            self._depth += 1
            for column, selector in self.fields.items():
                if cls == selector and self._capture_field is None:
                    self._capture_field = column
                    self._capture_depth = self._depth
                    self._current[column] = ""

    def handle_endtag(self, tag):
        if not self._in_item:
            return
        if self._capture_field and self._depth == self._capture_depth:
            self._capture_field = None
        self._depth -= 1
        if self._depth <= 0:
            self._in_item = False
            if self._current:
                self.items.append(self._current)

    def handle_data(self, data):
        if self._capture_field:
            self._current[self._capture_field] += data.strip()


def fetch_html(url: str) -> str:
    if url.startswith("file://"):
        with open(url[len("file://"):], encoding="utf-8") as f:
            return f.read()
    resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    return resp.text


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape a page into a CSV file.")
    parser.add_argument("--config", required=True, help="Path to config.json")
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        cfg = json.load(f)

    try:
        html = fetch_html(cfg["url"])
    except Exception as exc:  # noqa: BLE001 - clean CLI error
        sys.exit(f"Error fetching page: {exc}")

    parser_ = _ItemParser(cfg["item"], cfg["fields"])
    parser_.feed(html)
    items = parser_.items

    if not items:
        sys.exit("No items found - check the 'item' selector in config.json.")

    columns = list(cfg["fields"].keys())
    with open(cfg["output"], "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(items)

    print(f"Scraped {len(items)} items -> {cfg['output']}")
    for item in items[:5]:
        print("  " + " | ".join(f"{k}={v}" for k, v in item.items()))
    if len(items) > 5:
        print(f"  ... and {len(items) - 5} more")


if __name__ == "__main__":
    main()
