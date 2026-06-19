# Blotato Slots + REST Reference

**Date:** 2026-06-17
**Source:** Blotato REST API reference (Brent Bryson, 2026-06-17).

---

> **Scope of this file:** the Blotato REST API contract — base URL, auth, accounts, schedule slots, post publishing, sources/visuals, per-channel required fields, and common mistakes. Ramp arithmetic and `state.json` rules are in `skills/cadence/references/ramp-and-state.md`. Voice and drafting are in `skills/write-content/references/`. Post-tool mechanics (MCP tools) are in `skills/blotato-post/references/pipeline.md`.

---

## Auth + key handling

- **Base URL:** `https://backend.blotato.com/v2`
- **Header:** `blotato-api-key: <key>`
- **Where to read the key:** `~/.claude.json` at path `.mcpServers.blotato.headers["blotato-api-key"]`.
- **Never echo or print the key** — not in logs, not in summaries, not in output shown to Brent.
- **Preserve the key exactly.** It may end in one or more `=` characters (base64 padding). Do not strip, trim, or URL-encode trailing `=`.
- **Verify a key:** `GET /users/me` — a 200 response confirms the key is valid.

---

## Accounts (always first)

Account IDs change on reconnect. Fetch live IDs at the start of every run — do not use cached or hardcoded values.

### List accounts

```
GET /users/me/accounts
GET /users/me/accounts?platform=twitter   # filter by platform
```

Response shape: `{ "items": [{ "id": "…", "platform": "…", "username": "…" }] }`

Use `items[].id` as `accountId` in all subsequent calls.

### List subaccounts

```
GET /users/me/accounts/{accountId}/subaccounts
```

Returns `{ "items": [{ "id": "…", … }] }`. Use `items[].id` as:
- **Facebook:** `target.pageId` (required — see Per-channel fields).
- **YouTube:** `target.playlistIds` (optional playlist targeting).

---

## Schedule slots (optional — plan-gated)

> **LIVE TEST FINDING (2026-06-17):** On Brent's current Blotato plan, `POST /schedule/slots` returns **`Unauthorized`**. Slots and `useNextFreeSlot` are **OPTIONAL / best-effort — NOT the primary scheduling mechanism.**
>
> **The primary scheduling mechanism is explicit `scheduledTime` on `POST /posts`** — this is verified working. Use explicit ISO-8601 `scheduledTime` values on every `POST /posts` call. Fall back to `useNextFreeSlot` only if the plan is upgraded and slot creation is confirmed to work.

Slots are recurring posting windows. Each slot defines a time-of-day and day-of-week for a given channel. When `useNextFreeSlot: true` is set on a post, Blotato drops it into the next open slot for that channel. (Docs below preserved for reference — may work on other plans or after a plan upgrade.)

### List existing slots

```
GET /schedule/slots
```

Response: `{ "items": [{ "id": "…", "hour": 9, "minute": 0, "day": "monday", "selectedTargets": [{ "platform": "…", "accountId": "…", "subaccountId": "…" }] }] }`

### Create slots

```
POST /schedule/slots
Body: {
  "slots": [
    {
      "hour": 9,
      "minute": 0,
      "day": "monday",
      "selectedTargets": [
        { "platform": "facebook", "accountId": "…", "subaccountId": "…" }
      ]
    }
  ]
}
```

`day` values: `"monday"` | `"tuesday"` | `"wednesday"` | `"thursday"` | `"friday"` | `"saturday"` | `"sunday"`.

### Find next available slot

```
POST /schedule/slots/next-available
Body: { "platform": "…", "accountId": "…", "subaccountId": "…" }
```

Response: `{ "slot": { "slotId": "…", "slotTime": "<ISO-8601>" } }`

### Ramping rule — how slots change each week

Week N has **N slots/day/channel** (capped at 4 — see `ramp-and-state.md` for full arithmetic).

When advancing to a new week:
1. Call `GET /schedule/slots` and collect existing slot IDs per channel.
2. **Add** the new slots needed to reach the new count.
3. **Do not duplicate** a slot that already exists at the same `hour`/`minute`/`day`/`selectedTargets` combination.
4. Never delete existing slots when ramping up.

| Week | Slots to have per day per channel |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4+ | 4 |

---

## Publishing & scheduling

### Create a post

```
POST /posts
Body: {
  "post": {
    "accountId": "…",
    "content": {
      "text": "…",
      "mediaUrls": [],
      "platform": "twitter",
      "additionalPosts": [         // optional — X/Threads thread continuation
        { "text": "…", "mediaUrls": [] }
      ]
    },
    "target": {
      "targetType": "twitter"
      // platform-specific fields also go here — see Per-channel fields
    }
  },
  // --- SCHEDULING FIELDS ARE ROOT-LEVEL (siblings of "post") ---
  "scheduledTime": "2026-06-20T15:00:00Z"   // ISO-8601 UTC
  // OR:
  // "useNextFreeSlot": true
}
```

**Scheduling field placement is critical.**
`scheduledTime` and `useNextFreeSlot` are **root-level siblings of `post`** — they must NOT be nested inside `post` or inside `content`. If nested, Blotato publishes the post immediately without scheduling.

