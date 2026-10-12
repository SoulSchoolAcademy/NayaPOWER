# Human Value instrument — method verification report v1

**Naya Mu (HUMAN VALUE lead) · 2026-10-12 ~02:24–03:05 UTC · Lane Gamma #1715**
**Branch:** `naya5/human-value-method-validation` (includes PR #2417 grader fix)
**Label: FIRST-PARTY.** Naya Mu built the instrument (`tools/human_value/instrument.py`);
this battery is her own check. A different seat must re-verify before the
charter's Definition of Done is met.

## Nutshell

The human-value instrument had its measurement method stress-tested against 25
synthetic scenarios with known answers. It misfired on 3 of them; all 3 were
mechanical bugs and were fixed in this run. Battery is now 25/25 green, and
the 5 real pilot packets still grade byte-identically to the published pilot
report (8.8 / 7.3 / 6.8 / 6.8 / 8.2) — the fixes changed nothing for legitimate
packets.

## Human note

We have a scoreboard for human value — a tool that grades whether a shipped
change actually helped someone, based on evidence. But nobody had ever checked
whether the scoreboard itself tells the truth. So I built 25 rigged tests
where I already knew the right answer: a change that clearly helped, one that
did nothing, a harmful one, a broken one, a fake-it one — and ran the
scoreboard against them. It got 22 right and 3 wrong. I fixed the 3 wrong ones
and re-ran: 25 out of 25 right. One honest boundary remains: the scoreboard
checks that evidence is real, but it can't tell whether the person writing the
grade is being honest — that part still needs a second human (or second seat).

## Child note

Imagine a teacher's grading machine. We gave it 25 tests where we already knew
the scores. It graded 3 wrong. We fixed the machine. Now it gets all 25 right.
But the machine can't tell if a student cheated on the answers — it only
checks that the answers are written down properly. A second teacher still needs
to check for cheating.

## Grandma note

Dear, we built a little judge that scores whether our work truly helps people.
Before trusting the judge, I tested it with 25 practice cases where I knew the
fair score in advance. It stumbled on three — small mechanical mistakes, like
misreading which lines of a page someone pointed at. I corrected all three,
and now it scores every practice case perfectly. The one thing it can't do is
read hearts: if someone writes a glowing grade for worthless work, the judge
will believe the paperwork. That's why a second person always double-checks.

## Machine note

- **Subject:** `tools/human_value/instrument.py` @ `a3767489d0` (PR #2417 grader fix) + 3 method fixes (this branch)
- **Harness:** `tools/human_value/method-validation/battery/run_battery.py` (stdlib only, exit 0 = all known answers match; fixtures rebuilt under `/tmp/mv-fixtures` each run)
- **Result:** 25/25 PASS. Last run summary: `battery/last-run.json`
- **Regression:** all 5 pilot packets (`pilot/packets.json`) re-graded against this checkout → scores identical to PILOT-REPORT.md; zero UNVERIFIABLE evidence introduced by the fixes
- **Fixes (mechanical, in-lane):** recheck now carries cited `lines` through content-drift comparison (was whole-file hash); test-file heuristic tightened (was bare substring `"test" in basename`); `compare` now fails closed on `change_id` mismatch (was unenforced)
- **Portability note:** score totals depend on CPython ≥3.12 compensated `sum()`; on older interpreters a last-decimal flip (e.g. 8.8 → 8.7) is possible. Deterministic on this runtime.

## Learning lesson

A measurement instrument is only as honest as its verification battery — and
the battery must be written from the contract BEFORE the instrument runs, not
shaped to fit its output. Writing the known answers first caught three real
bugs that "it works on the pilot" never would have: whole-file drift
masquerading as cited-range drift, a substring heuristic any filename could
spoof, and an unenforced identity check that could have manufactured
"agreement" between grades of two different changes. The pilot proved the
instrument works on real data; the battery proved it works on adversarial
data. You need both.

## What it means

The charter's Definition of Done for the human-value lane requires independent
verification OF THE MEASUREMENT METHOD. This report delivers the first-party
half: the method is now mechanically verified against known answers, with
every misfire found, fixed, and re-proven green. The second half — a different
seat re-running this battery cold and confirming 25/25 — is still open and is
explicitly NOT claimed here.

## How to apply it

1. A different seat: clone this branch, run
   `python3 tools/human_value/method-validation/battery/run_battery.py`,
   confirm exit 0 and 25/25, and post the independent verification receipt.
2. Merge lane: this branch carries no PR and no merge press per lane rules;
   merge decision belongs to the merge lane after independent verification.
3. Future instrument changes: re-run the battery; any red case is a
   method regression — treat it as a P0.

## What's in it for you

Shawn gets a scoreboard he can trust at the mechanical level: when the
instrument says a change is REAL VALUE with verified evidence, that claim has
survived 25 adversarial probes. And the team gets a standing battery — every
future change to the instrument must stay green against it, so the
measurement method can never silently rot.

---

## Case results (known answer → instrument output)

| Case | Scenario (known answer) | Result |
|------|--------------------------|--------|
| KV-01 | Fully verified evidence, claimed 9s → 9.0 HIGH VALUE | PASS |
| KV-02 | Zero evidence, claimed 9s → 3.0 NO VALUE [NO_EVIDENCE_CAP] | PASS |
| KV-03 | harm_check found=true → DISQUALIFIED, score None | PASS |
| KV-04 | Attested-only evidence (command/url) → 5.0 THIN [UNCITED_CAP] | PASS |
| KV-05 | Receipt-only DELTA=10 → 8.0 [RECEIPT_SOFT_CAP]; total 8.8 REAL VALUE | PASS |
| KV-06 | Main-tip ref (PR #2417 fix): no collapse, equals ref^1..ref | PASS |
| KV-07 | Branch head: merge-base(origin/main)..head covers full branch delta | PASS |
| KV-08 | 8 malformed packet variants → exit 2, no score emitted | PASS |
| KV-09 | Verdict boundaries: all-7→7.0 REAL; all-9→9.0 HIGH; all-5→5.0 THIN; all-4→4.0 NO VALUE | PASS (4) |
| KV-10 | Cited file missing at ref → UNVERIFIABLE → 5.0 THIN [UNCITED_CAP] | PASS |
| KV-11 | Recheck: cited lines 1–3 unchanged, rest of file changed → drift UNCHANGED | PASS (was FAIL → fixed) |
| KV-12a | Compare identical cards → TRUST, 5/5 agree | PASS |
| KV-12b | Compare mismatched change_id → rejected, exit 2 | PASS (was FAIL → fixed) |
| KV-12c | Compare 9-vs-4 cards → DISPUTE, verdict mismatch, gap 5.0 | PASS |
| KV-13 | Test citation of non-test file (`contest_notes.md`) → UNVERIFIABLE, USE capped 5.0 | PASS (was FAIL → fixed) |
| KV-14 | No origin/main → documented ^1 fallback (last-commit delta only) | PASS |
| KV-15 | Recheck after cited file deleted → ROTTED on all dimensions | PASS |
| KV-16a | to-event REAL VALUE → schema-valid event minted, delta_v_actual=6.0 | PASS |
| KV-16b | to-event NO VALUE → refused, exit 2, mints nothing | PASS |
| KV-17a/b | pilot skeleton built with null scores; scoring it fails closed (exit 2) | PASS (2) |
| KV-18 | Verified citations + hollow 9s on docs tweak → 9.0 HIGH VALUE (trust boundary) | PASS |

## The three misfires — found, fixed, re-proven

**M1 — recheck content-drift compared the whole file, not the cited lines.**
`recheck_scorecard` rebuilt the citation as `{"kind", "path"}` and dropped the
`lines` the grader had cited; the drift hash then compared whole-file bytes.
A file edited outside the cited range reported CHANGED. Fix: carry
`item.get("lines")` through the citation. (KV-11 red → green.)

**M2 — test-file heuristic was a bare substring.** `"test" in basename`
accepted `contest_notes.md` as test evidence. Fix: accept only `tests/`
paths or test-named files (`test_*.py`, `*_test.*`, `*.test.*`). All real
pilot test citations still verify. (KV-13 red → green.)

**M3 — `compare` never checked both cards were for the same change.** Two
scorecards for different changes could report "agreement" — manufactured
consensus. Fix: fail closed with `InstrumentError` on `change_id` mismatch.
(KV-12b red → green.)

## What this does NOT claim (D32)

- Does NOT claim independent verification — this is first-party; a different
  seat must re-run the battery cold.
- Does NOT claim the instrument judges the truth of a grader's judgments —
  KV-18 proves it passes verified citations with hollow scores. Grader honesty
  is the human trust anchor; `compare` exists for second-seat checks.
- Does NOT claim real-world human outcomes — synthetic git fixtures, not
  production changes; the event-ledger side (`compute_hv.py`) is out of scope.
- Does NOT claim cross-interpreter score stability — last-decimal totals
  depend on CPython ≥3.12 compensated `sum()`.
- Does NOT claim the 5 pilot scores are "correct" human-value judgments —
  only that the fixed instrument reproduces them byte-identically (no
  regression from the 3 fixes).

## Receipts

- Battery: `tools/human_value/method-validation/battery/run_battery.py` (25 cases, 25/25 PASS, `last-run.json`)
- Report: this file
- Instrument delta: 3 surgical fixes, +24/−2 lines, all in `tools/human_value/instrument.py`
- Base: `665098e3f0` + PR #2417 commit `a3767489d0` (merged into branch)
- Commands: `python3 tools/human_value/method-validation/battery/run_battery.py` → exit 0
