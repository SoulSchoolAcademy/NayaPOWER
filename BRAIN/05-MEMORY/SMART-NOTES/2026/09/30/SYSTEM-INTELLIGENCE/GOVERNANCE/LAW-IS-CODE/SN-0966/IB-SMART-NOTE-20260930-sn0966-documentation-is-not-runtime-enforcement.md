# Documentation Alone Is Not Runtime Enforcement — After a Venue Change, Sweep the Code

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0966-documentation-is-not-runtime-enforcement
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 comment 6105463196 (2026-10-11T04:32:38Z) — protocol boot/navigation review REAL FINDING: kernel/protocol/cold_start_gate.py still hardcodes #1354 while live mission state says #2175 is the successor board — "documentation alone is not runtime enforcement." Corroborated by night-shift morning-flags.md (2026-10-11 02:04 PDT) flags #2 and #3, verified against main tip 57e935c1: auto_merge_gate.py (P5) requires intent posted to #1354 (lines 299–302); auto_merge_self_heal.py posts reverts to #1354 (BOARD_ISSUE = 1354, line 32); #1354 has been at GitHub's 2,500-comment hard cap with commenting platform-disabled since 2026-10-10 ~12:21 PDT — so every one of those code paths is silently broken against the live board #2175.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The board moved from #1354 to #2175 — in the docs. But the code never got the memo: the cold-start gate still demands "#1354" as a truth marker, the auto-merge gate still requires merge intent posted to #1354, and the self-heal path still posts reverts to #1354. Since #1354 hit GitHub's 2,500-comment hard cap on 2026-10-10 ~12:21 PDT, posting there is impossible — so all three code paths are dead against the live board, silently. The lesson: **a venue change is not complete when the docs are updated; it is complete when every hardcoded reference to the old venue in code has been found and repointed.** Docs describe; code executes. When the two disagree, the code wins — and here the code was pointing at a wall.

## 🩷 HUMAN NOTE

Imagine the office moves to a new building, and everyone updates the address on the website — but the security system still only opens doors for badges registered at the old building, and the alarm company still sends guards to the old address. The move isn't done because the website says so; it's done when the locks, the alarms, and the guard routes all know the new address. That's what happened here: the team's "address" moved from #1354 to #2175, but three pieces of machinery still had the old address hardcoded. One of them (the cold-start gate) actively demands the old address as proof of truth — which can never be satisfied again.

## 🟣 CHILD NOTE

Imagine your family moves to a new house, and you tell all your friends the new address — but you forget to tell the pizza place, the mailman, and the alarm company. Pizzas keep going to the old house. Nobody lives there anymore. The lesson: when something important moves, you have to update EVERYONE who uses the old address — not just your friends, but the machines and services too. The pizza place (the code) doesn't read your group chat (the docs). It only knows the address it was given.

## 🔵 GRANDMA NOTE

It's like changing your phone number and telling all your friends, but forgetting to update it at the bank, the doctor's office, and the pharmacy. Your friends can reach you; the important services can't — and they fail quietly, without telling you. The discipline the team wrote down: when an important address changes, make a list of every place the old number is written down — especially the machines that act on it without asking — and change every one. "Everyone knows" is not the same as "everything works."

## 🟠 NAYA NOTE

Apply this after ANY identifier or venue change (board number, branch name, issue, URL, constant, environment): (1) **grep the code, not just the docs** — run a repo-wide search for the old value (here: `1354`, `BOARD_ISSUE`) across all languages including workflow files and manifests; the three live instances found tonight (cold_start_gate.py REQUIRED_TRUTH_MARKERS, auto_merge_gate.py lines 299–302, auto_merge_self_heal.py BOARD_ISSUE=1354) were all executable paths, not prose; (2) **code wins over docs in a disagreement** — a manifest that says the new board is #2175 while a gate hardcodes #1354 means the gate's behavior is the truth and the manifest is a wish; never report the migration "done" from the docs side; (3) **silent breaks are the failure mode** — none of these paths errored loudly; they fail-closed or fail-to-nowhere against a capped issue, which looks like "nothing happened" rather than "something is wrong"; treat any hardcoded external venue as a rot risk on every change; (4) **the fix is mechanical, the decision is human** — repointing merge-safety machinery (auto-merge gates) touches law-as-code and needs Shawn's word (morning-flags #3 correctly held it for him); flag it, don't unilateral-fix it. Cousins: SN-0402 (hardcoded "current main" SHAs are snapshots, never currency — same rot class), SN-0549 (re-run the exact failed job before classifying — the sibling discipline of checking the executing thing, not the describing thing).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "stale_hardcoded_venue_after_board_migration",
  "evidence": {
    "finding": "#2175 comment 6105463196 (2026-10-11T04:32:38Z): kernel/protocol/cold_start_gate.py still hardcodes #1354 as a truth marker while live mission state says #2175 is the successor board",
    "corroboration": "night-shift morning-flags.md (2026-10-11 02:04 PDT) flags #2/#3 at main tip 57e935c1: tools/auto_merge_gate.py lines 299-302 requires intent posted to #1354; tools/auto_merge_self_heal.py line 32 BOARD_ISSUE = 1354",
    "cap": "#1354 at GitHub's 2,500-comment hard cap since 2026-10-10 ~12:21 PDT; commenting platform-disabled",
    "consequence": "all three code paths silently broken against the live board #2175 — no loud error, just dead writes",
    "held": "morning-flags #3 held the repoint for Shawn's word (merge-safety machinery = law-as-code = his gate)"
  },
  "rule": [
    "after any venue/identifier change, repo-wide grep for the old value across code, workflows, and manifests — docs don't execute",
    "in a docs-vs-code disagreement, the code's behavior is the truth — never report the migration done from the docs side",
    "treat hardcoded external venues as rot risks: they fail silently (fail-closed / fail-to-nowhere), not loudly",
    "repointing law-as-code machinery is a human-gate decision — flag it, don't unilateral-fix it"
  ],
  "lesson_line": "Documentation alone is not runtime enforcement — a venue change is done only when the code has been swept for the old value."
}
~~~

