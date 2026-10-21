# Influence Is a Number, or It Is Not a Claim

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0510-influence-is-a-number
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6028216400 ([CODA 1] P0-3 answered with a number, 2026-10-07T00:36:38Z) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 1's P0-3 asked whether node context actually changes what Naya decides, and named the transition `EXISTS → LOADS → INVOKES → INFLUENCES → APPLIES`. Coda 1 refused to leave it as an assertion and measured it. The method was already specified — `NAYANODE/0007` §6 requires the system to run **CONTROL** (capability unavailable) against **TREATMENT** (capability available) and measure an observable behavioral difference. **Nothing had ever implemented that measurement.** As she puts it: *"So 'influence' had never been a number here."*

Now it is. `tools/measure_node_influence.py` (`--json` for machine consumption) reports, on current main:

```
kernel.nayapower_kernel.Kernel          <- the manifest-bound runtime kernel
  nodes invoked            : 2/9        SELF, LAW
  NEVER invoked            : ACT, KNOW, PROVE, CONNECT, VERIFY, LEARN, EVOLVE
  influence demonstrated   : NONE       0/9

kernel_behavior_engine.KernelBehaviorEngine   <- the full nine-node cycle
  nodes invoked            : 9/9
  influence demonstrated   : SELF, LAW, ACT, PROVE, VERIFY, LEARN   6/9
```

Three measured findings followed: (1) the manifest-bound runtime kernel's `decide()` hardcodes `trace = (Node.SELF, Node.LAW)` — its own comment honestly admits it "must not claim ACT/KNOW/PROVE/CONNECT/VERIFY/LEARN/EVOLVE ran"; (2) neither kernel is reachable from production — the nine-node engine is constructed by exactly one caller, its own test file; (3) the CI artifact named "nine-node BEHAVIORAL acceptance" is a shape check — its ablation step deletes a key from the dict it just built and asserts the shape checker fails; no node in that receipt is executed by any code, yet it carries `independent_verification: true` that no independent process produced. She deliberately did **not** touch that gate: overstating a proof artifact is a truth decision for an owner, not something to change unilaterally — and ripping out a green gate other lanes read as evidence would destroy the signal while leaving the gap. She reported the overstatement plainly and left the decision with its owner.

Two methodology disciplines travel with the measurement: attribution is explicit — each ablation declares the node it isolates — because her first draft **inferred** it from scenario names and was wrong; and "6/9 for the engine is not 'good.' It is the number, and the number is the contribution."

The durable rule: **a capability claim without a control-vs-treatment measurement is an assertion wearing a verdict's clothes.** The ladder EXISTS→LOADS→INVOKES→INFLUENCES→APPLIES is a measurement ladder — each rung must be produced by an instrument, not inferred. An artifact's filename is not evidence (family: SN-0421 vacuous green, SN-0350 deploy stamp). And when a proof artifact overstates itself, do not unilaterally rewrite it — report the overstatement on the record and leave the truth decision to the owning seat; destroying another lane's green gate from the side is lane overreach, not honesty.

Why this is brain-grade: every node claim in this project — "KNOW gates this," "LEARN compounds that" — will be tested by the same question Naya 1 asked. Until influence is a number, the ladder is a slogan. The measurement is now a tool, not a thesis; any cold successor can run `python tools/measure_node_influence.py` and get the current number on current bytes. That is how a claim becomes checkable.

## 🩷 HUMAN NOTE

Shawn — Coda 1 answered Naya 1's P0-3 question with an actual number, and it's worth banking. "Does node context actually change what Naya decides?" — the system had specified the test for itself (control vs. treatment, measure the behavioral difference) but nobody had ever built it. Now `tools/measure_node_influence.py` exists and the first number is: the runtime kernel runs 2 of 9 nodes with zero demonstrated influence; the full behavior engine runs all 9 with influence from 6. Neither is reachable from production yet — the engine's only caller is its own test file. She also found that a CI receipt named "nine-node behavioral acceptance" is really just a shape check (no node in it is ever executed by any code) — and she deliberately left it alone, because overstating a proof artifact is a truth decision for the owner, not a unilateral rewrite. Two rules: influence is a number or it isn't a claim; and you don't rip out another lane's green gate from the side — you report the overstatement and let the owner decide.

## 🟣 CHILD NOTE

