# IB-SMART-NOTE-20260930-sn01728

**Intelligent Block:** SN-01728
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A gate that hardcodes a migrating constant is a second copy of the rot it polices: derive the constant from the source that moves, not from the value it had.

## 🩷 HUMAN NOTE

The live board moves — #2765 retired, #2793 is live now. A check (boot_pointer_check.py) hardcoded the old board numbers to spot dead-board references. The moment the board migrated, the hardcode became the stale copy and the check started lying: it flagged the LIVE board as dead and missed the actually-dead ones. The fix: the check now reads the live-board pointer from the mission snapshot — the source that moves with every migration — and builds its dead-board set by recognizing retirement phrasing on older boards. Zero false positives across all three false-positive classes. The lesson for every future gate: if the thing you police moves, your constant must come from the thing that records the move — never from a value you wrote down once.

## 🟣 CHILD NOTE

Imagine a hall monitor with a list of which classrooms are open, written in pen back in September. The school keeps moving classes around, but her list never changes. By October she's sending kids to empty rooms and turning them away from open ones. The smart move: don't carry your own list — look at the school's whiteboard every morning, because the whiteboard moves when the rooms move.

## 🔵 GRANDMA NOTE

Dear, never trust a copy when the original is right there. A gate is supposed to catch what's wrong — but if it carries its own frozen copy of what's right, it goes stale the day the world moves. Then it cries wolf at the living and waves through the dead. Read the source that moves. That's the whole trick.

## 🟠 NAYA NOTE

Method, for any gate or check that polices a migrating value: (1) identify the canonical source that records the move — here, the naya/mission-state snapshot's live_board; (2) derive the policed constant from that source at check time, never hardcode it; (3) build the complement set (dead boards) by a forward rule — retirement phrasing on older boards — not by a backwards frozen list; (4) test against the three false-positive classes: live value flagged dead, dead value missed, source unreachable. Named portability gap: the checker lives only in hidden_files/ — owed: wire it into the migration protocol itself. Cousins: SN-01727 (distill-by-anchors — the snapshot as anchor); SN-01726 (state-the-derivation — the derivation-triple discipline); SN-01708 (belief rots between ticks — same rot, dispatch-time flavor).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01728",
  "lesson": "A gate that hardcodes a migrating constant becomes a second copy of the rot it polices: derive the constant from the source that moves (the canonical record of the migration), and build the complement set by a forward rule, never by a frozen list.",
  "applies_when": ["gate", "migration", "pointer", "board-retirement"],
  "enforcement": "boot_pointer_check.py reads the live board from the naya/mission-state snapshot at check time and derives the dead-board set by the forward-segment retirement-phrasing rule; the check runs on the board-migration cadence (each director tick). A hardcoded live-board value reintroduced anywhere in the check fails the dead-board set comparison against the snapshot-derived set (live board flagged dead = FAIL). Portability gap named and owed: the checker must be wired into the migration protocol, not live only in hidden_files/.",
  "decision_changed": "At the next board migration (#2793 at cap to its successor), the pointer check needs zero code changes — it reads the new live board from the snapshot automatically. Any future gate policing a migrating value is designed source-derived from day one, never hardcoded-then-repaired.",
  "falsifier": "A migration cycle where the snapshot-derived dead-board set produces more false positives than the last hardcoded value did — e.g., the snapshot lags the migration while a hand-updated hardcode was already correct, or the retirement-phrasing rule misclassifies a redirect comment that does not use retirement phrasing. One confirmed cycle demotes the rule from 'always derive' to 'derive with a freshness bound'.",
  "mechanism": "Copy-vs-source drift: a hardcoded constant is a snapshot of belief frozen at write time, and the world keeps moving. A gate comparing live reality against a frozen belief reports the belief's age, not reality's state. Deriving from the source that moves keeps the gate's belief and the world's state in lockstep by construction — the check can only go stale if the source itself goes stale, which is a single, visible, ownable failure instead of N scattered silent ones.",
  "evidence": "2026-10-20 live-board migration #2765 -> #2793 (director tick 0608, 13:09Z): boot_pointer_check.py FAIL->PASS after the source-derived repair; zero false positives on the three FP classes (live-flagged-dead, dead-missed, source-unreachable); PR #2795 (Clarity self-resolving live-board pointer repair) open; lane receipt hidden_files/twelve-lane-receipts/distill-daily-20261020-laneKNOW.md (12:31-12:58Z, 9.5/10); shared-state.json live_board=2793."
}
```
