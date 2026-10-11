# The Flagship Test: A Gate Must Block the Exact Violation It Exists to Stop — Demonstrated on the Fixed Head

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0959-flagship-test-gate-must-block-its-reason-to-exist
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [NAYA 2 VERIFY] Cross-seat review 8.1/10 NEEDS_WORK of the automatic document checker, #2175 comment 6106374017 (2026-10-11T06:46:42Z); [NAYA 2 · WIRE LANE] D32 holes closed, wiring verified live — sign-out, #2175 comment 6106455756 (2026-10-11T06:58:22Z). Cousin/contrast: SN-0939 (sabotage every suite to prove tests are failable — build-side discipline; this note is the acceptance-side discipline).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The D32 document gate was built, tested 19/19 green, sabotage-proof, and wired to the merge path — and two independent reviews found it waved through the exact violations it exists to block: scores like "8.44" and sentence-final numbers like "42." passed clean. Every decimal was stripped as a "version," sentence-final integers were invisible to the matcher, and the flagship claim — "stops the 59-vs-58 class of errors permanently" — was simply untrue on the bytes. Tonight the holes were closed on head `bed665f9` and the closure was proven the right way: 23/23 tests green plus 7/7 independent probes where `8.44`, `0.58`, `42.` → FAIL and `v2.1`, `1.2.3`, `version 2.0`, sourced `8.44` → PASS — and the flagship, `"We scored 59."` → **FAIL R1**. The standing lesson: **a gate's acceptance criteria must include its flagship violation — the exact case the gate's own claim is built on — demonstrated blocked on the fixed head.** Tests-passing is not proof of enforcement; the flagship failing is.

## 🩷 HUMAN NOTE

Shawn — the honest version of tonight's D32 story: we built a document gate, it passed all its tests, it was wired to the merge path — and it was letting through the very thing it was built to stop. Unsourced scores like "8.44" and sentence-ending numbers like "42." sailed past. The gate's own claim — that it stops the "59 vs 58" class of errors — was not true yet. The wire lane closed the holes and proved the closure properly: not just "tests pass," but "the exact violation this gate exists for is now blocked," demonstrated on the fixed code, seven probes, with the flagship "We scored 59." refused. The durable rule we're keeping: every gate ships with its flagship test — the one violation it exists to stop, proven blocked on the real thing. A gate that can't see its own violation isn't enforcement.

## 🟣 CHILD NOTE

Imagine a goalie who never lets in a shot from far away — but nobody ever tested him from close up, where all the goals actually happen. The practice stats look perfect. The real game is a disaster. The flagship test is: shoot the ball where the goals actually come from. If the goalie stops that one, he's a goalie. If he doesn't, he's just a statue in a nice uniform.

## 🔵 GRANDMA NOTE

They say "the proof is in the pudding" — but only if you taste the right pudding. You don't judge a mousetrap on how pretty it looks; you put a mouse in it and see if it snaps. This note says: every guard you build must be tested against the one burglar it was built to catch. If it catches that one, it can guard the house.

## 🟠 NAYA NOTE

This note composes with SN-0939, not duplicates it. SN-0939 is the build-side discipline: prove your tests can fail (sabotage the suite — kill a mutant, watch red). This note is the acceptance-side discipline: prove your gate blocks *its flagship violation* — the one named in its own claim — demonstrated blocked on the fixed head. A suite can be fully failable and still pass a gate that can't see the violation: SN-0939's mutants test the harness; the flagship test tests the rule itself. The D32 sequence is the template: review found the blind spots (8.44 / 42. — two distinct matcher holes), fix lane closed them, wire lane re-verified with probes on both the block set AND the allow set (v2.1, 1.2.3, version 2.0, sourced 8.44 must still PASS — precision matters as much as recall), plus the live check-run proof that the gate fires on the real PR path. Flagship + allow-set + live wiring = a closed enforcement claim.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "gate_integrity_rule": "gate_accepted(head) IFF flagship_violation(head) == BLOCKED AND allow_set(head) == PASSED AND live_check_run(head) == COMPLETED",
  "anti_pattern": "tests-green acceptance for a gate whose flagship violation was never demonstrated blocked (enforcement theater)",
  "flagship_test_checklist": [
    "extract the flagship violation from the gate's own claim (what it says it stops)",
    "demonstrate it BLOCKED on the fixed head (the failing probe is the proof)",
    "demonstrate the allow set PASSED on the fixed head (no over-blocking)",
    "show the live check-run on the real PR path"
  ],
  "evidence_anchor": {
    "review": "6106374017 — 8.1/10 NEEDS_WORK: '8.44' and '42.' passed; 'stops the 59-vs-58 class' claim untrue",
    "closure": "6106455756 — head bed665f9: 23/23 tests; 7/7 probes; flagship 'We scored 59.' -> FAIL R1; d32-doc-scan + d32-gate-tests live",
    "matcher_holes": "decimals stripped as 'version'; sentence-final integers invisible to matcher"
  },
  "canonical_object": "INTELLIGENT_BLOCK"
}
~~~

## 🟢 LEARNING LESSON

A green suite measures the code against its tests — not the gate against its purpose. The distance between "the tests pass" and "the gate enforces" is exactly one demonstrated refusal: the flagship violation, blocked, on the bytes. When the gate's own marketing sentence can't survive its own checker, the checker is a display, not a control.

## 🟡 WHAT IT MEANS

"Gate accepted" now means three demonstrated facts, not one: the flagship violation is blocked (precision on the case that matters), the legitimate allow set still passes (no over-blocking), and the gate fires on the live PR path (SN-0958's wire proof). Reviews score against this triad; 8.1/10 with an unblocked flagship is correctly NEEDS_WORK, not a block on the people — a block on the proof.

## ⚪ WHAT'S IN IT FOR YOU

Gates that do what their name says. The flagship test turns every gate review into a one-line check a cold successor can run: find the gate's claim, feed it the flagship violation, watch the refusal. If the refusal is there, the gate is real; if not, no test count can rescue it.

## 🟨 HOW TO APPLY / HOW TO USE

When building or reviewing a gate: (1) write down the gate's flagship violation in the gate's own words (the claim it makes about what it stops); (2) before acceptance, demonstrate that exact input refused on the fixed head — the refusal log is the acceptance artifact; (3) demonstrate the allow set (marked versions, sourced numbers) still passes; (4) require the live check-run on the real PR path. A gate merges only when all four are on the record.

## 🔗 HOW IT CONNECTS

- **COMPOSES WITH** → SN-0939 — sabotage-proof suites (tests must be failable; gates must block their flagship)
- **SUPPORTS** → SN-0958 — wire proofs must prove the gate can run (block on the bytes + fire on the live path)
- **PREVENTS** → enforcement-theater acceptances: green suites masking blind gates

## 🧭 KEY DECISIONS / PRINCIPLES

- A gate is accepted only when its flagship violation is demonstrated blocked on the fixed head.
- Precision without recall is theater; recall without precision is damage — prove both (block set + allow set).
- The flagship violation comes from the gate's own claim, not from the test author.
