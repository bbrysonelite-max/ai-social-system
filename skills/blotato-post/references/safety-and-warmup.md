# Safety + Warm-Up Reference

**Date:** 2026-06-17
**Source:** `docs/superpowers/plans/2026-06-17-blotato-post-skill.md` (Pre-Publish Safety Rubric + Global Constraints); `Global Constraints` warm-up bullet (primary source; `docs/account-warm-up-plan.md` not yet merged).

---

> **Scope of this file:** guardrails only. Account IDs and per-platform required fields are in
> `accounts-and-channels.md`. Tool mechanics are in `pipeline.md`. This file is the
> GATE + RUBRIC + WARM-UP layer — read it before calling any `blotato_create_post`.

---

## The human gate

**Nothing is scheduled or published without Brent's explicit approval.** No exceptions. No autonomous posting, ever.

Before calling `blotato_create_post` for any post on any platform, stop and present Brent with:

1. The **exact text** that will be sent (character-for-character — no "close enough").
2. The **visual** (URL or preview) that will be attached.
3. The **scheduled time** (ISO-8601 UTC).
4. The **target platform(s)** with their live `accountId`.

Wait for an explicit "yes," "approved," "go," or equivalent affirmative. Silence, inaction, or "looks good" without a clear approval word is **not** approval.

If Brent says no, requests a change, or does not respond — **do not call `create_post`**. Revise and re-present.

There is no context — no urgency, no backlog, no "just schedule it" — that bypasses this gate.

---

## The 5-criterion safety rubric

A post may be scheduled only if **all five criteria pass.** Run this check for every post in the queue. Print one rubric line per post (see format below) before presenting the approval gate.

1. **Human-approved** — Brent has explicitly approved this exact text + visual + scheduled time. (No approval → do not call `create_post`.)
2. **Account-valid** — `accountId` resolved from a fresh `blotato_list_accounts`; all platform-required fields present (FB `pageId`, IG `mediaType`, YouTube `title`+`privacyStatus`). If a required field can't be satisfied (e.g. FB has no Page), the platform is **skipped with a clear message**, never sent broken.
3. **Voice/compliance intact** — text originated from `write-content` (passed its 5-criterion rubric) and was not mutated; if it was altered for platform fit, `write-content`'s gate was re-run and passed. Captions/titles/alt-text introduce no `never-say.md` violations.
4. **Warm-up respected** — scheduled (not immediate) unless Brent said "post now"; CTA is reach-safe for the current account state; not identical copy cross-posted same-minute.
5. **Media-valid** — `mediaUrls` are public and reachable; platform media constraints satisfied (IG = story/reel; YouTube = video).

### Rubric output format

Verify criteria 2–5 BEFORE presenting to Brent; criterion 1 (Human-approved) is always `PENDING` at presentation time and flips to `PASS` only on his explicit approval.

Print one line per post before the approval gate, like this:

```
[Platform] [AccountId] — Human-approved: PENDING | Account-valid: PASS | Voice/compliance: PASS | Warm-up: PASS | Media-valid: PASS
```

Replace `PENDING` with `PASS` only after Brent has given explicit approval in this session. A post with any criterion at `FAIL` is **not schedulable** — skip it with a clear reason. A post with criterion 1 at `PENDING` is **held at the gate** until Brent's explicit approval flips it to `PASS`; once all criteria are `PASS` the post may be scheduled.

Example (pre-approval presentation):

```
Instagram 53674 — Human-approved: PENDING | Account-valid: PASS | Voice/compliance: PASS | Warm-up: PASS | Media-valid: PASS
YouTube   27755 — Human-approved: PENDING | Account-valid: PASS | Voice/compliance: PASS | Warm-up: PASS | Media-valid: PASS
Facebook  37125 — Human-approved: PENDING | Account-valid: PASS | Voice/compliance: PASS | Warm-up: PASS | Media-valid: PASS
X         12730 — Human-approved: PENDING | Account-valid: PASS | Voice/compliance: PASS | Warm-up: PASS | Media-valid: PASS
```

After approval, flip `PENDING` → `PASS` and proceed to `create_post`.

---

## Warm-up ramp

New and reconnected accounts need a warm-up period before reaching audience. Blasting volume too early or posting raw links suppresses reach — sometimes permanently.

### Default mode: warm-up

