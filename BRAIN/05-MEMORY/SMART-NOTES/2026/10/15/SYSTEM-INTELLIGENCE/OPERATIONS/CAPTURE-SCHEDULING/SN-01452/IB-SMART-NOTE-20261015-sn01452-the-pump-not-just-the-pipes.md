# The Pump, Not Just the Pipes — Capture Triggers Itself

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01452-the-pump-not-just-the-pipes
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 20:38 PDT smart-note-distillation tick (2026-10-15) by Naya Clarity Narzan from board #2641 comment 6204285333 (Shawn's P0 mission directive, relayed 2026-10-15 ~16:38 PDT) and the open team question 6204269956 on what triggers capture in production.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Capture was workflow_dispatch-only. It ran 14 times Oct 7–10 (2 successes on the 10th), then silence — it never broke, it was never automatic. Shawn named it the P0 mission: the pump, not just the pipes. The objective: capture triggers itself. His recommended shape: put the capture workflow on a schedule — the smallest change that makes capture automatic (runtime loop later, if the math earns it). Acceptance, three tests: (1) scheduled runs fire on their own across a full cycle; (2) Smart Notes land in Supabase with receipts at every handoff, zero human pushes; (3) failures visible on the board with reasons — silence is never the failure mode again. P0 because every downstream piece starves without fresh captures. The dead branches were already closed: capture secrets verified present (NAYA_RUNTIME_EMAIL / NAYA_RUNTIME_PASSWORD), old V7 workflows last ran Sept 5–6 (mostly failed), the October runner's quiet is its own open thread. The remaining open question — schedule, runtime loop, or human — is to be answered through the protocol, with evidence.

## 🩷 HUMAN NOTE

Imagine a water system with perfect pipes but no pump — water only flows when someone carries buckets by hand. It worked fourteen times, then the bucket-carrier stopped coming, and nobody noticed for days. Shawn's order: install the pump. Not a bigger pipe — the pump itself. And wire an alarm, so if the pump stops, everyone hears it instead of discovering it weeks later.

## 🟣 CHILD NOTE

It's like a hamster water bottle that only drips when you squeeze it. The hamster drank 14 times while someone was there to squeeze, then got thirsty when nobody came. The rule says: make the bottle drip by itself — the smallest fix that makes water come on its own. And if it ever stops dripping, a bell should ring, not silence.

## 👵 GRANDMA NOTE

You can have the finest plumbing in the house, but without the pump nothing flows — someone had to carry the water by hand, and when they stopped, the house just quietly went dry. The instruction is to fit the pump so the water comes on its own, and to make sure that if the pump ever fails, it rings a bell instead of failing quietly. Quiet failure is the dangerous kind.

## 🧠 NAYA NOTE

This is the operating doctrine behind every scheduled job in this hive: a capability that only runs when a human pushes it is a demo, not a system. The acceptance triple is the reusable standard — (1) it fires on its own across a full cycle, (2) every handoff carries a receipt, (3) failures are visible with reasons. Notice the hierarchy Shawn implied: the schedule is the smallest change that earns automaticity; the runtime loop waits for the math to justify it. And the dead-branch discipline: verify the secrets exist (closed the "what if they don't exist" branch), name the old workflows' last runs (Sept 5–6, mostly failed) instead of leaving them as rumors, and route the real open question (what SHOULD trigger capture) through the protocol with evidence — not through guessing. When you stand up any background capability, ask: does it have a pump, or just pipes? And if the pump stops, who hears it?

## MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "manual_only_capture_silent_starvation",
  "evidence": {
    "directive": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2641#issuecomment-6204285333 (Shawn's P0 mission: 'the pump, not just the pipes', relayed 2026-10-15 ~16:38 PDT)",
    "team_question": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2641#issuecomment-6204269956 (what triggers capture in production — open; secrets CLOSED/present; October runner's quiet its own open thread)",
    "history": "capture was workflow_dispatch-only; 14 manual pushes Oct 7–10 (2 successes on the 10th), silence since — it never broke, it was never automatic; old V7 workflows last ran Sept 5–6 (mostly failed)",
    "shared_state": "hidden_files/shared-state.json naya2_to_builder (PUMP MISSION entry)"
  },
  "rule": "the_pump_not_just_the_pipes_capture_triggers_itself",
  "decision_changed": "how capture runs: previously workflow_dispatch-only (human pushes); now self-triggering — schedule first (smallest change that makes capture automatic), runtime loop later if the math earns it",
  "falsifier": "scheduled runs either fire on their own across a full cycle (holds) or silence recurs (fails); Smart Notes either land in Supabase with receipts at every handoff (holds) or they don't (fails)",
  "mechanism": "the schedule fires the workflow without human action; receipts at every handoff make the pipeline's progress auditable end-to-end; failures post to the board with reasons — silence is never the failure mode again, so starvation becomes visible within one cycle instead of days",
  "acceptance": ["scheduled runs fire on their own across a full cycle", "Smart Notes land in Supabase with receipts at every handoff, zero human pushes", "failures visible on the board with reasons — silence is never the failure mode again"],
  "related": ["SN-01450 (render from the probe — loud failures, not silent)", "OPERATIONS (capture scheduling)"]
}
~~~
