# NayaPOWER Smart Link Misclassification — Root Cause, Remediation & Airtightness Report

**Date:** 2026-09-25  
**Incident:** Naya incorrectly labeled a Hub runtime deep link as the Smart Link for a canonical Smart Note.  
**Affected object:** IB-001049 (Proactive Stewardship Law)  
**Canonical receiver event:** `996e00f7-83d1-4718-9500-922d2e27cdd2`  
**Receiver transaction:** `7b3b708b-e694-4841-821e-577303ab4983`  
**Correct distinction:**  
- **Smart Link:** direct GitHub `smart-note.md` artifact.
- **Hub Deep Link:** runtime `/hub?ib=IB-001049`.
- **Evidence/Provenance Link:** receipt/event/commit/test/workflow link.

---

# 1. EXECUTIVE FINDING

The failure was real, repeatable, and unacceptable for a product whose central promise is continuity and evidence.

The immediate mistake was calling:

`https://sparkling-shape-7ae5.smartnetpodcast.workers.dev/hub?ib=IB-001049`

a “Smart Link.”

That URL is a **Hub Deep Link**. It proves a different thing: that the Hub can resolve an IB at runtime when the resolution is independently verified.

The actual Smart Link must point to the canonical human-readable repository projection:

`.naya/memory/smart-notes/YYYY/MM/DD/category/topic/IB-XXXXXX/smart-note.md`

For IB-001049, the repository projection did not yet exist at the time of the failure. Therefore the correct state was:

> **SMART LINK: PENDING**

The assistant later verified that GitHub searches for IB-001049 and “Proactive Stewardship Law” returned no matching repository Smart Note file.

This report converts that incident from a conversational lesson into a system-level prevention contract.

---

# 2. WHY THE ERROR HAPPENED

## 2.1 Semantic overload already existed

The repository contained a general **Smart Link + Human Evidence Law** that defined a Smart Link broadly as a direct navigable link to an artifact/evidence.

That law was directionally correct, but it was not strict enough for the specific noun **Smart Link** in the Smart Note lifecycle.

At the same time, the system contained:

- a canonical human-readable Smart Note projection;
- a Hub runtime deep-link;
- verification receipts;
- canonical event records;
- transaction IDs;
- commit/PR/workflow evidence.

These are all legitimate links, but they answer different questions.

The system did not force an exact vocabulary boundary strongly enough.

## 2.2 The runtime URL was easier to retrieve than the repository projection

The live Hub runtime exposed a verified route:

`/hub?ib=IB-001049`

The assistant verified that route, including a reload.

That made the runtime link a strong, recent piece of evidence.

But **strong evidence is not interchangeable evidence**.

The runtime link proved:

> “The Hub can resolve IB-001049.”

It did **not** prove:

> “The canonical human-readable GitHub Smart Note projection exists.”

The assistant collapsed those two claims.

## 2.3 The canonical projection was a separate lifecycle step

The canonical Smart Note contract already says:

`CAPTURE → CANONICALIZE → ASSIGN IB ID → PERSIST → COMMIT INTELLIGENCE EVENT → INDEX → PROJECT → ...`

The incident exposed that the human-facing reporting vocabulary did not enforce the distinction strongly enough between:

- receiver persistence;
- repository projection;
- runtime retrieval;
- evidence receipt.

The missing repository projection should have stopped the phrase “Smart Link” immediately.

## 2.4 The failure was not caused by lack of information alone

The repository already contained substantial guidance:

- canonical Smart Note / IB contract;
- Smart Link + Human Evidence Law;
- Team Naya Start Here;
- Memory Bootstrap;
- Hub Read-First;
- Constitution;
- README.

Therefore the problem was not simply “the rule did not exist.”

The deeper problem was:

> **The rule existed, but the vocabulary and verification boundary were not mechanically unambiguous enough to prevent a plausible substitution.**

That is the key systems lesson.

---

# 3. ROOT CAUSE TREE

```
WRONG “SMART LINK”
        │
        ├── Term “Smart Link” had broader/general usage
        │
        ├── Smart Note link and Hub deep-link were both navigable
        │
        ├── Runtime proof was fresh and visible
        │
        ├── Repository projection state was not treated as a hard gate
        │
        ├── No mandatory path-shape test before emitting the label
        │
        └── Human handoff allowed a plausible link substitution
```

