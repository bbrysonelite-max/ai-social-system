---
name: make-thumbnail
description: >-
  Generate a deterministic, high-CTR 1280x720 YouTube thumbnail — Brent's real
  photo + a bold headline rendered by code (HTML -> PNG via headless Chrome), NOT
  AI image generation. Same inputs produce the exact same clean result every time:
  perfect text, real face, no garbling, no re-rolls. Use when Brent says "make a
  thumbnail", "thumbnail for this video", "need a thumbnail", or after a video is
  packaged and needs its YouTube thumbnail. One command, one proven layout.
---

# make-thumbnail (social system — creative)

**The deterministic thumbnail.** One proven layout, filled by code. No AI roulette,
no garbled text, no stranger's face. Same inputs → identical clean output.

## Quick start

```bash
python3 scripts/make_thumbnail.py --headline "AI ISN'T|HAPPENING|TO YOU"
# -> ./thumbnail.png  (1280x720)
```

- `--headline` (required) — `|` breaks lines. **The last line gets the accent color** (the pop).
- `--photo` — real photo, right side. Defaults to the bundled approved photo.
- `--out` — output path (default `./thumbnail.png`).
- `--accent` — accent hex (default `#ffd400`, the proven yellow).

## The layout (one proven design — this is the "elegant simple")

Real photo on the **right third**, faded into a dark canvas (no hard seam), faint
accent glow lower-right. Bold white headline on the **left**, last line in accent
yellow, with a yellow→red underline bar. 1280×720. This is the design Brent
approved ("it's me, and it's clean").

## What makes it get attention (baked into the template — don't fight it)

1. **One real face, large.** Brent's actual photo, not an AI render — high-trust, instant recognition.
2. **3–5 words, 2–4 lines.** Short. Readable on a phone. The script auto-shrinks the font as lines/length grow so it never clips.
3. **One accent pop.** The last line + underline carry the single color. Everything else is white on dark = maximum contrast.
4. **Curiosity, not credentials.** The headline hooks on tension ("AI isn't happening to you", "the ground floor is wide open").

## COMPLIANCE — hard rule

The headline is yours, but it must carry **NO tenure / rank / income / credential /
success claims** (FTC). No "39 years", no "$X", no "top earner". Hook on curiosity.
The skill never adds any text of its own — what you pass is what renders.

## How it renders (deterministic, no dependencies to install)

`scripts/make_thumbnail.py` fills `assets/template.html` (with `assets/fonts/` +
your photo) and screenshots it with **headless Chrome** at exactly 1280×720. Chrome
is already on the machine (it's what HyperFrames uses). No AI service, no API key,
no network. Same inputs always produce the same PNG.

## Where this fits

Part of the AI social media system. After `package-video` makes the captioned
master, run this for the YouTube thumbnail, then post via `cadence` /
`youtube-autoload.sh`. Image *generation* for in-feed posts still uses Blotato's
Nano Banana templates (in `blotato-post`); **thumbnails use this** — deterministic
beats generative when the result has to be clean and repeatable.
