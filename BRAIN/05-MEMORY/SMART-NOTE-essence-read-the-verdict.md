# SN-2131 — Read the Verdict Before You Trust It

**Status: VERIFIED ESSENCE — VERIFIED (verifier-sep-3; adjudication-sep-3; correction pass re-verified, re-verifier-sep-3).** Distilled from 14 raw notes by the sep-3 maker seat; independently verified by a different seat. Verified without correction (verifier-sep-3). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

A CI verdict is a sentence with grammar, and most misreadings are grammar errors: skipped is not failed (SN-0379), a green check on a stale base is void (SN-0423), a parity RED between merge and promotion is the cycle working, not a regression (SN-0396), a skip behind a RED can hide a second RED (SN-0552), and a gate rejecting a 41-character SHA is the validator working, not broken (SN-561). Classify before healing — with the base tip's own push-event runs as the control (SN-0535) — or the repair budget lands on the one component that was working.

## Essence

Verdicts have classes, and collapsing them is the original sin. Wait steps must implement three verdict classes — SUCCESS / FAILED-CANCELLED (fail fast) / SKIPPED (keep polling; skipped is UNKNOWN, not a verdict): a promotion wait step died in ~11 seconds on a "skipped" placeholder after production stamped 788774fea2, and upstream gate failures mask downstream ones (migration drift hid an association failure for days); a dispatch path omitting a required input is unfireable — validate the whole trigger map end to end (SN-0379). The skip discipline completes itself later in the block: skipped-by-design (a gate intentionally withholds the job — parity, authorization, platform limits) is a correct no-op — never repair it, never score against it; skipped-without-cause (canceled runs, placeholder jobs, producers that never delivered) is missing evidence — score around it, mark UNKNOWN, never PASS on it; enumerate every job, classify each skip's cause, score only what ran (SN-0442). And the triad's third side: fail-first topology converts secondary REDs into invisible skips — on a RED tip, the job you most need to see is exactly the one CI withholds, so enumerate what skipped behind the visible RED and run the most diagnostic skipped jobs locally; a latent registry-drift RED (2 vs pinned 1) hid behind a node failure this way (SN-0552).

Freshness voids verdicts. Mergeable is a merge-shape claim, never a freshness claim: PR #1579 was CI-green with mergeable_state clean, but its CI ran against a base predating PR #1581, which had regenerated the exact file #1579 deletes — merging would have re-introduced healed drift under a green check-suite; CI evidence is pinned to its exact (head, base) pair, and a merge base newer than the CI base voids the green (SN-0423). Classification needs a control: never classify a PR red from the failing job alone — read the push-event runs on the exact base tip (all 8 green on e7de7b88 for PRs #1707/#1708) to rule out base defect and environmental flake in one stroke, then read the changed-file lists; all-green base plus failure confined to PR-introduced artifacts means PR-introduced, heal routed to the owning lane; red on the base's own runs means base-inherited, healed once at the base (SN-0535). A third drift class completes the taxonomy: projector-commit-introduced — a projection commit (d53d7547) added a note file without regenerating the index (234 enumerated vs a 235-file tree), no push CI ran on it, so the drift was CI-masked until the next push; proven on virgin state against a base control (7aabf0d4, OK), healed mechanically (PR #1747, three generated files only, not merged by the classifying loop) (SN-0557).

