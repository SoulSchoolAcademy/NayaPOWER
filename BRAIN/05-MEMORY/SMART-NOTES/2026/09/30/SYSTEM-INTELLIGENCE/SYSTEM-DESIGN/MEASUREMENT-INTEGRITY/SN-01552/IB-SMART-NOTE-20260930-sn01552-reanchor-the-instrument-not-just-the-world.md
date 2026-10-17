# IB-SMART-NOTE — SN-1552

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/MEASUREMENT-INTEGRITY

## IN A NUTSHELL

The distill that fixes rot in the docs must also distill the rot in the instrument. On 2026-10-17 the distill-daily lane repaired boot rot — activation docs pointing cold Nayas at dead boards (#2537, #2175) — and proved the fix with the machine gate `boot_pointer_check.py`: PASS, no stale pointers. But the gate's own STANDING still named #2641 as the live board; the live board had migrated to #2721 on 2026-10-17 ~06:48Z (announce 6230827986, redirect 6230827688; shared-state.json `live_board` = "2721"). The instrument measuring the world carried a stale twin of the world. The fix landed anyway (the pointed-to boards were the checked files), but the next fix would have started from a lie: a PASS verdict whose premises were wrong. Every fixing pass must re-read its own measuring tool's standing assumptions against live state before trusting the verdict — re-anchor the instrument, not just the world.

## HUMAN NOTE

When you fix something and use a tool to check your fix, don't just check what the tool says — check what the tool *assumes*. Tools have their own little model of how the world is, written down when they were built. If the world moved since then (a board moved, a name changed, a permission shifted), the tool can say "all good" while standing on facts that are no longer true. Before you trust the green light, ask: does this tool know what "correct" means *right now*?

## CHILD NOTE

Imagine you have a spelling-checker that was taught "the capital of the country is Springfield." The capital changed to Riverton, and you wrote an essay saying "Riverton." Your checker would mark it wrong — and if you'd fixed your essay to say "Springfield" just to make the checker happy, you'd be *wrong* and the checker would say *perfect*. Before you believe the checker, make sure the checker learned the right facts!

## GRANDMA NOTE

Dear, it's like a ruler that's gotten shorter in the wash — it'll tell you everything's fine while every measurement is off. When the world changes (and it always does), don't just fix the shelves and trust the old ruler. Measure the ruler against something true first. A crooked measure gives you crooked work, and it will swear it's straight.

## NAYA NOTE

Future Naya (distill lanes, fix lanes, anyone who trusts a machine gate's PASS): an instrument's verdict is only as current as its premises. The 2026-10-17 worked template is the distill-daily run (receipt `twelve-lane-receipts/distill-daily-20261017.md`, commit `bcd14896064d17c988fbc151df2ce5a64dac95ef`, PR #2728, board receipt #2721 comment 6233898379): the gate `boot_pointer_check.py` proved "no stale pointers" PASS while its own STANDING pinned `live_board=2641` — three hours after the migration to #2721. The seat caught it, updated STANDING to `live_board=2721` with migration evidence, and flagged the unilateral edit for director review in the PR body. The standing rule: (1) every machine gate pins each world-fact it measures in its STANDING; (2) every fix run re-reads the instrument's standing world-facts against the live source (shared-state.json `live_board`, or a live GET) BEFORE running the measurement; (3) fail-closed on mismatch. A verdict from an un-re-anchored instrument is not evidence about the world — it's evidence about the instrument's twin of the world. Cousins: SN-0376 (instrument must declare coverage before verdict — blind spots, not premises), SN-0469 (audit the instrument before its verdict — ledger coverage, not standing-fact rot). This note is the missing sibling: the instrument's premises rot, not its scan range.

## MACHINE NOTE

```json
{
  "sn": "SN-1552",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T13:15:00Z",
  "applies_when": [["instrument","standing-facts"],["boot","pointer-gate"],["fix","measuring-tool"]],
  "enforcement": "every machine gate pins each world-fact it measures in STANDING and fails closed when the pinned fact disagrees with the live source at run start (e.g. boot_pointer_check.py diffs its STANDING live_board against shared-state.json live_board / live GET before trusting PASS); a fixing pass re-reads its instrument's standing world-facts against live state before the measurement run — 'be careful' is not an enforcement; the pinned-fact diff is",
  "evidence": ["twelve-lane-receipts/distill-daily-20261017.md (2026-10-17 ~05:40 PDT, Naya Clarity Narzan): gate boot_pointer_check.py PASS with its own STANDING still live_board=2641, three hours after live board migrated to #2721 (announce 6230827986, redirect 6230827688)", "commit bcd14896064d17c988fbc151df2ce5a64dac95ef 'distill-daily: point boot bytes at live board #2721'", "PR https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2728", "board receipt https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2721#issuecomment-6233898379"],
  "falsifiability": "the failure class exists only where the instrument pins world-facts in STANDING instead of re-deriving them per run; a gate that derives its world-facts live every run (or pins nothing) is outside this note's scope — the falsifier is the per-run derivation",
  "decision_change": "changes 'gate says PASS, ship it' to 'gate says PASS AND the gate's standing world-facts match the live source, ship it' — any future verdict consumed from a machine gate first triggers the pinned-fact diff",
  "mechanism": "instruments pin world-facts at author-time in STANDING; world migrations move the fact without touching the instrument; the instrument keeps asserting PASS against its stale twin, so the failure is silent — nobody re-derives the premises because the verdict looks healthy",
  "cousins": ["SN-0376","SN-0469"]
}
```
