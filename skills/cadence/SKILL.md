---
name: cadence
description: >-
  Weekly-batch content cadence system for Facebook, Instagram, and X only.
  Use when Brent says "run the weekly batch", "run cadence", "build this week's posts",
  or "schedule the week". Drafts and schedules approved social posts behind a mandatory
  human approval gate. Never touches YouTube.
---

# Cadence

The weekly orchestration layer for Brent's social-content system.

## Hard channel boundary

This skill supports only:

- Facebook Pages
- Instagram business or creator accounts
- X

YouTube is out of scope. Do not create, upload, schedule, verify, or manage YouTube content from this repository.

## Responsibilities

1. Verify the prior week's Facebook, Instagram, and X posts.
2. Compute the current weekly volume from `state.json`.
3. Re-verify live account IDs.
4. Pull fresh source material and enforce the no-repeat ledger.
5. Run `write-content` for voice-true platform drafts.
6. Build required Instagram visuals and optional Facebook/X visuals.
7. Assign explicit send times.
8. Present the complete batch for Brent's approval.
9. Schedule only after explicit approval.
10. Confirm every submission through the active publisher and update state.

## Publisher adapter

Blotato is the current provider, but cadence must treat it as a replaceable adapter.

Editorial logic, platform copy, approval rules, idea selection, and state tracking must not depend on Blotato-specific concepts beyond the adapter boundary.

Each approved post must be normalized to this provider-neutral contract before submission:

```text
platform: facebook | instagram | x
accountRef: stable internal account reference
text: final approved copy
media: zero or more approved media URLs
scheduledTime: ISO-8601 UTC
ideaSlug: no-repeat ledger key
approvalRecord: explicit Brent approval reference
```

The adapter must return:

```text
provider
providerPostId
platform
scheduledTime
status
publicUrl (when available)
errorMessage (when applicable)
```

## Source priority

1. Brent's current work, experiments, and lessons
2. `vault-personal`, including books, stories, frameworks, and Wispr transcripts
3. approved long-form source material
4. the social idea bank

Every selected idea receives a unique slug checked against `state.json.usedIdeas`.

## Approval gate

Nothing is scheduled or posted without Brent's explicit approval.

Accepted approval must be unambiguous, such as:

- approved
- yes, schedule these
- go

Silence, partial review, or "looks good" without clear authorization is not approval.

## Platform rules

### Facebook

- A connected Facebook Page is required.
- Text-only posts are allowed.
- Media is optional when it adds value.

### Instagram

- At least one approved media asset is required.
- Skip the individual post cleanly if media generation fails.

### X

- Text, media posts, and approved threads are allowed.
- Respect current platform limits and adapter validation.

## Verification

Never claim a post is scheduled or published based only on a submission response.

Confirm each post through the provider's status endpoint and record:

- scheduled
- published
- failed
- pending

Surface errors without automatically retrying unless Brent has approved a retry policy.

## Out of scope

- YouTube
- autonomous posting without approval
- changing approved copy inside cadence
- generating presenter video
- video-studio workflows
- redefining Brent's voice
