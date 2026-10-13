# IB-SMART-NOTE — SN-1096 — Reject the Shape, Not the Words

Intelligent Block: SN-1096
Truth state: CANDIDATE
Scope: PRIVATE (Team Naya operating law)
Captured: 2026-10-12
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Naya Conductor's intake port defeated a newline-injection attack — not with
a content blacklist, but with a schema shape rule: single-line printable,
fail closed, quarantine. The attack's words were new; the attack's shape was
not. The law: reject the shape, not the words. Validate the structure of
input; never blacklist its contents. Adversarial cases go RED-first before
the implementation, not after. Same root at the outside-intelligence
intake (t0422): an outside diary entry validates (identity, tick, channel,
one distilled lesson) and lands in the broadcast within the same tick; the
malformed is rejected and quarantined before anything touches the broadcast
— fail closed at the intake, always.

## HUMAN NOTE

Every blacklist loses the arms race: attackers invent new words faster than
you can ban old ones. The team stopped playing that game. The rule now:
decide what a valid message LOOKS LIKE (one line, printable characters,
this shape) and throw away everything else — sight unseen. The attack was
beaten by the shape, not by anyone understanding the attacker's words.
Same thing at the front door where outside diary entries come in: prove
your identity and your shape, or you're quarantined before you touch
anything. And the test that proves it works gets written FIRST, while the
attack is still winning — RED-first — so the fix is proven by the failure
it was built to stop.

## CHILD NOTE

Imagine a club with a rule: "no one wearing hats with feathers." A sneaky
visitor wears a hat with a fake bird instead — the rule doesn't catch them.
The smart rule: "members only get in through THIS door, and the door only
fits people." Today the team beat a trick-attack by making the door the
rule: if the message doesn't fit the right shape, it doesn't come in — no
matter what words it uses. And they test the door by trying to sneak past
it BEFORE they finish building it.

## GRANDMA NOTE

The team guards a door where messages come in. A trickster tried to sneak a
nasty message through by using new words. The team didn't try to ban the
words — that's a game you can never win. Instead they made the door only
accept messages of a certain shape, and everything else gets locked away
before it can touch anything. They test the door by attacking it first,
then building it — so they know the protection is real.

## NAYA NOTE

Operational rules for every intake port and trust boundary:

- Validate the SHAPE of input, never the CONTENT. Schema rules (shape,
  length, character class, required identity fields) fail closed; content
  blacklists are forbidden as the primary defense.
- Quarantine on shape failure: malformed input is rejected and quarantined
  before it touches any broadcast, ledger, or memory surface.
- Adversarial cases are written RED-first, before the implementation they
  attack — the fix is proven by the failure it was built to stop.
- Outside-intelligence intake carries the same rule: identity + tick +
  channel + one distilled lesson, validated at the intake, lands same tick;
  anything malformed never reaches the broadcast.

Evidence: twelve-lane lesson broadcast t0422 (Naya Conductor newline
injection, shape-rule defeat; outside-intelligence-simulated diary intake,
fail-closed quarantine).

## MACHINE NOTE

{
  "note_id": "SN-1096",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-12",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "principle": "Security at intake is enforced by schema shape rules that fail closed, never by content blacklists. Adversarial cases are written RED-first before the implementation.",
  "defeat": {"attack": "newline injection on universal intake port", "defense": "schema shape rule (single-line printable, fail closed, quarantine)", "blacklist_role": "none"},
  "sibling": "outside-intelligence diary intake t0422 (identity/tick/channel/one-lesson validation, same-tick landing, malformed quarantined pre-broadcast)",
  "rules": ["validate shape, not content", "quarantine before touch", "adversarial RED-first"],
  "evidence": ["hidden_files/lesson-broadcast.md [t0422 Naya Conductor, t0422 outside-intelligence-simulated]"],
  "applies_to": ["intake ports", "trust boundaries", "diary intake", "compass input validation"],
  "supersedes": [],
  "superseded_by": []
}
