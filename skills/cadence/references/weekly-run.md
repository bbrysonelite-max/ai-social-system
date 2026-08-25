# Weekly-Run Procedure

**Date:** 2026-06-17
**Source:** `docs/superpowers/specs/2026-06-17-cadence-system-design.md` (Architecture § Weekly-run procedure).

---

> **Scope of this file:** the ordered 8-step weekly batch procedure. Volume arithmetic and `state.json` rules are in `ramp-and-state.md`. Blotato REST endpoints and slot mechanics are in `slots-and-rest.md`. Drafting and voice are in `skills/write-content/SKILL.md`. Distribution tooling and the safety rubric are in `skills/blotato-post/SKILL.md`.

---

## Step 0 — Verify last week's posts published

Before drafting anything, confirm that the prior week's scheduled posts actually went out. This is the "Do, Then Share" proof loop.

### What to check

Read `state.json.scheduled`. For each entry where:
- `scheduledTime` is now in the **past** (before the current UTC time), AND
- `platform` is `facebook`, `instagram`, or `twitter`

Call:

```
GET /posts/{postSubmissionId}
```

(See `slots-and-rest.md` — Publishing & scheduling § Poll post status.)

### Classify each result

| Response | Classification | Action |
|---|---|---|
| Has `publicUrl` | **published** | Record the `publicUrl` |
| Has `errorMessage` | **failed** | Flag it — note the `errorMessage` and `platform` |
| Neither (status `in-progress`) | **in-progress** | Note it — may still be publishing |

**YouTube is a daily video channel** (1/day) — verify its prior posts too (`GET /posts/{id}`). YouTube videos are staged PRIVATE-first for Brent's review, so a "scheduled"/"private" status pending his approval is expected, not a failure.

### Present a verification summary

Before proceeding to Step 1, show Brent a short summary:

```
── Last-week verification ──────────────────────────────
Published:  <N>
Failed:     <N>  ← list each: [platform] errorMessage
In-progress: <N> ← may still be publishing
────────────────────────────────────────────────────────
```

### This step is read-only and non-blocking

Step 0 does **not** block drafting. If failures are found, surface them clearly so Brent can decide what to do (re-post manually, investigate, ignore), then proceed to Step 1. Do not attempt to re-post or retry failed posts automatically.

If `state.json.scheduled` is empty or has no past entries, note "No prior scheduled posts to verify" and proceed.

### Auto-offer to heal failures (non-blocking)

For any post classified **failed** in this step, offer — in the verification summary — to re-draft it into THIS week's batch (it flows through the normal gate like any other post, so nothing reposts without approval). Do not silently retry, and do not auto-`POST`. The point is that failures heal into the next batch instead of vanishing. A failed idea's slug stays in `usedIdeas`; re-drafting it is the one sanctioned recycle (note it explicitly to Brent).

---

## Step 0.5 — Learn from last week (engagement feedback loop)

Before choosing this week's ideas and times, read how last week actually performed and let the data shape Steps 3 and 6. Without this, every week is as blind as Week 1. **This step is read-only, best-effort, and non-blocking** — if analytics are unavailable it degrades to "no signal yet" and the batch proceeds on defaults.

### Pull engagement for last week's published posts

For each `state.json.scheduled` entry that Step 0 classified **published** (has a `publicUrl`), call:

```
GET /posts/{postSubmissionId}/analytics
```

(See `slots-and-rest.md` → Analytics.) Join each result back to its `ideaRef` (idea slug) and its `scheduledTime` hour + `platform`.

**If analytics endpoints 401/404 on Brent's plan** (likely — not yet live-verified): say so plainly, skip to "Apply the signal" with whatever is already in `state.json.performance` (possibly empty), and optionally ask Brent if he wants to hand-enter a few standout/dud posts. Never fabricate numbers; a missing readback is `unknown`, not `0`.

### Rank what worked

From whatever engagement data is available, compute two lightweight rankings:

