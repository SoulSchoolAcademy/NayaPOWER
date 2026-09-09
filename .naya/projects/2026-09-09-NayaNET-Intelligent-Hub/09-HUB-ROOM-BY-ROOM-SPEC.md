# 09 — HUB ROOM-BY-ROOM SPECIFICATION

**Project date:** 2026-09-09
**Status:** NEW-BUILD PRODUCT CONTRACT
**Reference:** `2026 09 08 452 NayaNET Hub.html` is frozen reference material only.

Think of the Hub as a house. Each room has a job, contents, controls, data boundary, relationship to the other rooms, and a clear definition of done.

## 0. GLOBAL HOUSE RULES

- One current Hub implementation will be built fresh.
- The 2026-09-08 4:52 reference is never edited as part of the rebuild.
- Historical/failed implementations are evidence, not architecture.
- No accidental deletion of a working requirement.
- No feature is removed without an explicit product decision.
- No control exists without a defined action.
- No link exists without a defined destination.
- No intelligence is claimed without evidence.
- No private data is shared without the appropriate consent boundary.
- Desktop has one left navigation rail and no right Hub sidebar.
- Mobile has no persistent left sidebar.

## 1. ROOM: HOME / INTELLIGENCE TODAY

**Purpose:** The front door. Immediately tells the user where they are, what matters now, and what they can do next.

**Must contain:**
- NayaNET identity
- personalized greeting: `Good morning, Shawn` / appropriate time-of-day variant
- current local time
- current date
- country/locale context
- concise intelligence statement / philosophy line
- privacy statement: `Private by default · Shared by choice · Collective by consent · Public by decision`
- primary search / Ask Naya entry
- Smart Feed / Intelligent Feed
- Personal Intelligence / Collective Intelligence / Activity Feed access or clear mode control
- current-state summary
- highest-value next action

**Important:** The welcome/time/date/country and philosophy statement are first-class product requirements. They must not disappear because another layer is being redesigned.

## 2. ROOM: SMART FEED / INTELLIGENT FEED

**Purpose:** Primary living intelligence surface.

**Contains:** Personal Intelligence, Collective Intelligence, Activity Feed and Intelligent Blocks.

**Block sequence:**
WISDOM → HUMAN → CHILD → GRANDMA → NAYA → MACHINE → WEAVER → LESSON / MEANING / ACTION.

**See:** `08-SMART-FEED-INTELLIGENCE-SPEC.md` for the full contract.

## 3. ROOM: SMART NOTES

**Purpose:** Capture and inspect the canonical personal intelligence events.

**Must contain:**
- new Smart Note capture
- search
- event-type categories
- time organization
- note list
- note detail/perspectives
- provenance
- privacy state
- verification state
- relationship to Intelligent Feed

**Canonical law:** Smart Note is the event; Feed is the projection.

## 4. ROOM: DAILY INTELLIGENCE / REPORTS

**Purpose:** Compress recent intelligence into a useful briefing.

**Must contain:**
- What Mattered
- What Was Learned
- What Carries Forward
- What Deserves Attention Next
- source/provenance
- time window
- relationship to previous learning
- clear distinction between observed evidence and interpretation

**Compounding path:** Day 1 → Day 2 → Day 7 → Day 30 → Day 365 → Lifetime.

## 5. ROOM: INTELLIGENCE LIBRARY

**Purpose:** Organized, searchable reference memory.

**Must contain:**
- global intelligence search
- all intelligence
- recent intelligence
- favorites
- lists
- groups
- metrics that are actually useful
- event provenance
- open canonical block

**Rule:** Library organizes the same canonical events; it does not clone them.

## 6. ROOM: COLLECTIVE INTELLIGENCE

**Purpose:** Turn intentionally shared, de-identified personal learning into collective value.

**Must contain:**
- privacy explanation
- contribution status
- consent control
- de-identification explanation
- collective intelligence stream
- ability to withdraw/disable contribution
- clear boundary between private and collective

