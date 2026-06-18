# Cadence System (Skill 3 `cadence`) — Design

Date: 2026-06-17
Status: design (approved in conversation; spec for review before planning)

## Goal

A durable weekly-batch content cadence system that produces and schedules on-voice
posts across Brent's connected channels at a **ramping volume**, behind a human
approval gate — so the content factory runs on a ~10-minute weekly touch instead of
daily willpower. This is the layer that makes the factory *stick* (prior attempts
fizzled because they depended on daily effort).

## The ramp (locked)

| Week | Posts/day/channel | Channels | Total/week |
|---|---|---|---|
| 1 | 1 | FB, IG, X (+YT best-effort) | 28 |
| 2 | 2 | " | 56 |
| 3 | 3 | " | 84 |
| 4+ | 4 | " | 112 (= 16/day target) |

Volume auto-steps up by calendar week from a fixed **start date**. 7 days/week.

## Operating model (Option A — approve-first)

Each weekly run drafts the whole week, **presents the full batch** (text + visuals +
send times) for Brent's review, and **only schedules on his explicit approval**. Once
voice is trusted (a week or two), this can graduate to hands-off (Option B) — out of
scope for v1 but the design must not preclude it.

## Architecture

A third skill, `skills/cadence/`, orchestrating the two existing skills + Blotato's
REST API directly (the MCP key only loads at session start; REST with the config key
works in-session — proven 2026-06-17). It does **not** re-implement drafting (that's
`write-content`) or invent voice — it sequences, schedules, and tracks.

### Components

1. **Ramp + state** (`state.json` in the repo or a data dir): `startDate`, computed
   `currentWeek` → `postsPerDayPerChannel`, a **used-ideas ledger** (so nothing
   repeats), and a record of what's been scheduled. Resumable; the source of truth
   for "what week are we in / what's left."

2. **Schedule-slot backbone** (Blotato `/schedule/slots`): define recurring posting
   slots per channel matching the week's volume. Ramp = add slots each week (Wk1: 1
   slot/day/channel … Wk4: 4/day). The batch fills slots via `useNextFreeSlot` or
   explicit `scheduledTime`. Blotato owns "when," the skill owns "what."

3. **Content supply**: pull fresh material from (a) the idea bank
   (`~/Desktop/Social Media Posts: Ideas/`, ~76 ideas) and (b) repurposed cores via
   `POST /source-resolutions-v3` (the webinar, the 2 YouTube scripts, long-form). The
   used-ideas ledger prevents repeats. Brent's own manual posts supplement freely.

4. **Drafting**: every post goes through `write-content` (voice + 5-criterion rubric +
   batch cadence-variety guard). The cadence skill never mutates voice.

5. **Visuals**: for Instagram (image/reel required), generate via Blotato
   `POST /videos/from-templates` (prompt-driven, `inputs:{}`), poll to `done`, use the
   returned public URL. FB/X are text-ok.

6. **Scheduler**: assemble each post per the REST contract (below), assign to the
   week's slots/times, present the batch, and on approval `POST /posts` with
   `scheduledTime` (or `useNextFreeSlot`). Confirm via `GET /schedules`.

7. **Approval gate**: the batch is shown in one view; nothing schedules without an
   explicit approval word (reuses `blotato-post`'s safety rubric). FB skips cleanly if
   no Page; any platform missing required fields is skipped with a message.

8. **Durability**: a weekly `/schedule` reminder triggers the run; state persists; the
   ramp advances automatically. The only recurring human action is the approval.

### Channels (honest scope)

- **Facebook** — `target.pageId` from `/users/me/accounts/{id}/subaccounts` (Page `53954221244`). Text/image.
- **Instagram** — `mediaType` reel/story; **a visual is generated every post**.
- **X** — text-ready; threads via `additionalPosts`. (Proven live 2026-06-17.)
- **YouTube** — `title` + `privacyStatus` + `shouldNotifySubscribers`; **a video upload**.
  4 fresh videos/day is not achievable from nothing — YT runs **best-effort** off
  repurposed webinar/long-form clips + Brent's own uploads, NOT 4-from-scratch/day.
  The ramp's 4/day applies fully to FB/IG/X; YT fills as footage allows.

### Blotato REST contract (from the API reference, base `https://backend.blotato.com/v2`, header `blotato-api-key`)

- Accounts: `GET /users/me/accounts`, `GET /users/me/accounts/{id}/subaccounts` (FB pageId).
- Publish/schedule: `POST /posts` (scheduling fields are **root-level siblings of `post`**, never nested); poll `GET /posts/{postSubmissionId}`.
- Slots: `GET/POST /schedule/slots`, `POST /schedule/slots/next-available`.
- Schedules: `GET /schedules`, `PATCH /schedules/{id}`, `DELETE /schedules/{id}`.
- Sources: `POST /source-resolutions-v3` (body wrapped in `source`), poll `GET /source-resolutions-v3/{id}`.
- Visuals: `POST /videos/from-templates` (UUID templateId, `inputs:{}`+`prompt`), poll `GET /videos/creations/{id}`.
- Key handling: read from config, never echo; key may end in `=` (base64 padding) — preserve exactly.

## Out of scope (v1)

- Fully-automated/hands-off mode (Option B) — design allows it later; not built now.
- YouTube at 4 fresh videos/day from scratch.
- Analytics-driven optimization (the `/analytics` endpoints exist — a future "what's
  working" loop, not v1).
- Writing/owning voice (that's `write-content`); creating the lead magnet.

## Why it sticks

The failure mode of past attempts = daily manual effort. This batches a **week ahead**,
auto-schedules, auto-ramps, never repeats, and asks Brent for ~10 minutes once a week.
Posting then runs itself.
