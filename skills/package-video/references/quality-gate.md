# Quality Gate — clone check + pre-publish checks

**This posts publicly under Brent's name. Nothing ships until every box below is
checked AND Brent has reviewed the PRIVATE upload.** Two gates: one on the clone
coming IN, one on the package going OUT. The gate is mandatory — no batch size,
deadline, or "just post it" overrides it.

---

## Approved clones — the ONLY looks allowed

Source of truth: Brent's approved-clone registry
(`~/Documents/New project/Brent's Favorite Clones/`). **Canonical look = blue-polo
Avatar IV.**

| Look | HeyGen ID(s) | Status |
|---|---|---|
| **Blue-polo Avatar IV** (canonical) | render `a1d0c5d8…` · Seedance ref `105da2e9…` | ✅ approved 2026-05-26 |
| Black-hoodie "3 Tools" | completed `c1b96c9c…` | ✅ approved 2026-05-26 |

**DO NOT USE** (Brent rejected / wrong lane):
- `dc9823ab…` — wrong clone, **rejected by Brent**.
- `5b175330…` and the portrait digital-twins — legacy new-render lane only.
- Anything not in the approved list above.

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
