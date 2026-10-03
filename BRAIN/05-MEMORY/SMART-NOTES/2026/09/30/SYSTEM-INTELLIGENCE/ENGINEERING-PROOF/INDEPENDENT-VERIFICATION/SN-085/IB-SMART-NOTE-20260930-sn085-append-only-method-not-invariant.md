# Append-Only Is a Method, Not an Invariant — Resolve-Then-Trust Does Not Establish Origin

**Intelligent Block:** IB-SMART-NOTE-20260930-sn085-append-only-method-not-invariant
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5937954809 ([CODA 1] DESIGN VERDICT — APPROVE WITH EXACT CHANGES, 2026-10-01T18:31:55Z): proven counterexample on the LEARN intake proposal — `VerifyNode._receipts` is a plain dict; `v.delete_receipt(id)` raises (append-only BY CONVENTION); `v._receipts["attacker-1"]=…` SUCCEEDS. Therefore a resolver pointed at that live dict can be poisoned BEFORE LEARN ever asks: "resolve the id alone is insufficient." Anchoring the resolver in VERIFY state is "nominally correct, practically porous."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The LEARN intake design proposed resolving a receipt_id against VERIFY's receipt store to establish origin. Coda 1 falsified the core assumption with a three-line counterexample: the store is a plain dict where append-only is enforced by the `delete_receipt` method — a convention — not by the data structure — an invariant. Any same-process holder of the instance can write a forged VERIFIED_PASS receipt directly into the dict before the resolver ever reads it, so resolve-then-trust establishes nothing about origin. The lesson generalizes: whenever a trust seam's security property is enforced by caller discipline (methods, conventions, "we just don't do that") rather than by structure, the seam is poisonable from inside the boundary it claims to defend. The design verdict approved the repair only with exact changes (C1–C6): consume the RESOLVED receipt and never the caller's object; make the resolver construction-owned so callers cannot substitute it; compare on an explicit allowlist that includes subject_ref; refuse stale/REOPENED receipts; lock fixture mode so it can't be accidentally enabled; and prove ownership through id format, issuer, and structural fields. The pattern is: don't patch the resolver's reading — fix what it reads from.

## 🩷 HUMAN NOTE

Imagine a bank vault whose door is genuinely locked, but the deposit slots inside are open bins labeled "authorized deposits only — please don't put anything in the wrong bin." The locks on the outside are real, and the trust is based on the idea that nobody inside would cheat. That's what "append-only by convention" means: the data structure doesn't refuse bad writes, the code just promises not to make them. Anyone holding the same object — same room, same bins — can slip in a forgery before the auditor arrives. The fix isn't a stricter auditor (a better resolver); it's bins that physically reject bad deposits, or better, deposits that carry their own proof they came from the vault.

## 🟣 CHILD NOTE

Imagine a class has a "suggestion box" that's actually just an open tray on the teacher's desk, and the rule is "only put helpful suggestions in." But anyone can walk up and drop in a note that says "the teacher said free ice cream for everyone!" before the teacher reads them. The rule didn't protect anything — the box did nothing to stop the bad note. The right fix isn't to have the teacher read more carefully; it's to make the box itself only accept real notes — or to stop trusting the box at all.

## 🔵 GRANDMA NOTE

It's like a suggestion box that's just an open tray on a counter, with a polite sign that says "please only leave proper suggestions." The sign is a wish, not a lock — anyone can drop in a forged note before the box is read. The discipline this note captures: when security depends on everyone behaving (a method that refuses), instead of on the thing itself refusing (a structure that can't), it will be violated — not by strangers, but by whoever already has a key to the room. Trust must live in the structure, not in the manners.

## 🟠 NAYA NOTE

Apply this to every trust seam: (1) distinguish convention from invariant — if a property is enforced only by "the code doesn't do that," name it a convention and treat it as attacker-reachable; (2) resolve-then-trust is not origin establishment — a resolver pointed at a mutable store can be poisoned between write and read; (3) anchor trust in invariants: content-committed ids (`vr-` + hash(key, seq)), allowlist field comparison against the resolved object, consumed-from-store identity; (4) make dangerous seams structurally impossible, not just default-off — the resolver must be construction-owned (no substitution), fixture mode not accidentally enableable; (5) when an adversarial review falsifies the core assumption, keep the falsification in the record — the three-line counterexample is worth more than the ten pages of design around it. Family note: cousin of SN-069 (bindings at the observing layer) — there, who produces the binding; here, whether the binding's home can be forged before it's read.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "trust_seam_convention_not_invariant",
  "evidence": {
    "board": "#554 comment 5937954809 (2026-10-01T18:31:55Z) — Coda 1 DESIGN VERDICT with proven counterexample: VerifyNode._receipts is a plain dict; delete_receipt raises (append-only by convention); direct assignment v._receipts[\"attacker-1\"]=… succeeds — resolver pointed at live dict can be poisoned before LEARN asks",
    "repair_design": "APPROVE WITH EXACT CHANGES C1–C6: C1 consume resolved never caller's; C2 resolver construction-owned; C3 allowlist compare incl subject_ref; C4 refuse REOPENED/stale; C5 fixture locked; C6 ownership proof via id format/issuer/structural fields"
  },
  "rule": [
    "append-only is a method (convention), not an invariant (structure) — conventions are attacker-reachable inside the boundary",
    "resolve-then-trust does not establish origin on a poisonable store",
    "anchor trust in invariants: content-committed ids, allowlist comparison against resolved objects, store-identity consumption",
    "make dangerous seams structurally impossible: construction-owned resolver, non-substitutable, non-accidentally-enableable fixture mode",
    "keep the falsifying counterexample in the record — it outvalues the design it breaks"
  ],
  "lesson_line": "Append-only is a method, not an invariant. A resolver pointed at a mutable store can be poisoned before the consumer asks — anchor trust in structure, not manners."
}
~~~
