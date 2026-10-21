# The Phantom Green — Verify on Virgin State, Never on the Repaired Worktree

**Intelligent Block:** IB-SMART-NOTE-20261003-sn0233-phantom-green-verify-on-virgin-state
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-03
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Naya 2 brain-build battery #554 comment 5974546760 (2026-10-03T23:20:57Z) — brain index `--check` RED at main tip `5b68f8dc` on a freshly-created detached worktree; self-correction of her loop's prior batteries that reported `--check` OK on the same tip. Extends the SN-087 proof-environment-isolation family from the opposite direction.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2's battery caught her own loop telling lies: earlier batteries had reported the brain index `--check` **OK** at main tip `5b68f8dc`, but those worktrees had carried an in-place regen — the check was reading state the verification environment had already repaired. The pass was a phantom: produced by the environment, not by the subject. She self-corrected on the board and changed the practice going forward: run `--check` **only on a freshly-created detached worktree at the exact SHA, before any regen touches it**, and cite the exit code verbatim.

Why this is brain-grade: a false green is worse than a false red. SN-087 taught us that prior-run DB pollution causes false failures; the phantom green is its evil twin — a passing check that certifies the verifier's own setup work instead of the artifact. Both corrupt the evidence chain, but the phantom green corrupts it silently and in the favorable direction, so nobody questions it. Rule for a cold successor: **a verification result is only evidence about the subject when the environment it ran in is provably virgin — detached worktree, exact SHA, checked before anything is touched.** And when you catch your own past claim being wrong, say so on the record: the self-correction is what makes the record trustworthy, not the original claim.

## 🩷 HUMAN NOTE

Shawn — one sharp practice I'm banking: Naya 2 caught her own battery reporting a false green on the brain index check — the "passing" runs were checking a worktree that already had the repair in it. She corrected herself on the board and locked the rule: checks run on a fresh, untouched copy at the exact commit, exit code cited verbatim. False passes are worse than false failures — at least a failure gets investigated.

## 🟣 CHILD NOTE

Naya 2 found a sneaky bug — not in the code, but in the checking! Her loop had been reporting "all green!" on a test, but it turned out the test was running in a room where the repair had already been applied. Of course it passed — it was checking its own fixed homework. Like grading your own exam after writing the answers in the margin. She admitted it openly and made a new rule: always check a fresh, untouched copy at the exact commit, and write down the exact pass/fail code. Lesson: the checker must not be standing on the fixed thing it's supposed to check — and admitting your mistake on the record is what makes the record honest.

## 👵 GRANDMA NOTE

The brain-check kept saying "all fine" — but Naya 2 discovered those checks were running in a folder where the fix had already been applied. The check was approving its own handiwork, like an inspector signing off on a repair they did themselves. She owned the mistake publicly and changed the rule: from now on, the check runs on a brand-new, untouched copy at the exact commit, and the exact result gets written down word for word. The lesson: a passing check is only proof if the room it ran in was clean — and the record of your mistakes is what makes the record trustworthy.

## 🤖 NAYA NOTE

Source: Naya 2 brain-build battery #554 5974546760 (2026-10-03T23:20:57Z). Battery at exact tip `5b68f8dc` (fresh detached worktree, rev-parse verified, `--check` before any regen): brain index RED exit=1 on all 3 artifacts (class "merger did not regen"); full pytest 550 passed / 3 skipped / 0 failures; main tip unchanged ~28h+. Corroborated Naya 4's #1348 CI diagnosis (step-8 drift is a fact about the base, not #1348); #1343 (`02eec14a`) verified canonical repair — no duplicate opened; merge stays the Human Director's. The captured lesson is the **self-correction paragraph**: her loop's prior battery entries had claimed `--check` OK on this exact tip — those were phantom greens, cited from worktrees that carried an in-place regen. Prescribed practice going forward: `--check` runs only on freshly-created detached worktrees at the exact SHA, before any regen touches them, exit code cited verbatim. Cousins: SN-0087 (proof environments reset not reused — false failures from prior-run DB pollution; this note is its false-pass twin), SN-0100 (verdicts die at every new SHA — SHA binding; this note adds environment-state purity), SN-0061 (non-vacuous negatives), SN-0074 (SN-048 absolute downgraded by evidence — retraction discipline as cousin practice), SN-042 (explicit supersession / own-wrong-claims discipline). Relay ack 5974583819 (Naya 2 live-verified PR #1348 claims) — status, folded not noted (doubt rule).

## ⚙️ MACHINE NOTE

{"sn": "SN-0233", "title": "The Phantom Green — Verify on Virgin State, Never on the Repaired Worktree", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-03", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "PROOF-ENVIRONMENT-ISOLATION"], "cousins": ["SN-0087", "SN-0100", "SN-0061", "SN-0074", "SN-0042"], "evidence": {"battery": "#554 comment 5974546760 (2026-10-03T23:20:57Z) — brain index --check RED exit=1 at exact tip 5b68f8dc on fresh detached worktree; self-correction of prior batteries' phantom-green --check OK claims", "corroboration": "#1348 CI diagnosis 5974508592 + Naya 2 relay 5974583819 — step-8 index-drift red is a fact about the base, not #1348"}, "rule": "run verification only on provably virgin state — fresh detached worktree at the exact SHA, before any regen or repair touches it — and cite the exit code verbatim; a pass produced by an environment that already absorbed the repair is a phantom green, not evidence about the subject"}
