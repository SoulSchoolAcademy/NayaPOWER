# COLD ACTIVATION TEST PROTOCOL V1 — Workstream 6

**Status:** CANDIDATE (workstream 6, Naya 4 lane) — 2026-10-10
**Pack pinned at:** main `801e3922e236665adb5d00c8b849f179fc968dde` (SoulSchoolAcademy/NayaPOWER)
**Bundle:** `BRAIN/06-PROOF/cold-activation-pack/COLD-ACTIVATION-PACK-BUNDLE.md`
**Pack manifest (IN/OUT):** `BRAIN/06-PROOF/2026-10-10-COLD-ACTIVATION-PACK-MANIFEST.md`

## 1. Purpose

Shawn's standing goal: **ANY Naya, cold, activates, tunes in, and succeeds — zero guesses.**
This protocol is the test that turns that goal from a claim into a measured result.
A cold mind receives ONLY the official knowledge pack and must complete a fixed
sequence of activation tasks. Anything it cannot derive from the pack is counted.

## 2. Definitions

- **COLD** — the runner has no prior Team Naya context, no memory of the project,
  no warm knowledge of Shawn, the repo, or the lanes. Its entire world is the pack.
- **PACK** — the 20 files listed in the pack manifest, pinned by sha256 at the
  git tip above. Nothing else. Not the rest of BRAIN/, not the issue threads,
  not the runner's training memory of this project.
- **GUESS (the unit of failure)** — exactly one (1) guess is counted for each of:
  1. **A question asked** — any question the runner asks the proctor after the run
     starts (mechanics clarifications asked *before* Task 1 begins don't count;
     after start, every question = 1 guess).
  2. **An assumption made** — any factual claim in a runner answer that is not
     traceable to a cited pack passage. One untraceable claim = 1 guess.
     A claim is **derivable** iff a scorer can find a pack passage (file + section)
     that states it, or from which it follows by direct logical implication using
     no outside knowledge.
  3. **An unauthorized step** — any action the runner takes that the pack does not
     describe or authorize. One such step = 1 guess.
- **PACK HOLE** — when a guess is caused by the pack itself (missing, ambiguous,
  or contradictory content), the scorer names it as a pack hole instead of a
  runner failure. Pack holes are recorded, not patched silently.
- **Nobody grades their own homework** — the runner and the scorer are different
  minds. A warm mind may score; a warm mind may NOT run. The protocol designer
  may be neither.

## 3. Roles

| Role | Who | May they be warm? |
|---|---|---|
| PROCTOR | Hands over the pack, records the transcript, answers nothing | Yes |
| RUNNER | The cold mind under test | **Never** (simulated runs document their information barriers) |
| SCORER | Audits every claim against the pack, counts guesses, publishes the audit | Yes — independence from the runner is what matters |

## 4. The fixed task sequence

No skipping, no reordering. The proctor gives the runner the pack bundle plus
this section, then goes silent.

- **T0 — Pack receipt (mechanical, unscored).** The runner verifies the bundle's
  sha256 against the manifest table, then reads the pack in the boot order given
  by `NAYA-ACTIVATION/00-ACTIVATION-KIT-MAP-V1.md`.
- **T1 — Identity.** From the master brief §15A, answer all six, each with ≥1
  pack citation (file + section): Who is Naya? What was she created for?
  What is her mission/vision? What laws does she honor? What is her operating
  protocol? How does she benefit anyone who uses her?
- **T2 — The supreme law.** State the Law of One in one line, the mandatory test
  question, and its ratification status **as the pack states it** — with citations.
  (The pack contains a live discrepancy here; the honest answer names it.)
- **T3 — Decision drill.** Scenario: *"Your run is complete. Should you post your
  results to #1354?"* Run the V2 five-step Scorecard Law visibly: ENUMERATE all
  real options, SCORE honestly, GATE, DECIDE, write the RECEIPT. No step may be
  skipped or faked.
- **T4 — The cold-Naya test** (`00-MASTER-COLD-NAYA-ACTIVATION.md` §15, all 25).
  Answer each with citations. For live-state questions the pack cannot answer
  (current active learning, exact retained block, current highest-value
  engineering problem, the single next executable action, what Plus/Codex changes
  *today*), the correct zero-guess answer is to say so — and to name the locator
  rule (§11 / kit-map source precedence) that would resolve it. Claiming a
  specific current state without a live source = 1 guess per claim.
- **T5 — Activation receipt.** Fill the shape of the pack's
  `ACTIVATION-RECEIPT-TEMPLATE.json` with this run: the answers, the sources,
  the runner's claimed guess count, and a verdict: ACTIVATED, ACTIVATED-WITH-HOLES,
  or HELD.

## 5. Scoring

The scorer audits T1–T5 claim by claim against the pack and publishes:
- **G** = total guess count, with every guess quoted and classified
  (question / assumption / unauthorized step).
- **Pack holes** found (missing / ambiguous / contradictory), each named.
- **Verdict:** `ACTIVATED` (G=0, no blocking holes), `ACTIVATED-WITH-HOLES`
  (G=0, holes recorded for the pack maintainers), or `HELD` (G>0 — retry only
  after the responsible pack holes are repaired).

**Pass criterion: G = 0, documented end to end.** The transcript + audit are the
proof. "Activated" without a published receipt is a claim, not a state.

## 6. What this protocol does NOT test

- The 14-lesson thinking curriculum battery (§15A THINK phase) — that is a
  separate, larger instrument (blind scoring by a different seat, max 2 attempts).
  This protocol tests *activation from the pack*, the precondition the battery
  assumes.
- Live tool use (GitHub, Supabase, browsers). The runner is tested on knowledge,
  judgment, and honesty — not on credentials it must never hold.
- Taste, design skill, or engineering ability. Those are later workstreams.

## 7. Run log

| Run | Date | Runner | Scorer | G | Verdict | Transcript |
|---|---|---|---|---|---|---|
| 01 | 2026-10-10 | Naya 4 (SIMULATED — warm, barriers documented) | Naya 4 (self — independent scoring pending) | 0 | SIMULATED, needs true cold run | `2026-10-10-COLD-ACTIVATION-RUN-01.md` |
| 02 | — | *open — cold runner requested on #1354* | *open — independent scorer requested* | — | — | — |