**This skill operates in warm-up mode (Phase 1) by default.** The skill NEVER auto-advances phases. It advances only when Brent explicitly instructs it to — for example: "move to ramp," "advance to phase 2," "we're warm now, turn on links," or "go to full volume." The final account state is **"warm"** (reached at Phase 3 — scale — when reach is stable and Brent says so); "warm" is a Brent-declared destination, not something the skill reaches on its own. Until Brent gives an explicit advance instruction, apply the warm-up constraints below to every post.

> **Vocabulary mapping — `write-content` ↔ `blotato-post`:** `write-content` uses a two-state axis (`warm-up` | `warm`) to drive CTA mode. These map onto this skill's three phases at different granularity:
> - `write-content` **`warm-up`** ↔ this skill's **Phase 1 (warm-up)** — native-value posts, reach-safe CTAs, no external links.
> - `write-content` **`warm`** (direct links allowed) ↔ this skill's **Phase 2 (ramp) or Phase 3 (scale)** — `warm` in write-content means the account has passed the cold/warm threshold, not that it has reached maximum volume. A `warm` draft from write-content is therefore treated here as Phase 2+ content (soft or direct CTAs are acceptable), NOT as still-cold. Brent must have explicitly advanced to ramp or scale before such a draft is scheduled.
> The three-phase model here is more granular than write-content's two-state model; both describe the same underlying account readiness axis.

### Volume targets

| Phase | FB + IG | X/Twitter | YouTube | Notes |
|---|---|---|---|---|
| **Warm-up** (default) | ~3–5 posts/week | ~1–2 posts/week | 1 post/week | Native value only; no external links |
| **Ramp** | 5–10 posts/week | 3–5 posts/week | 2–3 posts/week | Reach-safe CTAs; monitor reach before each step |
| **Scale** | Daily or near-daily | Daily | Weekly+ | Raw links OK once reach is stable and growing |

Brent must explicitly move from warm-up → ramp → scale. The skill does not auto-advance.

### What "native value" means in warm-up

During warm-up, every post must deliver value inside the platform — the reader must not need to leave to get the point.

- **No cold external links** to checkout pages, sign-up pages, or anything that requires a click away. If the value lives off-platform, save it for ramp/scale.
- **Reach-safe CTAs only:** comment-to-get prompts ("Comment FREEDOM and I'll send it"), DM keyword triggers, and save/share asks are all safe. Raw links are not.
- If reach drops on any platform across two consecutive posts, pause that platform and report it to Brent before scheduling more.

### Three phases in brief

**Phase 1 — Warm-up (current default)**
Low volume (~3–5/wk FB+IG, ~1–2/wk X). Native-value posts only. No external links. CTAs are engagement-based (comment, DM keyword). Goal: establish consistent signal to the algorithm.

**Phase 2 — Ramp**
Moderate volume (5–10/wk FB+IG, 3–5/wk X). Reach should be stable or climbing before entering this phase. Soft CTAs (link in bio, "DM me") become acceptable. Monitor reach after every batch.

**Phase 3 — Scale**
Higher volume and direct CTAs (checkout links, Tiger landing pages, webinar sign-ups) once reach is strong and Brent has confirmed the account is healthy. Do not reach this phase without explicit sign-off.

---

## Hard rules

These rules have no exceptions. No context — urgency, backlog, or operator instruction — overrides them.

1. **Never blast identical copy same-minute.** Do not schedule the same text to multiple platforms at the same scheduled time. Stagger by at least 30 minutes, or vary the caption to fit the platform. Identical simultaneous cross-posts are a spam signal.

2. **Never cold-link Tiger.** Do not include a direct link to a Tiger Claw checkout, sign-up, or onboarding page in any post during warm-up phase. Wait for scale phase and explicit approval from Brent.

3. **Never publish immediately by default.** `scheduledTime` is always set. The only exception is when Brent explicitly says "post now" — and even then, confirm before calling `create_post`.

4. **Never post to a platform missing a required field.** If a platform's required field cannot be satisfied (e.g. Facebook has no Page in `subaccounts`, or an Instagram post has no `mediaType`), skip that platform and deliver a clear message. Do not error out silently, do not guess, do not send a broken post. Example skip message for Facebook:

   > "Facebook has no Page connected in Blotato — connect a Page (dashboard: 'Facebook pages: Don't see your pages? Help') to enable FB posting."

   Continue posting to all other platforms that have valid required fields.
