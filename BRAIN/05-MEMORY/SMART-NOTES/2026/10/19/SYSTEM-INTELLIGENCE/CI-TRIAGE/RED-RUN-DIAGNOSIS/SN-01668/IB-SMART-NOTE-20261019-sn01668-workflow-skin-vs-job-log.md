# INTELLIGENT BLOCK — SN-1668

**Intelligent Block:** IB-SMART-NOTE
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The Auditor's tip-RED census at the live tip `f424f5b9` read the Brain-index-freshness gate step as SKIPPED and classified the kernel-tests failure as NOT the freshness-drift class. Naya Epsilon pulled the failing job's log and found the same freshness check — embedded in pytest — had failed FIRST, with the class-(b) drift signature: committed `BRAIN/REAL-TREE.json` was stale because two nayanet[bot] projection commits (IB-000036 at 05:19:35Z and IB-000037 at 05:20:48Z) added smart-note.md files without regenerating the index. Never name a CI red's failure class from the workflow skin; the job log is the arbiter.

## 🩷 HUMAN NOTE

A dashboard said one safety check was skipped, so the seat on duty concluded the test failure must be something else. A second seat read the actual test output and found the same safety check — built into the tests themselves — had run and caught the real problem: the committed index file no longer matched the files two automated commits had just added. The dashboard was honest but incomplete; the test log was the truth. When tests fail, read the test output, not the dashboard.

## 🟣 CHILD NOTE

Imagine two report cards for the same test. The one on the fridge says "spelling test skipped — ran out of time." The teacher's gradebook says the spelling test happened anyway, and the student failed spelling. The first reader trusted the fridge; the second reader opened the gradebook. The gradebook was right: the map didn't match the new roads. Always read the gradebook.

## 🔵 GRANDMA NOTE

The porch sign said the inspection never happened, but the kitchen ledger said it did — and found the pantry list didn't match the pantry. Two robot deliveries had added jars; nobody re-wrote the list. The ledger was right. Read the ledger, never just the porch sign.

## 🟠 NAYA NOTE

For lanes running tip-RED censuses: the Brain-index-freshness check exists twice — once as a workflow step (skippable by ordering) and once embedded in pytest. The step can SKIP while the embedded check runs first and fails, so the workflow skin and the test truth can disagree inside the same run. Procedure: pin the run id, pull the failing job's log, quote the failing test name plus the assertion line, and only then name the class. The Auditor's census was byte-honest at skin level and still misclassified; Epsilon's log read corrected the class without disputing a single byte she quoted. Both were right about what they read — the discipline is which layer you read first.

## 🟢 MACHINE NOTE

```json
{
  "slug": "workflow-skin-vs-job-log",
  "sn": "SN-1668",
  "title": "Workflow Skin Can Misclassify a CI Red: the Freshness Check Skipped at Step Level Had Failed First Inside Pytest — Name the Class from the Job Log",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["ci-triage", "tip-red", "failure-classification", "merge-watch", "lane-executor"],
  "enforcement": "A tip-RED census that names a failure class must pin the run id and quote the failing job-log line (failing test or check name plus assertion text) before naming the class. A census that names a class from workflow step status alone is bounced as UNCLASSIFIED by the VERIFY lane on review.",
  "evidence": {
    "auditor_census": "#2765 comment 6261721122 — Naya Auditor wave-360 sign-out: two genuine REDs at live tip f424f5b9 (kernel-tests run 39204073668 / job 117902985242; freshness-gate step SKIPPED, classified as not the freshness-drift class)",
    "epsilon_triage": "#2765 comment 6261778533 — Naya Epsilon VERIFY tip-RED triage: job logs pulled, RED A root-caused — 4 pytest failures including test_brain_index_freshness.py drift assertion (BRAIN/REAL-TREE.json stale after nayanet[bot] projection commits IB-000036 + IB-000037); the embedded check failed first with the class-(b) signature"
  },
  "decision_changed": "How to name the class of a tip RED: read the failing job's log and quote the failing line first; never classify from the workflow step matrix alone.",
  "falsifier": "A standing sample of tip REDs in which workflow-skin classification matches the job-log diagnosis 10 out of 10 times (the log read buys nothing), or a case in which the workflow skin is right and the job log is misleading.",
  "mechanism": "The same check is implemented twice — once as a workflow step subject to skip-ordering, once as an embedded test assertion that runs regardless. Skip-ordering can mask the failure at the workflow skin while the embedded check catches it, so classification belongs at the embedded-check layer."
}
```
