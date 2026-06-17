# blotato-post Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. **Three-agent rule applies: author / test / review by separate agents.**

**Goal:** Build the `blotato-post` Claude skill (Skill 2) that takes reviewed `write-content` drafts (optionally repurposed from a long-form core), generates visuals, and **schedules** them across Brent's connected channels via the Blotato MCP — behind a hard human-approval gate, honoring the account warm-up ramp.

**Architecture:** A `SKILL.md` orchestration file plus bundled reference files (accounts/channels, the Blotato pipeline, safety + warm-up). The skill is the *distribution* layer only — voice/drafting stays in `write-content`. Pipeline: (optional) `create_source` to extract a long-form core → `write-content` for voice → `create_visual` (or upload an existing asset) for visuals → **human approval gate** → `create_post` with `scheduledTime`. It never publishes immediately by default and never blasts identical copy.

**Tech Stack:** Markdown only (Claude skill format: frontmatter + instructions + reference files) calling the Blotato MCP tools. No code, no build. Verification is rubric-based plus one warm-up-safe live smoke test (schedule → confirm → delete; never publishes).

## Global Constraints

(Copied verbatim from `docs/DESIGN.md` and `docs/account-warm-up-plan.md` — every task implicitly includes these.)

- **Distribution only.** Voice/drafting lives in `write-content`. This skill must NOT rewrite copy; if it must alter text (e.g. trim for X), it re-runs `write-content`'s self-review gate on the result.
- **Hard human gate.** NOTHING is scheduled or published without Brent's explicit approval of the exact text + visual + time. No autonomous posting, ever.
- **Schedule, don't blast.** Default to `scheduledTime` (future), never immediate publish, unless Brent explicitly says "post now". Never schedule identical copy to multiple platforms in the same minute (spam signal) — vary or stagger.
- **Warm-up ramp** (`docs/account-warm-up-plan.md`): low volume first (~3–5/wk FB+IG, 1–2 X); native value, **no cold external links**; reach-safe CTAs (comment-to-get / DM keyword) before raw links; back off if reach drops. `write-content` runs in `warm-up` mode by default; this skill honors that mode.
- **Compliance** carries from `write-content`: no income/earnings/guarantee/health/company-endorsement claims (`skills/write-content/references/never-say.md`). This skill does not re-introduce claims via captions, titles, or alt-text.
- **Verified channels (live 2026-06-17):** Facebook `20306` (⚠️ no Page linked — not postable until Brent connects one), Instagram `53674` @brentbryson (`mediaType` story/reel only), YouTube `27755` (title + privacyStatus), X `12730` @pebobryson801 (threads OK). No LinkedIn/TikTok. Always re-verify with `blotato_list_accounts` at runtime (IDs can change on reconnect).
- **Media URLs must be public.** `create_visual` returns public URLs; use `create_presigned_upload_url` for local files (e.g. Desktop infographics).

---

## The Pre-Publish Safety Rubric (every post must PASS all five before any `create_post`)

A queued post may be scheduled only if all five hold. The skill prints one rubric line per post and **stops for human approval** before calling `create_post`.

1. **Human-approved** — Brent has explicitly approved this exact text + visual + scheduled time. (No approval → do not call `create_post`.)
2. **Account-valid** — `accountId` resolved from a fresh `blotato_list_accounts`; all platform-required fields present (FB `pageId`, IG `mediaType`, YouTube `title`+`privacyStatus`). If a required field can't be satisfied (e.g. FB has no Page), the platform is **skipped with a clear message**, never sent broken.
3. **Voice/compliance intact** — text originated from `write-content` (passed its 5-criterion rubric) and was not mutated; if it was altered for platform fit, `write-content`'s gate was re-run and passed. Captions/titles/alt-text introduce no `never-say.md` violations.
4. **Warm-up respected** — scheduled (not immediate) unless Brent said "post now"; CTA is reach-safe for the current account state; not identical copy cross-posted same-minute.
5. **Media-valid** — `mediaUrls` are public and reachable; platform media constraints satisfied (IG = story/reel; YouTube = video).

---

## File Structure

