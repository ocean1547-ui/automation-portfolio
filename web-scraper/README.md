# web-scraper

Extract structured data from a web page into a CSV file — no code changes
needed, just edit the JSON config.

![demo](demo.gif)

## How it works

`config.json` defines what to scrape with simple CSS class selectors:

```json
{
  "url": "https://example.com/products",
  "item": "product",
  "fields": {"name": "name", "price": "price"},
  "output": "products.csv"
}
```

## Usage

```bash
pip install -r requirements.txt
python scraper.py --config config.json
```

## Sample output

```
Scraped 5 items -> products.csv
  name=Wireless Mouse | price=$24.99
  name=USB-C Hub | price=$39.99
  ...
```

The `demo/` folder contains a sample shop page so you can try it
without hitting a real website.
