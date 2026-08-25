# creative-skills — media generation (avatars / video / images)

**Brought into `ai-social-system` 2026-06-22 so the whole social system has ONE
home.** These are the **creative half** — the skills that *make* media (avatars,
video, images). The **posting half** lives in `../skills/` (`write-content`,
`blotato-post`, `cadence`).

> ## Ground rule for this folder: NOTHING is thrown away.
> Every skill here is preserved verbatim. "Getting rid of duplicates" means
> **consolidating to one home (this repo)** — never deleting work. The copies
> that still live in `~/.claude/skills/`, `~/.agents/skills/`, `~/.codex/skills/`,
> and `~/Desktop/skills/Ai-social-media-System-Skills/` are untouched. We only
> retire a scattered duplicate **after** its content is safely committed here,
> and even then it's archived, not deleted.

> ## Why this is a separate folder (not `../skills/`)
> `../skills/` is symlinked into `~/.claude/skills/` and auto-loads as **live**.
> Some skills here are deprecated or not-yet-adopted — keeping them out of the
> live `skills/` folder means they're **preserved but won't auto-fire** (so the
> rejected HeyGen API-render path can't run by accident). Promote a skill to
> `../skills/` only when you decide it's canonical.

---

## What the LIVE posting system actually uses today

So the status column below is grounded, not guessed:

- **Images:** Blotato **Nano Banana** templates, via `blotato-post`
  (`blotato_create_visual`). This is the only image generator wired into posting.
- **Video:** `package-video` (your HeyGen **GUI** clip + HyperFrames packaging).
  You render the clone by hand — **no API auto-generation.**

None of the six skills below are currently wired into the posting system. They're
the creative stack that *could* feed it.

---

## The six skills — status is PROPOSED; correct any label

| Skill | What it does | Proposed status | Why |
|---|---|---|---|
| `heygen-avatar` | Create a persistent HeyGen avatar (face+voice) via prompt/photo | **KEPT — reference** | You built your blue-polo Avatar IV in the GUI. This skill *creates* avatars via API — kept for reference, not wired live. |
| `heygen-video` | Generate HeyGen presenter video via the v3 Video Agent API | **DEPRECATED — dead path** | This is the API/Video-Agent auto-render you settled as rejected (2026-06-19). Superseded by `package-video`. Preserved + labeled so it can't fire by accident. |
| `higgsfield-product-photoshoot` | Brand-quality product/social images, ad creative, thumbnails | **CANDIDATE — creative/thumbnails** | Strongest fit for real THUMBNAILS + ad creative. Decide: is this your canonical creative-image tool alongside Blotato's in-feed Nano Banana? |
| `higgsfield-soul-id` | Train a Soul Character (a model on your face) for Higgsfield | **CANDIDATE — pairs with Higgsfield** | Only useful if you adopt the Higgsfield image path above (gives identity-faithful images of you). |
| `higgsfield-marketplace-cards` | Amazon-style product LISTING cards (main + A+ modules) | **KEPT — out of scope for social** | E-commerce listings, not social posts. Preserved here for completeness; not part of the social pipeline. |
| `imagegen` | Generic raster image generate/edit (Codex system skill) | **KEPT — generic fallback** | Overlaps with the image tool you keep above. Preserved as a no-frills generic backup. |

### The two open decisions (yours to rule)

1. **Image path.** Live system = Blotato Nano Banana (in-feed). Higgsfield =
   higher-end thumbnails/creative. Keep both with clear roles, or pick one?
2. **HeyGen API skills.** `heygen-video` + `heygen-avatar` are the API path you
   render around by hand. Stay deprecated-but-kept, or promote either to live?

Until you rule, everything stays exactly as preserved here.

---

## Duplicate map (what this folder consolidates)

Each skill currently exists in two places; this repo becomes the canonical third
that the others can eventually point to or be retired toward (non-destructively):

| Skill | Other copy 1 | Other copy 2 |
|---|---|---|
| heygen-avatar | `~/Desktop/skills/Ai-social-media-System-Skills/` | `~/.claude/skills/heygen-skills/` |
| heygen-video | `~/Desktop/skills/Ai-social-media-System-Skills/` | `~/.claude/skills/heygen-skills/` |
| higgsfield-product-photoshoot | `~/Desktop/skills/Ai-social-media-System-Skills/` | `~/.agents/skills/` |
| higgsfield-marketplace-cards | `~/Desktop/skills/Ai-social-media-System-Skills/` | `~/.agents/skills/` |
| higgsfield-soul-id | `~/Desktop/skills/Ai-social-media-System-Skills/` | `~/.agents/skills/` |
| imagegen | `~/Desktop/skills/Ai-social-media-System-Skills/` | `~/.codex/skills/.system/` |
