---
name: cadence
description: >-
  Weekly-batch content cadence system. Use when Brent says "run the weekly
  batch", "run cadence", "build this week's posts", "schedule the week", or
  "do my content for the week". Drafts and schedules a full week of posts at the
  current ramp volume (1→4/day/channel, auto-advancing by calendar week) across
  Facebook, Instagram, and X (+ YouTube best-effort) behind a mandatory human
  approval gate. NEVER posts or schedules without Brent's explicit approval.
  NEVER repeats an idea already in the usedIdeas ledger.
---

# cadence (Skill 3)

The weekly-batch orchestration layer. One ~10-minute approval session per week
covers the full factory run: Sabrina's "Do, Then Share" playbook applied to
Brent's real receipts, at a volume that ramps automatically, distributed across
all connected channels via `write-content` (drafting) + Blotato (publishing).

**Voice and drafting stay in `write-content`. Distribution and scheduling stay
in `blotato-post`. This skill orchestrates both — it never rewrites copy.**

---

## What it does

`cadence` is the durable weekly-batch layer that sits above `write-content` and
Blotato. Each week it reads the current ramp volume from `state.json`, selects
enough fresh ideas (no repeats, no ideas already in `usedIdeas`) to cover the
week's total, runs each idea through `write-content` for voice-true drafts,
generates required visuals for Instagram, assembles every post with the correct
Blotato fields, presents the full batch for a single approval, and — only after
explicit approval — schedules every post via `POST /posts`, confirms each via
`GET /schedules`, and updates `state.json`. The ramp and no-repeat ledger
advance automatically; the only recurring human action is the ~10-minute
weekly review-and-approve.

---

## Inputs

**Required (computed automatically):**
- Current week number and per-day-per-channel volume — derived from
  `state.json.startDate` and today's date per `ramp-and-state.md`. No manual
  input needed.

**Optional overrides:**
- **Target week override** — `week=<N>` forces a specific ramp week (e.g.
  `week=2` to re-run the Week 2 volume). Use only when correcting a mismatch.
- **Core URL or file to repurpose** — a YouTube URL, article URL, PDF path, or
  raw text block to treat as the batch's primary source. Passed to Blotato's
  repurposing endpoint (`POST /source-resolutions-v3`) and then to
  `write-content`. Useful when a webinar recording or long-form piece should
  anchor the week.
- **`--dry-run`** — runs Steps 1–7 and shows the full batch at the gate but
  submits nothing (no `POST /posts`, no state update). The approval gate still
  runs so Brent can review; no `GET /schedules` confirmation appears because
  nothing is scheduled.

**Defaults:** compute week from `state.json.startDate`; no specific core;
live scheduling on approval.

---

## Process

### Load building blocks first

Before any computation, read all four source files:

1. `skills/cadence/references/ramp-and-state.md` — ramp table, week
   arithmetic, `state.json` schema, and update rules.
2. `skills/cadence/references/slots-and-rest.md` — Blotato REST base URL,
   auth, account/subaccount endpoints, slot management, `POST /posts` field
   contract, sources/visuals, per-channel required fields, common mistakes.
3. `skills/cadence/references/weekly-run.md` — the authoritative 8-step
   weekly procedure.
4. `skills/cadence/state.json` — live `startDate`, `usedIdeas` ledger, and
   `scheduled` history.

Read the Blotato API key from `~/.claude.json` at path
`.mcpServers.blotato.headers["blotato-api-key"]`. Never echo or print it.

### Execute the 8-step procedure

`references/weekly-run.md` is the authoritative procedure. Execute its 8 steps
in order:

