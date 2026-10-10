# Regen enumerates TRACKED files only — stage before regenerating, probe with a local commit

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0880-regen-tracked-files-only
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

`tools/regenerate_brain_index.py` enumerates **tracked** files only. A new BRAIN file sitting untracked in your worktree passes the local `--check` (false green), but CI runs the check on **committed bytes** and fails on index drift. The correct order is: write the file → **stage it** → regenerate the index → **probe with a local commit** before pushing. This corrects the 10-08 "SCHEMA-dir omission" note, which held only for untracked state.

## 🩷 HUMAN NOTE

The brain index regen tool lists only files git is already tracking. So if you create a new BRAIN file, run regen, and then check locally, the local check looks at your working tree — where the file exists — and passes. But CI checks what's actually committed, where the file doesn't exist yet, and the index no longer matches. That is exactly what happened: the first push failed CI step 8 on index drift because the new schema artifact was untracked.

The discipline, in order:

1. Write the new file.
2. `git add` it — stage it **before** regenerating.
3. Run the regen tool (it will now see the file).
4. Probe with a **local commit** and re-run the checks against the committed bytes before pushing.

Untracked-in-worktree `--check` passing means nothing about committed-bytes state. The local commit is the cheap, reversible experiment that tells you what CI will see — one command, zero blast radius, full information.

## 🟣 CHILD NOTE

Imagine a librarian who only writes down books that are already on the shelves. If you leave a new book on the floor, she says "looks fine!" because she can see it — but the official catalog she makes later is missing it, and the inspector finds the mistake. The fix is simple: put the book on the shelf first (stage it), then ask the librarian to write it down (regenerate), then check the catalog yourself before the inspector does (local commit probe).

## 🔵 GRANDMA NOTE

The indexing tool only counts files that are officially registered. Check your new file against what's actually registered, not against what you can see on your desk. Register first, recount, then test with a practice copy before sending the real thing.

## 🟠 NAYA NOTE

This note operationalizes the evidence law at the staging layer and refines the 10-08 SCHEMA-dir note. The causal mechanism is a **two-universe check mismatch**: `--check` evaluates the working tree (universe A); CI evaluates committed bytes (universe B). Any check that runs against universe A cannot certify universe B. The SN-0395 correction sequence — regenerate on the correct basis, stage, probe locally, push — is the standing repair; the new contribution is the ordering constraint (stage before regen) and the explicit scoping of the earlier note to untracked state only.

It also reinforces SN-0493's sibling discipline: assertions must compare the right universes. Mid-run, a byte-parity script asserted the remote blob against the *staged* blob while the regen changes were still unstaged (after a `git reset --soft`) — the assertion fired correctly, and because it fired before any commit or ref change, the failure was free. Assertions that fire before mutation make mistakes cheap; assertions that compare the wrong universe make mistakes invisible.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "lesson_class": "failure_classification_and_process_fix",
  "mechanism": {
    "regen_enumerates": "tracked_files_only",
    "local_check_evaluates": "working_tree",
    "ci_check_evaluates": "committed_bytes",
    "mismatch": "false_green_local_then_ci_index_drift_failure"
  },
  "required_order": [
    "write_new_brain_file",
    "git_add_stage_it",
    "run_regenerate_brain_index",
    "local_commit_probe",
    "re_run_checks_on_committed_bytes",
    "push"
  ],
  "never": [
    "run_regen_before_staging_new_file",
    "trust_untracked_worktree_check_as_committed_bytes_proof",
    "push_without_local_commit_probe_after_index_change"
  ],
  "assertion_discipline": {
    "compare": "matching_universes_staged_vs_working_tree_or_committed_vs_committed",
    "fire_before": "any_commit_or_ref_change",
    "property": "free_failures"
  },
  "corrects": "2026-10-08 SCHEMA-dir omission note (held only for untracked state)",
  "executable_implementation": "tools/regenerate_brain_index.py",
  "pairs_with": ["SN-0395", "SN-0493"]
}
~~~

## 🟢 LEARNING LESSON

The failure was not the regen tool being wrong — it was the operator testing in one universe and shipping in another. Any workflow that stages artifacts (index files, manifests, checksums) has this same shape: the generator's input set (tracked files) and the validator's input set (working tree) and the CI's input set (committed bytes) are three different universes, and only explicit ordering makes them coincide. The local commit probe is the cold-Naya-safe pattern: it produces committed bytes without touching any remote, so CI's verdict is knowable before the push.

## 🧭 KEY DECISIONS / PRINCIPLES

- Stage new files **before** regenerating any index that enumerates tracked files.
- A passing local check on a dirty worktree is not evidence about committed bytes — ever.
- Probe with a local commit (reversible, remote-free) before pushing after any index change.
- Assertions must compare matching universes and fire before any irreversible action.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-0395 — the correction sequence this run executed
- **REFINES** → 2026-10-08 SCHEMA-dir omission note — scopes it to untracked state only
- **PAIRS** → SN-0493 — a decision expires when the tip moves; same spirit: validate on the bytes you will ship
- **ENABLES** → Cold Naya continuity — a re-anchor or index change that a cold successor can execute without learning this the hard way

## 🧾 PROOF / PROVENANCE

~~~json
{
  "smart_note_id": "SN-0880",
  "lineage": "VERIFY-driver run log 2026-10-10 (Naya 4, 01:43-02:35 PDT) -> proactive capture",
  "run_log": "goals/bring-naya-to-life/hidden_files/verify-driver-run-2026-10-10.md",
  "evidence": {
    "branch": "naya4/verify-trial-evidence-v1",
    "pr": "#1766",
    "basis_tip": "fe25661c",
    "failed_push": "1a37a8d6 (CI step 8 index drift — new artifact untracked)",
    "corrected_push": "0853d9b6 (regen after staging, 1234->1235 files, force-pushed linear, CI 8/8 green)"
  }
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Truth state is CANDIDATE: seat-observed and evidence-backed, awaiting director ratification. The tracked-files-only behavior is asserted of `tools/regenerate_brain_index.py` as of 2026-10-10; if the tool's enumeration changes, this note's mechanism section must be revised. The 10-08 note being corrected is identified by description ("SCHEMA-dir omission") — if it exists under a different title, link it here on review.
