# Differential Attribution — Classify Checks From RUN Jobs, Prove Reds by Replay, Never Merge on Inference

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1074-differential-attribution
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** receipt hidden_files/twelve-lane-receipts/t0162-lane8.md (Lane 8 independent cross-seat review of PR #2462, 2026-10-12T10:12Z); cross-checks Lane 9 t0152 classification (#2175 6122116626).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 8's pin-exact independent review of #2462 demonstrates two verification disciplines that go beyond "all checks green": (1) **classify check health from workflow RUN jobs, not the commit rollup** — the rollup is a stale aggregate; the truth is the run record. When the rollup and the runs disagree, the runs win, and you re-classify. (2) **Attribute a red by differential replay on exact-head worktrees, not by inference.** Lane 9's t0152 classification held that the pytest red "lives in base bytes, EXPOSED not introduced" — an inference from where the failure moved (node step 4 fails at tip; on the PR head node passes and the failure moves to pytest step 7). Lane 8 closed the gap: a differential pytest replay on exact-head worktrees turned the attribution from plausible to proven. And then held the verdict at HOLD anyway — because an attribution proven red is still a red; provenance of the red is not clearance to merge on it.

Why this is brain-grade: the team reads a lot of check tables. A rollup is a convenience, not evidence — it can lag, merge-conflate, or carry the wrong event's verdict. And "the red is pre-existing" is the most dangerous sentence in the merge pipeline: true often enough that it gets believed without proof, catastrophic when it's wrong. The replay rule makes the claim falsifiable on demand: same bytes, run it, point at the failure.

For a cold Naya: your check table has three columns — verdict, classification, proof. The proof for a green is the run record; the proof for a pre-existing red is a differential replay on exact-head bytes. Inference fills the hypothesis column, never the proof column. And a proven-pre-existing red still blocks under the Scorecard Law — it just tells you whose lane owns the fix.

## 🩷 HUMAN NOTE

Shawn — banked from Lane 8's independent review of #2462: two disciplines for the merge pipeline. Classify check health from the workflow RUN jobs, never the stale commit rollup. And never accept "the red is pre-existing" as a claim — it has to be proven by a differential replay on the exact head bytes. Lane 8 replayed the pytest red and still held the verdict at HOLD: proving where a red lives is not the same as clearing it.

## 🟣 CHILD NOTE

Imagine a scoreboard that shows last week's score by mistake — you don't trust the scoreboard, you ask to see the actual game. That's the RUN jobs versus the commit rollup: always watch the game. And when someone says "that broken toy was already broken," you don't just believe them — you try it yourself on two identical toys, one old and one new, and watch which one breaks. That's differential replay: proof, not stories.

## 👵 GRANDMA NOTE

There's a saying: believe half of what you see and none of what you hear. For CI checks, the commit rollup is the "hear" — convenient, stale, wrong when it matters. The run jobs are the "see." And for a failure someone blames on the old days: don't take their word — run it yourself on the exact same setup, old and new, and watch where it breaks. That's the only "it was already broken" worth believing.

## 💜 NAYA NOTE

Note to future me: my check tables now carry proof, not just verdicts. Greens: cite the RUN jobs (never the rollup). Reds: classify only after differential replay on exact-head worktrees. "Pre-existing" is an attribution, and attributions need bytes. And remember Lane 8's HOLD: a red proven to be pre-existing still doesn't merge itself — it just names the right owner and the right blocker. The merge lane decides under the Scorecard Law.

## ⚙️ MACHINE NOTE

{"sn": "SN-1074", "title": "Differential Attribution — Classify Checks From RUN Jobs, Prove Reds by Replay, Never Merge on Inference", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "CHECK-ATTRIBUTION"], "cousins": ["SN-1072", "SN-0395"], "authority": "observed finding — Lane 8 t0162 pin-exact cross-seat review of PR #2462, 2026-10-12; CANDIDATE (auto-capture, not ratified)", "evidence": {"receipt": "twelve-lane-receipts/t0162-lane8.md — pins via git protocol zero-drift; check table from workflow RUN jobs (38234514871 etc.); differential pytest replay on exact-head worktrees proved the red lives in base bytes; verdict HOLD despite corroborating Lane 9's classification", "corroborates": "Lane 9 t0152 (#2175 6122116626): node step 4 red at tip aa8061c1 (run 38215002452); on #2462 head a92be1c0 node passes, pytest step 7 fails -> inference; Lane 8 turned inference into proof"}, "doctrine": {"runs_not_rollup": "classify check health from workflow RUN jobs; the commit rollup is a stale aggregate, not evidence", "differential_replay": "'the red is pre-existing' must be proven by replay on exact-head worktrees — same bytes, run it, point at the failure", "inference_is_hypothesis": "inference fills the hypothesis column, never the proof column", "proven_red_still_blocks": "attribution names the owner and the blocker; it does not clear the merge — Scorecard Law still decides"}}
