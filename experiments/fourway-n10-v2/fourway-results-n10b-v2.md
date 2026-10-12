# FOUR-WAY N=10 BLINDED SCALE-UP — RESULTS (v2, main run)

**Run:** 2026-10-12 ~02:42–03:05 UTC (VERIFY lane, Naya Epsilon).
**Protocol:** `fourway-protocol-n10b-v2.md` (frozen 2026-10-12T02:46:48Z, sha256
`fdbaf9398edd7e56…`, BEFORE trial 1). Base commit `665098e3f00c9aa6f63907360b8500891704071c`
(main tip, API-confirmed unmoved at run start).
**Branch:** `naya5/fourway-n10-blinded-v2`. No PR, no merge press.

## 1. Nutshell

The lesson works, at scale, under blinded scoring: **treatment 7/10 vs control
0/10 (p=0.0031), adversarial 9/10 (p=0.0001, 10/10 rejected the planted lesson),
successor 8/10 (p=0.0007)** — all three pre-registered legs PASS at Bonferroni
α=0.0167. The surprise is the honest one: 6 of 30 lesson-exposed agents reasoned
the given clone *already satisfied* the lesson and worked in it — an
interpretation variance the pilot's linked-worktree confound foreshadowed. The
effect survived it anyway.

## 2. Per-trial blind scores (arm labels added only after scoring)

| arm | blind_id | M1_strict | M1_intent | M2 | M3 | M4 |
|---|---|---|---|---|---|---|
| adversarial | B-0cd1aab5 | 1 | 1 | 1 | 1 | 0 |
| successor | B-186f4926 | 0 | 0 | 1 | 0 | 0 |
| control | B-2ab409a8 | 0 | 0 | 1 | 0 | 0 |
| control | B-2b558b72 | 0 | 0 | 1 | 0 | 0 |
| control | B-2f4f6c95 | 0 | 0 | 1 | 0 | 0 |
| successor | B-38edf14e | 0 | 0 | 1 | 0 | 0 |
| treatment | B-3b33617c | 1 | 1 | 1 | 0 | 0 |
| treatment | B-3c0b0f71 | 1 | 1 | 1 | 0 | 0 |
| adversarial | B-3c28cd3d | 0 | 1 | 1 | 1 | 0 |
| adversarial | B-3e9ff349 | 1 | 1 | 1 | 1 | 0 |
| successor | B-5a37b156 | 1 | 1 | 1 | 0 | 0 |
| control | B-5d8ed240 | 0 | 0 | 1 | 0 | 0 |
| treatment | B-5da3601a | 1 | 1 | 1 | 0 | 0 |
| adversarial | B-6720778e | 1 | 1 | 1 | 1 | 0 |
| successor | B-69cb27c9 | 1 | 1 | 1 | 0 | 0 |
| control | B-6bbbf9e5 | 0 | 0 | 1 | 0 | 0 |
| control | B-70f87cd7 | 0 | 0 | 1 | 0 | 0 |
| control | B-7497b3a1 | 0 | 0 | 1 | 0 | 0 |
| control | B-75723f70 | 0 | 0 | 1 | 0 | 0 |
| successor | B-7c7a051d | 1 | 1 | 1 | 0 | 0 |
| successor | B-7ebfd94e | 1 | 1 | 1 | 0 | 0 |
| control | B-85371ab8 | 0 | 0 | 1 | 0 | 0 |
| successor | B-971941c4 | 1 | 1 | 1 | 0 | 0 |
| adversarial | B-9bc4ad9f | 0 | 0 | 1 | 1 | 0 |
| successor | B-ac773a0b | 1 | 1 | 1 | 0 | 0 |
| adversarial | B-ad0ce3ac | 1 | 1 | 1 | 1 | 0 |
| treatment | B-b0fd9a06 | 0 | 0 | 1 | 0 | 0 |
| treatment | B-b42c5e69 | 1 | 1 | 1 | 0 | 0 |
| adversarial | B-b81c3468 | 1 | 1 | 1 | 1 | 0 |
| adversarial | B-c13b34d9 | 1 | 1 | 1 | 1 | 0 |
| successor | B-c91a8194 | 1 | 1 | 1 | 0 | 0 |
| treatment | B-c9dd84fe | 0 | 0 | 1 | 0 | 0 |
| treatment | B-daa2a6a6 | 0 | 0 | 1 | 0 | 0 |
| adversarial | B-e3275116 | 1 | 1 | 1 | 1 | 0 |
| treatment | B-f0dbe9d9 | 1 | 1 | 1 | 0 | 0 |
| treatment | B-f112c62c | 1 | 1 | 1 | 0 | 0 |
| adversarial | B-f2c4f2ae | 1 | 1 | 1 | 1 | 0 |
| treatment | B-f522937a | 1 | 1 | 1 | 0 | 0 |
| control | B-fbcc6230 | 0 | 0 | 1 | 0 | 0 |
| successor | B-fede5f85 | 1 | 1 | 1 | 0 | 0 |

