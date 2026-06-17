---
name: blotato-post
description: STUB — not yet implemented. Will take drafts from write-content, generate visuals (Blotato Nano Banana templates), and schedule/post across connected channels (Facebook, Instagram, YouTube, X) via the Blotato MCP. Build after write-content; requires the Blotato MCP tools (load on a fresh session).
---

# blotato-post (Skill 2) — BONES

> **Status: STUB + BLOCKED.** Requires the Blotato MCP tools, which only load on a
> fresh session. Build after `write-content` is done.

## Purpose

Take reviewed drafts → generate visuals → schedule/post across connected channels.
Distribution layer only; voice/drafting lives in `write-content`.

## Depends on
- Blotato MCP (`https://mcp.blotato.com/mcp`, registered, `✔ Connected`).
- Reviewed output from `write-content`.

## TODO before implementation
- [ ] Live-verify connected channels (FB, IG, YouTube, X) via the MCP.
- [ ] Map Blotato tool surface (publish, media/visual gen, scheduling).
- [ ] Human-in-the-loop review gate before anything schedules.
- [ ] Account warm-up ramp (low volume first) — see `docs/DESIGN.md`.
