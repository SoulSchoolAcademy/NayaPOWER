# IB-SMART-NOTE-20261008-sn0653-extract-claims-from-their-layer.md

**Intelligent Block:** SN-0653
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6053109026 ([NAYA 5] Automated reporting system BUILT — branch `naya5/automated-reporting` @ `974e706f0`, 2026-10-08T05:35:12Z) and 6053163937 ([NAYA 5] Reporting delivery WIRED — morning/hourly/nightly crons live, 2026-10-08T05:39:29Z — score-extraction accuracy fixes from first-run monitoring) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

EXTRACT CLAIMS ONLY FROM THE LAYER THEY DESCRIBE: first-run monitoring of Naya 5's automated reporting system caught three live corruption classes in heuristic score extraction — (1) an aspirational "3.0→10.0 drive" goal was extracted as Production Readiness **10.0** (a goal is not a current score); (2) a stale 2026-10-07 "Retrieval 6.5" overwrote the current 7.0 via file mtime (mtime is not a date — memory scores now carry filename date, not mtime); (3) a 10.0 could be heuristically fabricated (10/10 needs Shawn's word per mission law — 10.0 is now never heuristically extracted). The baked-in anti-corruption rules: area+score must share a sentence; multi-area sentences skipped; movement beats prefix ("re-score: 8.5 → 8.8" = 8.8); authoritative status never downgraded by heuristic claims. Doctrine: a measurement pipeline that reads the wrong layer doesn't mis-measure — it manufactures. Complements SN-0421 (skipped jobs ≠ proof) — both are "read the claim from the instrument that can actually make it."

## 🩷 HUMAN NOTE

Shawn — one measurement lesson worth banking from the automated reporting build: the extractor was confidently wrong in three ways, and each was the same mistake — reading a claim from the wrong layer. It read a *goal* ("drive 3.0→10.0") as a *current score* (10.0). It read a file's *modification time* as the *date of the score inside it* and let last week's 6.5 overwrite this week's 7.0. And it could have invented a 10.0 out of thin air — when only you get to say 10. All three got fixed the same way: the rule now is that a claim can only come from the layer that actually makes it. Goals come from the goals layer. Dates come from inside the file, not the filesystem. And a 10 comes from you — no heuristic is ever allowed to mint one. Degraded sources render "unavailable," never silently drop, and generation failures post a failure notice — never silent, never fabricated.

## 👶 CHILD NOTE

Imagine a report card machine that reads your teacher's note "we're aiming for straight A's!" and writes down "A+ in everything" — that's not your grade, that's the *goal*. Or it looks at when a folder was last touched instead of the date written on the paper inside, and gives you last year's grade. The rule: read what the paper actually says, not what you wish it said, and never invent a perfect score — only the teacher can give that.

## 👵 GRANDMA NOTE

Dear, this is about honest bookkeeping. The new report-writing helper was pulling numbers from the wrong places — treating a wish as a fact, treating the envelope's postmark as the letter's date, and nearly printing a perfect score nobody earned. We taught it three manners: a wish is not a fact, the date is inside the letter not on the envelope, and a perfect score can only come from Shawn himself. When it can't read something properly, it says "I couldn't read this" — it never guesses. That's how you keep reports trustworthy.

## 🧭 NAYA NOTE

This generalizes beyond the reporting tool — it is measurement-integrity law for any heuristic pipeline:

1. **Layer separation:** goals, current scores, and verdicts are different layers. A goal statement ("3.0→10.0 drive") is never a current-score claim. Extraction rules must pattern-match the layer, not just the numbers: area+score must share a sentence; multi-area sentences are skipped (no cross-contamination); movement beats prefix (the latest number in a "X → Y" movement is the current one).
2. **Recency from content, not filesystem:** mtime is a filesystem accident (re-saves, copies, tooling touch files). Embedded dates (filename date, frontmatter) are the claim's own timestamp. Stale-heuristic overwrote current-truth once; the fix makes embedded dates authoritative.
3. **Human verdicts are not extractable:** 10/10 per mission law requires Shawn's word. A heuristic must never mint a 10.0 — the absence of a claim is "unavailable," never an invention. Same family as SN-0421: a run-level SUCCESS with skipped behavioral jobs is not evidence; a heuristic 10.0 is not a score.
4. **Failure posture:** degraded sources render as "unavailable" (never silently dropped); generation failure posts a failure notice (never silent). 37/37 pytest green on the reporting tests including 8 regression tests for these exact fixes (commit `53fbd2d` on `naya5/automated-reporting`).

Any future extraction or distillation step should carry these four as its acceptance bar.

## MACHINE NOTE

{"sn": "SN-0653", "title": "Extract Claims Only from the Layer They Describe", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-08", "source": "#1354 comments 6053109026, 6053163937; branch naya5/automated-reporting @ 974e706f0, commit 53fbd2d", "doctrine": "layer_separated_extraction", "corruption_classes": ["goal_extracted_as_score", "mtime_as_claim_date", "heuristic_10.0_fabrication"], "rules": ["area_score_share_sentence", "skip_multi_area_sentences", "movement_beats_prefix", "authoritative_status_never_downgraded_by_heuristic", "embedded_date_over_mtime", "ten_never_heuristic", "degraded_renders_unavailable", "failure_posts_notice"], "pairs_with": ["SN-0421", "SN-0481"]}
