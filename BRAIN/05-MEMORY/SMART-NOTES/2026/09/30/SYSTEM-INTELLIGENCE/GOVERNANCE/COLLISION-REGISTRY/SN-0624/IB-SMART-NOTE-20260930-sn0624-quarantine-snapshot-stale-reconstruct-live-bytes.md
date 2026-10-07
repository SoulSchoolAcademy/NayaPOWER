# A Quarantine Snapshot Is Point-in-Time Evidence — Reconstruct the Collision Registry from Live Bytes Before Triaging

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0624-quarantine-snapshot-stale-reconstruct-live-bytes
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6049942788 ([Naya 4] quarantine list — 29 open ID collisions, 2026-10-08T00:57:15Z); #1354 comment 6050063949 ([Naya 2][PRIORITY-7 SIGN-OUT] collision triage, 2026-10-08T01:08:11Z) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 4's `learn/quarantine.json` snapshot (last seen 2026-10-07T23:55 UTC) listed **29 open ID collisions** and asked for triage. Naya 2 did not triage the list — she **rebuilt the registry from live bytes first**: main @ `823e51c57`, the #1229 branch @ `27bcbd04`, open SN PR heads, date-partition scan, leading zeros normalized. Result: **583 numeric SN IDs on the #1229 branch, zero collisions**; main held only tombstoned and by-design pairs. 28 of the 29 quarantined collisions had already been resolved by dedup agents' renumbering *before* the snapshot was consulted. The quarantine was empty of live collisions. The lesson: **a quarantine list is a triage request, not a verdict.** It decays the moment lanes keep working. Reconstructing from pinned live bytes before acting turned a 29-item renumbering queue into a no-action close — had anyone renumbered from the stale list, they would have invented damage that no longer existed. Verify the list, then triage the world — never the reverse.

## 🩷 HUMAN NOTE

Shawn, the collision quarantine looked like a 29-item emergency — but the list was yesterday's news. Twenty-eight of the 29 "collisions" had already been fixed by the dedup agents before the list was even looked at. Naya 2 ignored the list, rebuilt the real registry from live code at pinned versions, and found zero live collisions. So nothing was renumbered, nothing was broken, and the emergency was a false alarm. The rule going forward: never renumber from a list — always re-check the actual current state first. A stale list is worse than no list, because it looks authoritative.

## 👶 CHILD NOTE

Imagine your teacher gives you a list of 29 typos to fix in a class essay — but the list was printed yesterday, and your classmates already fixed 28 of them overnight. If you fix from the list, you'd be "fixing" things that are already fixed, and you might mess up the good work. The smart move: read the *current* essay first, find the typos that are really still there, and fix only those. Lists go stale — the real thing is always the freshest copy.

## 👵 GRANDMA NOTE

Dear, this is about lists and reality. A list is a photograph — it shows what was true when the picture was taken, not what's true now. When work continues around the clock, photographs age fast. The rule: before you act on any list, hold it up against the real thing and check each item is still real. The effort of checking is always smaller than the cost of "fixing" something that was already fine.

## 🧠 NAYA NOTE

Cold successor: when handed a quarantine list (quarantine.json, a board comment, a spreadsheet — any enumeration of defects), treat it as a *pointer to a triage*, never as the triage. The reconstruction procedure: (1) pin the revisions you will inspect — main HEAD SHA, each relevant branch HEAD SHA, open SN PR heads — naming each SHA in your receipt; (2) enumerate the actual artifacts at those SHAs (git ls-tree / tree API, recursive), normalizing identifiers (leading zeros, case, date-partition prefixes) before comparing; (3) only then classify each listed item as still-live, already-resolved, or never-real. Report the delta between the list and the world explicitly ("28/29 resolved since snapshot at <sha>, 0 live collisions") so the next successor knows the list's age, not just its contents. Never renumber, re-file, or re-close from list state alone. If the list author flags staleness themselves (as Naya 4 did: "this list may be stale"), that is a stronger reason to verify, not a license to act. A quarantine that cannot be reconstructed from live bytes is a rumor with formatting.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0624",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY",
  "doctrine": "A quarantine snapshot is point-in-time evidence; always reconstruct the collision registry from live bytes at pinned SHAs before triaging — never renumber from the list alone.",
  "family": "COLLISION-REGISTRY (SN-0033 first-claim, SN-0167 director-lock, SN-0480 registry) / COUNT-LEDGER-STALENESS",
  "evidence": [
    "#1354 comment 6049942788 (Naya 4: 29 open ID collisions, snapshot 2026-10-07T23:55 UTC, '28 already resolved by dedup agents — this list may be stale')",
    "#1354 comment 6050063949 (Naya 2 triage: rebuilt from main @ 823e51c57, #1229 @ 27bcbd04, open SN PRs; 583 numeric IDs, zero normalized collisions; quarantine empty of live collisions)"
  ],
  "falsifiers": [
    "Renumbering any SN from a quarantine list without re-verifying against live bytes",
    "Treating a quarantine snapshot's count as the current defect count",
    "A triage receipt that cites the list but names no revision SHAs"
  ],
  "applies_to": "all collision/defect quarantine triage on Team Naya lanes"
}
```
