# ai-social-system

The parent project for Brent Bryson's autonomous content factory — high-volume,
high-integrity social content in his own voice, batched once a week and distributed
across every connected channel.

> **Status: BONES.** Structure and design only. Skills are stubs until fleshed out.

## The model

Adopted from Sabrina Ramonov's (founder of Blotato) "content factory" process:
~250 pieces/week, batched in ~1 hour, every piece reviewed for brand voice before
it goes live. Human stays in the loop on creative direction; AI handles volume.

Pipeline: **idea → voice-true drafts → visuals + scheduling → weekly feedback loop.**

## The two skills (built in this order)

| Order | Skill | Job | Depends on |
|---|---|---|---|
| 1 | `skills/write-content` | Turn one idea into platform-specific posts **in Brent's voice**. Drafting only — no posting. | Voice sources (local) |
| 2 | `skills/blotato-post` | Generate visuals + schedule/post drafts across connected channels via the Blotato MCP. | Blotato MCP (loads on fresh session) |

The split is deliberate: Skill 1 has no external dependency and is built/tested first;
Skill 2 needs the Blotato MCP tools, which only load after a session restart.

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
│   ├── write-content/          # Skill 1 (voice) — stub
│   └── blotato-post/           # Skill 2 (distribution) — stub
└── content-db/                 # weekly content-idea database — bones
```
