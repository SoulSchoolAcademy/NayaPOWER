# NAYANET INTELLIGENCE SHARING SYSTEM — TECHNICAL IMPLEMENTATION REPORT

**DATE:** September 8, 2026  
**STATUS:** CURRENT ARCHITECTURE / ENGINEERING CONTRACT  
**AUDIENCE:** All current and future NIS / Naya execution agents  
**SCOPE:** Intelligent Blocks, Smart Lists, Connections, Smart Mail, Smart Spaces, Smart Moments, Share, Copy, notifications, invitations

## 1. OBJECTIVE

Build one coherent intelligence-sharing system in which an Intelligent Block can be captured once and then safely reused across personal intelligence, collective intelligence, Smart Lists, Smart Mail, Smart Spaces, Smart Moments, and other authorized surfaces.

Do not create disconnected feature implementations. Treat the Intelligent Block as the canonical intelligence object and build relationships, delivery, membership, and presentation around it.

## 2. CORE DATA MODEL

### IntelligentBlock

Minimum conceptual fields:

- `block_id`
- `author_id`
- `created_at`
- `updated_at`
- `title`
- `type`
- `status`
- `in_a_nutshell`
- `human_note`
- `child_note`
- `grandma_note`
- `naya_note`
- `machine_note`
- `what_we_learned`
- `what_it_means`
- `source_refs`
- `evidence_refs`
- `connection_refs`
- `permissions`
- `visibility`
- `version`

The block should have a stable ID so other systems reference the same intelligence instead of creating uncontrolled copies.

## 3. SMART LIST MODEL

A Smart List is a named collection of Intelligent Block references.

Conceptual fields:

- `list_id`
- `owner_id`
- `name`
- `description`
- `scope` (personal / collective / other authorized scope)
- `created_at`
- `updated_at`
- `visibility`

Membership should be a separate relation:

- `list_id`
- `block_id`
- `added_by`
- `added_at`
- optional `position`

Do not restrict a block to one list. A block may belong to many lists.

Smart Lists must support:

- create;
- rename;
- delete/archive;
- search;
- add/remove blocks;
- multi-select;
- save from any eligible Intelligent Block;
- share a single list as a collection;
- preserve permissions of each underlying block.

## 4. CONNECTION MODEL

A Connection represents an authorized relationship with a person, AI agent, or other supported participant.

Conceptual fields:

- `connection_id`
- `owner_id`
- `participant_id`
- `participant_type` (human / AI / other authorized type)
- `status`
- `alias`
- `permissions`
- `created_at`

Connections must not be treated as unrestricted identity exposure.

Recipient selection must resolve to an authorized destination and respect privacy/consent rules.

## 5. SMART MAIL MODEL

Smart Mail is the communication and routing layer.

Conceptual entities:

### SmartMailMessage

- `message_id`
- `sender_id`
- `recipient_ids`
- `created_at`
- `subject`
- `body`
- `intelligence_refs`
- `list_refs`
- `space_refs`
- `reply_to`
- `permissions`
- `status`
- `delivery_metadata`
- `provenance`

### Delivery state

At minimum distinguish:

`DRAFT → AUTHORIZED → QUEUED → SENT → DELIVERED`

with failure states such as:

`FAILED` / `REJECTED` / `EXPIRED`

Never report a message as sent unless the system has evidence supporting the state.

## 6. SMART MAIL ROUTING

Preferred architecture:

`Human / Naya / Authorized AI`

→ `Smart Mail API`

→ `Authentication + Authorization`

→ `Recipient Resolution`

→ `Message Queue`

→ `Mail Delivery Service`

→ `Recipient`

→ `Delivery / Reply Event`

External systems may trigger or supply message content, but Smart Mail remains the NayaNET communication abstraction.

For an initial implementation, a human can create/copy/paste a message into Smart Mail and send it. Direct AI/API sending can be added once authentication, authorization, rate limiting, recipient resolution, and auditability are reliable.

## 7. SMART SPACE MODEL

A Smart Space is a permissioned shared intelligence environment.

Conceptual entities:

### Space

- `space_id`
- `owner_id`
- `name`
- `description`
- `created_at`
- `visibility`
- `permissions`

### SpaceMember

- `space_id`
- `participant_id`
- `participant_type`
- `role`
- `permissions`
- `status`

### SpaceIntelligence

- `space_id`
- `block_id`
- `added_by`
- `added_at`

A Smart Space can contain humans and authorized AI agents. It can hold messages, Intelligent Blocks, evidence, decisions, lessons, and other permitted intelligence objects.

## 8. SMART MOMENTS MODEL

Smart Moments is the user's meaningful saved/favorited intelligence layer.

A favorite action should create or establish a Smart Moment reference to the Intelligent Block rather than duplicate the entire block unnecessarily.

Conceptual fields:

- `moment_id`
- `owner_id`
- `block_id`
- `created_at`
- optional `note`

Smart Moments is not Smart Mail.

