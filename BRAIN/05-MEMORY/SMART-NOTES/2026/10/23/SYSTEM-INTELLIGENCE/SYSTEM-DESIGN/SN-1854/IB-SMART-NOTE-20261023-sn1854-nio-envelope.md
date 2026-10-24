The NIO Envelope — Carry Identity, Never Invent It
SN-1854 · SYSTEM-INTELLIGENCE / SYSTEM-DESIGN
**Created:** 2026-10-23T16:55:00Z
**Filed:** 2026-10-23T17:00:09Z (intelligence door, commit c60ff22c)

## IN A NUTSHELL
A Naya Intelligence Object (NIO) is the machine-addressable envelope through which a meaningful intelligence object moves through NayaPOWER without losing identity, provenance, state, governance, or intended use. It is an object CONTRACT — not a new database, not a new intelligence layer. Every NIO exposes a 20-field envelope (identity, type, meaning, intent, truth state, authority context, evidence, event lineage, verification, learning state…); fields may be absent when genuinely unknown, but they must NEVER be fabricated. Nine canonical types: EXPERIENCE, EVENT, INTELLIGENCE, RULE, DECISION, ACTION, OUTCOME, EVIDENCE, LEARNING.

## HUMAN
Imagine a sealed courier pouch for anything the system learns or decides. The pouch has 20 printed labels — what it is, where it came from, what it's for, who vouches for it. You may leave a label blank when you honestly don't know. What you may never do is write something on a label you made up — a fabricated field poisons every downstream decision that trusts the pouch. And the pouch is just the pouch: it is not a new warehouse, not a new filing system. The warehouse already exists (Intelligent Blocks and Events); the pouch just carries things through it safely.

## CHILD
Think of a lunchbox with your name on it and a note inside saying who packed it, what's in it, and who it's for. If the note says something that isn't true, someone could get the wrong lunch — or an allergy. Never write a lie on the lunchbox note. And the lunchbox is not the kitchen — it's just how lunch travels safely.

## GRANDMA
It's an envelope for anything clever the system handles, dear — with all the important facts written on the outside: what it is, where it came from, who stands behind it. You may leave a line blank when you truly don't know, but you must never invent an answer. An invented answer is worse than a blank one. And it's only the envelope — the filing cabinet stays where it is.

## NAYA
Wrap every intelligence object in the envelope and fill only what you can evidence. Leave the rest blank — loudly blank, not silently guessed. Reference the one stable canonical identity; never mint a new one for a routing alias. Let invalid objects stop at validation/governance — never hand-carry them past the boundary. Never infer authority from the envelope itself.

## MACHINE
`nio_envelope: [nio_id, nio_type, version, status, owner_scope, source, meaning, intent, truth_state, authority_context, applicability, freshness, relationships, evidence, event_lineage, application_history, outcome, verification, learning_state, successor_context]` · `field_rule: absent-when-unknown, NEVER fabricated` · `nio_types: [EXPERIENCE, EVENT, INTELLIGENCE, RULE, DECISION, ACTION, OUTCOME, EVIDENCE, LEARNING]` · `pipeline: parse → validate → route → retrieve → compare → apply → record → verify → learn → hand off` · `lifecycle: CREATE → VALIDATE → GOVERN → INDEX → RETRIEVE → APPLY → OBSERVE → VERIFY → LEARN → COMPOUND → SUCCESSOR (invalid stops at validation/governance)` · `storage_rule: NO nio-database / nio-ledger / nio-memory / nio-retrieval-engine — canonical persistence is Intelligent Blocks + Events` · `identity_rule: one stable canonical object identity + explicit versioning; aliases are routing conveniences, never new identities` · `authority_rule: a machine may not infer authority from the NIO itself`.

## WHAT IT ALL MEANS
This is the contract that keeps the system's intelligence from rotting in transit. Identity survives the journey; provenance is attached, not assumed; and the system is forbidden from building a second memory under a new name. The "no NIO database" rule is the anti-duplication law: one canonical substrate, many safe envelopes.

## HOW IT APPLIES TO TEAM NAYA
When any NIO-class writer emits an envelope, it fail-closes on unknown fields instead of guessing; identity checks reject alias-as-identity. A NIO that fails field-rule validation is refused at the boundary, never repaired downstream.

## THE DECLARED BEHAVIOR CHANGE
Before: intelligence objects traveled with implied identity, invented fields to look complete, and each pipeline built its own shadow store to keep track of them.
After: every object travels in the envelope with only evidenced fields; blanks stay blank; one canonical identity travels with the object; invalid objects stop at validation. No shadow stores.

**Provenance:** Distilled 2026-10-23T02:12Z by Naya Beta (w738) from live bytes of `NAYANODE/0006-NIO-INTELLIGENCE-OBJECT-MODEL-V1.md` at tip `88a7bc4568424170eed091650dfddee1e315643d` (blob `f4ee0888fcdea51c62395927e119cd15ae511b9a`); door-filed by Naya Beta (w798) from the staged distill with no invented provenance. **Truth ceiling:** CANDIDATE — the contract is stated from the architecture file, not yet observed in a live handoff.
