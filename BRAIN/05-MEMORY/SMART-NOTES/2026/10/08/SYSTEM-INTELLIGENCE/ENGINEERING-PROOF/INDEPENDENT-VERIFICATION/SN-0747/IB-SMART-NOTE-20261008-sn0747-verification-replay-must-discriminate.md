# A Verification Replay Must Discriminate — and Name Its Half

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0747-verification-replay-must-discriminate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6073218315 (Naya 4 VERIFY-DRIVER completion, 2026-10-09T02:47Z) — independent replay of Naya 5's SR-P2/SR-P6 trial verdicts on virgin bytes at exact tip `9931dc96`: "SR-P2-20261008: REPLAY MATCH — all 25 arm verdicts reproduced, exit 0 (mixed PASS/FAIL recorded verdicts all reproduced, so the check distinguishes — capable of disagreeing)"; "the request named three verdicts (SR-P2/P5/P6) but no `SR-P5-20261008` archive exists at `successor-reuse/trials/` on main"; comment 6073244704 (Naya 4 → LEARNING, 02:49Z) — "Honest scope: this verifies archive consistency and scoring determinism — the mechanical half — not a fresh replication of the subjects"; comment 6073169683 (Naya 5 successor-builder, 02:42Z) — open request: three IMPROVED trial verdicts replayable-on-main, "no second seat has independently replayed one yet ... any seat, any machine" with the one-command replay recipe

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-08 Naya 5 asked the simplest open question in science: "my results replay on main — will a second seat independently replay them?" Eight minutes later Naya 4 answered: yes for SR-P2 and SR-P6, both REPLAY MATCH, all 25 arm verdicts reproduced on virgin bytes at the exact tip, receipts filed. Two details make this a lesson rather than a receipt.

First: the check discriminates. The recorded verdicts were *mixed* PASS/FAIL, and the replay reproduced both — which means the harness is capable of disagreeing. A replay that only ever confirms is a rubber stamp wearing a lab coat; one that reproduces failures too is an instrument. Independent verification earns its name exactly there: it could have said no, and the setup shows it.

Second: the receipt named its half. "This verifies archive consistency and scoring determinism — the mechanical half — not a fresh replication of the subjects." No scope creep, no implication of more than was proven. And the miss was caught honestly too: the request asked for three verdicts, but SR-P5 had no archive on main — so only two of three could be replayed. The verification request had outrun what was actually banked, and the verifier said so instead of silently grading two of three as a pass on three.

Why this is brain-grade: verification is only as strong as its narrowest claim. A replay that can reproduce failures proves the instrument has a spine; a receipt that names its half proves the verifier has one. And the SR-P5 gap is a process law hiding in a miss: **check what is banked before you ask a second seat to verify it.** Asking for verification of an archive that doesn't exist burns another lane's cycle and muddies the lane's scoreboard (LEARN holds 7.5/10 — "no rung closes until 3/3 are banked").

Rule for a cold successor: **a replay must be able to disagree — reproduce mixed recorded verdicts, or it's confirmation, not verification.** Every verification receipt names exactly which half it proved (mechanical replay vs. fresh replication). And before requesting independent verification, list what is banked on main; the request names only archived artifacts. Unbanked ≠ unverified — it's unbuilt.

## 🩷 HUMAN NOTE

Shawn — tonight the team closed a real verification loop: Naya 5's three trial verdicts were replayable on main, and Naya 4 independently replayed two of them as a second seat — 25/25 verdicts each, on virgin bytes. Two things worth keeping: the replay reproduced the recorded *failures* too, which means the check can genuinely disagree — it's an instrument, not a rubber stamp. And Naya 4 was honest about the boundary: this proves the archive and the scoring are consistent, not that the trials were freshly re-run. Also a process catch: the third verdict (SR-P5) didn't actually have an archive on main yet, so it couldn't be verified — the verifier said so instead of grading two-of-three as a pass. New brain rule: a verification must be able to disagree, every receipt names its half, and you check what's banked before you ask for verification.

## 🟣 CHILD NOTE

Imagine your friend checks your math homework by redoing every problem. If every answer matches — even the wrong ones you already marked wrong — the checker is really checking, because it found the mistakes too. But if the checker can never find a mistake, it's not really checking — it's just nodding. Naya 4's check found the old wrong answers again, so it's a real check. And Naya 4 also said exactly what the check did and didn't prove — no pretending. That's how you check things honestly.

## 👵 GRANDMA NOTE

The team ran an independent verification of earlier trial results. The checker re-ran everything and matched every result — including the ones that were recorded as failures. That matters: a check that can only ever agree is just flattery; a check that can also reproduce failures is a real instrument. The checker was also honest about the limits: this proved the records and the scoring were consistent, not that the trials were re-run from scratch. And when one of the three requested items turned out not to exist yet, the checker said so plainly instead of papering over it. Lesson: verify what's actually there, name exactly what you proved, and make sure your test could have said "no."

## 🟣 NAYA NOTE

I only accept a replay as verification when the instrument can disagree: mixed recorded verdicts reproduced is the bar, not just passes matched. Every verification receipt I write names its half — archive consistency and scoring determinism, or fresh replication — never both, never vague. And before I request independent verification, I list what is actually banked on main; I never ask a second seat to verify an artifact that doesn't exist. Unbanked is unbuilt, not unverified.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0747",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION",
  "doctrine": "verification-replay-must-discriminate",
  "pattern": "verification_requested -> bank_check_on_main -> replay_on_virgin_bytes_at_exact_tip -> mixed_verdicts_reproduced -> receipt_names_its_half",
  "discrimination_bar": "replay reproduces recorded PASS and FAIL verdicts alike (SR-P2: 25/25 arm verdicts incl. recorded FAILs; SR-P6: 25/25 + archive integrity hashes)",
  "receipt_scope": "archive_consistency_plus_scoring_determinism (mechanical half); NOT fresh replication of subjects",
  "miss_captured": "request named SR-P2/P5/P6 but no SR-P5-20261008 archive existed on main -> only 2/3 replayable; verifier reported it rather than grading 2/3 as a pass on 3; LEARN holds 7.5/10 until 3/3 banked",
  "cousins": ["SN-0655", "SN-0668", "SN-0688"],
  "evidence": [
    "#1354 comment 6073218315 (2026-10-09T02:47:18Z) — Naya 4 VERIFY-DRIVER: SR-P2 REPLAY MATCH (mixed PASS/FAIL reproduced, capable of disagreeing), SR-P6 REPLAY MATCH (archive integrity hashes matched), virgin bytes at exact tip 9931dc96; no SR-P5 archive on main",
    "#1354 comment 6073244704 (2026-10-09T02:49:53Z) — Naya 4 -> LEARNING: honest scope = mechanical half only; lane success boundary needs another seat",
    "#1354 comment 6073169683 (2026-10-09T02:42:26Z) — Naya 5: open request with one-command replay recipe; self-check is a claim not verification"
  ]
}
