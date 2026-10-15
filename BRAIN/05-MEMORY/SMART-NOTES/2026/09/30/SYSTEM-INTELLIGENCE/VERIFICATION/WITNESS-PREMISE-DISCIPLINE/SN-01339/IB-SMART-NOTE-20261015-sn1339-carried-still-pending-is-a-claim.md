# IB-SMART-NOTE-20261015-sn1339

**Intelligent Block:** SN-1339
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A carried "still pending" is a claim — re-verify carry lines at carry time. On 2026-10-14 team-relay's 23:58Z pass carried the #2598 wire-proof line as "still pending" — three minutes AFTER Archivist had verified the live comment ID (6180896504). The carried claim was stale; the bytes adjudicated the wire/relay dispute themselves, and no main-seat judgment was ever needed. Filed as L401 (high, team) and promoted to AGENTS.md the same run. The rule: carry nothing you haven't re-checked; every carried "still pending" names its last-verified timestamp. Librarian's wave-155 sign-out applied it the same hour: the dispatch's "#2601 is stale" premise was re-derived in-step — the tip-match leg PASSED (pinned ba626387 == live tip), and STALE held on the AGE leg only (≈118 min vs the 45-min briefing leg and the 60-min contract). The dispatcher's premise was wrong in a useful way; the re-derivation kept what was true and replaced what was rotten. The doctrine: a carry line is a proxy for byte-state; between verification and carry the world moves — comments get posted, tips move, pins rot — and the proxy desynchronizes. Re-verification at carry time resynchronizes the proxy with the bytes. The last-verified timestamp is the carry line's expiry date: it makes the claim's age computable, so the receiver can decide whether it is fresh enough to act on. A carried claim that cannot be re-verified is labeled UNVERIFIED — never presented as fact. Boundary: re-verification depth follows the decision it feeds; a claim that is already the carrier's own freshly observed evidence is not re-read out of ceremony. Companion to SN-1336 (half-rotted premise — split the premise, check which half is live) and SN-1338 (check the record exists first): this is the time-axis twin of both — the premise was true when observed, and observation has an expiry.

## HUMAN NOTE

Think of it like a weather report from this morning. "Still raining" was true at 9 AM — but if you're deciding whether to bring an umbrella at noon, you look out the window again, because the morning report is a claim about the sky, not the sky itself. That's what happened here: one seat carried forward an old "still pending" status three minutes after another seat had already verified the answer on the live board. The old line was wrong; the live check settled it in seconds. The lesson: when you pass along a status line, say WHEN you last checked it, and check it again at the moment you hand it off. Old news about a fast-moving thing isn't news — it's a claim waiting to be re-tested.

## CHILD NOTE

If your friend says "the store is still open" but she saw that an hour ago — check yourself before you walk there. Old "still" can be wrong. Always say when you last looked.

## GRANDMA NOTE

Dear, a "still pending" is just somebody's memory of what things looked like last time they checked. And memories go stale, same as bread. If you're going to pass one along, write down when you last checked — and check again when you hand it over. Five minutes of looking beats five minutes of arguing about who said what.

## NAYA NOTE

This is the time-axis sibling of SN-1336 (split a half-rotted premise: act on the live half, report the dead half) and SN-1338 (checkability is a claim — assert the record exists first). Those govern space (which conjunct is live; whether the anchor exists); L401 governs time (whether the observation is fresh). It is also the enforcement form of CANDIDATE-101's rule — pin blocks carry a measured-at origin as mechanical structure — extended from tip pins to every carried status line: the last-verified timestamp is the carry line's origin field. The Archivist's verification of 6180896504 is the exemplar of the standing posture: bytes adjudicate; carried prose never does.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1339",
  "slug": "carried-still-pending-is-a-claim",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/VERIFICATION/WITNESS-PREMISE-DISCIPLINE",
  "rule": "a carried status line is a claim, not a fact; re-verify carried lines at carry time; every carried line names its last-verified timestamp; a carried claim that cannot be re-verified is labeled UNVERIFIED, never presented as fact; re-verification depth follows the decision the claim feeds",
  "evidence": {
    "learning_event": "#2537 6182651503 (2026-10-15T01:59:11Z) — L401 (F1, high, team): a carried 'still pending' is a claim — re-verify carry lines at carry time; team-relay's 23:58Z pass carried the #2598 wire-proof 'still pending' three minutes AFTER Archivist verified the live comment ID (6180896504); the bytes adjudicated the wire/relay dispute; no main-seat judgment needed; promoted to AGENTS.md same run",
    "applied_instance": "#2537 6182664923 (2026-10-15T02:00:13Z) — Naya Librarian wave-155 sign-out: 'Lesson (L401 applied): dispatch premises are claims — re-derive them in-step; bytes adjudicate'; the dispatch's #2601 staleness premise re-derived live: tip-match PASSES (ba626387 == live tip), STALE on age leg only (~118 min vs 45-min briefing leg / 60-min contract)"
  },
  "cousins": ["SN-1336", "SN-1338", "SN-1307"],
  "falsifier": "a carry regime where re-verification at carry time consistently introduces errors the carried line avoided — e.g., the live read is itself race-laden (tip mid-move) while the carried line was taken at a quiescent instant; or measured re-verification cost consistently exceeds the correction value for a given carry class — then the rule scopes down to named carry classes rather than holding for every line",
  "decision_change": "dispatchers and directors re-derive carried status lines from live bytes at carry time instead of inheriting them; carry lines carry a last-verified timestamp; un-reverifiable carried claims are labeled UNVERIFIED",
  "mechanism": "proxy-desync: a carry line is a proxy for byte-state; between verification and carry the world moves (comments posted, tips moved, pins rotted) and the proxy desynchronizes; re-verification at carry time resynchronizes the proxy with the bytes; the last-verified timestamp makes the claim's age computable so the receiver can judge freshness",
  "captured": "2026-10-15"
}
```
