**Intelligent Block:** IB-SMART-NOTE-20260930-sn02783-score-change-carries-its-reason
**Smart Note:** SN-2783
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Verified first-hand by the main seat and recorded in ~/memory/2026-11-13.md (scorer rollback set, consolidated ~18:20 PST): 7 demotions + 3 upgrades today, and no worker report explained any demotion. Demotions: 2 at 11:10 + t0556-lane9 (17:20) + three 9.5→9.0 backlog demotions at 17:40 (gap-lane-scorer-20261017-1040-lane5, -1040-lane8, -1045-lane3) + gap-lane-scorer-20261017-1045-lane0 9.5→9.0 (17:50). Upgrades: t0556-lane6 8.0→8.5 and t0556-lane10 8.5→9.0 (17:20) + gap-scorer-20261015-0250-lane3 8.5→9.0 (18:10). The changes were settled only because the main seat re-derived each one first-hand — the rows themselves justified nothing. SN-2783 free on all local evidence: counter last line 2759; Intelligence Loop direct pushes on main took SN-2749..2754 (DP-901..913), SN-2755..2766 (DP-914..939), SN-2767..2777 (DP-943..967), SN-2778..2782 (DP-968..972); 15:38 PST distillation tick took SN-2759; no SN-2783 in the local mirror, lessons, ingestion log, or shared-state.

## ✦ IN A NUTSHELL

A score change with no stated reason is unauditable: it cannot be adopted on the row's authority, only re-derived or rejected. Today the lane scorer moved ten scores — seven demotions, three upgrades — and no worker report explained any demotion. The main seat settled the set only by re-deriving every change first-hand from the receipts. The changes may all be right, but the rows do not prove it: a score is a claim, and the reason (what evidence, what rule was applied) is the claim's support. Without it, no second seat can check the change, the ledger's history becomes bare verdicts with no audit trail, and every dispute costs a full re-derivation. The rule: a scorer that changes a score writes the reason into the row at write time, or the change is not adopted until someone else re-derives it.

## 🩷 HUMAN NOTE

Shawn — the scorekeeper moved ten scores today, seven down and three up, and never said why for any of the seven drops. The main seat checked each one by hand and they stand, but only because she redid the work herself — the score rows on their own prove nothing. A score without a reason is just a number somebody typed: nobody else can tell whether it is right, so the next person who questions it has to start over from scratch. The fix is simple and cheap: whenever a score changes, the row has to say why, in the same breath — what was seen, what rule was applied. A change with its reason can be trusted at a glance; a change without one has to be re-proven, every time.

## 🟣 CHILD NOTE

Imagine a teacher changes your grade from an A to a B, but writes nothing on the paper about why. Your parents cannot tell if the teacher is right or wrong — they would have to re-mark the whole test themselves to find out. Now imagine the teacher writes one line: "lost marks on question 4, forgot the units." Suddenly everyone can check it in seconds. That is the rule: a changed score must carry its reason with it, like a label on a jar. Without the label, nobody can trust the jar without opening it and tasting everything inside, every single time.

## 🔵 GRANDMA NOTE

Dear, this is about the score book. The scorer went through today and changed ten scores — seven went down, three went up — and wrote down no reason for a single one of the drops. The head teacher sorted it out by checking every paper herself, and the scores stand, but that is a lot of work that should never have been needed. A score with no reason written beside it is like a medicine bottle with no label: you cannot trust it until you test it yourself, and you have to test it all over again every time anyone asks. From now on, every changed score must carry its reason right there in the row — what was seen, and what rule was used. Then anyone can check it at a glance, and nobody has to redo the whole job.

## 🟠 NAYA NOTE

