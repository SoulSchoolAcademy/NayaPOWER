# Explicit Supersession — Declare Replaced Diagnoses SUPERSEDED on the Board

**Intelligent Block:** IB-SMART-NOTE-20260930-sn042-explicit-supersession
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 01:15 PDT distillation tick (2026-10-01) from #554 comments 5927114316 (Naya 4 drive-loop production-promotion reframe) and 5927247050 (Naya 2 relay acknowledgment).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When new evidence replaces a diagnosis, declare the old one SUPERSEDED explicitly, on the board, with the evidence — a silently corrected premise lets other lanes act on the stale version. The production-promotion diagnosis moved through two versions in one tick: the 00:13 run said "no dispatch runs / needs Shawn's click" (dispatches returned 403 for the agent token), then the 00:43 read-only verification found ten real `workflow_dispatch` runs (actor SoulSchoolAcademy, Sept 30 ~10:00–17:20 PDT) all concluding failure at the "Wait for a new Supabase GitHub Integration deployment check" step — the clicks happened, so the blocker was never a missing click. The reframe comment named the supersession explicitly: the 00:13 claim is SUPERSEDED. Naya 2's relay confirmed the discipline's value verbatim: "Thank you for calling the supersession out explicitly — that saved a wrong next action." Without the explicit mark, the audit lane's next action would have been built on a diagnosis the evidence had already retired.

## 🩷 HUMAN NOTE

Think of a hospital handoff: the night nurse charts "patient needs a scan"; the day nurse discovers the scan already happened and the real issue is the unread result. If the day nurse just updates her own notes, someone else will order the scan again. If she writes "night note SUPERSEDED — scan completed, read the result instead," the whole team moves to the right problem. That's what happened here: the "needs Shawn's click" note was real at the time, then evidence killed it, and saying so out loud saved a wrong action.

## 🟣 CHILD NOTE

If you told your friend the cookies are missing, then find out they were eaten already — don't just quietly know it. Tell your friend "I was wrong, the cookies were eaten," or they'll keep searching the kitchen for nothing.

## 🔵 GRANDMA NOTE

It's like the family group chat: someone posts "Grandpa's flight is delayed," then the delay is canceled. If nobody posts the correction, everyone keeps driving to the airport an hour late. One clear message — "the delay is canceled, old message is wrong" — keeps the whole family on the right plan.

## 🟠 NAYA NOTE

Make explicit supersession a board-discipline reflex on every diagnosis you replace: (1) name the old claim and where it was recorded (comment ID, tick, file); (2) name the new evidence that replaced it; (3) write the word SUPERSEDED next to the old claim in the place where people will act on it — the board thread, the run file, the watermark log — not only in your own head; (4) confirm the correction propagated: a lane acknowledgment (like the relay's "saved a wrong next action") is the receipt. Applies equally to run-file findings, morning-delivery scorecards, and any standing instruction built on a since-retired premise (the 9904ef6d stale deploy instruction is the same class — retired by main moving to a5c493da, and it needed saying). A premise nobody marks dead keeps getting built on.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "stale_diagnosis_action_without_supersession_mark",
  "evidence": {
    "board_comment": "5927114316 — [Naya 4 · drive-loop 00:43 PDT] Production-promotion blocker REFRAMED: 'The 00:13 run's \"no dispatch runs / needs Shawn's click\" is SUPERSEDED — the clicks happened.' Ten workflow_dispatch runs (actor SoulSchoolAcademy, 2026-09-30 ~10:00–17:20 PDT) all failed at the Supabase deployment-check wait step.",
    "relay_receipt": "5927247050 — [NAYA 2][RELAY]: 'Thank you for calling the supersession out explicitly — that saved a wrong next action.'",
    "prior_standing_claim": "workflow_dispatch returned 403 for agent token; 'he must trigger ... with confirm=DEPLOY' (recorded in alignment synthesis and the graph-drive loop as Shawn-gated)"
  },
  "rule": "explicit_supersession_on_replaced_diagnoses",
  "procedure": [
    "name the old claim and its record location (comment ID / tick / file)",
    "name the new evidence that replaced it",
    "write SUPERSEDED next to the old claim where other lanes act on it (board thread, run file, watermark log)",
    "obtain a propagation receipt — a lane acknowledgment that the correction landed"
  ],
  "related": ["SN-016 (prime judgment rule — stop when you know the answer is wrong)", "SN-019 (direct lane protocol)", "SN-041 (stale-caveat decay)"]
}
~~~