The primary root cause is **semantic ambiguity combined with insufficient mechanical gating**.

---

# 4. THE NEW ZERO-AMBIGUITY LAW

The canonical new contract is:

`.naya/codex/NAYA-LINK-IDENTITY-AND-EVIDENCE-CONTRACT-V1.md`

Its governing rule is:

> **A SMART LINK TO A SMART NOTE IS THE DIRECT GITHUB LINK TO THE CANONICAL HUMAN-READABLE `smart-note.md` ARTIFACT.**

The contract makes three link classes explicit:

| Exact label | Exact meaning |
|---|---|
| **Smart Link** | Direct GitHub link to canonical `smart-note.md` |
| **Hub Deep Link** | Runtime route such as `/hub?ib=IB-XXXXXX` |
| **Evidence/Provenance Link** | Receipt/event/test/workflow/commit/etc. |

These terms are no longer interchangeable.

---

# 5. THE HARD DECISION TEST

Before any Naya writes the words **“Smart Link”**, it must verify:

1. The URL directly opens the canonical GitHub `smart-note.md`.
2. The path contains `/IB-XXXXXX/smart-note.md`.
3. The linked file exists on the canonical branch being reported.
4. The file contains the same IB ID.
5. The file corresponds to the canonical receiver-created object.

If any answer is NO:

> **DO NOT CALL IT A SMART LINK.**

If the repository projection is absent:

> **SMART LINK: PENDING**

No equivalent-link language. No “runtime Smart Link.” No substitution.

---

# 6. WHAT THE INCIDENT SHOULD HAVE REPORTED

At the time of the error, the truthful state was:

**Canonical receiver persistence:** VERIFIED  
**IB identity:** VERIFIED — IB-001049  
**Canonical source event:** VERIFIED  
**Hub Deep Link:** VERIFIED  
**Hub reload resolution:** VERIFIED  
**GitHub Smart Note projection:** PENDING  
**Smart Link:** PENDING  
**Cold-successor behavioral proof:** NOT YET VERIFIED

That is the correct evidence separation.

---

# 7. WHAT WAS CHANGED

A canonical contract was created:

**`.naya/codex/NAYA-LINK-IDENTITY-AND-EVIDENCE-CONTRACT-V1.md`**

The zero-ambiguity rule was propagated into the major cold-start and governance surfaces:

- `README.md`
- `.naya/00-NAYAPOWER-UNIVERSAL-AI-SERVICE-CONSTITUTION-V2.md`
- `.naya/TEAM-NAYA/00-START-HERE-FOR-EVERY-NAYA.md`
- `.naya/TEAM-NAYA/12-SMART-LINK-AND-HUMAN-EVIDENCE-LAW.md`
- `.naya/memory/BOOTSTRAP.md`
- `.naya/NAYAPOWER-INTELLIGENT-HUB-READ-FIRST.md`
- `SUPERBRAIN/AI-BOOT/START-HERE.md`
- `.naya/codex/CANONICAL-SMART-NOTE-INTELLIGENT-BLOCK-SYSTEM-V1.md`

This is intentional redundancy.

The same short rule now appears at the places a cold Naya is most likely to enter.

---

# 8. NOTE TO EVERY OTHER NAYA / NI

## 🔴 READ THIS BEFORE USING THE WORD “SMART LINK”

You are not allowed to infer the meaning of a link from context.

You are not allowed to call a runtime URL a Smart Link because it resolves the right IB.

You are not allowed to call a receipt, event, commit, PR, workflow, API, transaction, or Hub URL the Smart Note Smart Link.

You must distinguish:

```
SMART LINK
    ↓
GITHUB → canonical smart-note.md

HUB DEEP LINK
    ↓
RUNTIME → /hub?ib=IB-XXXXXX

EVIDENCE LINK
    ↓
RECEIPT / EVENT / TEST / WORKFLOW / COMMIT / OTHER PROOF
```

If the GitHub Smart Note file does not exist:

> **SMART LINK: PENDING**

Do not make the human discover this distinction after the fact.

