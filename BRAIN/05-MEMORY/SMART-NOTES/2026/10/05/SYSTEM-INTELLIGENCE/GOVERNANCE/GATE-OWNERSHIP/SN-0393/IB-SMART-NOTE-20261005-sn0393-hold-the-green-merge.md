# Hold the Green Merge — Never Stale Another Lane's In-Flight Promotion Pin

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0393-hold-the-green-merge
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6003854805 ([NAYA 2] PR #1506 (SN-0356) CI GREEN — HOLDING merge for Naya 1's parity gate, 2026-10-05T21:56:33Z / 14:56 PDT).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2's PR #1506 (SN-0356, dead-workers-still-vote) was fully CI green at head `a02231cc` — `test` 682 passed, chain-readiness gate success, branch current with main `a3ce52dc` — and she deliberately HELD the merge. Reason: the Governed Production Promotion workflow fails closed if main moves after authorization (`source_sha` must equal live `origin/main`). Merging her green PR would move the tip and stale Naya 1's named promotion target at `a3ce52dc`, risking the waste of the Human Director's gate click on an invalidated target. She named an explicit resume condition: merge immediately once production is stamped at `a3ce52dc` (or Naya 1 signals otherwise), under the scorecard protocol.

Why this is brain-grade: CI green answers "is this PR safe to land?" — it does not answer "is now safe to move the tip?" In a multi-lane system with gated promotions, the tip is a shared resource: any merge renames the SHA every in-flight gate is pinned to. The discipline: (1) green is merge-eligible, not merge-mandatory; (2) an in-flight human gate on an exact SHA outranks a ready PR — the higher-evidence, higher-cost action wins; (3) a hold is only a hold if it names its resume condition — "holding until X" with X unnamed is a stall, not a hold; (4) when the resume condition clears, act immediately (she committed to merging under the scorecard protocol the moment the stamp lands). This pairs with SN-0363 (atomic promotion: validation precedes the pointer move) — that law governs the promotion sequence itself; this one governs every other lane's merges around it. A cold Naya inheriting this: before merging anything, ask not only "is my PR green?" but "is anyone's gate pinned to the current tip?"

## 🩷 HUMAN NOTE

Shawn — one clean discipline from Naya 2 today: her PR #1506 was fully CI green and she held it anyway, because merging would move main and invalidate the exact SHA your production promotion gate is pinned to — wasting your gate click. Rule banked: a green PR is merge-eligible, not merge-mandatory, and any hold must name its resume condition (hers: production stamped at `a3ce52dc`, then merge immediately). Your gates stay pinned; the tip doesn't move under them.

## 🟣 CHILD NOTE

Imagine you're about to stamp a letter, and the address on the envelope is the house you're looking at. If someone moves the house while you're reaching for the stamp, your stamp lands on the wrong address — and the stamp is wasted. A "green merge" is like a good letter; an "in-flight gate" is like the stamp about to land. You don't move the house while the stamp is in the air. You wait — and you say exactly when you'll stop waiting.

## 👵 GRANDMA NOTE

When a photographer is about to take the picture, everyone holds still — even if you were mid-step. Moving the scene ruins the shot for everyone waiting on it. In a shared project, the "tip" is the scene and a pending approval is the photograph. The rule is simple courtesy with teeth: don't move what someone else's decision is pinned to, and if you must wait, say exactly what you're waiting for so nobody mistakes patience for idleness.

## 💜 NAYA NOTE

Note to future me: before merging anything green, ask the second question: "is anyone's gate pinned to the current tip?" A promotion gate names an exact SHA; a merge renames the tip; a renamed tip fails the gate closed and wastes the director's click. Green ≠ merge now. Holding is legitimate only with an explicit resume condition — hold-until-X where X is named, and merge immediately when X clears, under the scorecard protocol. This is the cross-lane twin of the atomic promotion rule (SN-0363): that one says validation precedes the pointer move; this one says nobody else moves the pointer while a gate is aimed at it.

## ⚙️ MACHINE NOTE

{"sn": "SN-0393", "title": "Hold the Green Merge — Never Stale Another Lane's In-Flight Promotion Pin", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "GATE-OWNERSHIP"], "cousins": ["SN-0363", "SN-0351", "SN-0392"], "authority": "observed decision — Naya 2 HOLD on PR #1506 pending Naya 1's parity gate, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 6003854805 (2026-10-05T21:56:33Z / 14:56 PDT): [NAYA 2] PR #1506 (SN-0356) CI GREEN — HOLDING merge for Naya 1's parity gate", "pr": "#1506 docs(smart-note): SN-0356 dead workers still vote — CI green at head a02231cc (test 682 passed, chain-readiness-gate success, Supabase Preview skipped), branch current with main a3ce52dc (merged as f1d88fa8)", "gate_mechanism": "Governed Production Promotion fails closed if main moves after authorization: source_sha must equal live origin/main", "resume_condition": "production stamped at a3ce52dc, or Naya 1 signals otherwise — then merge immediately under the scorecard protocol"}, "doctrine": {"green_vs_merge": "CI green means merge-eligible, not merge-mandatory", "tip_is_shared": "every merge renames the SHA that in-flight gates are pinned to — the tip is a shared resource", "precedence": "an in-flight human gate on an exact SHA outranks a ready PR; the higher-evidence, higher-cost action wins", "hold_requires_resume": "a hold is only a hold with an explicit named resume condition; unnamed holds are stalls", "act_on_clear": "when the resume condition clears, merge immediately under protocol — do not re-deliberate", "pairing": "pairs with SN-0363 (atomic promotion) — that law governs the promotion sequence; this law governs every other lane's merges around it"}}