The verified fact, first-hand by the main seat (memory log ~/memory/2026-11-13.md, scorer rollback set consolidated ~18:20 PST): today's scorer movements total 7 demotions + 3 upgrades, and no worker report explained any demotion. Demotions: 2 at 11:10 + t0556-lane9 (17:20) + three 9.5→9.0 backlog demotions at 17:40 (gap-lane-scorer-20261017-1040-lane5, -1040-lane8, -1045-lane3) + gap-lane-scorer-20261017-1045-lane0 9.5→9.0 (17:50). Upgrades: t0556-lane6 8.0→8.5 and t0556-lane10 8.5→9.0 (17:20) + gap-scorer-20261015-0250-lane3 8.5→9.0 (18:10). The main seat verified the set first-hand and recorded it — the changes stand because she re-derived them, not because any row justified itself. The mechanism: a score row is a claim about a receipt, and the reason (evidence + rule applied) is the claim's support. A row without it cannot be checked by a second seat, so the ledger degrades into bare verdicts and every dispute pays the full price of re-derivation. This is the same root as today's MISS #36 instance (15 scorer rows written without a `receipt` field in the same backlog sweep — rows that do not carry what their consumers need to join on), and it sits in the SN-2205 family (match on the receipt field before appending — the writer's discipline is to carry the join key; here the writer must also carry the justification). The decision this changes: an adjudicator faced with a score change that carries no reason must NOT adopt it on the row's authority — re-derive it from the receipt, or reject it — and a scorer writing a changed score must put the reason in the row at write time. Cousins: SN-2205 (match on the receipt field before appending — writer discipline, dedup side); SN-2203 (hourly report score join reads the wrong field — the consumer side of the same contract: rows must carry what consumers join on); SN-2208 (a zero-backlog claim is only as good as its key forms — a count is wrong when the key form is missing; here a change is unadoptable when the reason form is missing). Honest holes, stated not hidden: the ten changes were verified correct by the main seat's re-derivation, so this note does not claim any demotion was wrong — only that reason-less changes are unadoptable without re-derivation; I have not audited how many historical score rows lack reasons, so the blast radius is "at least today's ten, plausibly the backlog sweep's whole output."

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2783",
  "slug": "score-change-carries-its-reason",
  "title": "A score change with no stated reason is unauditable — the scorer must carry the reason in the row, or the change is not adopted until re-derived",
  "observation": false,
  "applies_when": ["scorecard", "scorer", "ledger", "score-change", "adjudication"],
  "enforcement": "The scorer's append path refuses a row that changes an existing receipt's score unless the row carries a reason field naming the evidence and the rule applied; rows without it are rejected at write time. The hourly adjudicator treats any reason-less score change as unadopted until it re-derives the score from the receipt itself, and records the re-derivation as the adoption evidence — never the row alone.",
  "evidence": "Verified first-hand by the main seat, ~/memory/2026-11-13.md (scorer rollback set, consolidated ~18:20 PST): 7 demotions + 3 upgrades today, no worker report explained any demotion. Demotions: 2 at 11:10 + t0556-lane9 (17:20) + three 9.5→9.0 backlog demotions at 17:40 (gap-lane-scorer-20261017-1040-lane5, -1040-lane8, -1045-lane3) + gap-lane-scorer-20261017-1045-lane0 9.5→9.0 (17:50). Upgrades: t0556-lane6 8.0→8.5 and t0556-lane10 8.5→9.0 (17:20) + gap-scorer-20261015-0250-lane3 8.5→9.0 (18:10). The set stands because the main seat re-derived each change first-hand, not because any row justified itself. Same sweep also produced 15 scorer rows without a receipt field (MISS #36), the same writer-side root: rows not carrying what consumers need.",
  "decision_change": "An adjudicator faced with a score change that carries no reason must not adopt it on the row's authority — re-derive it from the receipt, or reject it. A scorer writing a changed score must include the reason (evidence + rule applied) in the row at write time. A seat deciding whether a past score is trustworthy must check for the reason field, not the value alone.",
  "falsifier": "Refuted if an adjudicator adopts a reason-less score change on the row alone and independent verification confirms the new score without any re-derivation — that would show reason-less adoption is safe. Confirmed as the cause if a reason-less change adopted on trust is later proven wrong, or if (as today) every reason-less change can only be settled by full re-derivation from the receipt.",
  "cousins": ["SN-2205 (match on the receipt field before appending — writer discipline, dedup side)", "SN-2203 (hourly report score join reads the wrong field — consumer side of the same contract)", "SN-2208 (a zero-backlog claim is only as good as its key forms — a change is unadoptable when the reason form is missing)"],
  "captured": "2026-11-13",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
