# Pin the Reconciled Score Outside the Extractor's Reach

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0726-pin-authoritative-score-outside-extractor-reach
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6070732936 ([NAYA 5 — HOURLY REPORT], 2026-10-08T22:59Z, Team 1/Learning section) — SoulSchoolAcademy. Exact recorded text: "On 2026-10-08 the hourly report generator was fixed after it had read worker logs' '7.0 PROVISIONAL' as the authoritative whole-area Learning score: Learning was pinned at 5.0 authoritative so heuristic extraction cannot overwrite a reconciled score."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The hourly report generator extracted a "7.0 PROVISIONAL" score from worker logs and published it as the authoritative whole-area Learning score — overwriting the reconciled 5.0. The fix was not another rule inside the extractor (SN-0655 already teaches extractor anti-corruption). The fix was structural: **Learning was pinned at 5.0 authoritative, in a location the extraction path can only read**, so no heuristic extraction can overwrite a reconciled score.

Why this is brain-grade: an extractor discipline is a promise the pipeline makes to itself — it breaks the first time the pipeline is rewritten, swapped, or run by a different seat. A pin is a boundary: the reconciled value lives behind a wall the extractor cannot write through. Discipline is one seat behaving well; a pin survives a seat behaving badly. Every score that moves "only on evidence" (10-area scorecard law) is a reconciled score — and a reconciled score that any heuristic can overwrite is a scorecard by rumor. SN-0655's rule (4) ("an authoritative status is never downgraded by a heuristic claim") is the extractor's side of this exact contract; this note is the data side: pin the value so the rule doesn't depend on the extractor's goodwill.

Rule for a cold successor: **reconciled scores are pinned outside the extraction path's write reach.** If a report shows a score that contradicts the pin, the pin wins — the report is mis-extracting. When you add a new reconciled score, add the pin in the same motion.

## 🩷 HUMAN NOTE

Shawn — a measurement-integrity fix from tonight. The hourly report had been showing Learning at 7.0 because the generator picked a "PROVISIONAL" number out of worker logs and treated it as the real score. The real reconciled score is 5.0. The fix: the real score is now pinned where the generator can only read it — no future run of the report can accidentally overwrite it. Standing rule: anything we agreed is the "official" number lives behind a wall the automated tools can't write through.

## 🟣 CHILD NOTE

Imagine the teacher writes your real test grade in ink in her gradebook, but the school website was guessing your grade from your practice quizzes. One day the website guessed wrong and told everyone you got a 70 instead of a 50. The fix isn't asking the website to guess better — it's putting the gradebook behind glass the website can only look at. The real grade goes in ink where guessers can't touch it.

## 👵 GRANDMA NOTE

The automated report was reading work notes and accidentally treating a rough guess ("7.0, provisional") as the official final score for Learning — the official score was 5.0. Rather than teaching the report to guess more carefully, the official number was locked away where the report can see it but never change it. The lesson: official numbers get a lock; automated tools can look, never touch.

## 🟠 NAYA NOTE

Make this mechanical in any reporting loop: (1) every score your system treats as authoritative gets a pin in a read-only-from-the-pipeline location — the pin is the score; (2) when a report's number contradicts the pin, the failure is in the extractor, never in the pin — debug the extraction, don't "update" the pin; (3) when reconciliation produces a new authoritative value, updating the pin is part of the reconciliation, in the same commit, or it didn't happen.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0726",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/MEASUREMENT-BOUNDARY",
  "doctrine": "pin-authoritative-scores-outside-extractor-reach",
  "rule": "Reconciled authoritative scores are pinned in a location the automated extraction path can only read; heuristic extraction can never overwrite a reconciled score. Extractor discipline (SN-0655) is the promise; the pin is the wall.",
  "failure_mode": "a provisional number scraped from worker logs becomes the published authoritative score — scorecard by rumor",
  "checks": [
    "identify which scores are reconciled (move only on evidence)",
    "confirm each lives behind a write boundary the reporting pipeline cannot cross",
    "on report-vs-pin mismatch, fix the extractor, never the pin"
  ],
  "cousins": ["SN-0655", "SN-0692", "SN-0343", "SN-0440"],
  "evidence": [
    "#1354 comment 6070732936 (Naya 5 hourly report, 2026-10-08T22:59Z): report generator read worker logs' '7.0 PROVISIONAL' as authoritative Learning score; Learning pinned at 5.0 authoritative so heuristic extraction cannot overwrite a reconciled score"
  ]
}
