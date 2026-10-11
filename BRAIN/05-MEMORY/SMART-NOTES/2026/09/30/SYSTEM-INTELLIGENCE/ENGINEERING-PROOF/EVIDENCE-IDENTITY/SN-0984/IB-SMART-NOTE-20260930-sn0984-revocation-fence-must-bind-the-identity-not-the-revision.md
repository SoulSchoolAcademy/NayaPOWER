# Revocation Fences Must Bind the Identity, Not the Revision

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0984-revocation-fence-must-bind-the-identity-not-the-revision
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/EVIDENCE-IDENTITY

## IN A NUTSHELL

While wiring the D36 revocation-ordering mechanism, the wire lane found a hole in the engine: `register_evidence` **unconditionally overwrites a revoked record with `eligible=True` at a new revision**. The fence is revision-scoped, not identity-scoped — and the RLQ-1 abstract model has no re-register transition at all. Re-registering a revoked evidence id re-qualifies it, verified live. The lane did not adjudicate intent ("intended or laundering hole" is D39's question); the gate asserts only specified behavior.

The durable rule: **a revocation that binds only the revision leaves the identity re-registerable.** Any state that can be re-entered by a version bump is not a state at all — it's a receipt with an expiration loophole. Revocation must bind the *identity* (this evidence id is revoked, at every revision) or the launder path is trivial: bump the version, get a clean qualification. This is the evidence-identity twin of the merge discipline "decisions expire when the tip moves" — there, the *rule* moves with time; here, the *hole* moves with the revision counter.

## HUMAN NOTE

Shawn — a lane wiring the revocation machinery found that revoked evidence can be brought back to life just by re-registering it under a new revision number: the system marks it eligible again, no questions asked. The revocation fence checks versions, not identities. Lesson banked: if revocation doesn't stick to the *identity* of the evidence, a version bump launders it. The owning lane (Naya 5 / D39) has the question now — intended behavior or hole — but the pattern is worth banking either way.

## CHILD NOTE

You take away a toy because it's broken — but the rule only says "the blue toy box is closed," and your friend just puts the toy in a red box and says "see, it's fine now." The toy is still the same broken toy. Rule: when you revoke something, the rule has to stick to the *thing itself*, not the box it's in — or someone will just change the box.

## GRANDMA NOTE

Like banning someone from the kitchen but letting them back in with a new name badge — the badge changed, the person didn't. A ban that attaches to the name tag instead of the person isn't a ban; it's paperwork. If you revoke something, the revocation has to follow the thing itself, no matter how many times it gets re-labeled.

## NAYA NOTE

This is one I want in my revocation checklist permanently. When I implement or review any revocation, withdrawal, or eligibility-removal mechanism, I ask: *what is the fence bound to?* If it's bound to a revision, a version, a snapshot — anything that advances — then re-entry is a one-line operation and the fence is theater. The D36 finding is the concrete instance: `register_evidence` overwrites a revoked record with `eligible=True` at a new revision, unconditionally; the RLQ-1 model has no re-register transition, so the hole is both a code bug and a spec gap. The honest move the wire lane made is also worth copying: they shipped the gate asserting *only specified behavior*, named the hole, routed the intent question to the owning lane (Naya 5 / D39), and did not unilaterally adjudicate. Bind the identity; assert only what's specified; route the intent question with evidence.

## MACHINE NOTE

```json
{
  "sn": "SN-0984",
  "slug": "revocation-fence-must-bind-the-identity-not-the-revision",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "EVIDENCE-IDENTITY"],
  "authority": "distillation tick 2026-10-11 06:38 PDT, CANDIDATE (auto-capture, not ratified)",
  "evidence": {
    "board_comment": "#2175 comment 6109275453 (2026-10-11T12:59Z — WIRE lane D36 sign-out, night shift)",
    "finding": "register_evidence unconditionally overwrites a revoked record with eligible=True at a new revision — verified live",
    "scope_of_fence": "revision-scoped, not identity-scoped; RLQ-1 abstract model has no re-register transition",
    "routing": "intended or laundering hole — D39's question (Naya 5), not adjudicated by the wire lane; gate asserts only specified behavior"
  },
  "rule": "revocation_must_bind_the_identity_not_the_revision",
  "procedure": [
    "on any revocation/withdrawal mechanism, ask: what is the fence bound to?",
    "if the fence binds a revision, version, or snapshot, demonstrate the re-registration launder path",
    "bind the identity: revoked evidence id stays revoked at every revision",
    "if intent is ambiguous (feature vs hole), ship asserting only specified behavior and route the intent question with evidence — never adjudicate unilaterally"
  ],
  "related": ["D32-D36 revocation directive family", "SN-0823 (reports expire when the tip moves — the time-twin of this revision-twin)"]
}
```
