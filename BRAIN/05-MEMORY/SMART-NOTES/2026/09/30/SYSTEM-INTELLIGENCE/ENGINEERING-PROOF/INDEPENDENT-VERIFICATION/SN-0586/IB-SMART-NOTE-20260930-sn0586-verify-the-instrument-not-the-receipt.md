# IB-SMART-NOTE — SN-0586 — Verify the Instrument, Not the Receipt — and Never Repair on the Evidence Branch

Intelligent Block: IB-SMART-NOTE-20260930-sn0586-verify-the-instrument-not-the-receipt
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-07
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Independent verification of trials 11–14 SOURCE-VERIFIED all four Tier-S transfer claims — but only after the verifier re-ran the graders and re-extracted the answers independently, which surfaced TEST DEFECTS in the shipped graders themselves: 5 under-scores and 2 over-scores from the explicit-choice extractor, an undocumented stats formula, and a receipt whose t11 control split (6/4) contradicted both the results file (7/3) and the corrected tally (9/1). The corrected data was equal-or-stronger in every trial, so the claims stood; the instrument did not. The repair rule is now law: re-grade on a new branch, re-issue the stats, correct the receipt — and never touch the evidence PR branches. Evidence is immutable; graders are repairable; the two must never meet.

## HUMAN NOTE
Shawn, when Naya 4 independently verified the four trial-evidence PRs (#1786–#1789) tonight, she didn't just re-read their receipts — she re-ran their graders and re-extracted the answers herself. That is what surfaced the defects: the shipped grader's extractor missed "Assign/Send <unit> to Call X" phrasings and misfired on generic-phrase-plus-later-mention answers, under-scoring 5 answers and over-scoring 2 across trials 11–13; the stats formula was never documented, so three of four reported effect sizes couldn't be exactly re-derived; and trial 11's receipt said the control split was 6/4 while the results file said 7/3 and the corrected truth was 9/1. The good news: after fixing the instrument, every claim got STRONGER, not weaker — all four Tier-S transfers verified with equal-or-better numbers (t11: treat 50/50 vs ctrl 0/50, p=1.08e-5, h=3.14; t12: 60/60 vs 30/60; t13: 50/50 vs 0/50; t14: 40/40 vs 28/40, p=7.14e-4, h=1.16). The standing rule from here: a receipt is only as honest as the instrument that produced it, so verification means re-running the instrument, never re-reading the receipt; and evidence PR branches are frozen the moment they open — any grader repair happens on a new branch, never on the evidence branch.

## CHILD NOTE
If your thermometer is broken and says you have no fever, you're still sick — you just need a working thermometer. And you never erase the doctor's notes while you're fixing the thermometer!

## GRANDMA NOTE
Honey, if the scale in the bathroom is off, the number it shows you isn't your real weight — get a good scale before you believe any number. And never tear up the receipt the store gave you just because you're double-checking the register.

## NAYA NOTE
This is the instrument-vs-evidence separation law for every verification seat from here on. (1) Verification = independent re-execution: re-run the graders, re-extract the raw data, adjudicate diffs against the answer text — never accept the shipped tallies as given. (2) Instrument defects do not automatically impeach the claim: classify them separately (TEST DEFECT / PROVENANCE GAP / RECEIPT PROSE / minor), correct the data, and re-test the claim on corrected data. (3) Evidence branches are append-only: the moment an evidence PR opens, its branch is frozen — repair work forks to a new branch, re-grades there, and corrected stats + corrected receipt prose ship as a follow-up; the original evidence bytes stay exactly as the claim was made. This pairs with SN-0392 (first RED is the only RED — read top-down) and the phantom-green doctrine: a green tally computed by a defective grader is the same class of phantom as a green check computed on absorbed state. LEARN's provisional 9.0 stands on the corrected, stronger data, still pending Trial-04R (#1768). Naya 2 independently corroborated the verdict against live bytes — SOURCE-VERIFIED or DEFECT-FOUND, both seats landed on the same truth.

## MACHINE NOTE
{
  "smart_note_id": "SN-0586",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn0586-verify-the-instrument-not-the-receipt",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM_INTELLIGENCE",
  "topic": "ENGINEERING_PROOF",
  "subtopic": "INDEPENDENT_VERIFICATION",
  "captured_at": "2026-10-07",
  "rule": "verify_the_instrument_not_the_receipt_repair_graders_on_a_new_branch",
  "procedure": ["re-run graders", "independently re-extract raw answers", "adjudicate extraction diffs against answer text", "classify instrument defects separately from claim defects", "correct data and re-test claim", "repair graders on a new branch", "re-issue stats and receipt prose as follow-up", "never touch the evidence PR branches"],
  "related": ["SN-0392 (first RED is the only RED)", "SN-0421 (skipped behavioral jobs = vacuous success)", "SN-0571 (/tmp is not an evidence store)"],
  "evidence": ["#1354 comment 6048866319 (NAYA 4 independent verification sign-out, 2026-10-07T23:23:30Z)", "#1354 comment 6048916851 (NAYA 2 relay acknowledgment, verdict stands)", "PR #1786 head 54bad733 / #1787 d310fc62 / #1788 9a0522e4 / #1789 85614652, base 9a571e99, main e363732be6b96264d68ca6ee508012af4f93ae2a"]
}
