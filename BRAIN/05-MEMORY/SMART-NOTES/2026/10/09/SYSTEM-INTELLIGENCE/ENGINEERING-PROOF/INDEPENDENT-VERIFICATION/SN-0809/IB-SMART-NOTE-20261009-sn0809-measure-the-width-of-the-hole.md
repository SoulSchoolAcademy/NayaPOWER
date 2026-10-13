# Measure the Width of the Hole Before Fixing — the Finder's One Is Rarely the Full Family

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0809-measure-the-width-of-the-hole
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comment 6086983423 (2026-10-09).
**Provenance:** #1354 6086983423 (STEWARD UPDATE — batch-4 fix pass complete at honest 9.0, 2026-10-09T18:35:49Z) — LESSON line from the fixer/steward report. Related: SN-0726 (measurement boundary), SN-0698 (recompute the statistic, not the summary).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The re-validator found one open evasion in batch-4's falsification check — underscores swapped for spaces to sneak a copy past. Before fixing, the fixer measured how wide the hole actually was: five open evasions, not one. Even a "case-only" rename written with spaces walked through, because the checker was erasing punctuation instead of treating all separators the same — and the original battery had never tested separator relabels at all. The fix folded every separator into one space: 5/8 open before, 8/8 closed after. Same discipline on hole 2 (chopped SHA fingerprints): the digit-requirement was the measurement that separated machine exhaust from English hex-words ("beef"/"face" pass, chopped SHAs fail), and the honest bound was written down, not hidden (all-letter hex words like "dead beef" pass by design). The fixer's own lesson: when a probe finds a hole, measure how WIDE it is before fixing — the fix that closes the measured width is the one you can trust.

## 🩷 HUMAN NOTE

Shawn — our inspector found one open door in the batch-4 checks, and before we fixed it we asked: is this one door, or a whole row of them? It was a row of five. The checker's cleaning routine was erasing punctuation, so five different tricks — including one our test battery had never even tried — all walked through. We fixed the whole row, not just the one door the inspector named, and re-tested everything: eight out of eight closed. The rule from now on: when a probe finds a hole, the first job is measuring how wide it is. A finding is a direction, not a measurement.

## 👶 CHILD NOTE

Imagine the fence inspector finds one broken board. Before you fix it, you walk the whole fence — and you find five broken boards! If you'd only fixed the one, the dog would still get out through the other four. Always walk the whole fence first. The inspector showed you where to look; you measure how big the problem really is.

## 👵 GRANDMA NOTE

Sweetie, it's like the doctor who finds one leak under the sink and doesn't just patch that spot — he checks the whole pipe, because one leak usually means the whole stretch is tired. We found one and fixed five, and then we checked the whole house. The fix you can trust is the one that covers what you measured, not just what you were told.

## 🤖 NAYA NOTE

When a probe, re-validator, or inspector hands you a hole:

1. **Treat the finding as a direction, not a measurement.** The finder's description is almost never the full extent — re-probe the whole family yourself before touching code.
2. **Vary the attack surface, not just the reported attack.** The original battery never tested separator relabels at all — the finder's probe set defined the boundary of what was known, and the hole lived exactly outside it. Probe the dimensions the battery assumed away (separators, case, whitespace, relabels).
3. **Fix the measured width, one principled change if possible.** Folding all separators into one space closed five evasions with one regex change — and the fix made the code match its own docstring, which is how you know it's the right fix.
4. **Tune to a measurement, then document the honest bound.** The digit requirement is what separates chopped SHAs from English hex-words — a measured distinction, not a guess. Where the bound genuinely ends ("dead beef" all-letter words pass), write it down as a bound, not a hidden gap. A documented limit is a design decision; an undocumented one is a surprise.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0809",
  "class": "ENGINEERING-PROOF",
  "subcategory": "INDEPENDENT-VERIFICATION",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "When a probe finds a hole, measure how WIDE it is before fixing: re-probe the full family yourself (especially the dimensions the existing battery assumed away), fix the measured width with the most principled change, and document the honest bound as a design decision rather than a hidden gap.",
  "worked_example": {
    "finding": "1 open evasion (underscore<->space relabel in falsification_first._norm)",
    "measured_width": "5/8 evasions OPEN, including 'case-only' rename written with spaces — the original battery never tested separator relabels",
    "fix": "re.sub(r'[^a-z0-9]+', ' ', ...) folds all separators to one space; code now matches its own docstring; 8/8 CLOSED after",
    "hole_2_tuning": "reassembled_hex_hits: runs of 2-6 char pure-hex tokens reassembling to 7+ chars with >=1 digit AND >=1 hex letter; chopped SHA FAILs, 'beef'/'face' prose PASSes",
    "honest_bound": "all-letter hex words ('dead beef') pass by design — documented as a bound",
    "board_comment": "#1354 6086983423"
  },
  "related": ["SN-0726", "SN-0698"]
}
```
