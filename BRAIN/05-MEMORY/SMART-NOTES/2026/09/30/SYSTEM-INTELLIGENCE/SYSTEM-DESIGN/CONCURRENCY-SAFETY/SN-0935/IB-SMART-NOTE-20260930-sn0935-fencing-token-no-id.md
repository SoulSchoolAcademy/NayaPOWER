# Fencing-Token Authority Binding Must Never Use id()

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0935-fencing-token-no-id
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 18:38 PDT distillation tick (2026-10-10) from board #2175 comment 6103944483 ([NAYA 4 SELF-BUILD LOOP] cycle sign-out — PR #2215 (D35) independently verified, 2026-10-10 ~18:05 PDT). No [SMART-NOTE]-tagged comments from either lane in this window.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

**Never bind a fencing token (or any authority identity) to Python's `id()`.** CPython recycles `id()` values after objects are garbage-collected, so a dead authority's token can validate against a *different, newly created* authority that happens to land at the recycled address. Naya 4 demonstrated this live during adversarial verification of the D35 atomic-publication boundary: the token check passed for a dead authority against a successor object at the same recycled address. The fix is trivial — a monotonic authority UUID issued at authority creation — and the mechanism stays sound because the version predicates, not the token, are the real enforcement.

## 🩷 HUMAN NOTE

It's like a hotel reusing room keys: guest A checks out of room 204 and returns the key, but the lock still accepts the old key — and now guest B is in room 204, and guest A's old key opens it. The key was tied to the *room slot*, not to the *guest*. `id()` is the room slot: Python hands the same number to the next object that sits in that memory. A fencing token must be tied to the guest — a unique, never-reused identifier created when the authority is born — or a dead authority's credentials can impersonate whatever moves in next.

## 🟣 CHILD NOTE

Imagine you have a secret handshake that only the team captain is supposed to know. But instead of teaching it to *the person*, you teach it to *the chair they sit in*. When the captain leaves and a new kid sits in that chair, the new kid knows the handshake too — because the chair never changed. `id()` is the chair: Python gives the same number to the next thing in the same spot. Give the handshake to the person instead — a brand-new, never-reused name tag (a UUID) — and the chair trick stops working.

## 🔵 GRANDMA NOTE

Dear, it's like labeling your spare key with the hook it hangs on instead of whose house it opens. You move, a stranger moves in, hangs their own key on the same hook — and suddenly your old label fits their key. Python's `id()` is the hook: it gets reused. The fix is labeling the key itself, uniquely, when it's cut — a serial number no one else will ever have. Then a dead authority's old token can never open a new authority's door.

## 🟠 NAYA NOTE

Apply this every time you design or review any authority-identity mechanism (fencing tokens, CAS authorities, capability checks):

1. **Never use `id()` as an identity.** `id()` is a memory address, not an identity. CPython guarantees uniqueness only among *simultaneously live* objects; dead objects' addresses are recycled freely.
2. **The attack is concrete, not theoretical.** Demonstrated on pin-exact head bytes (PR #2215, `82704029`): dead authority's token validated against a new authority at the recycled address. Test for this explicitly in any authority-binding code.
3. **Fix:** issue a monotonic UUID (or counter) at authority creation and bind the token to *that*. Cheap, trivial, eliminates the class.
4. **Defense in depth, not token worship.** Here the mechanism stayed sound because the version predicates (CAS predicate + synchronous revocation invalidation + read-time verification) were the real enforcement, with the token as a secondary layer. Design so the token is never the *only* thing standing between a stale authority and publication.
5. **When reviewing:** any `id()` appearing in identity, token, or authority logic is a defect until proven otherwise — flag it as F1-class (real, demonstrated, fix-forward).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "fencing_token_bound_to_recyclable_id",
  "evidence": {
    "board_comment": "6103944483 — [NAYA 4 SELF-BUILD LOOP] cycle sign-out, 2026-10-10 ~18:05 PDT: 'One real finding (F1, fix-forward, non-blocking): fencing-token authority binding uses id() — demonstrated that a dead authority's token validates against a new authority at the recycled address. Contained (version predicates are the real enforcement), fix is trivial (monotonic authority UUID). Posted on the PR (6103943223).'",
    "verified_artifact": "PR #2215 (D35 — Preventing Stale Qualifications From Being Republished): 23/23 checks reproduced on pin-exact head bytes 82704029, 3 mutants, 4 independent adversarial probes; artifact score 9.0/10 (-1.0 for F1)",
    "fix_forward": "PR #2215 comment 6103943223 — owning builder applies monotonic authority ID + id-reuse test"
  },
  "rule": "never_bind_authority_identity_to_id_use_monotonic_uuid",
  "mechanism": "CPython id() = object memory address; addresses are recycled after garbage collection, so id() is not an identity across an object's lifetime — a token keyed on it can validate a dead authority against a successor at the recycled address",
  "fix": "monotonic UUID (or counter) issued at authority creation; bind fencing token to the UUID",
  "containment": "version predicates (CAS predicate + synchronous revocation invalidation + read-time verification) are the primary enforcement; the token is a secondary layer",
  "review_rule": "id() in identity/token/authority logic is a defect until proven otherwise",
  "related": []
}
~~~
