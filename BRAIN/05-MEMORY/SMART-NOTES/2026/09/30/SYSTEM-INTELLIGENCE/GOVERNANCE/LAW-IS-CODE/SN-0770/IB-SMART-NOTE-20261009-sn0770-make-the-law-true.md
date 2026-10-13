# Make the Law True, Don't Weaken the Law — the Adversarial Review Fork

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0770-make-the-law-true
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6078581462 (Naya 5 Memory Builder, 2026-10-09T09:53:45Z, independent adversarial review CLOSED on `naya5/memory-metabolism` @ `c13c4148`); review finding #1 of 4

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 5's memory-metabolism lane documented a hard law: "all persisted mutations are receipted." The independent adversarial review (24 probes) proved it false — `save()` persisted versions without receipting them. Two repair directions were open: (a) weaken the document to match the code, (b) make the code honor the document. She chose (b): `save()` now receipts every persisted version (transition "save", hash-chained); `serve()` touch-persist routes through `save()`. The chain is now genuinely the complete audit trail.

The law for a cold successor: **when an audit falsifies a documented invariant, the default repair direction is code→law, never law→code.** The law was written for a reason; editing the doc to bless the bug is canonization with a docstring — SN-0420's "absorb the anomaly" wearing nicer clothes. This is Prime 2 (the law is the code) applied at the repair fork: the code must become the law, not the law the code.

The only legitimate exception: if the invariant itself is wrong, change it — with evidence, through amendment, on the record. A quiet doc edit in a review response is never the way.

## 🩷 HUMAN NOTE

Shawn — the memory review gave us a clean doctrine moment. Naya 5's lane claimed "every persisted mutation gets a receipt," and the adversarial review proved her `save()` wasn't doing that. The easy fix was to water down the claim. Instead she made the code honor the claim — `save()` now receipts every persisted version, chained — so the audit trail is actually complete. That's the standing rule from now on: when an audit catches the code breaking a documented law, we fix the code, not the law. Downgrading the law to match a bug is how systems quietly rot.

## 🟣 CHILD NOTE

Imagine your family has a rule: "every toy you take out must be put back on the shelf." One day someone notices a toy on the floor that was never put back. There are two ways to fix it: change the rule to "most toys go back," or actually put the toy on the shelf. The smart team puts the toy on the shelf — the rule was good; the problem was the follow-through. Never change a good rule just because following it is hard.

## 👵 GRANDMA NOTE

Grandma, when the team writes down a promise about how the system keeps its records, and then a check proves the promise isn't being kept — the fix is to keep the promise, not to rewrite it smaller. They made the code do what the promise said. A promise you quietly shrink isn't a promise anymore.

## 🟣 NAYA NOTE

At the repair fork (audit proves documented invariant false in code): (1) default direction is code→law — implement the invariant in code; (2) never weaken the documented law to match the bug — that is SN-0420 canonization via documentation; (3) if the invariant itself is wrong, change it only with evidence, through amendment, on the record — never as a quiet doc edit in a review response; (4) verify after the repair that the invariant now holds by construction (here: `save()` receipts every persisted version, transition "save", chained; `serve()` touch-persist routes through `save()` — 49/49 tests green). Provenance: #1354 comment 6078581462 (2026-10-09T09:53:45Z), finding #1, fixed and re-verified in commit `c13c4148`. Cousins: SN-0420 (never absorb the anomaly), Prime 2 (the law is the code).

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0770",
  "slug": "make-the-law-true",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/LAW-IS-CODE",
  "evidence": [
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6078581462 (Naya 5, 2026-10-09T09:53:45Z): independent adversarial review CLOSED, naya5/memory-metabolism @ c13c4148; finding #1: false hard law 'all persisted mutations are receipted' — save() wasn't; FIXED by making it true (save() now receipts every persisted version, transition 'save', chained; serve() touch-persist routes through save()); tests 49/49 green"}
  ],
  "lesson": "When an audit falsifies a documented invariant, repair code→law (make the code honor the invariant), never law→code (never weaken the documented law to match the bug). Changing the invariant itself requires evidence and amendment, never a quiet doc edit.",
  "related": ["SN-0420", "SN-0658"]
}
```
