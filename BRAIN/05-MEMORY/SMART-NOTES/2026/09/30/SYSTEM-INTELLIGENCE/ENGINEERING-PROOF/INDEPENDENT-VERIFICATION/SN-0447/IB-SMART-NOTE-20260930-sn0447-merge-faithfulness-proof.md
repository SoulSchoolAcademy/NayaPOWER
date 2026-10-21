# The Merge-Faithfulness Proof — MERGED Is Not MERGED-VERIFIED

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0447-merge-faithfulness-proof
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6014940038 (Naya 4 self-build 04:03–04:40 PDT cycle SIGN-OUT — post-merge verification of #1348, H9-1 EVOLVE first executable, squash-merged 2026-10-05T03:02Z as `04524d15`, verified at tip pin `adfa1d05`, 2026-10-06T11:08:57Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A squash merge rewrites history — the PR head SHA is gone forever, so "PR #1348 merged" says nothing about what is actually in the tip. Naya 4's 04:03 PDT cycle turned MERGED into MERGED-VERIFIED-AT-TIP with a four-step mechanical proof on #1348: (1) **Ancestry** — the compare API shows merge commit `04524d15` is a direct ancestor of tip `adfa1d05` (ahead 152, behind 0, merge_base == the merge commit); (2) **Zero drift** — every artifact's blob SHA is identical at PR head, merge commit, and tip (migration blob `f7c7a46408eb46c1…`, verify.sql blob `030f108661f6e345…`); (3) **Honest CI read** — `test`, `chain-readiness-gate`, `preflight`, `cvo-runtime`, `independent-verification` SUCCESS on the merge commit, Workers Builds x2 flagged as pre-existing infra noise, behavioral jobs skipped by design — cited as SN-0421 evidence boundary, never inflated; (4) **Ledger recompute** — `20261003170000` PRODUCTION_APPLIED with sha256 / 6047 bytes / 4 statements all exact vs recomputed at tip. Result: #1348 is source-faithful at tip; the evidence gap narrowed from "unapplied + unexecuted" to "unexecuted" (live invocation still pending, named as the next governed action).

Why this is brain-grade: the evidence law says merged ≠ verified, and this is the mechanical procedure that turns the left side into the right side. A cold Naya inheriting "PR merged" must never assert the content is in the tip without this proof — a merge ref pointing at a SHA proves the pointer moved, not that the content survived the squash. The four steps are cheap, API-native, and lane-agnostic; they apply to every PR, every seat, every node. Skipping them converts a claim (merged) into a conclusion (deployed-and-working) — exactly the fabrication the evidence law forbids.

## 🩷 HUMAN NOTE

Shawn — one clean verification recipe from the self-build lane: "merged" is not "verified." Your first EVOLVE executable (#1348) was squash-merged, which rewrites history — so the lane ran a four-step proof: the merge commit is a direct ancestor of the tip, every file's fingerprint is byte-identical across the PR head, the merge, and the tip, the CI was read honestly (green tests, skipped behavior jobs flagged as "not behavioral evidence"), and the ledger was recomputed against reality. It passed — #1348 is genuinely in the tip. Banked rule: every future merge gets this proof before anyone says it's in; a merge ref is a claim, the four-step proof is the verification. The remaining gap is named, not hidden: the executable has never been invoked live — that's the next governed action.

## 🟣 CHILD NOTE

Imagine you mail a letter by putting it in a new envelope (that's a squash merge — same letter, new envelope). "The letter was mailed" doesn't prove the letter inside is still the same letter you wrote. So you check: (1) the new envelope is really on the truck going to your friend's house; (2) the words inside are letter-for-letter identical to what you wrote; (3) the post office's inspection stamp is real; (4) your notebook copy matches too. Only then do you say "the letter arrived." If any check is skipped, you're guessing, not knowing. A cold Naya never guesses about what's in the tip.

## 👵 GRANDMA NOTE

A shipping company says your package was delivered — but the address label was rewritten along the way (a squash merge). You don't take their word for it; you check four things: the delivery truck's route really included your street, the contents match your packing list exactly, the driver's receipt is genuine, and your own copy of the order matches what arrived. Each check is simple. Together they prove the package is yours, not just that a truck drove by. "Delivered" is a claim; the four checks are the proof. Never spend a claim as if it were proof.

## 💜 NAYA NOTE

Note to future me: whenever a PR is merged and the question is "is its content in the tip?", run the four-step merge-faithfulness proof before asserting anything: (1) `compare` — merge commit must be an ancestor of the tip (ahead > 0, behind == 0, merge_base == merge commit); (2) `git ls-tree` / blob SHAs — every artifact byte-identical at PR head, merge commit, and tip; (3) CI on the merge commit — read which jobs ran, name the skipped ones, cite SN-0421 for the behavioral boundary; (4) recompute the ledger's claims (sha256/bytes/statements) at tip. Cheap, API-native, no credentials, no judgment calls. The verdict vocabulary is exact: MERGED-VERIFIED-AT-TIP (source-faithful), never just "merged." And when the proof leaves a gap — here, "never invoked live" — narrow it by name in the sign-out with the next action and the authority check it needs, never by silence.

## ⚙️ MACHINE NOTE

{"sn": "SN-0447", "title": "The Merge-Faithfulness Proof — MERGED Is Not MERGED-VERIFIED", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INDEPENDENT-VERIFICATION"], "cousins": ["SN-0421", "SN-0439", "SN-0441", "SN-0445"], "authority": "observed episode — Naya 4 self-build 04:03 PDT cycle, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#1354 6014940038 (Naya 4 self-build 04:03–04:40 PDT cycle SIGN-OUT — post-merge verification of #1348 at pin adfa1d05, 2026-10-06T11:08:57Z)"], "state": "merge commit 04524d15 (squash of #1348, 2026-10-05T03:02Z) direct ancestor of tip adfa1d05; migration blob f7c7a46408eb46c1… and verify.sql blob 030f108661f6e345… identical at PR head/merge/tip; CI SUCCESS on merge commit for test, chain-readiness-gate, preflight, cvo-runtime, independent-verification; ledger 20261003170000 sha256/6047B/4stmts exact at tip"}, "doctrine": {"merged_not_verified": "a squash merge rewrites history — 'merged' is a pointer move, MERGED-VERIFIED-AT-TIP is the four-step proof: ancestry, zero-drift blob equality, honest CI read, ledger recompute", "applies_everywhere": "lane-agnostic, PR-agnostic, node-agnostic — run the proof for every merge before asserting content is in the tip", "name_the_gap": "a proof that narrows the gap (unapplied+unexecuted → unexecuted) reports the remainder with its next action and authority check — never silences it", "family": "evidence law (merged ≠ verified) :: SN-0421 (skipped jobs aren't behavioral evidence) :: this (the mechanical procedure between the two)"}}
