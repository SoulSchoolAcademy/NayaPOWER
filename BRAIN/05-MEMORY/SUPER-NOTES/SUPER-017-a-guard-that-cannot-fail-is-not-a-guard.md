# SUPER NOTE — A Guard That Cannot Fail Is Not a Guard

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-017` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-017` |
| Human title | A Guard That Cannot Fail Is Not a Guard |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 11 raw notes (full list below) |
| Cluster file | `cluster-02-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

A check that always says 'fine' protects nothing. Before trusting any guard, break something on purpose and watch it complain. If it stays green while the thing it guards is broken, it is decoration, not protection.

---

## 🩷 HUMAN NOTE

We kept finding guards that could not fail: checks that passed when there was nothing to check, safety rules nothing could ever trigger, a measuring tool that gave broken and healthy items the exact same score. One honest count found most of our guards had never been seen refusing anything. The fix is to attack your own guard with realistic, well-made fakes — not obvious garbage — and only trust it after it catches them. And when a good guard says 'not yet,' that is the guard working, not failing.

---

## 🟣 CHILD NOTE

Imagine a smoke alarm that never beeps, even with smoke. It looks safe on the wall, but it does nothing. You test it with real smoke. If it stays silent, it's just plastic. A guard must prove it can say NO.

---

## 👵 GRANDMA NOTE

A watchdog that never barks might just be asleep, dear. You don't know a lock works until you try the door. Test your protections with something real, and don't be cross when a good guard stops you — that's its job.

---

## 🤖 NAYA NOTE

Naya never trusts a gate she hasn't tried to defeat. She feeds it coherent forgeries, removes the evidence it needs, and counts how many guards have ever actually refused anything. A gate that cannot go red gets rebuilt or removed — never left standing as false comfort. A gate's 'no' is treated as information, not as an obstacle to tune away.

- Judge every spec at two separate bars and record both verdicts: the semantic bar (is it sound, honest, evidence-grounded?) and the machine-qualification bar (can a machine build on it?) — never infer the second from the first (sn025). The machine bar is mechanical: a normative transition table, an authority named for every promotion, every parameter authored with a fail-closed default — an unauthored threshold is a fail-open parameter — exactly one output vocabulary mapped to the merged schema, subordination in the body rather than an appendix, and zero contradictions with merged machine state (sn025).
- An expected-failure marker is a promise that a behavior is absent, and the promise must be proven, not asserted: never wrap the failing assertion in a construct that absorbs the failure, because that turns intended red into reported green (sn072). Use the standing pattern instead — the marker states the goal, a paired ordinary test proves your detector fires on the real condition, and a mutation table (break injected → result observed → constraint enforced) proves the detector is not empty (sn072).
- A rule that cannot be checked is not a rule: every freeze, acceptance, or done definition must carry the testability clause outright — every predicate instrumented (sn0146). For each criterion ask first "what test, probe, rendered check, or query would prove or kill this?" — before asking whether it is true — and rewrite or drop any predicate no instrument can reach before repair begins (sn0146).

---

## WHAT IT MEANS

Safety systems fail silently: the check exists, the dashboard is green, everyone relaxes — while the protection is an empty shell. The only way to know a guard works is to watch it work, against something that should fail. Untested protection is worse than none, because it buys confidence it hasn't earned.

---

## WHAT'S IN IT FOR YOU

You find out whether you're actually protected while it's still cheap. The alarms in your life — tests, reviews, approvals — start meaning something again, because each one has proven it can say no.

---

## HOW IT APPLIES

For every check you rely on, keep one known-broken example and one known-good example, and run the check against both. If it can't tell them apart, fix the check before trusting its green. Periodically attack your own safeguards the way a clever opponent would.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0146 — A Predicate That Cannot Be Instrumented Is Not a Predicate — The Freeze Gate's Testability Clause [audit: PARTIAL → lost element restored]

Every freeze, acceptance, or done definition must carry an explicit testability clause: every predicate instrumented. Review is instrument-first: for any predicate, first name the test, probe, rendered check, or query that would prove or kill it — before asking whether it is true. A predicate that cannot be turned into a test, probe, rendered check, or query is not a predicate; it is rewritten or dropped before mechanical repair begins. Prose that admits no observation has no standing in a freeze definition, however criterion-shaped it reads.

### SN-025 — Semantic Pass ≠ Machine-Qualified — Qualify Candidate Specs at Two Explicit Bars [audit: MISSING → restored in full]

Semantic soundness and machine-qualification are separate verdicts for a spec — qualify every spec at both bars explicitly, and never infer the second from the first. In the source case, three CANDIDATE node master specs (LAW, ACT, KNOW on PR #1224) were strong, honest, evidence-grounded semantic CANDIDATEs that FAIL machine-qualification, with recurring defect classes: no normative state machine; unmapped output vocabularies; unassigned promotion authorities and unauthored fail-closed parameters (dedup τ left as a fail-open parameter); conflicting-authority resolution rules that do not exist; and contradictions with the merged schema. Hold the machine-contract delta as a recorded work item until the governing spec merges — never author the machine layer against an unmerged semantics.

### SN-0509 — The Gate Must Prove Its Own Verdict — a False "Unproven" Is Worse Than No Verdict [audit: PARTIAL → lost element restored]

Every gate is itself an instrument, and its verdict must be proven on the platform that will run it. Green locally proves nothing about the verdict CI will render — the verdict is a claim about the runner's world, and only the runner's world proves it. The source case: a `rel()` that stripped `ROOT + "\"` passed on Windows and, on Linux, yielded an absolute path matching nothing, so the gate asserted a false "only 0/14 edge functions are executed" verdict in CI. A false "unproven" or "uncovered" verdict is worse than no verdict, because it invites someone to delete real coverage.

