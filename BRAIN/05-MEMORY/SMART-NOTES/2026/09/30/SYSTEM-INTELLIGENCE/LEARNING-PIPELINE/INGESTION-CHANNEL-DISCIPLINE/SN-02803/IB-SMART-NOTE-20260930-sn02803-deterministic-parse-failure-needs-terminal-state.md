# A Deterministic Parse Failure Needs a Terminal State — Ingestion Re-attempts the Same Six Notes Every Run

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02803-deterministic-parse-failure-needs-terminal-state
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/learn/ingestion-log.md (1,365 runs; latest run 2026-11-14T15:08:43Z, run 20261114T150829Z, branch naya4/smart-notes-2026-09-30 @ 2f05d53c0ec2); per-note `##`-header shapes verified first-hand in the branch mirror this tick.

## ✦ IN A NUTSHELL

Six Smart Notes have failed ingestion parse on every LEARN run for a month — SN-0345 (1,322 occurrences), SN-0459, SN-0460, SN-0594, SN-0600, SN-0614 (1,279 each) — because they predate the six-section IB format: SN-0345 and SN-0600 use `## Essence` headers, SN-0459 has a bare `## MACHINE` label, SN-0460 and SN-0614 have no MACHINE section at all, SN-0594 has no `##` headers whatsoever. The loop re-scans the branch tree fresh every run and re-attempts them on identical bytes, so the failure is deterministic — and quarantine.json records first_seen / last_seen / seen_count for each one without ever gating the re-attempt. Recording a failure is not handling it. The rule: a deterministic failure needs a terminal state — skip after N consecutive identical failures (keyed by content sha), or repair the notes into IB format. Until either lands, a new PARSE_ERROR in the log is indistinguishable from the six permanent ones, so the log's error tail carries no signal at all.

## 🩷 HUMAN NOTE

Shawn — imagine a librarian who checks every returned book against the catalog, and six books are in a language the catalog can't read. Every morning she tries them again, fails again, and writes "couldn't read these six" in the log — for a month, 1,279 mornings in a row. She never sets them aside, never fixes them, never asks anyone to translate them — she just keeps trying and keeps failing, and the log fills up with the same six complaints until a genuinely new problem would be invisible in the noise. The fix is one of two moves: put the six on a "don't try again until something changes" shelf, or translate them into the language the catalog reads. The lesson underneath: a system that records a failure but never acts on the record is just a diary of the same mistake. The six notes aren't the problem — the loop with no ending is.

## 🟣 CHILD NOTE

Imagine you try to fit six puzzle pieces into a puzzle every single day. They don't fit — they're from a different puzzle. But every morning you try the same six pieces again, and every morning they don't fit, and you write it down in your notebook. After a month your notebook is full of "these six don't fit" and you can't find the note about the new piece that broke yesterday. The smart move: put those six pieces in a special box labeled "different puzzle — try again only if the puzzle changes," or find someone to reshape them so they fit. Trying the same pieces that never fit, every day, forever, isn't being careful — it's being stuck.

## 🔵 GRANDMA NOTE

Dear, it's like the neighbor who comes to your door every morning with the same six letters addressed to someone who moved away years ago. You tell him every day, "They don't live here," and he writes it down — and comes back the next morning with the same six letters. A month of mornings, and the notebook is full of the same note, and the one morning a letter comes for someone who actually lives here, you can't see it for all the old notes. The fix is simple: put those six letters in a drawer marked "gone away — don't bring again unless something changes," or find the right address and forward them properly. A record that never changes what you do is just clutter with a date on it.

## 🟠 NAYA NOTE

