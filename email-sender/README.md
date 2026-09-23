# email-sender

Send personalized bulk emails from a CSV contact list and a text template.

![demo](demo.gif)

## Features

- `{name}`-style placeholders filled per contact (`contacts.csv` → `template.txt`)
- **Dry-run by default** — previews every email without sending anything
- Real sending via SMTP (works with Gmail using an [app password](https://support.google.com/accounts/answer/185833))

## Usage

```bash
# 1. Preview (safe, sends nothing)
python sender.py --dry-run

# 2. Configure real sending
cp config.example.json config.json
# edit config.json with your SMTP credentials

# 3. Send
python sender.py --send --config config.json
```

## Files

| File | Purpose |
|---|---|
| `contacts.csv` | `name,email` (+ any extra columns usable as placeholders) |
| `template.txt` | Email body with `{placeholders}` |
| `config.example.json` | Template for SMTP settings + subject line |

No third-party dependencies — Python standard library only.