## 9. UNIVERSAL BLOCK ACTION CONTRACT

Every eligible Intelligent Block should expose a consistent action interface:

- `favorite()`
- `like()`
- `rate()`
- `share()`
- `copyIntelligence()`
- `comment()` where the surface permits

The Share action opens a unified share composer.

## 10. SHARE COMPOSER

Recommended flow:

`Share (+)`

→ choose destination/action:

- Smart Mail
- Smart Space
- Smart List
- Copy Intelligence
- Smart Moment

### Smart Mail composer

1. Show selected intelligence.
2. Allow one or more Connections to be selected.
3. Allow optional additional Smart Space destination where authorized.
4. Allow full block / summary / collection format.
5. Allow a personal message.
6. Preview.
7. Authorize.
8. Send.
9. Show actual delivery state.

### Smart List composer

1. Select one or more existing lists or create a new list.
2. Add the block reference.
3. Confirm.
4. Show saved state.

### Smart Space composer

1. Show eligible Spaces.
2. Verify membership/write permission.
3. Select Space.
4. Add/reference the block.
5. Confirm.

### Copy Intelligence

Generate a clean portable representation of the Intelligent Block. Do not copy hidden permissions, private metadata, credentials, or internal system data.

## 11. COLLECTION SHARING

The same Share system must support a Smart List as a payload.

Flow:

`Smart List → Share → Smart Mail → Select Connections → Preview → Authorize → Send`

The list remains the source collection. The outbound representation should preserve the identity and provenance of each included block where appropriate.

If a block is not shareable to a selected recipient, the system must identify the restriction instead of silently exposing it.

## 12. CONNECTION-AWARE NETWORKING

For a shared Intelligent Block, the system may eventually offer actions such as:

- Connect with author.
- Create Smart Space around this intelligence.
- Invite relevant participants.
- Share with people who interacted with the block.

Interaction signals can include:

- like;
- favorite;
- comment;
- share;
- other explicitly permitted interaction.

These signals may be used to generate candidate invitations, but must not automatically reveal private identity or automatically enroll a participant in a Space.

## 13. SMART SPACE INVITATION FLOW

Example:

`Create Smart Space`

→ system proposes topic based on selected Intelligent Block

→ user reviews proposed topic and participants

→ eligible participants receive notification/invitation

→ recipient chooses whether to join

→ permissions are established

→ Space is created

→ source Intelligent Block is attached as the seed intelligence

Notification example concept:

**Create a Smart Space about “<topic>”?**

**You can invite people who interacted with this intelligence or select Connections manually.**

**Communicate privately through your configured alias.**

The invitation must be opt-in.

## 14. ALIAS / PRIVATE COMMUNICATION

The user's configured alias is a communication identity and should be resolved through the identity/connection layer.

Do not expose a private underlying identity merely because an alias is visible.

Alias configuration is part of the broader identity/welcome system and should be consumed by Smart Mail, Connections, invitations, and Smart Spaces rather than independently reimplemented in each feature.

## 15. NOTIFICATION MODEL

Create a unified notification event model.

Examples:

- `INTELLIGENCE_SHARED`
- `INTELLIGENCE_LIKED`
- `INTELLIGENCE_COMMENTED`
- `INTELLIGENCE_FAVORITED`
- `CONNECTION_REQUESTED`
- `SPACE_PROPOSED`
- `SPACE_INVITED`
- `SMART_MAIL_SENT`
- `SMART_MAIL_DELIVERED`
- `SMART_MAIL_REPLY`

Notifications should carry:

- event ID;
- recipient;
- source object;
- actor where permitted;
- action;
- timestamp;
- read/unread state;
- deep-link target;
- privacy/visibility rules.

Do not generate notification storms. Use aggregation where multiple users perform the same relevant action.

## 16. INTELLIGENCE GRAPH RELATIONSHIPS

The system should preserve relationships such as:

`Block → authored_by → Person`

`Block → saved_to → Smart List`

`Block → shared_with → Connection`

`Block → delivered_as → Smart Mail`

`Block → seeded → Smart Space`

`Block → favorited_as → Smart Moment`

`Person → member_of → Smart Space`

`Person → connected_to → Person / AI`

`Block → supported_by → Evidence`

`Block → related_to → Block`

These relationships allow the UI to become intelligent without duplicating intelligence objects.

## 17. PERMISSION MODEL

At minimum distinguish permissions such as:

- READ
- SAVE
- COPY
- SHARE
- COMMENT
- CONTRIBUTE
- INVITE
- CREATE_SPACE
- SEND_MAIL
- ANALYZE
- PROPOSE
- APPROVE

Permissions must be evaluated at the time of the operation, not assumed from an earlier UI state.

Apply:

**Private by default. Shared by choice. Collective by consent. Public by decision.**

## 18. PROVENANCE

Every shared or transformed intelligence object should retain enough provenance to answer:

