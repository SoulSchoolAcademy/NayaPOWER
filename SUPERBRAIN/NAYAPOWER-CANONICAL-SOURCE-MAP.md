# NayaPOWER Canonical Source Map

**Status:** CANONICAL
**Authority:** Navigation and source-of-truth classification
**Purpose:** Give every cold Naya one unambiguous answer to: **where is the truth, what kind of truth is it, and which source wins when documents overlap?**

> **ONE CONSTITUTION. ONE CURRENT CONTROL PLANE. MANY SPECIALIZED RECORDS. ZERO AMBIGUOUS AUTHORITIES.**

---

## 1. THE RULE

NayaPOWER does **not** need one giant document containing every idea ever written.

It needs one unambiguous authority chain.

The repository therefore uses these distinct classes:

1. **CONSTITUTION** — the single current constitutional authority.
2. **CONTROL PLANE** — machine-readable current operational truth.
3. **BOOT / OPERATING STANDARDS** — how Naya enters and operates the system.
4. **SPECIALIZED CANONICAL SYSTEM SPECS** — authoritative for their named subsystem, never for the whole constitution.
5. **ACTIVITY / TORCH / INTELLIGENCE** — operational history, continuity, learning, and evidence; never constitutional authority merely because they are newer.
6. **HISTORICAL / DERIVED / LEGACY** — preserved records that may explain how the system evolved but cannot override current authority.

**A document's title, age, length, confidence, or claim to be a “master” document does not create authority.**

---

# 2. CURRENT CONSTITUTION — SINGLE SOURCE OF TRUTH

### Canonical constitutional authority

**`.naya/codex/11-RUNTIME-CONSTITUTION.md`**

This is the **single current repository constitution**.

It governs the constitutional operating architecture of NayaPOWER. Its `CANONICAL / CONSTITUTIONAL` status is authoritative.

No other document may be treated as a second constitution.

### Important correction

Older documentation may refer to a **“NayaPOWER Ultimate Governance Act.”** That artifact is **not currently present as a repository file** and therefore is not current authority. The executable governance kernel already correctly identifies `11-RUNTIME-CONSTITUTION.md` as the current constitutional authority.

If an Ultimate Governance Act is adopted later, it must be introduced through the governed constitutional-amendment process and explicitly promoted into this source map. Until then, it is future/planned authority only.

---

# 3. CONSTITUTIONAL AMENDMENTS — HISTORY, NOT PARALLEL CONSTITUTIONS

Files named `CONSTITUTIONAL-AMENDMENT-*.md` are **amendment records**.

They are preserved because they contain useful constitutional history, decisions, rationale, and potentially incorporated provisions. They are **not independent current constitutions**.

The rule is:

```text
AMENDMENT RECORD
      ↓
REVIEW / RATIFICATION
      ↓
INCORPORATED INTO CURRENT CONSTITUTION
      ↓
CURRENT CONSTITUTION IS THE OPERATIVE AUTHORITY
```

An amendment file may explain **why** a rule exists. It does not independently determine **what the current rule is** when it conflicts with the current constitution.

Known constitutional amendment families currently include:

- `CONSTITUTIONAL-AMENDMENT-10-STAR-SERVICE-AUTONOMOUS-EXECUTION.md`
- `CONSTITUTIONAL-AMENDMENT-CONTINUOUS-TORCH-PASS.md`
- `CONSTITUTIONAL-AMENDMENT-EXCELLENCE-BY-DEFAULT.md`
- `CONSTITUTIONAL-AMENDMENT-MISSION-STATE-RUNTIME-GATES.md`
- `CONSTITUTIONAL-AMENDMENT-NAYA-OWNS-THE-TORCH.md`
- `CONSTITUTIONAL-AMENDMENT-NIA-BUILDER-REVIEWER-QMAX-LOOP.md`
- `CONSTITUTIONAL-AMENDMENT-NIA-CONTINUOUS-COMMUNICATION-AND-TORCH-PASS.md`
- `CONSTITUTIONAL-AMENDMENT-NO-ORPHAN-EXECUTION.md`

