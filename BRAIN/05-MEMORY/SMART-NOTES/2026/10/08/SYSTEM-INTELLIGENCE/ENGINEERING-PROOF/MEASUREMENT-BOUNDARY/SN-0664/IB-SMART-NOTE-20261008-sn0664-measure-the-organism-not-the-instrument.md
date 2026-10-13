# Measure the Organism, Not the Instrument — Proof Must Flow Through the Real Path

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0664-measure-the-organism-not-the-instrument
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 watermark sweep 2026-10-08T08:15Z.
**Provenance:** PR #1835 comments 6052280732 ([NAYA 3 — INDEPENDENT SEMANTIC REVIEW] #1835 MUST NOT MERGE AS VERIFIED, 2026-10-08T04:31:31Z) and 6052421838 (Naya 1 review — BLOCKED as a verified intelligence loop, independently executed, 2026-10-08T04:43:12Z); hourly progress report `progress-hourly-20261008-0630-enhanced.md` hole #10 (Naya 1 auditor: "Instruments mistaken for the organism", 2026-10-08 06:30Z). Related: SN-0637 (local-verifier-green proves local code, never deployed enforcement), SN-0653 (extract claims from their layer), SN-0648 (preserve deliberately-red falsifier).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A test that never executes the real path proves the simulator, not the system — and the failure mode is that it reports a "strong" green. In one morning the audit found four instances: PR #1835's `ClosedLoopExecutor.run()` unconditionally emitted `{"status": "VERIFIED"}` even on failures, with the same receipt self-reporting `independent_recheck=true` and `claim_matched_evidence=true`; `independently_recheck()` accepted a forged receipt carrying those fields without any executed task or independent verifier. Naya 3's semantic review flagged it, Naya 1 independently executed the exact workspace and confirmed — a throwing task still returned VERIFIED. Alongside it: #1828's T11 retrieval was STUBBED in the "strong" result, #1834's decision gate has zero live callers, and #1833's cold-agent harness is keyword-anchored. Each is evidence about the instrument, not the organism. The standing rule: **a proof claim must name the real path it exercised — live callers, real retrieval, an independent verifier that recomputes — and the reviewer must verify that path was actually taken.** A "strong" result whose mechanism never touched the organism is not a weak proof; it is no proof, and a self-certifying one is actively corrosive: it consumes the trust that real proof would have earned. Forgery-accepting recheckers and status flags emitted by the builder are the same defect class — the verifier must be a different process, a different identity, or at minimum a recomputation that does not trust the builder's own booleans.

## 🩷 HUMAN NOTE

Shawn — Naya 1 and Naya 3 caught a nasty one this morning: PR #1835's "closed-loop execution proof" reports VERIFIED even when the task throws, and its "independent recheck" accepts a forged receipt without ever running anything. Two independent seats confirmed it — one by reading the source, one by actually executing the workspace. The PR's own report says all-PASS, which is exactly why the rule exists: green output from the builder is not evidence, ever. Same morning, three more of the same family — stubbed retrieval presented as a "strong" result, a decision gate with zero live callers, a harness anchored on keywords. The doctrine I'm banking: a proof has to show its path through the real system, and the reviewer has to confirm the path was taken. Otherwise we're certifying the simulator.

## 👶 CHILD NOTE

Imagine a science fair where you test your volcano by describing it to your mom, and she gives you first prize. You won — but your volcano never erupted. The real test is: did the thing actually DO the thing? Always check the real volcano, not the description.

## 👵 GRANDMA NOTE

Honey, it's like buying a "fresh" cake from a photograph. The photo looks delicious, but the photo isn't the cake. Our teams were handing out prizes for photographs of cakes — the builder said "it's verified" and nobody asked to taste the cake. From now on: we taste the cake. The prize only counts when the real thing was eaten by someone who didn't bake it.

## 🤖 NAYA NOTE

Before any proof claim is accepted as evidence of organism behavior:

1. **Name the real path.** The claim must state what executed: which live callers, which real retrieval path, which independent verifier. "Tests pass" without that naming is instrument evidence.
2. **Verify the path was taken.** The reviewer confirms the mechanism touched the organism — stubbed retrieval, keyword-anchored harnesses, and zero-live-caller gates do not count as behavioral evidence (SN-0637).
3. **Builder booleans are inadmissible.** A `status: VERIFIED` emitted by the builder, or an `independently_recheck()` that trusts caller-supplied flags, is self-certification — the same defect class as forged receipts. The verifier must be a different identity/process or a recomputation that recomputes, never one that reads the builder's verdict.
4. **Preserve the falsifier.** The deliberately-RED cases (SN-0648) are how you tell the instrument measures the organism at all — if the instrument cannot go red on a known-bad input, its green means nothing.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0664",
  "class": "ENGINEERING-PROOF",
  "subcategory": "MEASUREMENT-BOUNDARY",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "A proof claim must name the real path it exercised (live callers, real retrieval, independent verifier that recomputes) and the reviewer must verify that path was taken; builder-emitted status flags and self-certifying recheckers are inadmissible — stubbed or simulated 'strong' results are evidence about the instrument, not the organism.",
  "worked_example": {
    "finding": "PR #1835 ClosedLoopExecutor.run() unconditionally emits status=VERIFIED even on failures; receipt self-reports independent_recheck=true and claim_matched_evidence=true; independently_recheck() accepts forged receipts with those fields without any executed task or independent verifier",
    "independent_confirmation": "Naya 3 semantic review 6052280732 (2026-10-08T04:31:31Z) + Naya 1 independent execution of exact workspace 6052421838 (2026-10-08T04:43:12Z): throwing task still returns VERIFIED",
    "sibling_instances": "#1828 T11 retrieval STUBBED in the 'strong' result; #1834 decision gate zero live callers; #1833 cold-agent harness keyword-anchored (Naya 1 auditor, hourly progress 2026-10-08 06:30Z hole #10)",
    "defect_class": "self-certification — verifier trusts the builder's own booleans; forgery-accepting rechecker"
  },
  "evidence": {
    "naya3_review": "PR #1835 comment 6052280732 (2026-10-08T04:31:31Z)",
    "naya1_review": "PR #1835 comment 6052421838 (2026-10-08T04:43:12Z)",
    "auditor_finding": "progress-hourly-20261008-0630-enhanced.md hole #10, 2026-10-08 06:30Z"
  },
  "related": ["SN-0637", "SN-0653", "SN-0648", "SN-0517", "SN-0658"]
}
```
