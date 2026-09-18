# 12 — ROOM EXECUTION CONTRACTS

**Project:** NayaNET Intelligent Hub — Fresh Rebuild
**Status:** BUILD-READY ROOM INDEX
**Date:** 2026-09-09

This file is the quick-entry contract for every Hub room. A Naya or engineer should be able to start here, understand the room in minutes, then follow the linked detailed specification before changing code.

## UNIVERSAL ROOM CONTRACT

Every room must define:

**WHAT IT IS → WHY IT EXISTS → HUMAN → CHILD → GRANDMA → NAYA → MACHINE → WHAT IT DOES → HOW IT CONNECTS → DATA → PERSISTENCE → STATES → PRIVACY → DESKTOP → MOBILE → VERIFICATION**

No room is implemented until its unknowns are explicitly marked or resolved.

---

## 1. HOME / INTELLIGENCE TODAY

**In a nutshell:** The front door and orientation room.

- **Human:** what the user is experiencing now.
- **Child:** what matters most right now?
- **Grandma:** what simple practical wisdom should be obvious?
- **Naya:** interpret and orient the user without pretending certainty.
- **Machine:** current time, date, locale, identity and verified system state.
- **What it does:** greets, orients, searches, exposes current intelligence and next action.
- **Connects:** Identity → Smart Feed → Notes → Search → Reports → all rooms.
- **Must preserve:** personalized greeting, time, date, locale/country, intelligence philosophy and privacy law.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §1.

---

## 2. SMART FEED / INTELLIGENT FEED

**In a nutshell:** The living intelligence stream.

- **Human:** original experience/input.
- **Child:** first-principles question/curiosity.
- **Grandma:** lived wisdom/common sense.
- **Naya:** actual AI interpretation/synthesis.
- **Machine:** observable facts, status and evidence.
- **Weaver:** connects perspectives into coherent intelligence.
- **Wisdom:** distilled intelligence anchor.
- **Lesson / Meaning / Action:** what is retained, why it matters and what happens next.
- **What it does:** makes intelligence visible and lets users inspect, expand, search and act on canonical events.
- **Connects:** Smart Notes → Feed → Search/Library/Reports/Learning/Collective.

**Detailed contract:** `08-SMART-FEED-INTELLIGENCE-SPEC.md`.

---

## 3. SMART NOTES

**In a nutshell:** The canonical capture layer for personal intelligence events.

- **Human:** records the user's actual experience, insight, mistake, breakthrough, decision, idea, lesson, question, goal, win or opportunity.
- **Child:** captures the simple question underneath the note.
- **Grandma:** captures practical/lived wisdom when appropriate.
- **Naya:** may enrich, organize or interpret; never silently rewrites the Human record.
- **Machine:** records provenance, timestamps, IDs and observable processing state.
- **What it does:** creates, edits where permitted, searches and inspects canonical events.
- **Connects:** Identity → persistence → Smart Feed → Library → Search → Reports.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §3.

---

## 4. DAILY INTELLIGENCE / REPORTS

**In a nutshell:** Compresses intelligence into useful briefings and compounding learning.

- **Human:** what mattered to the user.
- **Child:** what deserves attention or a question.
- **Grandma:** practical lesson.
- **Naya:** synthesis and pattern recognition.
- **Machine:** time window, sources, receipts and verified state.
- **What it does:** answers What Mattered → What Was Learned → What Carries Forward → What Deserves Attention Next.
- **Connects:** Feed/Notes → daily briefing → Day 1 → Day 2 → Day 7 → Day 30 → Day 365 → Lifetime.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §4.

---

## 5. INTELLIGENCE LIBRARY

**In a nutshell:** Organized memory for finding and revisiting canonical intelligence.

- **Human:** original events and context.
- **Child:** simple retrieval intent.
- **Grandma:** useful categorization and common-sense organization.
- **Naya:** related intelligence and synthesis when genuinely available.
- **Machine:** index/provenance/ranking state.
- **What it does:** search, organize, favorite, group and inspect intelligence.
- **Connects:** same canonical events as Feed, Notes and Reports; never clones the intelligence database.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §5.

---

## 6. COLLECTIVE INTELLIGENCE

**In a nutshell:** Consent-based collective value created from intentionally shared, appropriately de-identified intelligence.

- **Human:** decides whether to contribute.
- **Child:** asks whether sharing is useful and safe.
- **Grandma:** applies common-sense privacy boundaries.
- **Naya:** explains contribution and collective meaning.
- **Machine:** records consent, contribution, de-identification and withdrawal state.
- **What it does:** explains, enables/disables and exposes collective intelligence.
- **Connects:** Private intelligence → consent boundary → collective projection.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §6.

---

## 7. EVIDENCE

**In a nutshell:** The truth/verification room.

- **Human:** source statement/input.
- **Child:** what exactly are we claiming?
- **Grandma:** what would convince a reasonable person?
- **Naya:** interpretation clearly separated from evidence.
- **Machine:** receipts, IDs, timestamps, runtime/build status.
- **What it does:** distinguishes observed truth from intent, interpretation and unverified claims.
- **Connects:** every consequential intelligence event and production verification path.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §7.

---

## 8. CONNECTIONS

**In a nutshell:** The controlled doorway to external intelligence/data sources.

- **Human:** chooses what to connect.
- **Child:** asks what this connection gives us.
- **Grandma:** checks whether the connection is trustworthy and necessary.
- **Naya:** explains connection value/status.
- **Machine:** connection health, authorization and verification state.
- **What it does:** inspect, verify and manage explicit source adapters.
- **Connects:** external services → adapters → authorized Hub intelligence.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §8.

---

## 9. SMART MAIL

**In a nutshell:** Private NayaNET communication using the user's alias identity.

