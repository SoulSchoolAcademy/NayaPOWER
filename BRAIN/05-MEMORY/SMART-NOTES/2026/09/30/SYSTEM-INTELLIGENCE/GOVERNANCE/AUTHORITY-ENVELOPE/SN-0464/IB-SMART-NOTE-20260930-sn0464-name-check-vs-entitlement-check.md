# Name-Checking Is Not Entitlement-Checking

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0464-name-check-vs-entitlement-check
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Authority-side review of PR #1468 (`tools/truth_state_guard.py`, head 9b906a90), posted https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1468#issuecomment-6021859648. The guard's `authority_is_valid` accepts any non-blank `promoter` + `scope` strings; a repo-wide search found no promoter roster, allowlist, or entitlement binding anywhere in the guard. Extends the #1468 semantic-poisoning closure (elevation requires authority AND evidence, fail-closed).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A guard that verifies the promoter's *name* is non-blank proves a claim was recorded, not that the claimant was entitled to promote. `authority_is_valid` returning True for any non-empty string is authentication theater: it answers "did someone sign?" while the attack answers "was the signer allowed?" A fail-closed elevation guard must bind the named promoter against an entitlement source (authority-grant roster, scoped to the promotion) — otherwise the poisoning hole it was built to close is still open to anyone who can type a name.

## HUMAN NOTE

Shawn's rule is that nobody gets authority from intelligence alone — authority comes from him. This note is the mechanical version of that: when code checks "who says so," it must also check "were they allowed to say so." The #1468 guard got the first half right (fail-closed, authority AND evidence, replay protection) but the authority half only checks that a name was written down. Any name passes. That's like a bouncer who checks that your ID has a name on it but never checks the guest list. The fix is small — check the name against the list — but without it, the door is decoration.

## CHILD NOTE

Imagine a clubhouse where the rule is "only members can put stars on the chart." The guard at the door asks everyone "what's your name?" and writes it down — but never looks at the member list. Anyone who says a name gets in. Writing down names is not the same as checking membership. Always check the list.

## GRANDMA NOTE

It's like signing for a package: the delivery person checks that you wrote *a* name, but never checks whether you're the person who ordered it. A signature without checking who you are doesn't prove anything. Always match the name to someone allowed.

## NAYA NOTE

Future Naya: whenever you review or build an authorization check, ask the two questions separately: (1) is the claimant identified? (2) is the claimant *entitled*? A check that answers only (1) is a claim recorder, not an authorization gate. For promotion/elevation paths specifically: bind `promoter` to the authority-grant source (the grant table, a roster, a scoped capability) and fail closed when the binding is absent. "Non-blank string" is never an entitlement proof. When you find a name-check standing alone, flag it as an open hole — politely, with the exact line — and do not call the gate closed until the entitlement binding lands.

## MACHINE NOTE

```json
{
  "sn": "SN-0464",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "principle": "name_check_is_not_entitlement_check",
  "evidence": {
    "review": "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1468#issuecomment-6021859648",
    "guard": "tools/truth_state_guard.py @ coda1/truth-state-poison-closure 9b906a90",
    "finding": "authority_is_valid accepts any non-blank promoter+scope; no roster/allowlist/entitlement binding found in guard"
  },
  "rule": "elevation guards must bind named promoter to an entitlement source; fail closed when binding is absent",
  "smart_link": "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1468#issuecomment-6021859648"
}
```
