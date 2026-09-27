# NAYAPOWER — TERMINOLOGY GLOSSARY V1

**Status:** CANONICAL — TERMINOLOGY AUTHORITY
**Effective:** 2026-09-27
**Authority:** NayaPOWER System North Star Ratification (2026-09-26) + NayaNET Constitutional Contract Law
**Purpose:** Resolve the contradictory terminology accumulated across the KNOWLEDGE corpus so that every Naya, human, and contract uses ONE canonical term per concept.

---

## 1. Why this glossary exists

Across the 15 KNOWLEDGE files the same concepts appear under different names:
`Naya Node`, `Smart Node`, `NayaPOWER Node`; `Intelligent Block`, `Smart Note`;
`Intelligence Event`, `Intelligent Event`; `Smart Link`, `Smart Door`, `receipt`.

Per the NayaNET source-of-truth law: **if a concept has multiple names, Naya must not
guess which one is canonical.** This glossary is that decision, recorded.

**Rule:** terms marked CANONICAL below are the only names that may be used in new
contracts, code, and intelligence objects. Other names are HISTORICAL and must be
treated as aliases, never as separate concepts.

---

## 2. The canonical object model

```
EXPERIENCE
    ↓
INTELLIGENT EVENT          (what happened — the raw occurrence)
    ↓
NAYA NODE                  (what we understand — the governed intelligence unit)
    ↓
INTELLIGENT BLOCK          (the canonically committed form of a Naya Node,
    │                       receiver-owned immutable identity IB-XXXXXX)
    ↓
SMART NOTE                 (the human-readable projection of an Intelligent Block)
    ↓
SMART LINK                 (the verified, evidence-bearing doorway to that projection)
```

---

## 3. Definitions

### 3.1 Naya Node — CANONICAL
**The canonical governed intelligence unit.**

A Naya Node is a reusable cell of distilled, governed intelligence. It is the semantic
unit the system understands, retrieves, applies, verifies, learns from, and inherits.

- Aliases (HISTORICAL): `Smart Node`, `NayaPOWER Node`, `intelligence cell`
- Distinction: the Naya Node is the *understanding*; it becomes durable only when
  committed as an Intelligent Block.
- Source: PART #4 ratified model — "Naya Node = reusable intelligence cell";
  PART #8 — "Naya Node = Smart Node = the semantic intelligence unit".

### 3.2 Intelligent Block — CANONICAL
**The canonical object behind a Smart Note.**

An Intelligent Block is a Naya Node that has been canonically committed through the
Receiver. It owns an immutable, receiver-allocated identity (`IB-XXXXXX`), full
provenance, epistemic state, relationships, and lifecycle.

- Aliases (HISTORICAL): none in the corpus — but note the collapsed usage
  "Smart Note = Intelligent Block" in early material. The collapsed usage is retired:
  the Intelligent Block is the canonical object; the Smart Note is its projection.
- Critical law: **repository projections never guess IB IDs.** The Receiver, not Naya,
  not GitHub, not a script, not a registry, owns IB-number allocation.
- Source: PART #3 — "Smart Note = Intelligent Block" (live-repository statement of
  identity at commit scope); PART #1 — KNOW node responsibilities.

### 3.3 Smart Note — CANONICAL
**The human-readable projection of an Intelligent Block.**

