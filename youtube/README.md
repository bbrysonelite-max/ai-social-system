# youtube — channel strategy (part of ai-social-system)
## Brent Bryson — AI for the Rest of Us
### YouTube channel identity, strategy, and production playbook

> **MERGED 2026-06-22.** This was the standalone `Youtube-system` repo. It now
> lives inside **`ai-social-system`** as the single source of truth — the
> Youtube-system repo is closed. This folder owns **channel strategy** (identity,
> audience, pillars, scripts, SEO, analytics). The **mechanism** — rendering,
> packaging, scheduling, posting — is owned by the live skills in `../skills/`:
> `write-content`, `package-video`, `cadence`, `blotato-post`. Where a tool name
> below conflicts with a skill, **the skill wins.**
>
> **Two corrections applied in this merge (do not reintroduce):**
> 1. **Posting/scheduling runs on Blotato**, not Buffer. Buffer does NOT replace
>    Blotato — that was a hallucination and is removed.
> 2. **No "100% AI avatar" auto-generation.** Brent renders his own clones in the
>    HeyGen GUI (the only quality he accepts); the system packages + posts the
>    finished clip — it does not auto-generate avatars.

---

## Mission
Produce a top 10% YouTube channel using consistency and valuable information as hooks.
One long-form video per week. Daily Shorts. Cross-platform distribution.
Brent renders the avatar clips himself in HeyGen; the system handles packaging,
captions, and cross-platform posting via Blotato.

## North Star
"Combining real intelligence with true distribution is an opportunity we'll never see again."

## Revenue Goal
$3,000/day net profit by December 31, 2026.
This channel is a primary engine of that mission.

---

## Repository Structure

  /youtube-system
    /identity
      SOUL_DOCUMENT.md            (Read first. Always.)
      CHANNEL_IDENTITY.md         (Brand, audience, pillars, cadence)
      AVATAR_SPECS.md             (HeyGen settings — all three clones)
      VOICE_FORMATTING_RULES.md   (ElevenLabs script formatting rules)
    /research
      topics_YYYY-MM-DD.json      (Weekly topic candidates from research agent)
      research_[topic].md         (Deep research briefs per video)
    /scripts
      script_v1_[topic].md        (AI-generated first draft)
      script_v2_[topic].md        (Post-edit approved final draft)
    /production
      thumbnail_brief_[topic].md  (Thumbnail direction and copy options)
      metadata_[topic].md         (Title, description, tags, chapters)
    /analytics
      analytics_log.md            (Weekly performance data and insights)
    /agents
      research_agent_prompt.md    (Prompt for research agent)
      script_agent_prompt.md      (Prompt for script generation agent)
      metadata_agent_prompt.md    (Prompt for SEO metadata agent)
    README.md                     (This file)
    WORKFLOW.md                   (Full 12-layer production system)

---

## The 12-Layer Workflow (Summary)
1.  Channel Identity System       COMPLETE
2.  Trend & Research Intelligence Agent
3.  Subject Selection & Approval Gate
4.  Deep Research & Learning Synthesis
5.  Script Generation
6.  Script Editing & Brent Review Gate
7.  Avatar Video Production (HeyGen)
8.  B-Roll, Captions & Post-Production
9.  Thumbnail Production
10. Metadata & SEO Package
11. Multi-Platform Publishing Agent
12. Analytics Feedback Loop

Full detail in WORKFLOW.md (building next).

---

## Rule Zero
If you are an agent reading this file:
Read SOUL_DOCUMENT.md before doing anything else.
Every output must pass this test: Does this sound like Brent Bryson?
If no — rewrite it.

---

## Build Status
- [DONE] SOUL_DOCUMENT.md
- [DONE] CHANNEL_IDENTITY.md
- [DONE] AVATAR_SPECS.md
- [DONE] VOICE_FORMATTING_RULES.md
- [NEXT] WORKFLOW.md
- [NEXT] Agent prompts
