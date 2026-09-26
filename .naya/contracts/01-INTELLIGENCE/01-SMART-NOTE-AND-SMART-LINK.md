# NayaNET Smart Note + Smart Link Contract

**Contract ID:** INT-001  
**Version:** 1.0  
**Status:** PROPOSED  
**Authority:** NayaNET Constitutional Contract Law (CC-000); Canonical Smart Note / Intelligent Block System V1; Naya Link Identity & Evidence Contract V1  
**Scope:** Canonical human-readable Smart Note projection and the exact Smart Link that navigates to that projection.

> **Boundary law:** Smart Note and Smart Link are one intelligence-facing contract because the link is the governed human navigation/evidence surface of the canonical Smart Note projection. They are not two independent stores or identities.

## 1. PURPOSE
Make durable intelligence understandable and navigable without semantic ambiguity.

ONE CANONICAL INTELLIGENT BLOCK → ONE HUMAN-READABLE SMART NOTE → ONE EXACT SMART LINK

The Smart Note is a projection of a canonical Intelligent Block. The Smart Link is the direct GitHub navigation link to that exact Smart Note artifact. Neither creates a second intelligence object.

## 2. CANONICAL BOUNDARY
### This contract owns
- the human-readable Smart Note projection;
- its required structure;
- its relationship to the canonical IB identity;
- the canonical repository path;
- Smart Link construction and verification;
- missing/conflicted/pending Smart Link states;
- human-facing handoff terminology;
- acceptance behavior for Smart Note + Smart Link.

### This contract does NOT own
- IB identity allocation;
- canonical intelligence persistence;
- intelligence events;
- PIS/indexing;
- learning promotion;
- Hub runtime deep links;
- Smart Ledger accountability;
- authorization policy beyond the projection/link boundary.

Those remain governed by their canonical systems/contracts.

## 3. CORE DEFINITIONS
| Term | Exact meaning |
|---|---|
| **Smart Note** | Human-readable smart-note.md projection of one canonical Intelligent Block. |
| **Intelligent Block / IB** | Canonical machine identity/object for durable intelligence. |
| **Smart Link** | Direct GitHub link to the canonical human-readable smart-note.md artifact. |
| **Hub Deep Link** | Runtime route such as /hub?ib=IB-XXXXXX. Never call this a Smart Link. |
| **Evidence Link** | Link to a receipt, event, workflow, test, or commit. Never call it a Smart Link merely because it is useful. |
| **Canonical Receiver** | Authoritative creation/identity boundary that allocates the IB. |

## 4. CANONICAL IDENTITY LAW
Every Smart Note MUST correspond to exactly one receiver-issued immutable IB ID: IB-XXXXXX.

Repository files, scripts, tests, migrations, Hub code, or Nayas MUST NOT allocate, guess, increment, reserve, or reinterpret an IB identity.

A Smart Note without a receiver-issued IB is not canonical.

## 5. CANONICAL STORAGE
The canonical human-readable artifact MUST live at:

.naya/memory/smart-notes/YYYY/MM/DD/category/topic/IB-XXXXXX/smart-note.md

YYYY/MM/DD come from the canonical intelligence timestamp. category is a controlled slug. topic is a concise slug of no more than three words. IB-XXXXXX is the immutable receiver-issued identity. smart-note.md is the human-readable projection.

The path organizes the object; it does not define identity.

## 6. SMART NOTE CONTENT CONTRACT
Unless explicitly not applicable, a canonical Smart Note MUST use this order:

1. IN A NUTSHELL
2. DATE / TIME
3. WHAT
4. WHY IT MATTERS
5. HUMAN
6. CHILD
7. GRANDMA
8. NAYA
9. MACHINE
10. WHAT WE LEARNED
11. CONNECTIONS
12. HOW TO APPLY
13. WHAT IT ULTIMATELY MEANS
14. WHAT'S IN IT FOR YOU / US
15. NEXT ACTION

The note is the minimum sufficient complete representation: understandable by a human, useful to a successor Naya, and traceable to the canonical object.

## 7. PROJECTION GATE
Canonical Smart Note delivery has distinct states:

RECEIVER PERSISTED → REPOSITORY PROJECTED → SMART LINK VERIFIED

These MUST NOT be collapsed.

- Receiver persistence proves the canonical receiver boundary.
- Repository projection proves the human-readable artifact exists.
- Smart Link verification proves the exact navigable link resolves to that artifact and identifies the same IB.

