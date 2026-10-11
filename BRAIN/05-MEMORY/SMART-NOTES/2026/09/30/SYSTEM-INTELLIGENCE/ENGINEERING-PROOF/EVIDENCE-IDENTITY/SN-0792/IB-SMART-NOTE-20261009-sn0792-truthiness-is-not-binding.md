# Truthiness Is Not Binding — a Claimed Identity Must Be Compared to a Trusted Expected Value

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0792-truthiness-is-not-binding
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6083930327 (2026-10-09T15:25:52Z, Naya sign-in finding on PR #1974 activation falsifier) — the receipt checker validated `receipt.repository` is merely non-empty and never compared it to the trusted expected repository identity; the 14-case test matrix had no wrong-repository negative control. Repair requested on #1974.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A trust validator that checks "is this field present?" is not verifying identity — it is verifying typing. The activation receipt checker on PR #1974 required `receipt.repository` to be non-empty, which means a forged receipt naming ANY repository passes. The law: a claimed identity is meaningless until it is compared against the trusted expected value. And the falsifier matrix must contain the wrong-identity negative control (a valid-looking receipt naming the WRONG repository must fail) — SN-0292's negative-control law applied to the specific mechanism of identity binding.

## HUMAN NOTE

On 2026-10-09, a sign-in audit of the activation receipt checker (PR #1974, draft) found a concrete false-acceptance gap: the checker proved the receipt NAMES a repository, not that it names the RIGHT one. Any repository string passed. The repair: bind the claim to the trusted expected repository identity and add the wrong-repository test case to the matrix — a checker that cannot catch the identity it exists to catch is a formatting check wearing a verifier's name.

## CHILD NOTE

Imagine a bouncer who checks that you HAVE a ticket, but never checks that the ticket is for THIS movie. A ticket to a different movie gets you in. A real bouncer checks: is this ticket for tonight's movie? Every checker must do that — not just "is something there," but "is it the right thing."

## GRANDMA NOTE

A lock doesn't ask if you have A key — it asks if you have THE key. Any old key that looks right won't turn it. A security check should work like a lock: compare against the exact expected thing, not just check that something was presented.

## NAYA NOTE

Operationally, for every trust-token validator I build or review: (1) every claimed identity field (repository, issuer, subject, tenant) gets compared to an explicit trusted expected value — never truthiness, never regex-shape; (2) the negative-control matrix includes the wrong-identity case (right shape, wrong value) — the exact lie the checker exists to catch (SN-0292); (3) the trusted expected values live outside the builder's reach (SN-0787) — otherwise binding is theater. When reviewing someone's checker, the first test I read is the identity test, and the second is the wrong-identity test; if the second doesn't exist, the checker's identity binding is unproven.

## MACHINE NOTE

```json
{
  "sn": "SN-0792",
  "law": "TRUTHINESS_IS_NOT_BINDING",
  "rule": "identity_claim must be compared (equality) against trusted_expected_identity; non-empty is insufficient",
  "mechanism": {
    "binding": "compare claimed identity field to trusted expected value, not truthiness or shape",
    "negative_control": "valid-shaped receipt with WRONG identity value must FAIL",
    "trusted_source": "expected values from trusted runner/config, never builder-supplied (SN-0787)"
  },
  "pipeline_state": "CANDIDATE"
}
```
