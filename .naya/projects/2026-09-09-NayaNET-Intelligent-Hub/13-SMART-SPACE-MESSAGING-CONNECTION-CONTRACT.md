# 13 — SMART SPACE, MESSAGING & CONNECTION CONTRACT

**Project date:** 2026-09-09  
**Status:** LOCKED PRODUCT CONTRACT  
**Scope:** Smart Spaces, shared conversation, Smart Messaging, Smart Mail relationship, saved Connections, collective wisdom

> **North Star:** NayaNET creates human connection around intelligence. People discover a topic, enter a Smart Space, converse, create intelligence together, choose who they want to retain as Connections, and may deliberately contribute distilled wisdom to the Collective.

## 0. THE FUNDAMENTAL MODEL

A Smart Space is **not** a technical integration, external connection, generic dashboard, or permanent group by default.

A Smart Space is a **living shared intelligence environment created around a topic, question, idea, project, challenge, opportunity, or Intelligent Board.**

The core lifecycle is:

**INTELLIGENT BOARD / SMART NOTE / ASK NAYA → CREATE SMART SPACE → INVITE → ACTIVITY FEED → JOIN → CONVERSE → NAYA WEAVES → INTELLIGENCE EMERGES → SAVE CONNECTIONS → SHARE WISDOM BY CONSENT**

The network grows through shared interests and useful intelligence rather than requiring people to begin by searching a directory of strangers.

## 1. WHAT A SMART SPACE IS

### Human
A place where humans meet around something meaningful and communicate.

### Child
A room where people who are curious about the same thing can come together and ask questions.

### Grandma
A gathering place for a conversation that matters, where you can meet people, learn from them, and choose whether to stay connected.

### Naya
The intelligence layer that understands the topic, helps organize the conversation, identifies emerging themes, distills useful learning, and helps participants compound what they discover.

### Machine
A persistent product object with a unique Space ID, creator, topic/context, membership state, messages/events, permissions, timestamps, lifecycle state, provenance, and consent records.

### Meaning
**Smart Space = shared conversation + human connection + compounding intelligence.**

## 2. CREATION PATHS

### 2.1 From an Intelligent Board — PRIMARY PATH

Every eligible Intelligent Board has a visible, clear action:

**CREATE SMART SPACE**

When selected:

1. Create a new Space using the Board as its seed context.
2. Preserve the source Board/event relationship.
3. Pre-fill a human-readable Space title from the topic.
4. Show the creator a review/confirmation surface.
5. Allow the creator to add an optional description or opening question.
6. Publish the Space only when the creator explicitly chooses to publish/invite.
7. Publish the Space invitation to the Activity Feed.

The Board does **not** automatically add people to the Space.

### 2.2 From a Smart Note

A Smart Note may expose **CREATE SMART SPACE** when the user wants to explore the Note with others.

Naya uses the Note as seed context while preserving the original Note as the canonical personal event.

### 2.3 Ask Naya

The user may say:

> “Naya, create a Smart Space about [topic].”

Naya proposes the Space context and asks for confirmation before publishing it.

### 2.4 From an Existing Space

A participant may create a related Space when a distinct subtopic or follow-on discussion deserves its own environment.

The new Space retains a relationship to the originating Space.

## 3. SPACE INVITATION

Publishing creates an **invitation**, not automatic membership.

The invitation appears in Activity Feed as a concise activity object:

**[Creator] created a Smart Space**  
**[Topic]**  
[short context]

Primary action:

**JOIN SPACE**

Secondary actions may include:

- View Space
- Not interested
- Hide/mute similar invitations where supported

### V1 distribution

The initial implementation should use Activity Feed discovery rather than mass notification to every user.

Future relevance-based distribution may use demonstrated interests, prior activity, and explicit notification preferences.

No topic-based broadcast should be assumed to mean every user is notified.

## 4. JOINING A SPACE

Joining is explicit.

A user who selects **JOIN SPACE** becomes a participant according to the Space's membership rules.

**Joining a Space does NOT automatically save every participant as a permanent Connection.**

This distinction is mandatory.

The user may participate, read, post, and learn without creating permanent relationships.

## 5. PEOPLE INSIDE A SPACE

Every participant has a NayaNET identity represented by their Smart Name / Smart Alias according to identity and privacy rules.

The participant list should make it easy to understand:

- who is participating
- who is the Space creator
- who is currently active/available when truthful presence exists
- whether a person is already a saved Connection
- whether the user can save that person

Example actions:

**@alias**  
**SAVE CONNECTION**

