# HyperFrames mechanics

HyperFrames (HeyGen, open-source, Apache-2.0) renders HTML/CSS → MP4 via headless
Chrome + ffmpeg. We use it for **downstream packaging only**: overlay captions +
lower-third + CTA onto a finished clip. CLI is `npx hyperframes@<ver>` (0.7.0 proven).

Prereqs (all present on the Cheese Grater): **Node 22+, ffmpeg, Chrome.**

## ⚠️ Install gotcha — read first

`npx skills add heygen-com/hyperframes` installs the skill **text** but NOT the
**binary assets** (the fonts and `gsap.min.js` are git-LFS files the installer
skips). **Missing `gsap.min.js` → the composition's timeline script throws → every
overlay renders invisible while the video still plays.** This cost a full failed
render on 2026-06-22.

**Fix:** clone the repo and copy the assets into your work dir's `public/`:

```bash
git clone --depth 1 https://github.com/heygen-com/hyperframes.git /tmp/hf
cp /tmp/hf/skills/graphic-overlays/assets/fonts/*           <work>/public/fonts/
cp /tmp/hf/skills/graphic-overlays/assets/vendor/gsap.min.js <work>/public/vendor/
```

(Reuse fonts/gsap already staged in `~/hyperframes-prototype/videos/brent-blackhoodie-overlays/public/` if present.)

## Step-by-step (proven 2026-06-22)

1. **Auth HeyGen** — see `credentials.md`.
2. **Pick + download a clean 16:9 master.** `heygen video list --human` → choose a
   1920×1080 clip with speech from the Brent Clone folder. `heygen video get <id>` →
   `.data.video_url` → `curl -sL "$URL" -o master.mp4`. **ffprobe to CONFIRM 1920×1080
   before using** — the API JSON does not report dimensions, and some "Flip the Script"
   clips are 9:16 (e.g. `d5c1e46a…` is vertical — skip it). The flagship 16:9 master is
   `d5920d626aa042ad85d45f2a9c410ca1` ("Tiger Claw Webinar - Flip the Script v1",
   1920×1080, 240s).
3. **Cut a segment + re-encode with dense keyframes** (sparse GOP freezes on seek):

   ```bash
   ffmpeg -y -ss <start> -i master.mp4 -t <dur> \
     -c:v libx264 -crf 18 -g 25 -keyint_min 25 -pix_fmt yuv420p \
     -movflags +faststart -c:a aac -b:a 160k <work>/public/input-video.mp4
   ```

   (Match `-g`/`-keyint_min` to the source fps — 25 shown.)
4. **Transcribe** (lightweight, no API key, local Whisper):

   ```bash
   npx --yes hyperframes@0.7.0 transcribe <work>/public/input-video.mp4 -d <work> --json
   ```

   → `transcript.json` = flat word array `[{text,start,end}, …]`.
5. **Generate the composition** with `scripts/build_comp16.py` (reads transcript.json,
   writes `public/index.html`). See the contract below.
6. **Lint:** `npx --yes hyperframes@0.7.0 lint <work>/public` → **0 errors**. The
   `timeline_track_too_dense` warning on the caption track is expected and OK.
7. **Render:** `PRODUCER_BROWSER_GPU_MODE=hardware npx --yes hyperframes@0.7.0 render <work>/public -o output.mp4 --fps <fps>`
8. **Verify by eye** — extract frames at a caption moment, the name-strip moment, and
   the CTA, and actually look at them. Never trust the "render complete" line.

## Composition contract (what build_comp16.py emits)

Root `#stage`: `data-composition-id`, `data-start`, `data-duration`, `data-fps`,
`data-width="1920"`, `data-height="1080"`. One paused GSAP timeline registered on
`window.__timelines["<composition-id>"]`.

- **Track 1 — base video:** `<video data-has-audio="true" data-start="0"
  data-duration=… data-track-index="1">` full-bleed (`object-fit:cover`). Keep audio
  with `data-has-audio="true"` (do NOT `muted`).
- **Track 2 — caption rail:** one `<div class="caption clip" data-start data-duration
  data-track-index="2">` per cue, clean lower-third subtitle.
- **Track 3 — name lower-third:** `<div class="clip" …>` top-left so it never collides
  with the bottom caption rail.
- **Track 4 — CTA end card:** `<div class="clip" …>` fullscreen, at the end.

**Lint rules learned the hard way:**

- **Never animate visibility/opacity on a `.clip` element** (`gsap_animates_clip_element`).
  The runtime owns clip visibility. Captions use `.clip` gating alone (clean hard-cut,
  no tween). For the name strip / CTA, wrap inner content in a child div (`.lt-inner`,
  `.cta-inner`) and animate **the child**, never the `.clip` host.
- **Different track-index per layer** — captions (2), name (3), CTA (4). Two timed
  elements on the SAME track that overlap in time = `overlapping_clips_same_track`.
- **Caption clips must not share a boundary** — leave a small gap (≈0.04s) between
  consecutive cues, or floating-point equality trips the overlap check.
- Body `font-family` must list concrete names (`"Inter", …`), not only a CSS var.

Render ≈ 1s of wall-clock per 0.5s of clip (e.g. ~52s for a 28s clip, 6 workers).
