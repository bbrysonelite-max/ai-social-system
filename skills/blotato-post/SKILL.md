---
name: blotato-post
description: STUB — not yet implemented. Will take drafts from write-content, generate visuals (Blotato Nano Banana templates), and schedule/post across connected channels (Facebook, Instagram, YouTube, X) via the Blotato MCP. Task #4 verification DONE; build pending (PR-B, three-agent rule).
---

# blotato-post (Skill 2) — BONES (verified, ready to build)

> **Status: STUB — Task #4 verification DONE 2026-06-17; full build pending (PR-B).**
> The Blotato MCP tools are live this session. Build against the verified surface below.
> Distribution layer only; voice/drafting lives in `write-content`.

## Purpose

Take reviewed drafts → (optionally extract a long-form core via Blotato `create_source`) →
generate visuals → schedule/post across connected channels. **Human-in-the-loop review gate
before anything schedules.** Respect the account warm-up ramp (`docs/account-warm-up-plan.md`).

## Verified connected channels (live, 2026-06-17)

| Platform | Account ID | Account | Posting requirement |
|---|---|---|---|
| Facebook | `37125` | Brent Bryson (Page `53954221244`) | `pageId` = `53954221244` ✅ Page connected; **postable** (business Page, not the personal profile — Meta only allows Pages) |
| Instagram | `53674` | @brentbryson | `mediaType` = `story`\|`reel` (visual-first; no plain caption feed post) |
| YouTube | `27755` | Brent Bryson | `title` + `privacyStatus` (public/private/unlisted) |
| X/Twitter | `12730` | @pebobryson801 | none; threads via `additionalPosts` |

LinkedIn + TikTok not connected. Subscription active. 0 posts scheduled (clean slate).

**Runtime rule:** account IDs can change on reconnect (FB went `20306` → `37125` when the
Page was added 2026-06-17). ALWAYS call `blotato_list_accounts` at the start of every run
and map platform→`accountId` from the live response. Never hardcode the IDs in this table.

## Verified Blotato tool surface (the repurposing engine)

- **Accounts:** `blotato_list_accounts` (call FIRST — returns accountId + required fields), `blotato_get_user`.
- **Sources (repurposing input):** `blotato_create_source` — extract/summarize a long-form
  core: `text`, `article`, `youtube`, `twitter`, `tiktok`, `perplexity-query`, `audio`, `pdf`,
  with `customInstructions`. `blotato_get_source_status` to poll long extractions.
- **Visuals (Nano Banana / templates):** `blotato_create_visual` (slideshows, quote cards,
  carousels, infographics, AI videos), `blotato_list_visual_templates`,
  `blotato_get_visual_status`, `blotato_create_presigned_upload_url` (push a local file →
  public URL; use for Desktop infographics).
- **Publish / schedule:** `blotato_create_post` (immediate, `scheduledTime` ISO-8601, or
  `useNextFreeSlot`; threads via `additionalPosts`), `blotato_get_post_status`,
  `blotato_list_posts`, schedule mgmt (`list`/`get`/`update`/`delete_schedule`).
- `mediaUrls` must be **publicly accessible URLs** (`create_visual` returns them).

## Division of labor (resolved — see `docs/DESIGN.md`)

`write-content` owns voice-true per-platform tailoring. `blotato-post` owns extraction
(`create_source`) + visuals (`create_visual`) + publish/schedule (`create_post`). No
one-click "atomize into N posts" call exists; the intelligence stays in the skills.

## TODO before/at implementation (PR-B)

- [x] Live-verify connected channels via the MCP — DONE.
- [x] Map Blotato tool surface — DONE (above).
- [x] FB Page connected (business Page `53954221244`) — all 4 channels now postable.
- [x] Plan the skill (writing-plans) — DONE (`docs/superpowers/plans/2026-06-17-blotato-post-skill.md`, PR #6).
- [ ] Build via three-agent rule (author/test/review separate).
- [ ] Human-in-the-loop review gate before anything schedules.
- [ ] Honor warm-up ramp: reach-safe CTAs, low volume first, no cold external links.
- [ ] Re-verify accounts at runtime (IDs change on reconnect — see Runtime rule above).
