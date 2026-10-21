# Push-Run Evidence — Query the CI Event That Answers the Question

**Intelligent Block:** IB-SMART-NOTE-20260930-sn036-push-run-ci-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The exact-main CI question for `a726a8376559609a3620f948ec7bfcabdba50abb` sat in genuine uncertainty until 2026-10-01 06:39 UTC (board comment 5926127502) — not because the evidence didn't exist, but because the evidence wrapper excluded push runs. Direct GitHub Actions push-run evidence closed it in one pass: Kernel Tests run 36812934009 (SUCCESS — Node 246/246, Python 545 passed/3 skipped, Brain index PASS), Collective Chain Readiness run 36812933999 (SUCCESS — controls 18/18 and 7/7, artifact still truthfully 2/11 satisfied), Promotion run 36812934028 (correct blocked/no-op, machine deployment not attempted). The durable lesson: when you assert "exact-main CI is green/unknown," name the run event (push, workflow_dispatch, pull_request) your evidence covers. A wrapper that only reads scheduled or PR runs manufactures uncertainty — or worse, manufactures confidence — about the push that actually landed the SHA. The correction lane also restated the boundary honestly: workflow-level promotion "success" is a no-op receipt, not a deployment; the protected deploy remains NEEDS_AUTHORITY.

## 🩷 HUMAN NOTE

The proof was sitting there the whole time — someone just checked the wrong mailbox. The CI runs that actually validated the main-branch SHA were push-triggered, and the tooling only looked at other kinds of runs, so the answer read "unknown" when it was "green." Always ask: which runs am I actually looking at? Match the event type to the claim.

## 🟣 CHILD NOTE

If you want to know whether the treehouse is safe, you have to look at the inspection of THIS treehouse — not the one next door. The wrapper was reading inspection reports for other treehouses, so it said "I don't know" even though this treehouse's report was right there saying "safe."

## 🔵 GRANDMA NOTE

It's like checking the answering machine for messages about a phone call — the message is there, you're just listening to the wrong recording. Ask what kind of recording you need before you say you have no message.

## 🟠 NAYA NOTE

When verifying exact-main (or exact-anything) CI status: (1) state the SHA and the claim; (2) query push-run evidence directly for that SHA — do not trust a wrapper unless you've verified which run events it includes; (3) report per-run: run ID, event type, suite, result; (4) separate "CI green" from "deployed" — a workflow success that records BLOCKED/no-op is a receipt, not a deployment; (5) keep the boundary explicit: protected deploys stay NEEDS_AUTHORITY and a green CI never converts that. A CI wrapper is itself a claim: it must name the events it covers, or it's a black box, not evidence.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": [
    {"board": "5926127502", "event": "exact-main CI uncertainty closed", "sha": "a726a8376559609a3620f948ec7bfcabdba50abb", "cause": "earlier wrapper excluded push runs", "fix": "direct GitHub Actions push-run query"},
    {"run": "36812934009", "suite": "Kernel Tests", "event": "push", "result": "SUCCESS", "detail": "Node 246/246; Python 545 passed/3 skipped; Brain index PASS"},
    {"run": "36812933999", "suite": "Collective Chain Readiness", "event": "push", "result": "SUCCESS", "detail": "controls 18/18 and 7/7; downloaded artifact still truthfully 2/11 satisfied; L01 not satisfied, L04–L11 UNKNOWN"},
    {"run": "36812934028", "suite": "Promotion", "result": "correct blocked/no-op", "detail": "durable artifact says BLOCKED; machine deployment not attempted; canonical proof not executed; protected-path explicit authorization required"},
    {"boundary": "workflow promotion success ≠ deployment; protected deploy remains NEEDS_AUTHORITY; bypass PROHIBITED"}
  ],
  "rule": "name_the_run_event_your_evidence_covers",
  "protocol": [
    "assert exact-SHA CI status only against run evidence for that SHA",
    "query push-run evidence directly; verify which events any CI wrapper includes before trusting its verdict",
    "report per-run: run ID, event type, suite, result, artifact honesty state",
    "separate CI green from deployed: a blocked/no-op workflow success is a receipt, not a deployment",
    "green CI never converts NEEDS_AUTHORITY on protected paths"
  ],
  "related": ["SN-018 (CI exit-2 triage)", "SN-021 (ci-test-red triage)", "SN-034 (AST strip-and-compare verification)"]
}
~~~
