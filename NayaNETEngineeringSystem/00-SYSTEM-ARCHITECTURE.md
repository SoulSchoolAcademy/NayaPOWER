# 00 — NayaNET System Architecture

## 1. Definition
NayaNET is the network/ecosystem in which humans, Naya/Superbrains, intelligence, communication, collaboration and services connect. NayaPOWER is the operating/governance architecture around intelligence and action. The Hub is the human-facing cockpit; it is not the canonical engine or source of truth.

## 2. North-star flow
```text
HUMAN INTENT + AUTHORITY
        ↓
NAYA POWER / SUPERBRAIN
        ↓
MISSION STATE / LEAD MODE
        ↓
CAPTURE → UNDERSTAND → ORGANIZE
        ↓
PRIMARY INTELLIGENCE SYSTEM
        ↓
COMPOUNDING + ADAPTIVE LEARNING
        ↓
EVIDENCE + VALUE + QUALITY
        ↓
CONNECTION + COMMUNICATION + COLLABORATION
        ↓
CONSENTED COLLECTIVE INTELLIGENCE
        ↓
CCT / CONTINUOUS CHAIN
        ↓
INTELLIGENT HUB PROJECTION
        ↓
HUMAN OUTCOME
        ↓
NEW LEARNING
```

## 3. Product surfaces
| Surface | Owns the experience of | Must not become |
|---|---|---|
| Smart Notes | durable meaningful intelligence events | generic activity log |
| Your Intelligence Today | daily synthesis of what mattered | duplicate feed |
| Intelligent Reports | longer-period synthesis/patterns/lessons | daily feed |
| Intelligent Library | durable searchable knowledge/meaning | social stream |
| Smart Lists | intentional organization/references | duplicate content store |
| Smart Feed | living presentation/discovery/activity | canonical database |
| Smart Tabs | navigation/retrieval views | storage silos |
| Connections | people/relationships | message transport |
| Smart Mail | intentional asynchronous delivery | live chat |
| Smart Spaces | topic-centered interaction/collaboration | private-data dump |
| Smart Share | explicit controlled sharing | implicit publication |
| Smart Ledger | event/provenance/integrity evidence | business-domain source of truth |
| PIS | primary intelligence flow | UI |
| CIS | compounding intelligence | mere archive |
| Adaptive Learning | verified learning/change | engagement optimizer |

## 4. System boundaries
- **Human authority:** the human sets destination and grants authority; AI intelligence does not create authority.
- **Privacy:** private by default; shared by choice; collective by consent; public by decision.
- **Truth:** publication, popularity, likes, comments, saves and list membership do not equal verification.
- **Canonicality:** derived views reference canonical objects rather than silently creating competing copies.
- **Activity:** an event is not automatically durable intelligence.
- **Evidence:** verification must follow the actual claim through implementation/runtime evidence.

## 5. Core relationships
```text
SMART NOTE → PIS → CIS → ADAPTIVE LEARNING → SUPERBRAIN
SMART NOTE / EVENT → SMART FEED
SMART NOTE → SMART LIST
SMART NOTE → SMART SHARE → COLLECTIVE INTELLIGENCE (when authorized)
SMART NOTE / TOPIC → SMART SPACE → PEOPLE → CONNECTIONS
CONNECTIONS → SMART MAIL → RECIPIENTS / SPACES
MEANINGFUL EVENTS → SMART LEDGER / PROVENANCE
PIS/CIS/LEDGER/OTHER CANONICAL SOURCES → TODAY / REPORTS / LIBRARY
ALL CANONICAL SYSTEMS → HUB PROJECTIONS
```

## 6. Engineering rule
No feature is designed in isolation. Before implementation, NIS must identify the canonical owner of every object it reads/writes, the authority boundary, event emitted, downstream consumers, and verification path.

## 7. Definition of done
A cold NIS can explain what each surface does, what it owns, what it consumes, what it emits, how it connects, where its UI lives, where its backend lives, and what evidence proves it works.

## Source authority
`.naya/NAYAPOWER-01-58-SYSTEM-MAP-DEFINITION-DIRECTIVE-V1.md`, `.naya/2026-09-11-18-35-NAYAPOWER-32-MASTER-SYSTEM-ARCHITECTURE.md`, and 01–58 source artifacts.