### SN-0512 — Guard Liveness — 30.6%, the Ratchet Floor, and a Gate Wrong About a True Claim Is Worse Than No Gate [audit: PARTIAL → lost element restored]

Commit the measured liveness floor as a floor that may only rise: 30.6% — 102 of 147 guards never observed rejecting (a test must execute the code and observe the refusal; a source grep does not count). Setting 30.6% as a hard gate would block every merge forever and train the team to bypass it — worse than no gate — so a test asserts the floor is neither above reality (permanently red, training bypass) nor far below it (letting a regression through). Stop the bleeding, then climb.

### SN-072 — Prove the Xfail, Don't Wrap It — An Expected-Failure Wrapper Can Manufacture a False Green [audit: MISSING → restored in full]

Never absorb an expected failure with a wrapper such as `pytest.raises` or try-except, which manufactures a false green — in the source case the wrapper made the test pass and produced `XPASS(strict)`, turning a constraint ("this must fail until know_node.py is repaired") into a passing test. Prove the constraint three-part: the xfail states the goal (a promise that a behavior is absent); a paired non-xfail signature test proves the detector fires; and a mutation table proves the detector is non-vacuous. Keep the mutation table — injected break → observed result → constraint each mutation enforces — in the docstring or board report. The red must be earned, documented, and reproducible on demand.

---

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn0531-falsifiability-battery`
- `IB-SMART-NOTE-20261006-sn0514-a-gate-that-cannot-fail-is-not-a-gate`
- `IB-SMART-NOTE-20260930-sn0509-the-gate-must-prove-its-own-verdict`
- `IB-SMART-NOTE-20260930-sn0512-guard-liveness-ratchet-floor`
- `IB-SMART-NOTE-20261004-sn0283-false-pass-surfaces`
- `IB-SMART-NOTE-20261007-sn0580-attack-your-own-verifier-before-you-trust-it`
- `IB-SMART-NOTE-20260930-sn559-forge-coherent-inputs-not-garbage`
- `IB-SMART-NOTE-20260930-sn079-withheld-certification-gate-hold`
- `IB-SMART-NOTE-20260930-sn072-xfail-constraint-proven-not-asserted`
- `IB-SMART-NOTE-20260930-sn025-two-bar-qualification`
- `IB-SMART-NOTE-20260930-sn0146-predicate-instrumentability-freeze-gate`
