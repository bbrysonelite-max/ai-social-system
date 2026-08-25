# YouTube-first → Facebook-announce loop

The distribution model for packaged videos. **YouTube is the compounding hub;
the socials are the megaphone that drives Brent's existing audience to it.**

## The loop (per video)

1. **YouTube** gets the full 16:9 captioned master — **private-first**; Brent reviews,
   then flips it public (or schedules). Title + description carry the
   `stan.store/brentbryson` free-guide link. This is the hub: searchable, compounds.
2. **Facebook** (Brent's strongest following) announces it the **same day**:
   - Post a **native teaser clip** (a 15–40s hook cut of the master) — NOT a bare link.
     Facebook throttles posts that send people off-platform but pushes native video.
   - Put the **YouTube link in the FIRST COMMENT, not the post body** (same throttle).
3. **Instagram** — same teaser as a Reel + "link in bio".
4. **X** — teaser clip + link directly in the post (X doesn't throttle links).

The teaser is a CUT of the captioned master — captions inherited, never re-added.

## Deliver a review folder

Build a folder (model: `~/Desktop/YouTube-Loop-Review/`) so Brent can review before
anything posts:

```
0_README.txt                       what each file is + caveats
1_youtube_master_16x9_captioned.mp4   the hub video
2_facebook_teaser_16x9_15s.mp4        native FB clip / IG Reel
3_thumbnail.png                       still option for an image post
4_ANNOUNCE_copy.txt                   ready-to-paste FB / IG / X copy
```

Teaser cut: `ffmpeg -y -i master.mp4 -t 15 -c copy teaser.mp4` (end on a beat if the
clip has one). Thumbnail: extract a frame with the name strip + a caption visible.

## Copy rules (compliance + voice)

- **No income/earnings/guarantee claims.** Opportunity + biography framing only —
  Brent's 39-year record is biography, never an earnings promise.
- **Audience skews ~85% women** — keep the voice warm and relational.
- **Thesis through-line:** AI to build your OWN distribution organization (not
  products, not "the business"). Pair with the follow-up spine where it fits.
- CTA destination: the lead magnet / `stan.store/brentbryson` — never a cold checkout.

## Copy template (fill the hook from the actual clip)

```
FACEBOOK (post body):
[1–3 line hook in Brent's voice, pulled from what he actually says in the clip]
Full video on my YouTube 👇 (link in the comments)

FACEBOOK first comment:
👉 [paste YouTube link]
Free guide — build your own distribution org with AI: stan.store/brentbryson

INSTAGRAM (Reel caption): [short hook] · Full video on YouTube — link in bio · stan.store/brentbryson
X: [hook] · Full breakdown 👇 [paste YouTube link]
```

Actual scheduling/posting goes through the `blotato-post` / `cadence` skills after
Brent approves — this skill only prepares the package and the copy.
