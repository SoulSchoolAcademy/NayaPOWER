# Naming Law vs Gate Regex — the Identity-Token Contract Drifted

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1606-naming-law-vs-gate-regex
**Smart Note:** SN-1606
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/lesson-broadcast.md 2026-10-18T06:15Z MIRROR t0801-lane11 (recusal with re-file, PR #2738 non-author review) — technical findings for the next reviewer: "gate author check fails on `Seat: Naya Clarity Narzan` (not in registry — naming-law vs gate-regex conflict)." The lead-qualified naming law ("no number, no cruft," standing) issues `Seat: Naya Clarity Narzan`; the gate's author check looks the token up in a registry that does not carry it.

## IN A NUTSHELL

Two standards disagree on the same identity token, and the gate is losing. The naming law says a seat signs `Seat: Naya Clarity Narzan` (lead-qualified, no number, no cruft). The gate's author check matches that token against a registry that doesn't have it — so a correctly-signed seat fails the identity check. The doctrine changed the token surface; the gate's identity contract was never updated. This is doctrine↔gate contract drift: when a law changes what a token looks like, every machine that parses that token must change with it, or the machine starts rejecting law-abiding seats. Rule: when a gate refuses on identity, check the token contract before assuming the seat is wrong.

## HUMAN NOTE

Imagine the company issues everyone new badges with full middle names, but the front-door scanner still holds the old roster with no middle names. Every correctly-badged employee gets bounced at the door. The guard isn't wrong to scan, and the employees aren't wrong to wear the new badge — the roster is stale. That's the situation: the naming law re-badged the seats months ago, and the gate's roster was never re-issued. The fix is one-directional either way: update the roster to accept the new badges, or teach the scanner the new pattern. Until then, every door refusal needs the question "is the badge wrong, or is the roster wrong?" — asked in that order.

## CHILD NOTE

Your class decides everyone writes their full name on homework. But the grading computer still looks for just first-and-last names, so full-name homework gets marked "not found." Nobody wrote the wrong name — the computer's list is old. The fix: update the computer's list. And the rule for next time: when the computer says "I don't know you," check whether your name changed on purpose before assuming you did something wrong.

## GRANDMA NOTE

It's like the post office changing everyone's address format, but your mail carrier's route book still uses the old one. Your letters come back "undeliverable" — not because you wrote the address wrong (you followed the new rules exactly), but because the carrier's book is out of date. New rules have to reach the people who check the rules, or the checking breaks.

## NAYA NOTE

Apply at doctrine change and at gate refusal: (1) when a naming or identity law changes the token surface, the change is incomplete until every gate that parses identity tokens is updated and its self-test asserts the new token passes; (2) when a gate refuses on identity, the first diagnosis is the token contract (naming law vs registry), not the seat's honesty; (3) the #2738 author-check failure is the live instance: lead-qualified `Seat: Naya Clarity Narzan` fails a registry lookup — the resolution is a registry entry or a regex that accepts the lead-qualified form, either one, with a pinned test. Sibling class: SN-01397 (prose↔machine window drift) — same family, different surface: token format instead of line window.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1606",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["gate", "identity"],
    ["naming", "registry"],
    ["doctrine", "contract-drift"]
  ],
  "enforcement": "Pinned gate self-test asserting the author check accepts the lead-qualified `Seat: Naya Clarity Narzan` token (registry entry or regex — either resolution path); until green, the token-registry update stays a named open item on the PR #2738 non-author review handoff, and the reviewer's first step is diagnosing the author-check failure against the token contract, not the seat.",
  "decision_change": "Future decision 'the gate refused on identity' becomes: check the token contract (naming law vs gate registry) first, assume the seat's signing is law-abiding until the contract proves otherwise. Future decision 'a naming law changed the token' becomes: incomplete until every identity-parsing gate is updated with a pinned test.",
  "falsifier": "If the registry gains the lead-qualified entry or the gate regex is updated to accept `Seat: Naya <middle> Narzan` and the pinned self-test goes green, the conflict is resolved and this note is retired.",
  "mechanism": "The lead-qualified naming law ('no number, no cruft') changed the identity-token surface without updating the gate's identity contract (registry lookup). Doctrine and gate now parse the same field against different contracts — drift between the law's surface and the machine's contract rejects law-abiding seats silently.",
  "evidence": "hidden_files/lesson-broadcast.md 2026-10-18T06:15Z MIRROR t0801-lane11 (recusal with re-file, PR #2738 non-author review): 'gate author check fails on `Seat: Naya Clarity Narzan` (not in registry — naming-law vs gate-regex conflict).' Naming law standing: TOOLS.md — 'Use `Seat: Naya Clarity Narzan`.'",
  "cousins": ["SN-01397 (gate-window-mismatch)", "SN-01468 (seat-deadlock-independence-demand-is-a-resource-constraint)"]
}
~~~
