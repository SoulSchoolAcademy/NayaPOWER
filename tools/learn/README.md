# tools/learn

LEARN-area instruments: code that makes learning lessons mechanical instead of prose.

## triage_disagreement.py

Variance-first triage for scorer disagreements (LEARN lesson, 2026-10-12).

Background: learn Battery D's single disagreement (TR-8DB748/M1) first looked
like rubric ambiguity. A preregistered probe re-tested with 3 fresh cold
readers under the FROZEN rubric — they converged unanimously, and a sharpened
rubric showed NO-DELTA (ceiling effect). The split was single-scorer reader
variance. Lesson: **triage reader variance FIRST, before assuming rubric
ambiguity.**

Machine protocol:
1. Validate the record is a genuine disagreement; refuse otherwise.
2. Require a frozen rubric (sha256 registered); refuse unfrozen or drifted.
3. Run N fresh cold readers through the `reader_fn` seam. The seam receives
   ONLY item text + frozen rubric — never the original votes.
4. Fresh readers unanimous → `READER_VARIANCE`: no instrument change, evidence
   recorded. The item is NOT re-graded.
5. Fresh readers still split → `RUBRIC_REVIEW`: escalate with the full evidence
   pack (votes, split pattern, reviewer instructions).

What it does NOT claim: it does not spawn real model readers (coldness is the
harness's operational duty); READER_VARIANCE is calibrated evidence, not proof
of a perfect rubric; it never edits rubrics.

## Usage

```bash
# Run the unit tests
python3 -m pytest tools/learn/test_triage_disagreement.py -q

# Dry-run the real Battery D borderline case (replays recorded votes)
python3 tools/learn/dryrun_battery_d.py

# Triage an arbitrary record file with replayed fresh votes
python3 tools/learn/triage_disagreement.py \
  --record tools/learn/fixtures/battery_d_TR-8DB748.json \
  --replay <fresh_votes.json> --register-rubric --ledger verdicts.jsonl
```

## Files

| file | what |
|---|---|
| `triage_disagreement.py` | the triage module + CLI |
| `test_triage_disagreement.py` | 15 unit tests incl. E2E dry-run |
| `dryrun_battery_d.py` | replays the real TR-8DB748/M1 case; exit 0 on match |
| `fixtures/battery_d_TR-8DB748.json` | real Battery D record + probe re-read (provenance inside) |
| `fixtures/disagreement_persists.json` | synthetic persist-on-reread fixture |
| `ledger.jsonl` | append-only receipts of dry-run triages |
