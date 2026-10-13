# New Order Mid-Flight: Track Acceptance, Don't Spawn a New Master Plan

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1219-track-acceptance-not-new-master-plan
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 13:08 PDT distillation tick (2026-10-13) from #2175 comment 6153634468 (DIRECTOR 10-POINT ACTIVATION ORDER — incremental acceptance tracker, NOT a new master plan), read from the director's board-window capture on disk.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Shawn's ten-point activation order landed **mid-execution**, while lanes were already in motion. The director did not write a new master plan — he stood up an **incremental acceptance tracker**: ten requested actions × (what exists now / next real proof + named owner / status). The statuses are **evidence states**, never aspirations: BUILT / NOT MERGED, BRANCH ONLY, PARTIAL / NOT PROVEN, DESIGN / UNPROVEN, DRAFT / UNWIRED, BLOCKED ON CONVERGENCE. The owners are the **existing lanes** (Naya 1 integrator, Naya 2 Governance, Naya 4 Activation, Naya 5 Succession) — no new master, no new hierarchy, official mission #2154 still outranks the comment. And one corruption was explicitly blocked: a reviewer's provisional 7.5 candidate-package score was forbidden from becoming the ratified project score — "don't turn my source-level review's provisional 7.5 into a ratified project score." The rule: when a new order arrives mid-flight, don't re-plan — stand up an incremental acceptance tracker against the existing owners with evidence-state statuses, and keep every provisional score labeled provisional until its proof lands. A second plan is a second truth about what the team is doing.

## 🩷 HUMAN NOTE

It's like the director shouting "ten new things!" into a kitchen that's already cooking dinner. The wrong move is tearing up the recipe and starting over — you'd waste the half-cooked food. The right move is taping a checklist to the fridge: what's already in the oven, what's still raw, who's responsible for each dish, and "done" means served, not started. And nobody gets to call dinner "excellent" before anyone's tasted it.

## 🟣 CHILD NOTE

Imagine you're building a big LEGO castle and your dad says "add ten more towers!" You don't smash the castle and start over — you make a list: which towers are already built, which ones still need pieces, who builds which one, and a tower isn't "done" until it's really standing. And you don't let anyone say "my tower plan is great" and count it as finished — plans aren't towers.

## 🔵 GRANDMA NOTE

It's like the boss calling with ten new chores while you're halfway through the laundry. You don't throw the wet clothes back in the hamper — you make a list: done, started, not started, and whose job each is. "Done" means hung on the line, not just decided on. And you don't let anyone grade their own unfinished work as an A — the grade comes when the job is truly finished.

## 🟠 NAYA NOTE

Apply this whenever a human order arrives while work is in motion: (1) **do not write a new master plan** — a second plan is a second truth about what the team is doing; (2) stand up an **incremental acceptance tracker** against the order: one row per requested action with (what exists now / next real proof + named existing owner / status); (3) statuses must be **evidence states** (BUILT/NOT MERGED, BRANCH ONLY, PARTIAL/NOT PROVEN, DESIGN/UNPROVEN, DRAFT/UNWIRED) — never aspirations or design scores; (4) keep the existing ownership (integrator, governance, activation, succession) — the order names owners, it doesn't create hierarchy; (5) **quarantine provisional scores**: a source-level review's provisional score is a candidate-package number, never the ratified project score — say so explicitly in the tracker so no one upgrades it by quoting; (6) the standing mission snapshot outranks the order's comment — link the tracker to it, don't fork it.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "new_order_mid_flight_spawning_parallel_master_plan",
  "evidence": {
    "tracker": "6153634468 (2026-10-13T19:37:06Z): 'DIRECTOR 10-POINT ACTIVATION ORDER — INCREMENTAL ACCEPTANCE TRACKER, NOT A NEW MASTER PLAN. Owner: existing Naya 1 integrator + Naya 2 Governance + Naya 4 Activation (#2533) + Naya 5 Succession (#2535). Current main 582e5e5f05. Official current mission #2154 outranks this issue comment. Baseline (Naya 4 self-assessment as shared): 6.0/10 deployed activation effectiveness; candidate design is stronger, but main and cold proofs still inadequate. Don't turn my source-level review's provisional 7.5 into a ratified project score.'",
    "evidence_states": "per-row statuses in the tracker: BUILT / NOT MERGED (#2533 head ea6c9ef8, test + team-review RED), BRANCH ONLY (AGENTS link on draft branch), PARTIAL / NOT PROVEN (mission snapshot links to still-open #2535), BUILT / DUPLICATED (dos-and-don'ts cards on #2534 and #2535), DESIGN / UNPROVEN (comprehension gate vs hash-verifying protocol_integrity_gate), DRAFT / UNWIRED (3h attunement not per-task), ROUTING (cold-Naya exam to Naya 3 cold-continuity lane)"
  },
  "rule": "new_order_mid_flight_track_acceptance_do_not_spawn_new_master_plan_evidence_states_only_provisional_scores_stay_provisional",
  "procedure": [
    "when a new order arrives mid-execution, do NOT write a new master plan — stand up an incremental acceptance tracker against the order",
    "one row per requested action: (what exists now / next real proof + named existing owner / status)",
    "statuses must be evidence states (BUILT/NOT MERGED, BRANCH ONLY, PARTIAL/NOT PROVEN, DESIGN/UNPROVEN, DRAFT/UNWIRED) — never aspirations or design scores",
    "keep existing ownership and lanes; the standing mission snapshot outranks the order's comment — link to it, don't fork it",
    "quarantine provisional scores explicitly: a source-level review's provisional number is a candidate-package score, never the ratified project score"
  ],
  "related": ["SN-1217 (converge, don't ship both — a second plan is a second truth)", "THE OATH scorecard 6.0/10 baseline (Naya 4 self-assessment, shared)"]
}
~~~
