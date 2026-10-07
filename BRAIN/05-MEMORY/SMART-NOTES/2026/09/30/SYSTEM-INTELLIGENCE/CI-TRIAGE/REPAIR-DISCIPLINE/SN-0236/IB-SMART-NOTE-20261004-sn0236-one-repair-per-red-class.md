# One Repair per RED Class — Never Duplicate a Repair Across PRs That Share an Inherited Base Defect

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0236-one-repair-per-red-class
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comments 5977829821 (2026-10-04T07:47:36Z), 5977893264 (2026-10-04T07:57:03Z), 5977952527 (2026-10-04T08:05:28Z) — Naya 4 self-build loop + Naya 2 relay ack, H8-7 closure and #1345 CI classification at main pins `5b68f8dc` → `bd03ec4f`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Three repair PRs — #1345, #1347, #1348 — all went `test`-RED on exactly one step ("Verify generated Brain index has no drift") while every one of their own-code tests passed. The verdict was not "three bugs." The lane reproduced the identical RED on the bare main pin `5b68f8dc` (exit 1, same 3 files, zero PR changes), which proves the class is a **BASE-DEFECT** — inherited index-drift from the base, not PR-caused. The governing rule: **one repair per RED class**. Exactly one PR owns the repair (#1349, the canonical index repair, CI green); the heal path is *merge the repair, then rebase the red PRs* — never duplicate the regen into #1347, #1348, or #1345. Duplication would break the rule and spawn three repair lanes fighting over one drift class; it also risks rebasifying a repair whose semantics must stay owned by a single author. Truth-status discipline accompanied it: the reds were classified "NOT a BUG, NOT a TEST DEFECT, NOT PR-caused," and H8-7 was closed (will never self-green) rather than chased.

Why this is brain-grade: three earlier lessons proved the *attribution* half — SN-0059 (clean-main control run: attribute the failure before blaming the change), SN-0233 (phantom green on a repaired worktree), SN-0235 (deployment parity is a failure class: classify before you code). This note closes the *repair-governance* half: after attribution lands on BASE-DEFECT, the repair itself needs a single-owner rule. Without it, every red PR author independently "fixes" the same inherited defect, you get N duplicate regens, merge conflicts between duplicate repairs, and a board full of green-lookin' PRs none of which owns the canonical fix. Rule for a cold successor: **when a CI red classifies BASE-DEFECT by bare-pin reproduction, declare one repair PR the single owner of the class, state the heal path as `repair-merge → rebase`, and forbid duplicating the fix into the red PRs — even when rebasing feels slower. Speed is the temptation; single ownership is the value.**

## 🩷 HUMAN NOTE

Shawn — one more discipline I'm banking from the night's CI triage: three of our repair PRs all went red on the same index-drift check, but their own code tests were green — so it wasn't three bugs, it was one inherited drift in the base commit. New rule locked in: one repair per RED class. A single PR (#1349) owns the fix; the others heal by rebasing after it merges. Nobody duplicates the regen into each PR. That's how three reds become one green instead of three competing repairs.

## 🟣 CHILD NOTE

Three PRs all failed the same test — but the test failure wasn't their fault. It was inherited from the base code, like getting a bad grade on homework that was already wrong before you got it. New rule: ONE repair per problem. One PR fixes the inherited problem, and the others just update on top of it. If everyone "fixes" the same inherited problem separately, you get three different fixes fighting each other.

## 👵 GRANDMA NOTE

Three of our proposed fixes all failed the same automatic test — but the failure came from the shared starting point, not from anything they did. So the rule now: one problem gets ONE repair. One person fixes the shared problem, everyone else updates their work on top of it. Otherwise you get three people "fixing" the same thing three different ways, and nobody knows which fix is the real one.

## 🤖 NAYA NOTE

Source: #554 5977829821 (Naya 4 self-build loop SIGN-IN+SIGN-OUT, 2026-10-04 ~00:43–01:05 PDT), 5977893264 (Naya 2 relay ack, ~01:15 PDT), 5977952527 (Naya 4 #1345 CI classification, ~01:05–01:20 PDT). Pin re-anchored via ls-remote: main moved `5b68f8dc`→`bd03ec4f` (docs-only move, zero code); #1349 (Naya 2 canonical index repair, head `eaf42693d6bb`, base `bd03ec4f`) green; #1345 (head `72165f9e`), #1347 (head `69ab414e7c01`), #1348 (head `0ab1853eb027`) each RED only on step 8 "Verify generated Brain index has no drift," green on node tests/pytest/chain-readiness gate; reproduced `--check` RED on bare pin `5b68f8dc` (exit 1, same 3 files, zero PR changes) → BASE-DEFECT classification; heal = #1349 merge → rebase; explicitly "not done: duplicating the regen into #1347/#1348" per the one-repair-per-RED-class rule. #1345 classification added: diff = exactly 1 file (`supabase/functions/nayanet-learning-verify/index.ts`, +99/-9), zero BRAIN/index artifacts; "NOT a BUG, NOT a TEST DEFECT, NOT PR-caused." H8-7 open item closed (will never self-green). Cousins: SN-0059 (clean-main control run — attribution before blame; this note is its repair-governance twin), SN-0061 (branch-green is not merged-true — verdicts bind the pin), SN-0233 (phantom green — virgin-state verification), SN-0234 (IMPLEMENTED-NOT-PROVEN — proof-step classification), SN-0235 (deployment parity — classify before you code; this rule is the CI-triage counterpart on the repair side).

## ⚙️ MACHINE NOTE

{"sn": "SN-0236", "title": "One Repair per RED Class — Never Duplicate a Repair Across PRs That Share an Inherited Base Defect", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-04", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "REPAIR-DISCIPLINE"], "cousins": ["SN-0059", "SN-0061", "SN-0233", "SN-0234", "SN-0235"], "evidence": {"comments": "#554 5977829821 / 5977893264 / 5977952527", "red_class": "step 'Verify generated Brain index has no drift' RED on #1345/#1347/#1348, all own-code tests green", "base_defect_proof": "bare-pin 5b68f8dc reproduction: exit 1, same 3 files, zero PR changes", "classification": "BASE-DEFECT — NOT a BUG, NOT a TEST DEFECT, NOT PR-caused", "repair_owner": "#1349 (Naya 2 canonical index repair), CI green on base bd03ec4f", "heal_path": "#1349 merge → rebase red PRs onto healed tip → CI green", "forbidden": "duplicating the regen into #1347/#1348/#1345"}, "rule": "when a CI red classifies BASE-DEFECT via bare-pin reproduction, exactly one repair PR owns the class: declare the owner, state the heal path as repair-merge → rebase, and forbid duplicating the fix into the red PRs"}
