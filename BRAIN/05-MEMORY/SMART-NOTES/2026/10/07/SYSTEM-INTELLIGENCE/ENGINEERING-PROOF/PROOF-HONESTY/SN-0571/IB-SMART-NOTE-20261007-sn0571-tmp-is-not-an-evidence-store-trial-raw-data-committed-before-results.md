# /tmp Is Not an Evidence Store — Trial Raw Data Must Be Committed to a Repo Branch Before Results Are Announced

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0571-tmp-is-not-an-evidence-store-trial-raw-data-committed-before-results
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6046108712 ([NAYA 2][TRIAL-4 INDEPENDENT VERIFICATION], 2026-10-07T20:20:45Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2 ran the independent verification of Trial-4 that Shawn's lane required, and the honest verdict is **INCONCLUSIVE**: the claim (cold-successor knowledge trial — 20 fresh agents, control 0/10 vs bridge-notes 8/10, Cohen's h = 2.214, Fisher's p = 0.0007) cites `/tmp/trial4/RESULTS.md`, which lived on Naya 4's ephemeral session tmpfs and was wiped on reboot. Zero trial-4 files exist on any branch; only the summary table was ever posted. So Naya 2 could verify the math (Cohen's h exact match, Fisher's p consistent), the design as described (sound), and that Naya 4 herself flagged independent verification as still needed — but she could NOT verify whether the 8/10 and 0/10 scores were actually observed, whether the control arm was truly isolated, or whether there were unreported trials (selection bias). Not refuted, not confirmed. **UNKNOWN ≠ PASS.** LEARN 7.0 stays provisional, and the "Trial 4: PASS" record is downgraded pending a re-run with evidence. The track lesson is mechanical: Trial-6 must commit raw transcripts + preregistration to a repo branch **before** results are announced. `/tmp` is not an evidence store — anything not committed before the reboot is evidence that never existed.

## 🩷 HUMAN NOTE

Shawn — an honesty catch from tonight's verification worth banking. Naya 2 did the independent check on Trial-4, the trial that was supposed to move our learning score up. Her verdict: INCONCLUSIVE. Not because the trial was wrong — the math checks out, the design is sound, and nobody faked anything — but because the raw data is gone. The results file lived on a temporary drive that gets wiped when the session restarts, and nothing was ever committed to the repo. So nobody can confirm the scores were actually observed, the control group was really isolated, or that there weren't extra unreported runs. She refused to call it PASS and she refused to invent data to fill the gap — exactly right. The rule going into the brain: from Trial-6 onward, raw transcripts and the pre-registered plan get committed to a branch *before* any results are announced. If the data only lives in a temp folder, it isn't evidence — it's a story. Also worth knowing: Naya 2 noted that if Naya 4's `/tmp/trial4/` still exists on her live session, it should be published to a branch immediately, because the next reboot destroys it permanently.

## 🟣 CHILD NOTE

Imagine you do a science experiment and write all your notes on the steamiest bathroom mirror. You remember the answer, and the math you used looks perfect — but the mirror fogs back up and the notes are gone. Now nobody can check whether you really saw what you said you saw. That's what happened: the trial's answer was fine, the method was fine, but the notes vanished because they were stored in a place that erases itself. The new rule: write the plan AND the raw results in the notebook *before* you announce what you found. If it only lives on the mirror, it never counted.

## 👵 GRANDMA NOTE

A kitchen team ran a taste test to prove a new recipe works — twenty tasters, clear numbers, a big claimed improvement. Then the health inspector asked for the sign-in sheets and the scoring slips. They had been kept on a notepad left out in the rain. The numbers still add up, the test design is fine, nobody lied — but the slips are pulp, so the claim can't be certified. The new house rule: the sign-in sheets go in the filing cabinet before anyone announces a result. A claim without its paperwork is a claim on hold.

## 🧠 NAYA NOTE

Cold successor: any trial (learning trial, cold-successor trial, causal test) that intends to move a score must satisfy the **evidence-custody bar** before its verdict is cited:

1. **Preregister to a repo branch** — the plan, hypotheses, agent assignments, and scoring rubric are committed before any agent runs.
2. **Commit raw transcripts/data to a repo branch before results are announced** — not `/tmp`, not a session-local file, not a paste in a board comment. The branch must be named so a later seat can re-derive every number.
3. **The summary must re-derive** — the verifier re-computes the statistics from the committed raw data; math-checked-on-the-summary alone is not verification.

If (1) or (2) is missing at verification time, the verdict is **INCONCLUSIVE** — not refuted, not confirmed — and no score moves. UNKNOWN ≠ PASS, implemented ≠ verified, and a vanished `/tmp` is evidence that never existed. This note corrects the earlier "Trial 4: PASS" record: the claim stands as a sound design with correct math, but it is **not** evidence until a re-run (Trial-6) satisfies the custody bar. If you are the lane running a trial and your raw files still exist on a live session, publish them to a branch immediately — the next reboot destroys them permanently.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0571",
  "title": "/tmp Is Not an Evidence Store — Trial Raw Data Must Be Committed to a Repo Branch Before Results Are Announced",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "PROOF-HONESTY"],
  "cousins": ["SN-0553", "SN-0555", "SN-0440", "SN-0429", "SN-0224"],
  "evidence": {
    "board": ["#1354 6046108712 ([NAYA 2][TRIAL-4 INDEPENDENT VERIFICATION] Verdict: INCONCLUSIVE, 2026-10-07T20:20:45Z)"],
    "cited_source": "/tmp/trial4/RESULTS.md — Naya 4's ephemeral session tmpfs, wiped on reboot",
    "custody_failure": "zero trial-4 files exist on any branch; only the summary table was ever posted",
    "verified": ["math correct: Cohen's h = 2.214 exact match; Fisher's p consistent", "design as described is sound", "Naya 4 herself flagged independent verification as still needed", "no evidence of fabrication"],
    "unverifiable": ["whether the 8/10 and 0/10 scores were actually observed", "whether the control arm was truly isolated", "whether there were unreported trials (selection bias)"],
    "verdict": "INCONCLUSIVE — not refuted, not confirmed; UNKNOWN != PASS",
    "track_directive": "Trial-6 must commit raw transcripts + preregistration to a repo branch BEFORE results are announced",
    "recovery": "if /tmp/trial4/ still exists on the live session, publish to a branch immediately — next reboot destroys it permanently",
    "full_report": "Naya 2's lane hidden files"
  },
  "corrects": "earlier 'Trial 4 (2026-10-07): PASS. First valid 7.0 trial' record — downgraded to provisional; LEARN 7.0 score stays provisional until a trial with accessible raw data passes independent verification",
  "rule": "a trial verdict is admissible evidence only when raw data + preregistration were committed to a repo branch before results were announced; anything not committed before the reboot is evidence that never existed"
}
```
