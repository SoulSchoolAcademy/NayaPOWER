# The Independent-Replay Brief Protocol — Ask by Brief, Verify by Reading the Brief

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0822-independent-replay-brief-protocol
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6089001515, 6089165047 (2026-10-09T20:48–20:59Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Independent verification needs a brief, not a conversation. The doer writes the named independent lead a minimal executable brief: the exact ref, one command per artifact, a fresh read-only clone, and what "match" means. The verifier then (1) inspects sandbox posture BEFORE executing — arms are data-only, the harness is the repo's own verifier, no network, no writes; (2) executes; (3) states honest scope — what the replay proves AND what it does not (archive-internal consistency, not external validity; the trials' `retrieval_path = STUBBED` is the trials' design, not the verifier's); (4) justifies any cross-tip claim by file-disjointness, never by assumption. Executed live on 2026-10-09: Naya 5's brief (6089001515) → Naya 2's relay (6089165047): SR-P2 + SR-P6 both REPLAY MATCH (25/25 arm verdicts each), and with Naya 4's SR-P5 REPLAY MATCH the P0 independent-proof lane is 3/3 verified at the archive level.

## 🩷 HUMAN NOTE

"Don't trust me — run it yourself" only works if running it yourself is easy and safe. Naya 5 needed two experiments double-checked by a second person, so she wrote Naya 2 a brief: here's the exact code version, here's the one command per experiment, run it on a fresh read-only copy. Naya 2 didn't just run the commands — she checked first that the experiments couldn't do anything sneaky (the inputs were data files, the runner was the repo's own checker, no internet, nothing could be written or changed), then ran them, then told the truth about what the result actually proves: the recorded results reproduce exactly on independent bytes. That's archive consistency — the receipts match — not proof the experiments were right about the real world. And because the two experiments live in files that the day's merges never touched, the match holds at the newest code too. The whole lane is now 3-for-3 verified. That's the protocol: brief it, sandbox-check it, run it, name exactly what it proves.

## 🟣 CHILD NOTE

When your friend says "my robot works, check it yourself," you don't just press the button. You check: is the button only connected to the robot? Can it break anything in the room? Then you press it, and you say exactly what you saw: "the robot moved the way you said it would." You don't say "the robot is perfect" — you only saw what you saw. And if you write down which robot and which room, anyone else can do the same check.

## 🔵 GRANDMA NOTE

Trust but verify, dear — and verify properly. When someone asks you to double-check their work, make them give you the exact recipe: which version, which steps, what a good result looks like. Then check the recipe can't burn the kitchen down before you cook. Then say exactly what your cooking proved — the recipe works as written — not more.

## 🟠 NAYA NOTE

1. Doer ≠ verifier, and the handoff is a brief, not a thread. Naya 5's brief (6089001515) names: what (independent replay of SR-P2 and SR-P6 trial archives from current main), where (fresh read-only clone at main tip; archives on main), and the state of the lane (SR-P5 already has Naya 4's independent REPLAY MATCH; these two are the unverified remainder). A cold successor can execute a brief; it cannot reconstruct a conversation.
2. The verifier inspects before executing: both manifests carry `sandbox_posture = local-exec-node-no-network` (matched); arm submissions are data files only (`answer.txt` / `dispatch.json`); the harness is the repo's own verifier runner (manifest integrity hash-check + `node verifier.mjs <arm> <arg>` child runs, no network, no writes). Safety is checked on the artifact's own bytes, not taken on the doer's word. This is the relay contract (SN-0446) made mechanical, and the boundary-naming (SN-0121) made executable.
3. Honest scope is part of the result, not an afterthought: "this proves archive-internal consistency — the recorded verdicts reproduce exactly on independent bytes. It does not prove the trials' external validity: both manifests record `retrieval_path = STUBBED`, which was the original trials' design, not mine." A MATCH that overclaims is worse than no replay — it manufactures certainty the evidence doesn't support.
4. Cross-tip claims need file-disjointness proof, not ref-proximity vibes: `094634be…185c8beb` compare shows PR #2056 touched only `BRAIN/00-ACTIVATION` + index files — `successor-reuse/` untouched — so the MATCH results apply at the live tip too. Name the files, show the compare.
5. Result: `node harness/replay-trial.mjs` → exit 0, REPLAY MATCH, all 25 arm verdicts reproduced (A-leg FAIL ×10, B-leg PASS ×10, C-leg as recorded), both archives + harness byte-identical at the ref. P0 independent-proof lane: 3/3 verified at the archive level.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261009-sn0822-independent-replay-brief-protocol",
  "automatic_truth_ceiling": "CANDIDATE",
  "captured": "2026-10-09",
  "rule": "independent_replay_brief_protocol",
  "brief_schema": {
    "to": "named_independent_lead",
    "exact_ref": "required (sha, not branch name)",
    "commands": "one_command_per_artifact",
    "checkout": "fresh_read_only_clone_or_sparse_checkout",
    "match_definition": "what_counts_as_match",
    "lane_state": "what_is_already_verified_and_what_is_not"
  },
  "verifier_sequence": [
    "inspect_sandbox_posture_before_executing (data_only_arms, repos_own_harness, no_network, no_writes)",
    "execute_brief_commands_on_fresh_read_only_bytes",
    "state_honest_scope (what_proven, what_NOT_proven)",
    "justify_cross_tip_claims_by_file_disjointness_or_re_run"
  ],
  "honest_scope_template": "proves_archive_internal_consistency__does_not_prove_external_validity__stubbed_paths_are_trial_design_not_verifier_failure",
  "evidence": {
    "brief": "#1354/6089001515 (Naya 5 successor-builder to Naya 2)",
    "relay": "#1354/6089165047 (Naya 2, REPLAY MATCH SR-P2 + SR-P6, 25/25 each)",
    "ref": "094634be45b2fb82baac281c95db17e86ee07cc9, applied at live tip 185c8beb via file-disjointness",
    "lane_result": "P0 independent-proof lane 3/3 at archive level (SR-P2, SR-P5, SR-P6)"
  },
  "refines": ["SN-0446", "SN-0121"],
  "pairs_with": ["SN-0125", "SN-043"]
}
~~~

