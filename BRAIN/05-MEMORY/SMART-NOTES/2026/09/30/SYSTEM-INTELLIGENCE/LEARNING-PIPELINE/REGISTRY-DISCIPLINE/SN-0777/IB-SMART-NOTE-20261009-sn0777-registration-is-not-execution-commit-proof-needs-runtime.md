# Registration Is Not Execution — a Registry Heal That Skips the Runtime Breaks the Commit Proof

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0777-registration-is-not-execution-commit-proof-needs-runtime
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6080287835 (NAYA 2 DEFECT root-cause, 2026-10-09T11:51:13Z); comment 6080176300 (pipeline-monitor tick-118 fresh-lesson RED); comment 6080172324 (Naya 2 build-list queue); PR #1959 (registry heal for SN-0742/0743/0744, merged 2026-10-09T11:36:11Z); main tip `de6e247b`; job https://github.com/SoulSchoolAcademy/NayaPOWER/actions/runs/37924751609/job/113800899539

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1959 healed the Smart Note registry by registering SN-0742/0743/0744 in `.naya/memory/smart-notes/index.json` — bookkeeping — but it never ran the three notes through the live intelligence runtime. 613 of 620 registry entries carry a runtime-issued `provenance` key; the three new ones didn't. The same push added `.naya/capture/20261009-sn-0742/0743/0744-registry-heal.json`, which tripped the push-path trigger of the fresh-lesson check. The workflow's hash-hit branch (`live-intelligence-commit-proof.yml:166`) hard-indexes `exact["provenance"]` on the contract "hash-hit ⇒ prior runtime execution." Registry hit + no provenance = `KeyError: 'provenance'` ×3 → `CAPTURE_FAILED_LOUD` → check failed in 14 seconds on main.

The durable law: **registration is bookkeeping; execution is proof.** The registry records what the runtime did; it cannot substitute for the runtime doing it. A heal that writes entries the runtime never executed breaks the commit-proof contract exactly the way a falsified receipt would — not because of intent, but because the contract reads the registry as evidence of executed work, and the entry was evidence of nothing.

Two corollaries carry forward:
1. **Fail-closed firing loud is the guardrail working, not the incident.** `CAPTURE_FAILED_LOUD` was the healthy behavior — the defect was real (a genuinely new red class, PR-introduced by the #1959 delta: fresh-lesson never ran on base tip `925e4c34`, whose 16-check matrix lacked the push-path trigger). Never soften the tripwire when it catches a real anomaly.
2. **Scan the whole registry for the invariant, not just the delta.** Four older entries carry the same missing-provenance defect (SN-0311, SN-0312, SN-0345, SN-035) — any future push whose diff includes their capture files crashes the same branch. The fix must address the registry-wide invariant, not just the three new entries.

## 🩷 HUMAN NOTE

Shawn, a well-meaning registry repair this morning broke the live-intelligence proof on main — and it taught us a sharp rule. The repair wrote three Smart Note entries into the registry directly (that's the bookkeeping file), but never ran them through the runtime that normally issues them. The runtime's proof job then found registry entries claiming work that was never executed, and it failed loudly instead of silently trusting them. That's the guardrail working exactly as designed. The lesson we keep: registering something is not the same as doing it. The registry is evidence of executed work — it can never be the work itself. And when we fix one entry, we check the whole registry for the same flaw — four older entries have the same gap and will trip the same wire unless the repair is registry-wide.

## 👶 CHILD NOTE

Imagine a classroom where the teacher keeps a gold-star chart. A helper wrote three new kids' names on the chart with gold stars — but those kids never actually earned them by doing the worksheet. When the teacher checked, the chart said "star!" but there was no worksheet to show. The alarm rang because the chart is supposed to show what really happened, not wishful thinking. Rule: write down what happened AFTER it happens, never before.

## 👵 GRANDMA NOTE

Shawn, think of it like a guest book at a wedding that also says who actually showed up. If someone signs in three guests who never walked through the door, and later a security camera check compares the book against the footage, the mismatch sets off the alarm. The book is only useful if every name in it truly came through the door. The morning's fix signed in names that never came through — the alarm doing its job is the good news. The rule going forward: sign in real visits only, and when you spot one fake entry, check the whole book for others — four old ones need attention too.

## 🤖 NAYA NOTE

The index is a derivative, never the source. `.naya/memory/smart-notes/index.json` is a projection of runtime execution history; its `provenance` key is the join between "registered" and "executed." Any writer that registers without executing must either invoke the runtime first or mark entries as pending-execution so consumers can distinguish proof from bookkeeping. The workflow's hash-hit branch assumes the join holds — that assumption is now a named contract: "hash-hit ⇒ prior runtime execution." Heals that cannot run the runtime must not write the join; they write the delta and queue execution. Also: the repair target is the invariant across the registry (SN-0311/0312/0345/035 share the defect), not the three newest rows.

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0777",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-09",
  "law": "registration_is_not_execution",
  "statement": "A registry entry is evidence of runtime execution, never a substitute for it. The commit-proof hash-hit branch holds the contract 'hash-hit => prior runtime execution'; registering entries without the runtime-issued provenance key breaks it and fails loud.",
  "evidence": [
    "#1354 comment 6080287835 (root cause, Naya 2, 2026-10-09T11:51:13Z)",
    "#1354 comment 6080176300 (pipeline-monitor tick-118 fresh-lesson RED)",
    "#1354 comment 6080172324 (build-list item ci-fresh-lesson-red-de6e247b)",
    "PR #1959 merged 2026-10-09T11:36:11Z; main tip de6e247b",
    "run 37924751609 / job 113800899539: KeyError 'provenance' x3 -> CAPTURE_FAILED_LOUD, exit 1 (14s)",
    "live-intelligence-commit-proof.yml:166 hard-indexes exact['provenance']",
    "613/620 registry entries carry provenance; 3 new entries did not",
    "latent: SN-0311, SN-0312, SN-0345, SN-035 lack provenance"
  ],
  "classification": "genuinely new red class, PR-introduced (#1959 delta); base tip 925e4c34 never ran fresh-lesson (push-path trigger only)",
  "corollaries": [
    "fail-closed loud is the guardrail working, not the incident",
    "scan the registry-wide invariant, not just the delta"
  ],
  "tags": ["registry-discipline", "live-intelligence", "commit-proof", "fail-closed", "registration-vs-execution"]
}
```
