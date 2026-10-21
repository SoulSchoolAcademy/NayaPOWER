# Every Learning Trial Ships a Fail-Closed Evidence Verifier — the Trial-4 Hole, Mechanized Shut

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0573-trial-evidence-fail-closed-verifier
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6046635816 ([NAYA 4][VERIFY-DRIVER] COMPLETION, 2026-10-07T20:52:44Z) + PR #1766 (`naya4/verify-trial-evidence-v1`, TRIAL-EVIDENCE-V1 spec CANDIDATE + `tools/verify_trial_evidence.py`)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Trial-4 was the lesson we paid for: a statistically overwhelming result (20 fresh agents, p=0.0007, h=2.214) was downgraded from PASS to **INCONCLUSIVE** because its raw data lived on ephemeral `/tmp` and was lost before independent verification (Naya 2, #1354 6046108712; SN-0571: "/tmp is not an evidence store"). The VERIFY-driver's answer (PR #1766) is not a reminder — it is **machinery**: a canonical `TRIAL-EVIDENCE-V1` spec (CANDIDATE) plus a fail-closed evidence verifier (`tools/verify_trial_evidence.py`) plus an 11-test conformance suite that includes a **Trial-4 regression replay** — the verifier is proven against the exact hole that burned us.

The rule is now executable: a trial's raw data must be committed in-repo (never /tmp) with committed custody, or the verifier marks the trial INCONCLUSIVE — the same verdict a human independent verifier would give. The regression replay is the proof the mechanism works: the verifier must reject the Trial-4 shape (summary statistics, no committed raw data) and accept the Trial-4R shape (raw data committed in-repo on PR #1768).

Why this is brain-grade: this is SN-0571's second half — SN-0571 stated the doctrine ("evidence must be in-repo"); this note mechanizes it (a tool that *enforces* the doctrine, with a conformance suite that *replays the failure*). Doctrine without enforcement is a wish; enforcement without a regression replay is untested. The three together — rule, enforcer, replay — are what a cold successor needs to run Trial-5 through Trial-N without re-paying Trial-4's tuition. A trial that cannot be independently verified is not a trial; it is a story with numbers.

## 🩷 HUMAN NOTE

Shawn — banking the mechanical fix for the Trial-4 lesson: every learning trial now ships a fail-closed evidence checker. The TRIAL-EVIDENCE-V1 spec plus a verifier tool plus an 11-test conformance suite (PR #1766) — and the suite replays Trial-4's exact failure to prove the checker catches it. The rule it enforces: trial raw data lives in the repo, committed, or the trial is marked INCONCLUSIVE automatically — no human has to notice. Trial-4 was a PASS on paper that died because its raw data was on /tmp; Trial-4R (#1768) is the shape the verifier now demands. Doctrine became machinery.

## 🟣 CHILD NOTE

Imagine a science fair where a kid shows amazing results but says "the notebook with my measurements got thrown away." Even if the results look perfect, the judges can't check them — so they can't count. The new rule: every experiment comes with a checklist that a strict robot runs — "is the notebook in the folder? is it signed?" If anything is missing, the robot marks it "cannot be checked" before anyone celebrates. And the robot was tested by feeding it the exact failed experiment from before, to prove it catches it.

## 👵 GRANDMA NOTE

It's like a bank that learned from a bad check: once, a perfect-looking deposit slip had no funds behind it, so the loss was real. Afterward, the bank didn't just write a memo — it installed a machine that refuses to accept any deposit without verified funds attached, and it tested the machine by feeding it the same bad slip to watch it reject it. The rule is no longer advice on a wall; it is a machine that cannot be bypassed.

## 🧠 NAYA NOTE

Cold successor: when you run or review any learning trial, invoke the TRIAL-EVIDENCE-V1 machinery. (1) Raw data must be **committed in-repo** — never /tmp, never a pasted summary, never "available on request" (SN-0571). (2) Run `tools/verify_trial_evidence.py` (PR #1766) against the trial package — it is fail-closed: missing committed raw data → INCONCLUSIVE, same verdict an independent verifier would reach. (3) The 11-test conformance suite (incl. Trial-4 regression replay) is the proof the verifier works; if you extend the spec, extend the replay. A trial's verdict is only as strong as its evidence custody — summary statistics alone are never verification (that is what INCONCLUSIVE means). Trial-4's surviving lesson: the Trial-4R shape (raw data committed in-repo, PR #1768) is the template; copy it.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0573",
  "title": "Every Learning Trial Ships a Fail-Closed Evidence Verifier — the Trial-4 Hole, Mechanized Shut",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "EVIDENCE-IDENTITY"],
  "cousins": ["SN-0571", "SN-0533", "SN-0440"],
  "evidence": {
    "board": ["#1354 6046635816 ([NAYA 4][VERIFY-DRIVER] COMPLETION, 2026-10-07T20:52:44Z)"],
    "artifact": "PR #1766 (naya4/verify-trial-evidence-v1): canonical TRIAL-EVIDENCE-V1 spec (CANDIDATE) + tools/verify_trial_evidence.py + 11-test conformance suite incl. Trial-4 regression replay; CI running, NOT merged at capture",
    "hole_closed": "Trial-4 INCONCLUSIVE (Naya 2, #1354 6046108712, 2026-10-07 20:11 UTC): raw data on ephemeral /tmp lost before independent verification; summary stats alone not verification",
    "regression": "conformance suite replays the Trial-4 shape (summary stats, no committed raw data) and requires the verifier to reject it; accepts the Trial-4R shape (raw data committed in-repo, PR #1768)"
  },
  "rule": "every learning trial ships a fail-closed evidence verifier: raw data committed in-repo (never /tmp) with committed custody, or the trial is INCONCLUSIVE — the same verdict an independent human verifier would give",
  "failure_mode_closed": "celebrating summary statistics as a PASS when raw data cannot be independently verified"
}
```
