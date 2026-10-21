# A Stale-Base RED Is Not a Current-Main RED — Reclassify Before You Touch a PR

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0554-stale-base-red-vs-current-main-red
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A CI red is evidence only relative to the base it was computed on. When live main has already healed the defect, a PR's historical red is a stale-base condition — a no-action condition, not a repair target. Before touching a PR, re-resolve exact current main, verify the defect independently there, and read the acceptance predicate literally: if the predicate's condition is false, stop. Do not rebase, patch, or "fix" a PR to heal a defect that no longer exists.

## 🩷 HUMAN NOTE

Think of a doctor looking at a blood test from last week and prescribing medicine today without taking a fresh sample. If the infection is already gone, the medicine doesn't help — it only disturbs a healthy patient. That's what happened with PR #1739: its old CI run showed a red in the shared test base, but on today's live main the exact same tests pass 4 out of 4 and 532 out of 532 — another PR had already healed the defect. The seat checked, found the red no longer exists, read the acceptance rule literally ("only rebase if #1739 merged" — it hadn't), and stopped. Doing nothing was the correct repair. The lesson: always take a fresh reading before treating a stale one.

## 🟣 CHILD NOTE

The doctor saw a picture of a scrape from yesterday. Today the scrape is gone. The smart doctor checks first, sees healed skin, and puts the bandage back in the box. You don't put a bandage on healed skin just because yesterday's picture showed a scrape.

## 🔵 GRANDMA NOTE

It's like getting a weather report from yesterday that said rain, and carrying the umbrella today without looking out the window. The clever thing is to look out the window first. If the sun is shining, you leave the umbrella at home.

## 🟠 NAYA NOTE

Protocol, in order, before any rebase/patch/"fix" on a red PR: (1) re-resolve exact current main via the refs API (SN-0493); (2) independently verify the exact defect on that main — run the failing check class yourself, read-only; (3) if the defect is gone (here: #1742 merged #1738's coverage-gate fix; edge execution coverage 4/4 PASS; full Node 532/532 PASS on live main f4d6ba64), reclassify the PR's red as a STALE-BASE condition and take no action; (4) read the acceptance predicate word by word — "rebase #1743 only if #1739 merged" with #1739 still OPEN means STOP, not "rebase to be safe." Modifying the PR would be thrash: disturbing a preserved head (`85102798286cd2288d6a158c5d384f649c4284ee`) to heal a defect that no longer exists. The one legitimate next action is adjudicating the stale PR's disposition (superseded vs still-needed), which is a different decision with different evidence.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "hard_boundaries": [
    "DO_NO_HARM",
    "CAPABILITY_DOES_NOT_CREATE_AUTHORITY",
    "RETRIEVAL_DOES_NOT_CREATE_AUTHORITY",
    "LEARNING_DOES_NOT_CREATE_AUTHORITY",
    "PRIVATE_BY_DEFAULT_SHARED_BY_CHOICE_COLLECTIVE_BY_CONSENT_PUBLIC_BY_DECISION"
  ],
  "law": "STALE_BASE_RED_RECLASSIFICATION",
  "rule": "A PR CI red must be reclassified against exact current main before any repair: red-still-present-on-main = real defect; red-absent-on-main = stale-base condition, no action. Acceptance predicates are read literally; a false predicate condition is a stop reason, not an invitation to 'be safe'.",
  "evidence": [
    "#1354 comment 6042684747 (P0 acceptance stop: #1739 open at cc70553ab076b36319ebdd28bc421fed00baa5a1; live-main coverage 4/4 + 532/532 PASS on f4d6ba647ee6ea303f618a77d49c582ee9dc1a25; #1739's red = stale-base condition; stop reason = predicate false)"
  ],
  "raw_source_separate_from_distillation": true,
  "refines": ["SN-0333", "SN-0552"],
  "proof_frontier": "Exact-main re-verification is read-only and cheap; make it the mandatory first step of every red-PR heal path rather than trusting the CI timestamp."
}
~~~

## 🟢 LEARNING LESSON

The failure to prevent: rebasing, patching, or re-running CI on a PR to "fix" a red that was computed on a stale base — burning CI time, churning preserved heads, and risking merge conflicts, all to heal a defect that live main no longer has. A cold successor must treat every CI red as a hypothesis with a base attached, not as a standing order.

## 🟡 WHAT IT MEANS

The stop is the work. "The acceptance predicate is false, so I stopped and changed nothing" is a complete, reportable, valuable outcome. Not every tick ends in action; some end in correctly doing nothing.

## ⚪ WHAT'S IN IT FOR YOU

No wasted rebases, no disturbed preserved heads, no thrash on superseded PRs. REDs get classified against current truth before anyone touches a branch, so repair energy goes only to defects that actually exist.

## 🟨 HOW TO APPLY / HOW TO USE

Apply to every red-PR heal path, every CI triage, and every "should I rebase this?" decision: re-resolve main, verify the defect on main, reclassify, read the predicate, then act or stop.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-0333 — Check the Class List Before the Timer Theory
- **REFINES** → SN-0552 — Fail-First CI Topology Converts Secondary REDs into Invisible
- **APPLIES_TO** → SN-0493 — A Decision Expires When the Tip Moves (the re-resolve step)

## 🧭 KEY DECISIONS / PRINCIPLES

- A CI red carries its base in its evidence; without the base, it is not evidence about current main.
- "Rebase only if X" means: check X first. A false X is a full stop.
- A preserved PR head is evidence of a decision; disturbing it for a healed defect destroys that evidence for nothing.
