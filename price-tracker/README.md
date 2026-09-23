# price-tracker

Watch a product page and get alerted when the price drops below your target.

![demo](demo.gif)

## How it works

1. Fetches the page (any `http(s)` URL, or a local `file://` URL for demos/tests)
2. Extracts the price with a simple CSS selector (`.price`, `#price`, or a tag name)
3. Appends the check to `price_history.json`
4. Compares with the previous check — prints an alert on a price drop,
   and a special alert when your target price is hit

## Usage

```bash
pip install -r requirements.txt
# edit config.json: set "url", "selector", and "target_price"
python tracker.py --config config.json
```

Run it on a schedule (cron / Task Scheduler) to monitor continuously.

## Sample output

```
Current price: $99.99

 PRICE DROP! $129.99 -> $99.99 (-$30.00)
 TARGET HIT! Price is at/below your target of $110.00. Buy now!
```

The `demo/` folder contains two sample product pages so you can see
the drop detection without hitting a real website.
