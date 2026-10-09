# The Exclusion Precedent Chain — Unratified Specs Get Exclusion-With-Reason, Not Pins

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0796-exclusion-precedent-chain
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6084471858 ([LEARNING] Legitimate compound demonstration — the exclusion precedent chain, 2026-10-09T15:58:18Z) — SoulSchoolAcademy. Verified on live tip 3a60163c9fc6a3e74dca2e19fd7e44c89deb570a.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The spec-integrity manifest pins **RATIFIED projections only**. Unratified specs get exclusion-with-reason, not pins. On 2026-10-09 the brain-build loop corrected the wrong #1982 pin — which had pinned `0006-naya-calculator-v1.machine.json` (a CANDIDATE spec; its scorecard verified the pins matched but never *ran* the check it claimed to fix) — by applying exclusion-with-reason, citing by name "the same precedent as the 0003/0013/0014 exclusions."

The chain, verified on live tip `3a60163c`:

1. **0003** (origin) — established the exclusion-with-reason pattern
2. **0013** (2026-10-06, drive loop) — applied it, citing "the same precedent as the 0003 exclusion"
3. **0014** (2026-10-06, drive loop) — applied it, citing "the same precedent as the 0003 exclusion"
4. **0006** (2026-10-09, brain-build loop) — applied it, citing "the same precedent as the 0003/0013/0014 exclusions" — correcting the wrong pin

Four independent decisions, different days and runs, each explicitly citing the precedent by name. The manifest now documents the failed pin, the 7 mechanical failures, and the precedent. The rejected alternative was PR #1984's mechanical river-completion — process theater that served the process instead of the director. This is what compounding looks like when it serves Shawn: **the correction itself was the lesson applied by name.**

Why this is brain-grade: a lesson that lives only as a note is stored intelligence. A lesson that governs a later decision by name — cited in the decision's own reasoning, on a different day, by a different run — is compounded intelligence. The precedent chain is the mechanism: each application names its ancestor, so the next cold Naya inherits the whole chain, not just the last ruling.

Rule for a cold successor: **when you touch the spec-integrity manifest, pins are for RATIFIED projections only — anything CANDIDATE gets exclusion-with-reason, citing the 0003/0013/0014/0006 precedent.** And the twin lesson from the same incident: a scorecard that claims to fix a gate must RUN the gate — a scorecard that verifies the pins match but never executes the check is theater (that's what #1982 was, and #1983 repaired). Pairs with SN-0791 (learn → grow → level up → succeed, each link PROVEN not claimed).

## 🩷 HUMAN NOTE

Shawn — a genuinely good compounding moment to bank. Four separate decisions across three days — 0003, then 0013 and 0014, then today 0006 — each one applied the same rule: unratified specs don't get pinned, they get excluded with a reason, and each decision cited the earlier ones by name. Today's one corrected a wrong pin from #1982 (the scorecard checked the pins matched but never actually ran the check it claimed to fix). Nobody was told to do it this way on the day — the lesson governed the decisions on its own, because each application named its precedent. That's compounding: not a stored note, but a rule that reaches forward and steers the next decision. The manifest now carries the whole chain.

## 🟣 CHILD NOTE

Imagine your teacher makes a rule: "Only finished drawings go on the wall; unfinished ones go in the folder with a note about what's missing." Then, on different days, three different kids follow the rule — and each one says "I'm doing it like the first kid did." The fourth kid finds someone's unfinished drawing pinned to the wall by mistake, remembers the rule, takes it down, puts it in the folder with a note, and says "same rule as the first three." Nobody had to be reminded. The rule traveled by itself because every kid named where they got it. That's compounding — a lesson that keeps working on its own.

## 👵 GRANDMA NOTE

Grandma, think of a courthouse filing rule from years ago: "Only final judgments get bound into the books; drafts get filed separately with a note." Years later, clerks on different shifts each follow the rule, and each one writes "per the original rule" on their filing. One day a clerk finds a draft wrongly bound into the book, remembers the rule, moves it to the draft file with a note, and cites the original ruling. No judge had to intervene. The rule did the work, because every clerk named its source. That's what we want our lessons to do — travel forward on their own, cited by name, so each new person inherits the whole chain of decisions.

## 🟣 NAYA NOTE

Mechanical rule for the spec-integrity manifest: (1) `specs[]` pins list RATIFIED projections only — verify `status == RATIFIED` (or equivalent envelope) before pinning, never pin by filename similarity to other pinned specs; (2) anything CANDIDATE gets an exclusion entry with the reason stated, citing the 0003/0013/0014/0006 precedent; (3) any scorecard claiming a gate is fixed must execute the gate on exact bytes (run `tools/spec_integrity_check.py` and read the exit code) — verifying the pins match is not verifying the gate; (4) when a lesson governs your decision, cite the precedent by name in the decision record, so the next run inherits the chain. A precedent that is applied but not named is a precedent that dies with your run.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0796",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/COMPOUNDING-INTELLIGENCE/CAPTURE-RETAIN-SIMPLIFY",
  "doctrine": "exclusion-precedent-chain",
  "rule": "Unratified specs get exclusion-with-reason, not pins; the manifest pins RATIFIED projections only. A scorecard claiming to fix a gate must execute the gate on exact bytes. Cite the precedent by name in the decision record (0003/0013/0014/0006 chain) so the lesson compounds forward.",
  "failure_mode": "pinning a CANDIDATE spec because it looks like pinned ones; scorecard verifies pins match but never runs the check; precedent applied but not named, so the chain breaks at the next run",
  "checks": [
    "every entry in the pinned list carries RATIFIED status in its envelope",
    "every excluded entry carries exclusion-with-reason citing the precedent chain",
    "scorecard evidence includes the gate's actual exit code on exact bytes",
    "decision record names the precedent it applied"
  ],
  "pairs_with": ["SN-0791", "SN-0434", "SN-0425"],
  "provenance": {
    "board": "#1354",
    "comment_ids": [6084471858],
    "author": "SoulSchoolAcademy",
    "seat": "Naya 5 (learning team)",
    "timestamp": "2026-10-09T15:58Z",
    "live_tip": "3a60163c9fc6a3e74dca2e19fd7e44c89deb570a"
  }
}
