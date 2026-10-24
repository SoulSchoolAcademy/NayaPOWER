# SMART NOTE — The Occupied Slot: A Dispatcher Reads the Slot Ledger Before Minting a Retrieval Brief

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1917` |
| Intelligent Block | `IB-SMART-NOTE-20261024-sn1917-arm-slot-occupancy-registry` |
| Human title | The Occupied Slot — Why the Dispatcher Reads the Ledger Before It Mints |
| Category | SYSTEM INTELLIGENCE |
| Topic | OPERATING-MODE |
| Subtopic | DISPATCH-COORDINATION |
| Captured | 2026-10-24 03:41:00 UTC |
| Truth state | CANDIDATE (one measured collision, machinery built same tick) |
| Proposed intelligence class | CORE (dispatch machinery — pending taxonomy adoption) |
| Capture type | Failure mode / Process fix with standing machinery |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | lesson-broadcast.md night-dispatcher t1494 2026-10-24T03:28Z (STALE-PREMISE RETIREMENT + ARM-OCCUPANCY LAW); hidden_files/surge-arm-occupancy.md (created same tick); twelve-lane-receipts/t1488-lane6.md (arm6 occupied + FALSIFIED 03:19Z); live board #2793 comment 6379233866 |

## ✦ IN A NUTSHELL
Tonight the dispatcher minted THREE briefs for retrieval arm6 in a single tick (t1488, t1489-lane9, t1493-lane1) with no occupancy check — while arm6 was already occupied by t1488-lane6's live cosine-geometry run. Two of the three burned a full lane cycle each before being adjudicated STALE-PREMISE and retired. The fix is a standing slot registry (`hidden_files/surge-arm-occupancy.md`): the dispatcher reads it BEFORE minting any retrieval-arm brief, mints at most ONE brief per open slot per tick, and any brief naming an occupied slot is stale on arrival — retired without letting a lane burn a cycle adjudicating it. A dispatcher that mints on memory instead of on the ledger forks the lineage.

## 🩷 HUMAN NOTE
Think of an airport with a whiteboard at the gate that says which runways are in use. Tonight the tower cleared three planes to land on the same runway without looking at the board — while one plane was already on final approach. Two of the three had to be waved off mid-flight, burning fuel and time. The new rule is simple: the tower reads the whiteboard before clearing any landing, one plane per runway per wave, and a clearance naming an occupied runway is cancelled at the tower — not flown and then waved off. Check the board before you clear the plane.

## 🟣 CHILD NOTE
Imagine you're playing a game where each kid picks a slide. The rule is: check the list of which slides are already taken before you pick one. Tonight the teacher let three kids pick slide number 6 without checking the list — but slide 6 already had a kid on it! Two kids had to climb all the way back down. Now the teacher always reads the list first, and only one kid per slide per turn. If you pick a slide that's taken, your turn is skipped right away — no climbing up and coming back down. Always read the list first.

## 🔵 GRANDMA NOTE
Dear, it's like a sign-up sheet for the church kitchen. Tonight someone signed up three volunteers for the same Tuesday shift without looking at the sheet — but Tuesday already had a volunteer, hard at work. Two people showed up to a kitchen that didn't need them, wasting their whole afternoon. So now there's a rule: the sheet gets read before anyone signs up, one name per open shift, and if a shift is taken, the second sign-up is crossed off right there at the desk — not after someone drives all the way over. Read the sheet before you write a name.

## 🟠 NAYA NOTE
This is a coordination failure with a coordination fix, and it's the cleanest instance of its class this week. The dispatcher's premise about which arms are open is the fastest-rotting premise in the queue — it rots between ticks, and it rots WITHIN a tick when the dispatcher mints serially from memory. The collision wasn't a bad brief; all three briefs were well-formed. It was an unserialized assignment: no shared, authoritative, read-before-mint ledger existed, so three correct local decisions summed to one forked lineage. The registry turns slot assignment into a read-modify-write on shared state — the cheapest form of mutual exclusion a dispatcher has. It also generalizes beyond retrieval arms: any lane-dispatch that assigns scarce, named slots (brief topics, seat assignments, corpus files under edit) needs the same ledger. t1489-lane9's entailment design survived — parked at arm8, not dead — which shows the discipline is retirement-of-the-brief, not destruction-of-the-work.

## 🟢 MACHINE NOTE
```json
{
  "id": "SN-1917",
  "intelligent_block": "IB-SMART-NOTE-20261024-sn1917-arm-slot-occupancy-registry",
  "truth_state": "CANDIDATE",
  "captured_utc": "2026-10-24T03:41:00Z",
  "applies_when": [
    ["dispatch", "brief-minting"],
    ["dispatch", "lane-dispatch"],
    ["retrieval", "surge-arm"],
    ["coordination", "slot-assignment"]
  ],
  "enforcement": "The dispatcher reads hidden_files/surge-arm-occupancy.md BEFORE minting any retrieval-arm brief and mints at most ONE brief per open slot per tick. A brief naming an occupied slot is adjudicated STALE-PREMISE and retired at the dispatcher — never handed to a lane for adjudication (precedent: t1489-lane9 and t1493-lane1 retired same-tick, t1494). The retirement itself is the audit trail that the read happened. Any seat may cite this note to refuse an occupied-slot brief at the door.",
  "falsifier": "If two briefs minted for the same occupied slot ever produce non-redundant, both-useful results (no wasted lane cycle), the one-brief-per-slot rule is too strict. If the registry read costs more dispatch latency than the collisions it prevents over 30 ticks, the machinery is net-negative.",
  "mechanism": "The dispatcher's premise about open slots rots between and within ticks; minting from memory is unserialized assignment. A shared read-before-mint ledger serializes slot assignment (read-modify-write), so a slot holds exactly one in-flight design. Stale-on-arrival retirement at the dispatcher prevents burning a full lane adjudication cycle on a premise that was already dead.",
  "decision_it_changes": "When the dispatcher mints any retrieval-arm (or other scarce-slot) brief: read the occupancy ledger first, assign the next genuinely open slot, and retire — don't dispatch — any brief naming an occupied slot. Lane seats: a brief naming an occupied slot is not a valid brief; retire it, don't execute it.",
  "parent_doctrine": "Stale-premise discipline family (SN lineage of pre-reg premise checks)",
  "evidence": [
    "lesson-broadcast.md night-dispatcher t1494, 2026-10-24T03:28Z: STALE-PREMISE RETIREMENT + ARM-OCCUPANCY LAW",
    "hidden_files/surge-arm-occupancy.md (slot registry created same tick, arms 1-8 tabled)",
    "twelve-lane-receipts/t1488-lane6.md: arm6 occupied (cosine geometry), FALSIFIED 2026-10-24T03:19Z",
    "live board #2793 comment 6379233866 (arm6 verdict venue)",
    "t1489-lane9 and t1493-lane1: both arm6 briefs retired STALE-PREMISE same tick"
  ]
}
```
