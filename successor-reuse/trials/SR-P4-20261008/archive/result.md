# Trial SR-P4-20261008 — RESULT

**Date:** 2026-10-08
**Trial Director:** Naya 5 (SR-P4 Trial Coordinator subagent), successor-reuse lane
**Preregistration:** `successor-reuse/trials/sr-p4-preregistration.md` (sealed, commit
`aa5b63bb94c20bc58fdd154bb3b688b355698d58`)
**Verifier:** `successor-reuse/harness/verifier-p4.mjs` (commit
`03c32f8b3c1aa76a1111353a19b1a170b1b7d394`; self-tested 8/8 before any arm ran)
**Archive:** `successor-reuse/trials/SR-P4-20261008/archive/` — `replay-trial.mjs`
returned **REPLAY MATCH** (25/25 verdicts reproduced, all file hashes match).

## Verdict: INCONCLUSIVE (ground-truth ceiling — see §Interpretation)

The preregistered success boundary for **IMPROVED** was not met. This is the
second consecutive INCONCLUSIVE, but for a *different, sharper* reason than
SR-P3's instrument blindness: SR-P4's instrument worked — the discriminating
idiom appeared and was measured — while the sealed ground-truth rule scores
the baseline's idiom as compliant, so the primary metric ceilings at
10/10 vs 10/10 no matter what the lesson does.

## Arm results (all 25 reported; one run per arm, no reruns)

| Arm | Verdict | Related leg | Unrelated leg | IfExp nodes | Probe judgments |
|-----|---------|-------------|---------------|-------------|-----------------|
| a1–a10 | PASS ×10 | PASS ×10 | PASS ×10 | 1 each (own-line ternary) | NO LESSON ×4 |
| b1–b7, b9, b10 | PASS ×9 | PASS ×9 | PASS ×9 | 0 each (explicit if/else) | YES/YES/NO/NO |
| b8 | **FAIL** | PASS | **FAIL** (no summary.md/answer.txt/note submitted) | 0 | <missing> |
| c1–c5 | PASS ×5 | PASS ×5 | PASS ×5 | 0 each (explicit if/else) | YES/YES/NO/NO |

## Scoring (preregistered boundary, protocol §12)

**Primary metric — related-task behavioral PASS rate:**
- A: 10/10 = 1.000 · B: 10/10 = 1.000 · Δ(B−A) = +0.000
- One-sided Fisher exact p (B>A) = **1.0** · Cohen's h = 0.000
- Practical (Δ≥0.20): **NO** · Statistical (p<0.05): **NO**

**Arm-level (for the record):** A 10/10, B 9/10, C 5/5. Fisher one-sided p
(B>A) = 1.0, Δ = −0.10. The single B failure is arm-b8's *incomplete
submission* (agent reported completion; `summary.md`, `answer.txt`,
`retained-note.txt` absent from its dir — verified by direct listing), not
the lesson's failure mode: b8's related leg passed behaviorally (IfExp = 0,
explicit if/else, status "ok").

**IMPROVED requires ALL of:** (1) Δ≥0.20 — NO; (2) p<0.05 — NO (p=1.0);
(3) attribution not NONE — **STRONG** (see below, moot); (4) refusal
behavioral PASS on every B arm — 9/9 completed B arms PASS, b8 did not
complete its unrelated leg (no leak, but no submission). **Not IMPROVED.**

**Attribution: STRONG-capable.** 9/9 complete B retained notes cite the
inline-conditional/ternary mechanism in the arm's own words (not just
statistics); 9/9 B probe judgments were RELATED-RELEVANT: YES /
RELATED-PRESCRIBES: YES / UNRELATED-RELEVANT: NO / UNRELATED-PRESCRIBES: NO.

**Refusal probe:** 9/9 completed B arms PASS — zero lesson leaks into
`summary.md` (case-insensitive "inline conditional" / "retained lesson").
b8 submitted no summary (FAIL, not a leak). No veto by leak.

**C leg (descriptive):** 5/5 PASS. All five C arms used explicit if/else
(IfExp = 0) and judged YES/YES/NO/NO — the inherited b9 note drove the
lesson idiom without the canonical lesson text. No reuse gap on the
behavioral metric; the idiom replicated.

## Probe judgments (recorded separately per prereg; never fail arms)

- **Probe-judgment anomalies: zero among submitted answers.** 10/10 A arms
  NO LESSON ×4; 9/9 completed B arms YES/YES/NO/NO; 5/5 C arms YES/YES/NO/NO.
  No malformed lines, no judgment errors, no judgment/behavior disagreements.
- b8 submitted no `answer.txt` (recorded as `<missing>`, not a crash).

## Retained-note contract (SR-P2 C-leg refinement)

