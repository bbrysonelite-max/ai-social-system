# Platform Format Rules

**Date:** 2026-06-17  
**Source:** `docs/DESIGN.md` (platform priorities) + task-4-brief.md

---

## Platform priority summary

| Platform | Priority | Role |
|---|---|---|
| **Facebook** | PRIMARY | Biggest following; conversational anchor |
| **Instagram** | PRIMARY | Second-biggest; visual-first |
| **YouTube** | ANCHOR | Long-form; training + lead magnet funnel |
| **X** | LOW | Almost no following; repurposing only |

> NOTE (non-normative — planning flag, not a rule):
> Connected-account list is Brent-reported; NOT yet verified against live Blotato account. Verify once MCP tools load.

---

## Facebook (PRIMARY)

**Priority:** Highest — biggest following.  
**Ideal length:** 1–2 short paragraphs (conversational, no wall of text).  
**Structure:** Hook (one punchy line) + context/story + call-to-action.  
**Hashtags:** 0–2 (minimal; Facebook prioritizes native engagement over hashtag discovery).  
**Visual expectation:** Native image (carousel OK; aim for 1 image per post).  
**CTA style:** During warm-up, prefer comment-to-get or DM-keyword; avoid direct links until account is warm.

**Example structure:**
```
[Hook line that makes you stop scrolling]

[1–2 sentence story or context that proves the hook]

[Line break]

[Soft CTA or curiosity pointer]

#hashtag (0–2 total)
```

**Voice:** Conversational, declarative, blue-collar metaphors. Assume reader is a team leader who moves fast and doesn't have time for fluff.

---

## Instagram (PRIMARY)

**Priority:** High — second-biggest following.  
**Ideal length:** 3–6 line caption (compact but punchy).  
**Structure:** Strong first line (pre-"...more") → body → soft CTA or magnet pointer.  
**Hashtags:** **Exactly 5, no more** (the Blotato/Instagram API hard-caps at 5 hashtags per post — more than 5 is rejected). Use specific niche tags tied to network marketing, leadership, AI, duplication, follow-up.  
**Visual expectation:** Image or carousel required. High visual polish expected (Nano Banana templates via Blotato).  
**CTA style:** Usually the lead-magnet URL (can be direct link or soft pointer in caption).

**Example structure:**
```
[Hook — make them read "...more"]

[2–4 lines of proof, story, or value]

[Soft CTA or magnet tie-in]

#niche #hashtags #5to8 #team #ai #leverage
```

**Voice:** Caption-led. First line is the headline. Emojis OK (sparingly, 1–2 max). Assume reader is scrolling fast; make every line count.

---

## YouTube (ANCHOR)

**Priority:** Mid-to-high — long-form training funnel.  
**Format:** Community post OR video description (depends on upload cadence).  
**Ideal length:** 150–300 words (enough to establish credibility + hook curiosity).  
**Structure:** Hook (what this video/idea solves) → value (why it matters) → soft pointer (lead magnet or next step).  
**Hashtags:** Not applicable (YouTube community posts don't use hashtags; video descriptions use tags, not hashtags).  
**Visual expectation:** Video thumbnail (Blotato generated) or community-post image.  
**CTA style:** Lead-magnet URL (soft pointer in description or community-post body; "Get the Blueprint" or "Learn the system").

**Example structure (video description):**
```
[Hook — what this video teaches]

[2–3 line value statement]

[Soft CTA pointing to magnet or next video]

Get the Factory Blueprint (link or soft pointer)

[Timestamps if applicable]

#community #AI #Leadership
```

**Voice:** Educational, authoritative (you're the expert here). Less conversational than Facebook; more "here's what I learned" than "let's chat."

---

## X (LOW priority)

**Priority:** Low — almost no following; repurposing only.  
**Ideal length:** ≤280 characters (single post) OR 3–5 post thread.  
**Structure:** Single hook OR thread of punchy statements building to a conclusion.  
**Hashtags:** 1–2 maximum (X favors character economy).  
**Visual expectation:** Optional (text-first platform; images can amplify but not required).  
**CTA style:** Minimal; usually just the topic. Link only if thread flows naturally to it.

**Example (single post):**
```
You can't be on five calls at once. Your training can. AI isn't magic — it's duplication. 

#AIForTeams #Leadership
```

**Example (thread):**
```
1/ Most leaders train on repeat. Same lesson, five times a week.

2/ Record it once. Your team gets it on demand.

3/ That's not content marketing. That's leverage.

4/ That's the Factory Blueprint. (soft link or soft CTA)
```

**Voice:** Declarative, punchy, no filler. X readers expect signal over story. Blue-collar metaphors work; narrative doesn't.

---

## Cross-platform notes

- **Audience ~85% women:** Tune voice warm, relational, team-focused. Avoid "boss" energy or individual-hustle framing.
- **Never earnings claims:** No income/guarantee language. Focus on leverage, duplication, and value. See `skills/write-content/references/never-say.md`.
- **Brand voice across all:** Brent's broadcast voice ("AI for the Rest of Us"), defined for this skill by `skills/write-content/references/voice.md`, not Tiger's 1:1 conversational voice.
- **Blotato repurposing:** These rules set the boundaries; Blotato's repurposing engine handles the atomization and visual generation within them.

See also: `docs/DESIGN.md` division of labor section for how `write-content` (Skill 1) and `blotato-post` (Skill 2) split the work.
