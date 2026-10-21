# SMART NOTE — The Import-Still-Red Experiment

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-102` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn102-import-still-red-experiment` |
| Human title | Import-Still-Red: Locate the Composition Gap by Experiment, Not by Patching |
| Category | SYSTEM INTELLIGENCE |
| Topic | ENGINEERING PROOF |
| Subtopic | INDEPENDENT VERIFICATION |
| Captured | 2026-10-01 21:15:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (diagnostic method — pending taxonomy adoption) |
| Capture type | Method / Proof discipline |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5940410766 (NAYA sign-out: RED composition test + disposable-branch import, RED test commit 3cdd1f82, candidate import local 0a1ee5c69) |

---

## ✦ IN A NUTSHELL

**When you suspect a missing composition seam, import the candidate package into a disposable host branch and re-run the RED test: if it stays red, the gap is in the *host's* integration seam, not the package.** On current main (`7bc74f09`), a RED test for the public nine-node composition seam failed because the package was absent; after importing the candidate nine-node commits into a disposable branch, the RED test *still* failed — plain `Kernel().decide()` does not compose the real nine-organ handoff lifecycle, it only evaluates the available gate path. The import-still-red result proved the seam is missing in the host kernel, so the next action is to build the host seam — not to keep patching the package.

---

## 🩷 HUMAN NOTE

The question was: is the missing piece in the new package, or in the old code it's supposed to plug into? Instead of guessing, the Naya seat did a clean experiment: first, it wrote a test proving the piece was missing. Then it imported the whole new package into a throwaway copy of the old code and ran the test again. Still failing. That *proves* the hole is in the old code's side of the connection — the new package isn't the problem. One experiment ended a whole category of guesswork about where to work next.

---

## 🟣 CHILD NOTE

You have two Lego sets and they won't click together. Is the broken piece in the new set or the old set? You snap the new set into a spare old set and they STILL won't click. So the new set is fine — the old set is missing its connector. Now you know exactly which set to fix, instead of staring at both.

---

## 🔵 GRANDMA NOTE

When something won't fit together, don't keep reshaping one side and hoping. Try the honest test: put them together in a scratch copy and see where they still don't meet. The side that fails the test in the scratch copy is the side that needs the work. It's the difference between guessing at a problem and asking the problem directly.

---

## 🟠 NAYA NOTE

1. **The experiment:** RED test on the host proves absence. Import the candidate package into a disposable host branch (never merged, never pushed — local `0a1ee5c69` here). Re-run the RED test. Red again ⇒ the integration seam is missing in the **host**. Green ⇒ the package supplies it.
2. **Presence ≠ composition.** This is the experimental arm of SN-073 (invocation ≠ consumption ≠ enforcement): the package being *present* tells you nothing about whether the host *composes* it. The import-still-red result is the proof.
3. **Respect the RED result's verdict on scope.** The instinct is to keep improving the package ("maybe it needs more commits"). The experiment says: stop patching the package; build the host seam — "implement the smallest real public-runtime composition seam on the disposable current-main branch, using existing node public methods and canonical persistence/receipt boundaries only."
4. **Bound the experiment.** Disposable branch, no merge, no push, original working tree untouched. The experiment must not move the thing it measures.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn102-import-still-red-experiment",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Method",
  "experiment": {
    "host": "current main 7bc74f0910a7c8d4b23a304a5d5cdeb618f91a3b",
    "red_test": "3cdd1f82456862bbf32b692619dfbc5a204c05bb — public nine-node composition seam RED (package absent)",
    "intervention": "imported candidate nine-node kernel commits into disposable local branch 0a1ee5c69 (not merged, not pushed)",
    "result": "RED test still fails — plain Kernel().decide() does not compose the real nine-organ handoff lifecycle",
    "conclusion": "missing seam is in the host kernel, not the package"
  },
  "rule": "import-still-red ⇒ gap is in the host; stop patching the package, build the host seam",
  "family": ["SN-073 invocation != consumption != enforcement", "SN-066 red before green", "SN-061 post-merge verification at the pin"],
  "evidence": ["#554 comment 5940410766"]
}
```

---

## 🔗 HOW IT CONNECTS

- **EXPERIMENTAL ARM OF SN-073** (invocation ≠ consumption ≠ enforcement): SN-073 stated the conformance doctrine; this gives the experiment that locates which side of the seam is at fault.
- **COROLLARY OF SN-066** (red before green): the RED test came first (3cdd1f82); the import was the diagnostic, not a premature fix.
- **FEEDS SN-093** (trace the whole chain, stop at the first exact failing handoff): the host seam, once built, gets the nine-organ trace treatment.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** One clean execution of the experiment; the conclusion ("missing seam in host kernel") is the experiment's own verdict, not an assumption. A second composition gap in a different domain would promote the method from instance to standing doctrine.

## 🌍 APPLICABILITY

- **Applies to:** any suspected missing integration seam between a candidate package and a host — kernels, adapters, plugins, bridge contracts.
- **Does NOT apply to:** defects *within* a package (where the RED test is on the package itself) — import-still-red is a host-vs-package diagnostic, not a general debugging tool.

## 🧬 SUCCESSOR EFFECT

Future Naya: when the RED test names a missing seam and the candidate exists somewhere, run the import-still-red experiment before writing any fix. Let the experiment tell you which side to build on.