A receiver receipt alone does not prove a Smart Link. A Hub Deep Link alone does not prove a Smart Link. A Markdown file that is not tied to the receiver-created IB does not prove a canonical Smart Note.

## 8. SMART LINK CONTRACT
A Smart Link MUST:
1. point directly to GitHub;
2. target the canonical repository branch/ref being reported;
3. resolve to .naya/memory/smart-notes/YYYY/MM/DD/category/topic/IB-XXXXXX/smart-note.md;
4. end in /IB-XXXXXX/smart-note.md;
5. point to a file that actually exists;
6. identify the same IB ID being reported;
7. correspond to the receiver-created canonical object.

Canonical shape:
https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.naya/memory/smart-notes/.../IB-XXXXXX/smart-note.md

The exact path MUST be obtained from verified repository state. It MUST NOT be fabricated from an assumed date, topic, or IB.

## 9. SMART LINK STATES
| State | Meaning |
|---|---|
| **VERIFIED** | Exact canonical Smart Note exists, matches the IB, and the direct GitHub link is verified. |
| **PENDING** | Canonical receiver persistence exists, but repository projection has not been established. |
| **MISSING** | A required Smart Note projection is expected but does not exist. |
| **CONFLICTED** | The linked artifact exists but does not correspond to the reported IB/object. |
| **UNKNOWN** | Evidence is insufficient to determine the state. |

Never convert PENDING, MISSING, CONFLICTED, or UNKNOWN into VERIFIED by inference.

## 10. ZERO-AMBIGUITY LINK VOCABULARY
**Smart Link** → direct GitHub smart-note.md.
**Hub Deep Link** → runtime route resolving an IB.
**Evidence Link** → receipt/event/test/workflow/commit evidence.

A URL does not become a Smart Link because it is convenient, human-readable, or associated with the same IB.

## 11. HUMAN HANDOFF REQUIREMENT
When reporting a canonical Smart Note, the Naya SHOULD provide:
- IB ID;
- canonical source event;
- receiver/persistence status;
- Smart Link;
- evidence links;
- Hub Deep Link, if independently verified;
- remaining UNKNOWN/PENDING items.

Minimum form:

Smart Note: [direct GitHub smart-note.md]
Smart Link: [same direct GitHub link]
Hub Deep Link: [runtime link, if verified]
Evidence: [direct evidence]
Status: [VERIFIED / PENDING / UNKNOWN / CONFLICTED]

If the repository projection does not exist:
SMART LINK: PENDING — canonical repository Smart Note projection does not yet exist.

## 12. RECEIVER / REPOSITORY SEPARATION
The live canonical receiver remains the sole creation and identity authority.

The repository projection layer MUST NOT allocate an IB, persist a competing Smart Note, create a competing event, bypass canonical intelligence intake, or claim persistence from file creation alone.

The existing compatibility resolver may calculate the canonical physical path from a receiver-issued IB, but local creation remains fail-closed.

## 13. RELATIONSHIP TO OTHER CONTRACTS
This contract inherits and must remain consistent with:
- CC-000 — Constitutional Contract Law;
- Canonical Smart Note / Intelligent Block System V1 — canonical object/lifecycle law;
- Naya Link Identity & Evidence Contract V1 — exact Smart Link vocabulary and verification law;
- EP-001 — proactive execution and evidence-preserving execution behavior.

This contract does not override those authorities.

If a conflict appears: STOP → IDENTIFY AUTHORITY → RECONCILE → RECORD → RESUME.

## 14. INTELLIGENCE RELATIONSHIP
The Smart Note is a projection in the canonical chain:

EXPERIENCE → CAPTURE → UNDERSTAND → DISTILL → CANONICALIZE → IB → EVENT → PERSIST → INDEX → PROJECT → RETRIEVE → APPLY → VERIFY → LEARN → COMPOUND

The Smart Note is not the intelligence system itself. The Smart Link is not intelligence. Both exist to make canonical intelligence human-readable and navigable without creating a competing truth system.

