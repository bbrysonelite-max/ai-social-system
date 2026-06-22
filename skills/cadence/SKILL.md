---
name: cadence
description: >-
  Weekly-batch content cadence system. Use when Brent says "run the weekly
  batch", "run cadence", "build this week's posts", "schedule the week", or
  "do my content for the week". Drafts and schedules a full week of posts at the
  current ramp volume (1→4/day/channel, auto-advancing by calendar week) across
  Facebook, Instagram, and X (text+image), plus YouTube as a daily video channel
  (auto-uploaded PRIVATE-first via scripts/youtube-autoload.sh, for Brent's review), behind a mandatory
  human approval gate. NEVER posts or schedules without Brent's explicit
  approval. NEVER repeats an idea already in the usedIdeas ledger.
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
Blotato. Each run first verifies that the prior week's scheduled posts actually
published (the "Do, Then Share" proof loop), then reads how they performed and
ranks the winning themes + send windows (the feedback loop), before drafting
anything new. Then it reads the current ramp volume from `state.json`, selects
enough fresh ideas (no exact or near-duplicate repeats, biased toward what
worked, auto-replenished from the vault) to cover the week's total, runs each
idea through `write-content` for voice-true drafts, generates required visuals
for Instagram, assembles every post with the correct Blotato fields, presents
the batch tiered for a single approve-by-exception review, and — only after
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

### Execute the 9-step procedure (Step 0 first)

`references/weekly-run.md` is the authoritative procedure. Execute its steps
in order, beginning with Step 0:

| Step | Name | What happens |
|---|---|---|
| 0 | Verify last week published | GET /posts/{id} for past FB/IG/X scheduled entries; report published/failed/pending to Brent before drafting; offer to heal failures into this batch (still gated). |
| 0.5 | Learn from last week | Read engagement (`GET /posts/{id}/analytics`) for last week's published posts; rank top/bottom themes + best send windows into `state.json.performance`. Read-only, best-effort — degrades to "no signal" if analytics unavailable. Feeds Steps 3 + 6. |
| 1 | Compute this week's volume | Read `startDate` from `state.json`; apply `week = floor((today - startDate) / 7) + 1`; `perDayPerChannel = min(week, 4)`. If `startDate` is missing, stop and ask Brent. |
| 2 | Re-verify accounts | `GET /users/me/accounts`; map platform → live `accountId`. Fetch `pageId` from FB subaccounts; mark FB SKIP if no Page found. |
| 3 | Pull fresh material | Apply "Do, Then Share" source priority; bias toward Step-0.5 top themes; no-repeat guard (exact + near-duplicate) against `usedIdeas`; auto-replenish from the vault before stopping; only ask Brent if receipts + bank + vault are all exhausted. |
| 4 | Draft each post | Run `write-content` skill per idea; accept only drafts that pass all 5 criteria; never mutate copy. |
| 5 | Build visuals | Generate visuals for every IG post (required); optional for FB/X; skip IG post cleanly if generation fails. |
| 6 | Assign send times (slots optional) | Compute explicit ISO-8601 UTC `scheduledTime` for each post spread across the week; prefer Step-0.5 `bestWindows`; enforce ≥30-min same-platform same-day stagger (slots/`useNextFreeSlot` are plan-gated, Unauthorized on Brent's plan). |
| 7 | Present batch + approval gate | Tiered (approve-by-exception): Tier 1 (sensitive/new/YouTube) shown in full; Tier 2 (routine, clean-rubric) as a collapsed scannable table; run rubric criteria 2–5; wait for explicit approval (see Approval gate below). |
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

**Present tiered (approve-by-exception) — do NOT dump 84 raw drafts.** At Week-3/4
volume a flat "read everything" list is a rubber stamp. Split the batch:

- **Tier 1 — review in full:** any post that is compliance-sensitive, a new/untested
  theme, an unusual CTA/link, scored anything but a clean rubric PASS, or is a
  YouTube video. Show every field + its own rubric line.
- **Tier 2 — approve-by-exception:** routine, on-pattern, clean-rubric posts in
  proven themes. Show a collapsed scannable table (#, platform, time, slug, first
  ~12 words, visual ✅) + one batch rubric summary line. Brent can say "expand N"
  to see any row in full, or approve the block.

A rubric FAIL is never hidden inside the Tier-2 block — it always goes to the
skipped/FAIL list. See `references/weekly-run.md` Step 7 for the full tiering rules.

**Skip rules:**
- Facebook with no connected Page → skip FB for this run; show the message:
  "Facebook has no Page connected in Blotato — connect a Page (dashboard:
  'Facebook pages: Don't see your pages? Help') to enable FB posting."
- Any platform missing a required field (IG without `mediaUrl`) → skip that
  post; show a specific message. Do not block the rest of the batch.

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
| YouTube | {live accountId} | {publish/schedule time} | {UUID} | {slug} | PRIVATE — staged for review (or Scheduled) |

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
  `usedIdeas` (exact + near-duplicate) before drafting; the ledger is append-only
  and persists across sessions. When the Desktop bank runs low the run
  auto-replenishes from the vault rather than stopping.
- **Feedback loop is automatic** — Step 0.5 reads last week's engagement and
  ranks themes + send windows into `state.json.performance`, which biases idea
  selection (Step 3) and send times (Step 6). Best-effort: degrades cleanly if
  analytics are unavailable on Brent's plan; never fabricates numbers.
- **Send times computed explicitly** — Step 6 assigns explicit ISO-8601 UTC `scheduledTime` values spread across the week's days per channel (primary path). Slot self-provisioning is optional — currently plan-gated (`POST /schedule/slots` returns Unauthorized on Brent's plan).
- **State persists** — `state.json` is updated immediately after every approved
  batch; the next run picks up exactly where this one left off.
- **Weekly trigger** — run `/cadence` at the start of each content week to keep
  the factory running; optionally set a `/schedule` reminder to trigger it
  automatically.

---

## YouTube — video channel (Brent supplies the clip)

YouTube is a video channel (`@BrentBrysonaios`, Blotato account `27755`).

🚫 **DO NOT auto-generate clones.** Settled 2026-06-19 after a full day of
failed attempts: every API/Video-Agent render (incl. HeyGen's own flagship) was
rejected. **Claude does NOT make the video.** Brent makes his clone himself in
the HeyGen GUI (Avatar IV / Seedance — the only quality he accepts); the good
clips live in his Projects **"Brent Clone"** folder. Claude's job is **downstream
only**.

**The working handoff:**
1. Brent points to a finished clip (a HeyGen video ID, or says which one).
2. Fetch its `video_url` (`heygen video get <id>` → `.data.video_url`).
3. Post it **AS-IS, full-width 16:9** (his preferred direction — NEVER crop to
   vertical 9:16; he rejects narrow-tall. 9:16 only if the piece is explicitly a
   Short) via `scripts/youtube-autoload.sh --video <url> --title "…" --desc-file <path>`
   (defaults PRIVATE; `--schedule <ISO-UTC>` to stage). Add title + the
   `stan.store/brentbryson` free-guide link in the description.
4. Brent reviews Private, flips Public when happy (or it auto-publishes if scheduled).

One canonical clone going forward: his **blue-polo Avatar IV** look. See
[[project-blotato-social-posting]] for the full settled model.

---

## Out of scope

- **No hands-off / auto-post mode** — Option B (fully autonomous scheduling
  without a weekly approval) is not built yet. The gate is mandatory.
- **No voice authorship** — `cadence` does not draft copy or select cadences.
  That is `write-content`'s domain. `cadence` passes ideas to `write-content`
  and accepts its output character-for-character.
- **No deep analytics optimization** — Step 0.5 adds a lightweight engagement
  feedback loop (top/bottom themes + best send windows) that *nudges* idea
  selection and timing. It is a ranking signal, not a full optimizer: no A/B
  testing, no automated copy tuning, and rankings never override Brent's gate
  judgment. Also gated on Blotato exposing analytics on his plan (not yet
  live-verified).
