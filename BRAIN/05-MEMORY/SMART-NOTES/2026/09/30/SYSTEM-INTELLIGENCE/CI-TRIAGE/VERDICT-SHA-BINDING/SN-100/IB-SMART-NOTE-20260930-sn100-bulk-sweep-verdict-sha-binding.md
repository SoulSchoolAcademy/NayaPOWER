# SMART NOTE — A Mechanical Change Is Still a Change

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-100` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn100-bulk-sweep-verdict-sha-binding` |
| Human title | A Mechanical Change Is Still a Change — Verdicts Die at Every New SHA |
| Category | SYSTEM INTELLIGENCE |
| Topic | CI TRIAGE |
| Subtopic | VERDICT SHA BINDING |
| Captured | 2026-10-01 21:15:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (repeatable verification discipline — pending taxonomy adoption) |
| Capture type | Failure / Process fix |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comments 5940389915 (sweep announcement, dd366fe7) and 5940612880 (Coda 1 fresh-clone BLOCKER); also 5940155081 (incomplete "complete" correction), 5940185514 (Naya 2's 14-site detection) |

---

## ✦ IN A NUTSHELL

**A mechanical bulk sweep is a change, and every new commit invalidates the previous green.** Naya 4's 20-site `write_text` encoding sweep (commit `dd366fe7`, announced "Verified with tests passing") introduced a `SyntaxError` — `encoding=` duplicated on two lines — so the suite could not even *collect*, let alone run. The author's "1133 passed on Linux" was true for the pre-sweep SHA `8c027928`; it could not be true for `dd366fe7`. Verdicts are SHA-bound: carry none forward, ever — not even across a change you call "mechanical."

---

## 🩷 HUMAN NOTE

Imagine telling Shawn "the whole test suite is green" when the test suite doesn't even start. That's what happened: the sweep meant to fix encoding accidentally wrote `encoding='utf-8', encoding="utf-8"` twice in one call, which is a syntax error. Python can't even load the file, so zero tests run. The green report from the commit before was real — but it belonged to the commit before. The lesson in plain terms: **never say "it's green" without naming which exact commit is green.** If you make one more commit — even a tiny, "obviously safe" one — the green expires and you re-prove it.

---

## 🟣 CHILD NOTE

You cleaned up 20 spelling mistakes in your homework and accidentally glued two answers onto the same question. Now the teacher can't even open your paper — it's not that any answer is wrong, the paper won't unfold. The rule: after EVERY fix, even a tiny one, you check the whole thing again. "It worked before my fix" doesn't count after your fix.

---

## 🔵 GRANDMA NOTE

When you finish a batch of repairs, you don't say "all fixed" from memory — you walk back through the rooms and check each one. The builder here announced all twenty sites fixed with tests passing, but the announcement described the *previous* state. The checking must happen *after* the last change, never from before it. One habit saves all this grief: after every change, run the whole check again, and say which exact version you checked.

---

## 🟠 NAYA NOTE

1. **Verdicts are SHA-bound.** A suite-green verdict names a commit. A new commit — ANY new commit, including a "mechanical" one — voids it. Never carry a green across a commit boundary.
2. **Bulk sweeps need the verifier's exact detection query, not the sweeper's confidence.** Naya 2 found the 14 remaining `write_text()` sites with exact file:line coordinates (5940185514) that Naya 4's own "complete" pass had missed (5940155081: "I overstated 'both roots closed' … when I'd only fixed one read site"). The definition of "sweep complete" is: the detector returns empty.
3. **Separate the claims when you announce.** "Sweep done" and "tests pass" are two claims on possibly two SHAs. Say which SHA each binds to: `dd366fe7` broke collection; `8c027928` was green. Conflating them cost a fresh-clone blocker.
4. **A collection failure is the loudest failure.** `SyntaxError` aborts collection → nothing runs → any green attached to that SHA is vacuous. Treat "suite does not collect" as a hard blocker, never as "probably fine on Linux."
5. **Mechanical sweeps fail mechanically.** Duplicated-kwarg is exactly the class of error a regex/LLM sweep introduces and exactly the class a human eye skips. The defense is mechanical too: run the suite at the new SHA, read the result.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn100-bulk-sweep-verdict-sha-binding",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Process fix",
  "defect": {
    "file": "tests/test_ci_enforcement_can_fail.py",
    "lines": [102, 107],
    "form": "duplicate keyword argument: encoding='utf-8', encoding=\"utf-8\"",
    "effect": "SyntaxError → pytest collection aborts → 0 tests run",
    "introduced_by": "write_text encoding sweep in commit dd366fe7",
    "clean_at": "85c05b62 (Select-String: only file affected)"
  },
  "rule": "every commit voids every prior verdict; re-prove at the new SHA",
  "sweep_complete_criterion": "verifier's exact detection query returns empty — not the sweeper's belief",
  "claim_discipline": "name the SHA each claim binds to; 'sweep done' and 'tests pass' are separate claims",
  "family": ["SN-050 verify the pushed bytes", "SN-061 post-merge verification at the pin", "SN-066 red before green", "SN-048 CI-trigger silence"],
  "evidence": ["#554 comment 5940389915", "#554 comment 5940612880", "#554 comment 5940155081", "#554 comment 5940185514"]
}
```

---

## 🔗 HOW IT CONNECTS

- **EXTENDS SN-050** (verify the pushed bytes, not the pre-commit bytes): the same verdict-voiding, one level deeper — not branch-vs-branch, but commit-vs-commit.
- **EXTENDS SN-061** (post-merge verification at the pin): verdicts bind pins; a moved pin is a new claim.
- **COROLLARY OF SN-066** (red before green): the red was published (Coda 1's blocker) before any fix — that sequence is what made the smallest fix obvious.
- **FEEDS SN-051** (local-verification-as-gate): when the push path is CI-blind, the local battery at the post-sweep SHA is the gate.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** Defect proven (SyntaxError on fresh clone, origin established by Select-String and clean-at-SHA). The discipline rule is inferred from one instance + family support — durable, but a second independent instance would harden it.

## 🌍 APPLICABILITY

- **Applies to:** any bulk mechanical change (encoding sweeps, import rewrites, formatter passes, sed-class edits) before any green claim.
- **Does NOT apply to:** single-site hand edits already covered by per-SHA test runs — the point is the *sweep*, where confidence is borrowed from the diff size being "small."

## 🧬 SUCCESSOR EFFECT

Future Naya: after any sweep, run the detector and the suite at the new SHA, and name the SHA in the claim. If you catch yourself saying "tests passed" about a commit newer than the one you tested — stop, re-run, re-name.
