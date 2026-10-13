# A Scan-Built Rate Is a Floor, Not a Rate — Keyword Scans Undercount Falsification

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1209-a-scan-built-rate-is-a-floor-not-a-rate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** lesson-broadcast.md [t0662] Naya Heart (2026-10-13, mirror t0651 78-row hand-judgment, 8.5/10); twelve-lane-receipts t0651-lane11; learning-events-2026-10-13-11.md candidate 155

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The number you report is only as good as the instrument that built it — and a keyword scan is an instrument with a known blind spot. t0645's 32.4% (55/170) falsification figure was built by keyword-scanning 78 rows, not hand-reading them. t0651-lane11 hand-read all 78 and found 28 more falsification/retraction events the scan could not see — brief-premise falsifications, adversarial bypass finds, self-falsified specs and pre-regs, probe-verdict falsifications: 83/170 = 48.8% on the fully hand-read frame, and the t0645 32.4% figure is SUPERSEDED as a rate (it survives only as a floor). The standing rule: **a scan-built rate is a floor, not a rate** — report it as "at or above the band," never as "the rate," and never let an enforcement gate consume a floor as a rate (the t0645 figure was barred from the FP-001 gate for exactly this reason). Keyword scans systematically undercount the thing you care about because the events live in prose the scan wasn't written to see. The same tick held the honest-qualification discipline: "falsification reporting is at or above the baseline band on every measured window since t1052" — not "48.8 > 45.2 therefore rising," because the two numbers come from different windows and the comparison is invalid.

## 🩷 HUMAN NOTE

Shawn — a measurement-honesty lesson from the audit lane: they'd been reporting a 32.4% falsification rate, but that number came from a keyword scan, not from reading the rows. When the lane hand-read all 78 rows the scan had judged, they found 28 real events the scan couldn't see — the real rate on the fully-read set is 48.8%. Two rules fell out of it: first, a number built by a scan is a floor, never a rate — you say "at or above," never "it is," and you never let a gate act on a floor as if it were exact. Second, don't compare rates across different measurement windows — "48.8 beats 45.2" is meaningless when the frames differ; the honest claim is "at or above the band on every measured window." Owed: a second seat spot-checks at least 10 of the 28 newly-found rows before anyone else consumes the 48.8% figure.

## 🟣 CHILD NOTE

Imagine counting how many kids in school wear glasses by searching photos for the word "glasses" in the captions. You'd miss everyone whose photo caption doesn't say the word — your count is too low, guaranteed. When you actually walk the hallways and look, you find 28 more kids. The new rule: a count made by searching words is a minimum ("at least this many"), never the real number — and you don't compare it to a count made a different way and say "it went up," because you measured two different things.

## 👵 GRANDMA NOTE

A hospital counted medication errors by searching incident reports for the word "error." The number looked low and reassuring. Then a nurse read every report by hand and found 28 more — near-misses, corrected orders, caught-before-administering events the keyword never matched. The count was a floor, not the rate. The new policy: a searched number is reported as "at least this many," and nobody compares this month's searched number to last month's hand-read number and declares a trend — different rulers, different measurements.

## 🧠 NAYA NOTE

Cold successor: whenever you see a rate or count, ask what instrument built it before you use it. If it was built by a keyword/scan pass over prose, treat it as a FLOOR: report "at or above X," gate nothing on it as an exact value, and mark the unjudged rows UNJUDGEABLE — never force a verdict the instrument couldn't see. The events you care about (falsifications, retractions, premise kills) live in prose the scan wasn't written for; hand-reading is the calibration pass that converts a floor into a rate. Second: rates are only comparable inside the same measurement frame — never claim a trend across different windows ("48.8 > 45.2 therefore rising" is invalid when the frames differ); the honest form is "at or above the baseline band on every measured window." Before the FP-001 gate consumes a hand-judged rate, a second seat spot-checks ≥10 of the newly-found rows.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1209",
  "title": "A Scan-Built Rate Is a Floor, Not a Rate — Keyword Scans Undercount Falsification",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "EVIDENCE-DISCIPLINE"],
  "cousins": ["SN-1080", "SN-1181", "SN-0648"],
  "evidence": {
    "lesson": "lesson-broadcast.md [t0662] Naya Heart — mirror, t0651 78-row hand-judgment, scorecard 8.5/10, 2026-10-13",
    "receipt": "twelve-lane-receipts/t0651-lane11 — 78 keyword-scanned rows hand-read; 28 more falsification/retraction events found; 55/170=32.4% floor SUPERSEDED by 83/170=48.8% on the fully hand-read frame",
    "event_classes_found": ["brief-premise falsifications", "adversarial bypass finds", "self-falsified specs/pre-regs", "probe-verdict falsifications"],
    "qualification_discipline": "'falsification reporting is at or above the baseline band on every measured window since t1052' — not '48.8 > 45.2 therefore rising' (different windows)",
    "learning_review": "learning-events-2026-10-13-11.md candidate 155",
    "owed": "second-seat spot-check of >=10 of the 28 TRUE rows before the FP-001 gate consumes the 48.8% rate; t0557-lane11 9 UNJUDGEABLE rows still commissioned to a different seat"
  },
  "rule": "a scan-built rate is a floor, not a rate: report 'at or above', never gate on it as exact, and compare rates only within the same measurement frame",
  "change": "t0645 32.4% barred as a rate (floor only); 48.8% is the hand-judged rate pending second-seat spot-check"
}
```

