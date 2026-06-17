---
name: blotato-post
description: >-
  Take reviewed write-content drafts (or a long-form core — YouTube URL, article,
  PDF, audio, raw text) and distribute them across Brent's social channels via
  Blotato MCP: generate visuals (Nano Banana templates or upload existing assets),
  assemble each post with platform-required fields, run the safety rubric, and
  SCHEDULE behind a mandatory human gate. Use when Brent says "schedule this,"
  "post this," "send these to Blotato," "repurpose this video," or "put this on
  my channels." NEVER posts autonomously. NEVER schedules without explicit approval.
---

# blotato-post (Skill 2)

Distribution layer for Brent's social content factory. Receives finished drafts
from `write-content`, pairs them with visuals, runs the safety gate, and schedules
across connected channels. **Voice and drafting stay in `write-content`. This skill
never rewrites copy. If copy must change for platform fit, re-run `write-content`.**

---

## Inputs

- **Reviewed `write-content` drafts** (normal path) — one draft per target platform,
  each having passed `write-content`'s 5-criterion self-review gate. The draft text
  is treated as final. Any mutation requires re-running `write-content`.

- **OR a long-form core to repurpose first** (alternate path) — one of:
  - YouTube video URL
  - Article URL
  - Local file path (PDF, audio)
  - Raw text block
  - Twitter/X thread URL or TikTok URL

  When a core is given, this skill runs repurpose → `write-content` → distribution
  in sequence before visuals and scheduling. See Process step 3.

- **Optional: target platforms.** Default = all platforms for which drafts were
  provided. Supported: `facebook`, `instagram`, `youtube`, `twitter`. Skip any
  platform with no draft or missing required fields.

- **Optional: `scheduledTime`** (ISO-8601 UTC). Default = ask Brent for the
  preferred slot or suggest the next sensible opening (never post immediately
  unless Brent explicitly says "post now").

- **Optional: account state** (`warm-up` | `ramp` | `scale`). Default = `warm-up`.
  Drives CTA and volume constraints. Read `references/safety-and-warmup.md` for phase
  definitions — ramp constraints affect CTA wording downstream. The skill never
  auto-advances phases.

---

## Process

### 1. Load references

Read all three reference files before taking any action:

- `skills/blotato-post/references/accounts-and-channels.md` — channel IDs,
  per-platform required fields, FB Page handling, runtime re-verify rule.
- `skills/blotato-post/references/pipeline.md` — tool mechanics: repurpose
  (`create_source`), visuals (`create_visual` / presigned upload), scheduling
  (`create_post`, confirmation tools).
- `skills/blotato-post/references/safety-and-warmup.md` — the human gate, 5-criterion
  safety rubric, warm-up ramp, hard rules.

### 2. Re-verify accounts (FIRST API call)

Call `blotato_list_accounts` and map platform → `accountId` from the **live**
response. Never trust the snapshot IDs in the reference table — IDs change on
reconnect (proven: FB `20306` → `37125` on 2026-06-17).

- Map each of the four platforms to its current `accountId`.
- For Facebook: confirm `subaccounts` contains at least one Page entry and extract
  the live `pageId`. If FB has no Page, set Facebook to SKIP for this run and
  surface the skip message:
  > "Facebook has no Page connected in Blotato — connect a Page (dashboard:
  > 'Facebook pages: Don't see your pages? Help') to enable FB posting."
- If any previously connected platform is absent from the live response, log the
  skip and continue with the remaining channels.

### 3. Repurpose a core (if a long-form core was provided)

Skip this step if Brent supplied finished `write-content` drafts directly.

