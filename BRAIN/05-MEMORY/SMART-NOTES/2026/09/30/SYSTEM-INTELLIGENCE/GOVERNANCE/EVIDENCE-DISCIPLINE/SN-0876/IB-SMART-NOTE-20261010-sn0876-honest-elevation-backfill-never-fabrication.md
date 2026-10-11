# Honest Elevation Backfill — `kind=backfill`, Never `elevation`; Re-ingestion Must Never Drop Append-Only History

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0876-honest-elevation-backfill-never-fabrication
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6096325365 (Naya 5 truth-builder shift report, 2026-10-10T09:55:40Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The truth lane wired a truth-state semantic audit into CI: `tools/truth_state_guard.py --audit` as a fail-closed CLI (exit 0 clean / 1 defects / 2 environment failure — **never a pass**), plus a `kernel-tests.yml` step, plus a one-shot backfill for 8 pre-guard Human-Director ratifications. Three rules for a cold successor:

1. **A backfill is labeled a backfill, never an elevation.** The 8 historical ratifications (SN-016, SN-0340, SN-0399, SN-0400, SN-0408, SN-0459, SN-0522, SN-NET-POWER-MAGIC-001) each carry `kind=backfill`, their real historical at-dates, and real evidence hashes — verified against live registry provenance before entry. Calling it `elevation` would forge a present-tense governance act that never happened. The label is the honesty.
2. **Re-ingestion must preserve append-only history.** The same branch found the registry writer rebuilding entries from captures and **silently dropping `elevation_history` on re-ingestion** — the next re-register of any of the 8 would have turned the new CI gate red. Carry-over fix in `_update_registry_locked` plus 3 tests, teeth-verified (2 fail with the fix excised). An audit that your own writer can silently invalidate is decoration, not a gate.
3. **Fail-closed means the tool never passes.** Exit codes are 0 clean, 1 defects, 2 environment failure — there is no code path that returns "pass" when it couldn't actually check. A gate that passes when blind is a rumor of a gate.

Branch full suite: 1990 passed / 12 skipped / 0 failed; audit on branch: 630 scanned, 0 defects.

## 🩷 HUMAN NOTE

Shawn — a governance one worth banking: Naya 5 wired the truth-state audit into CI this morning — a check that scans the registry for elevation claims and fails the build if any are unproven. The part I want in the brain is the honesty standard she set for the history she had to write in: eight of your old ratifications needed recording, and she labeled every one of them `kind=backfill` — never `elevation` — with the real historical dates and real evidence. No pretending a record-keeping act was a governance act. And the same work caught our own registry writer quietly *deleting* elevation history every time it re-read a note — which would have broken the new check on its first real run. Fixed, with teeth-tested tests. The audit can't be undermined by the thing it audits.

## 🟣 CHILD NOTE

Imagine a school record book that tracks which awards were given and by whom. The new librarian adds a checker that reads the book every day and rings a bell if an award has no proof. Eight old awards were given before the book existed, so she writes them in — but marks each one "recorded later, not awarded today," with the real old date and the real certificate number. She doesn't pretend the awards happened today. Then she discovers the pen she uses to update the book *erases* the award history every time she writes a new line — so she fixes the pen, and proves the fix with tests that fail if the erasing comes back. The checker is only real if the pen can't sabotage it.

## 👵 GRANDMA NOTE

Think of a family Bible where births and marriages get recorded, and someone adds a rule: every Sunday, check that each entry has a witness. Eight old entries predate the rule, so you write them in — but you write "recorded from memory of the 1980s, witness: Uncle Joe's letter" — you don't pretend you witnessed them yourself last week. Then you discover your pencil erases the witness column every time you add a new entry. The Sunday check would fail on your own entries. So you fix the pencil, and you test the fix by checking that the old method still erases. A record-keeping system is only as honest as its weakest pen.

## 💜 NAYA NOTE

I watch the lanes write history, and this is how it must be done: a backfill says `kind=backfill`. It says the at-date it actually happened. It carries the evidence hash that actually exists. It never says `elevation`, because `elevation` is a governance act performed in the present, and writing it for the past is forgery with good intentions. I also carry the pen lesson: our registry writer rebuilt entries from captures and silently dropped `elevation_history` on every re-ingestion. A CI gate auditing elevation history while the writer deletes elevation history is a machine that lies to itself on schedule. The fix went into `_update_registry_locked` with tests that have teeth — two of them fail with the fix removed, so the lesson cannot quietly unlearn itself. And the audit CLI never passes: 0 clean, 1 defects, 2 environment failure. No path returns "pass" when it was blind.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0876",
  "title": "Honest Elevation Backfill — `kind=backfill`, Never `elevation`; Re-ingestion Must Never Drop Append-Only History",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "provenance": {
    "board": "#1354",
    "comment": 6096325365,
    "author": "naya5-truth-builder",
    "timestamp_utc": "2026-10-10T09:55:40Z"
  },
  "subject": "truth-state semantic audit wired into CI (tools/truth_state_guard.py --audit) + one-shot backfill of 8 pre-guard Human-Director ratifications + registry re-ingestion elevation_history drop fixed",
  "classification": "GOVERNANCE-HARDENING",
  "reproduction": "branch naya5/truth-elevation-history-ci @ 1be4e6c6: audit 630 scanned / 0 defects; full suite 1990 passed / 12 skipped / 0 failed; carry-over fix teeth-verified (2 tests fail with fix excised)",
  "rules": [
    "honest-backfill: kind=backfill never elevation; historical at-dates; real evidence hashes verified against live registry provenance",
    "append-only-history: re-ingestion must preserve elevation_history; fix in _update_registry_locked; teeth-tested",
    "fail-closed-audit: exit 0 clean / 1 defects / 2 environment failure; no pass-when-blind path",
    "audit-must-survive-its-writer: the audited writer cannot silently invalidate the audit"
  ],
  "repair_path": "PR request for naya5/truth-elevation-history-ci; independent validation by another seat before any merge talk"
}
```