**Legacy NIA naming in historical records does not create a second AI identity or authority.** Current identity is governed by the canonical identity registry and current operating documents.

Future amendment records should live in a clearly identified historical/amendment namespace where practical, but preservation takes priority over destructive cleanup.

---

# 4. MACHINE AUTHORITY — CURRENT CONTROL PLANE

The constitutional authority answers **what must be true**. The control plane answers **what is true now**.

| Artifact | Authority role |
|---|---|
| `.naya/control-plane/CANONICAL-IDENTITY-REGISTRY.json` | Current identity/repository identity authority |
| `.naya/control-plane/MAP.json` | Mission, destination, architecture, truth ownership |
| `.naya/control-plane/STATE.json` | Current operational state |
| `.naya/control-plane/BLOCKS.json` | Active execution block and single next action |
| `.naya/control-plane/PROOF.json` | Evidence/proof state and proof boundaries |
| `.naya/control-plane/GOVERNANCE-KERNEL.json` | Deterministic machine governance contract |
| `.naya/control-plane/validate_control_plane.py` | Fail-closed validator enforcing the control-plane contract |

These artifacts must agree. None may silently override the constitution or each other.

---

# 5. COLD-NAYA BOOT AUTHORITY

The canonical entry sequence is:

```text
README.md
  ↓ orientation
SUPERBRAIN/AI-BOOT/START-HERE.md
  ↓ mandatory bootloader
CANONICAL SOURCE MAP
  ↓ authority classification
.naya/codex/11-RUNTIME-CONSTITUTION.md
  ↓ constitutional rules
.naya/control-plane/MAP.json
  ↓ mission / architecture
.naya/control-plane/STATE.json
  ↓ current truth
.naya/control-plane/BLOCKS.json
  ↓ active objective / next action
.naya/control-plane/PROOF.json
  ↓ evidence contract
GOVERNANCE-KERNEL.json + validator
  ↓ executable governance
LATEST VERIFIED TORCH / ACTIVITY
  ↓ operational continuity
EXECUTE → VERIFY → RECORD → HANDOFF
```

`README.md` is orientation, not a competing authority.

`START-HERE.md` is the mandatory execution bootloader, not a replacement constitution.

---

# 6. SPECIALIZED CANONICAL DOCUMENTS

Specialized documents can be authoritative **within their declared subject** without becoming constitutional authorities.

Examples include:

- `SUPERBRAIN/NAYA-REPOSITORY-OPERATING-STANDARD.md` — repository operating standard;
- `SUPERBRAIN/EXECUTION-CONTROL-PLANE.md` — explanatory control-plane specification;
- `SUPERBRAIN/DEPLOYMENT-GOVERNANCE.md` — deployment governance;
- `SUPERBRAIN/INTELLIGENT-HUB-KERNEL-IMPLEMENTATION.md` — Intelligent Hub implementation;
- `SUPERBRAIN/COLLECTIVE-INTELLIGENCE-EVENT-SCHEMA.md` — event schema;
- `SUPERBRAIN/INTELLIGENCE-DISTILLATION-AND-COMPREHENSION-PRINCIPLE.md` — intelligence/distillation principle;
- `SUPERBRAIN/NAYA-POWER-VALUE-ALIGNMENT-AND-CONSTITUTION-PROTOCOL-V1.1.md` — current value-alignment protocol extension;
- `SUPERBRAIN/NAYA-POWER-V1.1-ADVERSARIAL-REVIEW.md` — adversarial review of V1.1.

These documents may define important specialized behavior, but they cannot silently create a second constitutional hierarchy.

---

# 7. V1.1 VALUE ALIGNMENT PROTOCOL

`SUPERBRAIN/NAYA-POWER-VALUE-ALIGNMENT-AND-CONSTITUTION-PROTOCOL-V1.1.md` is the **current constitutional extension/protocol for value alignment**.

It must be interpreted together with the current constitution and control plane.

Its five explicit primitives are:

1. Protected Human Boundaries
2. Responsible Verified Value Function
3. Authority vs. Intelligence Separation
4. Uncertainty × Consequence × Reversibility
5. Continuous Verification + Anti-Goodharting