1. Call `blotato_create_source` with the appropriate `sourceType` and URL/content.
   Use `customInstructions` to shape the extraction for the intended use
   (e.g. "extract 5 takeaways for an Instagram carousel" or "identify the three
   strongest proof-of-leverage moments for a YouTube short-form script").
2. If `create_source` returns an `id` without finished content, poll
   `blotato_get_source_status` at 10-second intervals until `status` = `completed`.
3. **Hand the extracted core to `write-content`** (Skill 1) for voice-true
   per-platform drafting. `create_source` is a raw summarizer — it does not write
   in Brent's voice. Wait for `write-content`'s finished, gate-passed drafts before
   proceeding.

### 4. Prepare media (per target platform)

For each target platform with a valid account and an approved draft:

**Path A — Generate from a Blotato template:**
1. Call `blotato_list_visual_templates` to inspect available Nano Banana templates.
2. Call `blotato_create_visual` with the chosen `templateId` and a specific `prompt`.
   Visual generation takes 30 seconds to 5 minutes — it is async.
3. Poll `blotato_get_visual_status` until `status` = `completed`.
   On completion, collect the public `mediaUrl` / `imageUrls` for the next step.

**Path B — Upload an existing local asset:**
1. Call `blotato_create_presigned_upload_url` to get a short-lived upload URL.
2. Upload the file bytes via PUT to that URL.
3. Use the returned public URL in the post payload.

`mediaUrls` **must be publicly accessible URLs** — never pass local file paths or
private URLs. Both paths above return public URLs; use those.

**Platform media rules:**
- Instagram: every post requires `mediaType: story` or `reel` and at least one
  image/video URL. No plain caption-only feed posts via the API.
- YouTube: `title` (required) and `privacyStatus` (public/private/unlisted) required.
- Facebook and X: media is optional; text-only posts are valid.

If media generation fails and the platform requires it (Instagram), skip the
platform for this run and surface the reason.

### 5. Assemble each post

For each target platform, build the `create_post` payload:

- `accountId` — from the live `blotato_list_accounts` response (Step 2).
- `platform` — platform string (`facebook`, `instagram`, `youtube`, `twitter`).
- `text` — the approved draft from `write-content`, character-for-character.
- `mediaUrls` — public URL array from Step 4 (required for IG; include for others
  when a visual was generated or uploaded).
- `scheduledTime` — ISO-8601 UTC. Ask Brent for the slot if not provided.
  **Default path: always set a scheduled time.** Never omit it silently.
  Only omit if Brent explicitly says "post now" — and even then, confirm.
- Platform-specific required fields per `accounts-and-channels.md`:
  - Facebook: `pageId` (live value from `subaccounts`).
  - Instagram: `mediaType` (`story` or `reel`).
  - YouTube: `title`, `privacyStatus`, optionally `shouldNotifySubscribers`.
  - X: threads via `additionalPosts` array if applicable.

Do not call `blotato_create_post` yet. Stop at the safety gate (next section).

---

## Safety gate (REQUIRED before any `create_post`)

**Nothing is scheduled or published without Brent's explicit approval. No exceptions.**

### Pre-gate rubric check

Run the 5-criterion rubric for **every post** in the queue. Check criteria 2–5
now; criterion 1 (Human-approved) is always PENDING at presentation time.

**The 5-criterion safety rubric:**

1. **Human-approved** — Brent has explicitly approved this exact text + visual +
   scheduled time. PENDING until his explicit approval.
2. **Account-valid** — `accountId` resolved from a fresh `blotato_list_accounts`;
   all platform-required fields present (FB `pageId`, IG `mediaType`, YT `title` +
   `privacyStatus`). Missing required field → FAIL → skip platform with clear message.
3. **Voice/compliance intact** — text originated from `write-content` (passed its
   5-criterion rubric) and was not mutated. If altered for platform fit, `write-content`'s
   gate was re-run and passed. No `never-say.md` violations in captions, titles, or
   alt-text.
4. **Warm-up respected** — scheduled (not immediate) unless Brent said "post now";
   CTA is reach-safe for the current account state; not identical copy cross-posted
   at the same minute (stagger by 30+ minutes or vary the caption).
5. **Media-valid** — `mediaUrls` are public and reachable; platform media constraints
   satisfied (IG = story/reel; YouTube = video).

**A post with any criterion at FAIL is not schedulable.** Skip it with a clear
reason. A post with PENDING is held at the gate until Brent approves.

### Gate presentation

Print one rubric line per post:

```
[Platform] [AccountId] — Human-approved: PENDING | Account-valid: PASS | Voice/compliance: PASS | Warm-up: PASS | Media-valid: PASS
```

Then present for each post:
- The **exact text** (character-for-character).
- The **visual URL or preview** (if applicable).
- The **scheduled time** (ISO-8601 UTC).
- The **target platform** with live `accountId`.

For any platform SKIPPED (missing required field, no account, media failure):
- List the platform and reason in a SKIPPED section below the gate.
- Do not include skipped platforms in the approval prompt.

**Wait for explicit approval.** "Yes," "approved," "go," or equivalent affirmative.
Silence, inaction, or "looks good" without a clear approval word is NOT approval.
If Brent says no or requests a change — do not call `create_post`. Revise and
re-present.

---

## Scheduling

On explicit approval:

1. Flip `Human-approved: PENDING` → `PASS` in the rubric record.
2. Call `blotato_create_post` for each approved post with all assembled fields.
   `scheduledTime` must be set (ISO-8601 UTC) unless Brent said "post now."
3. After each `create_post`, confirm via `blotato_list_schedules` — verify the post
   appears in the schedule with the correct time and platform.
4. Optionally call `blotato_get_schedule` on a specific post ID to confirm a single
   scheduled entry.

**Never claim a post is live or scheduled without confirmation from
`blotato_list_schedules` or `blotato_get_post_status`.** Do not infer success from
the `create_post` response alone.

**Post-fire monitoring (when time passes):** Use `blotato_get_post_status` to check
delivery after the scheduled time. Use `blotato_list_posts` to review history.
To reschedule or cancel before fire time: `blotato_update_schedule` /
`blotato_delete_schedule`.

---

## Output

Present a summary table of what was scheduled and what was skipped:

| Platform | Account ID | Scheduled time (UTC) | Link / Post ID | Status |
|---|---|---|---|---|
| Facebook | {accountId from blotato_list_accounts} | {ISO-8601 UTC from blotato_list_schedules} | {post-id from blotato_list_schedules} | Scheduled |
| Instagram | {accountId from blotato_list_accounts} | {ISO-8601 UTC from blotato_list_schedules} | {post-id from blotato_list_schedules} | Scheduled |
| YouTube | {accountId from blotato_list_accounts} | {ISO-8601 UTC from blotato_list_schedules} | {post-id from blotato_list_schedules} | Scheduled |
| X | {accountId from blotato_list_accounts} | {ISO-8601 UTC from blotato_list_schedules} | {post-id from blotato_list_schedules} | SKIPPED — {reason} |

Populate with live values from the `blotato_list_schedules` confirmation. Never fill
the table from the `create_post` response alone.

Include a SKIPPED section if any platforms were not scheduled, with the specific
reason for each skip (missing required field, no account found, media failure,
approval denied, etc.).

---

## Out of scope

- **Does not write or voice copy.** Drafting, pillar selection, CTA wording, and
  voice verification belong to `write-content` (Skill 1). If copy must change for
  any reason, re-run `write-content`.
- **Does not create the lead magnet** ("The Factory Blueprint" or any downstream
  asset). This skill distributes posts, not the assets posts point to.
- **Does not post autonomously.** The human gate is not optional, not bypassable,
  and has no exceptions. No urgency, backlog size, or "just do it" instruction
  overrides it.
