# ai-social-system — Design

Date: 2026-06-17
Status: BONES (design captured; skills not yet implemented)

## Goal

Programmatically post valuable, on-voice content about Tiger Claw and the broader
"AI + distribution" thesis across Brent's connected social channels — to build
brand/authority, fuel the Flip-the-Script webinar funnel, and warm up the audience
(including Brent's own team) so they're primed before any ask.

This is **brand/visibility content**, not cold content-led lead gen (which Brent
rejected in 2026-04). Different machine, different purpose.

## The model (Sabrina Ramonov / Blotato content factory)

1. A **"Write Content" skill** encodes brand voice once, reused every run.
2. Local files (notes, screenshots, "receipts") become multi-platform posts.
3. **Blotato** generates visuals (Nano Banana templates) and schedules across channels.
4. Weekly batch + a feedback loop that updates the skill as the voice sharpens.

Human-in-the-loop review of every piece is non-negotiable.

## Division of labor (IMPORTANT — Blotato = the repurposing engine)

Brent chose Blotato specifically for its **repurposing** feature. So the two skills
split like this, mirroring how Sabrina hits volume (write strong cores, repurpose — not
write 250 originals):

- **`write-content` (Skill 1)** — produce the **voice-true core** piece(s) in Brent's
  voice. Quality and voice integrity, not volume.
- **`blotato-post` (Skill 2)** — use **Blotato's repurposing** to atomize the core into
  many platform-specific pieces + visuals (Nano Banana templates) + scheduling.

**Resolved (2026-06-17, after mapping the live Blotato tool surface):** there is no
one-click "atomize into N platform posts" MCP call. Blotato's repurposing surface is:
`create_source` (extract/summarize a long-form core — YouTube transcript, TikTok, article,
PDF, audio, tweet, raw text, or a Perplexity research query, with `customInstructions`).
So the split is:
- **`write-content`** owns the voice-true per-platform tailoring (the intelligence).
- **`blotato-post`** uses `create_source` to pull the core, `create_visual` for visuals,
  and `create_post` to publish/schedule per platform. The human gate enforces voice on
  anything generated before it schedules.

### Blotato tool surface (mapped 2026-06-17)
- **Accounts:** `blotato_list_accounts`, `blotato_get_user`.
- **Sources (repurposing input):** `blotato_create_source` (8 source types) +
  `blotato_get_source_status` (poll long extractions).
- **Visuals (Nano Banana / templates):** `blotato_create_visual` (slideshows, quote cards,
  carousels, infographics, AI videos), `blotato_list_visual_templates`,
  `blotato_get_visual_status`, `blotato_create_presigned_upload_url` (upload own assets →
  public URL; use for the Desktop infographics).
- **Publish / schedule:** `blotato_create_post` (immediate, `scheduledTime` ISO-8601, or
  `useNextFreeSlot`; threads via `additionalPosts`), `blotato_get_post_status`,
  `blotato_list_posts`, and schedule management (`list`/`get`/`update`/`delete_schedule`).
- Note: `mediaUrls` must be **publicly accessible URLs** — `create_visual` returns them;
  use `create_presigned_upload_url` for local files.

## Voice sources (canonical — do not fork prematurely)

| Source | Role | Path |
|---|---|---|
| `SOUL_DOCUMENT.md` | Broadcast voice, Three Windows, signature phrases | `bbrysonelite-max/Youtube-system/identity/` |
| `CHANNEL_IDENTITY.md` | Audience layers, content pillars | `bbrysonelite-max/Youtube-system/identity/` |
| `VOICE_FORMATTING_RULES.md` | Cadence/punctuation rules | `bbrysonelite-max/Youtube-system/identity/` |
| `voice-cadences.md` | Verbatim book cadences (Parallel Inversion, Reframe Correction, …) | `~/Desktop/vault-personal/04_The_Synthesizer/Atomic_Notes/` |
| `manifesto.md` ("The Third Window") | Narrative spine | `~/Desktop/_Desktop_System/10_Project_Files/Tiger_Claw/` |

Note: `vault-personal/.../soul-voice-block.md` is **Tiger-the-agent's 1:1 conversational
voice** — NOT the broadcast voice. Do not use it for posts.

## Brand architecture (decide per connected account)

- **Brent Bryson — "AI for the Rest of Us"** (@BrentBryson): Brent's face/channel — the manifesto voice. **Default posting identity.**
- **The Goods** (thegoods.ai): company, "creator of Tiger Claw".
- **Tiger Claw** (tigerclaw.io): the product.

Bios for product accounts exist in `tiger-claw-marketing-restore/brand/social-bios.json`.

## Connected channels (LIVE-VERIFIED via Blotato MCP, 2026-06-17)

Verified against the live Blotato account (`blotato_list_accounts` + dashboard screenshot).
Subscription active. 0 posts scheduled (clean slate). Priority reflects following size:

| # | Platform | Blotato account ID | Account | Posting requirement |
|---|---|---|---|---|
| 1 | **Facebook** (primary) | `20306` | Brent Bryson | requires `pageId` from a subaccount (a Facebook **Page**) |
| 2 | **Instagram** (primary) | `53674` | @brentbryson | `mediaType` = `story` or `reel` (visual-first, not plain feed caption) |
| 3 | **YouTube** (anchor) | `27755` | Brent Bryson | `title` + `privacyStatus` (public/private/unlisted) |
| 4 | **X** (low) | `12730` | @pebobryson801 | none; supports threads via `additionalPosts` |

⚠️ **Facebook Page gap (action for Brent).** The Facebook account is connected as a profile
but **no Page is linked** (`subaccounts: []`; dashboard shows "Facebook pages: Don't see your
pages? Help"). Blotato requires a `pageId` to post to Facebook, so the biggest channel is
**not postable until a Page is connected** in the Blotato dashboard. Resolve before FB goes live.

⚠️ **Instagram is story/reel only** via the API — there is no plain caption-only feed post.
IG drafts from `write-content` must be visual-first (image/carousel/reel with caption).

NOT connected (confirmed absent from the live account):
- **LinkedIn** — Brent wants to add this; account is not on a paid plan. Add once upgraded
  (LinkedIn favors long-form + infographics — strong fit for authority content).
- **TikTok** — bio exists, not linked.

## Messaging spine (drives EVERY post)

**The frame: "What will Tiger do for your team?"**

- Look **past the individual** — speak to leverage at the **team** level (current team:
  everybody in it; or future team).
- **Assume the reader is smart** enough to want a Tiger. Don't sell down; speak up.
- The desire being served: **AI that is safe, duplicable, and real leverage / real value.**
- Where Tiger delivers that: the **follow-up and coaching** part of the program
  ("Fortune is in Follow-up" + duplication doctrine — "give them their own Tiger").

This is leader-first positioning: the leverage is leaders (a leader = their whole team +
white-label potential), not individual tool sales. Tiger is the **proof**, not the pitch.

## Audience filter (who we attract — and repel)

Target: **leaders who think about their team, not themselves.** "My people: people who
don't think about themselves, they think about their team." Content should *repel* the
me-first individual and *attract* the team-first leader. Drumbeat: "your team."

## Content pillars (team-benefit angles)

Every piece answers a version of **"How does AI help your team?"**:
1. **Inform your team** — keep a team current on AI without overwhelm.
2. **Train your team** — AI as a duplicable training/coaching layer.
3. **Make your team more effective** — follow-up + leverage (Tiger's heart).
4. **Save your team money / time** — real value, "way more value than it costs".

Tone: biography-as-credibility (never earnings), focus outside Brent, "value must exceed
cost". See `skills/write-content/references/never-say.md`.

## CTAs / funnel (the two doors)

Primary goal right now is **email list growth from zero** — every email is 100% growth.

1. **Primary CTA (always): high-value lead magnet → email capture.** REUSE the existing,
   working funnel in `bbrysonelite-max/Youtube-system/lead-magnet/` — do not rebuild:
   - **Magnet:** "The Factory Blueprint — Your AI Agent Starter Kit for Network Marketers"
     (`factory-blueprint.html`).
   - **Newsletter:** "Agentic Loadout" (free weekly).
   - **Email capture (EXISTS):** Stan Store `stan.store/brentbryson/p/factory-blueprint`
     + Beehiiv option. (Resolves the email-capture dependency.)
   - **Welcome sequence (EXISTS):** 3 emails / 7 days, FK Grade 8, in-voice.
   - ⚠️ **Framing drift to resolve:** existing opt-in copy is *individual*-framed ("run
     YOUR network marketing business"); current positioning is *team*-framed ("how AI helps
     YOUR TEAM"). Confirm whether `factory-blueprint.html` is already team-framed inside, or
     re-point the opt-in copy to the team-leverage spine.
2. **Secondary CTA (sparingly, takeaway energy): open a conversation, not a sale.**
   "If you run a team and want to see what this looks like for your group — let's talk."
   This is the leader / white-label door.
3. **"Get a Tiger" and "find an opportunity" come AFTER the relationship** — in the nurture
   sequence and the conversation, segmented by who they are (team member / leader / prospect).
   NOT the cold social CTA. Don't checkout-link Tiger on cold social.

Warm-up caveat: during account warm-up, prefer reach-safe CTA mechanics (comment-to-get,
DM keyword) over raw outbound links, which algorithms throttle on cold accounts.

Note: this evolves Brent's 2026-04 "content is dead for lead gen" stance toward
**high-value lead magnets built on earned proof** (not generic free content). Recorded
intentionally. Dependency to resolve in the plan: lead-magnet asset(s) + email-capture
mechanism (tool/landing page).

## Open calibration items (needed to flesh Skill 1)

- [x] Platform set → Facebook, Instagram, YouTube, X (FB/IG first)
- [x] CTA / close → lead magnet → email (primary); Get-a-Tiger / find-NM-opportunity (secondary)
- [x] Hard "never say" list → see `skills/write-content/references/never-say.md` (CONFIRMED)

## Parked / backlog (separate workstreams — do NOT slop into write-content)

- **Webinar workstream.** Brent wants to bank several webinars now (team-focused angle:
  inform/train/effectiveness/savings), while top-of-mind. No webinar SKILL exists; the
  webinar *build* lives in `bbrysonelite-max/Tiger-Webinar-Funnel` (`webinar-script.md`,
  `heygen-production.md`, `booking-page.md`). Candidate **third skill** under
  `ai-social-system` later. Re-point new webinars to the "your team" frame (the existing
  one was self/opportunity-framed — fine, but the new ones lead with team).

## Open items pending Blotato MCP (Skill 2)

- [x] Enumerate connected channels in the Blotato account — DONE 2026-06-17 (4 channels, table above)
- [x] Map Blotato tool surface (publish, media/visual gen, scheduling) — DONE 2026-06-17 (surface above)
- [ ] **Brent action:** connect a Facebook **Page** in Blotato (FB not postable until then)
- [ ] Build Skill 2 (`blotato-post`) against the verified surface — via three-agent rule
- [ ] Account warm-up ramp before scaling to factory volume (see `account-warm-up-plan.md`, PR #4)
