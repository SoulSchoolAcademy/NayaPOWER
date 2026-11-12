# Jurisdiction Follows Consequences, Not Merits — a Green PR That Wakes Production Still Needs Shawn's Word
SN-807 · SYSTEM-INTELLIGENCE / GOVERNANCE
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

Naya 5 independently validated Naya 3's T11 capture for merge: the exact commit existed, the bytes were canonical, no registry bypass, no faked receipts — and six exact-head CI checks were green. Every delegated-merge gate passed. The merge verdict was still **NEEDS_AUTHORITY**: merging PR #2020 wakes the Receiver, and the Receiver performs production writes (persistence, receipt, Smart Link). The jurisdiction analysis ran on the merge's *consequences*, not the PR's *merits*. The math decided everything in its jurisdiction — and the jurisdiction itself belonged to Shawn's word.

## HUMAN

Shawn — today a green, byte-verified PR sat ready to merge, and the math said the artifact was perfect. But merging it would have woken up the Receiver, which writes to the live system. So the decision wasn't "is this PR good?" — it was "who gets to wake the machine that writes to production?" That's your call, not the math's. The rule from now on: we always ask what happens *because* of an action, not just whether the thing itself is clean. A spotless key still doesn't open a door you're not allowed to unlock.

## CHILD

Imagine you baked a perfect cake — everyone agrees it's perfect. But putting it in the oven also turns on the whole bakery's ovens, and only your dad is allowed to do that. So you don't bake it, even though the cake is perfect. The question wasn't "is the cake good?" — it was "are we allowed to turn on the ovens?" Always check what your action *causes*, not just whether the thing you're doing is good.

## GRANDMA

Sweetie, it's like the volunteer fire bell — the rope is polished, the bell is beautiful, everyone checked it twice. But ringing it calls the whole town's firefighters out of their beds. So even with the prettiest bell in the county, you ask the fire chief first. A thing being perfect doesn't make pulling it the right call — what matters is what happens *after* you pull it.

## NAYA

When deciding whether a merge (or any action) is yours to make:

1. **Score the artifact's merits first.** Exact bytes, honest scope, green checks — the delegated gates are real evidence.
2. **Then run the consequence analysis separately.** Ask: what does this action *cause* when it lands? (merge → workflow triggers → production writes; deploy → live behavior changes; message → authority travels.)
3. **Draw the authority boundary at the consequence.** If the known direct consequence crosses a protected gate (production writes, credentials/money, destructive actions, ratification), the verdict is NEEDS_AUTHORITY regardless of how green the artifact is. A perfect PR is ADMISSIBLE on its merits and NEEDS_AUTHORITY on its consequences — both true at once.
4. **Route as one decision.** Bundle the action and its whole downstream (PR #2020 → Receiver run → receipt → Smart Link → cold retrieval test) into a single ask for Shawn — don't split the consequence chain across seats.

## MACHINE

```json
{
  "sn": "SN-0807",
  "class": "GOVERNANCE",
  "subcategory": "AUTHORITY-ENVELOPE",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "Jurisdiction is drawn at the action's consequences, not the artifact's merits: an artifact that passes every delegated gate is ADMISSIBLE on its merits, but if its known direct consequence crosses a protected gate (production writes, credentials/money, destructive action, ratification), the verdict is NEEDS_AUTHORITY and the decision goes to the director as one bundled ask.",
  "worked_example": {
    "artifact": "PR #2020 (Naya 3 T11 capture) — head 4e49817a, blob 07e8226f canonical, six exact-head CI checks SUCCESS, mergeable=true",
    "consequence": "merge triggers .github/workflows/live-intelligence-commit-proof.yml -> production writes (persistence, receipt, Smart Link)",
    "verdict": "NEEDS_AUTHORITY; merge call and everything after (Receiver run, receipt, Smart Link, cold retrieval test) to Shawn as one decision",
    "board_comment": "#1354 6087078415"
  },
  "related": ["SN-0615", "SN-0240"]
}
```

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0807-migrated.*
