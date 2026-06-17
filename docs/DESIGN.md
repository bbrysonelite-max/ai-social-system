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

NOT connected: LinkedIn, TikTok (bios exist but accounts not linked).
⚠️ Connected-account list is Brent-reported; NOT yet verified against the live Blotato
account. Verify first thing once the MCP tools load (task #4).

## Open calibration items (needed to flesh Skill 1)

- [x] Platform set → Facebook, Instagram, YouTube, X (FB/IG first)
- [ ] CTA / close (webinar → Cal.com? follow/subscribe? signature sign-off?)
- [ ] Hard "never say" list (income claims, NuSkin compliance, banned words)

## Open items pending Blotato MCP (Skill 2, post-restart)

- [ ] Enumerate connected channels in the Blotato account
- [ ] Map Blotato tool surface (publish, media/visual gen, scheduling)
- [ ] Account warm-up ramp before scaling to factory volume
