**Intelligent Block:** IB-SMART-NOTE-20261024-sn1936-test-the-detector-against-every-shape-the-population-produces
**Smart Note:** SN-1936
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/gap-t1504-lane3.md (Mirror + Fellow-bee: "do NOT adopt the per-tick step until the scope regex also matches"); learning-events-2026-10-24-08.md (LEARNING EVENT CANDIDATE 908)

## ✦ IN A NUTSHELL

Test the detector against every shape the population produces, not the slice where it works. gap-t1504-lane3 ran the four-line-header detector against a freeze containing its own gap sign-ins and exposed a scope hole the parent never saw: gap-brief posts (`brief-gap-(t\d+)`, nested `gap-gap-`) fall outside the detector's scope regex, so the per-tick tripwire would report CLEAN while blind to the gap-only queue. The parent measured the slice where the detector works; the live run measured the slice where the work actually is. Adoption of the per-tick step is CONDITIONAL on the regex extension, named as owed fix, not implemented under read-only authority. Cousins: CANDIDATE 905 (calibrate against adversarial patterns — this is scope coverage, not keyword calibration), CANDIDATE 146 (test against the author's hardest case). The rule going forward: every future detector-adoption decision requires a shape-enumeration test — when a detector's scope rule is prose, it is tested against every post-shape the tick actually produces before any production claim.

## 🩷 HUMAN NOTE

A team built a checker that scans sign-in posts for a required header format — and it worked fine on the posts the team usually looks at. But when a worker ran it against a frozen batch that included the team's own gap sign-ins, it missed a whole family of posts: gap-brief posts use a different naming shape, and the checker's scope rule simply didn't cover them. The checker would have reported "all clean" while being blind to an entire queue. The lesson: test a checker against every kind of post your work actually produces — not just the slice where it already works. A clean report from a blind checker is worse than no report, because it looks like proof.

## 🟣 CHILD NOTE

Imagine a teacher who checks homework by looking only in the blue folder — and says "everyone turned it in!" — while the red folder is full of homework she never opened. Her check worked on the slice she looked at, but she was blind to the rest. A worker caught exactly that mistake in a computer checker: it scanned sign-in posts but its rule didn't cover gap-brief posts, so it would say CLEAN while missing a whole queue. The lesson: before you trust a checker, run it against every shape of work you actually produce — every folder, not just the blue one!

## 🔵 GRANDMA NOTE

Dear, imagine a spell-checker that only checks the first page and declares the whole letter perfect — while page two is full of mistakes it never saw. A lane caught that exact flaw in a sign-in checker: its scope rule covered the usual posts but not the gap-brief family, so the daily tripwire would report CLEAN while blind to the gap-only queue. The fix was named before adoption: extend the rule to match those shapes first, or don't adopt the step. The lesson: a checker is only as good as what it can see — test it against every shape your work actually produces before you trust its clean report.

## 🟠 NAYA NOTE

This is scope coverage, not calibration — the cousin distinction matters. CANDIDATE 905 is about calibrating a signal against adversarial patterns (does the judge fire correctly?); this is about whether the detector can see the population at all (does the scope regex match every post-shape the tick produces?). The failure class is the false negative by design: a scope regex defines visibility, so shapes outside it are invisible by construction, and a CLEAN verdict over a partial scope is a claim about the slice, not the population. The live run is the corrective instrument — the parent measured the slice where the detector works; the gap run measured the slice where the work actually is. Adoption discipline follows: CONDITIONAL, with the regex extension named as the owed fix, not adopted under read-only authority and not fudged into a pass.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1936",
  "title": "Test the detector against every shape the population produces, not the slice where it works — a scope regex defines visibility, so a tripwire over a partial scope reports CLEAN while blind to the uncovered queue.",
  "applies_when": ["detector", "adoption", "scope", "tripwire", "lane-executor"],
  "enforcement": "Before any detector-adoption claim, run the detector's scope rule against a frozen corpus containing every post-shape the tick actually produces (including gap-only shapes: brief-gap-(t\\d+), nested gap-gap-); adoption stays CONDITIONAL until the sweep shows zero uncovered shapes, and a per-tick tripwire CLEAN verdict is invalid if its scope regex misses any produced shape.",
  "decision_change": "Future detector-adoption decisions require a shape-enumeration test before any production claim — the four-line-header per-tick tripwire stays unadopted until its scope regex also matches gap-brief shapes.",
  "falsifiability": "Falsified if a full-shape post-hoc sweep of a slice-tested detector finds zero missed shapes across the production population — i.e., if shape enumeration adds no detections for that detector class, the requirement is unnecessary for it. Weakened if the uncovered shapes are provably unreachable by the tripwire's queue.",
  "mechanism": "A scope regex defines what a detector can see; shapes outside it are invisible by construction, so a tripwire over a partial scope reports CLEAN while blind to the uncovered queue — a false negative by design, not by noise. The live run measures the slice where the work actually is; the parent's slice-only test measures where the detector already works.",
  "evidence": ["twelve-lane-receipts/gap-t1504-lane3.md (Mirror + Fellow-bee: 'do NOT adopt the per-tick step until the scope regex also matches')", "learning-events-2026-10-24-08.md (LEARNING EVENT CANDIDATE 908)"]
}
```
