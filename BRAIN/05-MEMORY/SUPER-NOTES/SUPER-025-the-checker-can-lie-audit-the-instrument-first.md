# SUPER NOTE — The Checker Can Lie — Audit the Instrument First

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-025` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-025` |
| Human title | The Checker Can Lie — Audit the Instrument First |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 10 raw notes (full list below) |
| Cluster file | `cluster-03-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

Sometimes the test is what is broken, not the thing being tested. A measuring tool working in the wrong place, with too little room, or reading the wrong thing will report failures that never happened.

---

## 🩷 HUMAN NOTE

A harness that blames the wrong party is worse than silence. Test rigs fail in their own ways: scratch space fills up and the error gets swallowed, a shallow copy of the code makes history-scanning tests fail, a stale merged view invents a failure that exists nowhere, a counter quietly counts a different set than the ledger it checks. Even a bare number is meaningless without its counting method — two honest people can measure the same drift and get different numbers because they counted differently.

---

## 🟣 CHILD NOTE

If your ruler is bent, everything you measure looks crooked. Before you say the toy is broken, check the ruler. And if someone gives you a number, ask: how did you count?

---

## 👵 GRANDMA NOTE

In my kitchen, if the scale says the flour weighs ten pounds, I check the scale before I blame the recipe. Tools wear out and get set up wrong. A good cook tests her measures — and says plainly how she counted.

---

## 🤖 NAYA NOTE

When a check fails in a way that does not reproduce, Naya suspects the instrument before the product: she checks where the harness keeps its scratch files, whether its errors were silenced, whether the checkout shape matches what the test assumes, and whether the tool version is the one the CI actually uses. She recomputes ledgers from the artifact itself and tests them fail-first, and she never reports a count without its counting method.

---

## WHAT IT MEANS

Every verdict is two claims: one about the world, one about the tool that measured it. Teams that forget the second claim chase ghosts — repairing healthy code while the real defect sits in the rig. Auditing the instrument first is what keeps failure signals worth believing.

---

## WHAT'S IN IT FOR YOU

You stop fixing things that are not broken. Failures become believable again, so real problems get attention fast instead of drowning in false alarms and arguments about whose measurement was right.

---

## HOW IT APPLIES

When a failure will not reproduce: check the harness's environment — disk, paths, checkout depth; unsilence its error output; confirm the tool and version match what CI uses; verify the checker actually enumerates everything it claims to cover; and restate every count with its method. Only then classify the product.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0246 — The Runner Echoes Source — Measure the Failing Line, Never Infer It [audit: MISSING → restored in full]

**Rule 1 — log echo is not runtime evidence.** A line of source text printed in a log proves nothing executed; the runner echoes unevaluated script source, and citing that echo as a measured outcome is inference masquerading as measurement. In the source case the script had died at line 49, twenty-two lines before the treatment dict was ever constructed, so the cited `treatment.source_intelligent_block_id` in the log payload never executed.

**Rule 2 — measure the failing line, never infer it.** Map the traceback against the workflow source programmatically; never infer which assert failed from proximity to a log payload, log colour, or payload shape. Measured in the source case: line 49 was `assert comprehension["understands_raw_source_separate"]` (the conformance gate) and line 71 was the behaviour assert, which was never reached.

**Rule 3 — the failing line number is positive evidence.** Failure at line N proves lines 1 to N-1 in the same script executed cleanly. Because execution failed at relative line 49, relative line 48 — `assert comprehension["exact_current_capture_retrieved"]` — passed, which independently proves the exact block was retrieved; CODA 3 counted heredoc-relative lines independently (opener at file line 388, body at 389) and confirmed relative lines 48/49/50.

### SN-097 — Fail Loud, Attribute First — A Harness That Blames the Wrong Party Is Worse Than Silence [audit: PARTIAL → lost element restored]

The lost fail-loud rule: a dead harness must abort with a named environment fatal and a distinct exit code, never emit per-case FAIL verdicts for cases it never ran. In the source repair, a dead scratch clone aborts with a named FATAL and exit 3 — an environment failure, distinct from any test verdict. A verdict for an un-run case is fabricated evidence, not a conservative report.

---

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn097-fail-loud-attribute-first`
- `IB-SMART-NOTE-20260930-sn0341-harness-scratch-off-tmpfs`
- `IB-SMART-NOTE-20260930-sn0428-shallow-checkout-instrument-defect`
- `IB-SMART-NOTE-20260930-sn0443-stale-merge-ref-fabricates-the-red`
- `IB-SMART-NOTE-20261004-sn0246-runner-echo-is-not-runtime`
- `IB-SMART-NOTE-20261006-sn0469-count-what-the-ledger-counts`
- `IB-SMART-NOTE-20260930-sn0165-drift-counts-carry-counting-method`
- `IB-SMART-NOTE-20261004-sn0294-coverage-is-part-of-conformance`
- `IB-SMART-NOTE-20260930-sn0212-recompute-ledger-from-artifact-fail-first`
- `IB-SMART-NOTE-20261006-sn0429-instrument-ci-uses`