or:

**@alias**  
**CONNECTED**

Do not expose private identity information beyond the user's approved NayaNET identity and visibility settings.

## 6. CONNECTION CREATION

A Connection is created from an actual human interaction, not from a directory entry.

The recommended lifecycle is:

**DISCOVER → JOIN → INTERACT → CHOOSE PERSON → SAVE CONNECTION → COMMUNICATE / RECONNECT**

Saving a Connection means the user has deliberately chosen to retain that relationship.

The other person should not be silently added to the user's Connections merely because they participated in the same Space.

Future mutual-connection behavior may be added, but V1 must keep consent explicit.

## 7. CONNECTIONS ROOM RELATIONSHIP

The Connections room is exclusively the user's **saved human NayaNET network**.

It is not the home for:

- GitHub
- APIs
- external service integrations
- technical synchronization providers
- infrastructure adapters
- machine connections

Those belong in the appropriate technical/system architecture.

Connections must support:

- saved people
- Smart Name
- Smart Alias
- user-defined groups/categories
- search
- filtering
- connection detail
- remove/archive connection
- launch Smart Mail/message
- request/create Smart Space

## 8. CONNECTION ORGANIZATION

Users can create their own categories/groups.

Examples:

- Friends
- Family
- Church
- Business
- Project
- Team
- Community
- Topic
- Mastermind
- Any custom user-defined category

A person may belong to multiple groups.

Groups are organization tools, not separate identities or separate accounts.

The system must not assume a fixed category taxonomy.

## 9. CONNECTION SEARCH

Connections must have a dedicated search experience.

Search should be able to find:

- Smart Name
- Smart Alias
- group/category
- topic/context where permitted and indexed

Results must open the actual Connection record, not create a duplicate contact.

## 10. SMART SPACE CONVERSATION

A Space contains a shared conversation feed.

Participants can:

- post messages
- reply where threading is supported
- react where intentionally designed
- share relevant intelligence/events
- ask Naya about the conversation
- inspect participants
- save Connections
- access the Space's distilled intelligence

The conversation feed is **shared Space communication**, not private direct messaging.

## 11. SMART MESSAGING

Smart Messaging is the real-time/private communication layer associated with NayaNET relationships and Spaces.

Two communication modes must remain visually and conceptually distinct:

### SPACE MESSAGE
Visible to participants in the Space.

### DIRECT MESSAGE
Private conversation between the user and another person they are permitted to message.

If participants are online and real-time transport is available, the product may provide instant messaging.

If real-time transport is unavailable, the UI must show a truthful pending/offline state rather than pretending a message was delivered.

## 12. SMART MAIL RELATIONSHIP

Smart Mail is the communication system that can operate over the user's saved Connections and organized groups.

A user may:

1. Open Connections.
2. Select one or more people.
3. Select a group/category.
4. Choose **MESSAGE / SMART MAIL**.
5. Compose one message.
6. Review recipients.
7. Send.

### Group messaging requirement

The system must support sending a message to a selected group of saved Connections.

Example:

**Friends — 12 Connections**

**MESSAGE GROUP**

This is a deliberate product capability and should be treated as a first-class interaction, not an afterthought.

The same relationship may later support messaging Space participants where the user has permission to communicate with them.

## 13. SMART SPACE → CONNECTION → MAIL LOOP

```text
SMART SPACE
    ↓
MEET PEOPLE
    ↓
CONVERSE
    ↓
CHOOSE WHO TO RETAIN
    ↓
SAVE CONNECTION
    ↓
ORGANIZE CONNECTION
    ↓
SMART MAIL / DIRECT MESSAGE
    ↓
REQUEST OR CREATE ANOTHER SMART SPACE
```

This loop is one of the primary network-growth mechanisms of NayaNET.

## 14. SPACE OWNER / CONTROL

The person who creates a Smart Space is the **Space Creator / Owner**.

The creator controls the Space lifecycle.

### Creator may:

- publish the Space
- edit the Space title/description where supported
- manage creator-level settings
- close the Space
- leave the Space open for future conversation

### Participants may:

- join
- participate
- leave
- save Connections
- communicate according to permissions
- contribute intelligence
- propose/share wisdom according to consent rules

### Participants may NOT:

- unilaterally close another person's Space
- delete the creator's Space
- change creator-level ownership

This protects the person who opened the conversation from having another participant arbitrarily shut it down.

Administrative moderation capabilities, if required later, must be explicitly designed rather than silently added to V1.

## 15. SPACE LIFECYCLE

