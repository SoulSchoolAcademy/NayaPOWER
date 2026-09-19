# JOB 04 — SMART MAIL
## Mission
Turn the proven Smart Mail backend into a complete authenticated product surface inside the canonical Hub.

## Current known state
Live `nayanet-smart-mail` v12 is JWT-protected. Current evidence includes 64+ threads/messages in the recent audit and 130 members. Historical production closure proved authenticated send → receiver verification → receipt/cognition/Ledger.

## Job
Map the current Mail UI to v12 and close the remaining authenticated product boundary.

## Build
- Preserve existing visual Mail design.
- Map threads, messages, members, compose/send, read/delivery states, recipient selection/preview, and attachments.
- Validate authorization at read and at send.
- Attachment access must be authorized at the moment of use.
- Preserve message provenance and resulting execution/cognition/Ledger lineage.
- Prove recipient/receiver verification.
- Prove replay/idempotency for sends.
- Prove owner/member isolation with a real second user where possible.
- Handle loading, empty, error, unauthorized, and delivery states truthfully.
- Prove Cloudflare source/build/runtime parity.

## Acceptance
An authenticated user can compose and send a real message, recipient can receive/verify it, consequences are observable, unauthorized attachment/access is denied, and reload preserves state.

## Handoff
Update Mail activity/checklist/report and coordinate any Share/Spaces integration through canonical authorization.
