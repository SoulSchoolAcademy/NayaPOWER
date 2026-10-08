# Semantic Pass ≠ Machine-Qualified — Qualify Candidate Specs at Two Explicit Bars

**Intelligent Block:** IB-SMART-NOTE-20260930-sn025-two-bar-qualification
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

In one night, the build loop adversarially audited three CANDIDATE node master specs (LAW, ACT, KNOW on PR #1224) against the fail-closed bar, read-only. All three verdicts agree: strong, honest, evidence-grounded semantic CANDIDATEs that FAIL machine-qualification. The same defect classes recur across all three organs: no normative state machine ("Recommended" instead of the lock's CANONICAL one); unmapped output vocabularies (MN-03/MN-04 vs the merged NAYA-KERNEL-ACT/KNOW registry ids; nested ADMISSIBLE over AUTHORIZED); unassigned promotion authorities and unauthored fail-closed parameters (dedup τ left as a fail-open parameter); conflicting-authority resolution rules that don't exist; Prime-1 subordination present in substance but appendix-only; contradictions with the merged schema (e.g., ACT §8's `decision_state` in decision-context JSON, which the RATIFIED V2.1 calculus machine_view does not define at all). The doctrine: semantic soundness and machine-readiness are separate verdicts — qualify every spec at both bars explicitly, never infer the second from the first, and hold the machine-contract delta as a recorded work item until the governing spec merges (Shawn), never authoring the machine layer against an unmerged semantics.

## 🩷 HUMAN NOTE

Three organs, three audits, one pattern: the prose reads well, the ideas are honest and often exactly right against the machine where it cites machine state (KNOW's §§18–20 V2.1 dimensions confirmed exact against `kernel/value_calculus.py`, including the 9.0 bar) — and the spec still cannot be built on, because a machine needs the things prose doesn't say. A transition table that enumerates exactly which state changes are legal. A named writer for every promotion. A number for every threshold, with an author, because an unauthored τ is a fail-open parameter wearing a mask. One output vocabulary mapped to the merged schema, not two parallel ones. The standing rule that emerged: qualifying a spec means delivering TWO verdicts on the record, and "strong CANDIDATE" plus "fails machine bar" is not a contradiction — it is the correct, useful answer. The 8–9-item machine-contract deltas were recorded for the post-merge machine layer, derived from the merged spec only, never as a second semantics. Nothing is authored until #1224 merges.

## 🟣 CHILD NOTE

A story can be great and still not be a recipe. Before you build from someone's plan, check two things separately: does the plan make sense, and does it have every number, name, and rule the machine needs to run it? Both answers go on the report card, and "yes" to the first is never "yes" to the second.

## 🔵 GRANDMA NOTE

A wonderful cake recipe that's missing the oven temperature and the pan size is still a wonderful recipe — and you still can't bake from it. Three of the plans passed the taste test and failed the bake test this week, all in the same places: who does what, what happens exactly when something goes wrong, and what number goes in the box. Write down both grades. And never rewrite the recipe while the original is still being approved — wait until it's settled, then write the machine version from the final text.

## 🟠 NAYA NOTE

Do not collapse "good spec" into "buildable spec." The machine-qualification bar is mechanical, not taste-based: (1) a normative transition table for every state machine, mapped to the governing canonical machine (never "Recommended"); (2) an authority assigned for every promotion and terminal state; (3) every parameter authored with fail-closed defaults — an unauthored threshold is a fail-open parameter; (4) exactly one output vocabulary, mapped to the merged schema, with no nested or unscoped tokens across namespaces; (5) subordination to the governing authority (Ultimate Lock #1222, Prime-1) in the body, not appendix-only; (6) zero contradictions with merged machine state — verify every cited machine fact against the live code before asserting it. Record machine-contract deltas as post-merge work items derived from the merged spec; authoring a machine layer against unmerged semantics creates the second-semantics defect the audits keep finding. All three completed organs (LAW, ACT, KNOW) now await #1224 merge (Shawn) before their machine layers; PROVE/CONNECT/VERIFY/LEARN/EVOLVE still pending.

## 🟢 MACHINE NOTE

~~~json
{
  "domain": "spec_qualification_doctrine",
  "evidence": [
    {"organ": "LAW", "findings": "#1224 comment 5924671205 (board 5924672509)", "verdict": "strong honest semantic CANDIDATE; FAILS machine-qualification", "defects": ["revocation checked after consent (revoked grant can emit AMBIGUOUS, violates 0001 MUST)", "missing consent -> AMBIGUOUS vs 0001 'Consent record missing -> Deny'", "two output vocabularies unmapped; ADMISSIBLE nested over AUTHORIZED", "conflicting-authority precedence rules nonexistent", "schema-required grant_id/actor/action/scope appear 0x", "'Recommended' state machine unmapped to lock's CANONICAL section-7 machine", "no conflict-governance clause subordinating to Ultimate Lock #1222"]},
    {"organ": "ACT", "findings": "board 5924755989 (full findings on #1224)", "verdict": "FAILS machine-qualification", "defects": ["8 fail-closed gaps incl. undefined 'consequential'/'materially' in SHOULD/MUST holes, unbounded timeout-reconcile loops, unnamed malformed-expiry failure state", "6 merged-authority contradictions: MN-03 vs NAYA-KERNEL-ACT; decision_state in decision-context JSON undefined in RATIFIED V2.1 machine_view; two overlapping state enums in main schema", "5 internal inconsistencies; 1 overclaim"]},
    {"organ": "KNOW", "findings": "#1224 comment 5924859903 (board 5924866250)", "verdict": "FAILS machine-qualification bar", "defects": ["8 gaps: no normative transition table; VERIFIED/LEARNED promotion authorities unassigned; unauthored dedup tau (fail-open); consent-revocation propagation missing", "6 contradictions: MN-04 vs NAYA-KERNEL-KNOW; three unmapped epistemic vocabularies; unscoped BLOCKED/UNKNOWN tokens", "evidence-grounded where it cites machine state: RETRIEVAL_ELIGIBLE predicate and V2.1 dims/weights/floors confirmed exact incl. 9.0 bar"]}
  ],
  "machine_bar_checklist": ["normative_transition_table_mapped_to_governing_canonical_machine", "authority_assigned_for_every_promotion_and_terminal_state", "every_parameter_authored_with_fail_closed_defaults", "single_output_vocabulary_mapped_to_merged_schema", "governing_authority_subordination_in_body_not_appendix", "zero_contradictions_with_merged_machine_state_verify_citations_against_live_code"],
  "protocol": ["deliver_two_verdicts_on_record_semantic_AND_machine", "never_infer_machine_readiness_from_semantic_soundness", "record_machine_contract_delta_as_post_merge_work_item", "never_author_machine_layer_against_unmerged_semantics", "derive_machine_layer_from_merged_spec_only"],
  "pattern": "all three completed organs await #1224 merge (Shawn) before machine layers; PROVE/CONNECT/VERIFY/LEARN/EVOLVE pending"
}
~~~
