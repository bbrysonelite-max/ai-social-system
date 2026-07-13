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
  → Blotato
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
| 2 | `skills/blotato-post` | Approved production publisher for Facebook, Instagram, and X. |
| 3 | `skills/cadence` | Weekly orchestration, no-repeat ledger, approval gate, scheduling, and verification. |

## Publisher decision

**Blotato is the approved production publisher for Facebook, Instagram, and X.**

This decision is settled by Brent. Agents must not reopen publisher selection, propose migrations, or add competing publisher integrations unless Brent explicitly asks to reconsider it.

The internal post contract should remain clean and well-defined so the system is maintainable, but no active migration or shadow-provider project is authorized.

## Approval law

Nothing is posted or scheduled without Brent's explicit approval.

## Repository boundaries

- `ai-social-system`: Facebook, Instagram, and X content and distribution through Blotato
- `youtube-video-studio`: Two Brents YouTube and video production
- `tigerclaw-primitives`: Tiger Claw visual and motion primitives
- `vault-personal`: source material, stories, voice, books, and Wispr transcripts
