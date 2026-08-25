# Quality Gate — clone check + pre-publish checks

**This posts publicly under Brent's name. Nothing ships until every box below is
checked AND Brent has reviewed the PRIVATE upload.** Two gates: one on the clone
coming IN, one on the package going OUT. The gate is mandatory — no batch size,
deadline, or "just post it" overrides it.

---

## Approved clones — the ONLY looks allowed

> ## 🚫 NEVER GENERATE A CLONE. EVER.
> The video source is **ALWAYS one of the two finished approved clips below, used
> AS-IS.** Do NOT render, generate, or create an avatar video — not Avatar III / IV /
> V, not Video Agent, not photo avatars, not "just a probe." **Every generated render
> has been rejected as dog shit.** These two clips are the only good clones. Package
> them; never make a new one.

**Source of truth: the two clones in Brent's HeyGen "Brent clone 2" folder**
(confirmed by Brent + verified live 2026-06-22). These two finished MP4s ONLY:

| Clone | HeyGen ID | Verified | Role |
|---|---|---|---|
| **3 Tools** | `1adc7ebdf9b54e0fa3d94b129798a85d` | 16:9 1920×1080, audio ✅ | full content clip (~5 min) |
| **Blue shirt** | `d5920d626aa042ad85d45f2a9c410ca1` | 16:9 1920×1080, audio ✅ | full content clip (~4 min); HeyGen title "blue shirt appoved clone" |

⚠️ **`a1d0c5d8…` is NOT a usable clone** — it's an 8-second render *test*. It was
wrongly treated as "the blue shirt" 2026-06-22; the real blue shirt is `d5920d62…`.

These are **finished clips, posted AS-IS** (no render — every render is rejected).
Reusing the same clone repeatedly is fine.

**DO NOT USE:**
- `dc9823ab…` — wrong clone, **rejected by Brent**.
- `5b175330…` and the portrait digital-twins — legacy new-render lane only.
- **Old-registry IDs `c1b96c9c…` / `105da2e9…` (Seedance) are SUPERSEDED** by the two
  verified IDs above — the `Brent's Favorite Clones` registry is stale (Buffer-era).
- Anything not in the two approved IDs above.

### ⚠️ Stale registry data — DO NOT follow it
The registry json is from the **Buffer era (2026-05-26)** and is wrong on two points
the gate must OVERRIDE:
- It defaults `aspect_ratio: 9:16` and avatars `preferred_orientation: portrait`.
  **DEAD — 16:9 landscape ONLY.** 9:16 is rejected outright.
- It references the **Buffer** workflow. **DEAD — posting is Blotato.**

---

## GATE A — CLONE-IN  (check the clip BEFORE packaging)

- [ ] **Approved look** — blue-polo Avatar IV (canonical) or black-hoodie. NOT a
      rejected/legacy avatar (`dc9823ab`, `5b175330`, portrait twins).
- [ ] **16:9 landscape, 1920×1080, full-width** — `ffprobe` confirms it. Never 9:16.
- [ ] **Approved voice, clean audio** — the embedded approved voice; no robotic
      artifacts, no wrong/legacy voice.
- [ ] **Render is clean** — tight lip-sync, face clearly visible, no garbling,
      glitching, or warping.
- [ ] **Says the approved script** — the words match what was written + approved.
- [ ] **Duration sane** for the format (long-form ~5–8 min; teaser cut from it).

If any box fails → **stop. Do not package.** Get a clean 16:9 approved clip from
HeyGen first.

---

## GATE B — PUBLISH-OUT  (check the package BEFORE staging)

- [ ] **Captions baked exactly once** — clean readable rail, not flashy. No cut is
      re-captioned.
- [ ] **Lower-third = NAME ONLY** — no tenure / rank / income / credential. (The
      "39 Years in Network Marketing" lower-third was the exact mistake this prevents.)
- [ ] **CTA card** = `stan.store/brentbryson`, no income/earnings promise.
- [ ] **Thumbnail** — real photo, no claims, 1280×720 (via `make-thumbnail`).
- [ ] **Compliance scrub** — no income / earnings / guarantee / health / rank claims
      anywhere: title, description, captions, overlay, thumbnail.
- [ ] **Verified by looking** — frames extracted and eyeballed; never trust a
      success line.

---

## The human gate (last step, never skipped)

- [ ] **Staged PRIVATE-first** via `youtube-autoload.sh` (default private).
- [ ] **Brent reviews the private upload.**
- [ ] **Brent flips it public** (or it auto-publishes only if he scheduled it).

**Claude never makes a video public under Brent's name. Brent does.**
