#!/usr/bin/env python3
"""Render terminal-style animated demo GIFs from captured program output."""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 780, 470
BG = (20, 20, 20)
PROMPT = (126, 231, 135)
CMD = (255, 255, 255)
OUT = (200, 200, 200)
ALERT = (255, 215, 0)
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)
LH = 21
TOP = 18
MAXW = 92  # chars per line


def wrap(text):
    lines = []
    for raw in text.splitlines():
        lines.extend(textwrap.wrap(raw, MAXW) or [""])
    return lines


def render_frame(lines):
    """lines: list of (text, color)."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    y = TOP
    for text, color in lines[-21:]:
        d.text((16, y), text, font=FONT, fill=color)
        y += LH
    return img


def build(scenes, out_path):
    """scenes: list of ('cmd', str) | ('out', str)."""
    frames = []
    shown = []  # list of (text, color)

    def add_frame():
        frames.append(render_frame(shown))

    for kind, text in scenes:
        if kind == "cmd":
            full = "$ " + text
            shown.append(("", CMD))
            for i in range(1, len(full) + 1, 4):
                shown[-1] = (full[:i], CMD)
                add_frame()
            shown[-1] = (full, CMD)
            add_frame()
        else:
            for line in wrap(text):
                color = ALERT if any(k in line for k in ("PRICE DROP", "TARGET HIT")) else OUT
                shown.append((line, color))
                if len(frames) % 1 == 0:
                    add_frame()
    for _ in range(18):
        add_frame()
    frames[0].save(out_path, save_all=True, append_images=frames[1:],
                   duration=70, loop=0, optimize=True)
    print(f"saved {out_path} ({len(frames)} frames)")


def read(path, max_lines=None):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    if max_lines:
        lines = lines[:max_lines]
    return "\n".join(lines)


if __name__ == "__main__":
    build([
        ("cmd", "cd excel-cleaner && python cleaner.py --input data/messy_sales.csv --output data/cleaned_sales.csv"),
        ("out", read("/tmp/demo_out/excel.txt")),
    ], "/home/hatch/workspace/portfolio/excel-cleaner/demo.gif")

    build([
        ("cmd", "python tracker.py --config config.json"),
        ("out", read("/tmp/demo_out/price1.txt")),
        ("cmd", "python tracker.py --config config.json --url demo/product_v2.html"),
        ("out", read("/tmp/demo_out/price2.txt")),
    ], "/home/hatch/workspace/portfolio/price-tracker/demo.gif")

    email_out = read("/tmp/demo_out/email.txt", 22) + "\n... (2 more personalized emails)"
    build([
        ("cmd", "python sender.py --dry-run"),
        ("out", email_out),
    ], "/home/hatch/workspace/portfolio/email-sender/demo.gif")