A Space does not have to remain open forever.

### PROPOSED
Created but not yet publicly invited/published.

### ACTIVE
Published and accepting participation/conversation.

### QUIET
Still available, but conversation has slowed.

### CLOSED
The creator intentionally closed the Space.

A closed Space is no longer an active conversation environment.

Its retained intelligence, messages, provenance, and connection history remain subject to the applicable retention/privacy rules.

### REOPENING
If product policy permits, only the creator should be able to reopen a closed Space.

This must be a deliberate product control, not an accidental consequence of someone posting.

## 16. LEAVE VS CLOSE

These actions are fundamentally different.

**LEAVE SPACE** = one participant leaves.

**CLOSE SPACE** = the creator ends the Space for active participation.

Leaving must never close the Space.

A participant leaving does not erase their previously retained Connection decisions or intelligence contributions unless applicable privacy controls require removal.

## 17. SPACE INTELLIGENCE

Naya continuously treats the Space as a potential intelligence source while respecting privacy and consent boundaries.

Naya may identify:

- emerging themes
- important questions
- agreements
- disagreements
- lessons
- breakthroughs
- decisions
- opportunities
- actions
- repeated patterns
- possible wisdom candidates

Naya must distinguish:

**OBSERVED CONVERSATION** from **NAYA INTERPRETATION**.

No fabricated participant opinion, quote, agreement, breakthrough, or consensus may be presented as fact.

## 18. WEAVER / DISTILLATION

The Space is a source for intelligence distillation.

A Weaver layer may synthesize the conversation into:

- WISDOM
- LESSON
- MEANING
- ACTION
- QUESTIONS
- DECISIONS
- OPPORTUNITIES

The original messages remain the provenance source.

The distilled object must retain traceability to its source Space/conversation events.

## 19. SHARE WISDOM WITH THE COLLECTIVE

A Space may intentionally contribute valuable intelligence to the NayaNET Collective.

The user experience should make this explicit:

**SHARE WISDOM WITH THE COLLECTIVE**

Before contribution, Naya should present the proposed wisdom and explain the sharing boundary.

The user/authorized participants must be able to review what is being shared.

Collective contribution is never automatic merely because a conversation occurred.

### Principle

**Private conversation → deliberate distillation → deliberate consent → collective wisdom.**

This is how Smart Spaces can deliberately increase the intelligence of the collective over time.

## 20. THE MASTERMIND USE CASE

A valid high-value use case is a deliberate group forming a Space with the explicit purpose of creating new intelligence.

Example:

> “Let's create a NayaNET Mastermind Space around this challenge, explore it together, capture the breakthroughs, and share the wisdom we agree is valuable to the Collective.”

The product must support this without requiring a separate product mode.

The Space itself is the container for:

**people → questions → conversation → perspectives → Naya synthesis → breakthroughs → wisdom → collective contribution.**

## 21. NETWORK COMPOUNDING

The intended compounding loop is:

```text
DAY 1
Person creates Space around a topic.

DAY 1+
People discover it in Activity Feed.

DAY 1+
People join and converse.

DAY 2+
Naya identifies emerging intelligence.

DAY 2+
Participants save useful Connections.

DAY 2+
Participants communicate privately or regroup.

DAY 3+
The group distills valuable wisdom.

DAY 3+
Participants deliberately share approved wisdom with the Collective.

DAY N
Collective intelligence remembers the contribution.

NEXT
That intelligence can inform future Boards, Spaces, Feed items, and Naya responses.
```

The objective is not simply more content.

The objective is **more useful intelligence over time.**

## 22. NOTIFICATIONS

V1 should favor Activity Feed visibility and truthful notifications over indiscriminate broadcasts.

Possible truthful notifications include:

- someone joined your Space
- someone posted in your Space
- someone saved a Connection where disclosure is appropriate
- your Space received activity
- Naya identified significant emerging intelligence
- a wisdom contribution requires review/consent
- your Space was closed by its creator

Notification behavior must respect user preferences.

## 23. DATA OBJECTS

Minimum conceptual objects:

### Space
- space_id
- creator_user_id
- title
- description
- seed_source_id
- seed_source_type
- topic/tags
- status
- created_at
- published_at
- closed_at
- privacy/visibility state

### Membership
- space_id
- user_id
- role
- joined_at
- left_at
- membership_state

### Space Message
- message_id
- space_id
- author_user_id
- content
- created_at
- edited_at if supported
- provenance
- visibility

### Connection
- connection_id
- owner_user_id
- connected_user_id
- created_at
- status
- notes/labels where permitted

