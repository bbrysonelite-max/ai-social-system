---
name: write-content
description: STUB — not yet implemented. Will turn one idea (or a local file/screenshot) into platform-specific social posts in Brent Bryson's voice for Facebook, Instagram, YouTube, and X. Drafting only; no posting or scheduling (see blotato-post).
---

# write-content (Skill 1) — BONES

> **Status: STUB.** This skill is scaffolded but not built. Do not rely on it yet.
> Flesh out once the calibration items in `docs/DESIGN.md` are answered.

## Purpose

One command → platform-specific drafts in Brent's voice. Drafting only.
The earned-authority voice on AI for direct sales / affiliate / network marketing.

## Inputs (planned)

- A topic/idea, OR a local file (note, screenshot, a metric "receipt").
- Target platforms (default priority: Facebook, Instagram, YouTube, X).

## Outputs (planned)

- Labeled, platform-specific drafts ready for Brent's review, then handed to `blotato-post`.

## Voice engine (planned — loads every run)

See `references/SOURCES.md` for the canonical voice files. The skill must pass one test
on every output: **"Does this sound like Brent Bryson?"** If no — rewrite.

## TODO before implementation

- [ ] Answer calibration items in `docs/DESIGN.md` (CTA/close, never-say list).
- [ ] Bundle/refresh voice reference files into `references/`.
- [ ] Define per-platform format rules (FB/IG/YouTube/X).
- [ ] Write the generation + self-review loop.
