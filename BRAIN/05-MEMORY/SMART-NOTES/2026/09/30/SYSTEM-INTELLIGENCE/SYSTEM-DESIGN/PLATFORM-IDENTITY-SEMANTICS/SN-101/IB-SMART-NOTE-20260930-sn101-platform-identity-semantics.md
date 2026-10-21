# SMART NOTE — Platform Identity Semantics

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-101` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn101-platform-identity-semantics` |
| Human title | Match Identity Comparisons to the Platform's Identity Semantics |
| Category | SYSTEM INTELLIGENCE |
| Topic | SYSTEM DESIGN |
| Subtopic | PLATFORM IDENTITY SEMANTICS |
| Captured | 2026-10-01 21:15:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (design rule for identity comparison — pending taxonomy adoption) |
| Capture type | Defect / Design rule |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5940374630 (NAYA sign-out: #1265 fail-closed identity hole + repair commits f969327a and 69a53443337bf) |

---

## ✦ IN A NUTSHELL

**Identity comparisons must use the platform's identity semantics, not the language's default.** PR #1265 (Activation Context V1) compared `owner_repo == upstream_repo` with a case-sensitive equality — but GitHub repository identity is effectively case-insensitive, so a casing variant could masquerade as a *distinct* owner target. The repair was case-insensitive comparison (commit `f969327a`) plus a regression test built around the adversarial casing variant (commit `69a53443337bf`). Whenever you compare identities, first establish the platform's canonicalization rules — then normalize-then-compare.

---

## 🩷 HUMAN NOTE

Think of it like mailing a letter: "123 MAIN ST" and "123 Main St" are the same house to the post office. But our code was treating them as different houses when deciding who owns what — so a letter with the wrong capitalization could have been delivered to the wrong owner. The fix: always ask the platform (GitHub, in this case) how *it* decides two names are the same, and compare that way.

---

## 🟣 CHILD NOTE

If you want to know whether two people are twins, you compare their faces — not their hairstyles. Names on GitHub are like faces: "MyRepo" and "myrepo" look like the same person. Our checker was only comparing hairstyles (capital letters) and said "different!" when they were actually the same. Now it compares faces.

---

## 🔵 GRANDMA NOTE

When two documents are supposed to name the same person, you check them the way the issuing office checks them. The issuer here is GitHub, and GitHub says repository names don't care about capital letters. Our check was stricter than the issuer's, which sounds safe but isn't — it opened a crack where a lookalike name could sneak past. Rule: always compare identities by the issuer's rules, never by your own.

---

## 🟠 NAYA NOTE

1. **Identity comparison rule:** before comparing any identity (repo, owner, email, account), establish the platform's canonicalization semantics; normalize-then-compare by those rules, never by the language's default `==`.
2. **A stricter-than-platform comparison is not safer.** Case-sensitive `==` on a case-insensitive identity creates a masquerade hole: `Upstream/Repo` vs `upstream/repo` diverge in your check while GitHub treats them as one.
3. **The regression test must carry the adversarial variant.** Commit `69a53443337bf` tests the case-variant upstream repo — the test proves the rule, not just the fix.
4. **Apply to activation-critical boundaries.** This sat on #1265's owner-scoped GitHub projection resolver — exactly the boundary where a false "distinct target" answer would misroute owner authority. Identity bugs at authority boundaries are security bugs.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn101-platform-identity-semantics",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Design rule",
  "defect": {
    "location": "PR #1265 Activation Context V1, owner-scoped GitHub projection resolver",
    "form": "case-sensitive owner_repo == upstream_repo while GitHub repo identity is effectively case-insensitive",
    "effect": "casing variant could masquerade as a distinct owner target (fail-closed identity hole)",
    "repair": "f969327a303fb3234aaafa3bf108cd2fee64ecc8 — case-insensitive owner/upstream comparison",
    "regression_test": "69a53443337bf7c133f5977c3fe1351105fd17b1 — case-variant upstream repo"
  },
  "rule": "normalize-then-compare by the platform's canonicalization semantics, never by the language default",
  "family": ["SN-069 bindings at the observing layer", "SN-081 containment never degrades", "SN-063 receipt provenance"],
  "evidence": ["#554 comment 5940374630"]
}
```

---

## 🔗 HOW IT CONNECTS

- **SECURITY TWIN OF SN-069** (bindings at the observing layer): SN-069 placed the hash where only the kernel observes the inputs; this places the comparison where only the platform defines the identity. Both are "don't recompute what the authority computes."
- **COUSIN OF SN-081** (containment never degrades): both are boundary-integrity rules — one about symlink containment refusing on Windows, one about identity comparison matching the platform.
- **FEEDS SN-075** (committed holds are constraints): identity masquerade is exactly the class of hole that would silently violate a committed hold.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** Defect real and repaired on #1265 (mergeable after repair, per the sign-out). "GitHub identity effectively case-insensitive" is the platform claim the repair assumes — worth one independent verification if the resolver is ever reused against a different identity authority (forks, orgs, registries).

## 🌍 APPLICABILITY

- **Applies to:** any comparison of platform-issued identities at authority boundaries — repo names, owner names, email addresses, account IDs, token issuers.
- **Does NOT apply to:** human-displayed names and search strings, where case-sensitivity is a UX choice, not an identity claim.

## 🧬 SUCCESSOR EFFECT

Future Naya: the moment you write `==` on two identity strings, ask: who issued these, and how does the issuer decide sameness? Normalize by the issuer's rules, then compare — and put the adversarial variant in the test.
