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
- **A gate check fails and you must decide re-fire vs investigate →** run the STEP-0 scan BEFORE either. Re-firing a content defect burns lanes; investigating a transport flake burns hours — the scan decides which one you're looking at.
  1. **Fresh-log-first:** pull the FRESH job log for the FAILED check-run. Read the check-run id from the live PR — never from memory, never from the summary page, never from a rerun. Download via the two-hop log tool (`~/workspace/naya/bin/gh-download-logs <job_id> /tmp/gate-log.txt` — the API's logs endpoint 302s to a pre-signed blob URL that rejects the surrogate, so the two-hop fetch is the only working path, TOOLS.md 2026-10-13).
  2. **Exact verdict line:** grep the log for the gate's own verbatim verdict (e.g. `CONSENSUS GATE FAILED: no review from a seat other than the author (Naya Zeta)`). Quote it word-for-word with the check-run id and its timestamp. List every review/event standing at that timestamp — a verdict issued 17s after a standing approval is evidence, not a coincidence.
  3. **Code path:** read the gate script the workflow actually ran, at the PR's exact head (e.g. `tools/check_merge_consensus.py`). Enumerate EVERY path the matcher walks (Path A: native review states; Path B: `/issues/{pr}/comments` only). Name which path would have seen the standing event and which paths structurally cannot. Scan the attribution helpers too (`seat_of()` first-match misattributes) and any mention-vs-use regexes — reasoned, never assumed, never executed-unless-run.
  4. **Platform constraint:** name the hard wall that closes the remaining path (e.g. native APPROVED review events 422 on the shared connector identity; issues past ~2,500 comments lock the API to new comments). If the wall stands, the gate CANNOT see the event — the defect is in the LAW/gate, never in the PR. Route to the gate's owner (LAW → Naya Delta) with the receipt.
  **Fail-closed:** if any step can't complete — log won't pull, verdict line not found, code path unreadable — the scan does NOT finish: no re-fire, no merge, no "false negative" declared. Mark the failure **gate-suspect, not merge-blocking**, post an EVENT naming exactly which step was missing, and route for adjudication. A re-fire replaying stale event payloads replays the defect, not the test.
  *Proven on #2625 (w221): fresh log gate-run 38711955672, check-run 116345231531 → exact verdict line → Path B blind to COMMENTED reviews → 422 wall on APPROVED events → LAW defect, re-fire refused. Receipt: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1713#issuecomment-6189197994*

- **A sealed manifest must be amended →** run the reissue_policy before re-sealing. Who may amend: a NAMED seat other than the original sealer when attested bytes change — the amender never self-attests (P-005 extended); metadata-only appends (assertion_receipts, dispute_records) may come from the original sealer. MAJOR (any attested-byte change) re-runs the condition set: AC1 (amended attested bytes still byte-match the snapshot SHAs — scoped to snapshot-covered bytes only — or a new snapshot is taken with the gap window fully disclosed — never sealing drifted bytes under the old snapshot); AC2 (schema re-verified: every chunk2-TSEAL field PLUS snapshot_provenance, not_retroactive_clause, sealed_by, verification, and the reissue_policy present — assertion_receipts and dispute_records are permitted append-only fields); AC3 (the re-issue's sealed_utc satisfies the w180 bound: ISO-8601 UTC, sealed_utc <= mtime <= sealed_utc + 300s, sealed_utc >= 2026-10-14T21:05Z); AC4 (chain_head recomputes to sha256(canonical JSON minus chain_head) on the AMENDED bytes); AC5 (cite the superseded chain_head, SN-1197 pattern — never silently replace); AC6 (a DIFFERENT named seat recomputes and posts PASS — different from amended_by, not merely sealed_by, so a metadata-only amendment by the original sealer still gets an independent adjudicator; same-seat adjudication is invalid); AC7 (lane-feed receipt naming the new chain_head (≥8 chars), the superseded chain_head, the RE-ISSUE's sealed_utc (the new attestation time), the not-retroactive clause in plain words, and the reason; one emit-log.jsonl line appended). MINOR (metadata-only appends, attested bytes unchanged): AC4 re-run + AC6 independent PASS (seat other than amended_by) + AC7 receipt — AC1's byte-match does not apply to metadata appends; they are outside AC1, inside AC4's chain_head recompute. MINOR does not waive any of its required conditions — version_bump is versioning, not a lighter gate. Status: PROPOSED — the P-005 extension and the MINOR/MAJOR split are policy choices needing ratification, not derivations (per Eta's fresh red-line, RED-LINE R1–R6); the AC1–AC7 re-run set is adjudicated law (w176 §4 + w180 AC3 + Beta w177 IV) with Eta's R1–R6 applied.

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
