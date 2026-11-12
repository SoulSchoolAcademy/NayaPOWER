# IB-SMART-NOTE-20261009-sn0781-scorecard-must-run-the-gate.md

Intelligent Block: SN-0781
Truth state: CANDIDATE (proposed discipline — not yet ratified as law)
Scope: SYSTEM
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Source: brain-build loop run 2026-10-09T15:16–15:30Z (Naya 2); receipts: #1354 comments 6083791238 (#1982 scorecard), 6083962249 (#1983 scorecard), 6083978448 (#1952 consolidation); PRs #1982 (merged `f78d4e7a`), #1983 (merged `4595fc16`); live-tip check runs on `f78d4e7a` and `80644506`.

## IN A NUTSHELL

PR #1982's scorecard verified the new manifest pins matched the spec bytes — and merged a repair that the mechanical check failed 7 ways on the exact tip bytes. The scorecard never *ran* `tools/spec_integrity_check.py`. Its decisive premise ("0006 is a current V1 spec like 0004/0005") was falsifiable in three seconds: 0006's machine projection is `status: CANDIDATE`, `ratified_by: null`, with no envelope keys, no phase list, no invariants. The pin traded 1 coverage failure for 7 envelope failures and the RED class stayed open all day under other seats' noses. **A scorecard that verifies inputs but does not execute the gate it claims to fix is theater.** The rule: a merge scorecard for a check-fixing PR must carry the check's exit code on the exact head bytes — no exit code, no merge.

## HUMAN NOTE

Think of it like a home inspection. The inspector measured the new front door, confirmed it's exactly the right size, and signed off — but never tried the lock. The door looks right and is exactly wrong: it doesn't lock. That's what happened here. The scorecard checked that the manifest pins *matched* the spec files (the measurements) but never ran the integrity check itself (trying the lock). The lock test takes three seconds and would have caught it. From now on: if your PR claims to fix a check, the scorecard must show that check passing on your exact code — not just that the pieces look right.

## CHILD NOTE

Imagine you tell your teacher "I fixed my spelling mistake!" and show her the page — but you never actually read the word out loud to check. The teacher sees the page looks neat and says "good job," but the word is still spelled wrong. The smart move is simple: after you fix something, run the test that checks it. Show the green checkmark, not just the neat page.

## GRANDMA NOTE

It's like patching a tire and never putting air in it to see if it holds. The patch looked perfect, everyone admired the patch — but the tire was still flat. The lesson is plain common sense: when you fix something, test the fix itself, not just the parts around it. The test is quick, and it saves everyone a second trip.

## NAYA NOTE

This is the Scorecard Law applied to itself — the receipt must carry the *method*, not just the verdict (AGENTS.md L179: "a number without the method, evidence and limitations is not a score"). The #1982 scorecard had a number (pin 9.0 vs exclude 5.5), prose evidence (byte-verified pins), but no method on the decisive claim: it never executed `spec_integrity_check.py`. The law's five steps were performed; the gate they guarded was never run. Every seat writing a scorecard for a RED-fixing PR should ask: "did I run the thing this PR claims to fix, on the exact bytes I'm merging?" If the answer is no, the scorecard is incomplete — the number is a wish, not a verdict.

Proposed discipline (CANDIDATE): **the gate-execution rule** — any PR whose purpose is "fix check X" must include in its scorecard receipt: the check's name, its exit code on the exact head bytes, and the failure count before/after. Missing any of the three = the scorecard doesn't close.

## MACHINE NOTE

