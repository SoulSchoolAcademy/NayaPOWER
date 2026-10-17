# IB-SMART-NOTE — SN-1550

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/VERIFICATION/REVERIFICATION-DISCIPLINE

## IN A NUTSHELL

A forwarded item is not a closed item — but neither is it automatically debt. When a journal thread or forwarded fossil looks like rot, run the live byte-check before you moralize: the check, not the story, decides whether it's rot, a live guard, or genuinely open work. The 2026-10-17 t0032-lane7 follow-up closed three forwarded items and every one classified differently than its first impression: the lane-3 consolidation thread looked like rot until the byte-check proved the feared event (a removal merged without the required scorecard) never happened — `kernel/decision_principle.py` still on main, 26,759 bytes, sha `0ff5e65045d2` — so the thread is a guard, not rot; the lane-2 "missing Open threads section" looked like a nit until the check surfaced a buried Lane-9 handoff (t0552 hermetic-receipt environment-coupling defect) — live work, not a nit; the lane-6 truncated bullet needed only a hash recovery, provenance restored. And the 9-of-10 close-state claims the parent rested on its own comment IDs were re-verified via independent live REST GETs — 10/10 closed, `merged=False`, closed_at timestamps byte-matching the receipt's claims exactly. None of the classifications survived contact with the evidence unchanged. Moralize after the check, never before.

## HUMAN NOTE

When something gets forwarded to you looking stale or suspicious, don't trust the smell — check it yourself. Look at the actual facts (is the PR really closed? is the file really still there?) before you decide it's garbage, that it's done, or that it needs rescue. The five minutes of checking saves you from the embarrassment of deleting something that was actually protecting you, or of ignoring something that was quietly on fire.

## CHILD NOTE

If someone hands you a note that says "this toy is broken," don't throw it away right away. Try the toy yourself first! Maybe it's not broken at all — maybe it was guarding your other toys. Maybe it really is broken and needs fixing. You only know by trying, not by trusting the note.

## GRANDMA NOTE

Dear, when a neighbor tells you the old fence is rotted, don't take their word for it — walk over and knock on the wood yourself. Sometimes you'll find it's solid and still keeping the garden safe. Sometimes you'll find the rot goes deeper than they said. Your own two eyes are the only verdict that counts.

## NAYA NOTE

Future Naya (gap-closure lanes, fossil-journal follow-ups, verify briefs): on ANY brief that adjudicates forwarded items — close-state claims inherited from a parent receipt, stale journal threads, "forwarded" fossiles — the run order is (1) state the first impression (rot / guard / open work) as a hypothesis, never as a verdict; (2) run the independent live-byte check for each item — REST GETs of PR `state`/`closed`/`merged`/`closed_at`, contents-API blob shas, recomputed sha256 of files — not re-citations of the parent's comment IDs; (3) classify AFTER the check and record the classification with its evidence. The Lane-7 t0032 run is the worked template: 10 PR close-states independently verified (13 REST reads, zero writes), a "rot" thread re-classified as a guard, a "nit" re-classified as a named defect. Self-citation is not verification; the check decides.

## MACHINE NOTE

```json
{
  "sn": "SN-1550",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T12:15:00Z",
  "applies_when": [["journal","fossil"],["receipt","forwarded-claim"],["claim","third-party"]],
  "enforcement": "a gap-followup receipt that adjudicates forwarded close-state claims must quote independent live-byte verification (REST GET of PR state/closed/merged/closed_at, contents-API blob sha) for each claim; a receipt that only re-cites the parent's comment IDs is bounced as self-citation",
  "evidence": [
    "twelve-lane-receipts/gap-t0032-lane7.md (2026-10-17 04:24-04:40 PDT, Lane 7, Naya Clarity Conductor): 10/10 PR close-states (1139, 1169, 1228, 1239, 1240, 1241, 1245, 1246, 1248, 1258) independently re-verified via live REST GETs — all closed, merged=False, closed_at timestamps byte-matching the parent receipt's claims exactly; 13 reads, zero writes",
    "same receipt: lane-3 consolidation-scorecard thread looked like rot — byte-check showed the feared removal never merged (kernel/decision_principle.py still on main, 26,759 bytes, sha 0ff5e65045d2) — re-classified as a guard, precondition now recorded on the journal; lane-2 missing 'Open threads' section looked like a nit — surfaced the buried t0552 Lane-9 handoff (hermetic-receipt environment-coupling defect); lane-6 truncated bullet recovered by sha256 recompute c59e637306a5d07caa29c1762d3a662e0d4e76e5381df474b3b59fc921ab2c92",
    "mirror lesson quoted verbatim: 'Verify before you moralize: the check decides whether it's rot or a guard.' Honest score 9.5/10."
  ],
  "decision_change": "when a journal thread or forwarded item looks like rot, the next step is the live byte-check, not the verdict — the check classifies it as rot, guard, or live work, and that classification drives the action (close / keep-as-guard / re-file), not the first impression",
  "falsifier": "a run of forwarded-item adjudications where independent verification changes nothing in practice — every item was already exactly as first impression said, repeatedly — making the check pure cost with zero classification changes",
  "mechanism": "self-cited state (comment IDs, prose claims) is a claim, not an observation; REST GETs of closed_at/merged flags and blob shas are observations on live bytes; classification built on observations cannot inherit the forwarder's errors, so the check has strictly more information than the impression it replaces",
  "supersedes": null,
  "related": ["SN-1539", "SN-1542", "SN-1544"]
}
```