```
skills/blotato-post/
├── SKILL.md                          # orchestration: triggers, inputs, pipeline, safety gate, output, handoff
└── references/
    ├── accounts-and-channels.md      # verified channels, account IDs, per-platform required fields, FB Page gap handling, runtime re-verify rule
    ├── pipeline.md                   # the Blotato tool surface + how each step works: create_source (repurpose), create_visual / presigned upload, create_post (schedule), polling + public-URL gotchas
    └── safety-and-warmup.md          # the human gate, the 5-criterion safety rubric, the warm-up ramp rules, the no-blast / no-cold-link rules
```

`SKILL.md` loads all three references every run.

---

### Task 1: Accounts + channels reference (`references/accounts-and-channels.md`)

**Files:**
- Create: `skills/blotato-post/references/accounts-and-channels.md`
- Source (verbatim): `docs/DESIGN.md` "Connected channels" table; `skills/blotato-post/SKILL.md` (current stub, verified table).

**Interfaces:**
- Produces: `accounts-and-channels.md` with sections `## Verified channels (snapshot)`, `## Per-platform required fields`, `## The Facebook Page gap`, `## Runtime rule: re-verify first`.

- [ ] **Step 1: Write the file.** Into `## Verified channels (snapshot)`: the 4-row table (Facebook `20306`, Instagram `53674` @brentbryson, YouTube `27755`, X `12730` @pebobryson801) with the note "snapshot 2026-06-17; IDs can change on reconnect — re-verify at runtime." Into `## Per-platform required fields`: Facebook → `pageId` (from a subaccount); Instagram → `mediaType` = `story|reel`, optional carousel via multiple image `mediaUrls`; YouTube → `title` + `privacyStatus` (public/private/unlisted) + `shouldNotifySubscribers`; X → none, threads via `additionalPosts`. Into `## The Facebook Page gap`: FB account `20306` currently returns `subaccounts: []` → no `pageId` available → **FB is not postable**; the skill must detect this (no subaccount) and skip FB with the message: "Facebook has no Page connected in Blotato — connect a Page (dashboard: 'Facebook pages: Don't see your pages? Help') to enable FB posting." Into `## Runtime rule: re-verify first`: ALWAYS call `blotato_list_accounts` at the start of every run and map platform→`accountId` from the live response; never trust the snapshot IDs blindly.

- [ ] **Step 2: Verify.** Confirm all 4 channels present with IDs, all per-platform required fields listed, the FB Page-gap detection + message present, and the runtime re-verify rule stated.
Expected: matches the verified DESIGN.md table; FB gap handling explicit.

- [ ] **Step 3: Commit.**
```bash
git add skills/blotato-post/references/accounts-and-channels.md
git commit -m "feat(blotato-post): accounts + channels reference"
```

---

### Task 2: Pipeline reference (`references/pipeline.md`)

**Files:**
- Create: `skills/blotato-post/references/pipeline.md`
- Source (verbatim): `docs/DESIGN.md` "Blotato tool surface (mapped 2026-06-17)" + the live MCP tool descriptions.

**Interfaces:**
- Produces: `pipeline.md` with `## Step A — Repurpose a core (optional)`, `## Step B — Visuals`, `## Step C — Schedule the post`, `## Gotchas`.

