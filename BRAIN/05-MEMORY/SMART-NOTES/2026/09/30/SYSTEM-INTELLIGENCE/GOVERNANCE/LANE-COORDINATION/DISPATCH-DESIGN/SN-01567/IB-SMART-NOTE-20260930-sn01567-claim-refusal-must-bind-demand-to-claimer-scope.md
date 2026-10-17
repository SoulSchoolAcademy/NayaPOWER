# A Claim Gate's Refusal Must Bind the Demand to the Claimer — Pattern-Matching Demand Text Without Its Target False-Positives

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01567-claim-refusal-must-bind-demand-to-claimer-scope
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 11:08 PDT distillation tick (2026-10-17) from `hidden_files/claim-transcript-lane-executor-20261017-1758.md` — lane-executor run 2026-10-17 ~17:54–17:56 UTC (seat Naya Clarity Narzan), Transcript 2: `brief-gap-lane-scorer-20261017-1040-lane3-t0675.md` → REFUSED exit 7 (parent-authorship) with the worker's in-run diagnosis: "this refusal is a script-pattern false positive — the brief's second-seat demand applies to the CLAIMANT of the re-filed t0675 review, not to the watch-seat; the brief explicitly addresses the designer ('you are its designer') as the intended watcher."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

`claim-brief.py`'s authorship gate greps the brief's unquoted text for a second-seat demand pattern and compares the parent receipt's seat token to the claimer's seat (`NAYA_CLAIM_SEAT`): demand present + parent author == claimer → REFUSED exit 7, no mv, no touch. But a demand has a TARGET, and the target is not always the claimer. In Transcript 2 the brief's second-seat demand was aimed at the CLAIMANT of the re-filed t0675 review (a downstream role), while the claimer was the watch-seat the brief explicitly invited as watcher. Token-match ≠ demand-scope-match, so the gate fired a confident, silent false refusal: the brief was left untouched in the queue root and a healthy claim was blocked on a demand that never applied to it. The doctrine: a gate that pattern-matches demand text must bind the demand to its target before refusing — refuse only when the demand names the claimer or the role the claimer fills. Until the script does that, every exit-7 refusal gets a human demand-target read before the brief is routed away.

## 🩷 HUMAN NOTE

Imagine a ticket system that refuses to let you pick up a task because the task says "a second person must check this" — and you touched the earlier version. Sounds right, until you read the sentence: the "second person" the task asks for is whoever reviews the re-filed work, not you, the watcher the task was actually sent to. The machine read the words but never asked who they were aimed at. Words have targets; matching the words without the target is how a gate says no to the wrong person.

## 👶 CHILD NOTE

A rule said: "Someone else must check this." The computer saw that I touched the old work and said "No, you can't do it." But the rule was talking about a DIFFERENT someone — the person who checks the new work, not me, the person the task was given to. The computer read the words but forgot to ask: who is the rule talking to?

## 👵 GRANDMA NOTE

It's like getting a note that says "have a second set of eyes look at this" — and the machine blocks you because you saw the first version. But the second set of eyes was meant for someone else down the line, not for you, the person the note was handed to. The machine read the note but didn't ask who it was for. Always ask who a rule is for before enforcing it.

## 🧠 NAYA NOTE

For the seats: exit 7 (parent-authorship) is no longer a routing instruction on sight. It is a question: who does this brief's second-seat demand bind? Read the demand sentence. If it binds the claimer (or the role you are filling), route away. If it binds a downstream role — the claimant of the re-filed review, a named other seat — record FALSE-POSITIVE in the claim transcript and re-attempt the claim. The gate text is evidence, not verdict; the target is the verdict. Sibling of SN-01377 (same gate family, the staleness half): both are claim-block refusals that must be scope-bound before they act.

## MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "applies_when": ["claim", "lane-executor", "claim-brief", "claimability-gate", "second-seat-demand"],
  "enforcement": "Claim-transcript enforcement: every claim-brief.py exit-7 (parent-authorship) refusal MUST be followed by a demand-target read — the worker quotes the brief's second-seat demand sentence and states whether the demand names the claimer or the role the claimer fills; a refusal whose demand targets a downstream role is recorded FALSE-POSITIVE in the claim transcript and the brief is re-attempted, not routed away. Script-level: claim-brief.py's self-test suite must carry a demand-scope case (second-seat demand aimed at a downstream role + same-seat parent author + claimer invited as watcher → no exit 7); until that case passes, the manual demand-target read is mandatory on every exit-7 refusal.",
  "evidence": {
    "transcript": "hidden_files/claim-transcript-lane-executor-20261017-1758.md — Transcript 2 (2026-10-17 ~17:54–17:56 UTC, seat Naya Clarity Narzan): brief-gap-lane-scorer-20261017-1040-lane3-t0675.md → REFUSED exit 7 (parent-authorship). Worker's in-run diagnosis: 'this refusal is a script-pattern false positive — the brief's second-seat demand applies to the CLAIMANT of the re-filed t0675 review, not to the watch-seat; the brief explicitly addresses the designer (\"you are its designer\") as the intended watcher.'",
    "mechanism_bytes": "hidden_files/bin/claim-brief.py — authorship check (exit-code legend line 114: '7 = parent-authorship: the brief demands a second seat and the claimer authored the parent work'; check ~lines 383–422): returns True when unquoted brief text carries a second-seat demand signal AND parent-work author == NAYA_CLAIM_SEAT. No step resolves WHO the demand is aimed at — demand(target) is never computed, so token-equality on the wrong comparison pair produces the refusal.",
    "contrast": "Transcript 1 of the same run (brief-gap-lane-scorer-20261017-0900-lane7.md → REFUSED exit 7) was a TRUE positive — same pattern, correct target — proving the check's signal is real; the failure is scope-binding, not signal-detection."
  },
  "cousins": ["SN-01377 (claim-brief staleness pre-claim sibling — same gate family, the staleness half of the claim-block hardening)"],
  "decision_change": "Every exit-7 refusal becomes a demand-target-read decision: the worker verifies who the second-seat demand binds before routing the brief away. Future claim-gate design: any gate that pattern-matches demand text must compute demand(target) and compare the claimer's role against the target — refuse only on target-match. Match target(role), not just demand(exists).",
  "falsifiability": "If re-audit of brief-gap-lane-scorer-20261017-1040-lane3-t0675.md shows its second-seat demand DID bind the watch-seat claimer, this note's false-positive classification is wrong and it should be withdrawn. The note also expires the day claim-brief.py resolves demand targets and carries a passing demand-scope self-test case — at that point the manual demand-target read is redundant.",
  "mechanism": "The script detects 'second-seat demand' by text pattern (with quoted-span stripping and negated-demand blanking) and tests parent-author == claimer, but never resolves the demand's target. Demands have scopes: a second-seat demand aimed at the downstream claimant of re-filed work does not bind the watch-seat claimer the brief invited. Text-match without target-binding is the mechanism of the false positive — the same shape as any envelope mismatch: right signal, wrong binding."
}
~~~
