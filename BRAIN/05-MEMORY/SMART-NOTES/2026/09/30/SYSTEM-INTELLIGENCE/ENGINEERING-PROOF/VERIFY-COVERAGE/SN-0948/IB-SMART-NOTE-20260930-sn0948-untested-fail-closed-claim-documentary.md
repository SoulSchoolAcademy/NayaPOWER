# An Untested Fail-Closed Claim Is a Documentary Claim

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0948-untested-fail-closed-claim-documentary
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Night-shift deep-map t2232-c (2026-10-10, verified tip `62e59713`, no drift); hidden_files/night-shift-2026-10-10/scores.jsonl t2232-c entry.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The t2232-c deep map of `tests/` (verified tip `62e59713`, 238 test files — 172 Python + 49 TS, coverage mapped by area: LEARN densest, EVOLVE thinnest, fail-closed asserted for safety/memory/consent) produced one surgical finding: `kernel/runtime_boot.py` has zero tests. It is the file that carries the fail-closed boot claim — the assertion that the organism boots safely when something is wrong — and nothing in the test corpus exercises that claim. A fail-closed claim with zero tests is a documentary claim: it exists in prose, not in machinery. It can be true today and silently false tomorrow with no alarm, because no test would notice the regression. The doctrine this note banks: **any safety-critical claim (fail-closed boot, consent enforcement, memory boundaries, safety gates) must have named negative-control tests that prove the bad path is closed — not just positive tests that prove the good path works.** Negative controls are the difference between "we believe it's safe" and "we have seen it refuse." The worker named the one next action: `test_runtime_boot_fail_closed.py`. Note the discipline: the finding is not "the boot is broken" — it is "the boot's safety is unverified." The honest label is "documentary only," carried openly until the negative tests land. A cold Naya auditing any safety claim months from now should first ask: where is the test that tries to violate it? If the answer is "nowhere," the claim is prose.

## 🩷 HUMAN NOTE

Shawn — from tonight's deep map of the test suite: we mapped all 238 test files by area, and there's one hole that matters. `kernel/runtime_boot.py` — the file that carries our fail-closed boot claim, the promise that the organism starts up safely when something is wrong — has zero tests. Not one test tries to make it fail. So the fail-closed promise is currently a written claim, not a proven one: it could quietly stop being true and nothing would tell us. The rule banked: any safety-critical claim needs tests that *try to break it* — negative controls that prove the bad path stays shut. The one next action is a new test file, `test_runtime_boot_fail_closed.py`. The finding isn't "the boot is broken" — it's "the boot's safety is unverified," and the honest label is documentary-only until the tests land.

## 🟣 CHILD NOTE

Imagine a sign on a door that says "this door always locks itself when you close it." That's the claim. Now imagine nobody ever tried closing the door and then pulling the handle to check. That's the test. The sign might be telling the truth — but until someone actually tries the handle, the sign is just words on paper. Tonight we found a really important door (the boot that starts everything) whose sign had never been checked. The rule: for the doors that matter most, you don't just read the sign — you try the handle.

## 👵 GRANDMA NOTE

A recipe book claimed the soup was safe to can because the pressure cooker "always seals properly." But the cook had never once tested the seal — she trusted the manual. One day the seal wears out and nobody knows until jars start spoiling. The fix isn't to throw out the pressure cooker; it's to test the seal before every canning run — the test that tries to make it fail. Until then, "it always seals" is a claim in a book, not a fact in the kitchen.

## 💜 NAYA NOTE

Future Naya: (1) Every safety-critical claim (fail-closed boot, consent enforcement, memory boundaries, safety gates) must carry named negative-control tests that attempt the violation and assert refusal — positive tests of the happy path do not prove safety. (2) Label any unverified safety claim "documentary only" openly; never let prose pass as machinery in a scorecard or proof. (3) When deep-mapping a test corpus, the highest-value hole is the untested critical claim, not the untested helper — `kernel/runtime_boot.py` (zero tests, fail-closed boot claim) outranks any coverage-count gap. (4) File the negative-test action by exact filename (`test_runtime_boot_fail_closed.py`) so the hole is actionable, not ornamental. Evidence anchor: t2232-c deep map at verified tip `62e59713` (238 files: 172 py + 49 TS; LEARN densest, EVOLVE thinnest); zero tests for `kernel/runtime_boot.py`; named next action in scores.jsonl t2232-c entry.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0948",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "VERIFY-COVERAGE"],
  "cousins": ["SN-0511", "SN-0945", "SN-0247"],
  "rule": "A safety-critical claim (fail-closed boot, consent enforcement, memory boundaries, safety gates) without negative-control tests is a documentary claim, not a proven one. Label it 'documentary only' openly; prove it with tests that attempt the violation and assert refusal; positive happy-path tests do not establish safety.",
  "anti_rule": "Counting a prose claim as machinery in a scorecard; treating positive tests as safety proof; letting an untested critical path regress silently with no alarm.",
  "evidence": {
    "deep_map": "t2232-c, 2026-10-10, verified tip 62e59713 (no drift), zero REST",
    "corpus": "238 test files: 172 Python + 49 TS; LEARN densest, EVOLVE thinnest; fail-closed asserted for safety/memory/consent areas",
    "hole": "kernel/runtime_boot.py — zero tests; its fail-closed boot claim is documentary only",
    "next_action": "test_runtime_boot_fail_closed.py named by the worker as the one next action",
    "note": "finding is unverified-safety, not broken-boot — classification kept honest"
  },
  "authority": "observed field finding — Naya 4 night-shift deep map, CANDIDATE (auto-capture, not ratified)"
}
```
