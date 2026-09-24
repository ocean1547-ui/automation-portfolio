#!/usr/bin/env python3
"""
bulk-renamer: rename every file in a folder with a clean, consistent pattern.

    IMG_20260105_001.jpg, IMG_20260105_002.jpg, ...

Safe by default: --dry-run previews the new names without touching anything.

Usage:
    python renamer.py --folder demo/photos --prefix IMG --dry-run
    python renamer.py --folder demo/photos --prefix IMG --execute
"""

import argparse
from datetime import date
from pathlib import Path


def plan(folder: Path, prefix: str, start: int = 1) -> list[tuple[str, str]]:
    files = sorted(p for p in folder.iterdir() if p.is_file())
    today = date.today().strftime("%Y%m%d")
    plans = []
    n = start
    for path in files:
        new_name = f"{prefix}_{today}_{n:03d}{path.suffix.lower()}"
        plans.append((path.name, new_name))
        n += 1
    return plans


def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk-rename files in a folder.")
    parser.add_argument("--folder", required=True, help="Folder with files to rename")
    parser.add_argument("--prefix", default="FILE", help="Name prefix (default: FILE)")
    parser.add_argument("--start", type=int, default=1, help="Starting number")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true", default=True,
                       help="Preview new names (default)")
    group.add_argument("--execute", action="store_true", help="Actually rename files")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        raise SystemExit(f"Error: not a folder: {folder}")

    plans = plan(folder, args.prefix, args.start)
    if not plans:
        print("No files found.")
        return

    mode = "DRY RUN (nothing renamed)" if not args.execute else "RENAMED"
    print(f"=== bulk-renamer: {mode} ===")
    for old, new in plans:
        print(f"  {old}  ->  {new}")
        if args.execute:
            (folder / old).rename(folder / new)
    print(f"\n{len(plans)} files processed.")


if __name__ == "__main__":
    main()