| Step | Name | What happens |
|---|---|---|
| 1 | Compute this week's volume | Read `startDate` from `state.json`; apply `week = floor((today - startDate) / 7) + 1`; `perDayPerChannel = min(week, 4)`. If `startDate` is missing, stop and ask Brent. |
| 2 | Re-verify accounts | `GET /users/me/accounts`; map platform → live `accountId`. Fetch `pageId` from FB subaccounts; mark FB SKIP if no Page found. |
| 3 | Pull fresh material | Apply "Do, Then Share" source priority; enforce no-repeat guard against `usedIdeas`; if idea bank exhausted stop and ask Brent. |
| 4 | Draft each post | Run `write-content` skill per idea; accept only drafts that pass all 5 criteria; never mutate copy. |
| 5 | Build visuals | Generate visuals for every IG post (required); optional for FB/X; skip IG post cleanly if generation fails. |
| 6 | Assign send times (slots optional) | Compute explicit ISO-8601 UTC `scheduledTime` for each post spread across the week (primary path — slots/`useNextFreeSlot` are plan-gated and currently return Unauthorized on Brent's plan). |
| 7 | Present batch + approval gate | Show full batch; run rubric criteria 2–5; wait for explicit approval (see Approval gate below). |
| 8 | Schedule + update state | On approval: `POST /posts`; confirm via `GET /schedules`; append `usedIdeas` + `scheduled` entries to `state.json`. |

See `references/weekly-run.md` for the full per-step detail including
endpoint contracts, slot arithmetic, visual poll intervals, and state-update
rules. All step details are authoritative there; do not substitute from memory.

---

## Approval gate

**Nothing is scheduled (`POST /posts`) without Brent's explicit approval.
No exceptions. No batch size, time pressure, or "just do it" instruction
bypasses this gate.**

Before presenting, run the `blotato-post` safety rubric (criteria 2–5) on
every post. Criterion 1 (Human-approved) is PENDING until Brent approves:

```
[Platform] [AccountId] — Human-approved: PENDING | Account-valid: PASS | Voice/compliance: PASS | Warm-up: PASS | Media-valid: PASS
```

Any criterion at FAIL: skip that post with a clear reason. Do not include
failed posts in the approval prompt.

**Skip rules:**
- Facebook with no connected Page → skip FB for this run; show the message:
  "Facebook has no Page connected in Blotato — connect a Page (dashboard:
  'Facebook pages: Don't see your pages? Help') to enable FB posting."
- Any platform missing a required field (IG without `mediaUrl`, YT without
  `title`) → skip that post; show a specific message. Do not block the rest
  of the batch.

**Wait for Brent's explicit approval.** "Yes," "approved," "go," or an
equivalent affirmative. Silence or "looks good" without a clear approval word
is NOT approval. If Brent requests a change, do not call `POST /posts` — revise
and re-present.

**If unsure whether a post is over a line, ask Brent — he decides.**

All scheduling defaults to `scheduledTime` (ISO-8601 UTC) set at root level —
never nested inside `post`. Never schedule immediately unless Brent explicitly
says "post now."

---

## Output

After all `POST /posts` calls succeed and `GET /schedules` confirms each post,
present a summary table populated from live `GET /schedules` values — not
inferred from `POST /posts` responses alone:

| Platform | Account ID | Scheduled time (UTC) | Post ID | Idea slug | Status |
|---|---|---|---|---|---|
| Facebook | {live accountId} | {ISO-8601 UTC from GET /schedules} | {UUID from POST /posts, confirmed via GET /schedules} | {slug} | Scheduled |
| Instagram | {live accountId} | {ISO-8601 UTC from GET /schedules} | {UUID from POST /posts, confirmed via GET /schedules} | {slug} | Scheduled |
| X | {live accountId} | {ISO-8601 UTC from GET /schedules} | {UUID from POST /posts, confirmed via GET /schedules} | {slug} | Scheduled |
| YouTube | {live accountId} | {ISO-8601 UTC from GET /schedules} | {UUID from POST /posts, confirmed via GET /schedules} | {slug} | Scheduled / SKIPPED (no footage) |

Follow with a SKIPPED section listing every post that was not scheduled, the
platform, and the specific reason (no Page, missing required field, media
failure, rubric FAIL).

**Never claim a post is scheduled or live without confirmation from
`GET /schedules`.**

---

## Durability

The only recurring human action is the ~10-minute weekly approval. Everything
else is automatic:

- **Ramp advances automatically** — `week` is computed fresh each run from
  `state.json.startDate`; no manual volume input needed.
- **No-repeat guard is automatic** — every idea slug is checked against
  `usedIdeas` before drafting; the ledger is append-only and persists across
  sessions.
- **Send times computed explicitly** — Step 6 assigns explicit ISO-8601 UTC `scheduledTime` values spread across the week's days per channel (primary path). Slot self-provisioning is optional — currently plan-gated (`POST /schedule/slots` returns Unauthorized on Brent's plan).
- **State persists** — `state.json` is updated immediately after every approved
  batch; the next run picks up exactly where this one left off.
- **Weekly trigger** — run `/cadence` at the start of each content week to keep
  the factory running; optionally set a `/schedule` reminder to trigger it
  automatically.

---

## Out of scope

- **No hands-off / auto-post mode** — Option B (fully autonomous scheduling
  without a weekly approval) is not built yet. The gate is mandatory.
- **No YouTube 4-fresh-videos/day** — YouTube is best-effort repurposed footage
  only. This skill does not generate 4 original videos per day for YouTube.
- **No voice authorship** — `cadence` does not draft copy or select cadences.
  That is `write-content`'s domain. `cadence` passes ideas to `write-content`
  and accepts its output character-for-character.
- **No analytics optimization** — post-performance data does not feed back into
  scheduling or idea selection in this version.