### Connection Group
- group_id
- owner_user_id
- name
- created_at

### Connection Group Membership
- group_id
- connection_id

### Intelligence Candidate
- candidate_id
- source_space_id
- source_message/event IDs
- generated synthesis
- Naya/model provenance
- review state
- consent state

### Collective Contribution
- contribution_id
- source_candidate_id
- contributor/consent record
- de-identification state
- collective publication state
- timestamps

The exact database schema is an engineering decision only after this product contract is accepted.

## 24. UI REQUIREMENTS

Smart Spaces must not become oversized dashboard cards.

The interface should be:

- compact
- immediately scannable
- topic-first
- people-aware
- conversation-first
- visually premium
- consistent with the NayaNET intelligent-object language
- clear about active/closed state
- clear about whether the user is a participant
- clear about whether someone is a saved Connection

### Primary controls

**CREATE SMART SPACE**  
**JOIN SPACE**  
**MESSAGE**  
**PEOPLE**  
**SAVE CONNECTION**  
**SHARE WISDOM**  
**CLOSE SPACE** — creator only  
**LEAVE SPACE** — participant

No control may exist without a defined result.

## 25. SPACE SCREEN INFORMATION HIERARCHY

The Space screen should answer, in order:

1. **What is this Space about?**
2. **Why does it exist?**
3. **Who is here?**
4. **What's happening now?**
5. **What is Naya seeing?**
6. **What intelligence has emerged?**
7. **Who do I want to stay connected with?**
8. **What can I do next?**

The user should never have to hunt through oversized cards to discover the primary action.

## 26. EMPTY STATES

### No Spaces yet
Explain that Spaces appear when the user or others create conversations around topics of interest.

Primary action:

**CREATE SMART SPACE**

### Space has no participants beyond creator
Explain that the invitation is live and waiting for people to join.

### Space has no messages
Show the opening question/context and encourage the creator or participant to start the conversation.

### Connections empty
Explain:

> Your Connections grow from people you meet in Smart Spaces and choose to save.

Do not fabricate suggested Connections.

## 27. PRIVACY / CONSENT LAWS

1. Joining a Space does not automatically create a permanent Connection.
2. Saving a Connection is an intentional user action.
3. Private/direct communication is distinct from Space communication.
4. Space conversation does not automatically become Collective Intelligence.
5. Collective contribution requires deliberate consent.
6. A closed Space does not become public merely because it is closed.
7. Identity exposure must follow NayaNET identity/privacy rules.
8. The creator controls closing their own Space.
9. A participant controls whether they leave.
10. Technical integrations do not belong in the Connections room.

## 28. VERIFICATION CONTRACT

Before Smart Spaces are declared complete, verify the actual production experience:

**SOURCE → BUILD → DEPLOY → EXACT RUNTIME → DOM → VISIBLE SCREEN → CREATE → PUBLISH → ACTIVITY → JOIN → POST → PEOPLE → SAVE CONNECTION → CONNECTION GROUP → SEARCH → MESSAGE → CLOSE → PERSISTENCE → MOBILE → CONSENT**

Evidence must prove:

- Create Space actually creates a persistent Space.
- Board/Note provenance is retained.
- Published Space appears in Activity Feed.
- Join changes membership.
- Messages persist and display correctly.
- Participant aliases display according to privacy rules.
- Save Connection creates a persistent Connection.
- Groups organize Connections without duplication.
- Search finds actual saved Connections.
- Group messaging uses actual selected recipients.
- Direct messaging is distinct from Space messages.
- Creator can close their own Space.
- Non-creators cannot close it.
- Closed state persists after reload.
- Wisdom sharing is consent-gated.
- Mobile behavior is usable and complete.
- No fake delivery, membership, notification, intelligence, or collective contribution states are shown.

## 29. DEFINITION OF DONE

Smart Spaces are not done because the screen exists.

They are done when a real user can:

**SEE A TOPIC → CREATE A SPACE → PUBLISH IT → SEE IT IN ACTIVITY → JOIN → CONVERSE → SEE PARTICIPANTS → SAVE A PERSON → ORGANIZE THE CONNECTION → SEARCH THE CONNECTION → MESSAGE THE PERSON/GROUP → CREATE ANOTHER SPACE → DISTILL INTELLIGENCE → REVIEW WISDOM → CONSENT TO SHARE → CLOSE THE SPACE → RETURN LATER AND SEE THE TRUTHFUL STATE.**

That is the complete product loop.