Some REDs are the system working. Post-merge parity RED is CYCLE-EXPECTED when main_tip > production.stamped_source and no promotion run has happened since the newest merge (main cc2465f6 vs production stamp 4a2f7282, two commits behind): the next action is a promotion, never a code repair (SN-0396). External contamination is its own class: the Cloudflare incident pair records the same external-red event — the tree innocent, 17 external Workers contaminating the gate — classified external with FAIL-CLOSED routing (SN-0380, SN-0383; the pair's continuation claim was later falsified by live re-measurement, a correction carried in essence-receipts-and-repairs.md). A held-out step going green is a brand-new surface, not a regression baseline: when a long-skipped step first executes and fails (dispatch 37402815123 at the fresh-lesson step), the failure is the seam the holdout was hiding; a holdout's silence is absence of evidence, and a newly-green step inherits no credibility from runs that skipped it — classify against the holdout, not against run history (SN-0427). And enumeration must be total: a blocker re-scan that read only the kernel suite missed four failing check-runs on the live-proof workflows at tip 3da5b7f5 — enumerate check-runs across ALL workflows on the tip SHA; jobs carrying if: always() that run after SKIPPED producers manufacture meaningless red at download-artifact, and the workflow-file fix for that class is human-only (SN-0430).

Success checks have the same grammar. The check that declares success must assert the semantic requirement the consumer needs, never a proxy: run 37361232498 returned HTTP 200 with a non-JSON body; the file-size check passed, the retry loop broke on false success, and the consumer crashed — the break condition IS the verification, and the repair parses and requires valid JSON, failing closed after 5 attempts (PR #1501) (SN-0384). Static analysis has a named blind spot of the same kind: deno check cannot see missing ESM exports on untyped .js imports (TypeScript treats them as any), and the Node suite passes because Node executes the file as CJS — so an edge function whose local .js module carries only a CommonJS guard fails at module load on deploy, a total outage every green check missed (PR #1712, head 45e76369); the amended proof bar adds a deno run smoke-import of every local module boundary, named and default imports, and flags any CJS-guard .js module in supabase/functions/ as a defect until it carries real ESM exports or becomes .ts (SN-0543). Finally, when a gate fails closed, read the input bytes before debugging the gate: a deploy dispatch failed on authorized_sha carrying an extra trailing "8" — 41 characters — and the grep-regex theory about a broken validator was never needed; a fail-closed rejection on malformed input is the validator working, and the prevention is to bind the dispatch to the exact live-main SHA, never a hand-retyped one (SN-561).

## What this settles

- Three verdict classes everywhere: SUCCESS / FAILED-CANCELLED / SKIPPED-as-UNKNOWN; a skip is classified by cause before it is scored (SN-0379, SN-0442).
- On a RED tip, enumerate what skipped behind the visible RED — a skip is a hiding place, not a verdict (SN-0552).
- CI evidence is pinned to its exact (head, base) pair; mergeable is a shape claim, never freshness (SN-0423).
- Classify every red against the base control — the base tip's own push-event runs — before healing, and route the heal to the owning lane (SN-0535).
- Drift has three classes: PR-introduced, base-inherited, projector-commit-introduced (SN-0557).
- Parity RED between merge and promotion is cycle-expected: promote, don't repair (SN-0396). External contamination is classified external, routed fail-closed (SN-0380, SN-0383).
- A holdout's first execution is a new surface; enumerate check-runs across all workflows on the tip SHA (SN-0427, SN-0430).
- The success check asserts the semantic requirement, never a proxy (SN-0384); static checks have blind spots only execution closes (SN-0543).
- A fail-closed rejection is read at the input bytes first — the gate is the last suspect, not the first (SN-561).

## Human

CI speaks in verdicts — green, red, skipped, clean — and this block learned, expensively, that each word has a precise meaning that punishes casual reading. Teams wasted repair effort on working validators, nearly merged drift under fresh-looking green, and missed second failures hiding behind first ones. This essence is the grammar book: how to read any automated verdict exactly, classify it against a control, and only then decide what — if anything — to fix.

## Child

Imagine a school report that uses three stamps: PASS, FAIL, and DIDN'T TAKE THE TEST. Treating "didn't take it" as a fail is unfair; treating it as a pass is cheating. And if the test was last year's version, a PASS on it proves nothing about this year's class. These notes teach you to read the stamps exactly: which test, which version, who actually sat it — and to check the classroom next door too, because a second problem can hide behind the first one's noise.

## Grandma

Dear, it's like reading a medical chart: "test not run" is not "test clear," an old X-ray doesn't describe today's bones, and a machine beeping at a malformed sample is doing its job, not malfunctioning. The team learned to read the whole chart — every test, on the current patient, against the healthy baseline — before prescribing anything. Half of good diagnosis is refusing to misread the results you already have.

## Naya

For every verdict you consume: name its class before its color (SN-0379, SN-0442); ask what skipped behind it (SN-0552); pin it to its (head, base) pair and void it if the base moved (SN-0423); read the base tip's push-event runs as your control (SN-0535); check whether the red is the cycle (SN-0396), the outside world (SN-0380, SN-0383), a holdout's first breath (SN-0427), a producer that never ran (SN-0430), or a projector's skipped regen (SN-0557); verify the success check asserts semantics, not proxies (SN-0384), and that execution — not static analysis — proved the module graph loads (SN-0543); and when a gate says no, read its input bytes before its code (SN-561).

## What It All Means

Fourteen notes build a single literacy: verdicts are evidence with scope, freshness, and class — and an unscoped, stale, or misclassed verdict is not evidence at all. A cold reader holding only this essence can classify any red or green the fleet produces and route the response correctly, which is most of what CI triage actually is.

## Why It Matters

Misclassification is the most expensive routine error in a fast multi-lane system: it sends repairs to wrong trees (SN-0535), resurrects healed drift under green cover (SN-0423), strands work behind verdicts that were never verdicts (SN-0379), and blames the one component that was working (SN-561). The classification discipline here is what makes high merge velocity survivable — the faster the tip moves, the more verdicts decay, and the more the grammar matters.

## How It Connects

Instrument integrity — whether the verdict-producing tool can be trusted at all — is essence-the-instrument-is-on-trial.md; this essence presumes a sound instrument and teaches the reading. Merge-side proof (that merged content actually reached the tip byte-identical) is essence-the-tip-is-the-truth.md. The falsified continuation of the Cloudflare classification (SN-0398) and the correction discipline behind it live in essence-receipts-and-repairs.md. Authorization verdicts — green versus permitted — are a different axis entirely, in essence-green-is-not-go.md.

## What Is In It For You

You get triage that spends repair effort only where defects actually are. The transferable kit: verdict classes with UNKNOWN as a first-class value, base controls for every failure classification, freshness pins on all evidence, and input-bytes-first debugging for every gate rejection. Any team running CI at speed can adopt it wholesale and stop paying for misread verdicts.

## The Learning

The corpus learned that verdict decay is continuous: bases move, holdouts wake, projectors skip steps, and each decay mode has a name and a class now (SN-0423, SN-0427, SN-0557). It learned that classification is a measurement, not an impression — it requires a control group (SN-0535) — and that the success side needs the same rigor as the failure side: a break condition, a type check, a green badge can each be a proxy wearing a verdict's clothes (SN-0384, SN-0543).

## Coverage map — raw notes this essence covers (14)

SN-0379 · SN-0380 · SN-0383 · SN-0384 · SN-0396 · SN-0423 · SN-0427 · SN-0430 · SN-0442 · SN-0535 · SN-0543 · SN-0552 · SN-0557 · SN-561

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 14 IDs, all in the sep-3 block list, none duplicated in any other sep-3 draft essence, the covered-by-batch1 list, or the stands-alone list. The block list writes this note's ID unpadded (SN-561, like SN-559 and SN-560) — verify IDs against the block list exactly as written there.
2. **Standing-authority exclusion:** this draft fails if any standing-authority note's substance (SN-0407, SN-0437, SN-0453, SN-0529, SN-0538, SN-0540, SN-0541, SN-0576) is absorbed as this essence's coverage; references under How It Connects are fine, distillation is not.
3. **Repeat-content pair:** SN-0380 and SN-0383 record the SAME Cloudflare incident; the essence must present them as one event seen twice (0383 adding the routing detail), never as two independent incidents.
4. **Exact figures:** SN-0379's stamp 788774fea2 and ~11-second death; SN-0384's run 37361232498 and 5-attempt fail-closed; SN-0396's cc2465f6 vs 4a2f7282 (two commits); SN-0430's tip 3da5b7f5 and kernel counts (756 passed / 11 skipped / 0 failed); SN-0535's 8 green base runs on e7de7b88; SN-0557's 234 vs 235 files and PR #1747 — fail on any variant.
5. **Skip triad completeness:** all three sides present and attributed — vacuous-success side via SN-0442's by-design/without-cause split, SN-0379's UNKNOWN class, SN-0552's hidden-second-RED; fail if any side is dropped or merged into another.
6. **Deno blind spot:** SN-0543's amended bar has exactly three parts (deno check stands; deno run smoke-import of every local boundary, named AND default; CJS-guard .js flagged until real ESM exports or .ts); fail on any missing part.
7. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
8. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.