# Cadence System (Skill 3 `cadence`) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. **Three-agent rule: author / test / review by separate agents.** Steps use checkbox (`- [ ]`) syntax.

**Goal:** Build the `cadence` Claude skill (Skill 3) — a durable, approve-first weekly-batch system that drafts (via `write-content`), builds visuals, and schedules a full week of posts across Brent's channels at a ramping volume (1→4/day/channel over 4 weeks), via the Blotato REST API.

**Architecture:** A `SKILL.md` orchestration file + reference files + a seed `state.json`. Markdown-instruction skill (no app code), consistent with `write-content` and `blotato-post`. It sequences the two existing skills + Blotato REST; it does not re-implement voice or drafting. Verification is rubric-based + one warm-up-safe live check (schedule-then-delete; never over-posts).

**Tech Stack:** Markdown + Blotato REST API (`https://backend.blotato.com/v2`, header `blotato-api-key`). No build, no deps.

## Global Constraints

(Copied verbatim from the spec — every task implicitly includes these.)

- **The ramp (locked):** Wk1 1/day/channel → Wk2 2 → Wk3 3 → Wk4+ 4; 4 channels (FB, IG, X full; YouTube best-effort); 7 days/week. Volume auto-steps by calendar week from a fixed `startDate`.
- **Approve-first (Option A):** the weekly run presents the FULL batch (text + visuals + send times) and schedules NOTHING without Brent's explicit approval. Design must not preclude a later hands-off mode (Option B), but do not build B.
- **Distribution discipline:** never mutate `write-content` voice; reuse `blotato-post`'s safety rubric for the gate; FB skips cleanly if no Page; never repeat a used idea.
- **Channels:** FB needs `target.pageId` (Page `53954221244`, re-verify at runtime via `/users/me/accounts/{id}/subaccounts`); IG generates a visual every post (`mediaType` reel/story); X text/threads; YouTube = video upload, **best-effort from repurposed footage, NOT 4 fresh/day**.
- **Blotato REST:** base `https://backend.blotato.com/v2`, header `blotato-api-key` read from `~/.claude.json` (never echoed; key may end in `=`, preserve exactly). Scheduling fields (`scheduledTime`/`useNextFreeSlot`) are ROOT-LEVEL siblings of `post`, never nested. Always `GET /users/me/accounts` first (IDs change on reconnect).

## Verification approach

No unit tests (markdown skill). Each task verifies by re-reading against its brief + the spec. The final task does ONE warm-up-safe live check: create 1 schedule slot + schedule 1 post into it, confirm via `GET /schedules`, then DELETE it — never leaves an unintended live/scheduled post.

## File Structure

```
skills/cadence/
├── SKILL.md                        # orchestration: triggers, the weekly run, approval gate, output, durability
├── state.json                      # seed: startDate, usedIdeas[], scheduled[]
└── references/
    ├── ramp-and-state.md           # ramp table, week→volume computation, state.json schema + update rules, used-ideas ledger
    ├── slots-and-rest.md           # Blotato REST contract (accounts/subaccounts/posts/schedules/slots/sources/visuals); slot backbone + how to ramp slots; per-channel required fields; key handling
    └── weekly-run.md               # the step-by-step weekly procedure (compute → supply → draft → visuals → assign → present → approve → schedule → update state)
```

---

### Task 1: Ramp + state reference (`references/ramp-and-state.md`) and seed `state.json`

**Files:**
- Create: `skills/cadence/references/ramp-and-state.md`
- Create: `skills/cadence/state.json`

**Interfaces:**
- Produces: `ramp-and-state.md` (sections `## The ramp`, `## Computing the current week's volume`, `## state.json schema`, `## Update rules`) and a valid seed `state.json`.

