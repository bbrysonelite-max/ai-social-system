# Blotato Pipeline Reference

**Date:** 2026-06-17
**Source:** `docs/DESIGN.md` "Blotato tool surface (mapped 2026-06-17)"; `skills/blotato-post/SKILL.md` "Verified Blotato tool surface".

---

> **Channel IDs, account IDs, and per-platform required fields** are in
> `skills/blotato-post/references/accounts-and-channels.md`. This file covers the
> tool mechanics only — how to repurpose a core, make visuals, and schedule a post.

> **Always call `blotato_list_accounts` at the start of every run** to get live
> account IDs before any step below. See accounts-and-channels.md § "Runtime rule."

---

## Step A — Repurpose a core (optional)

Use this step when you have a long-form piece (YouTube video, article, PDF, audio
recording, tweet, or raw text) that you want to pull a core out of before drafting.
Skip it when Brent is starting from scratch or provides the core text directly.

### Tools

1. **`blotato_create_source`** — extracts and summarizes a long-form source.

   | Parameter | Value / notes |
   |---|---|
   | `sourceType` | `text` \| `article` \| `youtube` \| `twitter` \| `tiktok` \| `perplexity-query` \| `audio` \| `pdf` |
   | `url` or `content` | URL for article/youtube/twitter/tiktok; raw text for `text`; file URL for audio/pdf |
   | `customInstructions` | Shape the extraction for the intended use (e.g. "extract 5 takeaways for an Instagram carousel" or "identify the three strongest proof-of-leverage moments"). Be specific — this is the only control lever over what comes out. |

   The tool polls for up to ~20 seconds. If the extraction is still running when it
   returns, it responds with an `id` instead of finished content.

2. **`blotato_get_source_status`** — poll until extraction is done.

   - Use only when `create_source` returned an `id` without finished content.
   - Wait at least **10 seconds** between polls.
   - Poll until `status` is `completed`.
   - Use the returned summary/content as your core.

### Handoff to `write-content`

`create_source` does **NOT** write in Brent's voice — it summarizes the source
material, nothing more. Once the core is extracted, hand it off to the
`write-content` skill (Skill 1) for voice-true per-platform drafting.
`blotato-post` receives the finished drafts back from `write-content` before
proceeding to Steps B and C.

---

## Step B — Visuals

There are two paths: generate a visual from a Blotato template, or upload an
existing local asset (e.g. a Desktop infographic).

**IG requires a visual.** Every Instagram post must be visual-first (story, reel, or
carousel). Facebook and X may be text-only; YouTube community posts may include an
image but it is not required.

### Path 1 — Generate from a template

1. **`blotato_list_visual_templates`** — list available Nano Banana templates.
   Inspect the list and pick the template ID that fits the post type (quote card,
   carousel, slideshow, infographic, AI video, etc.).

2. **`blotato_create_visual`** — start async visual generation.

   | Parameter | Value / notes |
   |---|---|
   | `templateId` | ID from the template list |
   | `prompt` | Descriptive text of what the visual should show. Be specific — color, subject, energy. |
   | `inputs` | Leave as `{}` on the first attempt. Only populate if you know the template's required input fields. |

   Generation takes **30 seconds to 5 minutes** — do not assume it is instant.

3. **`blotato_get_visual_status`** — poll until done.

   - Poll until `status` is `completed` (or `failed`).
   - On completion the response includes a public `mediaUrl` or `imageUrls` array.
   - Use those URLs directly in `blotato_create_post` `mediaUrls`.
   - Carousel = pass multiple image URLs in `mediaUrls`.

### Path 2 — Upload an existing local asset

Use this when Brent has already created an infographic, screenshot, or graphic on
his Desktop that he wants to attach.

1. **`blotato_create_presigned_upload_url`** — get a short-lived upload URL.
2. Upload the file to that URL (PUT the file bytes).
3. The response includes a public URL — use that in `blotato_create_post` `mediaUrls`.

> `mediaUrls` MUST be publicly accessible. Do not pass local file paths or private
> URLs. Both `create_visual` and `create_presigned_upload_url` return public URLs —
> use those.

---

## Step C — Schedule the post

**Human gate before this step.** Show Brent all drafts + visual URLs and get
explicit approval before calling `blotato_create_post`. Nothing schedules without
sign-off.

### Tool: `blotato_create_post`

| Parameter | Value / notes |
|---|---|
| `accountId` | From the live `blotato_list_accounts` response — not from the snapshot table. |
| `platform` | Platform string (e.g. `facebook`, `instagram`, `youtube`, `twitter`). |
| `text` | The approved draft from `write-content`. |
| `mediaUrls` | Array of public URLs from Step B (required for IG; optional for others). |
| `scheduledTime` | **ISO-8601 UTC. Default path — always set this unless Brent explicitly says "post now."** |
| `useNextFreeSlot` | Alternative to `scheduledTime` when letting Blotato pick the next open slot. Do not use if Brent has given a specific time. |
| `additionalPosts` | Array for X/Threads/Bluesky threads. Pass subsequent thread posts here. |
| Platform-specific fields | See `accounts-and-channels.md` § "Per-platform required fields" (FB `pageId`, IG `mediaType`, YT `title` + `privacyStatus`). |

### Confirm + monitor

After scheduling, confirm with **`blotato_list_schedules`** — verify the post
appears in the schedule with the correct time and platform.

- **`blotato_get_schedule`** — retrieve a single schedule by its ID (e.g. to
  confirm one specific scheduled post before its fire time), as distinct from
  `blotato_list_schedules` which returns the whole queue.
- **`blotato_get_post_status`** — check delivery status of a specific post after
  the scheduled time has passed.
- **`blotato_list_posts`** — review post history.
- **`blotato_update_schedule`** / **`blotato_delete_schedule`** — reschedule or
  cancel if Brent requests a change before the post fires.

---

## Gotchas

| Issue | What to do |
|---|---|
| `mediaUrls` not public | Never pass local paths or private URLs. Use `blotato_create_visual` (returns public URL) or `blotato_create_presigned_upload_url` (upload → public URL). |
| Instagram plain caption | IG has no caption-only feed post via the API. Every IG post requires `mediaType: story` or `reel` and at least one image/video URL. |
| Visual gen is async | `create_visual` kicks off a job — poll `get_visual_status` until `completed`. Do not assume the visual is ready immediately. |
| Account IDs change on reconnect | Account IDs can change on reconnect — re-verify via `blotato_list_accounts`; see `accounts-and-channels.md`. Always call `blotato_list_accounts` first; map live IDs before posting. |
| `create_source` is not voice | The extraction is raw summarization, not Brent's voice. Hand the core to `write-content` before drafting platform posts. |
| Scheduling default | Always set `scheduledTime` (ISO-8601 UTC) unless Brent explicitly says "post now." Never omit it silently. |
