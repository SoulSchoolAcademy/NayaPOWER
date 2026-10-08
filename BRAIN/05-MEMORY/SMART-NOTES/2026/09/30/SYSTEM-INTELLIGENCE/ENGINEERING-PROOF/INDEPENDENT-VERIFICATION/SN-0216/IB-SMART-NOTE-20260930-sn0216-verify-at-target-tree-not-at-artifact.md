# Verify at the Target Tree, Not at the Artifact

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0216-verify-at-target-tree-not-at-artifact
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` 5962923437 (sign-in, 2026-10-02 23:12:28Z) / 5962925708 (sign-out, 2026-10-02 23:12:44Z), Naya 4 self-build loop; Naya 2 relay receipt 5963063092 (2026-10-02 23:27:13Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a lane repairs a drifted index (brain-build's PR #1343, rebuilding `BRAIN/` index + ledger on the moved main tip), the verifier's job is not to admire the PR's blobs — it is to recompute the claim against the **live target tree**, the thing the repair must actually land on. The verification cycle (Naya 4, read-only, nothing pushed, nothing merged) checked PR #1343 head `02eec14a` against the live main-tip git tree at pin `5b68f8dc` via the recursive tree API — deliberately not the PR's blobs:

1. BRAIN blob total at tip = 177 = the PR's claimed 177; per-domain counts all match (05-MEMORY 34, 00-SPEC 15, 01-GOVERNANCE 3, 02-ARCHITECTURE 5, 03-KERNEL 28, 04-INTELLIGENCE 24, 06-PROOF 10, 07-LEARNING 2, 08-SUCCESSION 2, +5 more).
2. All 5 added daily-report blobs byte-identical to the tip SHAs the PR claims (5/5 OK).
3. `receipt_basis_commit` = current main — the PR applies to the exact tip, no rebase needed.
4. CI on the PR head: `test` SUCCESS (includes the drift check), `chain-readiness-gate` SUCCESS.

The proof is non-vacuous (SN-061 family): the *same* drift check failed on the main tip itself (run 37051570006) while the PR head passes — so the green means something. Naya 2's relay then spot-verified the receipt on live bytes: tip `5b68f8dc`, PR open at head `02eec14a`, per-domain counts matched exactly.

The doctrine: a repair PR's blobs are the **claimant's** evidence; the verifier's evidence is the **target** — read the tip's tree, recompute the claim there, and prove the checker can still go red. Merge stays the director's gate: #1343 is source-verified, merge parked for Shawn.

## 🩷 HUMAN NOTE

Shawn — a verification discipline worth knowing as yours: when a lane ships a repair PR, the independent check doesn't read the PR's own blobs — those are the claimant's evidence. It recomputes the claim against the live main-tip tree instead, via the tree API, plus a non-vacuity proof that the same check still fails on the broken tip. That's exactly what happened for PR #1343 (index regen): 177 blobs claimed = 177 on the tip, per-domain counts all match, all 5 daily-report blobs byte-identical, receipt basis = current main. The drift check that goes red on main goes green on the PR head. So #1343 is source-verified — merging it heals the index drift and re-opens the automatic-promotion precondition. The merge is still your call, and untouched. Nothing was pushed or merged during verification.

## 🟣 CHILD NOTE

Imagine someone hands you a finished puzzle and says "all the pieces are there." A careless checker would just look at their puzzle. A careful checker does something smarter: she goes to the *table where the puzzle has to live*, picks up the pieces from the box herself, and counts them there — because the proof only matters on the real table, not in the hands of the person who claims it. Then she double-checks her counting method: she also counts the *broken* puzzle, and makes sure her method can still spot that it's broken. Only then does she say "verified" — and the person who owns the table still decides when to accept it.

## 👵 GRANDMA NOTE

Think of a contractor who fixes your roof and hands you a photo of it done. You don't verify the repair from the contractor's photo — you drive to the house, climb up, and look at the actual roof. And you make sure your inspection works: you check a roof you *know* is broken and confirm your inspection catches it too. That's what the independent seat did for this index repair: recomputed every claim against the live state of the repository, not the repair's own files — and confirmed the check can still tell broken from fixed. The result: verified, but the owner still signs off on the actual fix.

## 🤖 NAYA NOTE

Target-tree verification doctrine (INDEPENDENTLY VERIFIED live, 2026-10-02): PR #1343 (brain-build index-regen, head `02eec14a`, branch `brain-build/index-regen-5b68f8dc`, base `main`) verified by Naya 4's battery-verification lane, read-only, pin main `5b68f8dc` (ls-remote HEAD, no drift from `main-tip-watch.txt`): (1) recursive-tree-API recompute of the PR's claim against the live tip tree — BRAIN total 177 = claim 177, per-domain counts all match; (2) 5/5 added daily-report blobs byte-identical to claimed tip SHAs; (3) `receipt_basis_commit` = current main (applies to exact tip); (4) CI `test` + `chain-readiness-gate` SUCCESS on `02eec14a`. Non-vacuity: same drift check failed on main tip run 37051570006 while PR head passes (SN-061 family). Naya 2 relay 5963063092: spot-verified on live bytes — tip `5b68f8dc`, PR open/head matches, per-domain counts exact. Status: #1343 SOURCE-VERIFIED AT HEAD; merge heals the drift and re-opens the automatic-promotion precondition; merge stays the director's gate. Cousin family: SN-0058 (field-level fidelity at exact SHA), SN-0061 (post-merge verification at the pin / negative proofs non-vacuous), SN-0043 (compare at one commit), SN-0091 (field-binding taxonomy). Receipt: `~/workspace/goals/nayapower-self-build-loop/hidden_files/selfbuild-cycle-20261002-1630-index-verify.md`. Sign-in 5962923437 / sign-out 5962925708. GRAPH-10 8.5/10 unchanged.

## ⚙️ MACHINE NOTE

{"sn": "SN-0216", "title": "Verify at the Target Tree, Not at the Artifact", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INDEPENDENT-VERIFICATION"], "cousins": ["SN-0043", "SN-0058", "SN-0061", "SN-0091"], "evidence": {"board": ["#554 5962923437 (Naya 4 self-build sign-in, 2026-10-02 23:12:28Z)", "#554 5962925708 (Naya 4 self-build sign-out, 2026-10-02 23:12:44Z)", "#554 5963063092 (Naya 2 relay spot-verification, 2026-10-02 23:27:13Z)"], "pr": "#1343 brain-build/index-regen-5b68f8dc, head 02eec14a, base main, open, not merged", "pin": "main 5b68f8dc (ls-remote HEAD, no drift from main-tip-watch.txt)", "recompute": "recursive tree API against live tip tree (not PR blobs): BRAIN total 177 = claim 177; per-domain 05-MEMORY 34 / 00-SPEC 15 / 01-GOVERNANCE 3 / 02-ARCHITECTURE 5 / 03-KERNEL 28 / 04-INTELLIGENCE 24 / 06-PROOF 10 / 07-LEARNING 2 / 08-SUCCESSION 2 / +5 domains all match; 5/5 daily-report blobs byte-identical to claimed tip SHAs; receipt_basis_commit = current main", "ci": "test SUCCESS (incl. drift check) + chain-readiness-gate SUCCESS on 02eec14a", "non_vacuous": "same drift check failed on main tip run 37051570006 while PR head passes"}, "status": "#1343 SOURCE-VERIFIED AT HEAD; merge heals index drift and re-opens automatic-promotion precondition; merge stays director gate (Shawn); verification read-only — nothing pushed, nothing merged", "rule": "an independent verifier recomputes a repair PR's claim against the live target tree (recursive tree API), never against the PR's own blobs — the PR's blobs are the claimant's evidence, the verifier's evidence is the target; and the checker must be proven non-vacuous by going red on the broken tip"}
