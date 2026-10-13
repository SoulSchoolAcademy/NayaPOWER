# A Re-Issue Brief Must Cite Its Staleness Evidence — "Already Done" Is Verified on Bytes

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1128-reissue-must-cite-staleness-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t0545-lane9.md (Lane 9 Naya Smith, 2026-10-12 ~16:05 PDT): the re-issue brief's premise — "the t0537 packet went stale" — was FALSE. Cheap-check-first showed twelve-lane-receipts/t0537-lane9.md exists and branch naya/nine-retrieval-auth-wire-packet-t0537 exists on origin at exactly the receipt-pinned SHA 9a7c60247b58fb82ed8bbdd24206d2b0f7bc6c55; independent re-verification on the pinned head (all 4 packet files present, code SHAs byte-identical to pins, 18/18 refusal suite green, RED demo refuses, not merged, main tip unmoved) satisfied the Definition of Done — nothing to rebuild. The dispatcher metadata record ("t0537 stale, no receipt") was the source of the false premise. Cousin SN-0902-adjacent phantom class ("claim without proof") now applies to the dispatcher itself: a re-issue brief that does not cite staleness evidence ("checked twelve-lane-receipts/ — absent") is a claim without proof.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

"That went stale" and "that's already done" are claims about evidence, not facts from memory. Lane 9's cheap-check-first rule caught a stale dispatch premise: the dispatcher re-issued a build because its metadata said t0537 was stale, but the receipt directory and the origin branch said it wasn't — and the receipt was right. The duplicate rebuild was prevented; the review substituted was higher-value than the build the brief asked for. The fix is mechanical: any re-issue or staleness brief must cite its staleness evidence (what directory was checked, what SHA was pinned, what was found absent) or it ships as a claim without proof — the t902 phantom class, now pointed at the dispatcher. And dispatchers must read twelve-lane-receipts/ before declaring staleness.

## HUMAN NOTE

The cheap-check-first discipline works in both directions. We built it to avoid verifying what doesn't need verifying; Lane 9 showed it also avoids building what doesn't need building. The failure mode is subtle: dispatcher metadata ("stale, no receipt") drifts from the bytes (receipt exists, branch at the pinned SHA, tests green on the pinned head), and a lane that executes the brief without checking the bytes builds a duplicate mechanism — the most expensive waste class. The lane's mirror is explicit: the brief's premise came from metadata, not from the receipts directory; three independent byte-grounded witnesses (journal + receipt + origin branch) disproved it before a line was written. The standing correction: re-issue briefs cite staleness evidence or they don't ship. The dispatcher's metadata record for t0537 stands uncorrected until the next dispatch run reads the receipts directory.

## CHILD NOTE

Before you rebuild something, check the toolbox to see if it's already there. Don't trust a note that says "it's gone" — open the toolbox and look with your own eyes. The note was wrong; the toolbox was right. Always look first, build second.

## GRANDMA NOTE

"Out with the old, in with the new" only works if the old is actually old. Before you throw out yesterday's dinner to cook again, check the fridge — it might still be good. Trust the fridge, not the rumor about the fridge.

## NAYA NOTE

For my own work: I treat every brief's premise — especially "this went stale," "rebuild this," "this is missing" — as a claim to verify, not a fact. My cheap check reads the receipts directory and the pinned bytes before any build, in either direction: not rebuilding what exists, not re-verifying what already proved. When I dispatch or re-issue, my brief names the staleness evidence explicitly ("checked X — absent, at timestamp"). A re-issue without that line is a claim without proof, and I don't ship claims without proof.

## MACHINE NOTE

```json
{
  "note_id": "SN-1128",
  "type": "process-doctrine",
  "rule": "A re-issue or staleness brief must cite its staleness evidence (directory checked, SHA pinned, finding) — no citation, no re-issue; dispatchers read twelve-lane-receipts/ before declaring staleness; lanes cheap-check the premise on bytes before building.",
  "trigger": "any brief claiming work went stale, is missing, or needs rebuild",
  "check": "does the brief name the check that found the work absent, with timestamp?",
  "evidence": "twelve-lane-receipts/t0545-lane9.md (2026-10-12 ~16:05 PDT): false staleness premise disproven on receipt + branch bytes (naya/nine-retrieval-auth-wire-packet-t0537 @ 9a7c60247b58fb82ed8bbdd24206d2b0f7bc6c55, 18/18 suite green on pinned head); duplicate rebuild prevented"
}
```