- **Human:** writes the actual communication.
- **Child:** clarifies intent and recipient.
- **Grandma:** applies respectful/common-sense communication.
- **Naya:** can help draft, summarize or organize when invoked.
- **Machine:** transport, message ID, delivery/failed/pending receipts.
- **What it does:** inbox, sent, drafts, compose, connections, rooms, groups and lists.
- **Connects:** identity alias → Smart Mail namespace → communication adapters → receipts → intelligence when intentionally captured.
- **Truth law:** draft ≠ sent; pending ≠ delivered.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §9.

---

## 10. SMART SPACE

**In a nutshell:** Persistent organization/workspace layer associated with the user's NayaNET identity.

- **Human:** determines purpose and content.
- **Child:** asks what belongs here and why.
- **Grandma:** keeps the space understandable and useful.
- **Naya:** organizes and connects intelligence when authorized.
- **Machine:** object IDs, membership, permissions and persistence state.
- **What it does:** remains OPEN until the object model is explicitly defined.
- **Connects:** alias identity ↔ spaces ↔ lists/groups/projects ↔ canonical events ↔ search.
- **Important:** do not invent the missing object model during implementation.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §10 and `10-OPEN-DECISIONS-BEFORE-CODING.md` §9.

---

## 11. SETTINGS

**In a nutshell:** Governs how the Hub behaves.

- **Human:** chooses preferences and boundaries.
- **Child:** makes each control understandable.
- **Grandma:** defaults should be safe and sensible.
- **Naya:** explains consequences where useful.
- **Machine:** stores and enforces the actual setting.
- **What it does:** intelligence, communication, privacy, connections, experience and account controls.
- **Connects:** settings → enforcement points across every affected room.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §11.

---

## 12. TOP BAR

**In a nutshell:** Persistent context without becoming a control dump.

- **Human:** where am I and what can I do?
- **Child:** what is important here?
- **Grandma:** keep it simple.
- **Naya:** presence/access.
- **Machine:** connection/trust status.
- **What it does:** room title, search, status, Naya and account access.
- **Connects:** global navigation/state.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §12.

---

## 13. LOWER FEATURE REPORT BAR

**In a nutshell:** Persistent access to the five foundational principles/reports.

**Items:** SMART NOTES · NO DEAD ENDS · CONTEXT LAW · 10-STAR SERVICE · ADAPTIVE LEARNING.

- **What it does:** opens the preserved external reports.
- **Connects:** Hub → external report destinations.
- **Machine:** destination must be truthful and reachable.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §13.

---

## 14. LEFT SIDEBAR

**In a nutshell:** Primary desktop room navigation.

- **What it does:** routes to Personal, Collective, Communication and System rooms.
- **Human:** chooses destination.
- **Child:** labels must be immediately understandable.
- **Grandma:** navigation should never require remembering hidden gestures.
- **Naya:** active context can be reflected without taking over navigation.
- **Machine:** truthful badges/status only.
- **Rule:** desktop left rail only; no right Hub sidebar.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §14.

---

## 15. MOBILE NAVIGATION

**In a nutshell:** Purpose-built mobile access to the same house.

- **What it does:** provides high-frequency Home, Notes, Reports, Intel and Mail access plus a deliberate More/Menu path to every other room.
- **Rule:** no important room may become inaccessible.
- **Machine:** fixed UI must never obscure content.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §15.

---

## 16. ECOSYSTEM LINK BAR

**In a nutshell:** Connects the Hub to the broader NayaNET/HMC ecosystem.

- **What it does:** provides intentional external destinations such as Naya Power, Academy, Powercasts, White Paper, About Us and HMC Login.
- **Rule:** these links are ecosystem exits, not substitutes for internal Hub rooms.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §16.

---

## 17. SEARCH / RETRIEVAL

**In a nutshell:** Finds intelligence across the house, not merely visible cards.

- **Human:** search intent.
- **Child:** simple question.
- **Grandma:** useful relevance.
- **Naya:** semantic interpretation only when a real backend supports it.
- **Machine:** index, provenance, ranking and permission state.
- **What it does:** exact/keyword search now; semantic search only when genuinely implemented.
- **Connects:** Notes, Feed, Library, Reports, Lists, Groups, Spaces and authorized collective intelligence.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §17.

---

## 18. NAYA ACCESS

**In a nutshell:** The intelligent partner layer across the house.

- **Human:** asks/requests.
- **Child:** curiosity.
- **Grandma:** practical perspective.
- **Naya:** synthesis, explanation and action support.
- **Machine:** source/trust state for consequential answers.
- **What it does:** Ask, explain, summarize, compare, find related intelligence and suggest next action.
- **Connects:** Naya adapter ↔ canonical events ↔ rooms.

**Detailed contract:** `09-HUB-ROOM-BY-ROOM-SPEC.md` §18.

---

## EXECUTION RULE

Build in this dependency order:

```text
FOUNDATION
  ↓
IDENTITY BOOTSTRAP
  ↓
HOUSE SHELL
  ↓
HOME
  ↓
CANONICAL SMART NOTE EVENT
  ↓
SMART FEED / INTELLIGENT BLOCK
  ↓
SEARCH
  ↓
REPORTS / LIBRARY / COLLECTIVE / EVIDENCE / CONNECTIONS
  ↓
SMART MAIL / SMART SPACE / SETTINGS
  ↓
NAYA + PRODUCTION ADAPTERS
  ↓
FULL VERIFICATION
```

For every room:

```text
DEFINE → BUILD → LOOK → CLICK → TEST → PERSIST → MOBILE → VERIFY → LOCK
```

Never move forward merely because source code or a deployment succeeded. The exact production runtime must be observed and verified.
