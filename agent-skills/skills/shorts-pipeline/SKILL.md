---
name: shorts-pipeline
description: Use this skill when producing daily YouTube Shorts / Instagram Reels videos (1080x1920, ~30s). Covers the full pipeline: topic planning from rotating categories, image prompt generation, TTS narration, and ffmpeg assembly with Ken Burns effect and subtitle overlays. Use for batch short-form video production (e.g. 3 videos/day).
---

# Shorts Pipeline Skill

Daily short-form video factory: **plan → images → build**. Produces 1080x1920 vertical videos (~30 seconds, 25fps) from topic lists, ready to upload to YouTube Shorts / Instagram Reels.

## Pipeline overview

```
topics/*.json  →  plan.json  →  (agent generates images)  →  TTS mp3  →  ffmpeg  →  output/*.mp4
     ↑ pick one topic per category, no repeats (used.json rotation)
```

Three content categories, one video each per day:

| category | source file | content |
|---|---|---|
| `english` | `english_phrases.json` | 30-second English phrase lesson |
| `funny` | `funny_ideas.json` | short comedy skit |
| `guinness` | `guinness_facts.json` | amazing world record fact |

## Step 1 — Plan

Pick the next unused topic per category (track in `used.json`; reset rotation when exhausted). Write `plan.json`:

```json
{
  "date": "2026-10-02",
  "videos": {
    "english": { "index": 12, "narration": "...", "prompts": ["...", "...", "..."] },
    "funny":   { "index": 5,  "narration": "...", "prompts": ["...", "...", "..."] },
    "guinness":{ "index": 8,  "narration": "...", "prompts": ["...", "...", "..."] }
  }
}
```

- **narration**: spoken script, ~75-90 words (≈30s at normal TTS speed). English category follows a fixed lesson template (greeting → phrase → meaning → example → repeat-after-me ×2 → sign-off).
- **prompts**: 3 image prompts per video. Vertical 9:16, cheerful flat cartoon style, family-friendly, **no text, no watermark** in the image (subtitles are overlaid later).

Plan is idempotent: reuse existing `plan.json` if present.

## Step 2 — Images (agent)

Generate 3 images per video from the prompts (9 images/day). Save as `work/<date>/<category>_img<N>.jpg`. Skip if already present.

## Step 3 — Build

For each video:

1. **TTS**: synthesize narration to mp3 (English voice). Retry up to 3 times on failure.
2. **Subtitle overlay**: render narration text onto the images with PIL — white text with black stroke on a semi-transparent rounded banner, bottom-third placement, NotoSansCJK-Bold.
3. **Segment assembly** (ffmpeg, per 10s segment):
   ```
   scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,
   zoompan=z='min(zoom+0.0009,1.18)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'
   :d=250:s=1080x1920:fps=25,format=yuv420p
   ```
   (subtle Ken Burns zoom), libx264, `-preset medium -crf 20`.
4. **Concat** the 3 segments, mux with the TTS audio → `output/<date>_<category>.mp4`.

Build skips mp4s that already exist.

## Specs

- Resolution: 1080x1920 (9:16), 25fps
- Length: 3 segments × 10s ≈ 30s
- Audio: TTS narration only (no background music in v1)
- Output naming: `<date>_<category>.mp4` (e.g. `2026-10-02_english.mp4`)

## Commands

```bash
python3 build_shorts.py YYYY-MM-DD plan    # topics → plan.json + prompts only
python3 build_shorts.py YYYY-MM-DD build   # TTS + ffmpeg (needs images first)
python3 build_shorts.py YYYY-MM-DD         # plan + build
```

## Notes

- Captions must match the spoken narration exactly — generate overlay text from the same `narration` string used for TTS.
- Keep prompts text-free: any words in the image clash with the subtitle banner.
- If a topic list is exhausted, rotation resets automatically; never repeat the previous day's topic.
