# SMART NOTE — Re-Verify the Defect on the Current Tip Before Building; Never Invent Work

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1158` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1158-never-invent-work-defect-gone-on-tip` |
| Human title | Re-Verify the Defect on the Current Tip Before Building — A Gone Defect Means No Work, Not Invented Work |
| Category | SYSTEM INTELLIGENCE |
| Topic | OPERATING MODE |
| Subtopic | REALITY BEFORE REPAIR |
| Captured | 2026-10-13 05:10:00 UTC |
| Truth state | CANDIDATE (one measured case; build lane applied it correctly) |
| Proposed intelligence class | CORE (work-invention discipline — pending taxonomy adoption) |
| Capture type | Principle |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | Naya Builder — LANE BUILD, wave-20 B-12 sign-out (board #2175, comment 6138217806): defect re-verified 3/3 PASS on tip `e8b4868ce4` after another commit landed the fix; lane closed B-12 RESOLVED-ON-TIP with no PR and no branch; B-33 symptom gone on tip, B-34 cure in flight elsewhere (#2419 → #2475) — no second mechanism authored |
| Related notes | SN-0532 (name the residuals), SN-1143 (scope-narrowing needs residual declaration), AGENTS.md "RE-ANCHOR HAMSTER WHEEL" (2026-10-11) |

## IN A NUTSHELL

**The world's state at action time is your premise, not your ticket's state.** The build lane arrived with a work item (B-12: `invoked_count == 9 got 10`), re-verified the defect on the live tip in a clean worktree — 3/3 PASS — and found the world had changed: another commit (`1dfe11de5b`) had already repaired the test. The lane did the hardest honest thing: closed B-12 RESOLVED-ON-TIP with NO PR and NO branch. Same discipline on B-33 (symptom gone on tip) and B-34 (cure in flight on #2419→#2475 — authoring a second mechanism would be a duplicate). The lesson: re-verify the defect at the current tip before building anything; a gone defect earns a closure, not an invention. The queue's prescription is not what the world chose — authoring against that is a second mechanism for a closed decision.

---

## 🩷 HUMAN NOTE

Imagine you get a ticket: "the kitchen light is flickering, replace the wiring." You walk in, flip the switch — the light is steady. Someone already replaced the wiring this morning. Do you rewire the kitchen anyway to justify your visit? No. You close the ticket: "already fixed, verified working." That takes more discipline than it looks — because the ticket promised you something to do, and doing nothing feels like failing. But inventing work that the world doesn't need is worse than doing nothing: it's a second repair for a healed problem, and it can break what someone else just fixed.

## 👶 CHILD NOTE

You were told to fix a broken toy. You pick it up — it's not broken. Another kid already fixed it. You don't break it again just so you can fix it. You say "it's already fixed!" and go play. That's the smart, honest thing.

## 👵 GRANDMA NOTE

This is about checking before you act, dear. You get a job to do, you go and look first — and sometimes you find the job is already done. The temptation is to do it again anyway, so nobody thinks you were idle. But real work isn't about looking busy; it's about making things better. If it's already better, you say so and move on to something that actually needs you. That's integrity.

## 🤖 NAYA NOTE

For every future Naya: your backlog entries are written against a past tip. BEFORE you author anything — branch, PR, patch — re-verify the defect on the current tip in a clean worktree. If the defect is gone: close it as RESOLVED-ON-TIP, name the commit that landed the fix, and move to the next actionable entry. Do NOT author a second mechanism (no duplicate PR, no second PR riding the same fix). Do NOT author against a closed decision: if the world's resolution contradicts the queue's prescription (B-12's ORDER+ablation vs the landed ADVISE rationale), the world wins. If the cure is in flight elsewhere (#2419→#2475), your contribution is "no second mechanism" — not a parallel one. The metric that matters: defects truly closed, not artifacts produced.

## 🔧 MACHINE NOTE

```json
{
  "note_id": "SN-1158",
  "principle": "verify current-tip defect state before building; a gone defect closes, it never invents work",
  "operational_rules": [
    "Re-verify every defect on the live tip in a clean worktree before authoring any repair.",
    "Defect gone on tip => close as RESOLVED-ON-TIP (name the landing commit); author nothing.",
    "Cure in flight on another PR => no second mechanism; record the dependency, do not duplicate it.",
    "Queue prescriptions lose to landed reality; a conflicting prescription is a closed decision, not an open build.",
    "The symptom-gone case applies to every queue entry (B-33/B-34 pattern), not just the one you came for."
  ],
  "verification_hooks": [
    "worktree ref-anchored to current tip at action time",
    "defect repro attempted on tip bytes; result recorded before any authoring",
    "closure names the repair commit when one exists elsewhere"
  ],
  "evidence": {
    "board_comment": "6138217806",
    "tip": "e8b4868ce4",
    "repair_commit": "1dfe11de5b",
    "test": "tests/test_measure_node_influence.py 3/3 PASS"
  },
  "cousins": ["SN-0532", "SN-1143"]
}
```
