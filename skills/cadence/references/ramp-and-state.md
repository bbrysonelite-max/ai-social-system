# Ramp + State Reference

**Date:** 2026-06-17
**Source:** `docs/superpowers/specs/2026-06-17-cadence-system-design.md` (Ramp table + Architecture § Components 1–2).

---

> **Scope of this file:** the locked volume ramp, the week arithmetic, the `state.json` schema, and the update rules that keep the no-repeat ledger current. Channel IDs and post construction are in `skills/blotato-post/references/`. Voice and drafting are in `skills/write-content/references/`.

---

## The ramp

This table is locked. Do not adjust volumes, phases, or channel scope without an explicit instruction from Brent.

| Week | Posts/day/channel | Channels | Total/week |
|---|---|---|---|
| 1 | 1 | FB, IG, X (text+image) + YouTube (1 video/day) | 21 + 7 YT |
| 2 | 2 | " | 42 |
| 3 | 3 | " | 63 |
| 4+ | 4 | " | 84 (= 12/day across 3 channels) |

> **Note on Total/week:** The 1→4 ramp applies to **FB, IG, and X** (text+image). **YouTube is a daily video channel** — **1 video/day, every day** (account `27755`, channel `@BrentBrysonaios`; verified live 2026-06-19). It does not follow the 1→4 ramp; it's a steady daily lane. Each YouTube post needs a **video** at a public URL and is uploaded **PRIVATE-first** via `scripts/youtube-autoload.sh` for Brent's review. Remaining build: automatic daily-video generation (HeyGen) to feed it.

**7 days/week.** Volume is per channel per day. The ramp advances automatically by calendar week from `startDate` — no manual override is needed.

---

## Computing the current week's volume

### Arithmetic

```
week             = floor((today - startDate) / 7) + 1
perDayPerChannel = min(week, 4)
```

- `today` and `startDate` are both calendar dates (date only, not datetime). Subtract as whole days.
- `floor(...)` rounds down — if 9 days have elapsed, `floor(9/7) = 1`, so `week = 2`.
- Cap at 4. Once `week >= 4` the daily volume is always 4/channel.

### Worked example

Suppose `startDate = "2026-06-17"` and today is `"2026-07-08"` (21 days elapsed):

```
week             = floor(21 / 7) + 1  =  floor(3) + 1  =  4
perDayPerChannel = min(4, 4)          =  4
```

A 7-day batch starting 2026-07-08 would draft **4 × 3 channels × 7 = 84 posts (FB/IG/X)**, **plus 7 YouTube videos** (1/day) staged private-first.

Second example — today is `"2026-06-24"` (7 days elapsed):

```
week             = floor(7 / 7) + 1  =  1 + 1  =  2
perDayPerChannel = min(2, 4)         =  2
```

That matches the Week 2 row in the ramp table (2 posts/day/channel, 56/week total).

---

## state.json schema

`skills/cadence/state.json` is the live source of truth for cadence progress. It persists across sessions; never overwrite it — only append.

| Field | Type | Purpose |
|---|---|---|
| `startDate` | ISO date string (`"YYYY-MM-DD"`) | The calendar date the ramp started. Used in the week arithmetic above. Never change this after the first batch. |
| `usedIdeas` | Array of idea slug strings | Every idea slug that has been posted or scheduled. **This is the no-repeat guard** — before drafting a post for any idea, confirm its slug is NOT in this array. |
| `scheduled` | Array of schedule entry objects | Record of every post submitted to Blotato. Append an entry immediately after `blotato_create_post` returns a `postSubmissionId`. |

### `scheduled` entry shape

```json
{
  "postSubmissionId": "<UUID returned by blotato_create_post>",
  "platform": "<blotato platform string, e.g. twitter, facebook, instagram, youtube>",
  "scheduledTime": "<ISO-8601 UTC datetime string>",
  "ideaRef": "<slug of the idea this post was drafted from>"
}
```

All four fields are required. `ideaRef` ties the schedule entry back to the idea bank and cross-references `usedIdeas`.

---

## Update rules

After every batch completes (after Brent approves and all `blotato_create_post` calls succeed):

1. **Append to `usedIdeas`** — add the slug of every idea used in the batch. Order does not matter; duplicates must not be added (check before appending).
2. **Append to `scheduled`** — add one entry per post submitted, using the `postSubmissionId` returned by Blotato, the platform string, the scheduled time (ISO-8601 UTC), and the idea slug.
3. **Do not touch `startDate`** — it is set once at initialization and never changed.
4. **Do not remove entries** — `usedIdeas` and `scheduled` are append-only ledgers. Removing an entry would allow repeat posts.

The `usedIdeas` ledger is authoritative. If an idea slug appears there, it must not be drafted again — even if the original post was cancelled, deleted, or never fired. When the idea bank is exhausted (all slugs appear in `usedIdeas`), report this to Brent before running the batch and ask which ideas may be recycled.
