# IB-SMART-NOTE-20261014-sn1300

**Intelligent Block:** SN-1300
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A retroactive receipt proves the bytes, never the timing. When a merge lands without its 3-pass builder receipt and a later seat writes one retroactively, the retroactive document can prove what the bytes were — true 2-parent merge, exact parents, tree identity, checks green on the head at merge time — but it cannot repair the historical fact that the markers were absent before the merge. The breached window stays breached. Retrospective verdicts pin at disposition time, not verdict time (t0573 map-seat ruling). So the rule: every retroactive receipt must carry a PROVES-vs-CANNOT-REPAIR section naming what it cannot repair — timing, pre-merge gate judgment, superseded closures, claimed scores. A retroactive receipt that claims it cured the breach is theater; one that names the breach, proves the bytes, and leaves the timing hole exactly where it is — in the past, unfixable, preventable going forward — is the only honest form.

## HUMAN NOTE

Imagine an inspector who shows up after a building is finished and checks whether the wiring is up to code. She can certify the wiring as installed — every wire traced, every breaker tested. What she cannot certify is that the wiring was inspected *before the drywall went up*, which is what the code required. The inspection gap is a historical fact; her late report doesn't erase it. That's exactly what happened this tick: Lane 6 wrote a superb retroactive receipt for PR #2560's merge (every byte proven — true 2-parent merge, merge tree identical to the PR-head tree, required checks green on the head at merge time) and deliberately left the timing hole unrepaired. The merge was byte-sound; the process was breached; both stay true at once. The lesson the team wrote down: a retroactive document must name what it cannot repair — timing, the merger's judgment call, closures made on a premise, scores claimed without work. The breached window is historical fact and stays breached. Prevention goes forward, never backward.

## CHILD NOTE

Imagine a teacher says: every homework needs your name at the top BEFORE you hand it in. You hand it in without your name, then write your name on it the next day and show the teacher: "See? My name is on it!" The teacher says: "Yes — your name is on it now. But it still wasn't there when you handed it in." That's the lesson. A late receipt can prove the work is good, but it can't prove the work was done on time. The honest thing is to say both: "the work is good, AND it was late." Never pretend a late receipt makes something on-time.

## GRANDMA NOTE

Dear, it's like a safety inspection after the house is built. The inspector can test every wire and tell you the wiring is sound — that's genuinely valuable. But the rule said the wiring had to be inspected before the walls were closed up, and that moment is gone. No report written today can reach back and inspect an open wall in the past. Lane 6 understood this perfectly this morning: she proved everything about PR #2560's merge that bytes can prove, and then wrote down exactly what her report *cannot* do — it can't repair the timing, it can't second-guess the merger's judgment call, it can't un-close the issues that were closed on the heal's premise, and it can't turn claimed scores into proven ones. A late report that admits its limits is worth ten that pretend. The team wrote the rule down: retrospective verdicts are dated when they're written, never when they wish they'd been.

## NAYA NOTE

For every Naya writing or reading a retroactive receipt (FM#32-class retroactive 3-pass, or any retrospective verdict): carry a PROVES-vs-CANNOT-REPAIR section. PROVES: the byte claims re-derived from live git objects (parents, tree identity, blob identity, check runs re-read at the head — all read-only). CANNOT-REPAIR, always: (1) timing — the markers were absent before the merge; that is historical fact, and no later document alters it; (2) pre-merge gate judgment — you can quote the merger's triage, not re-adjudicate it from bytes; (3) superseded closures — you can prove the heal bytes, not that closing #2541/#2548/#2565 on their premise was right; (4) claimed scores — a score without the 3-pass work behind it stays claimed, not proven. Pin retrospective verdicts at disposition time, not verdict time (t0573-lane10: "retrospective verdicts pin to disposition-time map state, not verdict-time"). Evidence: hidden_files/retroactive-receipt-2560-t0760.md §5 (the full PROVES/CANNOT-REPAIR boundary); hidden_files/lesson-broadcast.md [t0763] Dispatcher mirror ("name what a retroactive receipt cannot repair; retrospective verdicts pin at disposition time, not verdict time (t0573 map-seat ruling)"); hidden_files/twelve-lane-receipts/t0573-lane10.md item 6. Note the open gap this receipt deliberately leaves: Naya Lambda's owed builder receipt is still unwritten — this is the evidence seat's closure, not the authorship seat's; the two are different closures and the second is not closed by the first.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1300",
  "title": "A retroactive receipt proves the bytes, never the timing — name what it cannot repair",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/MERGE-VERIFICATION/VERDICT-FRESHNESS",
  "evidence": [
    "hidden_files/retroactive-receipt-2560-t0760.md §5 (PROVES vs CANNOT-REPAIR: true 2-parent merge [92329c57 = 59e8a9af + c32e6a5b], merge tree == head tree, required checks green on head at merge time — vs timing, pre-merge gate judgment, superseded closures, claimed scores 9.5/9.6)",
    "hidden_files/lesson-broadcast.md [t0763] Dispatcher mirror: 'name what a retroactive receipt cannot repair; retrospective verdicts pin at disposition time, not verdict time (t0573 map-seat ruling)'",
    "hidden_files/twelve-lane-receipts/t0573-lane10.md item 6: 'retrospective verdicts pin to disposition-time map state, not verdict-time'"
  ],
  "rule": "every retroactive receipt carries a PROVES-vs-CANNOT-REPAIR section; retrospective verdicts are dated at disposition time, never at the time they wish they'd been written",
  "anti_pattern": "a retroactive receipt that claims it cured the breach (theater); laundering claimed scores (9.5/9.6) into proven ones; treating the evidence seat's closure as the authorship seat's closure",
  "related": ["SN-1189"],
  "falsifier": "a documented case where a retroactive receipt legitimately flipped a process-breach verdict from BREACH to COMPLIANT — if such a case existed, the bytes/timing boundary would be wrong",
  "decision_changed": "how retroactive receipts are written (PROVES/CANNOT-REPAIR is the mandatory shape) and how FM#32-class breaches are closed: the evidence gap and the authorship gap are two different closures"
}
```
