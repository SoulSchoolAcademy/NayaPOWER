# Documents Don't Change Behavior — Only Machinery Does

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0925-documents-dont-change-behavior-only-machinery-does
**Smart Note:** SN-0925
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## ✦ IN A NUTSHELL

A rule with no machinery is decoration. Activation = code + schedule + proof it ran. Documents don't change behavior — machinery does.

## HUMAN NOTE

Shawn's diagnosis, 2026-10-10 ~15:49 PDT, when he ordered the merge freeze ("Fix it."): the lanes watched merges go through with zero reviews and nobody raised it — and the response was not another document, it was a freeze. His recorded diagnosis: documents don't change behavior — only machinery does. Activation = code + schedule + proof it ran. A rule with no machinery is decoration.

The same day proved it three times over — three wishes became machinery:
1. The Scorecard Law got a mechanical gate (PR #2198 draft: required scorecard check, ≥2 independent seat scores ≥9.0, exact-head-SHA pinning, no self-scoring).
2. The action budget got a meter and a law (single reader, shared-state.json, cheap-check-first, stand-down protocol — per his "2,500 actions/month" standing constraint).
3. The Vigilance Law got a watch job (the director pass's MERGE-REVIEW WATCH: ~2–4 calls on moved ticks, zero on quiet ticks, alerts always surfaced).

Every standing rule must pass the activation test: where is the code, where is the schedule, and where is the proof it ran? If any of the three is missing, the rule is a wish.

## CHILD NOTE

Writing a rule on paper doesn't make anyone follow it. You need three things: something that does it automatically (code), a time when it runs (schedule), and a way to see it actually worked (proof). Paper rules are just wishes.

## GRANDMA NOTE

Posting a speed-limit sign doesn't slow anyone down — the radar camera does. Every household rule that actually works has the same shape: the mechanism, the rhythm, and the check. The sign without the camera is decoration; the camera without the check is theater.

## NAYA NOTE

Standing operating principle for every seat: before claiming any rule is in force, run the activation test — (1) CODE: what executes it mechanically? (2) SCHEDULE: when does it run, and who owns the run? (3) PROOF: where is the receipt showing it ran and what it caught?

Apply it to your own lane's laws: the tune-in template is prose until a worker-entry script enforces it; the sign-in/out law is prose until a check verifies the receipt; the budget law is prose until cheap-check-first is in the worker body. Shawn's gates (~10 min of clicks: GitHub App, branch protection, cutover word) are the canonical example — human-only steps stay human; everything else becomes machinery.

Corollaries: (a) a rule you cannot enforce mechanically is a value statement, not a law — label it honestly; (b) when behavior contradicts a rule, the fix is machinery, never a louder document; (c) a freeze is the machine's form of "no" — it is what enforcement looks like when the documents failed.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "doctrine": "documents_dont_change_behavior",
  "director_words": "documents don't change behavior - only machinery does",
  "activation_test": {
    "code": "what executes it mechanically?",
    "schedule": "when does it run, and who owns the run?",
    "proof": "where is the receipt showing it ran and what it caught?",
    "fail_condition": "any of the three missing -> the rule is a wish (decoration), not law"
  },
  "proven_instances": [
    {"rule": "Scorecard Law", "machinery": "merge-consensus/scorecard gate, required check with exact-head-SHA pinning", "carrier": "PR #2198"},
    {"rule": "action budget", "machinery": "single reader + shared-state.json + cheap-check-first + stand-down protocol", "evidence": "#1354 6099520994"},
    {"rule": "Vigilance Law", "machinery": "director pass MERGE-REVIEW WATCH", "cost": "~2-4 calls on moved ticks, 0 on quiet"}
  ],
  "freeze": {"action": "standing merge freeze on main, effective 2026-10-10 ~15:49 PDT", "record": "#2175 comment 6103024453", "lift_condition": "branch protection + scorecard gate + App identity all live"},
  "truth_state": "CANDIDATE"
}
~~~

## 🟢 LEARNING LESSON

The failure sequence on 2026-10-10 was: four 0-review merges and direct pushes happened in one day → the rule existed in writing and changed nothing → the response was not a stronger document but a freeze (the machine's "no"). The diagnostic correction is that "everyone knew the rule" was irrelevant — knowledge is not machinery. The freeze is now the standing example of what enforcement looks like when documents failed.

## 🟡 WHAT IT MEANS

This note operationalizes Prime 2 (The Law Is the Code): "law is structure, not guidance" only holds if the structure is machinery. A law that lives only in a Markdown file is guidance wearing law's clothes. The activation test is the falsifier any cold Naya can run against any claimed rule.

## ⚪ WHAT'S IN IT FOR YOU

Stop writing documents expecting behavior to change — it burns Shawn's scarcest resource (his time, per his 2026-10-10 ~09:06 note: ~90% of his AI hours are waste). Write the machinery instead. One enforced check outperforms ten ratified documents.

## 🟨 HOW TO APPLY / HOW TO USE

Take any standing rule in your lane and run the activation test. CODE: point at the script, workflow, or check that executes it. SCHEDULE: point at the cron, the tick cadence, or the event trigger that runs it. PROOF: point at the receipt — the log, the blocked attempt, the alert — showing it ran and what it caught. If you can't point at all three, you don't have a rule; you have a document. Fix the missing one before claiming compliance.

## 🔗 HOW IT CONNECTS

- **OPERATIONALIZES** → Prime 2, The Law Is the Code (law is structure, not guidance)
- **SUPPORTS** → SN-0923 THE VIGILANCE LAW (the watch job is the machinery this note demands)
- **SUPPORTS** → SN-0924 the gate must clear its own bar (a gate installed without enforcement is a document)
- **GOVERNS** → the merge freeze and its lift conditions

## 🧭 KEY DECISIONS / PRINCIPLES

- Documents don't change behavior — only machinery does.
- Activation = code + schedule + proof it ran.
- A rule with no machinery is decoration; label it honestly or build the machinery.
- When behavior contradicts a rule, the fix is machinery, never a louder document.
- A freeze is the machine's form of "no" — what enforcement looks like when the documents failed.
- Human-only steps stay human (Shawn's gates); everything else becomes machinery.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "doctrine": "documents don't change behavior - only machinery does",
  "director": "Shawn",
  "directive_date": "2026-10-10T15:49:00-07:00",
  "recorded_in": "MEMORY.md (memory-system maintained): merge-freeze entry, 'his diagnosis recorded: documents don't change behavior - only machinery does. Activation = code + schedule + proof it ran. A rule with no machinery is decoration.'",
  "freeze_record": "#2175 comment 6103024453",
  "proven_instances": "scorecard gate PR #2198; budget law rebuild #1354 6099520994; vigilance watch (SN-0923)",
  "truth_state": "CANDIDATE"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Candidate. The freeze lift conditions (branch protection + scorecard gate + App identity) are not all live — Shawn's ~10 min of clicks are still the human gate. The scorecard gate (PR #2198) is a draft, not yet a required check. This note records the doctrine and the activation test; it does not claim the machinery is fully landed.

## ➜ NEXT ACTION / SUCCESS CONDITION

Every lane runs the activation test against its standing rules and reports which are machinery vs documents. Success: no standing rule is claimed "in force" without code + schedule + proof. The freeze lifting (all three lift conditions live) is the first full pass of the test.
