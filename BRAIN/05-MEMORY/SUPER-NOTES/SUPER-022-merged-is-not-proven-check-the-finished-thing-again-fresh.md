# SUPER NOTE — Merged Is Not Proven — Check the Finished Thing Again, Fresh

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-022` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-022` |
| Human title | Merged Is Not Proven — Check the Finished Thing Again, Fresh |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 8 raw notes (full list below) |
| Cluster file | `cluster-02-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

Something being accepted, combined, or announced is not the same as it being right. After anything lands, check the final thing itself, fresh, field by field — as if you'd never seen it before.

---

## 🩷 HUMAN NOTE

Merging rewrites things. The version you checked beforehand is not the version that ends up in the final pile — we proved real damage that way, including a protected document quietly losing required fields in a green, celebrated merge. The reliable pattern: after the merge, go to the final state and re-verify — that the merge is really in the history, that nothing drifted, that the decided details match field by field. And do it clean: a fresh copy, an independent pair of eyes, because the builder's own workspace and memory are exactly what can't be trusted.

---

## 🟣 CHILD NOTE

When two drawings get glued into one picture, check the glued picture — not the drawings from before. Glue can cover things up. And ask a friend to look too; you might miss what changed.

---

## 👵 GRANDMA NOTE

After the seamstress combines the pieces, dear, you try on the finished dress — you don't just admire the pattern pieces. Things shift in the joining. A fresh look at the finished thing catches what everyone assumed.

---

## 🤖 NAYA NOTE

Naya treats 'merged' as the start of verification, not the end. She proves the merge commit is truly in the final history, that the content survived the join unchanged, and that sequential merges are replayed with real merge machinery, since each join changes the base for the next. Verification happens in a clean room at the exact final version, and her relay checks the pins themselves — not the builder's conclusions.

---

## WHAT IT MEANS

Joins are where systems quietly lose things: history is rewritten, fields vanish, bases shift under later steps. Pre-join checks, however rigorous, describe ingredients, not the meal. Post-join verification at the real final state is the only proof that the thing everyone now relies on is the thing that was actually approved.

---

## WHAT'S IN IT FOR YOU

The version you depend on is the version that was checked. No more 'but it passed before we merged it,' and no silent losses discovered weeks later by someone downstream.

---

## HOW IT APPLIES

After any merge or release, re-verify the final artifact in place: confirm it's really in the main line, compare its content against what was approved, and check the details that matter individually. Use a fresh environment and, where you can, a verifier who didn't build it.

---

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-034 — "Cosmetic-Only" Is a Claim, Not a Fact — Verify with AST, and Gate Status Promotions with Honesty Tests [audit: MISSING → restored in full]

"Cosmetic-only" is a claim, not a fact. Prove a "no behavioral change" claim mechanically with AST strip-and-compare: strip docstrings and compare against the prior watermark — all 8 changed node source files were checked AST-IDENTICAL to the prior watermark, a mechanical strip-and-compare, not a diff-eyeball. A green suite alone does not distinguish docstring-only from behavior-preserving-refactor-only. Gate status promotions with honesty tests: a status promotion (e.g. `SCAFFOLD` → `CANDIDATE` in `manifest.json`) ships guard tests asserting the honesty banner travels with the status — the CANDIDATE status carries the NOT RATIFIED / NOT MERGED banner, enforced in code rather than promised in prose, so a future reader can never see the status without seeing the caveat.

### SN-0586 — IB-SMART-NOTE — SN-0586 — Verify the Instrument, Not the Receipt — and Never Repair on the Evidence Branch [audit: MISSING → restored in full]

Verify the instrument, not the receipt. Verification means independent re-execution: re-run the graders and re-extract the answers independently, and adjudicate the diffs against the answer text — never accept the shipped tallies as given. Re-running surfaced defects in the shipped graders themselves (5 under-scores and 2 over-scores from the explicit-choice extractor, an undocumented stats formula, and a receipt whose control split contradicted both the results file and the corrected tally); instrument defects are classified separately from claim defects, the data is corrected, and the claim is re-tested on corrected data. Repair graders on a new branch — re-grade there, re-issue the stats, correct the receipt — and never touch the evidence branches: evidence PR branches are frozen the moment they open. Evidence is immutable; graders are repairable; the two must never meet.

### SN-061 — Post-Merge Verification at the Pin — Branch-Green Is Not Merged-True; Prove Negatives Non-Vacuous [audit: PARTIAL → lost element restored]

A passing negative suite is meaningless until a mutant kill proves the negatives can fail — non-vacuous negatives. Neutralize the gate under test and confirm the negatives fail: neutralizing the `V2_TERMINAL_STATUS` gate makes N1/N2 FAIL. If a mutant does NOT fail a negative, trace it to root cause before discarding it — a mis-targeted mutant (here, on the block-level superseded gate, while N1's attack is an edge-level exclusion) is documented and discarded as a diagnostic, not buried as a failed check.

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn0447-merge-faithfulness-proof`
- `IB-SMART-NOTE-20260930-sn061-post-merge-verification-at-pin`
- `IB-SMART-NOTE-20260930-sn0542-sequential-merge-verification-real-merge-machinery`
- `IB-SMART-NOTE-20260930-sn058-adversarial-implementation-fidelity-audit`
- `IB-SMART-NOTE-20260930-sn0586-verify-the-instrument-not-the-receipt`
- `IB-SMART-NOTE-20260930-sn0446-relay-verification-contract`
- `IB-SMART-NOTE-20260930-sn028-clean-room-verification`
- `IB-SMART-NOTE-20260930-sn034-ast-verify-cosmetic-only`
