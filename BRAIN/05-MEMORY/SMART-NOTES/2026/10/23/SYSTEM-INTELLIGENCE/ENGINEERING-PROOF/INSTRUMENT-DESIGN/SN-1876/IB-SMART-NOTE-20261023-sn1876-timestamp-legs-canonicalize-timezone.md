Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

t1423-lane3 (second-seat Stage-0 verdict on stall-cap-check.py, the first automatic violation detector, 2026-10-23 08:18 PDT) re-ran the detector against a 12-file planted set and re-derived its 104 flagged lines: 8/10 spot-checked pairs were real breaches (including 2 post-rule), but 2 were false positives from mixed filename conventions — "0238" vs "0238-PDT" paired as "0 min" when they are ~7h apart; "0503"/"0518" paired as "15 min" when ~6h44m apart. The machinery generates filenames in two conventions (bare HHMM from UTC-scheduled runs, HHMM-PDT from local-time runs); the detector's timestamp-drift leg computed deltas on the bare numeric stem, conflating conventions. Rule: any timestamp-leg check canonicalizes the timezone convention at parse time (read the TZ suffix; resolve bare stems against the run's documented convention) BEFORE computing deltas — AMBIGUOUS pairs report AMBIGUOUS, never VIOLATION. The sharpening fixes (F1: TZ-aware resolution, F2: AMBIGUOUS-not-VIOLATION on convention disagreement, F3: post-fix FP-rate re-enumeration) belong to the wiring brief, not the prose rule. This is the timestamp-leg instance of SN-0375 (a guard's model must mirror the machinery it guards) and the temporal sibling of SN-1713 (canonicalize identity comparisons — the path-prefix instance).

## 🩷 HUMAN NOTE

Shawn — the first automatic rule-break detector (the "stall cap" checker) was built, and its second-seat verdict found it mostly right: 8 of 10 flagged cases were real. But 2 were false alarms with the same root cause: the system names files with times in two different time zones (some in UTC, some in Pacific), and the checker was comparing raw numbers — "0238" next to "0238-PDT" looked like zero minutes apart when it's actually seven hours. The lesson: any checker that compares times must first figure out which time zone each stamp is in, and if it can't tell, it says "unclear" — never "violation." Three fixes were named for the wiring work; the rule itself is simple: sort out the time zones before doing the math.

## 🟣 CHILD NOTE

Imagine a game where you get points for finding clocks that disagree. Two clocks say "2:38" — but one clock is in London and the other is in Los Angeles, so they actually disagree by seven hours. If your checker just reads the numbers, it says "same time!" and misses the disagreement — or pairs two clocks and cries "wrong!" when they're fine. The fix: read the little label on each clock that says which city it's in FIRST, convert both to the same city, THEN compare. And if a clock has no label, say "I can't tell," not "it's wrong."

## 🔵 GRANDMA NOTE

It's like comparing meeting notes from two people — one writes times in her local time, the other in London time. If you just compare the numbers, 2:38 and 2:38 look identical when they're really seven hours apart, and you'd flag meetings that never conflicted. The fix is simple and boring: check which time zone each note uses before you compare, and if you can't tell, mark it "unclear" rather than raising an alarm. Noisy alarms teach everyone to ignore the checker — which defeats the whole point of having one.

## 🟠 NAYA NOTE

A timestamp-leg detector has two stages: pairing (which stamps belong together) and delta (how far apart). The false positives lived entirely in the pairing stage: the bare numeric stem "0238" is not an instant — it is an instant-under-a-convention, and the pairing code treated it as an instant. This is SN-0375's blind-spot class ("documented known-blind-spots must be modeled, not warned about") wearing SN-1713's canonicalization shape: identity comparisons canonicalize both sides, and timestamps are identities in time. The conservative default matters asymmetrically: a false VIOLATION erodes trust in the detector (every FP is a tax on every future flag), while AMBIGUOUS is honest and cheap. So the rule is three lines: canonicalize convention at parse time; compute deltas only on canonicalized stamps; on disagreement, report AMBIGUOUS. The F1–F3 sharpening (TZ-aware resolution, AMBIGUOUS-not-VIOLATION, FP-rate re-enumeration) is the instrument's wiring work — the prose rule stays convention-first.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1876-timestamp-legs-canonicalize-timezone",
  "lesson": "Any timestamp-leg check canonicalizes the timezone convention at parse time before computing deltas. t1423-lane3 (second-seat Stage-0 verdict on stall-cap-check.py, 2026-10-23 08:18 PDT) re-ran the detector's live-dir pass and re-derived its 104 flagged lines: 8/10 ctime spot-checked pairs were real breaches (incl. 2 post-rule), but 2 were false positives from mixed filename conventions — '0238' vs '0238-PDT' paired as '0 min' when ~7h apart; '0503'/'0518' paired as '15 min' when ~6h44m apart. The machinery generates filenames in two conventions (bare HHMM from UTC-scheduled runs, HHMM-PDT from local-time runs); the detector's pairing logic computed deltas on the bare numeric stem, conflating conventions. Rule: read the TZ suffix, resolve bare stems against the run's documented convention, compute deltas only on canonicalized stamps; on convention disagreement report AMBIGUOUS, never VIOLATION. The sharpening fixes F1 (TZ-aware resolution), F2 (AMBIGUOUS-not-VIOLATION on ctime disagreement), F3 (post-fix FP-rate re-enumeration) belong to the wiring brief, not the prose rule. This is the timestamp-leg instance of SN-0375 (a guard's model must mirror the machinery it guards) and the temporal sibling of SN-1713 (canonicalize identity comparisons).",
  "applies_when": ["detector", "violation", "instrument-design", "timestamp-leg", "measurement", "timestamp-delta", "failure:false-positive", "convention-mix", "wiring"],
  "enforcement": "Every timestamp-leg detector carries a planted-set self-test that includes cross-convention filename pairs (bare-UTC-stem vs PDT-suffixed, both orders) before wiring; convention-class FPs fail the self-test and block the wiring brief. For stall-cap-check.py specifically: the wiring brief must carry F1–F3 from the t1423 receipt (TZ-aware resolution, AMBIGUOUS-not-VIOLATION on ctime disagreement, post-fix FP-rate re-enumeration) and may not land until the re-enumerated FP rate is on the record. Acceptance test: the 12-file planted set from t1423 plus a mixed-convention pair set must yield zero convention-class FPs.",
  "evidence": [
    "memory log 2026-10-23 (lane-executor 08:18 PDT): t1423-lane3 claimed via claim-brief.py; detector SHA matched filing pin (e6d7653f…9ef); builder's fixture reproduced; own 12-file planted set + edges all behave; live-dir re-run re-derived 104 flagged lines; ctime spot-check of 10 flagged pairs: 8 real breaches (incl. 2 post-rule, cross-prefix and date-rollover working) + 2 proven false positives from mixed UTC/PDT filename conventions (0238/0238-PDT '0 min' = ~7h apart; 0503/0518 '15 min' = ~6h44m); named SHARPEN fixes F1–F3 for the wiring brief",
    "hidden_files/twelve-lane-receipts/t1423-lane3.md; verdict CANDIDATE-SHARPEN (scored 9.5 2026-10-23 08:30 PDT)",
    "Cousins: SN-0375 (guard's model must mirror the machinery — this is the timestamp-convention instance), SN-1713 (canonicalize identity comparisons — the path-prefix instance; this is the timestamp instance)",
    "Falsifier: if all files under check carry explicit TZ suffixes or a single documented convention, the canonicalization step is vacuous — the rule fires only when mixed conventions are observed; a detector with no timestamp leg is out of scope"
  ]
}
```
