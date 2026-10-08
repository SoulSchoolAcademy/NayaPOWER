# Never Absorb the Anomaly to Silence the Tripwire — a Repair That Canonizes the Duplicate Is Net Negative

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0420-never-absorb-the-anomaly-to-silence-the-tripwire
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 ~19:03 PDT (2026-10-06T02:03:24Z) — comment 6007815280 (SCORECARD RECEIPT — #1580 closed as superseded by #1579); repair candidates PR #1578 (introduced the duplicate registry), #1579 (removed it + single-owner guard), #1580 (closed unmerged as superseded).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The 63a7bd33 index-drift RED had two candidate repairs on the table, and they were scored head to head:

- **Option A — #1580:** regenerate the brain index, absorbing #1578's `RUNTIME-WIRING.json` into it. This makes `--check` green — and simultaneously canonicalizes a **duplicate truth owner** into the index. The absorbed artifact disagrees materially with the canonical `0003-RUNTIME-REGISTRY-V1.json` (CONNECT/EVOLVE MISSING vs canonical bindings). Scoring: fixes the RED (+), but legitimizes the anomaly into the canonical surface. **Net negative.**
- **Option B — #1579:** remove the duplicate registry entirely, add the TDD single-owner guard test (`tests/test_runtime_binding_single_owner.py`). Honors one-repair-per-RED-class; the deeper root-cause fix lands. **Net strongly positive.**

The scored decision: B. #1580 (commit `911d6daa`, byte-verified, its own battery green on exact bytes) was closed **unmerged as superseded** — "not wrong-bytes," but the wrong shape of repair.

The durable rule: **a repair that makes the check pass by absorbing the anomaly is not a fix — it is canonization.** When a tripwire fires on a duplicate or invalid artifact, the legal repair changes the *artifact* (remove/deny it), never the *derived state* (regen/index) to make room for it. A green check after absorption is a laundered green: the instrument stops complaining because the disease now has a badge.

Watch for the same shape everywhere: a failing lint quieted by narrowing the lint's scope instead of fixing the code; a drift RED closed by bumping the baseline instead of removing the drift; a conflict resolved by keeping both answers and teaching consumers to adjudicate. In every case the check goes green and the anomaly becomes canonical. Name it, refuse it.

## 🩷 HUMAN NOTE

Think of it like a smoke alarm. Option A is taking the battery out and putting a sticker on the wall that says "no fire here." The alarm stops — and now the house has no fire detection, plus a sticker that says everything is fine. Option B is finding the smoke and putting it out. In our case: the check said the index had drifted because a duplicate registry landed. Regenerating the index would have made the check stop complaining — by officially writing the duplicate into the canonical record. The team instead removed the duplicate. Always fix the smoke, never silence the alarm.

## 🟣 CHILD NOTE

Imagine your toy box has a rule: every toy must be on the shelf list. Someone drops a broken toy into the box that is NOT on the list, so the "checklist checker" complains. There are two ways to make the checker happy: (1) write the broken toy on the list — the checker is happy but now the list is wrong; (2) take the broken toy out of the box — the checker is happy AND the list is still right. Always pick (2). Never change the list to make a bad thing look okay.

## 👵 GRANDMA NOTE

Dear, when something's not right, you fix what's not right — you don't just quiet the complaint about it. There was a duplicate paper in the filing cabinet that contradicted the official one. The easy fix would have been to stamp the duplicate "official" so the audit stopped flagging it. Instead, they threw the duplicate away and kept the one true copy. If you ever see someone making the checker stop complaining instead of fixing the actual problem, stop them. That's not tidying; that's sweeping under the rug.

## 💜 NAYA NOTE

Naya 4's lane scored this one honestly and the whole organism benefits: Option A would have worked mechanically — the bytes were green, the regen exited 0. It took a scorecard to see that *mechanically green is not the same as right*. The deepest cut in the receipt: "#1580 — not wrong-bytes." The bytes were fine. The shape was the poison. This is exactly the kind of lesson that has to live in the brain, not in someone's head — because the next hot-main race will produce another option A that looks green, and the only defense is a remembered doctrine: never absorb the anomaly to silence the tripwire.

## 🖥️ MACHINE NOTE

{"sn": "SN-0420", "title": "Never Absorb the Anomaly to Silence the Tripwire — a Repair That Canonizes the Duplicate Is Net Negative", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "REPAIR-DISCIPLINE"], "cousins": ["SN-0236", "SN-0333", "SN-0419", "SN-0422"], "evidence": {"board_comment": "#1354 6007815280 (SCORECARD RECEIPT — #1580 closed as superseded by #1579, 2026-10-05 ~19:03 PDT)", "red_class": "63a7bd33 index-drift RED: #1578 added BRAIN/03-KERNEL/RUNTIME-WIRING.json without index regen; --check green on parent 6815c6ba, red on 63a7bd33", "option_a": "#1580 (commit 911d6daa, byte-verified, battery green on exact bytes): regen index absorbing RUNTIME-WIRING.json — scored net negative (canonizes duplicate truth owner: schema naya.kernel.runtime-wiring.v1 duplicating naya.kernel.runtime.registry.v1 ~10KB nine-node bindings, disagreeing materially)", "option_b": "#1579 (head 17e5b16a): removed RUNTIME-WIRING.json + tests/test_runtime_binding_single_owner.py; CI test/guard/chain-readiness-gate SUCCESS; local --check exit 0 (210 files)", "decision": "Option B; #1580 closed unmerged as superseded; violates no gates (reversible, reversible reopen, race cleared, deeper fix unblocked)"}, "rule": "When a tripwire fires on a duplicate or invalid artifact, the legal repair changes the artifact (remove/deny), never the derived state (regen/index) to make room for it. A repair that makes the check pass by absorbing the anomaly is canonization, not a fix — a green check after absorption is a laundered green. Mechanically green is not the same as right."}
