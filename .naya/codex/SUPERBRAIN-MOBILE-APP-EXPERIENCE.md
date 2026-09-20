# Naya Power — Personal Superbrain Mobile Web Experience

**STATUS:** PRODUCT ARCHITECTURE / IMPLEMENTATION TARGET

## 1. Product role

The web app is the human control surface for the private Superbrain. GitHub is the durable development/governance layer; the app should hide repository complexity from the human.

The user should experience Naya Power as a simple personal intelligence environment, not as a Git client.

## 2. Core navigation

### Home

- Naya greeting
- Current Intelligence State
- Today's progress
- Daily Intelligence button
- quick capture
- next best action

### Brain

- Search/ask Naya
- timeline
- subjects/projects
- Smart Notes
- Super Notes
- Master Notes
- receipts

### CIS

- Daily Intelligence
- Weekly
- Monthly
- Quarterly
- Six-Month
- Annual
- Lifetime
- growth/learning trends

### Network

- NayaNET status
- Connect Naya
- permission controls
- network lessons
- collective Daily Intelligence
- connected relationships

### Profile / Settings

- privacy
- permissions
- exports
- integrations
- model/provider settings
- account/security

## 3. Human interaction principle

The human should almost never need to understand the storage implementation.

Example:

**User:** "Make this a Smart Note."

**Naya:** Creates/updates the canonical event, verifies it, generates Naya + Human views, issues the receipt, and presents:

> **Done. Your Smart Note is official.**
>
> 🧠 Read Naya Note
>
> 👤 Read Human Note
>
> 🧾 View Receipt
>
> 🔗 View Source
>
> 🟢 Verified

## 4. Daily Intelligence experience

At the end of the day:

**"Naya, give me my Daily Intelligence Report."**

Naya presents a concise, human-friendly briefing covering:

- what happened;
- what was learned;
- how the user grew;
- wins;
- challenges/corrections;
- decisions;
- project/learning progress;
- scores where available;
- patterns;
- open loops;
- tomorrow's next best move.

The user can listen to the briefing using Naya voice and inspect the full written report.

## 5. NayaNET experience

The network screen should make the privacy boundary obvious.

Primary card:

> **Your Naya is private.**
> You decide if and what it shares.

Primary action:

**Connect to NayaNET**

Then show plain-language choices:

- Learn from the network
- Share selected knowledge
- Collaborate with selected Nayas
- Disconnect

Never hide scope details behind technical language.

## 6. Recommended first network interaction

A new user should see:

> **Want your Naya to learn from the collective intelligence of other Nayas?**
>
> You can contribute selected lessons without sharing your private conversations or identity by default.
>
> **[Learn Together] [Not Now]**

The actual implementation must perform real consent and privacy controls; the UI alone is not the security boundary.

## 7. Technical deployment model

The first product can be a responsive mobile-first web app/PWA.

Suggested separation:

```text
MOBILE WEB APP / PWA
        │
        ▼
NAYA POWER API / AUTH LAYER
        │
   ┌────┴────┐
   ▼         ▼
PERSONAL   FEDERATION
SUPERBRAIN  GATEWAY
   │         │
   ▼         ▼
CIS /       NAYANET
MEMORY      NETWORK
```

GitHub remains the source-control/governance/development layer. It should not be treated as the end-user database or permanent production federation transport.

## 8. First MVP

Build the smallest complete human loop:

1. Sign in.
2. Connect personal Superbrain.
3. Ask Naya.
4. Capture a Smart Note.
5. View Naya + Human notes.
6. View receipt.
7. Search/retrieve memory.
8. Request Daily Intelligence.
9. View current Intelligence State.
10. See NayaNET and privacy controls, initially disabled/preview if federation is not production-ready.

## 9. Product law

> **The complexity belongs in the system. The simplicity belongs with the human.**

The app is the concierge. The Superbrain is the engine. CIS is the compounding layer. NayaNET is the optional network.