Evidence, first-hand this tick: hidden_files/learn/ingestion-log.md holds 1,365 runs; the 15:08:43Z run (20261114T150829Z, branch @ 2f05d53c0ec2) lists PARSE_ERROR for SN-0345, SN-0459, SN-0460, SN-0594, SN-0600, SN-0614 — the same six as every run. Occurrence counts in the log: SN-0345 1,322; the other five 1,279 each. Ledger stands at 2,105 entries; quarantine.json shows 6 open. The six notes' shapes, read from the branch mirror: SN-0345 (system scorecard method, 2026-10-05) and SN-0600 (charter stratification, 2026-10-04) use `## Essence` / `## What this adds` style headers; SN-0459 (parallel execution directive, 2026-10-06) has `## MACHINE` as a bare label with no emoji-section JSON; SN-0460 (ratified-predecessor guard) and SN-0614 (self-governing intelligence) have no MACHINE section; SN-0594 (hub-is-intelligence-projection, 2026-10-01) has zero `##` headers. None of the six can ever ingest in their current bytes, so their content never reaches the learning ledger — the scorecard-method and charter-gate lessons are invisible to every brief the loop writes. Two costs, not one: the content loss, and the signal loss — the permanent error tail means a seventh, genuinely new parse failure is camouflaged on arrival. Repair path is one of two: (1) terminal state in learn_ingest — after N consecutive identical failures (same content sha), mark the path skipped in quarantine.json and stop re-attempting until the bytes change; (2) repair the six notes into the six-section IB format (re-file, not reconstruct — the content is on the branch, only the shape is wrong). Cousin map: SN-1546 (quarantine-drop doctrine — triage by reconstructability; this note is the loop-side twin: quarantine records but doesn't gate); SN-0786 (instruments must be total functions — cousin: a check that can't handle a legal input; here the loop can't handle a permanently-illegal one); SN-1643..1648 class (bare-label staging quarantine — different axis: staging-time format vs ingestion-time re-attempt); SN-0624 (quarantine snapshot is point-in-time evidence).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "deterministic_parse_failure_needs_terminal_state_skip_or_repair_never_reattempt_identical_bytes_forever",
  "mechanism": "learn_ingest re-scans the branch tree fresh on every run with no memory of past failures except quarantine.json, which records first_seen/last_seen/seen_count but is never consulted to skip — recording without gating. The six notes predate the six-section IB format, so split_sections finds no MACHINE NOTE (or a malformed one) on byte-identical input every run, and the failure is deterministic: same bytes, same error, forever. The permanent error tail then dilutes the log — a new parse failure is indistinguishable from the six known ones — and the six notes' content never enters the learning ledger",
  "evidence": "hidden_files/learn/ingestion-log.md (1,365 runs): latest run 2026-11-14T15:08:43Z (run 20261114T150829Z, branch @ 2f05d53c0ec2) lists PARSE_ERROR SN-0345, SN-0459, SN-0460, SN-0594, SN-0600, SN-0614; occurrence counts SN-0345 1,322, other five 1,279 each; ledger 2,105 entries, quarantine 6 open. First-hand header reads in the branch mirror: SN-0345/SN-0600 Essence-format; SN-0459 bare ## MACHINE label; SN-0460/SN-0614 no MACHINE section; SN-0594 zero ## headers",
  "falsifiability": "if the loop gains a skip-list or terminal state, or the six notes are repaired into IB format, the PARSE_ERROR lines for these six SNs stop appearing in ingestion-log.md; if any of the six ingests unchanged, the determinism claim fails; if quarantine.json is shown to already gate re-attempts (a run skips a listed path), the mechanism claim fails",
  "decision_change": "when the LEARN owner next touches learn_ingest, add a terminal state — skip a path after N consecutive identical parse failures keyed by content sha, recorded in quarantine.json which the loop already writes — or repair the six notes into IB format; until either lands, a LEARN run receipt must diff its PARSE_ERRORs against the known-six set before calling the run clean",
  "applies_when": [["ingestion", "parse-failure"], ["learning-pipeline", "re-attempt"], ["memory", "legacy-format"]],
  "enforcement": "the LEARN run receipt must list PARSE_ERRORs diffed against the known-six set (SN-0345/0459/0460/0594/0600/0614) — any PARSE_ERROR outside that set blocks the run's clean verdict; and once a skip-list lands, the quarantine.json seen_count for these six must stop growing on the next run, verified by diffing ingestion-log.md across two consecutive runs",
  "related": ["SN-1546 quarantine-drop-doctrine — triage by reconstructability; this note is the loop-side twin: quarantine records but doesn't gate", "SN-0786 verification-instruments-must-be-total-functions — cousin: a check that can't handle a legal input", "SN-1643..1648 bare-label staging quarantine — different axis: staging-time format vs ingestion-time re-attempt", "SN-0624 quarantine-snapshot-stale-reconstruct-live-bytes"]
}
~~~