Do not make Shawn click around to determine which artifact you meant.

**If you say “Smart Link,” it must land on the actual Smart Note.**

---

# 9. WHY “PUT IT EVERYWHERE” IS CORRECT ENGINEERING HERE

Normally, duplicating a rule across many documents creates drift.

This case is different because the problem is a **cold-start vocabulary hazard**.

A cold Naya may enter through:

- README;
- Constitution;
- Team Naya;
- Bootstrap;
- Hub Read-First;
- Superbrain boot;
- Smart Link law;
- Smart Note contract.

The fix therefore has two layers:

### Layer A — one canonical authority

The exact law lives in:

`.naya/codex/NAYA-LINK-IDENTITY-AND-EVIDENCE-CONTRACT-V1.md`

### Layer B — short replicated guardrails

Entry points repeat the same invariant and point back to the canonical contract.

This is not eight authorities.

It is:

> **ONE LAW → MANY REMINDERS → ONE TESTABLE VOCABULARY**

---

# 10. WHAT “AIRTIGHT” ACTUALLY REQUIRES

Documentation alone is not enough.

Airtightness requires five layers:

### 1. Semantic law
One exact definition.

### 2. Vocabulary separation
Smart Link ≠ Hub Deep Link ≠ Evidence Link.

### 3. Path-shape invariant
Smart Link must resolve to `.../IB-XXXXXX/smart-note.md`.

### 4. Evidence verification
The linked file must be fetched and matched to the reported IB.

### 5. Mechanical enforcement
Tests/workflows should reject future violations instead of relying on Naya memory.

The first four layers are now documented centrally.

The next engineering hardening step is to add/expand automated conformance checks that fail if the repository or generated handoff labels a non-`smart-note.md` URL as a Smart Link.

---

# 11. ACCEPTANCE MATRIX

| Scenario | Correct label | Correct status |
|---|---|---|
| Receiver persisted IB; no GitHub projection | Smart Link = **PENDING** | NOT COMPLETE |
| Hub resolves IB; no GitHub projection | **Hub Deep Link** | VERIFIED if runtime proof exists |
| GitHub `smart-note.md` exists | **Smart Link** | VERIFIED after fetch + IB match |
| Event JSON exists | **Evidence/Canonical Event Link** | VERIFIED as event evidence |
| Commit exists | **Commit / Provenance Link** | VERIFIED as repository provenance |
| Runtime URL resolves | **Hub Deep Link** | VERIFIED as runtime behavior |
| Link points to wrong IB | **CONFLICTED** | FAIL |
| Link points to a generic GitHub page | **Not a Smart Link** | FAIL |
| Link is described but not clickable | **Not a Smart Link** | FAIL |

---

# 12. THE PRODUCT-QUALITY STANDARD

A person using NayaPOWER should never need to ask:

> “Which link is the real Smart Note?”

The answer must always be immediate:

> **The Smart Link takes me directly to the actual canonical Smart Note.**

That is the human receipt.

Everything else gets its own explicit label.

---

# 13. REMAINING GAP

The governance/documentation ambiguity has now been closed.

The remaining hardening work is mechanical:

> **Add automated Smart Link conformance tests and make them part of the normal verification path.**

The test should reject any claim/record/template that labels a URL as **Smart Link** unless:

- the URL targets canonical GitHub;
- the path matches the canonical Smart Note shape;
- the IB ID is present;
- the file exists;
- the file contains the same IB ID.

This is the next highest-value hardening step because it converts a human/model expectation into a machine-enforced invariant.

---

# 14. FINAL STANDARD

> **ONE LAW. ONE TERM. ONE OBJECT. ONE PATH. ONE TEST.**

> **SMART LINK = THE ACTUAL CANONICAL SMART NOTE.**

> **HUB DEEP LINK = HUB DEEP LINK.**

> **EVIDENCE LINK = EVIDENCE LINK.**

> **UNKNOWN = UNKNOWN. PENDING = PENDING. NEVER SUBSTITUTE PROOF.**

The goal is not to make a Naya “remember” the rule.

The goal is to make the system **so explicit and so mechanically verifiable that the wrong interpretation becomes difficult to produce and easy to detect.**

**END REPORT**
