# Smart Mail — Engineering Specification

## What / why
Smart Mail is NayaNET's internal asynchronous intentional message-delivery layer. It is not ordinary external email and is distinct from live instant messaging.

Recipients can be individuals, selected people, connection groups, Smart Spaces, or other authorized audiences supported by the platform. Messages may reference Smart Notes, Smart Lists, Favorites, audio or other supported intelligence/media.

## Human interface
Inbox + composer. The composer must make **WHO receives this?** unmistakable before send. Show sender, audience, message, attached intelligence, delivery state and read state where supported. Provide search/filter/archive behavior according to the actual message contract.

## Front end requirements
- Inbox route and message detail/thread view.
- Compose flow with recipient/audience picker.
- Audience preview before send.
- Intelligence attachment picker referencing canonical objects.
- Read/unread and delivery state.
- Search/filter.
- Loading/error/empty/unauthorized states.
- Clear distinction from instant messaging and Space posting.

## Back end requirements
- Message persistence and inbox projection.
- Recipient resolution and eligibility check at send time.
- Communication preferences and audience constraints.
- Object-level authorization for attached intelligence.
- Stable message IDs, sender, recipients, timestamps and delivery state.
- Idempotent send behavior.
- Event/receipt recording for meaningful delivery.
- Large-audience abuse/rate controls where supported.

## Data / API contract
Conceptual message: `id, sender_id, recipient_type, recipient_ids/space_id, subject, body, attachment_refs, created_at, delivered_at, read_state, delivery_state`. These are design requirements, not claims that these exact tables/routes exist.

Conceptual APIs: compose/send, inbox retrieval, message detail, read/archive, recipient search and attachment lookup. Reuse current messaging/identity primitives.

## Connections
`Connections → recipients`; `Spaces → audience`; `Lists/Notes/Favorites → intelligence references`; `Smart Share → explicit sharing`; `Feed → mail activity`; `Ledger → delivery/provenance`; `Today/Reports → meaningful communication outcomes`.

## Security rule
`MESSAGE DELIVERY ≠ INTELLIGENCE ACCESS`. Being connected, being a Space member, or being able to send a message does not grant access to protected intelligence.

## Verification
Send to one real member; verify inbox receipt; attach authorized intelligence; test unauthorized attachment; test group/Space delivery; refresh; verify delivery/read state; test duplicate send; test revocation/eligibility at use time.

## Current state
**DEFINED** by `.naya/11`; the source explicitly states runtime implementation remains to be verified.

## Gap / next action
Inspect actual NayaNET messaging primitives and prove individual → group/Space delivery plus intelligence-reference authorization.

## Source authority
`.naya/2026-09-11-NAYAPOWER-11-SMART-MAIL-SMART-NOTE.md`; `.naya/2026-09-12-NAYAPOWER-47-SMART-SPACE-CONTRACT.md`; `.naya/2026-09-12-NAYAPOWER-46-IDENTITY-PRIVACY-PUBLICATION-CONTRACT.md`.


## COMPLETION CHECKLIST — 2026-09-19

- [x] Source contract identified
- [x] .naya authority identified
- [x] Live Edge Function v12 identified
- [x] Live mail tables identified
- [x] Authenticated send/receiver verification proven historically
- [ ] Current Hub UI mapped to live backend
- [ ] Two-real-user denial proven at current product surface
- [ ] Product-surface replay/idempotency proven
- [ ] Current source → build → runtime parity captured
- [x] Dated activity record exists
- [x] One next action recorded

**Current state:** IMPLEMENTED; complete current-surface closure remains. See [2026-09-19 activity](../ACTIVITY/2026/09/19/SMART-MAIL.md).
