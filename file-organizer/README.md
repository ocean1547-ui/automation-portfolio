# file-organizer

Tidy a messy folder by sorting files into subfolders by type — automatically.

![demo](demo.gif)

## How it works

- Images → `images/`, PDFs & docs → `documents/`, spreadsheets → `spreadsheets/`
- Archives → `archives/`, videos → `videos/`, everything else → `others/`
- Name collisions handled automatically (`report.pdf` → `report_1.pdf`)

## Usage

```bash
# Preview first (moves nothing)
python organizer.py --folder demo/inbox --dry-run

# Actually organize
python organizer.py --folder demo/inbox
```

Point `--folder` at your real Downloads folder to tidy it in one command.
Standard library only — no installation needed.