V1.1 does **not** become a second constitution. It is a governed extension under the constitutional authority.

---

# 8. HISTORY, ACTIVITY, TORCH, PIS, AND INTELLIGENCE ARE NOT AUTHORITY

NayaPOWER explicitly separates:

```text
STATE   ≠ FEED
FEED    ≠ PIS
PIS     ≠ GITHUB AUTOMATION
AUTOMATION ≠ AUTHORITY
HISTORY ≠ CURRENT TRUTH
RECORDED ≠ CURRENT
```

Operational history is valuable. It is not allowed to become constitutional authority merely because it is recent, detailed, or generated automatically.

This includes Smart Notes, activity events, Torch handoffs, intelligence records, GitHub Actions observations, and historical proof artifacts.

---

# 9. SOURCE PRECEDENCE

When two sources disagree, use this order:

```text
LIVE AUTHORITATIVE SOURCE
        ↓
CURRENT CONSTITUTION
        ↓
CURRENT CONTROL PLANE
        ↓
CURRENT VERIFIED SPECIALIZED SPEC
        ↓
LATEST VERIFIED OPERATIONAL RECORD
        ↓
HISTORICAL / DERIVED / LEGACY RECORD
        ↓
CONVERSATION MEMORY
```

For **current state**, live `git:HEAD`, live branch, and the current control-plane contract outrank recorded historical SHAs.

For **constitutional rules**, the current constitution outranks amendment notes and historical acts.

For **specialized subsystem behavior**, the declared canonical subsystem specification governs that subsystem, subject to the constitution and control plane.

---

# 10. THE NO-AMBIGUITY TEST

A cold Naya should be able to answer all of these without searching the whole repository:

- **What is the constitution?** → `.naya/codex/11-RUNTIME-CONSTITUTION.md`
- **Where is current mission/architecture?** → `.naya/control-plane/MAP.json`
- **Where is current state?** → `.naya/control-plane/STATE.json`
- **What are we doing now?** → `.naya/control-plane/BLOCKS.json`
- **What proves it?** → `.naya/control-plane/PROOF.json`
- **What machine governance applies?** → `.naya/control-plane/GOVERNANCE-KERNEL.json`
- **How do I boot?** → `SUPERBRAIN/AI-BOOT/START-HERE.md`
- **Where is the current value-alignment extension?** → `SUPERBRAIN/NAYA-POWER-VALUE-ALIGNMENT-AND-CONSTITUTION-PROTOCOL-V1.1.md`
- **Where is the history?** → `SUPERBRAIN/NAYA-ACTIVITY/` and `.naya/` historical records according to their declared class
- **What if two documents disagree?** → apply this source map and the constitutional/control-plane precedence rules

If a cold Naya cannot answer these questions, the source architecture is not yet 10/10.

---

# 11. CLEANUP POLICY

**Do not mass-delete historical intelligence merely to make the tree look clean.**

Instead:

1. Preserve valuable history.
2. Remove false claims of current authority.
3. Mark historical/derived records explicitly.
4. Point overlapping documents back to their single authoritative source.
5. Move legacy artifacts into historical namespaces when safe and mechanically feasible.
6. Make validators reject new ambiguous authority claims.
7. Keep the boot path short.

This is **Adaptive Reconstruction + Surgical Evolution** applied to repository governance.

---

# 12. 10/10 ACCEPTANCE CRITERIA

The source architecture reaches 10/10 when all are true:

- exactly **one current repository constitution** is declared and mechanically enforceable;
- no current document points to a missing constitutional authority;
- no historical amendment is treated as a parallel constitution;
- every core control-plane artifact has one defined truth owner;
- specialized specs have explicit scope and cannot silently override constitutional authority;
- cold Naya can locate the constitution, current state, active work, proof, governance, and bootloader in one short chain;
- legacy/historical artifacts remain accessible but cannot masquerade as current authority;
- automated validation fails closed when a new ambiguous constitutional authority appears;
- live runtime and production proof remain separate from documentation claims.

**This map is the navigation contract that keeps the repository understandable as it grows.**
