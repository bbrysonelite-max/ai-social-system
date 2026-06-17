# Account Warm-Up Plan

Date: 2026-06-17
Status: plan (gates high-volume posting; execute before scaling the factory)

## Why this exists

The accounts are cold (Facebook biggest, Instagram second, X almost none, YouTube the
anchor). A brand-new or long-dormant account that suddenly posts high volume — especially
with external links — gets **throttled, shadow-banned, or flagged as spam**. Warm-up earns
the platform's trust first, so the factory's volume lands instead of getting suppressed.

This is principle-based; Brent's 39-yr field judgment and live reach signals override any
specific number here.

## The rule of the ramp

1. **Complete the house before inviting anyone in** (profiles, bios, photos).
2. **Post native value first, no external links** — platforms suppress new accounts that push traffic off-platform.
3. **Engage like a human** — comment/reply on others, don't only broadcast.
4. **Raise volume gradually** — don't jump from 0 to factory volume.
5. **Introduce CTAs softly** (comment-to-get / DM keyword) before raw links.
6. **Watch reach** — if reach drops after a change, back off a step.

## Phase 0 — Foundation (before any posting)

- Complete every profile: name, handle, **bio from `tiger-claw-marketing-restore/brand/social-bios.json`**, profile + cover image (reuse YouTube thumbnails / brand stills).
- Set the **link-in-bio** destination = the lead magnet opt-in (`stan.store/brentbryson/p/factory-blueprint`). Confirm it works.
- Confirm the lead-magnet funnel is live end-to-end (opt-in → welcome email) before any CTA points at it.
- Decide identity per account (default: post **as Brent** — "AI for the Rest of Us").

## Phase 1 — Warm-up (≈ Weeks 1–2)

- **Volume:** low. ~3–5 posts/week per primary platform (FB, IG). 1–2 on X. No factory-volume yet.
- **Content:** native value posts from the idea bank via `write-content`, **no external links**. Pure value — answer "how does AI help your team."
- **Engagement:** daily — comment on / reply to others in your world (leaders, NM, direct-sales). This signals "real human" more than posting does.
- **CTA:** none, or "follow for more." `write-content` runs in **warm-up mode** (default).

## Phase 2 — Ramp (≈ Weeks 3–4)

- **Volume:** increase gradually toward factory cadence (roughly double Phase 1).
- **CTA:** introduce **reach-safe** mechanics — "comment BLUEPRINT and I'll send it" / DM keyword — instead of raw links. Lead magnet is the destination.
- Keep engaging. Vary cadences/hooks (the `write-content` batch-variety guard handles this).

## Phase 3 — Scale (Week 5+, once "warm")

- Move to full factory volume + Blotato repurposing/scheduling.
- Introduce **direct link CTAs** to the lead magnet, monitoring reach. If reach drops, revert to comment-to-get.
- This is when `write-content` flips to **account-state: warm**.

## Per-platform notes

- **Facebook (PRIMARY):** your biggest following = warms fastest. Favor conversational story posts; consider posting from a Page *and* engaging from your personal profile/groups. FB heavily suppresses off-site links early — comment-to-get is safest.
- **Instagram (PRIMARY):** caption-led + image/carousel. Link-in-bio only (no in-caption links anyway). Niche hashtags, not broad.
- **YouTube (ANCHOR):** the long-form home; lead magnet lives in the description. Less throttling risk; the warm-up concern is mostly FB/IG/X.
- **X (LOW):** almost no following — lowest priority. Repurpose, don't originate. Threads over single posts.

## Definition of "warm" (the trigger to flip to Phase 3)

An account is "warm" when, over ~2 weeks, it shows: stable or rising reach, real comments/DMs
from the target audience, and no visible suppression after a normal post. That's the green
light to flip `write-content` to `account-state: warm` and turn on link CTAs + full volume.

## Do NOT

- Blast identical copy across all platforms same-minute (spam signal) — Blotato repurposing varies it; keep it varied.
- Mass-follow / follow-unfollow to fake growth.
- Lead with external links on cold accounts.
- Buy followers.

## Out of scope

- Actual posting/scheduling (→ `blotato-post`, Skill 2, post-restart).
- Lead-magnet asset + email tooling (already exists: Factory Blueprint + Stan/Beehiiv).
