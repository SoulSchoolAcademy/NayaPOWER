# Execution Identity Is Not Content Identity — Name the Execution When Joining Evidence Across Runs

**Intelligent Block:** IB-SMART-NOTE-20260930-sn082-execution-identity-not-content-identity
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5937505410 (Naya 4 — Demo-1 specimen reconciliation, 2026-10-01T18:07:43Z): the dispatch-authorized specimen (Specimen A: `bf63549c`, execution `exec-2faff1791adc7906`) and the frozen-package specimen (Specimen B: `ac45084d`, execution `exec-c13bfd8d64a49878`) share decision identity `dec-demo1-live-001` and the same artifact SHA-256 (`54e359a5…`) but are DIFFERENT executions. "Matching artifact content does not make them the same run."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two receipts can agree on everything content-addressable — same decision id, same artifact bytes, same hash — and still be different runs. The dispatch authorized Specimen A (`exec-2faff…`); the frozen evidence package holds Specimen B (`exec-c13bfd…`). Joining them as "the Demo-1 evidence" without naming which execution you mean silently merges two distinct runs into one claim, and every downstream verdict (persistence contract compatibility, PROVE grading, seam acceptance) inherits the contamination. The fix is a naming discipline: whenever evidence comes from more than one pipeline, every reference must name the execution identity, not just the decision identity or the artifact hash. Content hash is necessary for integrity; execution identity is necessary for provenance. Both, or you're citing a different run.

## 🩷 HUMAN NOTE

Imagine two lab notebooks with the same experiment title and the same result graph — but different dates, different technicians, different calibration logs. If you staple them together as "the experiment," every conclusion you draw cites a hybrid that never ran. That's what happened here: two Demo-1 runs produced the same decision and the same artifact, so the lanes started treating them as one specimen. The reconciliation table un-stapled them. The lesson for future work: same result ≠ same run. When you combine evidence, check that the execution identities match, not just the outcomes.

## 🟣 CHILD NOTE

Imagine your class does the same science experiment twice — once on Monday, once on Friday — and both times the plant grows 3 cm. If someone writes "the experiment showed 3 cm," which day are they talking about? Maybe Monday's plant had a broken ruler and Friday's was measured correctly. You can't mix the two days' notes together. The lesson: same answer doesn't mean same test. Always write down WHICH run your evidence comes from.

## 🔵 GRANDMA NOTE

It's like two identical-looking prescription bottles from different pharmacies. Same pills, same dose — but different batch numbers, different pharmacists. If something goes wrong with one batch, the batch number is what tells you which bottle to check. You'd never mix them up on purpose. When the system keeps records from two different runs, it has to track the "batch number" (the execution identity) the same way — not just the name of the medicine.

## 🟠 NAYA NOTE

Apply this wherever evidence joins across pipelines: (1) in any table or package that aggregates evidence, the join key is execution identity (execution id / receipt id), never decision identity or content hash alone — decision ids can be reused across runs, hashes attest bytes not runs; (2) when you discover a mismatch (as here), publish the reconciliation table on the board immediately — it prevents every other lane from silently citing the wrong specimen; (3) preflight/verification steps must reject evidence whose execution identity doesn't match the authorized subject — the dispatch named `exec-2faff…`, so `exec-c13bfd…` evidence is inadmissible for the seam even though its bytes match; (4) this is the identity-join cousin of SN-057 (temporal attribution) — there, the direction of time mattered; here, the identity of the run matters.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "execution_identity_confusion",
  "evidence": {
    "board": "#554 comment 5937505410 (2026-10-01T18:07:43Z) — Naya 4 specimen reconciliation table: Specimen A (bf63549c, exec-2faff1791adc7906, dispatch-authorized, IMMUTABLE) vs Specimen B (ac45084d, exec-c13bfd8d64a49878, frozen package, historical); same decision_ref dec-demo1-live-001; same artifact SHA-256 54e359a5…; different executions",
    "key_quote": "Matching artifact content does not make them the same run."
  },
  "rule": [
    "execution identity (execution/receipt id) is the join key across pipelines — decision identity and content hash are necessary but not sufficient",
    "any reference to 'the specimen' must name which execution identity it means",
    "preflight must reject evidence whose execution identity differs from the authorized subject, even when bytes match",
    "on discovering a mismatch, publish the reconciliation table on the board before other lanes build on the wrong specimen"
  ],
  "lesson_line": "Matching artifact content does not make them the same run. Name the execution identity when joining evidence across runs."
}
~~~
