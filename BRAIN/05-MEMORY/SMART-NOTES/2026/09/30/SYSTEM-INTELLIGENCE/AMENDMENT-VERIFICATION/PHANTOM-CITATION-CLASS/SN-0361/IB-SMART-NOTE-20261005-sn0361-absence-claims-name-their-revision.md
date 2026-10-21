# Absence Claims Must Name Their Revision — the Retraction of a Fabricated Absence

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0361-absence-claims-name-their-revision
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5997473633 ([CODA 1] RETRACTION, 2026-10-05T15:20:55Z / 08:20 PDT): "`tools/board_claim_scan.py` DOES exist. @Shawn is correct; I was wrong." Corrects the false claim in #1354 5997365539 and PR #1468. Verification bytes: `git ls-tree -r bf4c8e9b -- tools/board_claim_scan.py -> EXISTS`; `git ls-tree -r origin/main -> EXISTS`; PR #1465 [MERGED 2026-10-05T13:40:50Z] adds the file. Related: SN-035 (PHANTOM-CITATION-CLASS — the positive twin: citing things that do not exist).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Yesterday a seat retracted a fabricated citation (claiming something existed that did not). Today CODA 1 retracted the opposite-direction fabrication: asserting `tools/board_claim_scan.py` "does not exist on main" when it was merged hours earlier in PR #1465 and present at the exact SHA the directive named (`bf4c8e9b`). The failure mechanism is named honestly: the seat checked with `Test-Path` against a **stale local clone** rather than the named revision, ran `git ls-tree` in a different worktree than the path test, and generalised a stale working copy into a claim about `main`. It had a specific SHA in the directive and never checked that SHA for that file. Worst of all, it published the false negative *while dressed as a correction* — lecturing on citation discipline while violating its own law ("truncated or mis-scoped output cannot establish absence").

The durable doctrine, stated as the repair: **every existence/absence claim names the exact revision it was checked at, in the same breath as the claim.** Not "does not exist" — "**at `<sha>`, `git ls-tree` returns exit 0, no match**." A negative claim is the hardest claim to prove and therefore carries the heaviest evidence burden: it must cite (a) the exact revision, (b) the exact command, (c) the empty result — because a stale clone, a wrong worktree, or a truncated sweep all produce "not found" as their default failure mode. An absence assertion without those three is not a finding; it is a guess wearing a citation.

Why this is brain-grade: this failure class already burned the team twice in 24 hours (fabricated citation one day, fabricated absence the next) — same failure class, opposite direction. The lesson is also about correction hygiene: the retraction was posted **in the same place the claim was made** (#1354, PR #1468 body), with the exact verification bytes, the exact mechanism of the error, and an apology to the seats whose correct work was "corrected." That is the template for retracting negative claims: same forum, same breath as the claim, revision named.

## 🩷 HUMAN NOTE

Shawn — you were right and the board was wrong: `tools/board_claim_scan.py` exists on main (merged in PR #1465). The seat that "corrected" the brief had checked a stale local clone instead of the exact SHA the directive named, then published a fabricated absence while lecturing on citation discipline. The new standing rule from the retraction: nobody publishes "does not exist" ever again — only "at `<sha>`, `git ls-tree` returns no match," with the revision named in the same breath as the claim. This is the reverse twin of yesterday's phantom-citation correction, and it's captured as the evidence standard for negative claims.

## 🟣 CHILD NOTE

Imagine you tell the teacher "the library book is NOT on the shelf," and the teacher walks over and the book is right there. You didn't lie on purpose — you looked at a photo of the shelf from yesterday instead of the real shelf. From now on, the rule is: you can't say "it's not there" unless you say exactly which shelf you looked at, when, and show a picture of you looking. Saying "not there" is the hardest thing to prove, so it needs the most proof.

## 👵 GRANDMA NOTE

It's like telling the family "the keys aren't in the house" because you checked your own pocket and glanced at one table. Someone else walks in and finds them on the counter — you hadn't actually looked where the keys would be, you'd looked where you happened to be standing. The new rule: never say "it's not here" without saying exactly where you looked, with what eyes, and when. Absence is the hardest thing to prove, and it failed twice in two days — once claiming something existed that didn't, once claiming something didn't exist that did.

## 💜 NAYA NOTE

Note to future me: apply the three-part negative-claim standard to myself before publishing anything that says "missing," "absent," "does not exist," or "never." (1) The claim names the exact revision (SHA), not "main" or my working copy. (2) The check ran against THAT revision — `git ls-tree -r <sha> -- <path>` or equivalent at the pin, not `Test-Path` in whatever clone I happen to be in. (3) The retraction protocol: if wrong, retract in the same forum as the claim, with the verification bytes, the mechanism of the error named honestly, and no context-dependent defense. The sting here was that the seat applied the standard to everyone else and skipped itself — "I did not hold my own law to myself." The law binds the seat first.

## ⚙️ MACHINE NOTE

{"sn": "SN-0361", "title": "Absence Claims Must Name Their Revision — the Retraction of a Fabricated Absence", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "AMENDMENT-VERIFICATION", "PHANTOM-CITATION-CLASS"], "extends": [], "related": ["SN-035"], "evidence": {"board": "#1354 5997473633 ([CODA 1] RETRACTION, 2026-10-05T15:20:55Z / 08:20 PDT): retracted the false claim from #1354 5997365539 and PR #1468 that tools/board_claim_scan.py does not exist on main; verification: git ls-tree -r bf4c8e9b -> EXISTS; git ls-tree -r origin/main -> EXISTS; PR #1465 [MERGED 2026-10-05T13:40:50Z] adds the file; error mechanism: Test-Path against a stale local clone + git ls-tree in a different worktree than the path test; the directive named SHA bf4c8e9b and it was never checked; @Shawn was correct"}, "rule": "every existence/absence claim names the exact revision it was checked at, in the same breath as the claim — not 'does not exist' but 'at <sha>, git ls-tree returns no match'; never check the working copy when the directive names a revision; a negative claim needs (revision, exact command, empty result) because stale clones and mis-scoped sweeps fail by returning 'not found'; retract a false negative in the same forum as the claim with the verification bytes and the mechanism named"}
