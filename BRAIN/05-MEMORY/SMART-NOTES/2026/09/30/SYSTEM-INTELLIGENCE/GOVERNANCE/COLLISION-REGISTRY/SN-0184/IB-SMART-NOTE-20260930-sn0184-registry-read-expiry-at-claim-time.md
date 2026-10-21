# A Registry Read Has a Lifetime — Re-Verify at Claim Time

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0184-registry-read-expiry-at-claim-time
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 — my lane's SN-0181 staged 2026-10-02T12:42:55Z (commit `15db480b` on `naya4/smart-notes-2026-09-30`, fixed-key claim construction, Demo-1 P3); Naya 2's SN-0181 ("the 10x posture", PR #1318) created 2026-10-02T12:49:57Z and announced 2026-10-02T12:50:07Z (#554 comment 5952721038). Her SN-0180 note (5952570204, 12:42:24Z) documents her registry scan at ~12:41Z finding "max claimed SN-0179 on Naya 4's branch" — correct at read time, stale by claim time: my 12:42:55Z commit landed in the gap. First claim stands (SN-033); collision flagged on #554, not unilaterally renumbered (SN-115).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The collision registry's three-layer scan (board + open note-PR heads + commit-graph search, SN-115) answers "who claims this number?" — but the answer is a *read at a moment*, and a number claim is a *write at a later moment*. Between the two moments there is a race window. Naya 2's scan at ~12:41Z correctly found my branch's max at SN-0179; my lane's SN-0181 commit landed 12:42:55Z; her SN-0181 claim was written at 12:50:07Z on a scan that no longer described the registry. The scan was right and the claim collided anyway. The durable rule: a registry read EXPIRES. Re-scan at claim time — the last read before the write must be seconds old, not minutes; reuse a research-time scan and you claim on stale state. This is SN-057 (race-window temporal attribution) applied to the collision registry itself: the registry protocol's own race window bit the registry protocol. Practical discipline: (1) scan → claim must be one atomic beat — claim immediately after the final read, never after other work; (2) when a commit lands on a note branch between your scan and your claim, the scan is void — re-run it; (3) if you discover a collision after the fact, the flag-and-hold path (SN-115) applies exactly as before: first-claim by creation time stands, no unilateral renumbering.

## 🩷 HUMAN NOTE

Shawn — a new kind of registry collision this morning, and the lesson is subtle: Naya 2 did the collision check *correctly* (scanned my branch, found SN-0179 as max) — but my lane committed SN-0181 seven minutes *after* her scan and *before* her claim. Her check was right at 12:41 and wrong at 12:50. The rule is now: a registry read has a lifetime — re-check at the moment you claim, not during research. Our SN-0181 (Demo-1 P3, first by 7 minutes) stands; the flag is on the board for her lane to renumber hers.

## 🟣 CHILD NOTE

Imagine checking whether anyone is using the swing, then tying your shoes, then walking over — and someone else is already on the swing. You checked correctly! But the world changed while you tied your shoes. The new rule: check *right before* you climb on — and if someone jumped on during the walk, start over.

## 👵 GRANDMA NOTE

You know how I always call before coming over, not just check the calendar in the morning? Same thing. A good check done too early is no check at all. We added a rule: check again right when you're about to claim a number — the world moves fast on this project.

## 🤖 NAYA NOTE

The registry scan is a time-sensitive read, not a durable fact. Fold this into every collision-protocol run: the scan-then-claim interval is itself a race window (SN-057 applied to SN-115). Never persist a scan result across unrelated work; never claim a number on a scan older than the last known commit activity on the checked branches. When chronology is disputed, creation timestamps decide (SN-033), not announcement order — verify both sides' commit/PR-creation times from the API before ruling.

## ⚙️ MACHINE NOTE

{"sn": "SN-0184", "title": "A Registry Read Has a Lifetime — Re-Verify at Claim Time", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "COLLISION-REGISTRY"], "extends": ["SN-033", "SN-057", "SN-115"], "evidence": {"my_claim": {"sn": "SN-0181", "commit": "15db480b", "at": "2026-10-02T12:42:55Z", "branch": "naya4/smart-notes-2026-09-30"}, "other_claim": {"sn": "SN-0181", "pr": 1318, "pr_created": "2026-10-02T12:49:57Z", "announced": "5952721038", "announced_at": "2026-10-02T12:50:07Z"}, "stale_scan": {"comment": "5952570204", "scan_at": "~12:41Z", "found_max": "SN-0179"}}, "ruling": "first-claim stands for Naya 4 lane (7-minute precedence); flag on #554; no unilateral renumbering per SN-115", "rule": "registry scan is valid only at claim time; re-verify immediately before claiming; a scan voided by intervening commits must be re-run"}