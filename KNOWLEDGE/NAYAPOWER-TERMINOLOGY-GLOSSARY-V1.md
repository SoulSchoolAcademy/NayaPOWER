# NAYAPOWER — TERMINOLOGY GLOSSARY V1

**Status:** CANONICAL — TERMINOLOGY AUTHORITY
**Effective:** 2026-09-28
**Authority:** NayaPOWER System North Star Ratification (2026-09-26) + NayaNET Constitutional Contract Law
**Purpose:** Resolve the contradictory terminology accumulated across the KNOWLEDGE corpus so that every Naya, human, and contract uses ONE canonical term per concept.

---

## 1. Why this glossary exists

Across the numbered KNOWLEDGE concept corpus the same concepts appear under different names:
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
DISTILLATION               (what it means)
    ↓
INTELLIGENT BLOCK          (the canonical durable intelligence unit, IB-...)
    ↓
SMART NOTE                 (the universal capture command + human-readable projection)
    ↓
SMART LINK                 (the verified, evidence-bearing doorway to that projection)
```

---

## 3. Definitions

### 3.1 Master Node — CANONICAL
**A reserved processing responsibility in the Nine-Node kernel.**

The only canonical kernel Nodes are:

`SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE`

A Master Node processes intelligence. A note or idea does **not** become a Master Node.

- `Naya Node` is now an **ambiguous historical term**. In new work, do not use it as the name of an intelligence object.
- If an older source says “Naya Node” and means durable intelligence, normalize to **Intelligent Block**.
- If it means a kernel responsibility, normalize to **Master Node**.
- If it means a separate persistent Naya identity/agent, use the explicit identity term defined by the identity contract; do not infer from this glossary.
- This reconciliation supersedes older concept-file language that treated “Naya Node” as the canonical semantic intelligence unit.

### 3.1A Smart Node — ACCEPTED HISTORICAL / HUMAN ALIAS
**A human shorthand for the Smart Note capture intent; not an object type.**

“Make this a Smart Node” remains a supported phrase for compatibility. It normalizes through NIA Language to `CAPTURE_DURABLE_INTELLIGENCE`.

The preferred universal command is now:

> **“Smart Note this.”**

Smart Node MUST NOT become a tenth Master Node, a durable object family, a database table, or a second graph.

### 3.2 Intelligent Block — CANONICAL
**The canonical durable unit of governed intelligence.**

An Intelligent Block is the persistent, provenance-bound object produced or refined by the governed Receiver. It owns the durable intelligence identity (`IB-...`), truth state, source lineage, applicability, relationships, evidence, and lifecycle.

- Intelligent Block is the object the system retains, indexes, retrieves, connects, verifies, learns from, supersedes, and passes to successors.
- Repository projections MUST NOT become a second source of truth.
- The Receiver owns canonical identity. Deterministic IDs are valid only where the canonical Receiver contract itself defines them.

### 3.3 Smart Note — CANONICAL UNIVERSAL CAPTURE COMMAND + PROJECTION
**The human command for durable capture and the human/Naya-readable projection of the resulting Intelligent Block.**

Primary command:

> **“Smart Note this.”**

NIA Language normalizes that phrase to `CAPTURE_DURABLE_INTELLIGENCE`.

After canonical commit, the Smart Note projection belongs at:

`.naya/memory/smart-notes/YYYY/MM/DD/category/topic/subtopic/IB-.../smart-note.md`

The path is navigation, not truth. The Intelligent Block remains canonical. The projection MUST carry the IB identity and provenance pointers and MUST be generated from verified persisted intelligence.

- Automatic capture may create/refine **CANDIDATE** intelligence only.
- A Smart Note projection does not create authority and does not prove learning.
- “Smart Node”, “lock this in”, and related phrases are aliases handled by the NIA Language contract.
- Canonical intent contract: `BRAIN/00-SPEC/0006-NIA-LANGUAGE-INTENT-CONTRACT-V1.md`.

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

An Intelligent Event is the immutable record of an occurrence: source/history from which intelligence may be distilled.

**EVENT ≠ INTELLIGENT BLOCK ≠ SMART NOTE PROJECTION ≠ LEARNING ≠ VERIFIED LEARNING.**

### 3.6 Experience Intelligence — CANONICAL CLASSIFICATION
Human, project, workflow, or domain intelligence represented as Intelligent Blocks and relationships. Older “Experience Node” language is historical unless a separate agent identity contract explicitly applies.

### 3.7 Meta-Intelligence — CANONICAL CLASSIFICATION
Intelligence about NayaPOWER/NayaNET itself: system behavior, drift, proof gaps, and bounded improvement candidates. It is represented as Intelligent Blocks and relationships. Older “Meta-Intelligence Node” terminology is historical.

---

## 4. Relationship map

```
INTELLIGENT EVENT  ──distills / derives──▶  INTELLIGENT BLOCK
                                                                    │
                                                                    ├──projects──▶  SMART NOTE
                                                                    │                    │
                                                                    └──receipts──▶  SMART LINK (to the Smart Note artifact)

MASTER NODES       ──process──▶  INTELLIGENT BLOCKS
EXPERIENCE / META-INTELLIGENCE are classifications carried by Blocks/relationships

SMART NOTE  ≠  INTELLIGENT BLOCK          (projection ≠ canonical object)
SMART LINK  ≠  SMART NOTE                 (doorway ≠ content)
SMART LINK  ≠  HUB DEEP LINK ≠ EVIDENCE LINK
EVENT       ≠  NODE ≠  UNDERSTANDING ≠  LESSON ≠  LEARNING ≠  VERIFIED LEARNING
```

---

## 5. Historical terms (DO NOT USE in new work)

| Historical term | Canonical term | Why retired |
|-----------------|----------------|-------------|
| Naya Node (as semantic intelligence object) | Intelligent Block | Ambiguous historical term; new work reserves Node for the Nine Master Nodes unless an explicit identity contract says otherwise |
| Smart Node | Smart Note capture alias | Supported human alias, not an object type |
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
