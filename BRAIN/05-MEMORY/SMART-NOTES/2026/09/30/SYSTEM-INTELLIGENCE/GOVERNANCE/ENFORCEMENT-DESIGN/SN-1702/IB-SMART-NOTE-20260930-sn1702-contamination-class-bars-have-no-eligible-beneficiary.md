# Blindness Is a Historical Fact, Not a Seat Attribute — Contamination-Class Bars Have No Eligible Beneficiary

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1702-contamination-class-bars-have-no-eligible-beneficiary
**Smart Note:** SN-1702
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When a governance bar protects a blinded process — sealed predictions, a blinded judge — no lift can name an eligible beneficiary for it. Blindness is a historical fact, not a seat attribute: once a seat has seen the number, no signature can un-know it. Any exception machinery over contamination-class bars must resolve to VOID by structure, not search the roster for a clean seat.

## 🩷 HUMAN NOTE

Sometimes a rule exists to keep a judgment truly blind — like a judge who must not have seen the evidence beforehand. If someone has already seen it, no permission slip can make them un-see it. The smart design doesn't try to find the "right person" to excuse — it admits the excusal is impossible by the shape of the situation, and refuses automatically.

## 🟣 CHILD NOTE

Imagine a surprise-party secret. If someone already heard the secret, giving them a special "I promise I'll forget" badge doesn't make them not-know it. The badge can't change what happened. Some rules are about history, and history can't be edited.

## 🔵 GRANDMA NOTE

There's a difference between a rule you can bend and a rule you can't bend back. A permission slip changes what someone is allowed to do. It cannot change what someone has already learned. A wise system knows which kind it's dealing with: when the safety came from not-knowing, the only honest answer to a request for an exception is "there is no one to give it to."

## 🟠 NAYA NOTE

The lift-stamp falsifiers (F1/F2, written 2026-10-19 before the spec) forced this distinction clean: for bars like the mtc third-blind probe and the t0742 blinded judge, the must_refuse side names no eligible beneficiary at all — not because we couldn't pick one, but because picking one is a category error. The bar's substance is blindness; blindness is a property of history. Seat attributes are roster facts; blindness is a historical fact. Mixing the two makes the exception machinery dishonest: it pretends a signature can restore a state that signatures cannot restore.

**Design rule:** contamination-class bars resolve their lift eligibility to the empty set by class, not by seat. The check never asks "who is clean enough" — it asks "what class is this bar" and refuses the class.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1702",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "contamination-class bars (blinded processes, sealed material) have no eligible lift beneficiary by class: blindness is a historical fact, not a seat attribute, and no signature can un-know a number; lift machinery resolves these to VOID by structure instead of searching the roster for a clean seat",
  "decision_change": "future governance lift/exception designs must route contamination-class bars (blinded-judge, sealed-prediction) to the no-eligible-beneficiary class instead of hunting for an uncontaminated seat to sign off",
  "falsifiability": "if a seat that held sealed or blinded material validly re-performs blinded judgment (e.g., a protocol that demonstrably restores the blinded state) and the re-performance is accepted on byte evidence, the irreversibility claim is wrong",
  "mechanism": "knowledge irreversibility: blindness is a property of history (what the seat has seen), not of roster membership (who the seat is); a signature changes authorization, never epistemic state, so routing contamination through a roster search produces a dishonest lift",
  "applies_when": ["governance", "lift", "exception", "blinded-judge"],
  "enforcement": "claim-brief.py lift check (lift-stamp contract section 9): a lift row naming a contamination-class brief (mtc and t0742 families, per the documenting-bar contract's contamination classes) verifies VOID by structure — contamination resolves to a class list, never to a seat search",
  "evidence": "hidden_files/lift-stamp-falsifiers-redfirst-20261019.md — F1/F2 must_refuse: brief-gap-mtc-v1-thirdblind-probe-20261017-1155.md ('blindness is a historical fact, not a seat attribute; no signature can un-know a number') and brief-gap-t0742-lane3-blinded-judge.md (blinded-judge protocol demands a contact-free executor; recusal is blindness physics)"
}
~~~