**Law:** Private by default. Shared by choice. Collective by consent.

## 7. ROOM: EVIDENCE

**Purpose:** Truth/verification room.

**Must contain:**
- Human evidence
- Naya evidence/status
- Machine evidence
- Feed projection state
- receipts
- verified/unverified state
- timestamps/IDs/provenance

**Rule:** This room exists to prevent source intent from being mistaken for runtime truth.

## 8. ROOM: CONNECTIONS

**Purpose:** Manage the user's saved human NayaNET network.

**Critical definition:** Connections is **not** the room for GitHub, APIs, technical integrations, sync providers, or machine/data-source connections. Those belong in system/adapter architecture.

A person enters Connections because the user **met/interacted with them through a NayaNET Smart Space and deliberately chose to save that relationship**.

**Core lifecycle:**
`DISCOVER → JOIN SPACE → INTERACT → CHOOSE PERSON → SAVE CONNECTION → ORGANIZE → MESSAGE / RECONNECT`

**Must contain:**
- saved people
- Smart Name
- Smart Alias
- user-defined connection groups/categories
- connection search
- connection detail
- remove/archive connection
- Message / Smart Mail action
- Create / Request Smart Space action where permitted

**Connection rules:**
- Joining a Space does not automatically create a saved Connection.
- Saving a Connection is an explicit user action.
- A person may belong to multiple user-defined groups.
- Groups are organizational containers, not separate identities.
- Connections must be searchable without fabricating contacts.

**Example groups:** Friends, Family, Church, Business, Project, Team, Community, Topic, Mastermind, or any custom user-defined category.

**Important relationship:** Saved Connections become a natural recipient source for Smart Mail and Smart Messaging.

## 9. ROOM: SMART MAIL

**Purpose:** NayaNET communication with saved Connections and permitted recipients.

**Must contain:**
- Inbox
- Sent
- Drafts
- Connections
- Rooms / Spaces where appropriate
- Groups
- Lists
- compose
- recipient selection
- message body
- communication modes
- truthful delivery state
- receipts

**Group messaging requirement:** A user can select an organized Connection group and send one message to that selected group, subject to recipient/communication permissions.

**Important:** Smart Mail and Smart Messaging are related but distinct:
- **Space Message:** shared with participants in a Smart Space.
- **Direct Message:** private person-to-person communication.
- **Smart Mail:** persistent communication workflow that can target saved Connections/groups and other permitted recipients.

A Space may provide a route into messaging its participants where permissions allow.

**Important:** A draft is not a sent message. A pending transport is not delivery.

## 10. ROOM: SMART SPACE

**Purpose:** A living shared intelligence environment created around a topic, question, idea, project, challenge, opportunity, or Intelligent Board.

**Core definition:**
`TOPIC + PEOPLE + CONVERSATION + INTELLIGENCE + CONSENT`

A Smart Space is where people meet and communicate around something meaningful. It is not merely a group chat and is not a technical integration.

**Primary creation path:** Every eligible Intelligent Board exposes **CREATE SMART SPACE**. The Board becomes seed context; people are never automatically added. The creator reviews the Space and explicitly publishes/invites it.

**Other creation paths:**
- Smart Note → Create Smart Space
- Ask Naya → Create Smart Space
- Existing Space → Create Related Space

**After publication:** The Space invitation enters the Activity Feed so relevant users can discover and choose to join.

**Joining:** Joining is explicit. Joining does not automatically save every participant as a permanent Connection.

**Space contents:**
- title/topic
- description/opening question
- source/seed context
- shared conversation
- participant list
- Naya intelligence/weaving layer
- emerging intelligence
- distilled wisdom/lessons/meaning/actions
- connection actions
- messaging actions
- consent/share controls
- lifecycle controls

**Space conversation:** Participants can post messages, reply where supported, ask Naya about the conversation, inspect participants, save Connections, and participate in intelligence distillation.