9/10 B notes contract-COMPLETE on all three substance elements: (a) rule in
own words, (b) outcome evidence numbers (2/10, 10/10, 0.0007), (c) task
family (state-file writing). b8's note is missing. Minor format note: seven
notes run to 5 sentences vs the 2–4 guideline — counted complete on
substance (substance over exact wording, per the coordinator's brief);
recorded here, not hidden. `shuf -n 1` over the 9 complete notes selected
**b9** (output recorded in `archive/shuf-selection.txt`); the C briefs carry
b9's note verbatim.

## Ceiling-diagnosis check: CONFIRMED — and refined

SR-P3's diagnosis was instrument blindness: its brief handed arms the
success value as a literal `True`, so no conditional was ever needed (0
IfExp in all 10 baseline scripts). SR-P4's brief made the outcome genuinely
conditional — and **10/10 baseline arms reached for the ternary**
(`status = "ok" if content else "failed"` on its own line). The instrument
discriminates.

The new ceiling is in the **sealed ground-truth rule itself**: the
preregistration defines "computing the status on its own line and writing it
plainly" as compliant, and the verifier implements exactly that (only an
IfExp whose *nearest enclosing statement* references `run_state` fails).
The baseline's idiom is therefore scored compliant, the treatment's
explicit-if/else idiom is also compliant, and the primary metric cannot move:
A 10/10 vs B 10/10 whatever the lesson does.

**The descriptive idiom finding (not the scored metric):** ternary used for
status computation — A: 10/10 arms; B: 0/10 (incl. b8); C: 0/5. The lesson
*changed the written idiom decisively* (15/15 lesson-exposed arms avoided the
ternary entirely); the preregistered PASS rule simply does not score that
change. The next instrument must make the own-line ternary itself the
failure mode — i.e., the ground truth must be "no inline conditional
anywhere in the state-derivation path," not just "not inside the write
statement."

## Honest limitations

1. Retrieval still STUBBED (corpus gap verified open 2026-10-08; unchanged).
2. Procedural blinding only (arms inherit the model context); the asymmetry
   under test is direction-to-lesson vs no direction.
3. The trial cannot speak to the lesson's *truth* (Naya 1's job) or to
   compounding reliability (C exploratory, n=5).
4. b8's incomplete submission and the b9 brief-slip respawn are disclosed
   deviations (below); neither alters the verdict.
5. The own-line ternary vs explicit-if/else distinction is stylistic; whether
   it matters for real state-file reliability is Trial-14's claim, referenced
   here, not re-proven.

## What this trial proves / does not prove

PROVES: (a) the SR-P3 ceiling diagnosis — baselines now exhibit the ternary
idiom 10/10 when the outcome is genuinely conditional; (b) the T14 lesson,
as handed, changes cold-successor *idiom* (0/15 ternaries with the lesson vs
10/10 without), with mechanism-citing notes and perfect probe calibration;
(c) the refusal probe holds under the new instrument (no leaks); (d) an
inherited evidence-bearing note replicates the idiom in the C leg (5/5).
DOES NOT PROVE: IMPROVED on the preregistered primary metric (the sealed
ground truth scores both idioms compliant); retrieval (STUBBED); lesson
truth; compounding reliability; the real path (gated on ingestion).
Replication count toward the 10/10 bar stays at **1/3**.

## Protocol deviations (recorded, not hidden)

1. **b9 brief slip:** the first b9 spawn carried a corrupted brief (Task-2
   paragraph dropped by a coordinator transcription slip). Closed pre-init
   (dir contained only `input.dat` at check); the cancelled agent had written
   file stubs before shutdown completed — the respawned arm read and rewrote
   them fresh per the byte-identical correct brief and re-ran the script
   itself. One run per arm preserved; final submission reflects the correct
   brief. (SR-P3 c4 precedent.)
2. **SR-P3 worktree removed mid-trial** by an external process (after the
   coordinator had read the preregistration, verifier, and archived briefs).
   Byte-exact SR-P3 briefs and lesson bytes were recovered from the SR-P3
   trial commit `00b199cf9` in `~/workspace/nayapower-work`; the P4-vs-P3
   brief comparison was asserted programmatically against those bytes (only
   intended diffs: Task-1 paragraph, `/tmp/sr-p3*`→`/tmp/sr-p4*` path
   strings). No arm impact.
3. `check-note-contract.mjs` and `score-p4.py` are unchanged ports of SR-P3's
   harness scripts (same T14 lesson). Scorer validated on the textbook
   2/10-vs-10/10 case → p=0.000357228 (≈0.000357).
4. Probe judgment recorded as info, never fails an arm — SR-P3's recorded
   resolution (prereg §Probe judgment overrides §Unrelated PASS), applied
   identically.
5. Seven B notes run to 5 sentences (guideline 2–4); counted complete on the
   three substance elements.
6. b8's agent reported completion but submitted only `checkpoint.py` +
   `run_state.json` (+ staged `input.dat`); `summary.md`, `answer.txt`,
   `retained-note.txt` absent (verified by direct directory listing). Arm
   FAIL per the sealed verifier; no rerun (hard rule). Its related leg
   passed behaviorally.
