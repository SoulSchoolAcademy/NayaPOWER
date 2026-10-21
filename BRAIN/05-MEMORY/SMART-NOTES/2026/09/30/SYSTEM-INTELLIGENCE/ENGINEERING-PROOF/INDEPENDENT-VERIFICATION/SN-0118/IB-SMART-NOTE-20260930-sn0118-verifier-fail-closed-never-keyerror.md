# SMART NOTE — A Crash Is Not a Verdict: Verifiers Must Fail Closed, Never KeyError

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-118` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn0118-verifier-fail-closed-never-keyerror` |
| Human title | A Crash Is Not a Verdict: Verifiers Must Fail Closed, Never KeyError |
| Category | SYSTEM INTELLIGENCE |
| Topic | ENGINEERING-PROOF |
| Subtopic | INDEPENDENT-VERIFICATION |
| Captured | 2026-10-02 00:20:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Proposed intelligence class | REUSABLE (verifier discipline for the evidence law) |
| Capture type | Failure classification / Process hardening |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5943060681 (Naya 2 brain-drive 17:01 PDT run: PR #1298 opened — `fix(value): independent_recompute fails closed on missing baseline id, accepts persisted name`; Coda 1's #1247 conformance run exposed the interop hole) |

---

## ✦ IN A NUTSHELL

**The verifier is the crux of the evidence law's independent-recomputation claim — and it crashed.** `independent_recompute()` in `kernel/value_calculus.py` hard-keyed `receipt["baseline_id"]`, but runtime-persisted receipts carry `baseline_candidate_id` — so the verifier died with a bare `KeyError` on real runtime-produced receipts. A crash is not a verdict; the evidence law's independent check must never crash on admissible input. The fix (PR #1298, head `5d5cb21d` on main tip `5885459a`): **tolerant reader, fail-closed writer** — accept `baseline_candidate_id` as the persisted-name alias; if both names are missing, raise an explicit `ValueError` refusing to recompute (a stated verdict), never a `KeyError` (an accident). The proof standard: the new persisted-name test was run as a negative control — it fails with `KeyError: 'baseline_id'` on pre-fix bytes and passes on fixed bytes. Two scoping facts keep the fix from being a grab: the writer-side name binding (persisting `baseline_id` alongside `baseline_candidate_id`) stays Naya 4's call on the #1243 seam — this PR touches the verifier only; and the diagnosis came from a conformance run (#1247), not a guess — interop holes are found where lanes meet, not where they write.

---

## 🩷 HUMAN NOTE

Imagine the court-appointed auditor whose one job is to double-check the books. One day she opens a real ledger and freezes — because the ledger labels the balance "opening balance (draft)" while her checklist only knows "opening balance." She crashes. That's not an audit finding; that's the auditor fainting. The fix is simple: teach the auditor both labels (they mean the same thing), and if neither label is there, she must *say so in writing* — "I cannot verify this ledger because the balance field is missing" — instead of fainting. And you prove the fix worked by handing her the old ledger first: she must faint on the old one and stand steady on the new one. Also: the person who *writes* the ledgers still decides which label gets stamped going forward — that's a separate job, and nobody snatches it.

---

## 🟣 CHILD NOTE

The checker has one job: check the homework independently. But when she got real homework (not practice homework), it said "answer_key_version" where she expected "answer_key" — and she just... broke. She didn't say "wrong" or "right." She broke. That's not checking; that's falling over. So the rule: the checker must accept BOTH label names (they mean the same thing), and if neither name is there, she must say clearly "I can't check this" instead of breaking. And you prove it by giving her the old homework first: she must break on the old one and work on the new one. One more rule: the person who *writes* the homework still decides which label to use from now on — the checker fixes her own checking, not someone else's writing.

---

## 🔵 GRANDMA NOTE

You hired an inspector to check every jar of preserves in the pantry. But the jars you actually canned have labels that say "peaches (batch B)" while her form only has a box for "peaches." So she stops, stares, and drops the clipboard. She didn't pass or fail a single jar — she just stopped working. The fix: her form now accepts both labels, and if a jar has neither, she writes "cannot inspect — no label" in the log instead of dropping the clipboard. To prove the fix, you hand her an old jar first: clipboard must drop on the old jar and stay in her hand on the new one. And the cannery still decides what goes on future labels — that's the cannery's call, not the inspector's. Everyone stays in their lane.

---

## 🟠 NAYA NOTE

1. **A crash is not a verdict.** `independent_recompute()` hard-keyed `receipt["baseline_id"]` while runtime-persisted receipts carry `baseline_candidate_id` — the verifier raised a bare `KeyError` on real runtime output. The evidence law's independent check must never crash on admissible input: an exception is a missing verdict, not a verdict. When your proof machinery can crash, your proof claim is conditional on the input being shaped the way you wrote it — which is exactly what the independent check is supposed to not assume.
2. **Tolerant reader, fail-closed writer.** The fix accepts `baseline_candidate_id` as the persisted-name alias (tolerant reader — the world persists what it persists), but if *both* names are missing, it raises an explicit `ValueError` refusing to recompute (fail closed with a stated reason). Never `KeyError`. This mirrors the P2 handoff discipline (`HandoffRefused`): refusal is a first-class, named outcome; accidents are not outcomes.
3. **Prove the fix with a negative control, not just a green suite.** The new persisted-name test was run against pre-fix bytes and fails with exactly `KeyError: 'baseline_id'`; on fixed bytes it passes. The negative control shows the test is capable of catching the defect — a test that passes on both versions proves nothing about this fix. Full-suite green (548 passed / 3 skipped, adversarial harness 6/6, value-calculus 65/65) is the regression guard, not the fix proof.
4. **Conformance runs find interop holes; unit lanes find unit holes.** The defect surfaced in Coda 1's #1247 conformance run — where lanes' real outputs meet — not in the lane that wrote the verifier. Seams between lanes are defect habitat; conformance runs are the trap.
5. **Scoped, not seized.** The fix touches the verifier only (rung-2 named file in the brain-drive lane); the writer-side name binding on the #1243 seam stays Naya 4's call. Tolerant reading never becomes a pretext for rewriting someone else's writer. The board comment says it plainly: "No duplicate mechanism: #1243's head carries the identical unfixed verifier line, and #1247 is a draft conformance doc, not a repair."

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn0118-verifier-fail-closed-never-keyerror",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Failure classification / Process hardening",
  "failure": {
    "location": "kernel/value_calculus.py :: independent_recompute()",
    "class": "verifier crash on runtime-produced input — hard-keyed receipt[\"baseline_id\"], runtime persists \"baseline_candidate_id\"; bare KeyError on runtime receipts",
    "discovered_by": "Coda 1 #1247 conformance run (interop hole, not a unit defect)",
    "doctrine": "a crash is not a verdict — the evidence law's independent-recomputation claim must never crash on admissible input"
  },
  "fix": {
    "pr": "#1298 (head 5d5cb21d on main tip 5885459a)",
    "mechanism": "tolerant reader (accept baseline_candidate_id as persisted-name alias) + fail closed (both names missing -> explicit ValueError refusing to recompute, never KeyError)",
    "negative_control": "new persisted-name test fails with KeyError: 'baseline_id' on pre-fix bytes, passes on fixed bytes",
    "regression": "brain index --check OK (166 files); adversarial harness 6/6 PASS; value-calculus + graph-binding 65/65; full suite 548 passed / 3 skipped; push byte-verified (remote tree SHA == local HEAD^{tree})",
    "scoping": "verifier only (rung-2 named file, brain-drive lane); writer-side name binding remains Naya 4's call on the #1243 seam — no duplicate mechanism, no seized ownership"
  },
  "evidence": ["#554 comment 5943060681"],
  "family": ["SN-112 pin what you consume (P3 post-intake aliasing — verifier-side hardening sibling)", "P2 HandoffRefused fail-closed handoff discipline", "SN-017 asserted is not verified (the verifier is the crux of the independent check)", "SN-031 classify-before-code (failure classification before repair)"],
  "open": ["writer-side name binding (persist baseline_id alongside baseline_candidate_id) on the #1243 seam — Naya 4's call", "PR #1298 awaits Shawn's merge word"]
}
```
