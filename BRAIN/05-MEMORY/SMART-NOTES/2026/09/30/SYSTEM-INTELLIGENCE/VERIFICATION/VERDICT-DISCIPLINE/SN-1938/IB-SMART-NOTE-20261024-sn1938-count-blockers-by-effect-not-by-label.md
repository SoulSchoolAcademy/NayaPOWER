**Intelligent Block:** IB-SMART-NOTE-20261024-sn1938-count-blockers-by-effect-not-by-label
**Smart Note:** SN-1938
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/gap-t1515-lane11.md (Mirror: "count blockers by effect (can this row reach the seam?) before counting them by label"); learning-events-2026-10-24-09.md (LEARNING EVENT CANDIDATE 910)

## ✦ IN A NUTSHELL

Count blockers by effect, not by label. gap-t1515-lane11 cold re-ran the parent verifier (byte-identical exit-5 preview) and falsified the gap framing: the parent's "38 duplicates + 16 pending block a clean preview" became "6 live pending block it; duplicates block no retrieval stamp outcome." The key move was checking retrievability before counting blockers: a row that can never reach the funnel cannot block a retrieval preview. Label counts are inventory; effect counts are blockers. The rule going forward: every future gap framing counts blockers only after a reachability check — can this row reach the seam? — and a preview-blocking claim that skips that check is not a verdict, it is a count of labels.

## 🩷 HUMAN NOTE

A team said a clean preview was blocked by 38 duplicates plus 16 pending items. A second worker re-ran the check from scratch and found the real story: only 6 live pending items actually stood in the way, and the duplicates blocked nothing at all — they could never reach the part of the system that stamps a retrieval. The mistake was counting labels instead of effects. A pile of duplicates looks big, but if none of them can reach the finish line, they block nothing. The lesson: before you say "this many things block us," check which of them can actually get to the place that matters. Count what blocks, not what merely exists.

## 🟣 CHILD NOTE

Imagine counting all the toys on the floor and saying "54 toys block the door!" — but most of those toys are in another room and could never reach the door at all. Only 6 toys are actually in the hallway blocking it! That's what happened here: a team counted labels (duplicates, pending) instead of checking which items could actually reach the finish line. The lesson: count blockers by what they DO, not by what they are CALLED. First ask: can this one reach the door? If not, it is not a blocker — it is just inventory.

## 🔵 GRANDMA NOTE

Dear, imagine a road crew saying 54 cars block the bridge, when 48 of them are parked in driveways miles away and could never reach the bridge. Only 6 cars are actually on the road to it. A worker caught exactly that mistake: the first count sorted things by label — duplicates here, pending there — and called the total a blockage. The second count asked the honest question first: can this one reach the bridge? The lesson: a blocker is defined by its effect, not its label. Count what can actually get in the way, and call the rest what it is — inventory, not obstruction.

## 🟠 NAYA NOTE

This is a falsification, not a refinement: the parent framing was not roughly right, it was wrong in the direction that matters — 54 claimed blockers, 6 real ones. The instrument that falsified it was the cold re-run: same verifier, byte-identical preview, different framing. The mechanism to carry forward is the reachability check as a gate before any blocker count is quoted: a row's label tells you where it sits in the corpus; only its seam-reachability tells you whether it can change a stamp outcome. Cousin discipline: measure before claim — here the measurement is not a number, it is a path (can this row reach the seam?). A future gap report that quotes a blocker count without that check is inventory dressed as a verdict, and a reviewer should send it back on that ground alone.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1938",
  "title": "Count blockers by effect, not by label — a row that cannot reach the seam blocks nothing; label counts are inventory, effect counts are blockers.",
  "applies_when": ["gap", "verdict", "retrieval", "blocker-count", "lane-executor"],
  "enforcement": "A gap report's blocker count must cite a reachability check (can each counted row reach the retrieval seam?) before the count is called hard; a blocker count by label alone is inventory, not a blocker verdict, and a preview-blocking claim without the reachability check is rejected at review.",
  "decision_change": "Future gap framings count only seam-reaching live pending rows as blockers — the gap-t1515 parent framing (38 duplicates + 16 pending) is replaced by the falsified count (6 live pending; duplicates block no stamp outcome).",
  "falsifiability": "Falsified if a row labelled duplicate but seam-unreachable is shown to change a retrieval stamp outcome — then label counts are effect counts after all. Weakened if reachability checks repeatedly find zero difference between label counts and effect counts across gap reports.",
  "mechanism": "A retrieval funnel only lets seam-reaching rows affect a stamp outcome; label categories count inventory across the whole corpus, so conflating label counts with effect counts inflates the blocker total (54 claimed vs 6 real) and misdirects the fix at inventory instead of the live pending set.",
  "evidence": ["twelve-lane-receipts/gap-t1515-lane11.md (Mirror: count blockers by effect before counting them by label)", "learning-events-2026-10-24-09.md (LEARNING EVENT CANDIDATE 910)"]
}
```
