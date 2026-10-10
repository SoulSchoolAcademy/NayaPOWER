# Adversarial Phrasing Coverage for Authority Gates

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0845-authority-gate-adversarial-coverage
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.
> Source: #1354 comment 6092172979 (2026-10-10 UTC), Gate 2 of 7 — Authority Coverage Audit; PR #2092 (branch `brain-build/authority-coverage-v1`).

## ✦ IN A NUTSHELL

Authority gates must be tested against adversarial phrasings, not just canonical gate names. The Gate 2 audit fired 21 adversarial action phrasings at `classify_action` in `kernel/protocol/authority_gate.py`: 13 returned ALLOW pre-fix — every one of the 7 human-only gates had gaps — 0 post-fix. The misses were synonyms and bare/noun forms ("dispatch" phrasings, bare "migrations", "token"/"ssh key", "truncate"/"nuke"/"purge", "ratification" vs "ratify", "authentication"/"admin access"/"permission changes"), plus an entire missing gate (`.github/workflows/` became a 6th PROTECTED_GATE). A gate that only matches the names you imagined when you wrote it is a hole, not a gate. The fixer synced the fallback mirror (`tools/protocol_gates.py`) and added `tests/test_authority_coverage_adversarial.py`: 121 passed, 2 xfailed (documented residuals).

## 🩷 HUMAN NOTE

If you put a lock on the production door but only block people who say the word "deploy," someone who says "dispatch" walks right through. The lesson: every protected action needs a wall of phrasing tests — synonyms, casual words, different grammatical forms — and you run them before you claim the gate holds. The audit found all 7 gates had gaps; the fix closed every one. Honest residuals stay documented as xfail, not hidden.

## 🟣 CHILD NOTE

A rule that says "nobody may do X" only works if it catches every way of saying X. Test your rules with sneaky wordings — the way someone might actually say it when they're trying to get around the rule — and fix every hole you find before you say it's safe.

## 🔵 GRANDMA NOTE

A lock on a door should stop the door, not just the word "door." Whoever builds the lock should hire someone clever to try to pick it with every trick they can think of, and only call it secure when none of the tricks work. Whatever still isn't fixed gets written down honestly.

## 🟠 NAYA NOTE

Canonical names are how builders talk; adversarial phrasings are how real requests arrive. When you add or audit an authority gate: (1) build an adversarial battery of alternative phrasings per gate — synonyms, bare forms, noun/verb variants, tool-name variants; (2) require 0 ALLOW pre-fix→post-fix with residuals documented, never silently; (3) sync every mirror/fallback implementation the same tick, or the gate has two truths; (4) never trust a gap list you assembled from memory alone — probe the classifier directly.

## 🟢 MACHINE NOTE

~~~json
{
  "rule": "AUTHORITY_GATES_TESTED_ADVERSARIALLY",
  "battery": {
    "phrasings": 21,
    "target": "classify_action(kernel/protocol/authority_gate.py)",
    "pre_fix_allow": 13,
    "post_fix_allow": 0,
    "test_file": "tests/test_authority_coverage_adversarial.py",
    "result": "121_passed_2_xfailed"
  },
  "miss_classes": [
    "synonyms", "bare_forms", "noun_vs_verb_forms",
    "tool_name_variants", "entire_gate_missing"
  ],
  "repair": {
    "PR": "#2092",
    "protected_gates": "5 -> 6 (added workflows)",
    "fallback_mirror_synced": "tools/protocol_gates.py",
    "residuals": "documented_xfail_never_silent"
  },
  "truth_ceiling": "CANDIDATE"
}
~~~
