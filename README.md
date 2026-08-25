# ⚠️ RETIRED (2026-07-23)

This system was consolidated into two living systems:

- **SOCIAL system** → private repo `brag-machine` (voice engine, cadence engine, warm-up, funnel, and Blotato REST knowledge absorbed there under `voice/`, `cadence/`, `docs/`)
- **YOUTUBE system** → Two Brents (~/Desktop/YOUTUBE; youtube-autoload.sh + HeyGen handoff moved there)

Nothing runs from this repo anymore. Kept for history.

---

# ai-social-system

The parent project for Brent Bryson's autonomous content factory — high-volume,
high-integrity social content in his own voice, batched once a week and distributed
across every connected channel.

> **Status: LIVE.** All three skills built, merged, and posting to production —
> FB, IG, X daily since 2026-06-17; **YouTube live since 2026-06-19** (daily video
> channel, auto-uploaded private-first for review).

## The model

Adopted from Sabrina Ramonov's (founder of Blotato) "content factory" process:
~250 pieces/week, batched in ~1 hour, every piece reviewed for brand voice before
it goes live. Human stays in the loop on creative direction; AI handles volume.

Pipeline: **see what's owed → pick an idea → research it → voice-true draft → visuals + scheduling → verify it published.**

## The skills (in run order)

`cadence` wraps the run: it **opens** by checking the schedule (what published, what's
**owed** this week), and **closes** by scheduling the approved batch. In between, each
owed slot flows through research → draft → visuals.

| Step | Skill | Job | Depends on |
|---|---|---|---|
| **open** | `skills/cadence` | Verify last week published; compute what's **owed** this week (ramp volume, gaps, no-repeat ledger). This scopes everything below. | state.json |
| 1 | `skills/research-content` | Pick an idea from the bank to fill an owed slot; **research it** into a brief (facts, the hook, sources). Research only. | Idea bank, WebSearch, `last30days` |
| 2 | `skills/write-content` | Turn the brief into platform-specific posts **in Brent's voice**. Drafting only — no posting. | Research brief + voice sources |
| 3 | `skills/blotato-post` | Generate visuals + schedule/post drafts across channels via Blotato. | Blotato (REST; MCP loads on fresh session) |
| 3b | `skills/make-thumbnail` | Deterministic 1280×720 YouTube thumbnail (real photo + code-rendered headline). | headless Chrome |
| **close** | `skills/cadence` | On approval: schedule the batch, confirm each published, update state. | Steps 1–3 |

You can't write until you know what you're writing about — **research runs before
`write-content`** — and you don't research blind: **`cadence`'s "what's owed" check
runs before research**, so you only research what the schedule actually needs.

### Channels

- **Facebook, Instagram, X** — text+image, ramp **1→4 posts/day/channel** over 4 weeks.
- **YouTube** — **daily video channel** (channel `@BrentBrysonaios`, Blotato acct `27755`).
  Each post needs a video; uploads are **automatic and PRIVATE-first** via
  `skills/cadence/scripts/youtube-autoload.sh` (Blotato has no raw local-file upload,
  so the video must be at a public URL — daily HeyGen renders already are). Brent
  reviews the private video in the morning queue, then flips it Public (or it
  auto-publishes if scheduled). **He never uploads manually.**

## Positioning

The earned-authority voice on **why AI + person-to-person distribution matters for
direct sales, affiliate marketing, and network marketing.** The differentiator is
proof, not hype — three generational windows, Blue Diamond, 39 years in distribution.
(See `docs/DESIGN.md`.)

## Layout

```
ai-social-system/
├── docs/DESIGN.md              # full design / spec
├── skills/
│   ├── write-content/          # Skill 1 (voice)
│   ├── blotato-post/           # Skill 2 (distribution)
│   └── cadence/                # Skill 3 (weekly orchestration)
│       ├── references/         # ramp, REST contract, weekly procedure
│       ├── scripts/            # youtube-autoload.sh (hands-free YouTube upload)
│       └── state.json          # startDate, usedIdeas ledger, scheduled history
└── content-db/                 # weekly content-idea database
```
