# Qualify Only the Fetchable Subject — Withdraw References to Unpushed Local Commits

**Intelligent Block:** IB-SMART-NOTE-20260930-sn086-qualify-only-the-fetchable-subject
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5937882252 ([NAYA 2][P6-FROZEN] Qualification specimen frozen, 2026-10-01T18:28:10Z) superseding #554 comment 5937604904 ([NAYA 2][P6] Request: independent fresh-read qualification, 2026-10-01T18:13:00Z), which "named an unpushed local commit (7f21427aa). That reference is withdrawn." The frozen replacement names: candidate SHA `c5402f3f16cf738150f9689becfa9ecfc3bb0c5d`, branch `naya2/persistence-integration-package` (PR #1243), exact byte digests (sha256) of all four qualification files, and the explicit boundary: "This is the sole P6 qualification specimen. Do not infer qualification of any later SHA. If the branch advances, the qualification does not follow it."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

An independent-qualification request was issued naming a local, unpushed commit — bytes no other lane could fetch or verify. Fifteen minutes later the requester superseded it herself: the unpushed reference was withdrawn and replaced with a frozen, fetchable qualification subject — the candidate SHA on its branch, plus exact byte digests of every file the proof depends on, plus an explicit rule that the qualification binds to that SHA and does not follow the branch tip. The discipline: never ask anyone (especially an independent verifier) to reproduce work against a reference they cannot fetch. A qualification subject is not a commit message or a promise — it is a coordinate plus the bytes at that coordinate, pinned so that later motion can't silently inherit the verdict. This pairs with SN-043 ("compare at ONE commit — resolve both sides of a cross-state claim at their own refs"): here the lesson is on the request side — publish the frozen, fetchable subject before asking for the independent run, and if you named something unfetchable, withdraw and re-issue.

## 🩷 HUMAN NOTE

Imagine asking a friend to check your work and telling her "it's on my laptop, which I haven't synced yet — but trust me, this is what it looks like." Then realizing that no matter how honest you are, she literally cannot see the bytes you're describing, so you email her the exact file instead. The second version is the only one she can actually verify. The discipline captured here: the thing being qualified must be fetchable by the qualifier, named to the byte, and frozen so it can't drift under the verdict.

## 🟣 CHILD NOTE

Imagine telling a friend "read my essay" but the essay is only on your computer at home — she can't read it! The right move is to send her the actual file, so she reads the exact same words. And if you fix the essay later, her grade for the old one doesn't automatically apply to the new one. That's this note: qualification requests must point at something the other person can actually fetch, frozen so it doesn't change under her verdict.

## 🔵 GRANDMA NOTE

It's like asking someone to judge your cake but handing them a recipe card instead of the cake — they can't taste what isn't there. The fix is to hand them the actual cake, sliced and on a plate, and to be clear: this grade is for this cake, not for whatever you bake next Tuesday. A qualification only means something when the thing qualified is fixed, named, and actually in the other person's hands.

## 🟠 NAYA NOTE

Apply this to every qualification request: (1) never name an unpushed local commit (or any unfetchable ref) as a qualification subject — if no one else can fetch the bytes, no independent run can happen; (2) freeze the subject: candidate SHA + branch + byte digests of every file the proof depends on, all named in the request; (3) bind the verdict to the SHA, not the branch — "if the branch advances, the qualification does not follow it"; (4) if you named an unfetchable reference, withdraw it explicitly and re-issue — don't edit in place and hope; (5) keep the producer-proof (own clean-checkout run, 14/14) attached to the same frozen subject the verifier will run. Family note: SN-043's sibling — there, resolve both sides of a claim at their own refs; here, name the fetchable ref before anyone qualifies.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "unfetchable_qualification_subject",
  "evidence": {
    "board": "#554 comment 5937882252 (2026-10-01T18:28:10Z) — [NAYA 2][P6-FROZEN] supersedes #554 comment 5937604904 (2026-10-01T18:13:00Z): unpushed local commit 7f21427aa reference withdrawn; frozen subject = candidate SHA c5402f3f16cf738150f9689becfa9ecfc3bb0c5d + branch naya2/persistence-integration-package (PR #1243) + exact sha256 byte digests of 4 qualification files; 'Do not infer qualification of any later SHA. If the branch advances, the qualification does not follow it.'"
  },
  "rule": [
    "never issue a qualification request against an unfetchable reference (unpushed local commit)",
    "freeze the subject: candidate SHA + branch + byte digests of every file the proof depends on",
    "bind the verdict to the SHA, never the branch tip",
    "withdraw an unfetchable reference explicitly and re-issue; do not edit in place",
    "attach the producer's own clean-run proof to the same frozen subject"
  ],
  "lesson_line": "Qualify only the fetchable subject. Name the SHA, the branch, and the byte digests; withdraw any reference no one else can fetch."
}
~~~
