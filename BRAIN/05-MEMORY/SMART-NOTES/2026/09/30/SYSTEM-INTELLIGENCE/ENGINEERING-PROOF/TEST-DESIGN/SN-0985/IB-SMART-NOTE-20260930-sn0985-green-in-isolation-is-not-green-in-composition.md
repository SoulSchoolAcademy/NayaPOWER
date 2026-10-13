# Green in Isolation Is Not Green in Composition

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0985-green-in-isolation-is-not-green-in-composition
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/TEST-DESIGN

## IN A NUTSHELL

While proving the #2345 end-to-end chain (PR `naya2/2244e-chain-proof`), the build lane found a composition defect: `test_learning_event_share_notify.py`'s outbox-absent simulation was **shadowed by the parent package attribute when composed with #2303's suite** — the test passed in its own file and silently tested something else in composition. Fixed in the test (4 lines, documented). The proof that held was the composed one: one synthetic failure run through the real CLIs in temp dirs — DETECTED → SHARED → ACKNOWLEDGED → RESOLVED → PRESERVED → REUSED (cold successor: fresh subprocess, scrubbed env, fresh broken scenario — retrieves the PRESERVED lesson and applies it) → BEHAVIORALLY_VERIFIED — 7/7 chain tests green, 95/95 with the four parents' suites on the exact pushed tree (byte-verified identical before the ref was created). The negative controls had teeth: successor with no lesson fails (control arm), successor refuses unpreserved lessons, kill-switch sabotage (`NAYA_EVENT_SHARE_NOTIFY=0`) fails the happy path at the handoff assertion.

The durable rule: **a unit-green test file is not evidence about the composed mechanism.** Name shadowing, fixture leakage, and import-time attribute resolution are composition-time phenomena — invisible to the file in isolation, load-bearing in the system. The proof of a composed mechanism must run the composed suite, on the exact pushed bytes. And a chain proof is only as strong as its negative controls: if the sabotage doesn't fail the happy path, the happy path proves nothing.

## HUMAN NOTE

Shawn — while proving the #2345 chain end-to-end, the lane found a sneaky defect: one test passed green on its own, but when run with the full suite it was silently testing the wrong thing (a package attribute shadowed its setup). Fixed in 4 lines. Lesson banked: tests green in isolation don't prove the composed system — run the composed suite on the exact bytes you're shipping, and make sure your negative controls actually fail when they should.

## CHILD NOTE

Your flashlight works fine in your bedroom — but in the living room with all the other electronics plugged in, it flickers. Testing it alone didn't tell you what happens when everything's together. Rule: test things the way they'll actually be used — together — because together is where the surprises live. And if your "what if it breaks" test doesn't break on purpose, it wasn't really testing anything.

## GRANDMA NOTE

It's like a recipe that works perfectly when you make each dish on its own, but in the real kitchen — everything cooking at once, sharing the stove — one dish keeps tasting off. You only find out when you cook the whole meal. Rule: judge the full meal, not the single dish — and make sure your safety checks actually catch the problems they're checking for.

## NAYA NOTE

I'm adding this to my proof discipline. Whenever I claim a composed mechanism works (chains, seams, handoffs between lanes' PRs), the proof battery runs the *composed* suites on the exact pushed tree — byte-verified before the ref is created — never the unit files in isolation. Concretely, I watch for fixture/setup shadowing: a test that simulates an absence (no outbox, no network, no permission) is the highest-risk kind, because composition can silently satisfy the thing it pretends is absent. And I keep the #2345 negative-control bar: the control arm must fail (successor with no lesson fails), the refusal must fire (successor refuses unpreserved lessons), and the sabotage must break the happy path at the right assertion (`NAYA_EVENT_SHARE_NOTIFY=0` fails at the handoff). If my sabotage doesn't fail my happy path, my happy path proved nothing — that's the test with teeth, and it's the one I trust.

## MACHINE NOTE

```json
{
  "sn": "SN-0985",
  "slug": "green-in-isolation-is-not-green-in-composition",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "TEST-DESIGN"],
  "authority": "distillation tick 2026-10-11 06:38 PDT, CANDIDATE (auto-capture, not ratified)",
  "evidence": {
    "board_comment": "#2175 comment 6109478558 (2026-10-11T13:23Z — BUILD LANE sign-out ~13:25Z, night shift, PR #2345 naya2/2244e-chain-proof)",
    "composition_defect": "test_learning_event_share_notify.py's outbox-absent simulation shadowed by the parent package attribute when composed with #2303's suite — green in isolation, wrong in composition; fixed in 4 lines, documented",
    "composed_proof": "synthetic failure through real CLIs in temp dirs: DETECTED->SHARED->ACKNOWLEDGED->RESOLVED->PRESERVED->REUSED (cold successor: fresh subprocess, scrubbed env) -> BEHAVIORALLY_VERIFIED; 7/7 chain green; 95/95 with four parents' suites on exact pushed tree (byte-verified before ref creation)",
    "negative_controls": "successor with no lesson fails (control arm); successor refuses unpreserved lessons; NAYA_EVENT_SHARE_NOTIFY=0 sabotage fails happy path at the handoff assertion — the test has teeth"
  },
  "rule": "prove_the_composed_mechanism_with_the_composed_suite_on_exact_bytes",
  "procedure": [
    "run composed suites (byte-verified tree), never unit files in isolation, when claiming a composed mechanism",
    "treat absence-simulating tests as highest risk for shadowing — verify what the test actually asserts under composition",
    "require negative controls: control arm fails, refusals fire, sabotage breaks the happy path at the right assertion",
    "if the sabotage does not fail the happy path, the happy path proves nothing"
  ],
  "related": ["SN-0719 (falsification — check your gates)", "SN-0815 (measure then adopt)"]
}
```
