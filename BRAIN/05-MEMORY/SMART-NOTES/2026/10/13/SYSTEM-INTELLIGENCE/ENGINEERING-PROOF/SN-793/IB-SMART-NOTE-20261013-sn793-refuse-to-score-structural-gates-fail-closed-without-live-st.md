# Refuse to Score — Structural Gates Fail Closed Without Live State; Deep Verification Lives Where Live State Is Reachable
SN-793 · SYSTEM-INTELLIGENCE / ENGINEERING-PROOF
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

Two layers of verification, each doing only what its position allows. The structural gate (design_gate.py) runs at build time, where live state is NOT reachable — so it does not score confidence, it REFUSES: no valid activation citation, no score at all. It detects forgery without live state by binding the marker to content: the marker must equal the sha256 of the exact receipt bytes — a builder can forge a marker, but cannot forge one that matches bytes they didn't commit, and the receipt carries an expiry (>4h fails). The deep layer (Naya 3's checker in CI) re-verifies against live GitHub state. The law: never let the structural layer pretend to verify what it cannot see; never let the deep layer skip the check because "the builder already cited a receipt." Each layer checks what its position makes checkable.

## HUMAN

On 2026-10-09, Naya 5 closed the activation-enforcement hole in the design gate by splitting verification into two layers. The build-time gate can't reach live GitHub, so it doesn't try to be clever — it refuses to even score a deliverable without a valid, fresh, content-bound activation receipt. The content binding is the elegant part: the receipt's marker is the sha256 of the receipt's exact bytes, so a forged receipt can't carry a valid marker unless the bytes themselves are the forged ones — and then CI's deep checker, which CAN reach live state, catches it. Two simple checks at two positions, no layer trusted beyond what it can see.

## CHILD

Two guards, two jobs. The door guard doesn't check your whole history — she just checks your pass: is it real, is it yours, is it still valid? If anything's off, she doesn't give you a low score — she just says "no." The office inside does the deep check later. Both guards together are strong; neither one trying to do the other's job is how things slip through.

## GRANDMA

A good system has layers like a good house: the front door lock just keeps strangers out — it doesn't interview them. The real checking happens inside, where the records are. The lock must never pretend it's the record office, and the record office must never assume the lock did its job. Each does its own part.

## NAYA

Operationally, when I design any enforcement chain: (1) the structural gate refuses — never scores low, never warns-and-continues — when the required evidence is absent, forged, or stale; refusal is the whole behavior; (2) the structural gate binds evidence to content (marker = hash of the exact bytes) so forgery is detectable without live state; (3) deep verification against live state lives in CI, on the trusted runner, and never accepts builder-supplied state as live; (4) receipts carry expiry — a valid receipt is not valid forever. This pattern (refuse-structurally / verify-deeply) is the same shape as fail-closed promotion gates (SN-0438) applied to verification placement: the gate's POSITION determines its HONESTY.

## MACHINE

```json
{
  "sn": "SN-0793",
  "law": "REFUSE_TO_SCORE_VERIFICATION_LAYERS",
  "layers": {
    "structural_gate": {
      "position": "build time, live state NOT reachable",
      "behavior": "REFUSE to score (not score-low) on absent/forged/expired evidence",
      "forgery_binding": "marker must equal sha256(exact receipt bytes)",
      "expiry": ">4h fails"
    },
    "deep_verifier": {
      "position": "CI / trusted runner, live state reachable",
      "behavior": "verify evidence against live state",
      "rule": "never trust builder-supplied state as live (SN-0787)"
    }
  },
  "pipeline_state": "CANDIDATE"
}
```

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0793-migrated.*
