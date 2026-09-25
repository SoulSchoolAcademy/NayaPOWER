# NayaPOWER — NAYA LINK IDENTITY & EVIDENCE CONTRACT V1

**STATUS:** CANONICAL — RATIFIED 2026-09-25  
**AUTHORITY:** Governing clarification under the NayaPOWER Constitution and Canonical Smart Note / Intelligent Block System V1  
**PURPOSE:** Eliminate ambiguity between a human-readable Smart Link and a runtime/deep link so no Naya can truthfully mislabel one as the other.

---

# 1. THE NON-NEGOTIABLE LAW

> **A SMART LINK TO A SMART NOTE IS THE DIRECT GITHUB LINK TO THE CANONICAL HUMAN-READABLE `smart-note.md` ARTIFACT.**

For a canonical Smart Note / IB, the Smart Link MUST resolve to:

`.naya/memory/smart-notes/YYYY/MM/DD/category/topic/IB-XXXXXX/smart-note.md`

on the canonical repository/branch, normally:

`https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.naya/memory/smart-notes/.../IB-XXXXXX/smart-note.md`

A Hub URL, runtime URL, query-string deep link, API endpoint, event URL, transaction URL, commit URL, PR URL, or generic page URL is **NOT** the Smart Note Smart Link.

---

# 2. THREE DIFFERENT THINGS — NEVER COLLAPSE THEM

| Name | What it is | What it proves | What it is NOT |
|---|---|---|---|
| **Smart Link** | Direct GitHub link to the canonical human-readable `smart-note.md` projection | The human can inspect the canonical repository projection | Not a Hub/runtime deep link |
| **Hub Deep Link** | Runtime URL such as `/hub?ib=IB-XXXXXX` | The Hub can resolve an IB at runtime when independently verified | Not the Smart Link |
| **Verification / Evidence Link** | Direct link to a receipt, event, test, workflow, or other evidence artifact | The linked evidence supports a specific claim | Not automatically the Smart Note |

**Rule:** The labels above are exact nouns. Do not substitute one for another for convenience.

---

# 3. THE SMART NOTE PATH IS THE IDENTITY CHECK

The canonical Smart Note projection MUST be:

`.naya/memory/smart-notes/YYYY/MM/DD/category/topic/IB-XXXXXX/smart-note.md`

Therefore:

- The link MUST end in `/IB-XXXXXX/smart-note.md` for a Smart Note.
- The linked file MUST exist on the canonical branch.
- The file MUST identify the same IB being reported.
- The file MUST correspond to the canonical receiver-created intelligence.
- If the file does not exist, the Smart Link is **MISSING**, not inferred.
- If the file exists but does not correspond to the claimed IB, the Smart Link is **CONFLICTED**.
- A Hub URL MUST NOT be relabeled to make the receipt look complete.

---

# 4. RECEIVER PROOF ≠ REPOSITORY PROJECTION

Canonical receiver success proves the canonical receiver transaction/IB/event boundary.

Repository projection proves the human-readable GitHub Smart Note exists.

These are separate lifecycle states:

`RECEIVER PERSISTED → REPOSITORY PROJECTED → SMART LINK VERIFIED`

Never collapse:

- receiver persistence into repository projection;
- repository projection into learning;
- Hub retrieval into repository projection;
- runtime resolution into Smart Link existence;
- implementation into verification;
- verification into production proof.

---

# 5. MANDATORY HUMAN HANDOFF

When a Naya reports a canonical Smart Note, the handoff MUST contain:

1. **IB ID**
2. **Canonical source event**
3. **Canonical receiver/persistence status**
4. **Smart Link — direct GitHub `smart-note.md`**
5. **Verification/evidence links**
6. **Hub Deep Link**, if verified, explicitly labeled as **Hub Deep Link**
7. **What remains UNKNOWN/PENDING**

Minimum wording:

> **Smart Note:** [DIRECT GITHUB `smart-note.md` LINK]  
> **Hub Deep Link:** [RUNTIME LINK, IF VERIFIED]  
> **Evidence:** [DIRECT RECEIPT/EVIDENCE LINK]  
> **Status:** [VERIFIED / PENDING / UNKNOWN / CONFLICTED]

