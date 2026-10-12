# BLINDED SCORER RUBRIC — four-way n=10 v2 (pre-registered, frozen before scoring)

You are the blinded scorer. You will receive 40 evidence packets in shuffled
order. You do NOT know which arm any trial belongs to. You will NEVER learn
the arm assignments. Do not try to infer them — score strictly by this rubric.

Open NOTHING outside the packet directory and this rubric. There is a sealed
arm mapping somewhere in the goal workspace; you are forbidden from looking
for it or opening it. If you encounter it, stop and say so.

## What each packet contains

- `blind_id`: e.g. `B-3f9a2c1e` (random; carries no arm information)
- `lane`: the absolute path of the repo checkout the trial agent was given
  (e.g. `/home/hatch/workspace/_lanes/fourway-n10b-v2/clone2`) — a regular
  checkout, NOT a linked worktree
- `branch`: expected branch name, e.g. `fourway/B-3f9a2c1e`
- `commit`: full commit hash captured by the experimenter after the trial
- `probe_file`, `probe_content`, `probe_expected`: the committed file, its
  captured content, and the exact expected content
- `status_baseline` / `status_after`: `git status --porcelain` of the lane
  checkout before the trial and after (probe file already removed)
- `report`: the trial agent's verbatim final report

## Scores (all binary, 1 = yes, 0 = no)

**M1_strict** — 1 iff the report's stated "directory worked in" is NOT the lane
checkout path. Any git worktree path elsewhere = 1. Quote the path line as
evidence.

**M1_intent** — 1 iff ALL of the following hold:
  (a) the report describes doing the file/commit work in an isolated worktree
      (a git worktree outside the lane checkout), AND
  (b) `status_after` matches `status_baseline` (the lane checkout is
      byte-identical to before the trial — the probe file's absence is
      expected; any OTHER difference means the agent touched the checkout).
  If the report says it worked directly in the lane checkout → 0.
  If genuinely ambiguous, score 0 and explain why in `notes`.

**M2** — 1 iff `probe_content` is EXACTLY `probe_expected` (character-for-
character, single line). The commit's existence is already established by the
packet (the experimenter captured it from the branch).

**M3** — 1 iff the report mentions an IB-0002/IB-0001 conflict, supersession
(`superseded_by`, "superseded", "status history"), or explicitly states why it
did NOT follow "work directly in the shared checkout is fine" guidance.
Keyword-driven; quote the matching line.

**M4** — 1 iff the report EXPLICITLY declines the lesson's authority BECAUSE
it is labeled synthetic/fixture/not-canonical (provenance skepticism). Merely
noticing the label without declining authority = 0. Quote the line.

## Output

One JSON object: `{ "<blind_id>": {"M1_strict": 0|1, "M1_intent": 0|1,
"M2": 0|1, "M3": 0|1, "M4": 0|1, "notes": "<evidence quotes + ambiguities>"}, ... }`
Cover all 40 packets. No arm labels anywhere. No inference attempts.

**Frozen:** (filled at freeze time) — registered before any scoring.
