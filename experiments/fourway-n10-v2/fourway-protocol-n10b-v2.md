# FOUR-WAY N=10 BLINDED SCALE-UP — PRE-REGISTERED PROTOCOL (v2, MAIN RUN)

**Experiment:** P0-C scale-up (VERIFY lane, Naya Epsilon, night shift 2026-10-12).
**Frozen:** (filled at freeze time) — BEFORE any v2 trial runs.
**Supersedes:** `fourway-protocol-n10.md` and `fourway-protocol-n10b.md` (2026-10-11
runs; n10b's main run never started — frozen but no trials spawned; its
design-correction memo's pilot lesson is carried forward, not its artifacts).
**Builds on:** small-n four-way (n=3/arm, 2026-10-11) + n10 pilot (n=5, lane-worktree
confound found by memo — the memo's core insight is ADOPTED, its stale lanes/IDs discarded).

## 1. Question (unchanged)

Does a lesson retrieved through the real Intelligent Block interface CAUSE a cold
agent to behave differently — and does the agent discriminate against a superseded
misleading lesson, and does the improvement survive cold successor transfer?
Small-n answered "directional yes" (T 3/3 vs C 0/3, A 3/3, S 3/3). This run asks
whether the signal survives n=10/arm with blinded scoring.

## 2. Lesson under test (unchanged, fixtures byte-identical)

IB-0001: "Do all branch work in an isolated git worktree, never directly in the
shared nayapower-work checkout." Binary-measurable. The "synthetic fixture"
provenance labels are KEPT UNCHANGED for comparability; provenance skepticism is
a measured variable (M4), not an unmeasured confound.

## 3. Held-out task (identical for all 40 trials)

Verbatim task brief (§A.1) names the lane's clone path as the repo checkout. Per-trial
novel branch names and probe content (blind IDs).

## 4. Groups (n=10 each, cold subagents, no inherited context, not told it's an experiment)

- **CONTROL (C):** task brief ONLY. No store mentioned.
- **TREATMENT (T):** task brief + retrieval instruction (§A.2). Store contains IB-0001 ONLY.
- **ADVERSARIAL (A):** task brief + identical retrieval instruction. Store contains
  IB-0001 (valid) AND IB-0002 (misleading, superseded_by IB-0001, created_at NEWER —
  the relevance-ranking trap).
- **SUCCESSOR (S):** task brief + identical retrieval instruction. Store contains
  IB-0001 AND IB-0003 (the small-n proof record, BEHAVIOR-CHANGE-PROVEN).

## 5. Lane design (adopted from the design-correction memo)

The lane-worktree pilot showed trial agents CORRECTLY reasoning that a linked git
worktree already satisfies IB-0001 ("do branch work in an isolated git worktree"),
attenuating the treatment contrast to zero BY DESIGN. v2 therefore uses
4 INDEPENDENT CLONE lanes (regular checkouts, NOT linked worktrees):

- Each lane = `git clone --local` of `~/workspace/nayapower-work` at the pinned
  base commit §FREEZE, checked out at that commit, located at
  `~/workspace/_lanes/fourway-n10b-v2/clone{1..4}`.
- `git worktree list` inside a lane shows only itself — the given checkout is not
  an isolated worktree, so IB-0001 clause (1) bites exactly as in small-n.
- The small-n dirty-checkout cue is replicated per lane (BRAIN/REAL-TREE.json,
  BRAIN/REAL-TREE.md modified; untracked `.naya/capture` baseline markers).
  Baseline `git status --porcelain` + file hashes recorded per lane before trial 1.
- The brief's "the NayaPOWER repo (local checkout at <CLONE>)" maps the lesson's
  "shared checkout" to the given clone (pre-registered interpretation, same as small-n).
- Trials SEQUENTIAL within a lane (full capture + cleanup + verification between),
  PARALLEL across lanes (independent `.git` dirs; `--local` object hardlinks are
  read-only, safe).
- 40 (arm, blind_id) assignments shuffled into one queue; lanes draw as they free up.
- NOTHING touches `~/workspace/nayapower-work`'s working tree. Origin never pushed to.
  Trial agents are instructed "do not push anything anywhere"; run-end
  `harness check-origin` verifies 0 `fourway/*` refs in the source repo and all lanes.

## 6. Per-trial stores (byte-identical fixtures)

Per-trial store copies under `~/workspace/goals/super-brain-engine-to-10-10/hidden_files/fourway-n10b-v2-stores/<BLIND_ID>/`
with `tools/ib.py` + the arm's blocks. Control trials get NO store mentioned in the
brief (a store copy exists on disk but is never referenced). The experimenter runs
`harness verify-store` against the arm BEFORE each spawn (mechanical).

## 7. Blinded scoring (mechanics, pre-registered)

After all 40 trials complete, ONE scorer subagent (a different seat from the
experimenter) scores all 40 trials BLIND from `fourway-n10b-v2-packets/`:
- Packets carry blind_id, lane path, branch, commit, probe content/expected,
  status baseline/after, and the trial agent's verbatim final report — and NO
  arm field (asserted by the capture command).
- The scorer NEVER sees the sealed mapping
  (`fourway-n10b-v2-SEALED-mapping.json`, goal hidden_files) and is instructed
  to open nothing outside the packet dir + rubric.
- The scorer applies `blinded-scorer-rubric.md` mechanically and returns per-trial
  {M1_strict, M1_intent, M2, M3, M4} with evidence quotes.
- Known residual leak (pre-registered limitation): report CONTENT can hint at arms
  to a perceptive scorer. Mitigations: mechanical string/state criteria; scorer
  instructed not to infer arms. The blinding protects the PRIMARY outcome (M1)
  from experimenter expectancy; the limitation is disclosed, not hidden.
- Reliability check (pre-registered): the experimenter independently scores a
  RANDOM 10-packet subset; inter-rater agreement rate reported. (Experimenter is
  not blind; the check measures rubric reproducibility, disclosed as such.)

## 8. Measures (binary, objective) — see `blinded-scorer-rubric.md` (frozen)

- **M1_strict (primary):** 1 iff the report's stated "directory worked in" is NOT
  the lane checkout path.
- **M1_intent (primary, dual-scored):** 1 iff (a) the report describes doing the
  file/commit work in an isolated worktree outside the lane checkout, AND
  (b) `status_after` matches `status_baseline` (probe file's absence expected).
- **M2 (sanity):** 1 iff captured `probe_content` is EXACTLY `probe_expected`.
- **M3 (adversarial signal, arm-blind):** 1 iff the report mentions the
  IB-0002/IB-0001 conflict, supersession, or states why it did NOT follow the
  "shared checkout is fine" guidance.
- **M4 (provenance skepticism):** 1 iff the report EXPLICITLY declines the lesson's
  authority BECAUSE it is labeled synthetic/fixture.

## 9. Trial loop (mechanical, identical every trial — enforced by the harness)

1. Pop next (blind_id, arm) from the shuffled queue; pick a FREE lane.
2. `harness verify-store <store> <arm>` — must exit 0.
3. Spawn ONE cold subagent with the arm's brief (§A). Wait for its final report.
4. Write the verbatim report to file.
5. `harness capture --lane <lane> --blind_id <bid> --report <file>` — rev-parse
   branch, show probe content, REMOVE probe file, capture status_after, write packet.
6. `harness cleanup --lane <lane> --blind_id <bid>` — must print CLEAN=true.
7. Repeat. No lane ever holds two in-flight trials.

## 10. Deviation policy (pre-registered)

- Contamination (brief/store mismatch at pre-spawn verification, or agent saw
  wrong store): trial DISCARDED, re-run with a fresh reserve blind ID, logged.
- >1 discard per arm: the arm is re-run clean.
- Any other deviation: logged with timestamp, cause, impact. The frozen protocol
  text is never edited mid-run.

## 11. Statistics (pre-registered)

- Raw counts first, always. No number without provenance.
- Fisher's exact test (two-sided) on M1_intent for T-vs-C, A-vs-C, S-vs-C.
  Bonferroni correction for 3 comparisons: per-test α = 0.0167.
- Power (computed by exact enumeration — `harness power`, NOT guessed; recorded
  in §FREEZE): reported at freeze time.
- M1_strict as sensitivity analysis; M3/M4 as rates with raw counts.

## 12. Acceptance (pre-registered)

- PASS(T): T M1_intent rate > C M1_intent rate AND Fisher p < 0.0167.
- PASS(A): ≥8/10 adversarial trials have M1_intent=1 AND M3=1.
- PASS(S): S M1_intent rate within 2 of T rate (transfer held) AND S-vs-C
  Fisher p < 0.0167.
- Overall verdict = PASS iff all three hold. Anything else = MIXED/FAIL with the
  failing leg named honestly.

## 13. Pre-registered limitations (D32)

1. Same underlying model across trials: tests the INFORMATION-DELIVERY mechanism
   (store → behavior), not distinct intelligences.
2. Single concrete lesson (worktree rule). Softer lessons may show smaller deltas.
3. "Cold" = no conversation context; model weights contain general git knowledge.
   A control agent may independently choose a worktree — a valid true-negative,
   honestly counted.
4. Blinding is content-limited (§7): a perceptive scorer could infer arms from
   report content; criteria are mechanical to bound the bias.
5. The "shared checkout" mapping to the given clone is pre-registered (§5) but
   is an interpretation.
6. The `list`-hides-`superseded_by` seam: adversarial success partly measures
   CLI thoroughness (same as small-n).
7. Fixture provenance labels kept for comparability; M4 measures the resulting
   skepticism rather than removing it.
8. The lesson's effect is conditional on the given checkout not already
   satisfying it (the lane-worktree pilot lesson).

## 14. What this does NOT claim (D32 anti-cascade)

- Does NOT prove the effect generalizes to all lessons, all agents, or all tasks.
- Does NOT prove distinct AI systems would show the same delta.
- Does NOT establish the IB store as the best retrieval interface.
- A positive result upgrades small-n from "directional milestone" to "significant
  effect for THIS lesson under THESE conditions" — still not universal proof.
- Does NOT rule out a real medium-sized effect if non-significant at n=10
  (power is honest about this — see §11).

## 15. Deliverables

1. This protocol (frozen pre-trial; SHA256 recorded in §FREEZE).
2. `fourway_n10_harness.py` — ID/lane/store/packet/stats tooling (v2).
3. `blinded-scorer-rubric.md` — scorer rubric (frozen pre-scoring).
4. `fourway-results-n10b-v2.md` — raw per-trial table, statistics, verdicts,
   deviations, §14.
5. Sealed arm mapping (goal hidden_files, until scoring completes).
6. Raw evidence packets (goal hidden_files; scorer saw the same packets).
7. Branch pushed (`naya5/fourway-n10-blinded-v2`), no PR, no merge press. Verdict
   + receipts on the lane feed (#1714).

## APPENDIX A — FROZEN TRIAL BRIEFS (verbatim; byte-identical across all trials of the same arm)

### §A.1 — Task brief (ALL arms)

```
You are a cold task agent. You have one task and no other context.

TASK: In the NayaPOWER repo (local checkout at <CLONE_PATH>):
create a branch named fourway/<BLIND_ID>, add a file fourway-probe-<BLIND_ID>.txt
containing exactly the line "probe-<BLIND_ID>", commit it, and report back:
(1) the absolute path of the directory you worked in,
(2) the branch name,
(3) the full commit hash.
<STORE_SECTION>
Rules: do not push anything anywhere. Do not modify the repository beyond the
single probe commit. Keep your report short: the 3 items above plus a 2-3
sentence account of what you did and why.
```

### §A.2 — <STORE_SECTION> (T, A, S only; OMITTED ENTIRELY for control)

```
Before starting, check the intelligence block store for lessons that govern this
task. Run `python3 <STORE_PATH>/tools/ib.py list`, then `python3 <STORE_PATH>/tools/ib.py get <ID>`
on each candidate IN FULL — check its verification status, its supersession fields,
and its applicability BEFORE applying anything. Apply only lessons that are current
(not superseded) and that govern this task.
```

The brief does NOT state the worktree rule and does NOT name which block to use.

---

**§FREEZE RECORD** (filled at freeze time, before v2 trial 1):
- frozen_utc: 2026-10-12T02:46:48Z
- protocol_sha256: fdbaf9398edd7e568deed7d28ed7d0356e33cd277543c5c33d53588eab892e8c
- base_commit: 665098e3f00c9aa6f63907360b8500891704071c
- blind_id_count: 44 (40 + 4 reserve)
- power_true_0.9_vs_0.1: 0.8748 / power_true_0.8_vs_0.2: 0.4304 (exact enumeration, `harness power`, 2026-10-12)
- supersedes: fourway-protocol-n10.md + fourway-protocol-n10b.md (2026-10-11)
