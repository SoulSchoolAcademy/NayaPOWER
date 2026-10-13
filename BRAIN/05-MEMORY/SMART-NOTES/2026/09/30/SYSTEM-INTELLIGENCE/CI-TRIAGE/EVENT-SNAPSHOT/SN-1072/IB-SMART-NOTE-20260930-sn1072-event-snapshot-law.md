# The Event-Snapshot Law — a Body-Fixing Gate Needs a Synchronize to See the Fix

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1072-event-snapshot-law
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 comment 6122116626 (Lane 9 t0152 verdict, HOLD — 2026-10-12T10:08:22Z); receipt hidden_files/twelve-lane-receipts/t0152-lane9.md; PR #2462 review comment 6122164610 (pin-fix confirmation).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A CI gate that reads the PR body does not read the body — it reads the event snapshot. The receipt-pin gate listens only to `opened`/`synchronize` events, and it evaluates the body as captured in THAT event. Patching the PR body and then re-running the check changes nothing: the re-run replays the original snapshot, and the gate keeps failing against the old text. The fix is two-handed: patch the body AND push a tree-identical empty commit to fire `synchronize`, which delivers the fixed body to the gate in a fresh event. Lane 9 demonstrated it live on #2462: the checker replayed on the original body → `{"verdict":"MISSING"}` (exit 1); on the patched body for the new head → PASS (exit 0); after the synchronize-firing empty commit, the Receipt pin gate went MISSING → SUCCESS on fresh CI bytes. Tree byte-identical, parent pinned — the commit's only job was to be an event.

Why this is brain-grade: the natural response to a body-gate failure is "fix the body, re-run." That response is broken by design — the re-run cannot see the fix. Every minute spent re-running before understanding the snapshot semantics is burned on a phantom red.

For a cold Naya: before you touch anything that a check consumes via the event payload (PR body, PR title, labels — anything the check doesn't fetch from the API at run time), ask: does this check see live state, or the triggering event? If the event — then your edit needs a new event. An empty commit with an identical tree is the honest trigger: it changes nothing but the delivery.

## 🩷 HUMAN NOTE

Shawn — a mechanical lesson from Lane 9's #2462 pin fix: CI gates that read the PR body see only the body's state at the moment the triggering event fired. Editing the body and re-running the check replays the old snapshot — the fix is invisible. The repair is body patch + a tree-identical empty commit to fire `synchronize`, which hands the gate the fixed body. Banked so no one burns a red cycle on this again.

## 🟣 CHILD NOTE

Imagine a teacher who only reads your homework when the bell rings. If you fix your answers after the bell, the teacher keeps grading the old version — your corrections are invisible. The fix is to ring the bell again. The empty commit is the bell: it changes nothing about your work, but it tells the checker to look at the new answers.

## 👵 GRANDMA NOTE

You can't judge today's newspaper by yesterday's delivery. The checker only reads what's handed to it when the bell rings — fix the words, then ring the bell again with an empty commit, and let it read the fresh paper.

## 💜 NAYA NOTE

Note to future me: when a CI check reads the PR body (or anything carried in the event payload rather than fetched live), assume EVENT-SNAPSHOT semantics until proven otherwise. Fix + re-run is a no-op on that class. The repair shape is: patch the body, push a tree-identical empty commit to fire `synchronize`, watch the gate read the fresh snapshot. Verified on #2462: replay on original body MISSING, on patched body PASS, gate MISSING→SUCCESS on fresh CI bytes with byte-identical tree.

## ⚙️ MACHINE NOTE

{"sn": "SN-1072", "title": "The Event-Snapshot Law — a Body-Fixing Gate Needs a Synchronize to See the Fix", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "EVENT-SNAPSHOT"], "cousins": ["SN-0395"], "authority": "observed finding — Lane 9 t0152 on PR #2462, 2026-10-12; CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#2175 6122116626 (2026-10-12T10:08:22Z) — receipt-pin MISSING, fix plan named; t0152-lane9.md — pin replay MISSING on original body / PASS on patched body, gate flipped on fresh CI after synchronize-firing empty commit; PR #2462 comment 6122164610 — pin-fix confirmation", "mechanism": "receipt-pin gate listens only to opened/synchronize events; CI re-runs replay the event snapshot, not live PR state", "failure_mode": "fix-body-then-rerun is a silent no-op — the gate keeps failing against the pre-fix snapshot", "repair_shape": "patch body + tree-identical empty commit to fire synchronize; tree 78b5f5f491d34ac8e7ae562e633098b45c3387d7 byte-identical, head b41a3ffa9 -> a92be1c0"}, "doctrine": {"event_snapshot_law": "a check that consumes event-payload state can only be fixed via a new event", "audit_the_instrument_first": "when a body-gate red survives a body fix, the gate is not stale — the re-run is; pair with SN-0395 (audit what the instrument read)", "honest_trigger": "empty tree-identical commit is a legitimate event trigger, not a cheat — it changes the delivery, not the content"}}
