# AI Social System

Brent Bryson's social-content factory for **Facebook, Instagram, and X only**.

> **Hard boundary:** This repository never creates, schedules, uploads, publishes, or manages YouTube videos. YouTube and long-form video production belong exclusively in the separate `youtube-video-studio` repository.

## Mission

Turn Brent's real work, ideas, stories, and lessons into voice-true social posts, then distribute approved posts reliably across Facebook, Instagram, and X.

## Pipeline

```text
idea or source material
  → voice-true drafts
  → platform-specific visuals
  → Brent approval
  → publisher adapter
  → Facebook / Instagram / X
  → verification and performance feedback
```

## Active channels

- Facebook Pages
- Instagram business or creator accounts
- X

No YouTube account may be configured in this repository.

## Core skills

| Order | Skill | Responsibility |
|---|---|---|
| 1 | `skills/write-content` | Draft platform-specific posts in Brent's voice. Never publishes. |
| 2 | `skills/blotato-post` | Current publishing adapter for Facebook, Instagram, and X. |
| 3 | `skills/cadence` | Weekly orchestration, no-repeat ledger, approval gate, scheduling, and verification. |

## Publisher policy

Blotato remains the current production publisher, but it is an adapter—not part of the editorial core.

The system must keep a provider-neutral post contract so Blotato can later be replaced by Buffer, Postiz, Mixpost, or another approved publisher without rewriting voice, research, cadence, or approval logic.

No provider migration occurs until a shadow test proves all three active channels can:

1. authenticate reliably
2. accept text and required media
3. schedule at an exact time
4. return a durable post identifier
5. expose success or failure status
6. operate without touching YouTube

## Approval law

Nothing is posted or scheduled without Brent's explicit approval.

## Repository boundaries

- `ai-social-system`: Facebook, Instagram, and X content and distribution
- `youtube-video-studio`: Two Brents YouTube and video production
- `tigerclaw-primitives`: Tiger Claw visual and motion primitives
- `vault-personal`: source material, stories, voice, books, and Wispr transcripts
