# The Step Title Is Not the Diagnosis — Read Exit-Code Semantics and the Input Path Before the Step Name

**Intelligent Block:** IB-SMART-NOTE-20261018-sn01654-step-title-is-not-the-diagnosis
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-1540-lane9.md (2026-10-18, Naya Clarity Narzan, lane-9 scorer seat) — independent re-proof of PR #2399's delivery-gate failure on head a545f11079ca77ce6789d224ab519f272c7ca0e4; run 38201357308, job 114655261876.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A CI step's title is its **intent**, printed identically on PASS and FAIL — it cannot be the diagnosis. The diagnosis lives one level down: the step's **exit-code semantics** and the **code path** that produced the exit. The scorer that read the failing step name first got "policy refused the shipment"; the scorer that read the exit code (2 vs 1) and the gate's input path got the truth — tool plumbing upstream of the rule, not a policy refusal at all.

## 🩷 HUMAN NOTE

Shawn — the #2399 delivery-gate red carried a beautifully misleading name: "Delivery gate — bound receipt or no shipment." The name made the cause look like a policy decision about receipts. It wasn't. The exit code and the gate's own code path showed the failure happened *upstream of the rule entirely* — plumbing, not policy. The standing rule this earned: when a gate fails, read the cause channel (exit code + input path) before the intent channel (the step name). Names say where; codes say what.

## 🟣 CHILD NOTE

Imagine a smoke alarm that shouts "FIRE IN THE KITCHEN!" every time it goes off — even when it's just a low battery. The alarm's words say "kitchen," but the little blinking pattern on the side says "battery." If you only listen to the words, you call the fire department for a dead battery. The rule: read the blink pattern (the code) first, then the words (the name).

## 🔵 GRANDMA NOTE

It's like a medicine bottle labeled "for headaches." The label is what the maker *meant* it for, but the label is printed on every bottle — the ones that help, and the ones that were recalled. If the medicine made you feel worse, you don't start with the label; you start with what actually happened — the dose, the timing, the reaction. The label describes intent; the effects describe cause. Diagnose from causes, not labels.

## 🟠 NAYA NOTE

Cold successor: the gate-failure diagnosis procedure.

1. Get the step's **exit code / conclusion** from the jobs API (not the badge, not the title). Learn the gate's exit-code contract first: in this gate, exit 2 vs 1 distinguished tool-plumbing failure from judged failure.
2. Walk the gate's **input path**: which rungs fed this step, and where exactly did the value break? Re-execute the gate's rungs locally on the pinned head bytes with the live inputs, blob-verified, like CI would.
3. Only then read the step name — as the *location* of the failure, never as its *cause*.
4. Known failure mode of this rule: a gate whose exit codes are uniform (everything exits 1) carries no cause in the code channel — then the name plus logs do the work. This rule fires where exit codes distinguish cause classes; where they don't, it stays silent.

Refines (not replaces) SN-0921, which taught "classify a CI red by the failing step name, never by the badge." That note moved diagnosis one level deeper than the badge; this note moves it one level deeper still: badge -> step -> exit code + code path. Same ladder, one more rung.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1654",
  "title": "The Step Title Is Not the Diagnosis — Read Exit-Code Semantics and the Input Path Before the Step Name",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "RED-RUN-DIAGNOSIS"],
  "applies_when": ["ci", "gate-diagnosis", "verify", "gate-failure", "merge-readiness", "blocker-classification"],
  "enforcement": "Gate-failure diagnosis receipts must cite the step's exit code and the failing code path — jobs-API step conclusion and/or local re-execution of the gate's rungs on pinned bytes — before any step-name-based cause claim. The scorer bounces diagnoses that name only the step title as unverified.",
  "cousins": ["SN-0921 (classify a CI red by the failing step name, never by the badge — this note refines it one rung deeper: badge -> step -> exit code + code path)"],
  "evidence": {
    "delivery_gate_failure": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-1540-lane9.md (2026-10-18): PR #2399 head a545f110, delivery-gate run 38201357308, job 114655261876, failed step 'Delivery gate — bound receipt or no shipment'",
    "exit_code_truth": "exit code 2 vs 1 plus the gate's own code path showed the failure was upstream of the rule entirely — tool plumbing, not policy; the step name described intent, identical on PASS and FAIL",
    "parallel_leg": "same receipt, leg (a): the CI red described the INPUT SNAPSHOT, not the current state — verdicts are functions of (inputs, trigger-set), never of the badge alone",
    "independent_proof": "delivery-gate TOOL-ERROR narrowed to two raise-site candidates via protected re-execution of pr_changed_files + pinned design-gate fetch (PASS exit 0 on live-equivalent inputs) — cause localized by code path, not by name"
  },
  "decision_change": "when a CI gate fails, the diagnosis order becomes: exit-code semantics and input path first, step name last — the name tells you WHERE it failed (the location), the code tells you WHAT failed (the cause). Step-name-first diagnoses are treated as provisional until the code channel confirms them.",
  "falsifier": "a gate whose exit codes are uniform (all failures exit 1) — the code channel carries no cause information there, and the step name plus logs do the work. If future gate-failure diagnoses show the step name alone beating code-first reading as the correct diagnosis, this note is demoted to a conditional.",
  "mechanism": "step names are author-written intent strings, printed identically on PASS and FAIL; exit codes and input paths are cause-carrying. A diagnosis that reads only the intent channel will systematically misattribute plumbing failures as policy decisions."
}
```
