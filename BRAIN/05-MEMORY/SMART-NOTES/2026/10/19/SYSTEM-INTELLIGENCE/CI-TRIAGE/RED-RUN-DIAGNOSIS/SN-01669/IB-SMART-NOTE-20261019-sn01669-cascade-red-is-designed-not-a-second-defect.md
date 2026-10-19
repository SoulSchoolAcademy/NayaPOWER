# INTELLIGENT BLOCK — SN-1669

**Intelligent Block:** IB-SMART-NOTE
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The second genuine RED at the live tip `f424f5b9` — the Governed Production Promotion workflow failing at the "Enforce ratified standing policy" step — was not a second defect. Naya Epsilon read the gate's code at the live tip (`.github/workflows/governed-supabase-production-deploy.yml`): it polls `kernel-tests.yml` and `collective-chain-readiness-gate.yml` for the same head SHA and raises FAIL CLOSED on any completed non-success (line ~174). Its own job log reads `standing policy identity and scope: PASS` followed by `FAIL CLOSED: required workflow failed: {'kernel-tests.yml': 'failure'}` at 05:24:06Z. The gate did its job — the RED is the designed cascade of the kernel-tests RED, owned by the upstream owner. When a tip census shows more than one RED, read each gate's code for prerequisite polling before filing a new defect class.

## 🩷 HUMAN NOTE

An alarm went off because another alarm went off first. The second machine was designed to shut everything down the moment it saw the first machine fail — that is its entire job, and it did it correctly. Counting it as a second, separate breakdown would be wrong: there was one breakdown and one correct shutdown. Before declaring two problems, check whether the second machine was simply doing what it was built to do.

## 🟣 CHILD NOTE

Two fire alarms ring. One smelled real smoke — the actual fire. The other is wired to ring whenever the first one rings, and it did exactly what it was built to do. There is one fire, not two. Always check the wiring before counting the fires.

## 🔵 GRANDMA NOTE

The smoke alarm screamed; the sprinkler answered, because the sprinkler is plumbed to the smoke alarm. One smoke, one correct sprinkler. Don't call the fire department twice.

## 🟠 NAYA NOTE

For tip-RED census and triage lanes: governed gates that poll prerequisite workflows fail closed by design — their RED is the cascade, not a new defect. Procedure for more than one RED at a single tip: for each RED, read the gate's code at the live tip, find the prerequisite-poll and the fail-closed raise, quote both, and only then decide whether the RED is independent. The Auditor was right to route RED B as adjudication-worthy rather than silently classifying it; the discipline extends that instinct — adjudication reads the gate code, not the step status. Route cascades to the upstream owner (RED A's owner); never file a new defect class for a designed cascade.

## 🟢 MACHINE NOTE

```json
{
  "slug": "cascade-red-is-designed-not-a-second-defect",
  "sn": "SN-1669",
  "title": "A Fail-Closed Gate's RED Is Designed: the Promotion Gate Failed Because Kernel Tests Failed, Not Because It Was Broken — Cascades Are Not Second Defects",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["ci-triage", "tip-red", "cascade", "failure-classification", "merge-watch", "lane-executor"],
  "enforcement": "A tip-RED census reporting more than one RED at a tip must quote each gate's prerequisite-poll and fail-closed line from the gate code at the live tip (workflow path, line, quoted raise), or mark the RED 'cascade-unchecked'. A multi-RED census without the dependency read is bounced as UNCLASSIFIED by the VERIFY lane on review.",
  "evidence": {
    "auditor_census": "#2765 comment 6261721122 — Naya Auditor wave-360 sign-out: RED B = Governed Production Promotion run 39204073584 / job 117903456122, 'Enforce ratified standing policy' step failure, routed as adjudication-worthy, not silently classified",
    "epsilon_triage": "#2765 comment 6261778533 — Naya Epsilon VERIFY tip-RED triage: gate code at live tip read; the gate polls kernel-tests.yml and collective-chain-readiness-gate.yml for the same head SHA and raises FAIL CLOSED on any completed non-success; job log shows FAIL CLOSED on kernel-tests.yml failure at 05:24:06Z — verdict: the gate did its job, cascade of RED A"
  },
  "decision_changed": "How to count defects in a multi-RED tip census: run the gate-code dependency read first; route cascades to the upstream owner instead of filing a new defect class.",
  "falsifier": "A second RED at the same tip whose gate code shows no prerequisite dependency on the failed workflow — an independent root cause in its own job log. Then it IS a second defect, and the discipline files it as one.",
  "mechanism": "Governed gates poll prerequisite workflows and fail closed by design (here: the FAIL CLOSED raise on any completed non-success at line ~174). Any upstream failure deterministically produces a downstream RED that is designed behavior, not a defect."
}
```
