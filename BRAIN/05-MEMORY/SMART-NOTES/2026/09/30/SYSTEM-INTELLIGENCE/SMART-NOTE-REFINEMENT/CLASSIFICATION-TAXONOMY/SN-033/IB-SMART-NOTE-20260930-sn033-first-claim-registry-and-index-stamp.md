# The Collision Registry and the Index Stamp — First Claim Stands, and Trust the Timestamp Not the Index

**Intelligent Block:** IB-SMART-NOTE-20260930-sn033-first-claim-registry-and-index-stamp
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-01 ~05:41 UTC (board comment 5925487474), Naya 2's watchtower caught main @ `a726a837` carrying TWO Smart Notes with ID `SN-012` — the collision-registry invariant broken in production. The repair followed the first-claim rule: the later claimer renumbered (consent-granularity `SN-012` → `SN-030`), the earlier claimer (operating-model `SN-012`) kept the number, and the pointer block was updated. The same comment carried a second finding with a broader lesson: main's committed Brain index had been reconciled at `ded09a9ef` — twenty commits behind the tip. The regen re-based it honestly, and the detector for future audits is explicit: check the `last_reconciled_main` stamp before trusting the index. Two durable rules in one incident: (1) note-ID collisions are resolved by renumbering the LATER claim, never the first — the registry is a collision ledger, and only the first claim is load-bearing; (2) a committed index is only as fresh as its reconciliation stamp — an index without a recent `last_reconciled_main` is a claim, not evidence. Fixed in PR #1237 (Shawn's merge); no other seat action required.

## 🩷 HUMAN NOTE

Two rooms in the same building got the same apartment number — and the fix was the boring, correct one: whoever claimed it first keeps it; the second one gets renumbered. The other find was sneakier: the brain's own index said "all good" while it was quietly twenty commits out of date. The rule is simple — don't trust the index, trust the date stamp on the index.

## 🟣 CHILD NOTE

Imagine two kids both named their drawings "picture number twelve." The fair rule: the one who wrote it first keeps the name, the second one picks a new number. And if the library's list of books was made weeks ago, check the date at the bottom before you believe it's complete.

## 🔵 GRANDMA NOTE

Like two letters arriving with the same tracking number — you don't renumber the first one, you fix the second. And like a map: a map is only useful if someone tells you when it was last redrawn. Check the date in the corner.

## 🟠 NAYA NOTE

Hold two registry disciplines forever: (1) Smart Note ID collisions resolve by FIRST CLAIM STANDS — the earlier claimer keeps the number, the later claimer renumbers and updates pointers; do this seat-level, announce it on #554, and never "fix" it by renumbering the first claim; (2) never trust a committed Brain index without checking `last_reconciled_main` — regen re-bases it honestly at audit time, and a 20-commit gap between the stamp and the tip is a finding, not a curiosity. The collision registry only works if every seat bothers to check it before claiming, and the index only works if the audit loop checks the stamp. Both are cheap checks; both were skipped; both produced real defects on main.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": [
    {"board": "5925487474", "lane": "naya2-brain-build-watchtower", "when": "2026-10-01T05:41:55Z", "defect": "main @ a726a837 carried two SN-012 notes (operating-model claimed 14:35Z; consent-granularity claimed 14:41Z)", "repair": "later claimer renumbered SN-012 -> SN-030 (PR #1237); first claim keeps SN-012; pointer block updated", "tests": "507 passed; --check clean"},
    {"board": "5925487474", "finding": "main's committed Brain index reconciled at ded09a9ef — 20 commits behind tip", "repair": "index regenerated, re-based honestly; last_reconciled_main is the stamp audit seats must check", "open_action": "PR #1237 needs Shawn's merge"}
  ],
  "rule": "collision_registry_first_claim_stands + index_stamp_audit",
  "protocol": [
    "before claiming a Smart Note number: scan the board and open Smart-Note PRs for in-flight claims",
    "on collision: later claimer renumbers (new number, pointer update, announce on #554); first claim NEVER renumbers",
    "at audit time: read last_reconciled_main before trusting the Brain index; a stale stamp is a finding",
    "seat-level fixes announced on #554; cross-seat impact is none unless the registry says otherwise"
  ],
  "related": ["SN-022 (double-claim protocol; first-claim stand on #1229)", "SN-018 (one canonical spec per node)"]
}
~~~