**Intelligence loop:**
`CONVERSATION → NAYA WEAVES → EMERGING INTELLIGENCE → DISTILLATION → REVIEW → SHARE WISDOM BY CONSENT → COLLECTIVE`

**Connection loop:**
`MEET → INTERACT → SAVE CONNECTION → ORGANIZE → SMART MAIL / DIRECT MESSAGE → CREATE/REQUEST ANOTHER SPACE`

**Creator control:** The person who creates the Space is its Creator/Owner. The Creator can publish, manage creator-level controls, and **CLOSE SPACE**. Participants cannot unilaterally close someone else's Space.

**Leave vs close:**
- `LEAVE SPACE` = one participant exits.
- `CLOSE SPACE` = Creator ends active participation/conversation for the Space.

**Space lifecycle:**
`PROPOSED → ACTIVE → QUIET → CLOSED`

A Space may remain open indefinitely if its Creator chooses. It may also be closed when the conversation is complete. A closed Space remains subject to retention/privacy rules; closing does not make it public.

**Share Wisdom:** Space intelligence is never automatically added to Collective Intelligence. Participants must deliberately review and consent to a proposed wisdom contribution.

**Mastermind use case:** A group can deliberately create a Space to solve a problem, discover breakthroughs, distill the resulting intelligence, and intentionally contribute approved wisdom to the Collective.

**See:** `13-SMART-SPACE-MESSAGING-CONNECTION-CONTRACT.md` for the complete product and verification contract.

## 11. ROOM: SETTINGS

**Purpose:** Control how the Hub operates.

**Required areas:**

### Intelligence
- Smart Notes automatic capture
- intelligence processing/enrichment
- learning/compounding behavior

### Communication
- Smart Mail enabled
- notification behavior

### Privacy
- collective contribution
- sharing defaults
- visibility defaults

### Connections
- connection/privacy controls
- communication permissions

### Experience
- appearance/preferences where applicable
- reduced motion/accessibility
- notification preferences

### Account
- identity/profile
- alias
- ambassador/referral where applicable

Every setting must specify: what it changes, scope, default, persistence, immediate effect, failure behavior, and where the setting is enforced.

## 12. TOP BAR

**Purpose:** Persistent context and high-value global status.

**Required contents:**
- current page/room title
- global search entry or compact search control
- truthful connection/status indicator where applicable
- Naya presence/access
- account/profile access if intentionally enabled

**Visual:** premium, quiet, never competing with the feed.

**Rule:** Top bar should not become a dumping ground for controls.

## 13. LOWER BAR / FEATURE REPORT BAR

**Purpose:** Persistent access to the five foundational feature principles/reports.

**Required items:**
- SMART NOTES
- NO DEAD ENDS
- CONTEXT LAW
- 10-STAR SERVICE
- ADAPTIVE LEARNING

**Behavior:** external report links; preserve exact destinations from the frozen reference unless intentionally changed.

Desktop: fixed/anchored lower strip.
Mobile: positioned above mobile navigation without obscuring content.

## 14. LEFT SIDEBAR

**Purpose:** primary room navigation.

**Required grouping:**

### PERSONAL
- Home / Intelligence Today
- Smart Notes
- Daily Intelligence / Reports
- Intelligence Library

### COLLECTIVE
- Collective Intelligence
- Evidence
- Connections

### COMMUNICATION
- Smart Mail
- Smart Spaces where intentionally exposed as a top-level entry

### SYSTEM
- Settings

**Visual:** premium dark rail, clear active state, beautiful icons, readable labels, optional truthful badges.

**No right Hub sidebar.**

## 15. MOBILE NAVIGATION

**Purpose:** replace persistent sidebar on small screens.

**Reference five-item pattern:** Home, Notes, Reports, Intel, Mail.

The new build may preserve this pattern while ensuring access to Collective, Evidence, Connections, Smart Spaces and Settings through a deliberate More/Menu mechanism.

**Requirement:** no important room may become inaccessible on mobile.

## 16. ECOSYSTEM LINK BAR

