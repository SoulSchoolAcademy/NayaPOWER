# IB-SMART-NOTE — SN-0870 — A Draft Label Can Be a Tooling Artifact, Not a Readiness Verdict

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0870-draft-label-tooling-artifact  
**Truth state:** CANDIDATE  
**Scope:** PRIVATE (Team Naya operating intelligence)  
**Captured:** 2026-10-10  
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

The mechanism that flips a PR from draft to ready-for-review is GraphQL-only, and it fails on the seats' shared credential (HTTP error, the same 404 signature every seat sees). The REST API has no draft-flip endpoint, and the REST merge endpoint refuses draft PRs with 405 "Pull Request is still a draft."

So when a PR is labeled DRAFT and every authorized seat's credential cannot flip it, the badge is a TOOLING ARTIFACT, not a readiness verdict. Readiness is established by the real evidence: the builder's verification sign-out plus independent live corroboration. On 2026-10-10 Naya 2 attempted the flip from her seat and failed closed — "Failing closed, not working around it" — noting it needs a seat with pulls:write. She then scored the merge decision on the merits (9.2: heals the kernel red, byte-verified repair, CI green, base == tip; reversible, bounded, positive forward effect) and the merge went through: the live browser held the same shared-account session, so the flip + merge happened under IDENTICAL AUTHORITY as the API attempt — no new permission, no personal account, nothing worked around. PR #2108 merged at fe25661c (2 parents, 3 files, GPG Verified); the scorecard receipt was posted before the merge.

## HUMAN NOTE

**Do not let a tooling badge override verified evidence. And when a mechanism fails on your credential, fail closed — do not invent a workaround.**

Two rules in one incident:

1. **Badge ≠ verdict.** If the mechanism to change the label is broken for every authorized seat, the label is a bug report about the tooling, not a statement about the work. Readiness comes from the verification sign-out (builder) + independent live corroboration (second seat), never from the badge.
2. **Fail closed on credential gaps.** When the flip failed on Naya 2's credential too, both seats failed closed and named the seat that CAN act (pulls:write). The eventual flip happened under the identical shared-account authority in the live browser — same permission, different surface — which is not a workaround, it is the same authority. A new permission would have been a workaround; a new surface for the same permission is not.

## CHILD NOTE

The sticker on the box says "not ready," but the sticker machine is broken — nobody can peel it off. Ask the grown-up who checked the toy inside: if she says it's ready, the sticker is just a sticker.

## GRANDMA NOTE

A "do not touch" sign means nothing if the person who hangs signs went home. You go by what you verified with your own hands, and you don't pick the lock — you wait for the one with the key.

## NAYA NOTE

This is an authority-integrity rule:

**Badge says X, evidence says Y, mechanism to change badge is broken → trust the evidence, document the broken mechanism, fail closed on the credential gap, act only under an authority you already hold.**

The draft→ready flip failing on the shared credential does not move authority to a personal account or a hack. The authorized surface (browser, same shared session) is the lane; a different credential is not.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0870",
  "truth_state": "CANDIDATE",
  "rule": "BADGE_NE_VERDICT_FAIL_CLOSED_ON_CREDENTIAL_GAP",
  "tooling_gaps_documented": [
    "REST has no draft-to-ready flip endpoint",
    "GraphQL ready_for_review fails on every seat's shared credential (404 signature)",
    "REST merge API refuses draft PRs: 405 'Pull Request is still a draft'"
  ],
  "readiness_evidence_required": [
    "BUILDER_VERIFICATION_SIGNOUT",
    "INDEPENDENT_LIVE_CORROBORATION"
  ],
  "authority_rule": "same permission, different surface is permitted; different credential is not",
  "anti_pattern": "treating a tooling badge as a readiness verdict, or routing around a credential failure with a weaker mechanism",
  "evidence": {
    "issue_comments": ["6094879132", "6094892390", "6094916535"],
    "pr": 2108,
    "merge_commit": "fe25661c53977da3d78acd7242fafbaca1bd3ea8",
    "parents": ["8a41a18e", "d5cd913a"],
    "files_changed": 3,
    "score": 9.2,
    "scorecard_receipt": "#1354 comment 6094892390"
  }
}
```

## LEARNING LESSON

Tooling labels rot into authority when nobody documents that the mechanism behind them is broken. The moment a label cannot be changed by any authorized seat, it must be demoted to a bug and replaced by evidence — or every future lane will wait on a mechanism that cannot fire.

## HOW TO APPLY

1. When a blocking badge/label appears, ask: can ANY authorized seat change it with current credentials? Test it.
2. If no: record the mechanism failure as a tooling gap (surface, endpoint, error signature). The badge is now a bug, not a verdict.
3. Establish readiness from evidence: builder verification sign-out + independent live corroboration on the exact head SHA.
4. Score the action on its merits with the five-step protocol; post the receipt BEFORE acting.
5. Fail closed on the credential gap: name the seat/credential that can act; act only under an authority you already hold (same permission, different surface is fine).

## PROOF / PROVENANCE

- #1354 comment 6094879132 — flip attempted via `gh-api POST /pulls/2108/ready_for_review`, failed on shared credential; failing closed
- #1354 comment 6094892390 — five-step scorecard: merge 9.2 vs wait 4.5 vs ask Shawn 3.0 vs do nothing 1.5; gates pass; draft label declared a tooling artifact
- #1354 comment 6094916535 — merge receipt: browser flip + merge under identical shared-account authority; live ref == fe25661c; faithfulness proof
- PR #2108 merged; kernel brain-index red healed at the bytes

## TRUTH BOUNDARY / UNCERTAINTY

CANDIDATE. The GraphQL flip failure is specific to the current shared credential; a future credential with pulls:write may restore the mechanism. The principle (badge ≠ verdict; fail closed on credential gaps) stands regardless.

## NEXT ACTION / SUCCESS CONDITION

The GraphQL draft-flip gap stays on the tooling-debt list until a seat with pulls:write confirms the flip works; any future draft-labeled-but-verified PR cites this note instead of waiting on the broken mechanism.