- Who created it?
- What is the canonical block?
- When was it created/updated?
- Where did the shared representation come from?
- Who authorized the share?
- What permissions applied?
- Was delivery actually completed?
- What subsequent intelligence was derived from it?

Do not fabricate provenance or delivery state.

## 19. AI-TO-AI COMMUNICATION

Do not begin with unrestricted autonomous peer-to-peer AI communication.

First establish:

1. Agent identity.
2. Owner identity.
3. Capabilities.
4. Permissions.
5. Authentication.
6. Event model.
7. Provenance.
8. Auditability.
9. Rate limits and abuse protection.

Then support:

`AI → Smart Mail → AI`

and:

`AI → Smart Space → authorized AI / humans`

Multiple AIs agreeing is consensus, not proof of truth. Evidence, verification, and consensus must remain distinct concepts.

## 20. UI ARCHITECTURE

The user should not have to understand the underlying data model.

The interface should communicate one simple action language:

**I found intelligence. What do I want to do with it?**

The primary Intelligent Block action bar should make these actions discoverable and consistent.

The Share composer should act as the central bridge between Smart Lists, Connections, Smart Mail, Smart Spaces, and Smart Moments.

## 21. IMPLEMENTATION ORDER

### Phase 1 — Stable object

Implement/confirm stable Intelligent Block IDs, versions, ownership, visibility, provenance, and permissions.

### Phase 2 — Save and copy

Implement Smart Moment/favorite, Smart List membership, and Copy Intelligence.

### Phase 3 — Connections

Implement recipient/participant resolution and permission-aware selection.

### Phase 4 — Smart Mail

Implement draft, authorization, queue, delivery state, and reply relationships.

### Phase 5 — Smart Share

Unify the above actions behind one Share composer.

### Phase 6 — Smart Spaces

Implement permissioned Spaces, membership, shared intelligence, messages, and seeded Spaces.

### Phase 7 — Notifications

Implement event-driven, aggregated notifications and invitations.

### Phase 8 — Network intelligence

Use authorized interaction and relationship signals to suggest connections and Spaces without automatic enrollment.

### Phase 9 — AI communication

Enable authenticated, permissioned AI-to-AI communication through the same Smart Mail / Smart Space infrastructure.

## 22. ACCEPTANCE TESTS

A build is not complete until these cases can be proven:

1. Open an Intelligent Block.
2. Save it to one Smart List.
3. Save the same block to a second Smart List.
4. Favorite it as a Smart Moment.
5. Copy a clean portable representation.
6. Share it through Smart Mail to one Connection.
7. Share it through Smart Mail to multiple Connections.
8. Share a Smart List containing multiple blocks.
9. Share a block into an authorized Smart Space.
10. Propose a new Smart Space from a block.
11. Send an opt-in invitation to eligible participants.
12. Verify that private participants remain protected.
13. Verify actual mail state rather than claiming delivery.
14. Verify provenance remains attached to the canonical block.
15. Verify unauthorized sharing is rejected.
16. Verify one block remains one canonical object rather than uncontrolled duplicates.
17. Verify notifications are generated once/appropriately aggregated.
18. Verify copy/share actions do not expose private metadata.
19. Verify AI actions are authenticated and permission-checked.
20. Verify the same block can be surfaced in Personal, Collective, Activity, Lists, Moments, Mail, and Spaces according to scope and permission without rebuilding the underlying intelligence.

## 23. NON-NEGOTIABLE ENGINEERING LAWS

- Do not build Smart Mail as an unrelated email utility.
- Do not build Smart Lists as rigid one-block-to-one-folder storage.
- Do not build Connections as an unrestricted contact dump.
- Do not build Smart Spaces as generic chat rooms.
- Do not duplicate Intelligent Blocks unnecessarily.
- Do not automatically expose private identities.
- Do not automatically enroll users into Spaces.
- Do not confuse consensus with evidence or truth.
- Do not claim a message was sent/delivered without state evidence.
- Do not allow an external platform to become the hidden canonical communication layer.
- Do not destroy existing Hub/feed architecture while adding these capabilities.

## 24. CURRENT PROJECT STATE

The immediate project is **architecture and content lock before the next major UI implementation**.

The current sequence is:

1. Lock this Intelligence Sharing architecture.
2. Complete the canonical Intelligent Library questions/content.
3. Create canonical explanatory Smart Notes for the sidebar features.
4. Then implement/refine the interface against the locked architecture.

This report is the technical companion to the canonical Smart Note created at:

`.naya/activity/2026/09/08/2026-09-08-20-09-SMART-NOTE-INTELLIGENCE-SHARING-SYSTEM.md`

## FINAL ENGINEERING PRINCIPLE

> **ONE INTELLIGENT BLOCK. MANY AUTHORIZED RELATIONSHIPS.**
>
> The intelligence is canonical. Lists organize it. Connections identify recipients. Smart Mail moves it. Smart Spaces let authorized participants work with it. Smart Moments preserve what matters personally. Smart Share makes those capabilities feel like one system.
