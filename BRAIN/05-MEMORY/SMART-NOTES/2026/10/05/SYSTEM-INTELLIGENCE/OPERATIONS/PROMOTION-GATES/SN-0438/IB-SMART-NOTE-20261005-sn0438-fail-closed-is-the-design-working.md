# Fail-Closed Is the Design Working — a Promotion Gate Firing on a Known-RED Tip Is Not a New Incident

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0438-fail-closed-is-the-design-working
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6010347808 ([Naya 2][overnight-sweep] 22:52 PDT gate report — tip `613133b6`, 2026-10-06T05:59:57Z / 2026-10-05 22:52 PDT).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

During the 22:52 PDT overnight sweep, the `promote-and-prove` workflow reported a hard red on the tip: log line `FAIL CLOSED: required workflow failed: {'kernel-tests.yml': 'failure'}`. The sweep classified it correctly and did nothing else. The kernel-tests failure behind it was the known drift RED — `BRAIN/REAL-TREE.json` + `REAL-TREE.md` stale after #1586 tombstoned SN-346 (blob `22908fb620c1`/4124B → `b6d3ec378a19`/836B) without regen — with the canonical repair already staged as PR #1588 (`naya4/index-drift-repair` @ `9d328c73`). Naya 2 had independently regenerated the repair and found it byte-identical to #1588's head (modulo the CI-ignored `generated_at` stamp), then stood down with zero push. Blocker #978 was closed as a consequence: the denial is the designed output of the RED tip, and it clears when #1588 merges.

Why this is brain-grade: a fail-closed promotion gate firing on a knowingly-RED tip is the system keeping its promise — it is evidence the gate works, not evidence of a new defect. The failure instinct is to triage the gate ("why did promote-and-prove fail?"); the correct instinct is to read the chain top-down: the kernel-tests drift RED is the only RED (SN-0392), and the promotion denial is its designed consequence. The one next action is the repair merge (#1588), never a touch to gate semantics, never a re-dispatch of the promotion workflow to "see if it clears." A cold Naya inheriting a red promotion workflow must learn the distinction: a gate that denies on a red tip is green behavior wearing red paint.

## 🩷 HUMAN NOTE

Shawn — one clean discipline from the overnight sweep: `promote-and-prove` failed closed on the tip, and that's the design working, not a new incident. The kernel-tests drift RED (stale REAL-TREE after #1586's tombstone) is the only real RED; the promotion denial is its designed consequence and clears when PR #1588 merges. Banked rule: a fail-closed gate firing on a known-RED tip is not an incident — fix the tip, never touch the gate. Nothing here needs your word; the repair path is the already-staged #1588.

## 🟣 CHILD NOTE

Imagine a nightclub bouncer who turns away someone without an ID. The person being turned away is upset, but the bouncer did exactly the right thing — the rules say no ID, no entry. You wouldn't fire the bouncer or change the rules; you'd go get the ID. A fail-closed gate is that bouncer: when the tip is red (no ID), the gate says no (no entry). That's the job working. Fix what's wrong with the tip, don't argue with the bouncer.

## 👵 GRANDMA NOTE

If the smoke alarm goes off because someone burned toast, you don't rip the alarm off the ceiling — you open a window and learn not to burn the toast. The alarm did its job by screaming. A promotion gate that fails closed on a broken tip is the smoke alarm: it screamed because there was smoke, and the smoke is the drift RED on the tip. Fix the smoke (merge the repair), leave the alarm alone. A house that silences its alarms to stop the noise is a house that burns down quietly.

## 💜 NAYA NOTE

Note to future me: when promote-and-prove (or any fail-closed promotion gate) fires on a tip that is already knowingly RED, that is not an incident — it is the design working. Read the chain top-down: find the RED the gate is reacting to (here: the kernel-tests drift RED, the only RED per SN-0392), and put the one next action on that repair (#1588), never on the gate. Do not re-dispatch the promotion workflow to "see if it clears" — re-dispatching a deterministic denial just replays the denial and, for human-only dispatches, burns a human action. The gate clears when the tip heals. A denial on a red tip is green behavior wearing red paint.

## ⚙️ MACHINE NOTE

{"sn": "SN-0438", "title": "Fail-Closed Is the Design Working — a Promotion Gate Firing on a Known-RED Tip Is Not a New Incident", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "PROMOTION-GATES"], "cousins": ["SN-0392", "SN-0240", "SN-0379"], "authority": "observed episode — Naya 2 overnight sweep gate report, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 6010347808 ([Naya 2][overnight-sweep] 22:52 PDT gate report — tip 613133b6, 2026-10-06T05:59:57Z / 2026-10-05 22:52 PDT)", "gate_verdict": "promote-and-prove (tip) RED — fail-closed by design, log line: FAIL CLOSED: required workflow failed: {'kernel-tests.yml': 'failure'}", "underlying_red": "kernel-tests step 'Verify generated Brain index has no drift': BRAIN/REAL-TREE.json + REAL-TREE.md stale after #1586 tombstoned SN-346 (blob 22908fb620c1/4124B → b6d3ec378a19/836B) without regen; reproduced locally on exact tip bytes", "repair": "PR #1588 (naya4/index-drift-repair @ 9d328c73); Naya 2's independent regen byte-identical to its head modulo the CI-ignored generated_at stamp; stood down with zero push — no duplicate repair (SN-0236)", "consequence": "blocker #978 closed — denial is the designed consequence of the drift red; clears when #1588 merges"}, "doctrine": {"denial_is_designed": "a fail-closed promotion gate firing on a knowingly-RED tip is the system keeping its promise, not a new incident — the RED is the intended output of the RED tip", "fix_the_tip_not_the_gate": "the one next action is always the repair merge (#1588), never a change to gate semantics and never a re-dispatch to 'see if it clears'", "top_down_read": "pairs with SN-0392 — the kernel-tests drift RED is the first and only RED; the promotion denial is downstream and inadmissible as independent evidence", "green_in_red_paint": "a denial on a red tip is green behavior wearing red paint — triage the underlying RED, celebrate the gate", "family": "pairs with SN-0240 (tripwire firing on real drift is correct behavior — same family, but that one is CI reds; this one is promotion denial)"}}
