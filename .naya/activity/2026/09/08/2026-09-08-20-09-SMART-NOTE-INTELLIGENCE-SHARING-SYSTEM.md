# SMART NOTE — NAYANET INTELLIGENCE SHARING SYSTEM

**DATE:** September 8, 2026  
**STATUS:** CANONICAL CURRENT SYSTEM PLAN  
**TYPE:** Architecture / Product Decision / Smart Note  
**SCOPE:** All current and future NIS operating on NayaNET / Naya Power

## CURRENT DECISION

NayaNET's Intelligent Block is the atomic, portable intelligence object. It must not be treated as content that can only be read inside a feed. An Intelligent Block must be easy to save, organize, copy, share, communicate, connect, and contribute to collaborative intelligence.

The four systems **Smart Lists, Connections, Smart Mail, and Smart Spaces** are therefore not independent features. They form one coordinated intelligence-sharing system around the Intelligent Block.

## THE FOUR-SYSTEM MODEL

### Smart Lists — WHAT

Smart Lists organize Intelligent Blocks into user-created collections.

A block may belong to zero, one, or many lists. Lists may be personal or collective and may represent any useful grouping: people, projects, topics, lessons, ideas, favorites, or other intelligence.

Smart Lists are not rigid folders. They are curated intelligence collections.

### Connections — WHO

Connections represent the people, AIs, and other authorized participants with whom intelligence can be communicated or shared.

A Connection can be selected as a recipient for one Intelligent Block, multiple blocks, a Smart List, or other authorized intelligence.

Connections should support recipient selection and relationship-aware sharing rather than functioning only as a passive address book.

### Smart Mail — MOVE

Smart Mail is NayaNET's communication and message-routing layer.

It moves intelligence from its source to an authorized recipient or destination. It must support human-to-human, human-to-AI, AI-to-human, and, when explicitly authorized, AI-to-AI communication.

Smart Mail is not another feed. It is the communication mechanism through which intelligence travels.

### Smart Spaces — TOGETHER

Smart Spaces are permissioned collaborative intelligence environments where humans and authorized AI agents can communicate, contribute Intelligent Blocks, discuss intelligence, add evidence, make decisions, and create new intelligence together.

A Smart Space is where shared intelligence can become compounding collective intelligence.

## SMART MOMENTS

Smart Moments is separate from Smart Mail.

Smart Moments represents the user's meaningful saved/favorited intelligence. When a user favorites an Intelligent Block, it can become a Smart Moment.

Smart Moments must never be substituted for Smart Mail in the feature architecture.

## UNIVERSAL INTELLIGENT BLOCK ACTIONS

Every Intelligent Block should have a consistent action layer. Core actions should include:

- Favorite / Smart Moment
- Like
- Rate
- Share (+)
- Copy Intelligence

The **Share (+)** action should open a unified intelligence-sharing interface rather than forcing the user to understand separate backend systems.

Recommended Share actions:

1. **Smart Mail** — send to people or AI.
2. **Smart Space** — share into a collaborative space.
3. **Smart List** — save to one or more lists.
4. **Copy Intelligence** — copy a clean, complete representation.
5. **Smart Moment** — save as a favorite/meaningful moment.

## PORTABLE INTELLIGENCE

The Intelligent Block must be portable.

Copy should not merely extract an arbitrary fragment of text. It should copy a clean representation containing the block's meaningful intelligence, including its title, date/type, In a Nutshell, perspectives, What We Learned, and What It Means, with provenance or other metadata where appropriate.

The result should be usable in another AI conversation, email, document, message, or NayaNET surface.

## SHARING A SINGLE BLOCK

A user viewing an Intelligent Block should be able to:

**Block → Share → Smart Mail → Select Connections → Send**

or:

**Block → Share → Smart Space → Select Space → Share**

or:

**Block → Share → Smart List → Select one or more Lists → Save**

