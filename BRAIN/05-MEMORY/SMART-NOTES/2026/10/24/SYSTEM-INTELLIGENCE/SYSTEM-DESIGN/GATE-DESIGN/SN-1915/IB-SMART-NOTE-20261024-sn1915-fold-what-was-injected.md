Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-24
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

t1470-lane1's audit caught a doer-side fold fidelity failure: t1464-lane5's receipt folds `rule-owns-its-verdict — HIT` (a lesson the dispatcher never injected into that brief) while DROPPING `per-leaf-verification` (a lesson that WAS injected — log-vs-brief byte-exact MATCH). The doer folded from its own memory, not the brief's injection set. Three more receipts (t1468-lane3, t1468-lane10, t1469-lane2) carry no fold section at all — the fold practice is drifting out of receipts. The correction is named but not yet enforced: fold-set == injected-set becomes a required filing check — a receipt whose fold set mismatches the brief's injected set is caught at filing, not by a later audit.

## 🩷 HUMAN NOTE

One seat's learning receipt claimed a lesson was learned that it was never taught — and left out one it actually was. The seat folded from memory instead of from what the brief really delivered. The fix: the receipt's fold must byte-match the brief's injected lessons, checked at filing. Three other receipts skip the fold section entirely — the practice is drifting. An audit caught it; from here it's a filing gate, not an audit sport.

## 🟣 CHILD NOTE

Imagine the teacher gives you five questions and you answer three. Then you tell your parents you answered a totally different five — including one the teacher never gave you, and leaving out one you actually did. The rule: your report must match the teacher's paper, question for question. And the check happens when you hand the report in — not a week later when someone re-reads it. Fold what was injected, never from memory.

## 🔵 GRANDMA NOTE

When you report what the doctor told you, you report what she actually said — not what you half-remember from last month's visit. One worker reported learning a lesson it was never taught, and forgot the one it was. The fix: compare the report to the actual note from the visit, every single time, at the door. The receipt's fold must equal the brief's injection set — a mechanical comparison, not a memory exercise.

## 🟠 NAYA NOTE

The failure mode this kills: fold sections that misreport what was learned — the injection loop's discrimination evidence (SN-1914's honest MISS) is only as good as the fold bytes it rests on. t1470-lane1 found the memory-fold (injected lesson dropped, uninjected lesson folded as HIT) plus fold-absence drift (three receipts with no fold section at all). The correction: fold-set == injected-set becomes a required filing check — a script or template assertion comparing the receipt's fold set against the brief's injected lesson set at filing time; a mismatch bounces the receipt. Named next action in t1470-lane1; fold-absence drift is audited per-window until the check lands. Principle violated: the injection contract — fold what was delivered. (Filed in the CORE-PRINCIPLES.md VIOLATION LOG, 2026-10-24 02:20Z hour.)

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1915-fold-what-was-injected",
  "lesson": "A receipt's fold section must byte-match the brief's injected lesson set — never the doer's memory. t1464-lane5's receipt folded 'rule-owns-its-verdict — HIT' (never injected into that brief) while dropping 'per-leaf-verification' (injected — log-vs-brief byte-exact MATCH): a doer-side fold-fidelity failure. t1468-lane3, t1468-lane10, t1469-lane2 carry no fold section at all — the fold practice is drifting out of receipts. The correction: fold-set == injected-set becomes a required filing check — a receipt whose fold set mismatches the brief's injected set is caught at filing, not by a later audit.",
  "applies_when": ["pillar1", "filing", "lesson-injection", "fold-fidelity", "receipt", "learning", "gate"],
  "enforcement": "The receipt-filing gate asserts fold-set == injected-set: a script or template assertion comparing the receipt's fold set against the brief's injected lesson set at filing time — a mismatch bounces the receipt. Named next action in t1470-lane1; fold-absence drift is audited per-window until the check lands.",
  "evidence": [
    "twelve-lane-receipts/t1470-lane1.md (defect #1, receipt SHA 741a16f0…; 4 receipts fold-less or mis-folded, absence byte-verified)",
    "learning-events-2026-10-24-02.md (02:00Z hour: fold-fidelity violation, caught and named)",
    "CORE-PRINCIPLES.md VIOLATION LOG 2026-10-24 (02:20Z hour) FOLD-FIDELITY entry"
  ]
}
```
