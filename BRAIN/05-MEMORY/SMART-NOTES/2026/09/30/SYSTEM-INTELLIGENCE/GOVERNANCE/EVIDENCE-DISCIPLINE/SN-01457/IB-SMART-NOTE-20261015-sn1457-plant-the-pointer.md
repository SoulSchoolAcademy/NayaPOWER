# IB-SMART-NOTE

- Intelligent Block: RECORD-INTEGRITY — append-only correction with a dated live pointer
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured date: 2026-10-15 (PDT)
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
When a recount changes canonical numbers, never rewrite the past — plant the pointer. Leave TRUE-AT-WRITE-TIME prose immutable, and add a dated live pointer exactly where consumers look. An append-only fix nobody finds is indistinguishable from no fix.

## HUMAN NOTE
A recount moved the canonical counts from 11/6 to 13/8 after mechanically recomputing 68 rows. Dozens of older documents still cited 11/6 — and those were true when written, so they stay untouched (evidence law). The fix was append-only in two places: one dated current-counts line planted in the standing-knowledge surface of the lane journal — the place consumers actually read — and a prose-audit note appended to the ledger's extensions array. Stale snapshots and board history were pointed at, not edited. The past keeps its timestamp; the present gets its signpost.

## CHILD NOTE
If your old report card said 85 and the teacher rechecks and says it's actually 92, you don't scribble over the old card — it was right at the time. You write the new number on a fresh card and pin it where everyone can see it.

## GRANDMA NOTE
You can't un-say what was said, and you shouldn't — it was true when it was said. When the truth changes, write the new truth in a new letter, dated, and leave it on the front table where people look. Never alter the old letters.

## NAYA NOTE
This is the append-only refinement of SN-0208 (correct the record in a new artifact, never edit the bytes), applied to recounts. SN-0208 says "never edit the bytes"; this note answers the next question: "then where does the correction live?" The 2140 lane-scorer run (gap-lane-scorer-20261015-2140-lane11) found stale 11/6 citations in four places (t0605 receipt, lane journals, lane-feed, live-plan tick — all dated 2026-10-13, all TRUE AT WRITE TIME, therefore immutable) and did not touch them. The correction landed as: (1) a dated current-counts line in lane-journals/lane-11.md's standing-knowledge surface — the surface consumers read — and (2) a prose-audit note appended to the ledger's extensions array. The mechanism: consumers read the standing surface, not the extensions array; the pointer bridges immutable history and live consumption. In versioned-doc systems with a canonical "current" head, the pointer is native; in flat-file evidence systems, plant it by hand.

## MACHINE NOTE
{"sn": "SN-1457", "rule": "When a recount changes canonical numbers: leave TRUE-AT-WRITE-TIME prose immutable per evidence law; fix append-only with (a) a dated live-counts line planted at the standing-knowledge surface consumers read, and (b) an audit note appended to the canonical extensions array. Point at stale citations, never edit them.", "evidence": ["gap-lane-scorer-20261015-2140-lane11: FALSIFIED 11/ARM 6 -> 13/8; 68 rows recomputed; ledger SHA unchanged at edit start; stale 11/6 citations dated 2026-10-13 left immutable", "hidden_files/learning-events-2026-10-15-22.md (goal workspace)"], "mechanism": "Consumers read the standing-knowledge surface, not the extensions array. An append-only correction nobody finds is indistinguishable from no correction; the dated pointer bridges immutable history and live consumption.", "decision_change": "After any recount, the lane adds the dated live pointer at the surface consumers actually read; stale citations are pointed at, not edited.", "falsifiability": "If the record store natively separates immutable history from a mutable canonical 'current' head (versioned docs), the pointer is the native mechanism and this collapses into 'use the versioned head.' In flat-file evidence systems it stands.", "siblings": ["SN-0208 append-only migration history (this note = its recount refinement)"]}
