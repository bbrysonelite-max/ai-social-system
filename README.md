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

Pipeline: **idea → voice-true drafts → visuals + scheduling → weekly feedback loop.**

## The three skills

| Order | Skill | Job | Depends on |
|---|---|---|---|
| 1 | `skills/write-content` | Turn one idea into platform-specific posts **in Brent's voice**. Drafting only — no posting. | Voice sources (local) |
| 2 | `skills/blotato-post` | Generate visuals + schedule/post drafts across connected channels via Blotato. | Blotato (REST; MCP loads on fresh session) |
| 3 | `skills/cadence` | Weekly-batch orchestration: ramp volume, no-repeat ledger, approve-first gate, schedule the week across all channels. | Skills 1 + 2 |

The split is deliberate: Skill 1 has no external dependency and is built/tested first;
Skill 2 talks to Blotato; Skill 3 orchestrates both into the durable weekly run.

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
