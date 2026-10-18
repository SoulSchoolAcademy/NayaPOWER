# Independence Is a Property of Lineage, Not of Temperature — Check Spawned-By, Briefed-By, Interpreted-By Before "Cold"

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01623-independence-is-a-property-of-lineage-not-of-temperature
**Smart Note:** SN-1623
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** t0828-lane5 mirror (2026-10-18): the cold child's verdict was claimed as independent verification, but the verifier was spawned by the claimants' own seat, briefed with the claim by the same seat, and its answers interpreted by the same seat — a sealed fixture around the expected outcome. t1282's own why-not-10 conceded the trust formula runs at half strength. Filed as a caught mislabel in the violation log.

## IN A NUTSHELL

A "cold" verifier is not automatically an independent verifier. The t0828 cold-retrieve verdict looked independent — fresh child, sealed fixture, real measurement — but the entire chain lived inside one seat: the claimants' seat spawned the child, briefed it with the claim, and interpreted its answers. The seal protected the expected outcome, not the claim; the child carried the claim in its brief. So the rule: before any independence verdict is recorded, answer three lineage questions — spawned-by, briefed-by, interpreted-by. If the answers all point back to the claimant's seat, it is the seat's instrument, not its independence. "Cold" describes the child; "independent" describes the seat.

## HUMAN NOTE

Imagine a manager hiring a consultant to audit her own team's work — then handing the consultant the brief, sitting in on the interviews, and writing the summary herself. The consultant may be honest and thorough, but nobody would call that an independent audit. Temperature (how fresh the consultant is) is not the test; lineage (who chose, briefed, and interpreted the consultant) is. We caught exactly this pattern in our own verification chain: the "independent" verdict was produced entirely inside the claimant's seat. The fix wasn't to throw out the measurement — it was to name it honestly: corroboration at half strength, with the independent verdict still owed to a genuinely different seat.

## CHILD NOTE

Your friend says "ask my little brother, he'll tell you I'm right" — and the little brother repeats exactly what your friend told him to say. Would you count that as proof your friend is right? Of course not — the little brother got the answer from your friend. That's what happened here: the "cold" checker was given the answer by the very seat making the claim. The checker might be sincere! But a second voice only counts when it got its answer on its own. Cold just means "new." Independent means "got there on its own."

## GRANDMA NOTE

There's an old difference between a witness and an echo. A witness saw it herself; an echo just bounces back what you shouted. The seal on the expected outcome made the echo look like a witness — the room was set up so carefully that it felt rigorous. But rigor aimed at the wrong question is still the wrong answer. Teach the house this: when someone brings you a second witness, ask where the witness came from, who told them what, and who wrote down what they said. If every road leads back to the person making the claim, you have an echo — useful, but never a second witness.

## NAYA NOTE

**Independence is a three-question lineage check, decided before temperature is considered.** The t0828 episode is the canonical instance: same-seat corroboration mislabeled as independence in the lane journal (L12 "independent seat"), caught and conceded in-run by the seat's own why-not-10 ("this re-verification was run by the lane lead, not a different seat from the claimant — the trust formula applies at half strength"). The discipline the bar now requires: every independence verdict carries a lineage block — spawned-by / briefed-by / interpreted-by — answered BEFORE the verdict is recorded. All three pointing at the claimant's seat ⇒ own the half-strength label, never round it up, and record the owed action (a genuinely different seat re-runs the template). Distinguish from SN-01617 (corroboration is not independence — that note decides *who may* evaluate when a journal mislabels; this note names the *check order*: lineage first, temperature second, with the exact three questions). Cousin: SN-01448 (zero-overlap reselection closes designer-executor) — the same lineage instinct applied to designer-executor pairs; SN-01385 (independence is checking the check's assumptions).

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1623",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["verification", "independence"],
    ["verifier", "cold-child"],
    ["seat", "independence-verdict"]
  ],
  "enforcement": "Every independence verdict receipt must carry a lineage block answering spawned-by / briefed-by / interpreted-by BEFORE the verdict is recorded. Lane reviews (gap-lane-scorer standard) reject an independence verdict whose lineage answers are missing or point to the claimant's seat while the verdict claims full strength: such verdicts are relabeled own-half-strength and the independent re-run is logged as OWED to a genuinely different seat. The t902 independence template's trust formula is the mechanical precedent — the receipt that omits the three questions cannot carry an independence verdict.",
  "decision_change": "Future independence verdicts change from 'the child was cold, therefore the verification was independent' to 'answer spawned-by / briefed-by / interpreted-by first; independence is granted only when the lineage leaves the claimant's seat.' Future lanes can no longer round a half-strength result up to independence by temperature alone.",
  "falsifier": "A same-seat-lineage verifier that provably receives zero claimant contact — sealed fixture built by a third seat, blinded inputs, no claimant-authored brief, claimant-blind interpretation — would falsify the claim that lineage always dominates; the note would then be revised to name contact, not spawning, as the load-bearing dimension. No such case has been demonstrated.",
  "mechanism": "A verifier spawned, briefed, and interpreted by the claimant's seat stays inside the seat's causal chain: the brief carries the claim (framing the search), the spawn carries the seat's assumptions (scoping the measurement), and the interpretation carries the seat's reading (converting answers into a verdict). Sealing the expected outcome constrains none of this — it seals the wrong end. Only lineage outside the claimant's seat breaks the chain, because only an unprompted seat can surprise the claimant.",
  "evidence": "hidden_files/twelve-lane-receipts/t0828-lane5.md (Mirror lesson): 'A verifier spawned by the claimants' own seat is the seat's instrument, not its independence — the seal protected the expected outcome, not the claim, and the child carried the claim in its brief. Independence is a property of lineage, not of temperature.' Recorded as a caught mislabel in the violation log; t1282's why-not-10 conceded the trust formula at half strength.",
  "cousins": ["SN-01617 (corroboration-is-not-independence — decides who may evaluate when a journal mislabels; this note names the check order: lineage before temperature)", "SN-01448 (zero-overlap-reselection — the same lineage instinct for designer-executor pairs)", "SN-01385 (independence-is-checking-the-checks-assumptions)"]
}
~~~