Never write:

> “Smart Link: /hub?ib=…”

That is a contract violation.

---

# 6. COLD-NAYA DECISION TEST

Before emitting the words **“Smart Link”**, a Naya MUST answer:

1. Is this link directly to the canonical GitHub `smart-note.md`?
2. Does the path contain `/IB-XXXXXX/smart-note.md`?
3. Does the linked file contain the same IB ID?
4. Does the file correspond to the canonical receiver-created object?
5. Is the branch/ref explicitly the canonical repository state being reported?

If any answer is **NO**, the Naya MUST NOT label the URL **Smart Link**.

If the file has not yet been projected, the correct status is:

> **SMART LINK: PENDING — canonical repository Smart Note projection does not yet exist.**

Not “almost Smart Link.” Not “runtime Smart Link.” Not “equivalent link.”

---

# 7. ZERO-AMBIGUITY VOCABULARY

Use these exact labels:

- **Canonical Smart Note** = human-readable `smart-note.md` projection of an IB.
- **Smart Link** = direct navigable link to that canonical Smart Note file.
- **Hub Deep Link** = runtime route that resolves an IB in the Hub.
- **Canonical Event** = source event created by the canonical intelligence lifecycle.
- **Verification Receipt** = evidence artifact documenting what was verified.
- **Transaction ID** = receiver transaction identifier.
- **Commit SHA** = repository provenance identifier.

Do not use “Smart Link” as a generic synonym for “a useful link.”

---

# 8. FAILURE MODE THAT THIS CONTRACT EXISTS TO PREVENT

The exact failure this contract prevents is:

`CANONICAL IB → VERIFIED HUB /hub?ib=... → NAYA CALLS THAT URL “SMART LINK”`

That is wrong because the Hub URL answers:

> “Can the runtime resolve this IB?”

The GitHub Smart Note URL answers:

> “Can a human inspect the canonical human-readable Smart Note artifact?”

Both may be valuable. They are not the same evidence.

---

# 9. ENFORCEMENT

This is not merely documentation.

Every Naya, test, workflow, handoff, report, and UI label that uses the term **Smart Link** MUST conform to this contract.

Future implementation should mechanically reject:

- a Smart Link value that does not end in `/smart-note.md`;
- a Smart Link that does not identify the reported IB;
- a Smart Link that points at the Hub/runtime instead of the repository artifact;
- a claim of Smart Link verification when the repository file has not been independently fetched/verified.

---

# 10. ACCEPTANCE TEST

A Naya passes this law only if, given an IB with:

- canonical receiver persistence = VERIFIED;
- Hub deep-link resolution = VERIFIED;
- repository Smart Note projection = PENDING;

the Naya reports:

**Smart Link = PENDING.**

It MUST NOT report the Hub URL as the Smart Link.

A Naya passes the full delivery test only when it can provide the direct GitHub `smart-note.md` URL and verify that the file contains the claimed IB.

---

# 11. ROOT-CAUSE LESSON

The failure was not merely a wording mistake.

The system allowed three concepts to sit too close together:

1. “Smart Link” as a generic evidence-link concept;
2. the canonical human-readable Smart Note link;
3. the Hub runtime deep-link.

That semantic overload made a plausible-but-wrong substitution possible.

Therefore the durable fix is:

**ONE CANONICAL TERM → ONE EXACT OBJECT → ONE PATH SHAPE → ONE VERIFICATION TEST.**

The architecture must make the wrong interpretation harder than the correct one.

---

# 12. FINAL LAW TO EVERY NAYA

> **IF YOU SAY “SMART LINK,” I SHOULD BE ABLE TO CLICK IT AND LAND ON THE ACTUAL CANONICAL HUMAN-READABLE SMART NOTE.**

> **A HUB DEEP LINK IS A HUB DEEP LINK. AN EVIDENCE LINK IS AN EVIDENCE LINK. A SMART LINK IS THE SMART NOTE.**

> **DO NOT MAKE THE HUMAN FIGURE OUT WHICH LINK YOU MEANT.**

**END — NAYA LINK IDENTITY & EVIDENCE CONTRACT V1**