| Scheduling option | When to use |
|---|---|
| `"scheduledTime": "<ISO-8601 UTC>"` | Default — use this unless Brent says "post now." |
| `"useNextFreeSlot": true` | Use when letting Blotato pick the next open slot. Do not combine with `scheduledTime`. |
| Neither | Omit both only when publishing immediately on Brent's explicit instruction. |

`content.platform` and `target.targetType` **must match** — a mismatch causes a publishing error.

### Poll post status

```
GET /posts/{postSubmissionId}
```

Response `status` values: `in-progress` | `published` | `failed`. On `published`, the response includes `publicUrl`.

### Manage the schedule queue

```
GET /schedules                  // list all scheduled posts
GET /schedules/{id}             // retrieve one scheduled post
DELETE /schedules/{id}          // cancel a scheduled post
PATCH /schedules/{id}           // update (reschedule) a post
```

> **DELETE gotcha (verified 2026-06-17):** `DELETE /schedules/{id}` must be sent with the auth header ONLY. Do **NOT** set `Content-Type: application/json` and do **NOT** send a request body — an empty body with that content-type returns `400 "Body cannot be empty"`. Send the DELETE bare: auth header, no body, no content-type.

---

## Sources & visuals

### Repurpose a source

```
POST /source-resolutions-v3
Body: {
  "source": {
    "sourceType": "youtube" | "article" | "text" | "twitter" | "tiktok" | "pdf" | "audio" | "perplexity-query",
    "url": "…"       // for youtube/article/twitter/tiktok/pdf/audio
    // OR:
    "text": "…"      // for sourceType "text"
  }
}
```

Response includes an `id`. Poll until complete:

```
GET /source-resolutions-v3/{id}
```

Poll until `status` is `completed`. On completion the response includes `content` (extracted summary) and `title`.

The extraction is raw summarization — **not Brent's voice**. Hand the extracted content to `write-content` for voice-true drafting.

### Generate a visual

```
POST /videos/from-templates
Body: {
  "templateId": "<bare-UUID>",   // UUID only — NOT the full template path
  "inputs": {},
  "prompt": "…",
  "render": true
}
```

Discover available templates: `GET /videos/templates` *(verify the visual path live before the first real IG batch — not yet smoke-tested)*

Poll until ready:

```
GET /videos/creations/{id}
```

Poll until `status` is `done`. On completion the response includes `mediaUrl` and/or `imageUrls`. Use those URLs directly in `content.mediaUrls` when creating a post. Carousel = pass multiple image URLs.

Visual generation takes **30 seconds to 5 minutes** — do not treat it as instant. Poll with at least 10 seconds between attempts.

---

## Per-channel required fields

All fields below go inside `target` unless noted.

| Platform | Required fields | Notes |
|---|---|---|
| **twitter** | none | Thread continuation via `content.additionalPosts[]`. |
| **threads** | none | Thread continuation via `content.additionalPosts[]` (same pattern as twitter/bluesky). |
| **facebook** | `target.pageId` | Fetch `pageId` from `/users/me/accounts/{id}/subaccounts` → `items[].id`. Also: `mediaType: "reel"` for video; `mediaType: "story"` for story; omit `mediaType` for text or image feed post. |
| **instagram** | `target.mediaType` (`"reel"` or `"story"`) + at least one URL in `content.mediaUrls` | Default `mediaType` is `"reel"`. No caption-only feed post — a media URL is always required. |
| **youtube** | `target.title` (required), `target.privacyStatus` (`"private"` \| `"public"` \| `"unlisted"`) (required), `target.shouldNotifySubscribers` (boolean, required) + at least one **video** URL in `content.mediaUrls` | **VERIFIED WORKING 2026-06-19** — posted live to account `27755` (https://www.youtube.com/watch?v=9iWR89XEmOo, private test). Blotato posts to YouTube fine; the only requirement is a video file URL. To host a local/remote video, `POST /v2/media` with `{"url":"<public video url>"}` → returns a Blotato-hosted `url` → use that in `content.mediaUrls`. `content.text` = video description. YouTube is also valid as a `sourceType` in `POST /source-resolutions-v3` for repurposing YouTube URLs as content cores. |

---

## Common mistakes

| Mistake | Effect | Fix |
|---|---|---|
| Nesting `scheduledTime` or `useNextFreeSlot` inside `post` | Post publishes immediately instead of scheduling | Move both fields to root level, sibling of `"post"` |
| Missing Facebook `target.pageId` | API error or post goes to wrong page | Fetch `pageId` from subaccounts before posting |
| `content.platform` ≠ `target.targetType` | Publishing error | Both must be the same platform string (e.g. both `"instagram"`) |
| Using full template path as `templateId` instead of bare UUID | Visual generation fails | Strip to bare UUID only |
| Calling `/accounts` instead of `/users/me/accounts` | 404 | Correct path is `/users/me/accounts` |
| Using cached account IDs across sessions | Posts to wrong account if IDs changed on reconnect | Always call `GET /users/me/accounts` at the start of each run |
| Posting to Instagram without a media URL | API error | IG always requires `mediaType` + a URL in `content.mediaUrls` |
