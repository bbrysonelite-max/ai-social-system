---
name: package-video
description: >-
  Package a FINISHED talking-head clip (one of Brent's HeyGen clones) for posting:
  add clean captions + a name lower-third + a CTA end card, baked into ONE 16:9
  master, then prep the YouTube-first → Facebook-announce loop. Use when Brent says
  "package this video", "caption my clip", "add captions / lower-third / CTA to this
  video", "prep this clone for posting", or "make the YouTube + the Facebook announce".
  Downstream packaging + distribution only — it does NOT generate avatars (Brent makes
  clones himself in the HeyGen GUI). 16:9 landscape ONLY — never 9:16.
---

# package-video

Takes a finished clone clip and turns it into a posting-ready package: a single
**16:9** master with clean captions + a name lower-third + a CTA end card, plus
the Facebook/IG/X announcement copy to drive viewers to it. Rendered once with
HyperFrames. **Brent makes the clone; this skill only packages and distributes it.**

Proven working example: `~/hyperframes-prototype/caption-demo-16x9/` (built 2026-06-22).

## Hard rules (do not break)

1. **16:9 landscape ONLY.** Never render or deliver 9:16 with the current clone set —
   Brent rejects vertical outright. If the only clean clip is vertical, get a 16:9 one
   from HeyGen instead. (See [[feedback-never-9x16-current-clones]].)
2. **Captions baked exactly ONCE** into the master. Every social cut (FB teaser, IG
   Reel, X clip) is a *cut of that one file* — never re-caption.
3. **Clean readable caption rail — not flashy.** No matte-occlusion VFX, no behind-the-
   head word effects. Lower-third subtitles that read.
4. **The clip plays untouched.** Captions/overlays are the only thing added. Never
   recolor, crop, or re-time the footage.
5. **Secrets: reference by name, never echo a key value.** See `references/credentials.md`.
6. **Compliance — NO claims in any overlay, thumbnail, or copy.** No tenure ("X years
   in…"), no rank/title, no income/earnings/success claims, no implied results.
   The lower-third is **identification only** (name). Thumbnails hook on curiosity,
   never credentials. **Brent is the authority on the lines and clears any
   descriptor.** (A prominent "39 Years in Network Marketing" lower-third was the
   exact mistake that triggered this rule — name only, always.)

## Quality gate (MANDATORY — it posts under Brent's name)

Two gates around the package, every box mandatory — full checklist in
**[references/quality-gate.md](references/quality-gate.md)**:

- **GATE A — CLONE-IN** (before packaging): the clip is an **approved look**
  (blue-polo Avatar IV canonical, or black-hoodie — never a rejected/legacy clone),
  **16:9 1920×1080**, approved voice, clean render, says the approved script.
- **GATE B — PUBLISH-OUT** (before staging): captions once · **lower-third name-only**
  · CTA `stan.store/brentbryson` · thumbnail clean · compliance scrubbed · verified
  by looking.
- **The human gate:** staged **PRIVATE-first** → **Brent reviews** → **Brent flips
  public**. Claude never makes a video public under Brent's name.

⚠️ The approved-clone registry's defaults are **stale** (`9:16` / `portrait` / Buffer) —
the gate **overrides** them: **16:9 only, Blotato only.**

## Quick start (the proven path)

```bash
# 0. Prereqs (all present on the Cheese Grater): Node 22+, ffmpeg, Chrome.
# 1. Auth HeyGen (key from kloop.env — see references/credentials.md; never echo it):
KEY=$(grep -m1 'HEYGEN_API_KEY=' ~/Desktop/GitSync/kloop.env | sed -E 's/.*HEYGEN_API_KEY=//' | tr -d '[:space:]"')
printf '%s' "$KEY" | ~/.local/bin/heygen auth login; unset KEY
# 2. Find a clean 16:9 speaking master in the Brent Clone folder:
~/.local/bin/heygen video list --human          # pick a 1920x1080 clip with speech
~/.local/bin/heygen video get <id>              # → .data.video_url ; download + ffprobe to CONFIRM 16:9
# 3. Cut a segment, transcribe, generate, lint, render — see references/hyperframes.md
```

Full step-by-step (auth → download → cut → transcribe → compose → lint → render →
verify) is in **[references/hyperframes.md](references/hyperframes.md)**. Use the
generator at `scripts/build_comp16.py` to emit the composition from the transcript.

## Workflow checklist

- [ ] Auth HeyGen CLI from `kloop.env` (never the stale `BRENT_CREDENTIALS.md` keys)
- [ ] **GATE A — clone-in:** clip is an APPROVED look (blue-polo Avatar IV / black-hoodie,
      not a rejected/legacy clone), **16:9 1920×1080** (ffprobe-confirm), approved voice,
      clean render, says the approved script — see [references/quality-gate.md](references/quality-gate.md)
- [ ] Cut the segment; `npx hyperframes transcribe` for word timings
- [ ] Generate composition (`scripts/build_comp16.py`): video + caption rail + name
      lower-third + CTA end card, each on its own track-index
- [ ] `npx hyperframes lint public` → 0 errors (track-density warning is OK)
- [ ] Render with `PRODUCER_BROWSER_GPU_MODE=hardware`
- [ ] **Verify by extracting frames and looking** — never trust the success line
- [ ] **GATE B — publish-out:** captions once · lower-third name-only · CTA clean ·
      thumbnail clean · compliance scrubbed — see [references/quality-gate.md](references/quality-gate.md)
- [ ] Build the review folder + announce copy (see [references/announce-loop.md](references/announce-loop.md))
- [ ] **Human gate:** stage **PRIVATE-first** → Brent reviews → Brent flips public

## Where things go

- **Credentials map:** [references/credentials.md](references/credentials.md)
- **HyperFrames mechanics + install gotcha + composition contract:** [references/hyperframes.md](references/hyperframes.md)
- **YouTube-first → Facebook-announce loop + copy templates:** [references/announce-loop.md](references/announce-loop.md)
- **Composition generator:** `scripts/build_comp16.py`

## Out of scope

- **No avatar/clone generation.** Brent makes clones in the HeyGen GUI; every
  API/Video-Agent render has been rejected. This skill starts from a finished clip.
- **No posting.** It produces the master + teaser + copy for review; actual
  scheduling goes through the `blotato-post`/`cadence` skills once Brent approves.
- **No 9:16.** See hard rule 1.
