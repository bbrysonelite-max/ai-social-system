# AGENTS.md

## Repository purpose

This repository is the canonical social-content and distribution system for:

- Facebook
- Instagram
- X

## Hard prohibition

Do not create, schedule, upload, publish, verify, or manage YouTube content from this repository.

YouTube and long-form video production belong exclusively in the separate `youtube-video-studio` repository.

## Publisher rule

Blotato is the current publisher adapter, not the architecture.

Keep all editorial logic, voice rules, approval gates, cadence, and state tracking provider-neutral so the publisher can be replaced later.

## Approval rule

Never post or schedule without Brent's explicit approval.

## Source boundaries

- `vault-personal`: source material and voice
- `tigerclaw-primitives`: Tiger Claw visual and motion primitives
- `youtube-video-studio`: YouTube and video production
- `ai-social-system`: Facebook, Instagram, and X only
