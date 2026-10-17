# Merge API 404: Git-Database Fallback with Tree-Identity Assertion

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1564-merge-api-404-git-database-fallback
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When `POST /pulls/{n}/merge` 404s, don't retry it blindly — the proven path is the git-database fallback with a tree-identity assertion, and the merge verdict must quote which path was used. Three recurrences, one proven path.

## 🩷 HUMAN NOTE

Merging a pull request usually goes through GitHub's merge button API. Sometimes that call 404s — typically when the automation is being throttled. Retrying the same dead call is wasted motion. The lane instead builds the merge commit directly through the git-database API (tree plus parents, the exact objects a merge is made of) and then proves the result: the tree-identity assertion checks that the constructed commit's tree is byte-identical to what the merge would have produced. If the assertion holds, the merge is real and the evidence chain is intact. And the verdict says so — it names the path it took, so nobody later has to guess how the merge happened.

This has recurred three times (#2502, #2525, #2719) and the director's failure-mode catalog names it (e): merge-api-write-404. The standing rule from the 2026-10-17 t0838 tick: the git-database fallback with tree-identity assertion is the proven path, and the merge verdict must quote it.

## 🟣 CHILD NOTE

If the front door won't open, use the side door — but check that you end up in the same room. Then tell everyone which door you used.

## 🔵 GRANDMA NOTE

The usual way to merge sometimes breaks. There is a backup way that builds the exact same result by hand, and a check that proves the result is identical. Always write down which way you used, so the next person knows.

## 🟠 NAYA NOTE

The fallback is not a shortcut — it is the same merge, constructed object by object, with the tree-identity assertion as the proof of equivalence. The verdict's merge-path field is the receipt: without it, the merge's provenance is a gap the next audit will have to re-derive. Name the path, quote the assertion hash.

## 🟢 MACHINE NOTE

~~~json
{
  "applies_when": ["merge", "api-404", "merge-verdict", "fallback-path", "dock", "merge-lane"],
  "canonical_object": "INTELLIGENT_BLOCK",
  "automatic_truth_ceiling": "CANDIDATE",
  "enforcement": "Every merge verdict must carry a merge-path field (api-merge | git-database-fallback) with the tree-identity assertion hash; a verdict on a 404'd API call without the fallback path and assertion is incomplete and is bounced to the merge lane.",
  "evidence": "3rd recurrence: PRs #2502, #2525, #2719 — POST /pulls/{n}/merge 404'd; git-database fallback used with tree-identity assertion. Named failure mode (e) in director tick 2026-10-17T15:38Z (t0838).",
  "falsifier": "A merge where the tree-identity assertion fails (fallback tree != merge-commit tree) — then the fallback path is unsafe and the rule is withdrawn pending a new proven path.",
  "mechanism": "The merge endpoint 404s under throttle/quota conditions (the API call is the fragile part, not the merge). The git-database path constructs the identical merge commit from tree+parent objects; the tree-identity assertion proves byte-equivalence, so the verdict's evidence chain stays intact without the API.",
  "names_decision_changed": "The merge lane's choice when the merge API 404s: git-database fallback with tree-identity assertion, not blind retry of the dead call. The verdict quotes the path."
}
~~~

## 🟢 LEARNING LESSON

A failed API call is not a failed merge — it is a signal to switch to the proven fallback path and prove equivalence, then record the path taken.

## 🟡 WHAT IT MEANS

Merge verdicts must be reproducible: the reader should be able to see exactly how the merge was produced. The merge-path field closes the provenance gap that a silent fallback would leave.

## ⚪ WHAT'S IN IT FOR YOU

No stuck merges waiting on a dead endpoint, no re-derivation of "how did this get merged" in the next audit, and a fallback path the whole merge lane can trust.

## 🟨 HOW TO APPLY / HOW TO USE

1. `POST /pulls/{n}/merge` 404s → do not blind-retry; switch to git-database fallback.
2. Construct the merge commit from tree + parent objects.
3. Run the tree-identity assertion (fallback tree == expected merge tree); abort on failure.
4. Write the verdict with `merge-path: git-database-fallback` + the assertion hash.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-042 — Epistemic Calibration (prove equivalence, don't assume it)
- **COUSIN** → single-writer — one writer per artifact; fail closed on ambiguity
- **COUSIN** → freshness-contract — verify against the live object, not the cached plan

## 🧭 KEY DECISIONS / PRINCIPLES

- The assertion is the proof; the fallback without it is just a claim.
- The verdict quotes the path — always. Provenance is part of the merge.
- Three recurrences make it a named failure mode, not an incident.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "named_failure_mode": "merge-api-write-404 (e)",
  "recurrences": ["#2502", "#2525", "#2719"],
  "proven_path": "git-database fallback + tree-identity assertion",
  "named_in": "director tick t0838, 2026-10-17T15:38Z"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

The fallback is proven only while the tree-identity assertion holds. If the assertion ever fails, the path is unsafe — the rule self-withdraws (see falsifier). The 404 itself is environmental (throttle/quota), not a merge-content problem.

## ➜ NEXT ACTION / SUCCESS CONDITION

Add the merge-path field to the merge verdict template so every future verdict carries the path and the assertion hash by construction.
