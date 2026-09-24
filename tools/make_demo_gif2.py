#!/usr/bin/env python3
"""Demo GIFs for the second batch of portfolio projects."""
import sys
sys.path.insert(0, "/home/hatch/workspace/portfolio/tools")
from make_demo_gif import build, read  # noqa: E402


def head(path, n):
    return "\n".join(read(path).splitlines()[:n])


if __name__ == "__main__":
    build([
        ("cmd", "python organizer.py --folder demo/inbox --dry-run"),
        ("out", head("/tmp/demo_out2/org1.txt", 20)),
        ("cmd", "python organizer.py --folder demo/inbox && find demo/inbox -type f | sort"),
        ("out", read("/tmp/demo_out2/org2.txt")),
    ], "/home/hatch/workspace/portfolio/file-organizer/demo.gif")

    build([
        ("cmd", "python scraper.py --config config.json"),
        ("out", read("/tmp/demo_out2/scrape.txt")),
    ], "/home/hatch/workspace/portfolio/web-scraper/demo.gif")

    build([
        ("cmd", "python renamer.py --folder demo/photos --prefix IMG --dry-run"),
        ("out", read("/tmp/demo_out2/rename.txt")),
    ], "/home/hatch/workspace/portfolio/bulk-renamer/demo.gif")
