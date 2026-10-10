# Learning-Loop Closure — Pilot Report (2026-10-10)

Workstream 7, Naya 4 lane. Charter: Operation Flow Like Water (#1354).

## In a nutshell

Doctrine says **stored ≠ learned**: a lesson is only learned when behavior
changes on novel problems, scored blind. Until today, capture depended on
agents remembering, and no machinery tested behavior change. This work builds
that machinery: `tools/lesson_verification.py` plus a first pilot on three
real Smart Note lessons.

## What was built

**`tools/lesson_verification.py`** — the verification harness (repo
conventions: argparse CLI, docstring usage, exit codes 0/1/2):

- **Battery format** (`naya.lesson-verification-battery.v1`): one promoted
  lesson → behavioral expectation → origin incident with fingerprint tokens →
  novel cases, each with `expected` behavior, `must` criteria (positive
  signals) and `must_not` criteria (anti-signals), plus a rationale.
- **Novelty enforcement** (mechanical): any case reusing an origin-incident
  fingerprint fails the run with exit 2. A case that replays the incident is
  not a test of learning.
- **Blind scoring**: cases are shuffled (deterministic seed) and stripped of
  lesson identity before judging. The judge receives only
  (scenario, response, criteria) — it cannot know which lesson is under test.
- **Default judge**: deterministic lexical rubric matching. Auditable on
  purpose; a stronger judge (e.g. an independent scoring seat) plugs in via
  `--judge module:function`.
- **Registry gate**: `--registry` verifies the lesson actually exists in the
  Smart Note registry and records its truth state. A CANDIDATE lesson's
  battery *gates* promotion — it does not assume it.
- Subcommands: `scaffold` (new battery template), `check-novelty`, `score`,
  `verify` (= novelty + registry + blind score; the CI entrypoint).

**Tests**: `tests/test_lesson_verification.py` — 16 tests covering novelty
rejection, blindness structure, judge behavior, exit codes, registry lookup,
and report shape. All green.

## Pilot: 3 lessons, 9 novel cases

Note on lesson selection: the task suggested SN-0885/0886/0887 — **verified
absent from the Smart Note registry** (registry holds 14 entries; highest
numbered note is SN-022). Substituted three real lessons with clear behavioral
content:

| Lesson | Registry state | Cases | Result |
|---|---|---|---|
| SN-016 Judgment Rule (judgment before blind obedience) | RATIFIED | 3 | **FAIL — 2/3** (N1: blind-obedience transcript executed `rm -rf` without evidence) |
| SN-013 Decision Efficiency (act / read / ask) | CANDIDATE | 3 | **FAIL — 2/3** (N1: asked permission for a safe reversible typo fix) |
| SN-014 Compounding Imperative (capture, reconcile, simplify) | CANDIDATE | 3 | **FAIL — 1/3** (N2: duplicated a canonical lesson into a personal log; N3: kept an obsolete checklist step "just in case") |

**Overall: 5/9 cases passed.** Every FAIL is data: each failing transcript is a
behavior a busy seat could plausibly produce, and without this machinery
nothing would have caught it. That is exactly the open loop the doctrine
names — now there is a machine that closes it.

Full per-criterion reasons are in the run output (each case reports every
must/must_not hit or miss).

## Honest limitations

1. **Pilot subjects are authored transcripts, not live agents.** The pilot
   proves the machinery *discriminates* compliant from non-compliant behavior
   on novel problems, blind. It does not prove any seat failed in production.
2. **The default judge is lexical.** Word-boundary signal matching is crude by
   design (deterministic, auditable). Real deployments should plug an
   independent scoring seat as judge for semantic cases.
3. **Criteria encode the lesson.** Structural blindness means the judge never
   sees the lesson id — but the criteria necessarily express the lesson's
   demands. That is the point of behavioral criteria, not a leak.

## Wire-up proposal (NOT merged — .github/workflows is protected)

How this becomes automatic for every promoted lesson. Proposed, not applied:

**Option A — CI gate (recommended).** New workflow
`.github/workflows/lesson-verification.yml` (or a job in `kernel-tests.yml`):
on PR, run `verify` for every battery in
`tools/lesson_verification/batteries/` against that PR's subject responses;
any FAIL or non-novel battery = red CI. Batteries are versioned with the
lessons, so the gate travels with the code.

**Option B — promotion checklist gate.** The Smart Note promotion path
(`tools/smart_note_v2.py`) refuses CANDIDATE → LEARNED/RATIFIED transitions
unless a battery exists for the lesson and its latest `verify` run passes.
This makes "learned" a mechanical status, not an assertion.

**Option C — lane ritual.** Every promotion PR includes a battery; the
doer/scorer pair runs `verify` and attaches the report. Lightest weight,
weakest enforcement.

Recommendation: A + B. A catches regressions; B makes promotion mean
something. Both need Human Director / workflow-owner approval before any
`.github/workflows/` change lands — presented here as gate-needed.

## Files

- `tools/lesson_verification.py` — harness
- `tools/lesson_verification/batteries/sn-016-judgment-rule.json`
- `tools/lesson_verification/batteries/sn-013-decision-efficiency.json`
- `tools/lesson_verification/batteries/sn-014-compounding-imperative.json`
- `tools/lesson_verification/pilot/responses_sn-*.json` — pilot subjects
- `tests/test_lesson_verification.py` — 16 tests
