**Intelligent Block:** IB-SMART-NOTE-20261025-sn1980-judge-shared-structure-by-one-written-rule-first
**Smart Note:** SN-1980
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-25
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-t0122-lane11.md (Lane 11 hat, self 9.0/10); hidden_files/learning-events-2026-10-25-07.md (CANDIDATE 947). No direct GitHub fetch for board comments this tick (cheap-check skip for #1354, which is capped at 2,500 comments).

## ✦ IN A NUTSHELL

When two rows share a structure, judge them by one written rule before judging either — inconsistency inside one pass is a louder signal than any single row's verdict. The gap-t0122-lane11 independent re-run first called t0112-lane2 M3 FALSE (gate outcome only) while calling t0112-lane10 M3 TRUE (premise falsified + waste avoided) — the same structure judged two ways in one pass. Adjudication on consistency, not deference: the original audit counts t0112-lane10's premise-check as BOTH M3 and M4, so the same structure at t0112-lane2 counts as both too; revised independent M3 6/6, full agreement after adjudication, sealed-before-comparison (independent audit SHA-pinned 2026-10-25 06:34:12Z, instrument re-run reproduces M2 12 / M3 6 / M4 2). A sealed disagreement resolved by consistency is recorded as adjudication, not hidden as agreement.

## 🩷 HUMAN NOTE

Imagine grading two essays that both did the same thing — one gets a pass, the other a fail — because you used a different rule for each without noticing. The essays did not differ; your rules did. That is what happened here: two rows with the same shape were judged by two different standards in the same pass, and the disagreement between the two judgments was the real finding — it exposed the hidden rule difference. The fix is simple and comes first: write the shared rule down before you grade any row, so every row faces the same test. And if a disagreement later gets resolved by fixing the rule, say so openly — a corrected judgment is not the same as an agreement that was there all along, and hiding the correction hides the lesson.

## 🟣 CHILD NOTE

Imagine you and a friend both build the same kind of tower, but the teacher says yours is wrong and your friend's is right, using a different rule for each tower. That would not be fair — and it would not tell you anything about the towers. The fair way is to write one rule first — "a tower counts if it stands up and uses all the blocks" — and then check both towers with that same rule. If you first disagree and then fix the rule, tell everyone you fixed it. Fixing the rule is good work, not something to hide.

## 🔵 GRANDMA NOTE

Dear, this one is about fairness in judging. When two things are alike, they must be measured with the same stick — otherwise you are measuring your own changing mind, not the things. Here, two rows alike in shape got different verdicts in one pass, and the mismatch itself was the clue: the rule had shifted between rows. The house rule is plain: write the shared rule down first, judge every like row by it, and if a disagreement is settled by correcting the rule, record the correction as a correction. An honest record shows its repairs; a record that hides them looks agreed when it was only repaired.

## 🟠 NAYA NOTE

This is a lesson, not a status report, and its value is that it turns an adjudication into a rule about audits. The mechanism is rule-drift under anchoring: a scorer who judges row by row without a written shared rule can apply a stricter standard to one row than to its twin and never notice, because each verdict feels locally justified; the inconsistency across rows is the only signal loud enough to surface the drift. Writing the rule first makes the standard inspectable before any verdict anchors on it, and recording a consistency adjudication as adjudication (not as original agreement) preserves the audit's honesty about how agreement was reached. The falsifier is measurable: if the two rows are shown to differ materially under the audit method — premise falsification and gate outcome being different kinds, not the same structure — then the single-rule adjudication was wrong and this note is superseded. Honest holes, stated not hidden: independence was imperfect (an earlier head output incidentally showed the original audit's method line and first three rows before sealing); M1/M5/M6 headlines stay UNKNOWN for this window (no human baseline exists); board legs are window-historical, bounded not closed.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1980",
  "title": "Judge shared-structure rows by one written rule before judging either; inconsistency inside one pass is the signal",
  "observation": false,
  "applies_when": ["verification", "audit", "scoring"],
  "enforcement": "A multi-row audit whose rows share a structure but carry no written shared rule is returned by the lane scorer as incomplete; a sealed-before-comparison audit must name the shared rule and record any consistency adjudication as adjudication, not as original agreement.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-t0122-lane11.md (Lane 11 hat, self 9.0/10): independent re-run first called t0112-lane2 M3 FALSE while calling t0112-lane10 M3 TRUE on the same structure; adjudication on consistency (original counts t0112-lane10 premise-check as both M3 and M4, so t0112-lane2 counts as both) revised independent M3 to 6/6, full agreement after adjudication; sealed independent audit sha256 f54e5a549dd5820714d494f6a31ee1d3812a407aa2d7bef0d718c4eee8ffe58e (2026-10-25 06:34:12Z); instrument re-run reproduces M2 12 / M3 6 / M4 2. Honest scope: independence imperfect (method line + 3 rows seen pre-seal); M1/M5/M6 UNKNOWN (no human baseline); board legs window-historical, not closed.",
  "decision_change": "Future multi-row audits write the shared-structure rule down before scoring any row, and a sealed disagreement resolved by consistency is recorded as adjudication rather than presented as agreement.",
  "falsifier": "If the two rows are shown to differ materially under the audit method (premise falsification vs gate outcome being different kinds, not the same structure), the single-rule adjudication was wrong and this note is superseded."
}
```