1. **By theme/pillar** — group by `ideaRef` family (and, where known, the pillar from `write-content`); rank by an engagement proxy (e.g. `likes + 2×comments + shares + clicks`). Identify the top ~3 and bottom ~3.
2. **By send window** — group published posts by `(platform, hour-of-day UTC)`; rank by the same proxy. Identify the best 1–2 windows per platform.

Keep it simple and explainable — this is a nudge, not an optimizer. With fewer than ~5 published posts, note "insufficient signal" and treat rankings as provisional.

### Persist the signal

Write the rankings to `state.json.performance` (schema in `ramp-and-state.md`). This is a rolling, overwrite-latest field (NOT an append-only ledger) — it always reflects the most recent read.

### Apply the signal (downstream)

- **Step 3 (idea selection):** bias toward themes/pillars in the top ranking; deprioritize (don't ban) the bottom ones. Brent's editorial judgment at the gate still wins.
- **Step 6 (send times):** prefer the best-performing windows per platform instead of the static defaults.

### Present a one-line signal summary

Before Step 1, show Brent:

```
── Last-week signal ────────────────────────────────────
Top themes:   <slug-family> (<proxy>), …   |  insufficient signal if <5 posts
Best windows: FB 16:00Z · IG 22:00Z · X 15:00Z
Analytics:    live  (or: unavailable — using prior/no signal)
────────────────────────────────────────────────────────
```

If there is no signal at all (first run, or analytics unavailable and `performance` empty), print "No engagement signal yet — proceeding on defaults" and continue.

---

## Step 1 — Compute this week's volume

Read `state.json` (`skills/cadence/state.json`) and extract `startDate`.

Apply the arithmetic from `ramp-and-state.md`:

```
week             = floor((today - startDate) / 7) + 1
perDayPerChannel = min(week, 4)
```

The active channels for each day are **Facebook, Instagram, and X** (text+image, 1→4 ramp) **plus YouTube** (1 video/day, staged private-first — see the YouTube section below).

Total posts to draft this week:

```
total = perDayPerChannel × 3 channels × 7 days
```

Example — Week 2: `2 × 3 × 7 = 42` posts.

Confirm the figure before proceeding. If `startDate` is missing from `state.json`, stop and ask Brent to confirm the ramp start date — do not assume.

---

## Step 2 — Re-verify accounts

Account IDs change on reconnect. Always fetch live IDs at the start of every run.

```
GET /users/me/accounts
```

Map each platform (`facebook`, `instagram`, `twitter`) to its current `accountId`.

For **Facebook**: call `GET /users/me/accounts/{facebookAccountId}/subaccounts` and extract the `pageId` — prefer the known pageId `53954221244` if present in `items`, else fall back to `items[0].id`, else mark Facebook as **SKIP** for this run and surface:

> "Facebook has no Page connected in Blotato — connect a Page (dashboard: 'Facebook pages: Don't see your pages? Help') to enable FB posting."

If any expected platform is absent from the live response, log the skip and continue with the remaining channels.

See `slots-and-rest.md` (Auth + Accounts section) for the full endpoint contract and response shape.

---

## Step 3 — Pull fresh material (content supply)

Pick enough ideas to cover the week's full volume (Step 1 total), applying the **no-repeat guard**: before selecting any idea, confirm its slug is **not** already in `state.json.usedIdeas`. Skip any idea whose slug appears there.

**Bias by last week's signal (Step 0.5).** If `state.json.performance` has rankings, weight selection toward the top themes/pillars and lean away from the bottom ones. This is a nudge, not a filter — never repeat a used slug to chase a winning theme; instead pick a *fresh* idea in that theme's family. Brent's judgment at the gate overrides any ranking.

### Do, Then Share — content strategy

This is Sabrina Ramonov's "Do, Then Share" playbook applied to Brent's business. Prioritize real, earned material before reaching for the idea bank.

**Source priority (highest to lowest):**

1. **Brent's real receipts and journey this week** — things he actually did or learned: building Tiger, working his distribution network, team outcomes, process notes, screenshots, metrics. Document the journey even before big results land. A single concrete win → many posts. Anchor in Brent's 39-year network-marketing track record wherever credibility context helps — this is a rare, earned proof point that sets him apart.

2. **Repurposed cores** — feed a long-form source into Blotato's `POST /source-resolutions-v3` (the REST repurposing endpoint; same as `create_source` in the Blotato MCP), poll until `status: completed`, then extract the content. One strong core → atomize it into many platform posts. This is high leverage. See `slots-and-rest.md` (Sources & visuals section) for the endpoint contract; hand extracted content to `write-content` for voice-true drafting — the raw extraction is never Brent's voice.

   **Source priority within repurposed cores (highest first):**

   a. **Personal Obsidian vault** (`~/Desktop/vault-personal/`) — the PRIMARY and richest repurposing source. Contains:
      - **Three books** at `02_The_Library/Book_1`, `02_The_Library/Book_2`, `02_The_Library/Book_3` — feed chapters/sections via `create_source` (`POST /source-resolutions-v3`, `sourceType: text` or `pdf`) and repurpose each many ways.
      - **~354 notes / 1000+ ideas** across `01_Active_Projects`, `02_The_Library`, `03_The_Stream`, `04_The_Synthesizer` — a deep, effectively unlimited idea reservoir.
      The vault (books + ideas combined) is effectively unlimited supply; the binding constraint each week is good graphics, not content volume.

   b. **Webinar recording, YouTube scripts, written-up case studies, field stories** — strong evergreen cores; use whenever a recording or long-form piece should anchor the week.

   c. **The ~76-idea Desktop bank** (`~/Desktop/Social Media Posts: Ideas/`) — use for fill when vault and other cores do not cover the week's volume.

   The `usedIdeas` no-repeat guard applies across all sources — vault-derived slugs are tracked alongside idea-bank slugs.

3. **The idea bank** (`~/Desktop/Social Media Posts: Ideas/`) — final fill only (see 2c above).

**Do, Then Share principles to apply:**

- Lead with **proof and what was learned**, not generic AI filler. A real win first, then repurpose it many ways.
- Free education comes first; Tiger or the lead magnet is the CTA (not the lede).
- "Repurpose one win 20 ways" — a single result or story can cover an entire week across platforms if atomized correctly.
- Vary angles per platform: a stat becomes an IG visual, an insight becomes an X thread, a story becomes a Facebook post.

**No-repeat guard (exact + near-duplicate):** For every candidate idea or story, generate or confirm a slug (a short identifier, e.g. `"webinar-launch-june-17"` or `"tiger-rebuild-week-3"`). Reject a candidate if EITHER:
- its slug exactly matches an entry in `state.json.usedIdeas`, OR
- it is a **near-duplicate** of a used idea — same core claim/angle under a different slug (e.g. `clone-the-leader-x` vs `clone-your-leader`). Exact-slug matching alone is not enough; compare the *meaning*, not just the string. When two candidates are near-duplicates of each other within the same batch, keep one.

**Auto-replenish before stopping (do NOT dead-end on the Desktop bank).** The Desktop bank (`~/Desktop/Social Media Posts: Ideas/`, ~76 ideas) is *fill only* and will exhaust quickly at Week-3/4 volume. When it runs low or dry, pull fresh material automatically — in this order — before ever asking Brent for permission to recycle:

1. **Brent's real receipts this week** (source priority 1 above) — always first.
2. **The personal vault** (`~/Desktop/vault-personal/`) — the effectively-unlimited reservoir: the 3 books (`02_The_Library/Book_1..3`) and ~354 notes / 1000+ ideas across `01_Active_Projects`, `02_The_Library`, `03_The_Stream`, `04_The_Synthesizer`. Pull fresh angles here via `create_source` / direct read, slug each, and run them through the same no-repeat guard. **Prefer vault angles in last week's top-performing themes** (Step 0.5). This is the replenishment path — the bank exhausting is normal, not a stopping condition.

**Only stop and ask Brent** if (a) real receipts, the Desktop bank, AND the vault are all exhausted of non-duplicate ideas for the week's volume — which should be rare given the vault's size — or (b) a Step-0 *failed* post needs its used slug recycled (the one sanctioned recycle; flag it explicitly).

Collect the selected ideas with their slugs before proceeding to Step 4.

---

## Step 4 — Draft each post

Run the `write-content` skill (Skill 1) for each selected idea.

- Supply the idea, any supporting receipt/file, and the target platforms for that idea (FB, IG, X — or a subset if the idea fits fewer platforms).
- `write-content` handles: voice, pillar selection, CTA mode, per-platform format, and the 5-criterion self-review gate. All five criteria must pass before a draft is accepted.
- Do not mutate copy after `write-content` produces it. If copy must change for any reason, re-run `write-content`.
- `write-content` enforces cadence variety across a batch. If fewer than 3 distinct cadences appear in a batch of 3+ drafts, it will revise before showing output.

The `write-content` skill does not post, schedule, or generate images. Collect all approved drafts and pass them forward.

---

## Step 5 — Build visuals

**Posts are graphics-led.** Good images and carousels (Blotato Nano Banana templates + Brent's existing infographic library) carry most posts. Video is occasional — it is NOT required every post, so weekly volume does not demand a fresh video per slot. Use video only when footage or production value clearly warrants it.

For every **Instagram** post, generate a visual before scheduling. Instagram requires at least one image/video URL — caption-only posts are not supported via the API. An image is sufficient; video only when footage/value warrants.

For **Facebook** and **X**: text-only posts are valid. Visuals are optional but recommended for reach. Generate them when a visual adds clear value and templates are available.

### Visual generation procedure (per `slots-and-rest.md`)

1. Discover available templates: `GET /videos/templates` *(verify the visual path live before the first real IG batch — not yet smoke-tested)*
2. Generate: `POST /videos/from-templates` with `templateId` (bare UUID only — not the full path), a prompt describing the desired visual, and `"render": true`.
3. Poll: `GET /videos/creations/{id}` at 10-second intervals until `status` is `"done"`. This takes 30 seconds to 5 minutes — do not treat it as instant.
4. Collect the `mediaUrl` or `imageUrls` from the completed response. These are the values to pass in `content.mediaUrls` when creating the post.

If visual generation fails for an Instagram post, skip that post for this run and surface the reason. Do not block the rest of the batch.

---

## Step 6 — Assign send times (slots optional)

Compute explicit send times for every post and distribute them across the week's 7-day window.

### Primary path — explicit `scheduledTime` (use this)

> **Plan limitation (verified 2026-06-17):** `POST /schedule/slots` returns `Unauthorized` on Brent's current plan. Compute explicit ISO-8601 UTC `scheduledTime` values directly — do not rely on slots or `useNextFreeSlot`.

For each channel and each day, assign a send time by staggering posts at sensible hours. Example spread for `perDayPerChannel = 2`:

- Post 1: 14:00 UTC (morning in US-friendly zones)
- Post 2: 20:00 UTC (early evening)

**Prefer the best-performing windows from Step 0.5** (`state.json.performance.bestWindows`, per platform) over these static defaults whenever signal exists. The defaults above are the fallback for platforms/hours with no signal yet.

Adjust hours per channel character (e.g. FB/IG slightly earlier, X can go later). Spread posts for the same idea across different days — do not cluster all posts on day 1. **Enforce the stagger here:** two posts on the same platform on the same day must be ≥30 minutes apart (the safety rubric checks this at the gate — satisfy it now, don't leave it to fail later).

Assign one explicit `scheduledTime` (ISO-8601 UTC) to each post. These values are used directly in the Step 8 `POST /posts` calls at root level.

### Optional — `useNextFreeSlot` (only if plan supports slots)

If Brent's plan is upgraded and `POST /schedule/slots` no longer returns `Unauthorized`, you may instead:

1. Call `GET /schedule/slots` and count existing slots per channel per day.
2. Create any missing slots via `POST /schedule/slots` to reach Week N count (capped at 4). Do not duplicate same `hour`/`minute`/`day`/`selectedTargets`. Never delete existing slots.
3. Set `useNextFreeSlot: true` on each post (instead of `scheduledTime`). Do not combine both.

Until slot creation is confirmed working, use the explicit `scheduledTime` path above.

Record the intended scheduled time for each post — this is needed for the approval presentation in Step 7.

---

## Step 7 — Present batch + approval gate

Nothing is scheduled without Brent's explicit approval. **But do not dump 84 raw drafts on him** — at Week-3/4 volume a flat "read everything" list is a fiction nobody reads carefully, and the gate becomes a rubber stamp. Present **tiered (approve-by-exception)** so the human attention lands where it matters.

### Tiered presentation (approve-by-exception)

Split the batch into two tiers:

**Tier 1 — REVIEW IN FULL (show every field).** A post goes here if ANY of:
- it touches a compliance-sensitive line (income/earnings/health/company-endorsement adjacency — anything `write-content`'s `never-say.md` flags as borderline),
- it introduces a **new or untested theme/angle** (not in last week's `performance` top set, or a brand-new claim),
- it carries an unusual CTA or links somewhere other than the standard lead magnet / `stan.store/brentbryson`,
- its rubric scored anything other than a clean PASS on criteria 2–5,
- it's a YouTube video (always full-review — it's Brent's face).

For each Tier-1 post show the full detail: **platform + live `accountId`, exact text (character-for-character), visual URL/preview, scheduled time (ISO-8601 UTC), idea slug.**

**Tier 2 — APPROVE-BY-EXCEPTION (collapsed table).** Everything else — routine, on-pattern, clean-rubric posts in proven themes. Show one scannable row per post:

| # | Platform | Time (UTC) | Idea slug | First ~12 words of text | Visual |
|---|---|---|---|---|---|
| 1 | Facebook | 2026-06-24T16:00Z | followup-fortune | "The fortune isn't in the sale. It's in the follow…" | ✅ img |

Tell Brent explicitly: **"Tier 1 needs your eyes. Tier 2 is routine — say 'expand 7' to see any row in full, or approve them as a block."** Any Tier-2 row is expandable to full detail on request.

### Rubric (applies to BOTH tiers)

Run the `blotato-post` safety rubric — criteria 2–5 now; criterion 1 (Human-approved) is PENDING until Brent approves. Print one rubric line per **Tier-1** post (full), and a single **batch rubric summary** for Tier 2 (e.g. "Tier 2: 38 posts, all Account-valid ✅ / Voice ✅ / Warm-up ✅ / Media-valid ✅"):

```
[Platform] [AccountId] — Human-approved: PENDING | Account-valid: PASS | Voice/compliance: PASS | Warm-up: PASS | Media-valid: PASS
```

Any criterion at FAIL: the post drops to a FAIL list (skipped), never into Tier 2's clean block. A FAIL is never hidden by collapsing.

### Skip handling

- **Facebook with no Page:** skip cleanly with the message from Step 2.
- **Any platform missing required fields** (IG missing `mediaUrl`): skip with a specific message. Do not block the rest of the batch.
- List all skipped posts in a SKIPPED section below the gate.

### The approval gate

**Wait for Brent's explicit approval.** "Yes," "approved," "go," or equivalent. Silence or "looks good" without a clear affirmative is not approval. If Brent requests a change, do not call `POST /posts` — revise and re-present.

**If unsure whether a post is over a line, ask Brent — he decides.**

---

## Step 8 — Schedule + update state

On Brent's explicit approval:

### Schedule each approved post

For each approved post, call `POST /posts` with:
- All assembled fields (accountId, content.text, content.platform, target.targetType, platform-specific required fields)
- `scheduledTime` (ISO-8601 UTC) at root level — **not** nested inside `post` (see `slots-and-rest.md` common mistakes)
- Or `useNextFreeSlot: true` if slot-based assignment was chosen in Step 6

### Confirm scheduling

After each `POST /posts`, call `GET /schedules` and verify the post appears with the correct time and platform. Do not claim a post is scheduled without confirmation from `GET /schedules`.

### Update state.json

After all `POST /posts` calls succeed:

1. **Append to `usedIdeas`** — add the slug of every idea used in this batch. Check before appending; do not add duplicates.
2. **Append to `scheduled`** — add one entry per submitted post:

```json
{
  "postSubmissionId": "<UUID returned by POST /posts>",
  "platform": "<platform string>",
  "scheduledTime": "<ISO-8601 UTC>",
  "ideaRef": "<idea slug>"
}
```

3. Do not touch `startDate` — it is set once at initialization and never changed.
4. `usedIdeas` and `scheduled` are append-only ledgers. Never remove entries.

### YouTube — daily video channel (1/day, PRIVATE-first)

YouTube is a **daily** channel: 1 video/day, account `27755`, channel `@BrentBrysonaios` (verified live 2026-06-19). Each post needs a **video** at a public URL — Blotato has no raw local-file upload. Don't hand-build the call; use the autoload script:

```
skills/cadence/scripts/youtube-autoload.sh \
  --video <PUBLIC_URL> --title "…" --desc-file <path> [--schedule <ISO-UTC>]
```

It runs `POST /v2/media` (host the video) → `POST /posts` (youtube target, `privacyStatus: private` by default) → polls and returns the YouTube URL. The video stays **PRIVATE** until Brent reviews it in his morning queue and flips it Public (or it auto-publishes if `--schedule` was used). **Never publish a YouTube video straight to Public — private-first, always.** Video copy convention: front edification hook + tasteful subscribe/like (front AND back) + email CTA → `stan.store/brentbryson`. YouTube also remains valid as a `create_source` input for repurposing.

#### HeyGen video — Brent supplies the clip, Claude does NOT generate

🚫 **DO NOT generate clones via API/CLI/Video-Agent.** Settled 2026-06-19 after a
full day of failed renders — every automated attempt (incl. HeyGen's own Video
Agent) was rejected; the looks Claude picked were the bad ones. **Brent makes the
clone himself in the HeyGen GUI** (Avatar IV / Seedance — the only quality he
accepts). Good clips live in his Projects **"Brent Clone"** folder.

**Handoff (downstream only):**
1. Brent names a finished clip (HeyGen video ID).
2. `heygen video get <id>` → `.data.video_url`.
3. Post **AS-IS, full-width 16:9** — **NEVER crop to vertical 9:16** (Brent prefers
   horizontal; 9:16 only if explicitly a Short) — via
   `youtube-autoload.sh --video <url> --title "…" --desc-file <path>` (PRIVATE
   default; `--schedule` to stage). Add title + `stan.store/brentbryson` link.
4. Brent reviews Private → flips Public (or auto on schedule).

Canonical clone going forward: his **blue-polo Avatar IV** look. (HeyGen key in
`~/Desktop/GitSync/kloop.env`; `sk_V2_hgu_` trial keys expire — see [[project-blotato-social-posting]].)

### Completion summary

Present a summary table of what was scheduled and what was skipped, populated from live `GET /schedules` confirmation values — not from the `POST /posts` response alone.

| Platform | Account ID | Scheduled time (UTC) | Post ID | Status |
|---|---|---|---|---|
| Facebook | … | … | … | Scheduled / SKIPPED |
| Instagram | … | … | … | Scheduled / SKIPPED |
| X | … | … | … | Scheduled / SKIPPED |
| YouTube | 27755 | … | … | PRIVATE — staged for review (or Scheduled) |