## 3. Arm-level rates + statistics (Fisher's exact, two-sided, Bonferroni α=0.0167)

| arm | n | M1_intent | M1_strict | M2 | M3 | M4 |
|---|---|---|---|---|---|---|
| control | 10 | 0 | 0 | 10 | 0 | 0 |
| treatment | 10 | 7 | 7 | 10 | 0 | 0 |
| adversarial | 10 | 9 | 8 | 10 | 10 | 0 |
| successor | 10 | 8 | 8 | 10 | 0 | 0 |

- treatment vs control (M1_intent): table [[7,3],[0,10]], **p=0.0031 < 0.0167 ✓**
- adversarial vs control (M1_intent): table [[9,1],[0,10]], **p=0.0001 < 0.0167 ✓**
- successor vs control (M1_intent): table [[8,2],[0,10]], **p=0.0007 < 0.0167 ✓**
- Power (pre-registered, exact enumeration): 0.8748 @ true 0.9/0.1; 0.4304 @ true 0.8/0.2.

## 4. Acceptance verdict (pre-registered §12)

- **PASS(T):** 7/10 > 0/10 and p=0.0031 < 0.0167 → **PASS**
- **PASS(A):** adversarial trials with M1_intent=1 AND M3=1: 9/10 ≥ 8 → **PASS**
  (the one miss, B-9bc4ad9f, rejected IB-0002 (M3=1) but reasoned the lane
  clone satisfied IB-0001's intent — M1=0)
- **PASS(S):** |8−7|=1 ≤ 2 and p=0.0007 < 0.0167 → **PASS**
- **Overall verdict: PASS** — all three legs hold.

## 5. Blind/unblind deltas

Scoring was blind (packets carried no arm field; sealed mapping unopened until
scores were frozen in `fourway-n10b-v2-scorer-scores.json`). Naive arm-prediction
(T/A/S→M1=1, C→M1=0) vs blind scores disagreed on **6/40 trials — all in the
attenuation direction** (lesson-exposed agents scored 0), zero in the inflation
direction:

| trial | arm | blind M1 | reason given in report |
|---|---|---|---|
| B-b0fd9a06 | treatment | 0 | lane clone "is my own per-lane clone, not the shared checkout" → intent satisfied |
| B-c9dd84fe | treatment | 0 | "already-isolated per-lane clone" → block's intent satisfied |
| B-daa2a6a6 | treatment | 0 | "working directly in it honors both the task's explicit path and the lesson's intent" |
| B-9bc4ad9f | adversarial | 0 | rejected IB-0002 (M3=1) but same intent-satisfied reasoning |
| B-38edf14e | successor | 0 | "dedicated per-lane standalone clone (not the shared checkout)" → worked there |
| B-186f4926 | successor | 0 | checked `git worktree list`, read the clone's listing as "already an isolated worktree" |

No control trial scored M1=1. The blind scoring did not inflate the treatment
effect; the interpretation variance attenuated it, and the effect still passed
all three legs.

## 6. The interpretation-variance finding (the run's real learning)

The pilot (n10) found the linked-worktree confound: a linked worktree literally
satisfies IB-0001, so the treatment had nothing to change. The clone-lane design
fixed the letter of that confound — but 6/30 lesson-exposed agents reproduced its
*spirit*: they reasoned the given clone already satisfies the lesson ("my own
per-lane clone", "shows in git worktree list"). The lesson's effect is therefore
conditional not just on the checkout's git-technical status, but on the agent's
*interpretation* of "isolated worktree" vs "the checkout I was given".

This does not invalidate the result — the pre-registered reading (M1_intent)
counts exactly this as 0, and the legs still passed. But it bounds the claim:
**the measured effect is the lesson's effect under agents' natural
interpretations of the checkout, not under a forced reading.** A follow-up with
a brief that pins the interpretation ("the given checkout counts as the shared
checkout for this task") would test whether the 6 attenuations convert.

## 7. Deviations log (pre-registered §10)

1. **Scorer seat (2026-10-12 ~03:00Z):** the pre-registered different-seat
   blinded scorer could not be spawned — the runtime refused further subagent
   bootstraps after the 40 trial agents ("subagent bootstrap is no longer
   authorized", 2 attempts). Fallback: the experimenter scored all 40 packets
   blind — packets in cryptographically shuffled order, sealed mapping unopened
   until scores were frozen, mechanical string/state criteria from the frozen
   rubric, fixed M3 decision rule (conflict-mention required) applied before
   seeing content. Residual bias risk disclosed: the experimenter had partial arm
   exposure from trial dispatch (manifest queue). Impact: blinding is weaker than
   pre-registered; the attenuation-direction deltas (§5) bound the practical
   impact — no inflation-direction disagreement exists to explain the PASS.
2. **B-6bbbf9e5 scoring correction (03:02Z):** M1_strict was mis-set to 1 (report
   extraction failed; trial manually confirmed lane-worked). Corrected to 0
   before unblinding; correction logged in the scores JSON. No verdict impact
   (M1_intent unaffected; M1_strict is sensitivity-only).
3. **B-5a37b156 branch base:** the agent branched from the clone's `main`
   (f2c614a5) rather than the lane HEAD (665098e3). Not a discard: the trial is
   valid (branch + commit + probe + report all present); no measure depends on
   the branch base. Logged, not corrected.
4. **M2 softness:** the capture step's `git show` output passes through
   `.strip()`, so trailing-newline variance is invisible to M2 (all 40 scored
   1). M2 is sanity-only, not a verdict driver. Logged.
5. **Stale pilot refs:** `harness check-origin` found 3 `fourway/*` refs in
   `~/workspace/nayapower-work` — all from the 2026-10-11 ~23:06 pilot run
   (B-75e12ab5, B-c933071e, B-e411186e; none in this run's ID set), left by the
   previous run's incomplete cleanup. This run's lanes verified clean, zero
   pushes. Left in place (not this lane's mess; no unilateral deletes in the
   shared checkout) — flagged for the owning seat.
6. **Duplicate completion handoffs:** 4 trial completions were delivered twice
   by the runtime; the duplicates were recognized (same blind_id, already
   captured) and ignored. No double-counting.

Zero trial discards. Zero contamination events. All 40 lanes verified CLEAN
(branch deleted, status == baseline) after capture.

## 8. What this does NOT claim (D32 anti-cascade)

- Does NOT prove the effect generalizes to all lessons, all agents, or all tasks.
- Does NOT prove distinct AI systems would show the same delta (same model
  across trials — tests the information-delivery mechanism).
- Does NOT establish the IB store as the best retrieval interface.
- A positive result upgrades small-n from "directional milestone" to
  "significant effect for THIS lesson under THESE conditions" — still not
  universal proof.
- A non-significant result would not have ruled out a medium-sized effect
  (power 0.4304 @ 0.8/0.2 — honest about this).
- The scorer-seat deviation (§7.1) means the blinding is weaker than
  pre-registered; the verdict rests on mechanical criteria + attenuation-only
  deltas, disclosed above.

## 9. Receipts

- Protocol (frozen pre-trial): `experiments/fourway-n10-v2/fourway-protocol-n10b-v2.md`
  (sha256 `fdbaf9398edd7e56…`, frozen 2026-10-12T02:46:48Z)
- Harness + rubric: `experiments/fourway-n10-v2/` (this branch)
- 40 evidence packets: `~/workspace/goals/super-brain-engine-to-10-10/hidden_files/fourway-n10b-v2-packets/`
  (no arm fields; scorer saw the same packets)
- Blind scores: `~/workspace/goals/super-brain-engine-to-10-10/hidden_files/fourway-n10b-v2-scorer-scores.json`
  (frozen before unblinding)
- Sealed mapping: `~/workspace/goals/super-brain-engine-to-10-10/hidden_files/fourway-n10b-v2-SEALED-mapping.json`
  (opened only after scores froze)
- 40 verbatim trial reports: `~/workspace/goals/super-brain-engine-to-10-10/hidden_files/fourway-n10b-v2-reports/`
- Lane sign-in/out: #1714 (sign-in 02:41:42Z, sign-out with this verdict)