- [ ] **Step 1: Write `ramp-and-state.md`.** `## The ramp`: the locked table (Wk1 1 → Wk4+ 4 per day per channel; FB/IG/X full, YT best-effort; 7 days/wk). `## Computing the current week's volume`: weeks elapsed since `startDate` (floor) → week 1..4+, capped at 4/day/channel; give the exact arithmetic (e.g., `week = floor((today - startDate)/7) + 1`, `perDay = min(week, 4)`). `## state.json schema`: fields `startDate` (ISO date), `usedIdeas` (array of idea IDs/slugs already posted), `scheduled` (array of `{postSubmissionId, platform, scheduledTime, ideaRef}`). `## Update rules`: after a batch schedules, append used idea slugs to `usedIdeas` and entries to `scheduled`; the ledger is the no-repeat guard.
- [ ] **Step 2: Write seed `state.json`** with `startDate` = `"2026-06-17"`, `usedIdeas` = the slugs already posted this session (`["clone-the-leader-x","right-five-things-x","lead-the-moving-x"]` — the live tweet + 2 scheduled), `scheduled` = the 3 known posts (X live + 2 scheduled, with their postSubmissionIds `1af29dd8-...`, `cf299378-...`, `59e36aa0-...`). Valid JSON.
- [ ] **Step 3: Verify** the week arithmetic example matches the table and `state.json` parses (`jq . state.json`).
- [ ] **Step 4: Commit.** `git add skills/cadence/references/ramp-and-state.md skills/cadence/state.json && git commit -m "feat(cadence): ramp + state reference and seed state.json"`

---

### Task 2: Slots + REST reference (`references/slots-and-rest.md`)

**Files:**
- Create: `skills/cadence/references/slots-and-rest.md`
- Source (verbatim): the Blotato API reference pasted by Brent 2026-06-17 (base, endpoints, payloads, common mistakes).

**Interfaces:**
- Produces: `slots-and-rest.md` (sections `## Auth + key handling`, `## Accounts (always first)`, `## Schedule slots (the cadence backbone)`, `## Publishing & scheduling`, `## Sources & visuals`, `## Per-channel required fields`, `## Common mistakes`).

- [ ] **Step 1: Write the file** with the verbatim REST contract: base `https://backend.blotato.com/v2`, header `blotato-api-key` (read from `~/.claude.json` at `.mcpServers.blotato.headers["blotato-api-key"]`, never echo, preserve trailing `=`). `GET /users/me/accounts` + `/users/me/accounts/{id}/subaccounts` (FB pageId, YT playlists). Slots: `GET/POST /schedule/slots` (fields hour/minute/day/selectedTargets), `POST /schedule/slots/next-available`; how to RAMP — Wk N has N slots/day/channel; add slots when the week advances; never duplicate a slot. Publishing: `POST /posts` with `post:{accountId,content:{text,mediaUrls,platform[,additionalPosts]},target:{targetType,...}}` and **root-level** `scheduledTime` or `useNextFreeSlot`; poll `GET /posts/{id}`. Schedules: `GET /schedules`, `DELETE /schedules/{id}`. Sources: `POST /source-resolutions-v3` (body wrapped in `source:{sourceType,url|text}`), poll. Visuals: `POST /videos/from-templates` (UUID templateId, `inputs:{}`+`prompt`), poll `GET /videos/creations/{id}`. `## Per-channel required fields`: twitter (none), facebook (`target.pageId` REQUIRED), instagram (`mediaType` reel/story + a media URL), youtube (`title`+`privacyStatus`+`shouldNotifySubscribers`, video media). `## Common mistakes`: nested scheduling fields; missing FB pageId; platform/targetType mismatch; full-path templateId.
- [ ] **Step 2: Verify** every endpoint + the "scheduling fields are root-level" rule + per-channel required fields are present and match the API reference.
- [ ] **Step 3: Commit.** `git commit -m "feat(cadence): Blotato slots + REST reference"`

---

### Task 3: Weekly-run reference (`references/weekly-run.md`)

**Files:**
- Create: `skills/cadence/references/weekly-run.md`

**Interfaces:**
- Consumes: `ramp-and-state.md`, `slots-and-rest.md`, plus the `write-content` and `blotato-post` skills.
- Produces: `weekly-run.md` (`## Step 1 Compute volume` … `## Step 8 Update state`), the ordered procedure.

