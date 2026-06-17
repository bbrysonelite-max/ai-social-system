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

Open question to resolve in the plan: how much per-platform tailoring `write-content`
does up front vs. how much Blotato's repurposing handles — with the human review gate
enforcing voice on whatever Blotato generates.

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

## Connected channels (per Brent, 2026-06-17 — to be live-verified via Blotato MCP next session)

Priority reflects following size, not platform hype:

1. **Facebook** — biggest following → primary. Conversational, community storytelling.
2. **Instagram** — second-biggest → primary. Visual, caption-led.
3. **YouTube** — long-form anchor (existing Youtube-system pipeline).
4. **X** — almost no following → lowest priority, repurposing only.

NOT connected yet:
- **LinkedIn** — Brent wants to add this; account is not on a paid plan. Likely add once
  upgraded (LinkedIn favors long-form + infographics — strong fit for authority content).
- **TikTok** — bio exists, not linked.
⚠️ Connected-account list is Brent-reported; NOT yet verified against the live Blotato
account. Verify first thing once the MCP tools load (task #4).

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
- [ ] Hard "never say" list (income claims, NuSkin compliance, banned words)

## Open items pending Blotato MCP (Skill 2, post-restart)

- [ ] Enumerate connected channels in the Blotato account
- [ ] Map Blotato tool surface (publish, media/visual gen, scheduling)
- [ ] Account warm-up ramp before scaling to factory volume
