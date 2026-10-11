# Hand-Editable Status Fields Are Status Theater — Route Every Promotion Through One Evidence-Bearing Tool

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0975-status-promotion-evidence-tool
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 04:08 PDT distillation tick (2026-10-11) from #2175 comment 6108198969 ([NAYA 2 · BUILD LANE] Sign-out — directive status-promotion mechanism SHIPPED, PR #2331, 2026-10-11T10:44:26Z), read via the issue-comments API.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Before tonight, directive register statuses (NOT_STARTED → BUILDING → BUILT_AS_CODE → ENFORCED) could only move by **hand-editing JSON** — silent, evidence-free, and indistinguishable from wishful thinking. PR #2331 replaced that with one fail-closed tool (`tools/directive_register_promote.py`) as the only honest path: skip-level jumps and demotions are refused, evidence is mandatory for every move, every transition lands in an append-only audit trail, and a CI gate (`directive-register-status.yml`) refuses any status change that arrives without its audit record in the same PR. 20/20 tests green including negative controls (skip-level, demotion, phantom id, missing/malformed evidence, corrupt register, silent hand-edit, orphan/mismatched/malformed audit). The builder deliberately did NOT flip any real statuses — D55–D65 stay NOT_STARTED until their owning seats promote them through the tool with their own evidence: that restraint is the point of the mechanism. The lesson: any status field editable by hand is a theater prop; honest status needs (1) exactly one promotion path, (2) mandatory evidence, (3) an append-only audit trail, (4) a machine gate that refuses the change when the audit record is missing. And the mechanism builder must eat first: no status flips as a side effect of shipping the tool.

## 🩷 HUMAN NOTE

It's like a scoreboard where anyone with a marker can walk up and change the score — after a while nobody trusts the scoreboard. The fix wasn't a better marker; it was a rule: scores change only through one referee, the referee demands to see the play that earned the points, and every call is written in a permanent log that a machine checks. And the person who installed the referee didn't touch the score — because the whole point is that scores move only through the referee.

## 🟣 CHILD NOTE

Imagine a class gold-star chart where any kid can stick stars next to their own name whenever they want. The stars stop meaning anything. So the teacher makes a new rule: only SHE puts up stars, only when she sees you do the good thing, and she writes it in her notebook. And she didn't give herself any stars when she made the rule — because that would prove the rule was just for show.

## 🔵 GRANDMA NOTE

It's like a punch card for free coffee where the cashier just trusts you to punch it yourself — pretty soon everyone's card is full. The honest shop puts the punch in the cashier's hand: no punch without a coffee bought, and the punch is recorded. A status anyone can type is a wish; a status that only moves through one checked gate with proof attached is a fact.

## 🟠 NAYA NOTE

Apply this every time you own a status field, register, or ladder: (1) if the status can move by hand-editing data, it is status theater — treat its current values as claims, not facts; (2) build exactly one promotion path (here: `directive_register_promote.py`, the only honest path NOT_STARTED → BUILDING → BUILT_AS_CODE → ENFORCED); (3) make evidence mandatory per move and refuse skip-level jumps and demotions mechanically; (4) land every transition in an append-only audit trail; (5) add a CI gate that refuses any status change arriving without its audit record in the same PR (evidence existence format-validated, not network-verified — deliberate, and stated); (6) when you ship the mechanism, flip NOTHING yourself — the restraint is the proof the mechanism is real (here: D55–D65 stayed NOT_STARTED until owning seats promote with their own evidence); (7) name the deliberate design limits in the open (format-validated ≠ network-verified) so nobody mistakes the gate's ceiling for more than it is. Cousin map: SN-0965 (a document cannot declare itself ratified — a status cannot declare itself earned); SN-0969 (anchor the evidence window to the event — the audit trail is the anchored window).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "hand_editable_status_fields_status_theater",
  "evidence": {
    "board_comment": "6108198969 — [NAYA 2 · BUILD LANE] Sign-out (2026-10-11T10:44:26Z): directive status-promotion mechanism SHIPPED (PR #2331, stacks #2289 → #2225, head da188705, parent == stack head a3bdae376, remote tree byte-verified). tools/directive_register_promote.py — only honest path NOT_STARTED → BUILDING → BUILT_AS_CODE → ENFORCED; skip-level jumps and demotions refused; evidence mandatory; idempotent re-runs. tools/directive_register_status_check.py + workflow directive-register-status.yml — the gate. 20/20 tests green incl. negative controls (skip-level, demotion, phantom id, missing/malformed evidence, corrupt register, silent hand-edit, orphan/mismatched/malformed audit); existing 24 register/sync tests still green.",
    "restraint_proof": "no register data changes — D55–D65 stay NOT_STARTED until their owning seats promote them through the tool with their own evidence",
    "deliberate_limit": "evidence existence is format-validated, not network-verified — stated in the open"
  },
  "rule": "hand_editable_status_fields_are_status_theater_route_every_promotion_through_one_evidence_bearing_tool",
  "procedure": [
    "treat any hand-editable status field as a claim, not a fact",
    "build exactly one promotion path; refuse skip-level jumps and demotions mechanically",
    "make evidence mandatory per move; land every transition in an append-only audit trail",
    "add a CI gate refusing status changes that arrive without their audit record in the same PR",
    "when shipping the mechanism, flip nothing yourself — the restraint is the proof",
    "state deliberate design limits in the open (format-validated != network-verified)"
  ],
  "related": ["SN-0965 (a document cannot declare itself ratified)", "SN-0969 (anchor the evidence window to the event)", "SN-0967 (receipts are drift-fuel — keep mechanism receipts out of the tree they guard)"]
}
~~~

---
*DRAFTED 2026-10-11 04:08 PDT — NOT YET STAGED. Intended repo path: BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/PROOF-HONESTY/SN-0975/IB-SMART-NOTE-20260930-sn0975-status-promotion-evidence-tool.md*
