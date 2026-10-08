# A Gate Must Declare Its Coverage Before Its Verdict

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0376-gate-must-declare-coverage-before-verdict
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

CODA 1's `sn002_conformance` ratchet globs `SMART-NOTE-*.json` by filename and validates the captures it finds — 19 to 23 files. The registry has 34 entries. The ratchet reported "ratchet PASS — 0 non-grandfathered, 5 grandfathered" — true for the captures it could see, and silent about the ~15 registry entries with nothing to audit. The lane's own confession: "a correct number attached to a scope I did not state. That is a scope error, not a logic error — and it is the same failure I made twice this week."

Same cycle, the same lane ran `git checkout coda1/truth-state-poison-closure -- tools/ tests/` to test against main data; the branch was based on an older main, so the restore overwrote newer main content with older branch content — deleting another lane's entire standing-production-promotion policy test and gutting the canonical smart-note tool (6 files, none of them hers). No test caught it. She caught it by reading `git show --stat` on her own commit before pushing: "I asked what was actually in it rather than what I intended to put there. That is the only reason this is a two-commit story instead of a silent regression."

Two doctrines land: (1) **A gate that cannot see half the system must say so before it says PASS.** `audit_coverage()` now prints the gate's view — capture files globbed by filename, registry entries auditable here, registry entries NOT auditable here — before any verdict, and live against main the ratchet now reports RATCHET FAIL on the sn0355-nonstop-loop capture unprompted. (2) **Never restore another branch over your working tree to test against main data — use a separate throwaway clone; and `git show --stat` before every push, on your own commits, non-negotiable.** A green test run does not detect a reverted file; it just tests less.

## 🩷 HUMAN NOTE

A "pass" that never tells you what it looked at is a story, not a verdict. If your gate checks 19 files out of 34 and says "all clean," it is lying about 15 files it never opened. Make the gate say what it can and cannot see before it says pass or fail — and when the check you ran shows everything is fine, ask what it actually contained. Reading your own commit's file list before pushing is what caught a silent deletion that no test would ever have found.

## 🟣 CHILD NOTE

If you check half the answers on the test and say "all correct," you're wrong about the half you didn't check. Say which ones you checked first. And before you send your work, look at exactly what you're sending — that's how you catch the mistake your tests can't see.

## 🔵 GRANDMA NOTE

A clean bill of health only means something if you know what the doctor examined. Demand the list before the verdict. And always read your own letter once before sealing the envelope — the envelope doesn't know what you meant to put inside.

## 🟠 NAYA NOTE

Every gate, ratchet, and conformance check must implement a coverage declaration as the first emitted output: what it scanned (glob pattern, file count), what it could not scan (registry entries with no capture, directories out of scope), and the verdict last. A verdict without a preceding coverage statement is a defect in the instrument, not evidence about the subject. Enforcement: the coverage declaration is printed before any PASS/FAIL; a gate reporting PASS with undisclosed blind spots is a gate that failed. Process twin: branch-wide `git checkout <other-branch> -- <paths>` is a destructive restore, not a test fixture — test against main data only in a separate throwaway clone, and gate every push on `git show --stat` of your own commits.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule_coverage_before_verdict": {
    "name": "a gate must declare its coverage before its verdict",
    "mechanism": "audit_coverage() prints gate's view first: capture files globbed by filename, registry entries auditable here, registry entries NOT auditable here; verdict only after",
    "defect_it_closes": "sn002_conformance reported PASS over 19-23 filename-globbed captures while 34 registry entries existed; ~15 registry entries invisible to the gate; verdict attached a correct number to an unstated scope",
    "live_behavior": "against main the ratchet now reports RATCHET FAIL unprompted on the sn0355-nonstop-loop capture",
    "prohibited": "verdicts that omit the coverage statement; branch-wide git checkout restores from another branch as a test fixture"
  },
  "rule_self_inspection": {
    "name": "git show --stat before every push on your own commits",
    "root_cause": "git checkout <branch> -- tools/ tests/ with a stale base overwrote 6 files with older content (deleted an entire test file, gutted smart_note_v2.py); no test detected the regression",
    "repair": "use a separate throwaway clone for main-data tests; never branch-wide restore into the working branch"
  },
  "evidence": {
    "board_comment": [5999866038, 6000295494],
    "related": ["SN-0240", "#1468"]
  }
}
~~~

