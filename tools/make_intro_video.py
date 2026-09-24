#!/usr/bin/env python3
"""Build a faceless portfolio intro video: title cards + demo GIFs + voiceover."""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path("/home/hatch/workspace/portfolio")
OUT = BASE / "marketing"
W, H = 1280, 720
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PROJECTS = [
    ("excel-cleaner", "Excel Auto-Cleaner",
     "Messy spreadsheets in, clean data out — automatically",
     BASE / "excel-cleaner" / "demo.gif"),
    ("price-tracker", "Price Tracker",
     "Get alerted the moment a price drops to your target",
     BASE / "price-tracker" / "demo.gif"),
    ("email-sender", "Bulk Email Sender",
     "100 personalized emails in the time it takes to send one",
     BASE / "email-sender" / "demo.gif"),
    ("web-scraper", "Web Scraper",
     "Turn any webpage into a clean CSV file",
     BASE / "web-scraper" / "demo.gif"),
]


def text_fit(draw, xy, text, font_path, start_size, fill, anchor="mm", max_w=1100):
    size = start_size
    while size > 20:
        font = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=font) <= max_w:
            break
        size -= 4
    draw.text(xy, text, font=font, fill=fill, anchor=anchor)


def card(title, subtitle, path):
    img = Image.new("RGB", (W, H), (18, 22, 32))
    d = ImageDraw.Draw(img)
    text_fit(d, (W // 2, H // 2 - 60), title, FONT_B, 72, (255, 255, 255))
    text_fit(d, (W // 2, H // 2 + 40), subtitle, FONT_R, 34, (150, 180, 220))
    img.save(path)


def run(*args):
    subprocess.run(args, check=True, capture_output=True)


tmp = OUT / "video_build"
tmp.mkdir(exist_ok=True)

# Cards
card("James", "Python Automation Specialist", tmp / "intro.png")
card("github.com/ocean1547-ui/automation-portfolio",
     "Real working demos — message me to automate your work",
     tmp / "outro.png")
for slug, title, sub, _ in PROJECTS:
    card(title, sub, tmp / f"card_{slug}.png")

INTRO, OUTRO, CARD_T, GIF_T = 4.0, 4.0, 2.0, 6.1
segs = []


def img_seg(png, dur, name):
    out = tmp / name
    run("ffmpeg", "-y", "-loop", "1", "-i", str(png),
        "-t", str(dur), "-vf", "scale=1280:720,format=yuv420p",
        "-r", "15", str(out))
    segs.append(out)


def gif_seg(gif, dur, name):
    out = tmp / name
    run("ffmpeg", "-y", "-stream_loop", "-1", "-i", str(gif),
        "-t", str(dur),
        "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,"
               "pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x121620,format=yuv420p",
        "-r", "15", str(out))
    segs.append(out)


img_seg(tmp / "intro.png", INTRO, "s00.mp4")
for i, (slug, *_rest, gif) in enumerate(PROJECTS, 1):
    img_seg(tmp / f"card_{slug}.png", CARD_T, f"s{i:02d}a.mp4")
    gif_seg(gif, GIF_T, f"s{i:02d}b.mp4")
img_seg(tmp / "outro.png", OUTRO, "s99.mp4")

lst = tmp / "list.txt"
lst.write_text("".join(f"file '{s}'\n" for s in segs))
video = tmp / "silent.mp4"
run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
    "-c", "copy", str(video))

final = OUT / "intro_video.mp4"
run("ffmpeg", "-y", "-i", str(video), "-i", str(OUT / "video_script_audio.mp3"),
    "-c:v", "copy", "-c:a", "aac", "-shortest", str(final))
print("saved", final, final.stat().st_size, "bytes")