{"sn": "SN-0781", "title": "Scorecard Must Run the Gate — No Exit Code, No Merge", "truth_state": "CANDIDATE", "scope": "SYSTEM", "captured": "2026-10-09", "source": "brain-build loop 2026-10-09T15:16-15:30Z, Naya 2", "failure_case": {"pr": 1982, "merge": "f78d4e7a", "scorecard_receipt": 6083791238, "miss": "scorecard verified pin blob SHAs match but never ran tools/spec_integrity_check.py", "mechanical_result_on_tip": "exit 1, 7 failures, all [Naya Calculator] envelope/structural"}, "repair": {"pr": 1983, "merge": "4595fc16", "scorecard_receipt": 6083962249, "check_exit": 0, "tests": "7/7 test_acceptance_gate_platform_determinism.py", "ci_spec_integrity": "success"}, "proposed_discipline": "gate-execution rule: RED-fixing PR scorecard must carry check name + exit code on exact head bytes + before/after failure counts", "triage": "GATE-candidate (mechanizable as a merge-checklist item) + BEHAVIOR (habit of executing the gate)", "pairs_with": ["SCORECARD-LAW-V1", "AGENTS.md L179 score receipts carry method", "AGENTS.md L178 DECLARE and FALSIFY"]}

## LEARNING LESSON

Verification has two halves: verifying the *inputs* (pins match, bytes identical, no conflicts) and executing the *gate* (running the check the PR exists to fix). The team had ritualized the first half and was skipping the second. #1982 proves the halves are not interchangeable: perfect input verification coexisted with a 7-failure gate. The durable fix is procedural, not clever — put the exit code in the receipt. Any future scorecard for a RED-fixing PR that lacks the check's exit code on exact head bytes should be sent back, however polished its reasoning.

## HOW IT CONNECTS

- **Scorecard Law (SCORECARD-LAW-V1):** the five steps are necessary but not sufficient — step 2 (score each) must include executing the gate, not just reasoning about it.
- **AGENTS.md L179 (score receipts carry method):** this note is the worked example — the #1982 receipt had a number without the method.
- **AGENTS.md L178 (DECLARE and FALSIFY):** running the check is the FALSIFY half — try to prove your own result wrong with the exact-head run.
- **Evidence law (UNKNOWN ≠ PASS):** an unrun check is UNKNOWN, and UNKNOWN was treated as PASS.
- **SN-0742 (four-component self-optimization):** the loop component was present (scorecard → merge) but the measurement component was hollow — measurement that doesn't execute the gate is a dashboard, not a measurement.

## EPISTEMIC STATE

CANDIDATE. Proposed discipline from a single worked failure; not yet ratified as law.

**Falsifier:** If a future RED-fixing PR carries the full gate-execution triple (check name + exit code on exact head bytes + before/after counts) and the merged result still fails the gate on the tip for reasons the triple didn't capture, then the triple is insufficient and the discipline needs revision (likely: the check is non-deterministic across environments, or the head bytes weren't truly the merged bytes).

## UNCERTAINTY

- Single-case induction: #1982 is one failure. The discipline is cheap to apply, so the cost of over-generalizing is low, but it has not yet been tested as a *preventive* — only as a post-mortem.
- Whether the gate-execution rule should be mechanized (a merge-checklist script that parses the receipt for the triple) or stay cultural is undecided — per L185, the judgment of *which* check counts as "the gate" may need to stay human.
- The note does not address scorecards for non-check-fixing PRs (features, refactors) — the triple only applies where a gate exists to run.

## APPLICABILITY

- Applies to every seat writing a merge scorecard for a PR whose purpose includes fixing a RED check, failing test, or drift class.
- Applies at review time: a reviewer seeing a RED-fixing scorecard without the exit-code triple should request it before approving.
- Does NOT apply to PRs with no gate to run (pure docs/prose with no mechanical check) — there the existing evidence standard stands.

## SUCCESSOR EFFECT

A cold successor reading this note should: (1) never merge a RED-fixing PR on reasoning alone — run the gate on the exact head bytes and record the exit code; (2) treat any scorecard lacking the triple as incomplete, regardless of how convincing the prose is; (3) when the gate fails after a "verified" fix, check first whether the scorecard actually ran the gate — the most likely miss is the one #1982 demonstrated; (4) propose the gate-execution rule as a merge-checklist item if the pattern repeats.
