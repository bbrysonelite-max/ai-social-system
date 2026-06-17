# write-content Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `write-content` Claude skill that turns one idea (or a local file) into platform-specific social posts in Brent Bryson's voice — drafting only, no posting.

**Architecture:** A `SKILL.md` orchestration file plus bundled reference files (voice, pillars/audience, CTA, compliance, platform formats, gold examples). The skill loads the references every run, drafts per platform, then runs a self-review gate before showing output. No posting/scheduling/images (that is the separate `blotato-post` skill).

**Tech Stack:** Markdown only (Claude skill format: frontmatter + instructions + reference files). No code, no build, no runtime deps. Verification is rubric/example-based, not unit tests.

## Global Constraints

(Copied verbatim from `docs/DESIGN.md` — every task implicitly includes these.)

- **Messaging spine:** "What will Tiger do for your team?" — look past the individual to team leverage; assume the reader is smart; AI that is safe, duplicable, real leverage/value; lands in follow-up + coaching.
- **Audience filter:** team-first LEADERS (direct sales / affiliate / network marketing; ~85% women). Repel the me-first individual. Drumbeat: "your team."
- **Pillars:** (1) Inform your team (2) Train your team (3) Make your team more effective (4) Save your team money/time.
- **Voice sources (canonical):** `Youtube-system/identity/SOUL_DOCUMENT.md`, `.../CHANNEL_IDENTITY.md`, `.../VOICE_FORMATTING_RULES.md`; `~/Desktop/vault-personal/04_The_Synthesizer/Atomic_Notes/voice-cadences.md`; `~/Desktop/_Desktop_System/10_Project_Files/Tiger_Claw/manifesto.md`. Do NOT use `soul-voice-block.md` (that is Tiger-the-agent's 1:1 voice).
- **CTA:** primary = high-value lead magnet → email (existing Factory Blueprint → Agentic Loadout, Stan/Beehiiv); secondary = conversation (not a sale) for leaders/white-label. Do NOT checkout-link Tiger on cold social. During warm-up prefer reach-safe mechanics (comment-to-get / DM keyword) over raw links.
- **Compliance (never):** income/earnings claims, guarantees of results/rank/income, "get rich", health/product claims, naming a specific company (e.g. NuSkin) as endorsing, anything unbackable, disparaging competitors. Brent's track record (Subway, Blue Diamond, 39 yrs) = biography only, never expected earnings. See `skills/write-content/references/never-say.md`.
- **Platforms (priority):** Facebook (biggest) + Instagram primary; YouTube long-form anchor; X lowest. No LinkedIn/TikTok yet.

---

## The Verification Rubric (used by every task that produces or tests output)

A draft PASSES only if all five hold:
1. **Voice** — uses at least one of Brent's named cadences appropriately (Parallel Inversion / Reframe Correction / Triple-Negation / Absolute Binary / Anaphoric Stack / Isolated Beat); short declarative sentences; no banned words ("leverage synergies", "utilize", "folks", "friend"); no exclamation-point padding.
2. **Compliance** — passes `never-say.md`: no income/earnings/guarantee/health/company-endorsement claims; Brent's record framed as biography only.
3. **Frame** — speaks to "your team"; team-first, not me-first; ties to follow-up/coaching where relevant.
4. **Platform** — matches that platform's format rules (see `platform-formats.md`).
5. **CTA** — correct CTA for the mode (lead-magnet primary; soft/reach-safe during warm-up; no cold Tiger checkout link).

---

## File Structure

```
skills/write-content/
├── SKILL.md                          # orchestration: trigger, inputs, process, self-review gate, output
└── references/
    ├── voice.md                      # distilled voice: cadences (verbatim examples), signature phrases, formatting
    ├── pillars-and-audience.md       # spine, 4 pillars, team-first audience filter
    ├── cta-and-funnel.md             # CTA strategy, lead magnet, two doors, warm-up mechanics
    ├── never-say.md                  # compliance (ALREADY EXISTS — keep)
    ├── platform-formats.md           # FB / IG / YouTube / X format rules
    └── examples.md                   # 3 gold-standard posts (one per non-overlapping pillar) that pass the rubric
```

---

### Task 1: Distill the voice reference (`references/voice.md`)

**Files:**
- Create: `skills/write-content/references/voice.md`
- Sources to pull from (read-only): `Youtube-system/identity/SOUL_DOCUMENT.md`, `.../VOICE_FORMATTING_RULES.md`; `~/Desktop/vault-personal/04_The_Synthesizer/Atomic_Notes/voice-cadences.md`; `~/Desktop/_Desktop_System/10_Project_Files/Tiger_Claw/manifesto.md`

**Interfaces:**
- Produces: `voice.md` — the single voice file `SKILL.md` loads. Must contain four sections: `## Cadences`, `## Signature phrases`, `## Formatting rules`, `## What Brent is NOT`.

- [ ] **Step 1: Assemble the file.** Pull, verbatim, into `## Cadences`: the named cadences from `voice-cadences.md` (Parallel Inversion, Reframe Correction, Triple-Negation, Absolute Binary, Anaphoric Stack, Isolated Beat) — each with its definition and 2 verbatim examples. Into `## Signature phrases`: the phrase list from `SOUL_DOCUMENT.md` ("When the wind blows…", "Crack the ice…", "If you're not future-ready…", etc.) marked "deploy verbatim, never paraphrase". Into `## Formatting rules`: the rules from `VOICE_FORMATTING_RULES.md` (short sentence after long; ≤2 commas before a period; ≤20 words/sentence; FK Grade 8; rhetorical question cadence; ellipsis/em-dash usage). Into `## What Brent is NOT`: the list from `SOUL_DOCUMENT.md`.

- [ ] **Step 2: Verify against sources.** Re-read each source section and confirm every cadence has its verbatim examples and no phrase was paraphrased. Confirm the file does NOT pull from `soul-voice-block.md`.
Expected: all six cadences present with examples; signature phrases verbatim.

- [ ] **Step 3: Commit.**
```bash
git add skills/write-content/references/voice.md
git commit -m "feat(write-content): distilled voice reference"
```

---

### Task 2: Pillars + audience reference (`references/pillars-and-audience.md`)

**Files:**
- Create: `skills/write-content/references/pillars-and-audience.md`
- Source: `docs/DESIGN.md` (Messaging spine, Audience filter, Content pillars sections)

**Interfaces:**
- Produces: `pillars-and-audience.md` with sections `## The spine`, `## Audience filter`, `## The four pillars` (each pillar: name + one-line definition + one example angle).

- [ ] **Step 1: Write the file** using the verbatim spine, audience filter, and four pillars from the Global Constraints above. For each pillar add one concrete example angle drawn from the idea bank (`~/Desktop/Social Media Posts: Ideas/`), e.g. Train → "AI as a duplicable onboarding step your whole team runs the same way."

- [ ] **Step 2: Verify.** Confirm all four pillars present, the spine question is exact, and the audience filter explicitly says repel me-first / attract team-first.
Expected: matches spec.

- [ ] **Step 3: Commit.**
```bash
git add skills/write-content/references/pillars-and-audience.md
git commit -m "feat(write-content): pillars + audience reference"
```

---

### Task 3: CTA + funnel reference (`references/cta-and-funnel.md`)

**Files:**
- Create: `skills/write-content/references/cta-and-funnel.md`
- Source: `docs/DESIGN.md` (CTAs / funnel section); `Youtube-system/lead-magnet/LEAD_MAGNET_STRATEGY.md`

**Interfaces:**
- Produces: `cta-and-funnel.md` with `## Primary CTA`, `## Secondary CTA`, `## Warm-up mode`, `## Hard rules`.

- [ ] **Step 1: Write the file.** Primary: lead magnet → email (Factory Blueprint → Agentic Loadout; opt-in `stan.store/brentbryson/p/factory-blueprint`). Secondary: conversation, not sale ("If you run a team and want to see this for your group — let's talk"). Warm-up mode: comment-to-get / DM-keyword instead of raw links. Hard rules: never cold-checkout-link Tiger; "Get a Tiger" / "find an opportunity" only after relationship.

- [ ] **Step 2: Verify.** Confirm lead-magnet primary, conversation secondary, warm-up reach-safe mechanics, and the "no cold Tiger link" rule are all present.
Expected: matches spec CTA section.

- [ ] **Step 3: Commit.**
```bash
git add skills/write-content/references/cta-and-funnel.md
git commit -m "feat(write-content): CTA + funnel reference"
```

---

### Task 4: Platform formats reference (`references/platform-formats.md`)

**Files:**
- Create: `skills/write-content/references/platform-formats.md`

**Interfaces:**
- Produces: `platform-formats.md` with one `### <Platform>` block each for Facebook, Instagram, YouTube (community/caption), X — each block stating: priority, ideal length, structure, hashtag norm, visual expectation.

- [ ] **Step 1: Write the file** with concrete rules:
  - **Facebook (PRIMARY):** conversational story; 1–2 short paragraphs + a line-break hook; 0–2 hashtags; native image; CTA as comment-to-get during warm-up.
  - **Instagram (PRIMARY):** caption-led; strong first line (pre-"more"); 3–6 line body; up to ~8 niche hashtags; image/carousel expected.
  - **YouTube:** community-post or video-description copy; hook + value + soft pointer to lead magnet in description.
  - **X (LOW priority):** single punchy hook ≤280 chars or a 3–5 post thread repurposed from the core; minimal hashtags.

- [ ] **Step 2: Verify.** Each of the four platforms has all five fields and FB/IG are marked PRIMARY.
Expected: four complete blocks.

- [ ] **Step 3: Commit.**
```bash
git add skills/write-content/references/platform-formats.md
git commit -m "feat(write-content): platform format rules"
```

---

### Task 5: Gold-standard examples (`references/examples.md`)

**Files:**
- Create: `skills/write-content/references/examples.md`
- Inputs: one idea each from the idea bank (`~/Desktop/Social Media Posts: Ideas/ideas-*.md`) for three different pillars.

**Interfaces:**
- Consumes: `voice.md`, `pillars-and-audience.md`, `cta-and-funnel.md`, `never-say.md`, `platform-formats.md` (Tasks 1–4 + existing).
- Produces: `examples.md` — 3 anchor posts (one Facebook, one Instagram, one X), each labeled with its pillar, that PASS the full rubric. These anchor the skill's quality bar.

- [ ] **Step 1: Draft three exemplar posts** — pick three idea-bank entries across three pillars; write one FB post, one IG caption, one X hook/thread, applying all references. Use a named cadence in each.

- [ ] **Step 2: Score each against the Verification Rubric** (all five criteria). Revise any that fail until all three pass. Write the passing posts into `examples.md` with a short "why this passes" note under each.
Expected: 3 posts, each PASS on all 5 rubric criteria.

- [ ] **Step 3: Commit.**
```bash
git add skills/write-content/references/examples.md
git commit -m "feat(write-content): gold-standard example posts"
```

---

### Task 6: The SKILL.md orchestration

**Files:**
- Modify (replace stub): `skills/write-content/SKILL.md`

**Interfaces:**
- Consumes: all `references/*.md`.
- Produces: a working skill invokable with one command.

- [ ] **Step 1: Write the frontmatter** — `name: write-content`; `description:` that triggers on "write content / draft a post / turn this idea into posts in my voice" and names the platforms (FB/IG/YouTube/X) and that it is drafting-only.

- [ ] **Step 2: Write the body** with these sections:
  - `## Inputs` — an idea/topic OR a local file path (note, screenshot, "receipt"); optional target platforms (default: FB + IG, add YouTube/X on request).
  - `## Process` — (1) load all `references/*.md`; (2) if a local file was given, read it and extract the point/"receipt"; (3) pick the pillar; (4) draft the post(s) per target platform using `voice.md` + `platform-formats.md`; (5) attach the correct CTA from `cta-and-funnel.md` (warm-up mode unless told otherwise).
  - `## Self-review gate (REQUIRED before showing output)` — run each draft against the Verification Rubric (the five criteria, reproduced here); if any fail, rewrite before presenting. State the rubric result line per draft.
  - `## Output` — labeled per-platform drafts + the pillar + the CTA used, ready for Brent's review; explicitly hand off to `blotato-post` for visuals/scheduling (do not post).

- [ ] **Step 3: Verify the skill loads and runs (calibration run #1).** Invoke the skill on one idea-bank entry. Confirm the output: produces labeled FB + IG drafts, each passes the rubric, and the self-review result lines are present.
Expected: on-voice, compliant, team-framed, platform-correct drafts with a passing rubric line each.

- [ ] **Step 4: Commit.**
```bash
git add skills/write-content/SKILL.md
git commit -m "feat(write-content): SKILL.md orchestration + self-review gate"
```

---

### Task 7: Calibration / "95% confident" eval

**Files:**
- No new files (tuning pass). May edit any `references/*.md` or `SKILL.md`.

- [ ] **Step 1: Run the skill on 3 diverse idea-bank entries** (different pillars, different platforms incl. one X thread).

- [ ] **Step 2: Score all outputs against the rubric** and have Brent eyeball them for voice fidelity. Record any miss (wrong cadence, off-frame, weak hook, compliance slip).

- [ ] **Step 3: Tune the references** to fix recurring misses (e.g., strengthen a formatting rule, add a banned phrase, sharpen a pillar example). Re-run the failing case.
Expected: 3/3 outputs pass the rubric and read as Brent.

- [ ] **Step 4: Commit.**
```bash
git add -A
git commit -m "feat(write-content): calibration tuning to 95% confidence"
```

---

## Verification (whole feature)

- `write-content` invokes on an idea or local file and returns labeled FB/IG (and on request YouTube/X) drafts.
- Every draft passes the 5-criterion rubric; the skill prints a rubric result line per draft.
- No posting/scheduling/image generation occurs (that is `blotato-post`).
- All six reference files exist and are loaded by `SKILL.md`.

## Out of scope (explicitly)

- Posting, scheduling, repurposing, image/visual generation (→ `blotato-post`, Skill 2, post-restart).
- The content idea database proper (currently the Desktop folder).
- Lead-magnet asset creation / email tooling (exists: Factory Blueprint + Stan/Beehiiv).
- Webinar workstream (parked).
