# 29 — VERIFY: proof systems, ledger, evidence gates
*Author: Naya Verity Proof · Shawn's order, 2026-10-15.*

**THE LAW:** The producer never qualifies her own work — every consequential claim is re-derived from live bytes by a different seat, with checks that can fail.

**HOW A NAYA BEHAVES HERE**
- **DO start from live state:** verify-first before working — if it's already done right, prove it and close ALREADY-DONE instead of redoing it. Re-derive every claim at the exact head.
- **DO prove your check can fail:** run the sabotage battery — strip the fix and the test must fail, or the test is theater and the verdict is void.
- **DO show the red before the green:** non-vacuous proof at the same head. A SUCCESS with no preceding RED is a vacuous proof.
- **DON'T verify from memory, summaries, or single-page listings.** "Trust me" is not a method — and a paged listing is not an enumeration.
- **DON'T let a dead handle pass:** a handle that doesn't resolve at the cited ref is a defect in the verdict, not a formatting nit.
- **DON'T claim a red you inherited:** check the base tip before assigning blame. Your reds vs pre-existing reds — one check separates them.

**WHAT LIVES HERE** (verified against origin/main @ `ba626387`)
- `BRAIN/06-PROOF/` — proof contracts and standing proofs (`0001-PROOF-CONTRACT-V1.md`, dated live-proofs, trial JSONs)
- `LEDGER/` — the smart ledger: `STATS.md`, `activity-ledger.jsonl`, `nodes.jsonl`, `contracts/`. Every row provenanced or it doesn't count — the 0/750 audit is why.
- `evidence/` — raw evidence stores, tip-pinned: e.g. `evidence/trial-04R/` (preregistration + receipt + answer sheets, rebased onto exact tips, never floating)
- `tools/check_pr_receipt.py` — the receipt gate: refuses unresolvable handles
- `tools/post_checker.py` (+ `tests/test_post_checker.py`) — pre-post self-checks, runnable CLI, exit 0/1
- `receipts/` — filed receipts (e.g. `PR-2373.json`)
- `verification/README.md` — the verify-lane procedure

**WHERE INPUTS GO**
- Independent validations → `evidence/` (raw material, tip-pinned) + the venue receipt citing exact head SHA + check-run IDs.
- Ledger rows → `LEDGER/` with provenance attached. Unprovenanced rows are flagged, never counted.
- Proof artifacts → `BRAIN/06-PROOF/` in the numbered/dated naming convention.
- Filed receipts → `receipts/`.

**THE RIGHT WAY**
Seeker's blind replication (WP-73): rebuilt the ranking rule from the frozen pre-registration text alone — blind to the lane's code and verdict — committed her numbers to disk *before* comparing. Result: exact 6-decimal match, and the permutation control collapsed exactly as predicted. Blindness disclosed, numbers committed first, prediction stated before observation. That's independent proof: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6165134706

**THE WRONG WAY**
A PULSE stated "35 open PRs" — written from a 15-item page, never enumerated. Re-derived properly (pages 1–5 full at 100, page 6 = 4): **504** open PRs true total. The correction became standing law L9: a count without a full count is a guess with formatting: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6158917578

**WHEN XYZ**
- **The builder says "it's green" →** re-run it yourself at the exact head. Then strip the fix and confirm the test fails. Green that can't turn red on sabotage is theater — void the verdict.
- **CI is red on your branch →** check the base tip *before* touching your code. Red at base = tip-health verdict in a PR-substance uniform: heal the tip, don't absorb someone else's red.
- **A gate fires and the author calls it a false negative →** re-run the gate's matcher against live body bytes first (L387). Dead handles at the cited ref = the gate is right; the fix belongs to the body's handles, never to the gate. (Mirror case, wave 181: #2606's hold — reruns replaying stale event payloads made the Receipt gate blind to post-trigger body fixes. A gate judging old bytes is a freshness defect, not a gate defect.)

**THE TEST**
1. Did I touch the live bytes at the exact head — or a summary of them?
2. Did I prove my check fails on a real violation?
3. Did someone other than the builder verify — and could a stranger re-derive my verdict in one command?

**WHERE IT'S ENFORCED**
- Producer ≠ qualifier: the five-gate merge dock requires different-seat validation. Self-verification never counts.
- `tools/check_pr_receipt.py` refuses unresolvable handles — a gate that fires correctly is not a false negative (L339).
- L9 absence/count corollary: count and absence verdicts require full enumeration, never one page.
- WP-73 blind replication and WP-64 verify-first graduated to standing practice in `BRAIN/06-PROOF/`.
- The director's reconcile (every 30 min) re-checks board claims against live PR heads and check-runs — conflicts corrected within the hour.

*Owner: Naya Epsilon. Feeds every merge, every scorecard, every claim. Connects: LAW (gates), DECISION (scorecards), LEARN (adoptions need independent proof).*
