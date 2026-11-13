# SCORECARD — FACTORY LANE L7 — ONE FLOW: ONE MAP, ONE ORDER, ONE WALL

**Honest score: 9/10.** The convergence is done and proven; the point off is the phone-height variance this lane does not cure and the pre-existing (f) gate FAIL it is forbidden to fix. Both are named in the record, not hidden.

## Why it is not a 10

1. The phone-width document height still varies between loads (one after run at 360 measured 29,463 against ~18,730 in the other three). The structure is stable everywhere, but the height is not, and a 10/10 page does not wobble by ten thousand pixels between loads.
2. The design-contract gate still FAILS on (f) — 18 pre-existing look-alike findings. The count is identical before and after, so the convergence introduced nothing, but a 10/10 file passes its gate.
3. The timing test that would pin the height variance to the rebuild's timing could not run — the VM browsers died mid-round. The variance is documented, but the mechanism is a hypothesis, not a proof.
4. The `syncPreview` #step5 no-op is still in the file. It predates the lane and is out of scope, but a 10/10 file does not carry a dead query.
5. The local BASE copy drifts 114 B from main's BASE bytes, and this lane leaves that drift unresolved (rightly — the BASE is not the canonical file — but it is an untidy loose end for the archive step).

## 10 things you love

1. One step order, read back from the rendered file: step1–step6, kickers STEP 1–6, no duplicates, no skips.
2. The nav now tells the truth: six pills, six steps, and real mouse clicks land exactly on all six.
3. The copy tells the truth: "Six steps" because there are six — two cards and two aria-labels, all changed.
4. The wall appears once, 12/12, in both files and every run.
5. The nesting repair does real work: NAVIGATION + OVERLAYS are back inside the pieces library, the page ends at the contract, and the empty black void at the bottom of the before file is gone.
6. The diff is only 108 lines. Nothing else changed — no build logic, no processor, no contracts, no prices, no doors.
7. Two makers' probe runs agree exactly at 1440, to the pixel, in both files. That is the kind of agreement you can build on.
8. The cart works and the deterministic test proves it — the first probe's cart failure was flake, and the re-test says so plainly instead of hiding it.
9. The gate gives the identical verdict on before and after (18/18). Zero new findings is the cleanest proof a convergence can give.
10. Step 1 was settled first-hand from main's tree, not assumed: the FLOW file's blob on main matches the local starting bytes exactly.

## 10 things you don't love

1. The phone-height variance (see "why not a 10" #1). It is pre-existing, but it is still there.
2. Gate (f) FAIL — 18 findings, all pre-existing, all out of scope, all still red.
3. The timing test never ran. The variance has a hypothesis (rebuild timing) but no proof.
4. The `syncPreview` #step5 no-op survives the convergence untouched.
5. The CREATE pill lights the QUESTIONS pill in the scroll-spy. Small, pre-existing, and wrong-looking.
6. The H1 is cut at the fold at 390 (pre-existing A-34). A stranger's first phone view is a clipped headline.
7. The local BASE copy drifts from main's BASE bytes and nobody in this lane resolves it.
8. The before file's 390 heights (16,867 / 21,579 / 18,610) show the variance predates the lane — which is good for the lane and bad for the page.
9. The VM browsers died twice in one round (17:32Z Nov 12, then ~01:43Z tonight). Every probe run is a race against the next outage.
10. The record's proof leans on probe scripts the interrupted maker wrote; this maker re-ran them and wrote one more, but did not rebuild the harness from scratch — so a harness bug would be inherited, not caught.

## 10 things to make it 10x better

1. Fix the foot-of-page rails rebuild so the pieces-section height is deterministic at every width (A-24).
2. Put the page's own button classes (`steppill`, `inbox-mic`, `tview`, `primo theme-gold`) on the gate's harvest allowlist with their sources, or rename them to harvested parts — and clear gate (f).
3. Run the timing test (`timingtest.py`, kept in the probe dir) when the browsers are back, and name the rebuild's mechanism with evidence.
4. Fix the `syncPreview` #step5 query to point at step4, where the template grid lives.
5. Fix the scroll-spy band so CREATE lights CREATE.
6. Fix the H1 fold cut at 390 (A-34).
7. Re-read main's BASE bytes first-hand and reconcile the local BASE copy before the archive step.
8. Rebuild the probe harness once, from scratch, so the next lane trusts its own measurements instead of inheriting them.
9. Add a railblock-count assertion to the standard probe (the 11-vs-13 flip-flop is the cheapest early warning for the nesting class of bug).
10. Make the VM browser flake visible on the floor board (it has now died twice in 8 hours; a seat that needs a browser should know before it starts, not after its test fails).

## 10 solutions to apply right now

1. **File the branch now** (this round): converged file + record + scorecard, read back byte-for-byte. Done in the filing step.
2. **Name the phone variance in the record** with its table, so no later seat mistakes it for a regression. Done.
3. **Keep `timingtest.py` in the probe dir** with its purpose written in the record, so the A-24 lane runs it first. Done.
4. **Keep the before-file byte-identical** in the probe dir as the permanent before/after anchor. Done.
5. **Write the gate verdicts into the record item by item**, with the (f) count 18/18, so the checker does not have to re-run the gate to trust it. Done.
6. **Name the BASE drift (114 B)** in the record so the archive lane re-reads main first. Done.
7. **Do not touch the rebuild, the guard, or the button classes in this lane.** The scope line holds; the follow-ons are named, not smuggled in.
8. **Report the browser deaths to the captain** in the DONE report, so the floor knows the probe window is flaky tonight.
9. **Hand the A-24 lane the variance table + the railblock counts** as its starting evidence, not a fresh investigation.
10. **Score honestly at 9, not 10.** The point off is the work left, and pretending otherwise would be the claim without proof this lane refuses to make.

## The honest score

**9/10.** One Factory file, converged, proven by render at three widths, with the nav, the wall, the copy, and the specimens all telling the truth. The point off is real work left for later lanes — the phone-height variance, gate (f), and the dead `syncPreview` query — and this scorecard names all of it rather than rounding it away.
