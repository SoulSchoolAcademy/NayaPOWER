# Trial-04R Receipt Note — Cold-successor knowledge re-run

**Trial:** T4R-20261007-knowledge-rerun. **Executed:** 2026-10-07.
**Verdict:** PASS (Tier S).

- 20 fresh agents spawned (10 BRIDGE with corpus in-context, 10 COLD with no corpus).
- 19/20 returned valid answer sheets. The one loss: **T4R-A19** (bridge arm) —
  the worker errored on an inference-proxy **429** at 20:54:35Z. Excluded per the
  preregistered missing-agent rule (9 >= 8/arm, trial stays powered). Infrastructure
  failures are not subject failures.
- Results: bridge 9/9 success at 8.89/9 mean; cold 0/10 success at 0.00/9 mean.
- **Fisher's exact two-sided p = 1.1e-05. Cohen's h = 3.1415.**
  Bayes P(bridge > cold) = 1.0. Tier-S bar (p<0.05, h>=1.4): MET.
- Validity gate held (cold mean 0.0 < 4.5, no ceiling). Negative-transfer guardrail
  clean (3.0 vs 3.0 on general questions). Retrieval rate in bridge arm: 100%.
- Evidence discipline: every record committed to branch `naya4/trial-04R-evidence`
  (preregistration, arm assignment, corpus, answer sheets, raw JSON, grader,
  results, receipt). Nothing trial-material lives only in /tmp.
- Durable lesson: corpus access does not eliminate confabulation — one bridge
  agent (T4R-A14) invented a plausible-but-wrong 10-step variant of a nine-step
  loop despite having the corpus. Grading rubrics must stay mechanical.