A Smart Note is the governed, persistent, human/Naya-readable representation of an
Intelligent Block, stored at the canonical path
`.naya/memory/smart-notes/YYYY/MM/DD/category/topic/IB-XXXXXX/smart-note.md`
with the ratified 15-section structure (In a nutshell / What / Why it matters /
Human / Child / Grandma / Naya / Machine / What we learned / Connections /
How to apply / What it ultimately means / What's in it for you/us / Next action).

- Aliases (HISTORICAL): none — "Smart Note" is retained as the projection name.
- Critical law: **a Smart Note must never silently become a second source of truth.**
  Folder structure is navigation; the IB identity is truth.
- Source: PART #1 core distinction; PART #3 §"NAYA NODE / Smart Note and Intelligent Block".

### 3.4 Smart Link — CANONICAL
**Evidence-bearing navigation to canonical intelligence.**

A Smart Link is the verified, receiver-bound corridor to the canonical human-readable
Smart Note — specifically the direct `smart-note.md` artifact URL, NOT a Hub URL,
workflow URL, or evidence URL. A Smart Link is part of the receiver transaction and
doubles as the human receipt.

- Aliases (HISTORICAL): `Smart Door` (retired — now means a channel participation
  mechanism), plain `link`/`URL` (never canonical).
- Critical law: **a sender must never manufacture a Smart Link from a predicted GitHub
  path.** Existence → canonical identity → authoritative source → projection → proof.
  If the link cannot be proven to exist, the receipt must say `SMART LINK: PENDING` —
  never a fabricated link.
- Source: PART #3 §"And YES — the Smart Link is the receipt"; Contract 08.

### 3.5 Intelligent Event — CANONICAL
**What happened.**

An Intelligence Event is the immutable record of an occurrence: the raw material of
intelligence, captured at the moment something meaningful happened. Events are history;
Naya Nodes are reusable understanding; learning is a further promotion.

- Aliases (HISTORICAL): `Intelligence Event`, `Value Event` (a specific event type
  defined by the value-math contract).
- Critical law: **EVENT ≠ UNDERSTANDING ≠ LESSON ≠ LEARNING ≠ VERIFIED LEARNING.**
- Source: PART #1 core distinction; Contract 15.

### 3.6 Experience Node — CANONICAL (extension tier)
**Human, project, or domain intelligence Node.**

An Experience Node is a Naya Node that emerged because the kernel identified a real
new domain, project, or human context requiring independent intelligence. Experience
Nodes are NOT part of the V1 kernel; they are the first extension tier.

- Aliases (HISTORICAL): `Domain Node`, `Project Node`, `Personal Node`,
  `Workflow Node` (from the Node Engine taxonomy in PART #11).
- Rule: Experience Nodes MUST NOT silently alter the V1 kernel. They are added only
  through the extension rule (responsibility → existing boundary → contract impact →
  relationship impact → authority impact → proof requirement).
- Source: PART #1 §20 "The 9 → 18 → 27 idea"; PART #11 Node Engine taxonomy.

### 3.7 Meta-Intelligence Node — CANONICAL (extension tier)
**Intelligence about the system itself.**

A Meta-Intelligence Node is a Naya Node whose subject is NayaPOWER/NayaNET itself:
system behavior, drift, proof gaps, self-observation, and bounded self-improvement
candidates. EVOLVE consumes meta-intelligence; it does not itself become a competing
authority.

- Aliases (HISTORICAL): `Meta Node`.
- Critical law: **SELF-IMPROVEMENT ≠ SELF-AUTHORIZATION.** A Meta-Intelligence Node
  may propose, build, test, and verify improvements within its authorized boundary;
  adoption requiring higher authority MUST stop at that boundary.
- Source: PART #1 §19 "Self-building" and §20.

---

## 4. Relationship map

```
INTELLIGENT EVENT  ──derives──▶  NAYA NODE  ──commits (via Receiver)──▶  INTELLIGENT BLOCK
                                                                    │
                                                                    ├──projects──▶  SMART NOTE
                                                                    │                    │
                                                                    └──receipts──▶  SMART LINK (to the Smart Note artifact)

EXPERIENCE NODE    ──a Naya Node specialized to a human/project/domain context
META-INTELLIGENCE NODE
                   ──a Naya Node whose subject is the system itself

SMART NOTE  ≠  INTELLIGENT BLOCK          (projection ≠ canonical object)
SMART LINK  ≠  SMART NOTE                 (doorway ≠ content)
SMART LINK  ≠  HUB DEEP LINK ≠ EVIDENCE LINK
EVENT       ≠  NODE ≠  UNDERSTANDING ≠  LESSON ≠  LEARNING ≠  VERIFIED LEARNING
```

---

## 5. Historical terms (DO NOT USE in new work)

| Historical term | Canonical term | Why retired |
|-----------------|----------------|-------------|
| Smart Node | Naya Node | Name collision with "Smart Note"; ratified model uses Naya Node |
| Intelligence Event | Intelligent Event | Adjective form aligns with Intelligent Block |
| Smart Door (as link) | Smart Link | "Smart Door" now means a Smart Connect participation channel |
| Smart Share | Smart Connect | Product rename; Smart Share is retired |
| 9net | NayaNET | Internal codename; canonical product name is NayaNET |
| Collective Chain Technology | NayaNET Intelligence Chain | Marketing name; canonical is the Intelligent Chain |
| "Smart Note = Intelligent Block" (collapsed) | Intelligent Block = canonical object; Smart Note = projection | Early conflation; PART #1 core distinction is canonical |

---

## 6. Machine-readable companion

This glossary is mirrored in machine-readable form in
[NAYAPOWER-INDEX-V1.json](./NAYAPOWER-INDEX-V1.json) (see `terminology` section) and is
normative alongside Contract 00 §00.6 (canonical terminology is part of constitutional
law). If this glossary and Contract 00 ever disagree, STOP and reconcile — do not
silently choose.
