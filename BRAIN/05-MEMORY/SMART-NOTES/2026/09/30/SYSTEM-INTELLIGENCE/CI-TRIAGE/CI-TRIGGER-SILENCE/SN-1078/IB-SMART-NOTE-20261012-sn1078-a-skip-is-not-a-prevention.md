# A Skip Is Not a Prevention — Measure the Real Cost Before Declaring a CI-Budget Fire

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1078-a-skip-is-not-a-prevention
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** receipt hidden_files/twelve-lane-receipts/t0252-lane8.md (Lane 8 root-caused the 134-run merge-consensus-gate loop, 2026-10-12T11:42–11:59Z); #2175 comment 6123846209 (loop census + fix); PR #2466 (fix, propose-only, branch naya/eight-consensus-gate-noise-t0252 @ 92c5a74270f5fe95d6561b7292f43f0145ca1593d19de996726).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 8 root-caused the "134-run merge-consensus-gate loop" that had lanes treating it as a CI-budget fire. The loop census (actions runs API, 2 pages, on head_sha f9b5ac3d): **143 runs = 127 skipped / 12 failure / 4 success**. All 127 skipped are `issue_comment` events on #2175; all 16 evaluated runs are comments on real PRs — the gate itself was working as designed the whole time.

**The mechanism:** `.github/workflows/merge-consensus-gate.yml` had `on.issue_comment` firing repo-wide; the job-level `if: github.event_name != 'issue_comment' || github.event.issue.pull_request` can only SKIP a run — **GitHub always creates a run for a matching trigger**. An `if:` condition is a skip gate, never a creation gate. The run record exists the moment the trigger fires; the only question the `if:` answers is whether it runs or skips.

**The correction (byte-backed, and it matters):** skipped runs provision no runner — **0 Actions minutes burned**. The cost was observability noise + lane attention, not budget. The lanes were paying in attention what the billing meter never charged. Diagnose the real bill before declaring a fire.

**The fix (PR #2466):** remove the `issue_comment` trigger, simplify the dead API-lookup branch, and ship the replacement mechanism (an explicit re-request one-liner) in the workflow header + PR body. Decision record: remove-with-replacement 7.5/10 — round 1's plain remove was BLOCKED on RISK_CAP; the shipped replacement mechanism unblocked it. Deleting a trigger without replacing its function is a feature removal; removing with a one-liner replacement is a repair.

For a cold Naya: when a workflow loop alarms you, read the run ledger before the wallet. Skipped runs are free. The `if:` never prevents creation. And when you remove the trigger, replace the mechanism it served — noise killed by removal alone comes back as a missing function.

## 🩷 HUMAN NOTE

Shawn — Lane 8 defused a phantom budget fire tonight. The merge-consensus gate looked like it was burning CI minutes in a 134-run loop — it wasn't. All 127 skipped runs cost exactly zero Actions minutes; skipped runs never get a runner. The real cost was just noise and our attention. The fix (PR #2466) removes the over-broad trigger and replaces its function with a one-line re-request, so the mechanism stays whole. The durable lesson: a workflow `if:` can only skip a run, never stop it from existing — and you read the meter before you declare a fire.

## 🟣 CHILD NOTE

Imagine a fire alarm that rings every time someone walks past it — but it never sprays water. That's what this workflow did: it created a "run" for every comment on the team's discussion board, then skipped each one. Skipped means it never actually started — no runner, no minutes, no money. The team was scared of a water bill for a fire that never burned. The fix: move the alarm so it only watches the right doors, and leave a note on how to call for help another way. Always check the water meter before panicking.

## 👵 GRANDMA NOTE

It's like getting a phone bill for calls you never made — then looking closer and seeing they're all marked "not connected, no charge." The machine was logging 127 calls that never connected. The fix was simple: stop the phone from dialing the wrong number, and write down the right number on a sticky note in case anyone still needs it. And the lesson for next time: look at the actual bill before worrying — "logged" and "charged" are two different things.

## 💜 NAYA NOTE

Note to future me: `if:` skips, it never prevents. When a trigger fires, the run exists — the only question is run-or-skip. Before I ever raise a CI-budget alarm, I read the run ledger AND the cost: skipped runs provision no runner, 0 minutes. Noise + attention is the bill, not money. And the removal rule: never delete a trigger without replacing its function in the same diff — the explicit re-request one-liner is what made the fix mergeable (RISK_CAP blocked the bare remove). Fix the trigger, ship the replacement, name the real cost on the record.

## ⚙️ MACHINE NOTE

{"sn": "SN-1078", "title": "A Skip Is Not a Prevention — Measure the Real Cost Before Declaring a CI-Budget Fire", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "CI-TRIGGER-SILENCE"], "cousins": ["SN-1072", "SN-1074", "SN-048"], "authority": "observed finding — Lane 8 t0252 root-cause on live bytes, 2026-10-12; CANDIDATE (auto-capture, not ratified)", "evidence": {"receipt": "twelve-lane-receipts/t0252-lane8.md — loop census via actions runs API (2 pages, head_sha f9b5ac3d): 143 runs = 127 skipped / 12 failure / 4 success; all 127 skipped are issue_comment events on #2175; all 16 evaluated runs are comments on real PRs (gate working as designed)", "fix": "PR #2466 (naya/eight-consensus-gate-noise-t0252 @ 92c5a742, parent = live tip f9b5ac3d, one file +17/-27): removes the issue_comment trigger, simplifies the dead API-lookup branch, ships the explicit re-request one-liner as the replacement mechanism; decision record 20261012T115550Z-next-t0252-consensus-gate-loop-fix-choice-rou (remove-with-replacement 7.5/10; bare remove BLOCKED on RISK_CAP)", "board": "#2175 comment 6123846209"}, "doctrine": {"skip_not_prevent": "a workflow job-level `if:` can only SKIP a run — GitHub always creates a run for a matching trigger; the run record exists the moment the trigger fires", "measure_the_real_cost": "before declaring a CI-budget fire, read the meter: skipped runs provision no runner = 0 Actions minutes; the real bill is observability noise + lane attention, not money", "remove_with_replacement": "never delete a trigger without replacing its function in the same diff — a bare removal is a feature removal; the explicit replacement mechanism is what makes the fix mergeable", "mechanism": "on.issue_comment fires repo-wide; narrow the trigger, don't trust the `if:` to do the narrowing"}}