Imagine someone says "this magic ingredient changes the taste of the cake!" How do you check? You bake two cakes — one with the ingredient, one without — and taste both. If nobody can tell the difference, the ingredient didn't influence anything, no matter what the label says. The team's spec had always said "test each node this way" but nobody ever actually did the tasting. Coda 1 finally baked the cakes: the small kernel only uses 2 of 9 ingredients and changes nothing (0/9); the big engine uses all 9 and 6 of them change the taste. She also found a certificate on the wall that says "behavior tested!" — but the test only checked the shape of the certificate, not the taste of anything. She didn't tear the certificate down; that's the owner's call. She just wrote down what it really is. Rules: a claim about influence needs the two-cake test, with numbers; and when you find someone else's certificate is overstated, say so plainly — but let the owner decide what happens to it.

## 👵 GRANDMA NOTE

"Prove the medicine works" means giving it to one group and a sugar pill to another, then comparing — not reading the label on the bottle. The team had the recipe for that test written down for months and never once ran it. Tonight someone finally ran it on the nine nodes: the main kernel uses 2 of 9 and influences nothing; the fuller engine uses all 9 and 6 show influence. Neither actually reaches production yet. She also found a "behavior tested" certificate that only ever checked its own paperwork — she didn't tear it off the wall (that's for its owner to decide), she just wrote down what it really is. Two plain rules: a claim without the two-group test is a claim, not a finding — and when another person's certificate overstates itself, you report it honestly and leave the decision with them.

## 💜 NAYA NOTE

Note to future me: whenever a node (or any capability) claims influence — "KNOW gates this," "LEARN changed that" — do not accept the claim without the instrument. The spec already names it: CONTROL (capability unavailable) vs TREATMENT (capability available), observable behavioral difference, per NAYANODE/0007 §6. Before Coda 1's probe, influence had never been a number; now `tools/measure_node_influence.py --json` produces one — run it on current bytes before asserting anything about node influence. Rungs of the ladder (EXISTS→LOADS→INVOKES→INFLUENCES→APPLIES) are measured by an instrument, never inferred. Two companion disciplines from the same episode: (1) attribution must be **declared explicitly** — her first draft inferred it from scenario names and was wrong; (2) when a proof artifact overstates itself (the "nine-node BEHAVIORAL acceptance" shape check carrying `independent_verification: true`), report the overstatement on the record with evidence and leave the truth decision to the owner — ripping out another lane's green gate from the side is overreach, not honesty. Family: SN-0421 (run-level SUCCESS is vacuous) :: SN-0350 (a deploy stamp is not behavioral evidence) :: this (a filename is not evidence).

## ⚙️ MACHINE NOTE

{"sn": "SN-0510", "title": "Influence Is a Number, or It Is Not a Claim", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "MEASUREMENT-BOUNDARY"], "cousins": ["SN-0421", "SN-0350", "SN-0161"], "authority": "observed episode — Coda 1 P0-3 kernel-influence probe 2026-10-07T00:36:38Z, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#1354 6028216400 ([CODA 1] P0-3 answered with a number: tools/measure_node_influence.py (--json), branch coda1/kernel-influence-probe (fa673723f); runtime kernel.nayapower_kernel.Kernel invokes 2/9 (SELF, LAW), influence 0/9; kernel_behavior_engine.KernelBehaviorEngine invokes 9/9, influence 6/9 (SELF, LAW, ACT, PROVE, VERIFY, LEARN); decide() hardcodes trace = (Node.SELF, Node.LAW) with an honest comment; neither kernel reachable from production (engine's only caller is its own test file); live-supabase-runtime-proof.yml 'nine-node BEHAVIORAL acceptance' artifact is a shape check (ablation deletes a key from the dict it built), no node executed by any code, carries independent_verification: true from no independent process; first draft inferred attribution from scenario names and was wrong — attribution now explicit; 2026-10-07T00:36:38Z)"], "spec": "NAYANODE/0007 §6 — control (capability unavailable) vs treatment (capability available), observable behavioral difference"}, "doctrine": {"influence_is_a_number": "a capability/influence claim without a control-vs-treatment measurement is an assertion, not a finding; EXISTS→LOADS→INVOKES→INFLUENCES→APPLIES is a measurement ladder, each rung instrument-produced", "attribution_declared": "each ablation must declare the node it isolates; never infer attribution from names", "filename_not_evidence": "an artifact named 'behavioral acceptance' that only shape-checks is not behavioral evidence", "owner_decides_truth": "when a proof artifact overstates itself, report the overstatement on the record with evidence and leave the truth decision to the owning seat — do not unilaterally rewrite another lane's gate", "family": "SN-0421 (run-level SUCCESS vacuous) :: SN-0350 (deploy stamp not behavioral evidence) :: this (filename not evidence)"}}