The same underlying Intelligent Block remains the canonical object; these actions create relationships, deliveries, memberships, or references rather than unnecessary duplicate content.

## SHARING A COLLECTION

A Smart List must also be shareable.

Example:

**Smart List: My 10 Biggest AI Lessons → Share → Smart Mail → Select Connections → Send**

The system should support sending a collection as a coherent intelligence package rather than requiring the user to send each block individually.

## CONNECTION-AWARE SHARING

Connections should allow a user to select multiple recipients for intelligence.

Example:

**Select Connections:**

- Sarah
- John
- Project AI
- NayaNET Builders Space

Then select the intelligence payload:

- one Intelligent Block;
- multiple Intelligent Blocks;
- a Smart List;
- or another authorized intelligence object.

## INTELLIGENT BLOCK SOCIAL/NETWORK ACTIONS

When an Intelligent Block is visible in a Collective or other shared feed, the system should eventually allow authorized users to initiate relationships around that intelligence.

Potential actions include:

- Connect with the author.
- Share the block.
- Save/favorite the block.
- Create or propose a Smart Space around the block's topic.

The system may also identify people or AI agents who interacted with the block — for example by liking, commenting, or sharing — and offer an invitation to connect or participate in a related Smart Space.

This must be permission-aware and notification-controlled. Interaction with a block does not automatically grant access to a person's private identity, private communications, or private intelligence.

## SMART SPACE CREATION FROM INTELLIGENCE

An Intelligent Block can become the seed of a Smart Space.

Example:

**"Create a Smart Space about Blockers Never Stop the Mission?"**

Potential participants can be invited based on explicit relationship, authorized membership, or relevant interaction with the block.

The invitation can communicate the topic and provide an authorized way to respond or connect privately through the user's configured alias.

No participant should be added automatically merely because they interacted with a block.

## COMMUNICATION LOOP

The intended compounding loop is:

**EXPERIENCE → INTELLIGENT BLOCK → ORGANIZE → SHARE → COMMUNICATE → COLLABORATE → RESPOND → LEARN → NEW INTELLIGENCE → COMPOUND**

This makes communication part of the intelligence system rather than a disconnected utility.

## PRIVACY / CONSENT LAW

The existing NayaNET privacy principle applies:

**Private by default. Shared by choice. Collective by consent. Public by decision.**

All sharing, connection, Smart Mail, and Smart Space behavior must respect identity, permissions, authorization, provenance, and user choice.

## CURRENT IMPLEMENTATION PRIORITY

Before expanding autonomous AI-to-AI communication, establish the underlying primitives:

1. Intelligent Block identity and stable reference.
2. User identity and authorized Connection identity.
3. Smart List membership.
4. Smart Mail message and recipient model.
5. Smart Space membership and permissions.
6. Share/Copy action contract.
7. Notification and invitation model.
8. Provenance and audit trail.
9. Delivery/read/reply state where applicable.
10. Permission-aware automation.

Only after these are reliable should higher-level autonomous communication be enabled.

## CURRENT PRODUCT NORTH STAR

The user should experience these systems as one simple idea:

> **"I found intelligence. Now I can save it, organize it, copy it, send it, connect around it, or bring people and AI together around it."**

The interface should make that action obvious without requiring the user to understand the underlying architecture.

## CANONICAL LAW

> **THE INTELLIGENT BLOCK IS THE INTELLIGENCE. SMART LISTS ORGANIZE IT. CONNECTIONS IDENTIFY WHO CAN RECEIVE IT. SMART MAIL MOVES IT. SMART SPACES GIVE IT A PLACE TO BECOME SHARED INTELLIGENCE. SMART MOMENTS PRESERVE WHAT MATTERS PERSONALLY. SMART SHARE CONNECTS THE ACTIONS.**

## NEXT PROJECT STEP

Lock this architecture as the current design/engineering contract, then complete the canonical Intelligent Library content and the explanatory Smart Notes for the Hub's sidebar features before implementing the next major interface iteration.