- [ ] **Step 1: Write the procedure.** (1) Compute this week's volume from `ramp-and-state.md`. (2) Re-verify accounts via `GET /users/me/accounts` (+FB subaccounts). (3) Pull fresh material: from the idea bank (`~/Desktop/Social Media Posts: Ideas/`) and/or repurpose a core via `create_source`, **skipping any idea slug already in `state.json.usedIdeas`**; pick enough for the week (volume × 7 × channels, FB/IG/X). (4) Draft each via the `write-content` skill (voice + variety guard). (5) For each IG post, generate a visual (`/videos/from-templates`) and poll to `done`. (6) Ensure slots for this week's volume exist (`/schedule/slots`); assign posts to days/slots. (7) Present the FULL batch (per-platform text + visual link + scheduled time) and STOP for explicit approval (reuse `blotato-post` safety rubric; skip FB if no Page). (8) On approval, `POST /posts` with `scheduledTime` per assignment; confirm via `GET /schedules`; append slugs to `usedIdeas` and entries to `scheduled` in `state.json`. Note YouTube is best-effort (only if repurposed footage is available).
- [ ] **Step 2: Verify** all 8 steps present, the no-repeat check references `usedIdeas`, the approval gate precedes any `POST /posts`, and YT best-effort is stated.
- [ ] **Step 3: Commit.** `git commit -m "feat(cadence): weekly-run procedure reference"`

---

### Task 4: SKILL.md orchestration

**Files:**
- Create: `skills/cadence/SKILL.md`

**Interfaces:**
- Consumes: all three references + `state.json`.
- Produces: an invokable skill.

- [ ] **Step 1: Frontmatter** — `name: cadence`; `description:` triggering on "run the weekly batch", "run cadence", "build this week's posts", "schedule the week"; states it drafts+schedules a full week at the current ramp volume across FB/IG/X (+YT best-effort) behind an approval gate, never posts without approval, never repeats.
- [ ] **Step 2: Body** — `## What it does` (one-paragraph summary); `## Inputs` (optional: target week override, a specific core URL to repurpose, dry-run flag); `## Process` (load the 3 references + state.json, then run `weekly-run.md`'s 8 steps); `## Approval gate` (reproduce/point to the safety rubric; full-batch view; explicit approval required); `## Output` (table of scheduled posts: platform / time / idea / status, + skipped + why; never claim scheduled without `GET /schedules` confirmation); `## Durability` (a weekly `/schedule` reminder triggers this; state + ramp auto-advance); `## Out of scope` (no hands-off mode, no YT 4-fresh/day, no voice authorship).
- [ ] **Step 3: Verify** the skill loads all references + state, the gate precedes scheduling, triggers are present, no placeholder text.
- [ ] **Step 4: Commit.** `git commit -m "feat(cadence): SKILL.md orchestration"`

---

### Task 5: Warm-up-safe live check + slot bootstrap

**Files:** No new skill files (validation). May create the Week-1 slots.

> **Safety:** never leaves an unintended scheduled/live post. Schedule-then-delete only.

- [ ] **Step 1: Accounts** — `GET /users/me/accounts` + FB subaccounts; confirm the 4 channels + FB pageId; key read from config, not printed.
- [ ] **Step 2: Slot bootstrap (Week 1 = 1/day/channel)** — create one daily slot per channel for FB/IG/X via `POST /schedule/slots` (e.g., a sensible daily hour each). Confirm via `GET /schedule/slots`.
- [ ] **Step 3: Safe schedule check** — schedule ONE test post into a slot (X, far-future `scheduledTime`), confirm in `GET /schedules`, then `DELETE /schedules/{id}`; confirm gone. Nothing publishes.
- [ ] **Step 4: Tune + commit** any fixes. `git commit -m "feat(cadence): live slot bootstrap + schedule safety check"`

---

## Verification (whole feature)

- `cadence` runs the 8-step weekly procedure, computes the right ramp volume, pulls only unused ideas, drafts via `write-content`, builds IG visuals, and STOPS at the approval gate before scheduling.
- On approval it schedules via Blotato REST and confirms via `GET /schedules`; state ledger updates so nothing repeats.
- Slots exist for the current week; FB skips cleanly without a Page; YT is best-effort.
- The live check schedules-then-deletes without leaving anything live.

## Out of scope (explicitly)

- Hands-off mode (Option B), YT 4-fresh-videos/day, analytics-driven optimization, voice authorship (that's `write-content`), lead-magnet creation.