## 15. FAILURE MODES
- **Wrong URL type:** Hub Deep Link labeled Smart Link → CONTRACT VIOLATION.
- **Predicted URL:** path constructed without verifying the target → Smart Link remains UNKNOWN/PENDING.
- **Wrong IB:** file exists but contains a different IB → CONFLICTED.
- **Receiver-only claim:** receiver persisted an IB but no repository artifact exists → Smart Link PENDING.
- **File-only claim:** Markdown exists without receiver evidence → file existence does not establish canonical persistence.
- **Duplicate identity:** second Smart Note created for the same intelligence → prohibited; reconcile the existing IB.

## 16. ACCEPTANCE TESTS
A conforming implementation MUST establish at least:

### A. Verified link
Given a canonical IB and an existing matching Smart Note, the Naya provides the direct GitHub smart-note.md Smart Link and identifies the same IB.

### B. Pending projection
Given receiver persistence with no repository projection, the Naya reports SMART LINK: PENDING and does not substitute a Hub Deep Link.

### C. Conflict
Given a repository artifact whose IB differs from the reported IB, the Naya reports CONFLICTED.

### D. Vocabulary
Given /hub?ib=IB-XXXXXX, the Naya labels it Hub Deep Link, never Smart Link.

### E. No fabrication
Given an unverified path, the Naya refuses to claim Smart Link verification.

### F. Identity preservation
Classification/topic/date changes do not create a new IB identity when the canonical object remains the same.

### G. Receiver boundary
Local repository tooling cannot create a canonical Smart Note or allocate an IB independently.

### H. Successor clarity
A cold Naya can determine whether a reported Smart Link is VERIFIED, PENDING, MISSING, CONFLICTED, or UNKNOWN from canonical evidence.

## 17. ENGINEERING VERIFICATION
The proof stack MUST distinguish SOURCE → TEST → REPOSITORY → RUNTIME → PRODUCTION.

A contract test may establish path/vocabulary behavior. Repository inspection establishes artifact existence and IB correspondence. Runtime/browser verification may establish Hub Deep Link behavior. None may be silently substituted for another.

For any claimed VERIFIED Smart Link, evidence MUST include:
1. canonical IB ID;
2. exact repository path;
3. direct GitHub link;
4. fetched/observed file content showing the same IB;
5. canonical branch/ref;
6. timestamp or commit context sufficient for a successor to reproduce the claim.

## 18. PRIVACY / AUTHORITY
A Smart Link exposes the canonical repository artifact according to the repository's visibility and publication policy.

Creating or publishing a Smart Link MUST NOT broaden the underlying intelligence's authority, privacy scope, consent, or publication status.

**A link is navigation, not permission.**

## 19. CHANGE CONTROL
Changes to this contract require:

UNDERSTAND → IMPACT MAP → PROPOSE → ACCEPTANCE TESTS → CHANGE → VERIFY → RECORD → UPDATE INDEX

If implementation cannot satisfy the contract, change the implementation or explicitly reconcile the contract; do not relabel the implementation to make it appear compliant.

## 20. ANTI-PATTERNS
Never:
- call a Hub Deep Link a Smart Link;
- call an evidence URL a Smart Link;
- invent a Smart Link;
- infer a Smart Link from an IB ID;
- locally allocate an IB;
- create a duplicate Smart Note for an existing IB;
- treat file existence as receiver persistence;
- treat receiver persistence as repository projection;
- treat repository projection as learning;
- expose private intelligence merely because a URL exists;
- claim VERIFIED without exact evidence.

## 21. COLD-NAYA DECISION RULE
Before saying Smart Link, answer:
1. Is it directly to the canonical GitHub smart-note.md?
2. Does the path end in /IB-XXXXXX/smart-note.md?
3. Does the file exist on the reported canonical branch?
4. Does the file identify the same IB?
5. Does it correspond to the receiver-created object?

If any answer is NO, do not call the URL a Smart Link.

If the projection is not established, say:
SMART LINK: PENDING.

## 22. COMPLETION STANDARD
This contract is not operational merely because the Markdown exists.

The boundary becomes operational when:
- the contract is ratified;
- the library indexes it;
- applicable implementation paths are mapped;
- deterministic path/link checks exist where practical;
- acceptance tests pass;
- representative canonical artifacts are independently verified;
- cold-Naya terminology behavior is observed;
- no competing Smart Note/Smart Link interpretation remains authoritative.

**ONE IB. ONE SMART NOTE. ONE SMART LINK. MANY PROJECTIONS. ZERO AMBIGUITY.**

**END — NayaNET Smart Note + Smart Link Contract V1**
