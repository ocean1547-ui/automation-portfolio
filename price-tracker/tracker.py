#!/usr/bin/env python3
"""
price-tracker: watch a product page and alert when the price drops.

How it works:
  1. Fetches the page (http(s) URL, or a local file:// URL for demos/tests).
  2. Extracts the price using a simple CSS selector (.price, #price, or a tag).
  3. Appends the check to price_history.json.
  4. Compares with the previous check and prints an alert on a price drop,
     plus a special alert when the price hits your target.

Usage:
    python tracker.py --config config.json
    python tracker.py --config config.json --url file:///path/to/product_v2.html
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser

import requests


class _SelectorParser(HTMLParser):
    """Grab the text of the first element matching a simple CSS selector."""

    def __init__(self, selector: str):
        super().__init__()
        self.selector = selector
        self._capture = False
        self._depth = 0
        self.text = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        match = (
            (self.selector.startswith(".") and attrs.get("class", "") == self.selector[1:])
            or (self.selector.startswith("#") and attrs.get("id") == self.selector[1:])
            or (self.selector == tag)
        )
        if match and not self.text:
            self._capture = True
        if self._capture:
            self._depth += 1

    def handle_endtag(self, tag):
        if self._capture:
            self._depth -= 1
            if self._depth <= 0:
                self._capture = False

    def handle_data(self, data):
        if self._capture:
            self.text += data


def fetch_html(url: str) -> str:
    if url.startswith("file://"):
        with open(url[len("file://"):], encoding="utf-8") as f:
            return f.read()
    resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    return resp.text


def extract_price(html: str, selector: str) -> float:
    parser = _SelectorParser(selector)
    parser.feed(html)
    text = parser.text.strip()
    m = re.search(r"[\d,]+\.\d{2}", text.replace(",", ""))
    if not m:
        raise ValueError(f"No price found with selector '{selector}' (got: {text!r})")
    return float(m.group().replace(",", ""))


def load_history(path: str) -> list:
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return []


def main() -> None:
    parser = argparse.ArgumentParser(description="Track a product price and alert on drops.")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--url", help="Override the URL in the config (handy for demos)")
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        cfg = json.load(f)

    url = args.url or cfg["url"]
    state_file = cfg.get("state_file", "price_history.json")
    target = cfg.get("target_price")

    try:
        html = fetch_html(url)
        price = extract_price(html, cfg.get("selector", ".price"))
    except Exception as exc:  # noqa: BLE001 - show a clean error for CLI use
        sys.exit(f"Error checking price: {exc}")

    history = load_history(state_file)
    previous = history[-1]["price"] if history else None
    history.append(
        {"timestamp": datetime.now(timezone.utc).isoformat(), "price": price, "url": url}
    )
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    print(f"Current price: ${price:,.2f}")
    if previous is None:
        print("Baseline recorded. Run again later to detect changes.")
    elif price < previous:
        print(f"\n PRICE DROP! ${previous:,.2f} -> ${price:,.2f} "
              f"(-${previous - price:,.2f})")
        if target is not None and price <= target:
            print(f" TARGET HIT! Price is at/below your target of ${target:,.2f}. Buy now!")
    elif price > previous:
        print(f"Price went UP from ${previous:,.2f} to ${price:,.2f}.")
    else:
        print(f"No change since last check (${previous:,.2f}).")


if __name__ == "__main__":
    main()
