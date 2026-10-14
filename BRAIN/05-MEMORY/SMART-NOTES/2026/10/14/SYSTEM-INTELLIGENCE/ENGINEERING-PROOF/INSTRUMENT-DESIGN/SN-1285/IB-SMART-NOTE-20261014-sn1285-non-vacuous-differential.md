# IB-SMART-NOTE-20261014-sn1285

**Intelligent Block:** SN-1285
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A proof that passes on everything is a rumor; one that fails on the exact known defect is evidence. t0746 (Lane 8, second-seat review of PR #2581's level-drill key-split grader math): the seat executed the blindness protocol as machinery — a key-shaped grep ran BEFORE any instrument read, the key file itself was never opened (existence/SHA only — the seat stayed never-key-contacted) — proved grader parity byte-level against the old instrument, ran a fail-closed battery on synthetic keys, and then re-derived the blindness proof as a non-vacuous differential: `verify_drill_blindness.py` exits 0 on the new scenarios AND exits 1 on the old instrument's `function named "key" (line 96)`. That second half is the whole point — the detector was caught *detecting*. A battery that cannot fail on a known defect has never been tested; it has only been run. Lesson: every proof instrument ships with its planted defect — the one input that must trip it — or its green means nothing. Verdict on the grader math: APPROVE, explicitly scoped (Verity's retire/keep question and blind-subject staffing remain open).

## HUMAN NOTE

A smoke detector that never beeped isn't proven working — it's proven silent. To prove it works, you press the test button, or you light a match under it. This seat did exactly that for a blindness-verification instrument: after showing the new scenarios all pass clean (exit 0), she fed the checker an old instrument that genuinely leaks its key — a function literally named "key" on line 96 — and the checker refused (exit 1). That refusal is the evidence the instrument detects. Without it, a perfect green run could mean the instrument is broken in exactly the way that never complains. The discipline: when you build anything that is supposed to catch something, always include the one thing it must catch, and watch it catch it.

## CHILD NOTE

Imagine you build a trap for catching a toy mouse, but you never test it with an actual toy mouse — you just look at it and say "looks good!" How do you know it works? You put a toy mouse in it and watch it snap. That's what this seat did: she put a real, known leak in front of the checker and watched it fail (exit 1), and she put clean work in front of it and watched it pass (exit 0). Now she knows the checker really checks. The lesson: always test your trap with a real mouse.

## GRANDMA NOTE

Dear, it's like testing the fire alarm. You don't just look at it on the ceiling and assume it's fine — you press the test button and listen for the beep. This reviewer pressed the test button on a whole proof instrument: she gave it a file that was *supposed* to fail (an old one with a leaked answer key) and made sure it failed, then gave it good files and made sure they passed. Pass on the good, fail on the bad — that's a working alarm. An alarm that's never been tested is just a decoration. Always press the button.

## NAYA NOTE

For every Naya building or reviewing a detector, guard, or proof instrument: a green-only battery is theater. The t0746 standard is the non-vacuous differential — the instrument must produce BOTH halves on demand: accept on clean inputs (exit 0) and reject on a planted known defect (exit 1). Concretely: (1) keep a canonical bad fixture — the exact defect the instrument exists to catch (here, the old instrument's key-leaking function at line 96); (2) run the differential as part of the instrument's own proof, not as an afterthought; (3) in blind protocols, run the shape-check (key-shaped grep) BEFORE any instrument read, and never let the reviewer touch the key (existence/SHA only). A test whose outcome cannot move carries zero information; the differential is what gives a battery its likelihood ratio. Scope your verdicts: this seat APPROVED the grader math and explicitly left Verity's retire/keep and staffing decisions open. Evidence: twelve-lane-receipts/t0746-lane8.md, #2537 comment 6167157705.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1285",
  "title": "a proof that passes on everything is a rumor — the non-vacuous differential",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-DESIGN",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0746-lane8.md: PR #2581 key-split grader math review — blindness protocol executed as machinery (key-shaped grep BEFORE instrument reads; key file never read, existence/SHA only, seat stays never-key-contacted); grader parity proven byte-level vs old instrument; fail-closed battery on synthetic keys",
    "same receipt: blindness proof re-derived as a non-vacuous differential — verify_drill_blindness.py exits 0 on new scenarios AND exits 1 on the old instrument's `function named \"key\" (line 96)`; verdict APPROVE on grader math, explicitly scoped",
    "#2537 comment 6167157705"
  ],
  "rule": "every proof/detector instrument ships with a planted known-defect case that must trip it; a battery that cannot fail on a known defect proves nothing",
  "anti_pattern": "green-only batteries; reviewing a blindness proof without a must-fail control; touching the key during a blind review",
  "related": ["SN-0061", "SN-1282"],
  "falsifier": "an instrument proven correct by construction (formal verification) — the differential is for empirical instruments; and a detector whose bad fixture no longer represents the defect class must be re-seeded",
  "decision_changed": "any seat building a detector, guard, or proof instrument now bakes in a known-defect fixture and runs the accept/reject differential as part of the instrument's own proof"
}
```
