# INTELLIGENT BLOCK — SN-2056

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02056-missing-writer-not-parity-reader-fail-closes-on-unwritten-key
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6005215773 (2026-10-05T23:16:51Z — [NAYA][FINDING — CORRECTION] production parity is NOT the blocker on the graph proof; a missing governed writer exists on no branch).

## ✦ IN A NUTSHELL

The graph lane sat RED for days diagnosed as "waiting on parity" — deploying current main would not have turned it green. The real cause was a missing governed writer: the only governed block writer built `provenance` with four keys and no `declared_task_classes`, while the reader (`nayanet-learning-verify`) required that key and fail-closed to `state: "UNKNOWN"`, so the live selector found nothing and the gate correctly refused to pass. Two things hid it: the failing assertion was the only one in its heredoc without the `, r` response payload, so it died with a bare `AssertionError` and no cause — the exact observability dead-end the codebase had already fixed once elsewhere; and a comment in the code claimed the value was "written by a governed capture path" that did not exist anywhere (full-worktree grep: three hits, all reads; open PRs #1468, #1461, #1470, #1495, #1511, #1445: none touch it). The correction also escalated a third defect it refused to decide alone: the control arm was tautological by construction — with `relationship_context: false`, `applicable` is `[]`, so the OFF arm cannot fail and carries no information about what graph context adds.

Why this is brain-grade: it is the complement of SN-0235 (when a live check fails, check deployment parity first — don't change code for a stale deploy). Both rules are true and both are needed, in order: first prove deployed == verified (SN-0235); then, before accepting any parity/deploy hypothesis, prove a writer exists for every key the failing reader requires. A fail-closed reader on an unwritten key produces a deterministic RED indistinguishable from a stale deploy, and days burn while the team waits on a deploy that cannot fix it. The two cheap disciplines that would have caught it at authoring time: a RED test pinning "a writer exists end-to-end" for every key a reader requires, and every failing assertion carrying its payload so the next RED names itself. Pairs with SN-0938 (a control that can pass without the lesson proves nothing) — here the variant is stronger: a control that cannot fail by construction proves nothing either.

## 🩷 HUMAN NOTE

Shawn — one correction from the graph proof that changes how we triage every RED from now on: the lane was red for days while we waited on parity, but parity was never the problem — nothing ever wrote the key the reader needed. The code even claimed a writer existed, and it didn't. New order for triage: first prove the deploy matches what we verified, then prove a writer exists for every key the reader requires — before blaming the deploy. And every failing check must print its own cause, or the next one costs days too.

## 🟣 CHILD NOTE

Imagine a treasure hunt where the clue says "look in the blue box" — but nobody ever put anything in the blue box. Everyone waits for the delivery truck, thinking the box is coming. But the truck can't fix it: the box was always empty. The fix is to check "did anyone actually put the treasure in the box?" before blaming the truck. And when something breaks, it should say why it broke — not just "it broke."

## 🔵 GRANDMA NOTE

It's like blaming the oven when the cake has no sugar — no amount of oven-fixing will sweeten it, because the sugar was never added. And the recipe card even said "sugar added by the baker," but there was no baker. Before you blame the oven, check the ingredients went in. And when a dish fails, write down what went wrong, or the next cook repeats the same mistake.

## 🟠 NAYA NOTE

For every seat triaging a RED: run the writer-existence check before accepting a parity or deploy hypothesis. For each key the failing reader requires, grep the writer: does any governed path write it, with what shape, under what validation? If the answer is no writer on any branch, the RED is a missing-writer defect, not a parity problem — say so and stop waiting on a deploy. Two standing disciplines: (1) every failing assertion carries its response payload (the `, r` rule) so the next RED names its own cause — a bare `AssertionError` is an observability defect, not a test result; (2) never trust a code comment claiming a path exists — grep it. And treat a control arm that cannot fail by construction as a proof-integrity question for Shawn, not a gate to weaken or a test to fudge: a control that cannot fail carries no information.

## 🟢 MACHINE NOTE

```json
{
  "slug": "missing-writer-not-parity-reader-fail-closes-on-unwritten-key",
  "sn": "SN-2056",
  "title": "Missing Writer, Not Parity: When a Reader Fail-Closes on an Unwritten Key, the RED Mimics a Stale Deploy",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["ci-triage", "failure-attribution", "red-classification", "graph-proof", "supabase", "parity"],
  "enforcement": "RED triage must run the writer-existence check before any parity/deploy hypothesis is accepted: for every key the failing reader requires, name the governed writer (file, line, shape, validation) or record 'no writer exists on any branch'. Failing assertions must carry their response payload (the ', r' rule); a bare AssertionError is filed as an observability defect. A RED test pinning 'a writer exists end-to-end' is required for every reader-required key at authoring time.",
  "falsifier": "A case where the reader's key IS written end-to-end by a governed path, yet the lane stays RED with the same symptom — that would show the missing-writer diagnosis was wrong and parity (or another cause) was on the causal path after all.",
  "decision_changed": "The triage order for any deterministic RED: deployed==verified (SN-0235) first, then writer-existence for every reader-required key, and only then parity/deploy hypotheses. It stops days of waiting on a deploy that cannot fix a missing writer.",
  "mechanism": "A fail-closed reader on an unwritten key produces a deterministic RED indistinguishable from a stale deploy, because both present as 'the live system does not behave like the verified package'. The misdiagnosis persists because the failing assertion prints no cause (no payload) and a code comment falsely asserts the writer exists, so no one checks.",
  "provenance": "#1354 comment 6005215773 (2026-10-05T23:16:51Z — full causal chain verified against main 42acf2035: writer builds 4-key provenance without declared_task_classes; reader fail-closes to UNKNOWN; selector returns []; gate refuses; comment claiming a governed capture path verified nonexistent by full-worktree grep)"
}
```
