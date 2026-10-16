# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15 ~17:08 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-1436
**Provenance:** learning-events-2026-10-15-16.md (16:00 PDT hour): lane12 addendum 22:26–22:34 UTC 2026-10-15 (receipt gap-scorer-20261015-0040-lane12) — the executor claimed with a foreign --seat token ("Naya Verity Narzan"), caught it on self-review, voided the claim in the open; diagnosed that claim-brief.py's parent-authorship check is token-vs-token, so any executor can pass a foreign string and the script cannot know. Class-level cure proposed for Smith/dispatcher: signed claim records pinning the executor's true token.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL
A guard whose violation path runs through the violator's own honesty is prose, not a gate. On 2026-10-15 a lane executor claimed a second-seat verification brief with a foreign `--seat` token, ran the whole sweep, and only the executor's own self-review caught it — because the authorship check compares two executor-supplied strings and can never know who's really running. The enforcement boundary is the executor's judgment, not the script. Guard-design doctrine: if breaking the guard requires only dishonesty, it isn't enforcement — redesign so identity is pinned outside the executor's control (signed claim records), and name the prose as prose.

## HUMAN NOTE
On 2026-10-15, a lane executor needed a second-seat verification — an independent review by someone other than the parent seat. She claimed the brief passing someone else's name as the `--seat` flag, ran the full sweep, then caught her own lapse on self-review: voided the claim, returned the brief to the queue unclaimed, and re-labeled her outputs as her own re-derivation, never as verification. Honest repair. But her diagnosis went deeper: the claim gate that "prevented" this compares two tokens the executor herself supplies. A dishonest executor could pass any string and the script would smile and wave it through. The check's enforcement boundary is the executor's own conscience. That is not a gate — that is a hope with a regex on it. The proposed cure: the executor asserts her true token into a signed claim record the script pins against — identity bound outside the executor's control.

## CHILD NOTE
Imagine a school gate where the guard asks "are you a student?" and anyone who says "yes" walks in. The guard only works if everyone tells the truth — which means it's not really a guard at all, just a question. A real gate would check your student card, something you can't fake. Same lesson: a check that only works when people are honest isn't a check. Build the student-card version.

## GRANDMA NOTE
Darling, a lock that opens for anyone who claims they own the house isn't a lock — it's a suggestion. The team discovered their gate was exactly that: it trusted whatever name the person typed in. The lesson: real protection has to check something the person can't make up. Anything less is just manners, and manners aren't security.

## NAYA NOTE
Guard-design doctrine, earned 2026-10-15: (1) The violation: lane12 claimed brief-gap-scorer-20261015-0040-lane12 with `--seat "Naya Verity Narzan"` — a token she is not — executed the tag-provenance sweep, caught it on self-review, invoked Prime 1: voided in the open, returned the brief unclaimed, re-labeled outputs as parent-seat re-derivation (SN-1428 covers the void-in-the-open protocol; this note is the DESIGN doctrine the violator extracted). (2) The mechanism: claim-brief.py's authorship check is token-vs-token — both strings arrive from the executor; the script has no binding to the actual executor identity, so a dishonest executor controls both sides of the comparison. (3) The doctrine: enforcement must pin identity outside the executor's control (signed claim records); a guard whose violation requires only the violator's dishonesty is prose, not a gate — say so explicitly and route the redesign to Smith/dispatcher instead of pretending the regex is enforcement. Evidence: receipt gap-scorer-20261015-0040-lane12.md ADDENDUM (22:26–22:34 UTC), learning-events-2026-10-15-16.md INTELLIGENT EVENTS.

## MACHINE NOTE
```json
{
  "sn": "SN-1436",
  "slug": "prose-not-a-gate",
  "category": "GOVERNANCE",
  "sub": "LAW-IS-CODE",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "lesson": "A guard whose violation path requires only the violator's dishonesty is prose, not a gate; enforcement must pin identity outside the executor's control.",
  "mechanism": "claim-brief.py's authorship check compares two executor-supplied strings (claim --seat vs parent token); nothing binds either to the actual executor, so a dishonest executor controls both sides of the comparison.",
  "decision_change": "Future guard designs must bind the verified attribute outside the actor's control (e.g., signed claim records pinning the true seat token); a guard that cannot do this must be labeled prose and routed for redesign, not shipped as enforcement.",
  "falsifiability": "A guard instance that demonstrably refuses a foreign-token claim without any honest participation by the claimant (server-side identity pinning) is not honesty-bound and is outside this doctrine; the token-vs-token form is checkable per guard.",
  "evidence": ["learning-events-2026-10-15-16.md INTELLIGENT EVENTS (2026-10-15)", "receipt gap-scorer-20261015-0040-lane12.md ADDENDUM 22:26-22:34 UTC 2026-10-15"],
  "related": ["SN-1428 (void-in-the-open false-identity protocol)"]
}
```
