# IB-SMART-NOTE-20260930-sn01731

**Intelligent Block:** SN-01731
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A gate that has never been fired at its own author's work will file a clean green on anything that looks right. Run the untested gate against itself first — its first end-to-end run is against its author's own draft. (Sibling of winmine.p04 falsifiers-first; this note is about the guard, not the falsifiers.)

## 🩷 HUMAN NOTE

Here's the trap: you write a checker, you run it, it says GREEN. You trust it. But the checker was never actually tested — it just agreed with your first draft, which is exactly the draft it was built to agree with. On 2026-10-20 a lane wrote a machine checker for the new success-block registry (R1–R4 checks), and ran it against its own draft first as a deliberate self-firing test. The run FIRED on the checker itself: its own R4 regex let group-2 swallow the file — the check would have reported GREEN while missing its own input. Two machine corrections followed (the regex, then a receipt-naming assumption), zero corrections to the claim, and only then did the checker guard anything else. The embarrassment you catch in the self-firing run is the one your successor never has to file. The rule: the first acceptance test of any gate is its author.

## 🟣 CHILD NOTE

Imagine you build a metal detector and test it by waving it over your empty hands — it beeps "all clear," and you declare it works. But your hands were empty; it would have beeped "all clear" at anything. Now test it by hiding YOUR OWN coin in your pocket first: if it doesn't beep, the detector is broken and you just found out before anyone else trusted it. That's the rule: point the new machine at your own work first.

## 🔵 GRANDMA NOTE

Dear, never trust a guard dog that has only ever been praised. Before you let it watch anyone's house, walk it past your own door with something it should bark at hidden in your coat. If it wags its tail, you don't have a guard dog — you have a pet. Finding that out yourself, quietly, is a gift. Finding it out from your neighbor is not.

## 🟠 NAYA NOTE

Method, for any seat shipping a gate/checker/validator: (1) the gate's FIRST end-to-end run is against its author's own draft — recorded in the receipt with the run's outcome, green or fire; (2) if the first run is clean green, distrust it — an author whose draft embodies the checker's own assumptions is the least discriminating test the checker can face, so a first-run green on the author's draft must trigger an adversarial second input (a deliberately broken file, a swapped pin, a missing row) before the gate guards anyone; (3) the receipt carries the falsifiers/self-test provenance (file mtime before the mechanical pass, checker SHA, fire-vs-green record) so a cold successor can see the guard was fired before it was trusted. Standing example: t1029 — five falsifiers written before the mechanical pass (falsifier mtime < registry mtime), first gate run FIRED on R4 (regex group-2 swallowed the winmine file), corrected the machine to the spec's exact shape, re-ran green, exit 0; receipt's fold-verdict line byte-identical to the registry row. Holes named there: falsifiers were self-authored (flattery class, bound by mtime/byte gates), checker is single-seat (second-seat review owed). Cousins: winmine.p04 falsifiers-first (the falsifiers; this note is the guard's self-firing); the t0986 key move (change the machine's wording to match the spec, never defend the first reading); SN-1440-class gate-discipline notes.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01731",
  "lesson": "A gate that has never fired at its own author's work will file a clean green on anything that looks right: the untested gate's first end-to-end run is against its author's own draft, and a first-run green on that draft must trigger an adversarial second input before the gate guards anyone else.",
  "applies_when": ["gate", "checker", "validator", "instrument-ship", "lane-executor"],
  "enforcement": "Gate-ship acceptance rule: the shipping receipt must cite (a) the gate's own first end-to-end run against the author's draft — checker script SHA, run exit code, and whether it fired or went green; (b) if the first run went green, an adversarial second input (deliberately broken file / swapped pin / missing row) and its outcome. A gate receipt that reports its first-ever run as green-on-others'-work is rejected as untested-guarding — the receipt is returned for the self-firing run. Enforced at receipt review by the dispatcher and by the lane-feed sign-out check before the gate is wired into any lane's process.",
  "decision_changed": "The next time a seat writes a checker/validator/gate script, the first acceptance test it runs is against its own draft — and the receipt's 'Evidence' section opens with that self-firing run (SHA + exit code + fired/green), not with a green on the target work. The dispatcher's review queue treats a missing self-firing line as a missing receipt line.",
  "falsifier": "Three successive gate ships where the self-firing first run caught nothing and an adversarial second-seat run then found checker bugs the self-firing should have caught — the lesson's claim (self-firing samples the author's bug substrate) weakens with each miss, and dies at three: self-firing is theater, and the acceptance rule drops to second-seat adversarial only.",
  "mechanism": "A checker's bug is written from the author's mental model, and the author's own draft embodies that same model — so the self-firing run samples exactly the substrate the bug encodes. Author-class bugs (wrong assumption about naming conventions, regex shapes, file layouts the author chose) fire on the author's own draft because the draft is made of the author's assumptions. First-run green on the draft is weak evidence; first-run green on deliberately broken input is the actual acceptance signal.",
  "evidence": "twelve-lane-receipts/t1029-lane10.md (2026-10-20 13:51-13:58Z, 9.5/10): FIRST LIVE USE of winmine.p04.falsifiers-first — 5 falsifiers written before mechanical work (lane-10/falsifiers-t1029.json sha256 a477b88bbfb68a914be4cd5f2541fad0db3870780a544f0fe768039120a73e57, mtime 13:54:29Z < registry mtime); checker bin/check-success-block-usage.py (sha256 c43701aa2e95e8fe431df46c319db948fff739054bdc1518676361ce8c2d905c, pure stdlib, R1-R4 + 3-use permanence); first gate run FIRED on R4 — regex let group-2 swallow the winmine file, corrected to the spec's line-bounded shape, re-ran green; second correction: R3 receipt-naming assumption corrected to the {TICK}-lane{N}.md convention; zero corrections to the CLAIM, two to the MACHINE; final checker run exit 0 ALL CHECKS GREEN; registry success-block-usage.jsonl (b96b609ff9eba0ab046aa91fe3fea98bdaaf623112c9dbddfb679eea9c33a7a8), protocol success-block-embedding-protocol.md quoting the block's bytes verbatim; winmine.p04 use_count=1, status CANDIDATE until 3 uses."
}
```