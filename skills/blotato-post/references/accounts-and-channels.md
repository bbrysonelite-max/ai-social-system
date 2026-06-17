# Accounts + Channels Reference

**Date:** 2026-06-17
**Source:** `docs/DESIGN.md` "Connected channels" table; `skills/blotato-post/SKILL.md` (verified channel table + tool surface). All IDs live-verified via `blotato_list_accounts` + dashboard on 2026-06-17.

---

## Verified channels (snapshot)

> snapshot 2026-06-17; IDs can change on reconnect — re-verify at runtime (see `## Runtime rule: re-verify first` below).

| # | Platform | Account ID | Account | Postable? |
|---|---|---|---|---|
| 1 | **Facebook** | `37125` | Brent Bryson — Page `53954221244` ("Brent Bryson") | Yes (Page connected) |
| 2 | **Instagram** | `53674` | @brentbryson | Yes (visual-first: story or reel) |
| 3 | **YouTube** | `27755` | Brent Bryson | Yes |
| 4 | **X/Twitter** | `12730` | @pebobryson801 | Yes |

**Not connected:** LinkedIn (add once on paid plan — strong fit for long-form/authority content). TikTok (bio exists, not linked).

Subscription active. 0 posts scheduled at verification (clean slate).

---

## Per-platform required fields

These are the fields Blotato requires beyond `accountId` + `content` when calling `blotato_create_post`.

**Facebook**
- `pageId`: must be `53954221244` (the connected "Brent Bryson" Page).
- Pull `pageId` from the matching subaccount in `blotato_list_accounts` response — don't hardcode.
- Meta restriction: Blotato can only post to a Facebook **Page**, never a personal profile. The personal-profile following is large but NOT auto-postable.

**Instagram**
- `mediaType`: must be `story` or `reel`.
- No plain caption-only feed post is available via the API — every IG post must be visual-first (image, carousel, or reel with caption).
- Carousel: pass multiple image URLs in `mediaUrls`.

**YouTube**
- YouTube via Blotato is a **video upload**, not a community/text post.
- `title` (required — no title, no post).
- `privacyStatus`: `public` | `private` | `unlisted`.
- `shouldNotifySubscribers`: `true` | `false`.
- A video file URL must be included in `mediaUrls` — YouTube posts require a video.

**X/Twitter**
- No extra required fields beyond `accountId` + `content`.
- Threads: pass subsequent posts in `additionalPosts` array.

---

## Facebook Page handling

The Facebook Page IS connected as of 2026-06-17 (Page `53954221244`, account ID `37125`). All 4 channels are currently postable.

However: the FB account ID changed (`20306` → `37125`) when Brent reconnected and granted the Page. This is concrete proof that account state can change between runs.

**The skill must detect at runtime whether Facebook is postable:**
1. Call `blotato_list_accounts` (see Runtime rule below).
2. Find the Facebook account entry.
3. Check that it has a `subaccounts` array with at least one entry (the Page).
4. If `subaccounts` is empty or absent, **skip Facebook** with this message:

> "Facebook has no Page connected in Blotato — connect a Page (dashboard: 'Facebook pages: Don't see your pages? Help') to enable FB posting."

Do not error out; continue posting to the remaining channels.

---

## Runtime rule: re-verify first

**ALWAYS call `blotato_list_accounts` at the start of every run** and map platform→`accountId` from the live response. Never trust the snapshot IDs blindly — account IDs change on reconnect (proven: FB `20306` → `37125` on 2026-06-17).

Step-by-step:
1. Call `blotato_list_accounts`.
2. Map each platform to its current `accountId` and any required subaccount values (e.g., FB `pageId`).
3. Use those live values for all subsequent `blotato_create_post` calls.
4. If a previously connected account is no longer present, log the missing platform and skip it — do not abort the whole run.

The snapshot table above is a reference for expected state and required fields. The live response is the source of truth at post time.
