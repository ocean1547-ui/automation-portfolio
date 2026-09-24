#!/usr/bin/env python3
"""
file-organizer: tidy a messy folder by sorting files into subfolders by type.

Images -> images/, PDFs & docs -> documents/, spreadsheets -> spreadsheets/,
archives -> archives/, videos -> videos/, everything else -> others/.

Name collisions are handled automatically (report.pdf -> report_1.pdf).

Usage:
    python organizer.py --folder demo/inbox --dry-run   # preview only
    python organizer.py --folder demo/inbox             # actually move files
"""

import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf"},
    "spreadsheets": {".csv", ".xls", ".xlsx", ".ods"},
    "archives": {".zip", ".tar", ".gz", ".rar", ".7z"},
    "videos": {".mp4", ".mov", ".avi", ".mkv"},
}


def category_for(suffix: str) -> str:
    for category, extensions in CATEGORIES.items():
        if suffix.lower() in extensions:
            return category
    return "others"


def unique_dest(folder: Path, name: str) -> Path:
    dest = folder / name
    stem, suffix = dest.stem, dest.suffix
    i = 1
    while dest.exists():
        dest = folder / f"{stem}_{i}{suffix}"
        i += 1
    return dest


def organize(folder: Path, dry_run: bool) -> dict:
    moved: dict = {}
    files = [p for p in folder.iterdir() if p.is_file()]
    for path in sorted(files):
        category = category_for(path.suffix)
        target_dir = folder / category
        dest = unique_dest(target_dir, path.name)
        if not dry_run:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(path), str(dest))
        moved.setdefault(category, []).append(
            f"{path.name} -> {category}/{dest.name}"
        )
    return moved


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize a folder by file type.")
    parser.add_argument("--folder", required=True, help="Folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        raise SystemExit(f"Error: not a folder: {folder}")

    moved = organize(folder, args.dry_run)
    total = sum(len(v) for v in moved.values())
    mode = "DRY RUN (nothing moved)" if args.dry_run else "ORGANIZED"
    print(f"=== file-organizer: {mode} ===")
    for category in sorted(moved):
        print(f"\n[{category}]")
        for line in moved[category]:
            print(f"  {line}")
    print(f"\n{total} files processed.")


if __name__ == "__main__":
    main()