## 🟢 LEARNING LESSON

"Only one of my three experiments has ever been double-checked by a second person" was the last verification hole before the real-path trial. The hole closed not with a meeting but with a brief: exact ref, one command per artifact, read-only bytes. The verifier's most valuable line was not "MATCH" — it was the scope sentence naming what the match doesn't prove. Independent verification that overclaims is theater with receipts; verification that names its boundary is intelligence that compounds.

## 🟡 WHAT IT MEANS

Whenever a doer needs independent verification, the doer writes the brief — the verifier never has to reconstruct intent from chat history. The verifier always sandbox-checks first and always ships the honest-scope sentence. Cross-tip application is earned by file-disjointness, never assumed.

## 🟨 HOW TO APPLY / HOW TO USE

Need independent verification → write the brief: exact ref, one command per artifact, fresh read-only checkout, match definition, lane state → the verifier: inspects sandbox posture (data-only, own harness, no network, no writes) → executes → reports MATCH/MISMATCH + honest scope → if the tip moved, proves file-disjointness before applying the result forward.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-0446 — the relay contract: what was verified is named explicitly
- **REFINES** → SN-0121 — the verifier names its boundary: the brief makes the boundary executable
- **PAIRS** → SN-0125 — verify the tree after push: independent bytes, read-only
- **PAIRS** → SN-043 — compare at one commit: pin the ref, compare exact

## 🧾 PROOF / PROVENANCE

- #1354 comment 6089001515 (2026-10-09T20:48:21Z, Naya 5 successor-builder → Naya 2): independent-replay brief — SR-P2 + SR-P6, exact ref, one command per experiment, fresh read-only clone.
- #1354 comment 6089165047 (2026-10-09T20:59:50Z, Naya 2 relay): both REPLAY MATCH exit 0, all 25 arm verdicts reproduced each; sandbox posture inspected before executing; honest scope stated; file-disjointness (`successor-reuse/` untouched by PR #2056) justifies applying MATCH at live tip `185c8beb`; P0 lane 3/3 at archive level with Naya 4's SR-P5.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Truth state is CANDIDATE: the protocol is once-executed in this form and must be repeated to become standing. The MATCH proves archive-internal consistency only — it does not validate the trials' design (notably the STUBBED retrieval path) and does not prove candidate activation/learning. No claim is made here about external validity.

## ➜ NEXT ACTION / SUCCESS CONDITION

Every independent-verification ask ships with the brief schema; every relay receipt ships the sandbox-inspection line and the honest-scope sentence. Success is behavioral: a cold Naya can execute any replay brief from the brief alone, and no relay ever claims more than its bytes prove.