- [ ] **Step 1: Write the file.**
  - `## Step A — Repurpose a core (optional)`: `blotato_create_source` extracts/summarizes a long-form core — source types `text | article | youtube | twitter | tiktok | perplexity-query | audio | pdf`. Use `customInstructions` to shape extraction (e.g. "extract 5 takeaways for an Instagram carousel"). It polls up to 20s; if still processing it returns an `id` → poll `blotato_get_source_status` (≥10s between polls) until `completed`. **The extracted core is then handed to `write-content` to draft on-voice posts** — `create_source` does NOT write in Brent's voice.
  - `## Step B — Visuals`: two paths. (1) Generate: `blotato_list_visual_templates` → pick a template id → `blotato_create_visual` (pass a descriptive `prompt`, leave `inputs: {}` on first attempt); it takes 30s–5min → poll `blotato_get_visual_status` until done → use returned `mediaUrl`/`imageUrls`. (2) Reuse an existing asset (e.g. a Desktop infographic): `blotato_create_presigned_upload_url` → upload → use the returned public URL. IG needs visual-first (story/reel); a carousel = multiple image URLs.
  - `## Step C — Schedule the post`: `blotato_create_post` with `accountId` + `platform` + `text` + platform-required fields + `mediaUrls` (public). Set `scheduledTime` (ISO-8601 UTC) — **default path; never omit it unless Brent said post now**. X/Threads/Bluesky threads via `additionalPosts`. After scheduling, confirm via `blotato_list_schedules`. Status via `blotato_get_post_status`; history via `blotato_list_posts`.
  - `## Gotchas`: `mediaUrls` MUST be public; IG is story/reel only (no plain caption feed post); visual gen is async (poll, don't assume instant); IDs can change on reconnect (re-verify).

- [ ] **Step 2: Verify.** Confirm all three steps + gotchas present; that Step A explicitly hands off to `write-content` for voice; that Step C defaults to `scheduledTime`.
Expected: full pipeline documented against the verified tool surface.

- [ ] **Step 3: Commit.**
```bash
git add skills/blotato-post/references/pipeline.md
git commit -m "feat(blotato-post): Blotato pipeline reference"
```

---

### Task 3: Safety + warm-up reference (`references/safety-and-warmup.md`)

**Files:**
- Create: `skills/blotato-post/references/safety-and-warmup.md`
- Source (verbatim): the Pre-Publish Safety Rubric above; `docs/account-warm-up-plan.md` (when it merges via PR #4) or the Global Constraints warm-up bullet.

**Interfaces:**
- Produces: `safety-and-warmup.md` with `## The human gate`, `## The 5-criterion safety rubric`, `## Warm-up ramp`, `## Hard rules`.

- [ ] **Step 1: Write the file.** `## The human gate`: before ANY `create_post`, present the exact text + visual + scheduled time and wait for Brent's explicit approval; no approval → do not schedule. `## The 5-criterion safety rubric`: reproduce the five criteria verbatim from this plan (Human-approved / Account-valid / Voice-compliance intact / Warm-up respected / Media-valid), with the one-rubric-line-per-post output format. `## Warm-up ramp`: low volume first (~3–5/wk FB+IG, 1–2 X); native value, no cold external links; reach-safe CTAs before raw links; back off if reach drops; the three phases (warm-up / ramp / scale) and that this skill stays in warm-up defaults until Brent flips to "warm". `## Hard rules`: never blast identical copy same-minute; never cold-checkout-link Tiger; never publish immediately by default; never post to a platform missing a required field (skip + message).

- [ ] **Step 2: Verify.** Confirm the gate, all five rubric criteria, the warm-up phases, and the four hard rules are present.
Expected: matches the safety rubric + warm-up plan.

- [ ] **Step 3: Commit.**
```bash
git add skills/blotato-post/references/safety-and-warmup.md
git commit -m "feat(blotato-post): safety + warm-up reference"
```

---

### Task 4: The SKILL.md orchestration

**Files:**
- Modify (replace the stub): `skills/blotato-post/SKILL.md`

**Interfaces:**
- Consumes: all three `references/*.md`.
- Produces: a working distribution skill invokable with one command, gated on human approval.

- [ ] **Step 1: Write the frontmatter** — `name: blotato-post`; `description:` triggering on "schedule this / post this / send these to Blotato / repurpose this video / put this on my channels", naming that it takes `write-content` drafts (or a long-form core), generates visuals, and SCHEDULES via Blotato behind a human gate. Remove the STUB/BLOCKED language.

- [ ] **Step 2: Write the body** with these sections:
  - `## Inputs` — reviewed `write-content` drafts (the normal path), OR a long-form core to repurpose first (a YouTube URL / file / article); optional target platforms (default = whatever drafts were provided for); optional `scheduledTime` (default: ask Brent / next sensible slot); optional account-state (default `warm-up`).
  - `## Process` — (1) load all `references/*.md`; (2) `blotato_list_accounts` to re-verify channels + map platform→accountId (per `accounts-and-channels.md`); (3) if a core was given, `create_source` then route the extracted content through `write-content` for on-voice drafts; (4) for each target platform with a valid account, prepare media (generate via `create_visual` or upload an existing asset) per `pipeline.md`; (5) assemble each post (text + media + required fields + `scheduledTime`); (6) run the safety rubric and **STOP at the human gate**.
  - `## Safety gate (REQUIRED before any create_post)` — reproduce the 5-criterion rubric; print one rubric line per post; present text + visual + time; wait for explicit approval. Skip (with message) any platform missing a required field (e.g. FB with no Page).
  - `## Scheduling` — on approval, `create_post` with `scheduledTime` (never immediate unless told); confirm via `blotato_list_schedules`; report scheduled time + platform + (if available) post URL.
  - `## Output` — a table of what was scheduled (platform / time / link) + what was skipped and why; never claim a post is live without confirming via `get_post_status`/`list_schedules`.
  - `## Out of scope` — does not write/voice copy (that's `write-content`); does not create the lead magnet; does not autonomously post.

- [ ] **Step 3: Verify the skill loads.** Re-read `SKILL.md`; confirm it loads all three references, calls `list_accounts` first, routes repurposed cores through `write-content`, enforces the gate before `create_post`, and defaults to scheduled (not immediate).
Expected: skill structure complete; gate unmissable.

- [ ] **Step 4: Commit.**
```bash
git add skills/blotato-post/SKILL.md
git commit -m "feat(blotato-post): SKILL.md orchestration + safety gate"
```

---

### Task 5: Warm-up-safe live smoke test + calibration

**Files:**
- No new skill files (validation pass). May edit any `references/*.md` or `SKILL.md` to fix misses.

> **Safety:** this test NEVER publishes. It exercises read + generate + schedule-then-delete only. Do NOT call `create_post` without `scheduledTime`, and delete every test schedule immediately after confirming it.

- [ ] **Step 1: Read path.** Run `blotato_list_accounts` and confirm the live map matches `accounts-and-channels.md` (and that FB still reports no Page, so the skip path is exercised). Run `blotato_create_source` on a short YouTube URL and confirm extracted `content` returns.
Expected: account map verified; a source extracts.

- [ ] **Step 2: Visual path.** Run `blotato_create_visual` with a benign test prompt (e.g. a quote card) and poll `get_visual_status` to completion; confirm a public `imageUrls`/`mediaUrl` is returned. (No posting.)
Expected: a public media URL is produced.

- [ ] **Step 3: Schedule-then-delete (the safe write test).** Take one approved test draft, schedule a single post to the **lowest-risk channel** (X `12730`, or YouTube with `privacyStatus: private`) with `scheduledTime` ~24h in the future. Confirm it appears in `blotato_list_schedules`. Then immediately `blotato_delete_schedule` it and confirm it's gone. **It must never go live.**
Expected: schedule created → visible → deleted → absent; nothing published.

- [ ] **Step 4: Gate test.** Attempt a Facebook post in a dry run; confirm the skill detects the missing Page and SKIPS FB with the gap message rather than erroring or sending broken.
Expected: FB skipped with the clear message; other platforms unaffected.

- [ ] **Step 5: Tune + commit.** Fix any miss found above (e.g. polling logic, skip message, gate wording). Re-run the failing step.
```bash
git add -A
git commit -m "feat(blotato-post): live smoke test (schedule-then-delete) + calibration"
```

---

## Verification (whole feature)

- `blotato-post` invokes on `write-content` drafts (or a long-form core), re-verifies accounts, prepares visuals, and **stops at the human gate** before scheduling.
- Every queued post prints its 5-criterion safety rubric line; nothing is scheduled without explicit approval.
- Default path schedules (never immediate); FB is skipped cleanly while it has no Page; identical copy is never blasted same-minute.
- The live smoke test proves read + visual-gen + schedule-then-delete without ever publishing.
- All three reference files exist and are loaded by `SKILL.md`.

## Out of scope (explicitly)

- Writing or voicing copy (→ `write-content`).
- Connecting the Facebook Page (Brent's action in the Blotato dashboard) and upgrading LinkedIn.
- The content idea database proper (currently the Desktop folder).
- The webinar workstream (parked; candidate Skill 3).
- Autonomous / unattended posting of any kind.
