# INTELLIGENT BLOCK — SN-2070

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02070-attempt-the-brief-dont-inherit-the-skip
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Gate-stall receipt 2026-11-05 12:43 PST (twelve-lane-receipts/gate-stall-20261105-1243.md, mirror lesson); surfaced by the daily learning review 2026-11-05 13:20 PST (learning-events-2026-11-05-13.md, CANDIDATE 1012). Distinct from SN-2068 (skip on gates, never on flags — which skips are legitimate) and SN-2066 (a free verdict reads the registry) — this is the fresh-attempt rule for stall receipts.

## ✦ IN A NUTSHELL

Attempt the brief, don't inherit the skip: a stall receipt is only as honest as the attempts behind it. The 11:39 gate-stall run left `brief-gap-gap-t1002-lane2.md` unattempted on its seat-bar text; the 12:43 run attempted it and the script refused exit 2 on a live stamped claimability gate — so this receipt's stall claim rests on 31/31 fresh script verdicts with zero inherited judgments. The durable rule: **every brief in a stall run gets a fresh claim-script verdict in that run; inherited text is never a verdict.**

## 🩷 HUMAN NOTE

Shawn — when a run stalls, its receipt says "we tried everything and nothing could move." That claim is only true if the run actually tried everything, this time. The morning run skipped one brief because an old note said it was barred — but when the next run tried it for real, the script itself refused it on a stamped gate, which is stronger proof and the only kind that counts. From now on, a stall receipt has to show a fresh attempt for every single brief — no "skipped because last time said so." A receipt built on borrowed skips is a rumor; a receipt built on fresh attempts is proof.

## 🟣 CHILD NOTE

Imagine you have a list of 31 chores and you tell your teacher "I tried them all and none of them worked." But for one chore, you didn't actually try it — you just remembered that yesterday someone said it wouldn't work. Your teacher can't trust your report, because that one chore might have worked today. The new rule: you have to actually try every chore, every single time, and write down what happened each time. Then your report is honest, because every word in it comes from something you really did.

## 🔵 GRANDMA NOTE

Dear, it's like telling the family you knocked on every door on the street and nobody answered — but you skipped one house because last week someone said nobody lives there. Maybe someone moved in since. The only honest report is the one where you knocked on every door yourself, today. From now on, we knock on every door, every time, and we write down what each knock brought — no borrowing yesterday's knocks for today's report.

## 🟠 NAYA NOTE

For every seat that produces a stall receipt: attempt the claim script on every brief in the queue, in this run, and record the fresh exit code per brief. Never carry a skip forward on prior-run text — not on seat-bar prose, not on a previous receipt's verdict. Gates, seats, and claimability stamps change between runs, so a prior run's judgment is evidence about then, not now. In the live instance, the 11:39 run's one inherited skip turned out to be a live stamped claimability gate ("NON-Clarity SEATS ONLY", stamped 2026-10-26) that the script enforces itself with exit 2 — the fresh attempt both confirmed the stall and strengthened the receipt from 30 fresh + 1 inherited to 31/31 fresh. A receipt reviewer rejects any stall receipt that records a brief as skipped on prior-run text; the run re-attempts it. The claim gate's exit codes are the verdicts; inherited text is never a verdict.

## 🟢 MACHINE NOTE

```json
{
  "slug": "attempt-the-brief-dont-inherit-the-skip",
  "sn": "SN-2070",
  "title": "Attempt the Brief, Don't Inherit the Skip",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["stall", "receipt", "claim-gate"],
  "enforcement": "A stall receipt is accepted only when every brief carries a fresh claim-script verdict from this run; the receipt reviewer rejects any receipt that records a brief as skipped on prior-run text, and the run re-attempts it. The claim gate's exit codes are the verdicts; inherited text is never a verdict.",
  "falsifier": "Proven wrong if, over a sustained window, every inherited skip re-attempted fresh returns the identical verdict while no gate or seat changed in between — then inheritance costs no honesty and fresh attempts are pure overhead.",
  "decision_changed": "How stall runs produce receipts: attempt every brief fresh instead of compressing inherited skips into '31 skipped' — a stall claim rests on fresh script verdicts only.",
  "mechanism": "Gates, seats, and claimability stamps change between runs, so a prior run's judgment is evidence about then, not now; only a fresh script verdict proves the refusal still holds now. An inherited skip compresses that evidence away, so the receipt's stall claim rests on fewer attempts than it claims — the 12:43 run's fresh attempt on the inherited brief surfaced a live stamped gate the 11:39 text had only described.",
  "provenance": "Gate-stall receipt 2026-11-05 12:43 PST (twelve-lane-receipts/gate-stall-20261105-1243.md, mirror lesson): the 11:39 run left brief-gap-gap-t1002-lane2.md unattempted on its seat-bar text; the 12:43 run attempted it and the script refused exit 2 on a live stamped claimability gate ('NON-Clarity SEATS ONLY', stamped 2026-10-26), so the receipt's stall claim rests on 31/31 fresh script verdicts (29x exit 7 parent-authorship, 2x exit 2) with zero inherited judgments. Surfaced by daily learning review 2026-11-05 13:20 PST (learning-events-2026-11-05-13.md, CANDIDATE 1012). Distinct from SN-2068 (skip on gates, never on flags) and SN-2066 (a free verdict reads the registry)."
}
```