**Purpose:** connect the Hub to the broader NayaNET/HMC ecosystem.

Frozen-reference destinations:

| Label | Destination |
|---|---|
| HOME | https://hmclibrary.groovemember.net/home |
| NAYA POWER | https://academy.nayanet.app/ |
| 5 DAY CHALLENGE | https://academy.nayanet.app/ |
| ENTER FREE | https://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab |
| POWERCASTS | https://nayanet.groovepages.com/powerplayer |
| WHITE PAPER | https://nayanet.groovepages.com/whitepaper |
| ABOUT US | https://nayanet.groovepages.com/aboutus |
| HMC LOGIN | https://hmclibrary.groovemember.net/login |

## 17. SEARCH ENGINE

**Purpose:** Find intelligence, people, Spaces, and retained relationships rather than merely filter visible cards.

Must search across:
- Smart Notes
- Intelligent Blocks
- Human perspective
- Naya perspective
- Machine evidence
- Weaver synthesis
- Lesson/Meaning/Action
- tags
- lists/groups/Spaces
- saved Connections
- reports where indexed

Each result must show why it matched and open the original canonical object/event.

Search modes may include:
- exact/keyword
- semantic when a real intelligence backend exists
- filters
- recent/favorites
- personal/collective/activity scope

Search must not fabricate semantic answers when semantic intelligence is unavailable.

## 18. NAYA ACCESS

Naya should be available as an intelligent partner, not merely a portrait.

Possible entry points:
- Ask Naya
- ask about this block
- ask about this Space
- explain
- summarize
- compare
- find related intelligence
- suggest next action
- help distill Space intelligence

All responses must declare their source/trust state where consequential.

## 19. CROSS-ROOM CONNECTIONS

```text
HOME
 ├─ Search → Intelligence Library / canonical event / Connections / Spaces
 ├─ Capture → Smart Note
 ├─ Smart Note → Intelligent Feed / Create Space
 ├─ Intelligent Board → Create Smart Space
 ├─ Smart Space → Activity Feed / Conversation / Participants
 ├─ Space participant → Save Connection
 ├─ Connection → Groups / Search / Smart Mail / Direct Message / Create Space
 ├─ Space conversation → Naya Weaving → Intelligence
 ├─ Space intelligence → Wisdom Review → Collective by Consent
 ├─ Naya → Event enrichment / Space weaving
 ├─ Machine → Evidence / receipt
 └─ Action → next event / learning

SETTINGS → controls all applicable rooms
SMART MAIL → communication workflow
TECHNICAL INTEGRATIONS → explicit system adapters, not Connections
```

## 20. VISUAL HOUSE LANGUAGE

Every room belongs to the same visual system:
- obsidian/black foundation
- white high-contrast typography
- purple/magenta intelligence light
- sapphire/blue machine/source accent
- green verified/success
- restrained gold for evidence/significance/caution
- dimensional surfaces
- tactile elevation
- beautiful icons
- strong whitespace
- editorial hierarchy
- controlled glow

The Hub should feel like one extraordinary instrument, not ten unrelated pages.

**Sizing law:** Controls, cards, navigation items, and connection objects must be compact enough to scan quickly. Do not use oversized UI merely to make the interface look premium. Premium means clarity, hierarchy, proportion, and purposeful space.

## 21. ROOM DEFINITION TEMPLATE

Every future room must answer these questions before implementation:

1. What is the room called?
2. Why does it exist?
3. What user problem does it solve?
4. What must the user see first?
5. What objects live inside it?
6. What can the user create?
7. What can the user edit?
8. What can the user delete/close/leave?
9. What can the user click?
10. Where does every click go?
11. What changes immediately?
12. What persists?
13. Where does the data live?
14. What other rooms consume that data?
15. What permissions apply?
16. What are empty/pending/error states?
17. What does desktop look like?
18. What does mobile look like?
19. What is the accessibility contract?
20. How is the room verified in production?

If any answer is unknown, mark it **OPEN DECISION** rather than inventing it.
