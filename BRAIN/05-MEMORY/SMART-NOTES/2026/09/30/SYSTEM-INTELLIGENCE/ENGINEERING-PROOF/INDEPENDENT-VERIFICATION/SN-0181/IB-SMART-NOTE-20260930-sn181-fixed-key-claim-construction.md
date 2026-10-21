# SMART NOTE — Build the Claim From a Fixed Key List; Injected Keys Never Reach the Claim

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-181` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn181-fixed-key-claim-construction` |
| Human title | Build the Claim From a Fixed Key List; Injected Keys Never Reach the Claim — Demo-1 P3's Post-Action Claim Hygiene |
| Category | SYSTEM INTELLIGENCE |
| Topic | ENGINEERING PROOF |
| Subtopic | INDEPENDENT VERIFICATION |
| Captured | 2026-10-02 12:45:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (repeatable implementation discipline — pending taxonomy adoption) |
| Capture type | Earned lesson / Implementation discipline |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5952470036 (Naya 4 self-build loop sign-out, Demo-1 P3 complete, 2026-10-02T12:36Z); `naya_kernel/prove_observation.py` on `naya4/nine-node-kernel-v1` @ `353d294b578dbd2375c05d86ec2bcf4c45604da2` (PR #1216 draft, unmerged) |

---

## ✦ IN A NUTSHELL

**The post-action claim must be assembled from an explicit, fixed key list — never copied from the incoming payload's keys.** In Demo-1 P3, `verify_observation_chain` runs fail-closed (EXECUTED-path check first: never proof-before-ACT; then ACT seal recompute, receipt-hash consistency, artifact re-hash, handoff receipt seal, KNOW block provenance + gated retrieval) and only then builds the EMPIRICAL post-action claim (observation + outcome + acceptance + causal limits + learning eligibility) from a fixed enumeration of allowed fields. Any key arriving on the input that is not on that list cannot reach the claim — by construction, not by inspection. 6/6 RED-first tests green (tamper / proof-before-ACT / invention / valid-prove+cross / challenged-at-crossing / G5 non-vacuity); live cold-replay from the persisted P1 receipt re-derived the same KNOW block (`kb-d16a19de20a668d514fab0ae`), all 7 re-verifications MATCH, PROVE PASS L2, crossing True, receipt `decision-demo1-prove-live-001` persisted (sha256 `a9f2d011…`).

---

## 🩷 HUMAN NOTE

Think of a sworn witness statement: the form has printed fields — what happened, what was seen, what followed, what it means, what it doesn't mean — and the witness may only write inside those fields. If someone slips a note into the envelope with extra "facts" scribbled on it, the clerk is not allowed to copy those scribbles into the statement, no matter how plausible they look. The form's printed fields are the entire vocabulary the statement may speak. Demo-1 P3 works the same way: the post-action claim is typed to exactly five fields (observation, outcome, acceptance, causal limits, learning eligibility), and the code builds it by pulling only those fields from verified evidence — never by iterating over whatever arrived in the input. Invention-by-copying becomes structurally impossible.

---

## 🟣 CHILD NOTE

Imagine your teacher says your book report must have exactly three paragraphs: what the book is about, your favorite part, and what you learned. You can't turn in a fourth paragraph about the movie you watched yesterday — even if it was really cool, it doesn't belong. The PROVE step does the same: it is only allowed to write the five specific things it was asked for, built only from things it actually checked. Anything else that tries to sneak in gets left out.

---

## 🔵 GRANDMA NOTE

When the county assessor writes up your house, the form has set boxes: address, square feet, condition, sale price. The assessor may not add a box for "rumor the neighbor sold for more" — only the boxes on the form get filled, and only from what was actually measured. P3 built the same rule into code: the claim form is fixed, and the pen only touches evidence that was verified first. That's how a cold reader — or a fresh Naya months from now — can trust that every word in the claim earned its way in.

---

## 🟠 NAYA NOTE

1. **Fixed key list = invention cannot ride in on the payload.** SN-069's rule ("adapter invents no executed_at/observed_at/received_at") was about the seam not inventing fields; this is the same law moved into the claim itself: the claim constructor enumerates its allowed keys, so a novel key on the input has no path into the output. The invention-test (one of the 6 RED-first tests) proves the negative directly.
2. **Seal re-verify + artifact re-hash happen BEFORE PROVE sees anything.** Order is load-bearing: `verify_observation_chain` first refuses proof-before-ACT (EXECUTED-path check — the master directive's "NEVER outcome-proof-before-ACT" as an executable gate), then re-verifies every upstream seal and re-hashes the artifact. Only verified facts enter; the claim is then *composed*, never *copied*.
3. **Truth-state honesty is part of the claim.** The directive held: PROVE never writes VERIFIED — L2/L4 emit SUPPORTED. ACT success ≠ outcome success; the claim is bounded to the bound bytes. A claim that says less than it could is the integrity signal a cold successor can audit against.
4. **Live cold-replay is the acceptance proof, not the unit tests alone.** The 6/6 RED-first tests gate the implementation; the 7/7 re-verification MATCH on a cold replay from the persisted P1 receipt (same KNOW block re-derived deterministically) proves the claim construction survives the process-death boundary — write ≠ memory (SN-103 family).
5. **Where it sits in the directive.** This is the Demo-1 master directive's pre-action proof (identity + authority + scope + capability + parameters + admissibility) and post-action proof (observation + outcome + acceptance + causal limits + learning eligibility) operationalized at the PROVE/CONNECT gate. Remaining hole stays explicit: VERIFY intake of the proven observation (P4), then LEARN/EVOLVE/FRESH SELF — never outcome-proof-before-ACT remains the standing fence.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn181-fixed-key-claim-construction",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Earned lesson / Implementation discipline",
  "rule": "post-action claim constructed from explicit fixed key list; injected input keys have no path into the claim",
  "implementation": {
    "module": "naya_kernel/prove_observation.py",
    "gate": "verify_observation_chain — EXECUTED-path check (never proof-before-ACT) → ACT seal recompute → receipt-hash consistency → artifact re-hash → handoff receipt seal → KNOW block provenance + gated retrieval",
    "claim_fields": ["observation", "outcome", "acceptance", "causal_limits", "learning_eligibility"],
    "truth_states": "PROVE emits SUPPORTED at L2/L4, never VERIFIED",
    "tests": "6/6 RED-first green (tamper, proof-before-ACT, invention, valid-prove+cross, challenged-at-crossing, G5 non-vacuity); suite 594 + 545 passed, 3 skipped",
    "live_cold_replay": "7/7 re-verifications MATCH from persisted P1 receipt; KNOW block kb-d16a19de20a668d514fab0ae re-derived; receipt decision-demo1-prove-live-001 sha256 a9f2d011…"
  },
  "branch": "naya4/nine-node-kernel-v1 @ 353d294b578dbd2375c05d86ec2bcf4c45604da2 (draft PR #1216, unmerged)",
  "family": [
    "SN-069 bindings at the observing layer (adapter invents no fields)",
    "SN-027/SN-065 phantom-citation class (honest PARTIAL > invented capability)",
    "SN-103 prove memory across the process-death boundary (write != memory)",
    "SN-066 red-before-green (RED-first tests precede the fix)",
    "Demo-1 master directive: NEVER outcome-proof-before-ACT; pre-action/post-action proof structure"
  ],
  "evidence": ["#554 comment 5952470036", "naya_kernel/prove_observation.py @ 353d294b578dbd2375c05d86ec2bcf4c45604da2", "~/workspace/demo-staging/receipts/decision-demo1-prove-live-001.json (a9f2d011…)"]
}
```

---

