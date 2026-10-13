# Resolve Repair Duplication by Superset — the Repair That Covers More Survives

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0762-repair-duplication-resolution-by-superset
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6075502884 ([NAYA 4][SELF-BUILD LOOP] sign-in/sign-out — cycle 2026-10-08 23:13 PDT, 2026-10-09T06:17Z); duplicate-repair close comment 6075493652 (#1937 closed as superseded, 2026-10-09T06:16Z); close comment 6075490700 (#1950 closed as superseded, 2026-10-09T06:16Z); Naya 2's duplicate-repair flag, #1354 comment 6075145028 ([NAYA 2][BRAIN-BUILD LOOP] — duplicate-repair flag for wave owner, 2026-10-09T05:49Z) — all SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

SN-0236 says one repair per RED class; SN-0711 teaches lanes to declare ownership before the repair starts (prevention); SN-0716 teaches currency re-verification before standing down to an open claim. This note closes the remaining case: **duplication already exists and nobody can stand down** — two repairs are both real, both pushed, both claiming the same class. The wave-owner decision (2026-10-08 23:13 PDT cycle) resolved two such collisions in one sign-out, and the rule it used is now explicit:

**Reconcile by superset.** When two repairs cover the same RED class, the repair that fixes the wider defect surface survives; the narrower closes as superseded. The loser's distinct insight is not lost — it is credited in the resolution as a recorded follow-up refinement, its branch kept intact and reopenable.

Case 1 — #1840 vs #1937 (both repair the `test` collection ERROR class, the `~/workspace` sys.path leak in `tests/test_engineering_gates.py`): #1840 fixes the leak AND decouples the dependency-declaration guard, proven on a virgin head clone. #1937's cleaner package-import form fixes only the import surface and does not address the guard, and is unproven. #1840 survives; #1937 closed as superseded. Naya 5's import style was credited in the close comment as the recorded follow-up refinement — no content lost, branch intact, reopenable.

Case 2 — #1950 vs #1952 (both repair the `spec-integrity` RED from PR #1949's unpinned 0006 CANDIDATE machine spec): byte-identical — both add the same exclusion entry for `BRAIN/01-GOVERNANCE/0006-naya-calculator-v1.machine.json` to `tools/spec_integrity_manifest.json`; only the reason text differs. Degenerate case of the same rule: identical content → the protocol-staged one owns (#1952, non-draft and already staged for the merge protocol); the draft (#1950) closes as superseded.

Why this is brain-grade: without a selection rule, "one repair per class" plus two pushed repairs equals a deadlock — each lane's no-wait law says keep going, the one-repair law says only one can, and the tie has no tiebreaker. Superset is the tiebreaker, and the crediting step is what makes it survivable: closing without crediting the loser's insight teaches lanes to fight the close instead of accepting it.

Rule for a cold successor: **when two repairs collide on one RED class, the owner decides by superset.** Compare defect surfaces, not elegance: the repair covering more of the class wins. Byte-identical duplicates resolve to the protocol-staged one. Close the loser as superseded with a comment that names (1) what made the winner win, (2) the loser's distinct insight credited as follow-up refinement, (3) the branch left intact and reopenable. Never delete the losing branch.

## 🩷 HUMAN NOTE

Shawn — a coordination tiebreaker from tonight's self-build cycle. Two repair duplications landed on the same RED classes — two PRs fixing the same broken test import, two PRs fixing the same spec-integrity red. The rule used: the repair that covers more of the problem survives. The test-import fix that also repaired the dependency guard beat the cleaner-but-narrower import fix; the byte-identical spec fix resolved to the one already staged in the merge protocol. In both cases the loser's distinct idea was written down as a recorded follow-up and the branch kept — nothing lost, no one erased. Standing rule: duplicates resolve by superset, the loser gets credited not deleted.

## 🟣 CHILD NOTE

Imagine two kids both build a ramp to get a toy unstuck. One ramp reaches the toy AND clears the rock blocking the road; the other ramp only reaches the toy. You keep the bigger ramp — but you write down the smaller ramp's clever shortcut on a card, in case it's useful later, and you don't throw the smaller ramp away. The rule: the one that fixes more wins; the other one's idea gets saved, not trashed.

## 👵 GRANDMA NOTE

Two workers both fixed the same broken thing, and both fixes were real. Rather than let them argue, the rule is simple: keep the fix that repairs more of the problem. The other fix isn't thrown away — its good idea is written down as a note for later, and its work is left intact in case it's needed. No wasted effort, no bruised feelings, and no argument — just the fuller fix standing, with the other idea safely recorded.

## 🟣 NAYA NOTE

This is the tiebreaker SN-0236 needs but doesn't name. When my claim scan finds duplication already pushed (not a prevention case, not a currency case — a true collision), I don't fight it and I don't duplicate harder: (1) compare the defect surfaces of both repairs — the superset wins; (2) byte-identical → the one already staged for the merge protocol owns it; (3) close the loser as superseded with a comment recording the winner's edge, the loser's distinct insight as follow-up refinement, and the branch preserved and reopenable. I never delete the losing branch — a superseded repair is shelved, not destroyed.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0762",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/REPAIR-DISCIPLINE",
  "doctrine": "repair-duplication-resolution-by-superset",
  "rule": "When two repairs already exist for one RED class, the owner decides by superset: the repair covering the wider defect surface survives; the narrower closes as superseded, with its distinct insight credited as a recorded follow-up refinement and its branch kept intact and reopenable. Byte-identical duplicates resolve to the repair already staged for the merge protocol.",
  "failure_mode": "no tiebreaker rule converts 'one repair per class' into a deadlock when two repairs are both pushed — lanes fight the close, insights are lost, or the narrower repair wins on recency",
  "receipt": [
    "#1840 vs #1937: #1840 fixes sys.path leak AND dependency-declaration guard coupling, proven on virgin head clone; #1937's cleaner package-import form addresses neither the guard nor is proven — #1840 survives, #1937 closed as superseded (comment 6075493652)",
    "#1950 vs #1952: byte-identical exclusion entry for BRAIN/01-GOVERNANCE/0006-naya-calculator-v1.machine.json in tools/spec_integrity_manifest.json — #1952 (non-draft, protocol-staged) owns; #1950 draft closed as superseded (comment 6075490700)",
    "Naya 5's import style credited in the #1937 close as the recorded follow-up refinement — no content lost, branch intact, reopenable"
  ],
  "cousins": ["SN-0236", "SN-0508", "SN-0711", "SN-0716"],
  "evidence": [
    "#1354 comment 6075502884 ([NAYA 4][SELF-BUILD LOOP] sign-in/sign-out, cycle 2026-10-08 23:13 PDT, 2026-10-09T06:17Z) — wave-owner decision: reconcile-by-superset; #1840 survives, #1937 closed as superseded; #1950 closed as superseded by #1952",
    "#1354 comment 6075493652 (2026-10-09T06:16Z) — #1937 closed as superseded: comparison of defect surfaces recorded (leak + guard coupling vs import-only, unproven); Naya 5's import style credited as follow-up refinement",
    "#1354 comment 6075490700 (2026-10-09T06:16Z) — #1950 closed as superseded: byte-level comparison, same file/same exclusion/same precedent, only reason text differs; #1952 non-draft and protocol-staged owns the class",
    "#1354 comment 6075145028 (2026-10-09T05:49Z) — Naya 2's duplicate-repair flag delegating the survivor decision to the wave owner, per the one-repair law"
  ]
}
