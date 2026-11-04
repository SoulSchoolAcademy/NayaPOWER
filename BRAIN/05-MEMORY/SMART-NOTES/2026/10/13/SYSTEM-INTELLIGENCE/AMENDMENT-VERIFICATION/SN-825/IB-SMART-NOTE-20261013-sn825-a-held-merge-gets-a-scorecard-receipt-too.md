# A Held Merge Gets a Scorecard Receipt Too
SN-825 · SYSTEM-INTELLIGENCE / AMENDMENT-VERIFICATION
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

Builder A finished the WO4 decision-seam wiring (82/82 tests green, `tsc --strict` clean, PR #2063 open non-draft) and ran the full 5-part scorecard on the *merge decision itself*: (A) merge now under auto-merge law scored 6.0 — fast, but it would supersede Naya 4's in-flight #1733 without her word; (B) post receipt and HOLD the merge for Naya 4's ack on the #1733 supersede disposition scored 9.0; (C) drop the port and wait scored 6.5. The winner was B: merge HELD, receipt posted, work parked-verified, and one crisp decision assigned to the lane owner — close #1733 as superseded, merge #1733 and rebase the port out, or another call. The scorecard applies to holds, not just merges: verified-parked with a named decision beats a fast merge that tramples a lane. Coordination outranks speed.

## HUMAN

Shawn — a builder finished a real piece of work (the decision seam for WO4, all tests green) and then did something better than merging: they ran the scorecard on the merge decision itself. Merging now would have stepped on Naya 4's in-flight work on the same seam. The math said holding the merge scored 9.0 versus 6.0 for merging fast. So the work is done, verified, parked, and the only open question is Naya 4's call on the older branch. The lesson for the system: a hold gets the same written receipt as a merge — done doesn't mean merged, it means verified and parked with a clear owner for the last decision.

## CHILD

You finish your homework AND check the answers — but you don't hand it in yet, because your teacher is still working on that same worksheet and you don't want to overwrite hers. You leave a note saying "done, ready, just waiting on you." That's smarter than handing it in first.

## GRANDMA

One of the builders did the work perfectly — every test passed — and then stopped instead of filing it, because another builder still had that same drawer open. They wrote down exactly why waiting is the better move and handed the choice to the person who owns the drawer. The machine's rules now say: stopping-on-purpose gets the same careful write-up as going-ahead.

## NAYA

This operationalizes the standing lane-respect directive ("do NOT unilaterally supersede another seat's in-flight work") as a scored merge decision rather than a vague courtesy. Applicability: any verified PR that would supersede or duplicate another lane's open work. The hold receipt must state (1) what is proven (tests, hashes, branch tip), (2) the scored options with the hold option scored honestly, (3) the single decision that belongs to the lane owner with its enumerated alternatives, and (4) a no-wait fallback — the builder moves the moment the word comes. The hold is reversible by construction: nothing merged. Pairs with SN-0493 — the parked PR must re-anchor when the tip moves before any later merge.

## MACHINE

```json
{
  "sn": "SN-0825",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "evidence": [
    "gh:SoulSchoolAcademy/NayaPOWER#1354:6089716930",
    "gh:SoulSchoolAcademy/NayaPOWER#2063",
    "gh:SoulSchoolAcademy/NayaPOWER#1733"
  ],
  "rule": "a held merge receives the same 5-part scorecard receipt as a merged one; verified-parked with a named lane-owner decision beats a fast merge that supersedes in-flight work",
  "scored": {"merge_now": 6.0, "hold_for_lane_owner": 9.0, "drop_and_wait": 6.5},
  "hold_receipt_requires": ["proof of verification", "honestly scored options", "single decision assigned to lane owner with enumerated alternatives", "re-anchor per SN-0493 before any later merge"],
  "do_not": ["do not merge over another lane's in-flight work without their word", "do not treat verified-done as merged"]
}
```

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0825-migrated.*
