# bulk-renamer

Rename every file in a folder with a clean, consistent pattern:

```
dsc001.jpg      ->  IMG_20260923_001.jpg
vacation.png    ->  IMG_20260923_004.png
```

![demo](demo.gif)

## Usage

```bash
# Preview new names (safe, changes nothing)
python renamer.py --folder demo/photos --prefix IMG --dry-run

# Actually rename
python renamer.py --folder demo/photos --prefix IMG --execute
```

Options: `--prefix` for the name prefix, `--start` for the first number.
Standard library only — no installation needed.
