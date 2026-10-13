# A Fail-Closed Gate Must Prove Its Authority Corpus Is Populated Before It Switches On

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1126-fail-closed-stamped-corpus-first
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 board, Lane 9 (Naya Smith) t0537 SIGN OUT 6133484595 (2026-10-12 15:20 PDT): SURGE slice (b) refusal-point packet on branch naya/nine-retrieval-auth-wire-packet-t0537 @ 9a7c60247b58fb82ed8bbdd24206d2b0f7bc6c55 — mechanical refusal-predicate run proved the corpus has NO retrieval_authorized writer, so wiring fail-closed excludes everything; the M3 stamping migration is REQUIRED before wiring (authority decision in Shawn's gate queue). Cousin SN-1121 (name the refusal point) — distinct: SN-1121 governs the refusal-point contract; this governs the activation ordering.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A fail-closed gate switched on over an empty authority corpus denies everything — including the legitimate. **Before activating any fail-closed enforcement, run the refusal predicate against the live corpus and prove the authorized set is non-empty.** Lane 9's mechanical proof: the refusal predicate fired correctly, then the same run showed zero authorized writers exist today — wiring now would exclude the whole corpus, so the M3 stamping migration must land FIRST. Prove population before activation, never assume the corpus is ready.

## HUMAN NOTE

Fail-closed is the right default, but "fail closed" is a claim about the world, not a property of the code. The code can be perfect and the deployment catastrophic if the authority corpus it consults is empty or stale. The activation discipline: (1) run the refusal predicate against the live corpus — RED-first, prove it refuses; (2) measure the authorized set — how many writers/records carry the stamp today; (3) if the set is empty, the stamping migration is a prerequisite, not a follow-up. The migration and the wiring are one work order in sequence: stamp first, wire second. Wiring a gate that denies everything is indistinguishable from an outage.

## CHILD NOTE

Imagine a bouncer with a guest list, but nobody ever wrote any names on the list. The bouncer does their job perfectly — and turns away EVERYONE, even the people who were invited. Before the bouncer starts, someone has to check: is the list empty? If it is, write the names first, then start the bouncer.

## GRANDMA NOTE

A strict rule is only as good as the records it checks. If the membership book is empty, the strictest doorman in the world will bar the door to your own family. Always check the book is filled before you post the guard — stamp the records first, enforce second.

## NAYA NOTE

For my own work: whenever I design or review a fail-closed enforcement, the activation plan opens with the population proof — run the predicate against live bytes, count the stamped set, name the stamping migration as the predecessor. "Fail closed" never means "assume the corpus is ready." The refusal predicate test and the population measurement ship in the same packet as the wiring proposal.

## MACHINE NOTE

```json
{
  "note_id": "SN-1126",
  "type": "doctrine",
  "rule": "Fail-closed activation requires a population proof: run the refusal predicate against the live corpus, count the stamped set; an empty set makes the stamping migration a predecessor, not a follow-up.",
  "trigger": "proposing or reviewing activation of fail-closed enforcement",
  "check": "is there a measured count of authorized records on live bytes, and a named stamping migration ordered before wiring?",
  "evidence": "#2175 6133484595 (2026-10-12 15:20 PDT): Lane 9 t0537 — refusal predicate mechanically proved zero retrieval_authorized writers in corpus; M3 stamping migration REQUIRED before wiring (Shawn's gate queue)"
}
```
