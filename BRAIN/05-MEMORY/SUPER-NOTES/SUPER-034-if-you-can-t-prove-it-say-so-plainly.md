# SUPER NOTE — If You Can't Prove It, Say So Plainly

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-034` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-034` |
| Human title | If You Can't Prove It, Say So Plainly |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 10 raw notes (full list below) |
| Cluster file | `cluster-04-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

A claim is only as good as its proof. A number the maker made up, work nobody else can see, or a check that never looked everywhere — none of that counts. Honest words are: proven, or not proven yet.

---

## 🩷 HUMAN NOTE

Again and again, 'done' turned out to be a story: a success count printed by the same program being tested, fixes that lived only on one person's machine, a safety check that quietly examined half the files and passed the rest unseen. The discipline is plain. Test against the real, live thing, not a copy of it. A checker must prove it can catch a real failure, and must say how much it actually covered. Work that exists only locally doesn't exist for the team. And when the final proof needs permission you don't have, ship everything ready and label it honestly: built, not yet proven.

---

## 🟣 CHILD NOTE

If you say 'I cleaned my room,' someone should be able to look and see it's true. You can't just say the words. And if your flashlight only shines on half the room, you have to say 'I only checked half.' If you couldn't check at all, you say 'not checked yet' — you never pretend.

---

## 👵 GRANDMA NOTE

It's the difference between a neighbor who says the fence is fixed and one who walks you over and shows you. This team learned to show, not tell — and when they truly can't show yet, they say so in plain words instead of dressing it up. That honesty is worth more than a confident story.

---

## 🤖 NAYA NOTE

Naya never accepts a producer's own string, count, or summary as evidence — she verifies against live bytes and independent reads. Her verifiers always carry a load-bearing negative control: a check that cannot fail proves nothing. She declares coverage before any verdict, treats local-only work as unreviewable, and restores what can be verified while plainly marking what cannot. Where a protected boundary blocks the last proof step, she ships the executable packet and the honest label.

---

## WHAT IT MEANS

False confidence is more expensive than admitted ignorance, because everyone downstream builds on it. A system that labels its own certainty honestly — proven here, unseen there, unproven at the boundary — lets people spend effort exactly where doubt actually lives, instead of re-checking what is solid or, worse, trusting what was never checked at all.

---

## WHAT'S IN IT FOR YOU

When this team says something works, you can lean on it — and when it might not, they tell you before you lean. You stop wasting time double-checking honest work, and you stop being surprised by work that was only ever a confident story.

---

## HOW IT APPLIES

Ask every claim: where is the proof, and who else can see it? Make every checker catch a planted failure before trusting its passes. Write down what a check covered before quoting its result. Push work where the team can review it. And use the honest labels out loud: done and proven, or built and not yet proven.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0272 — Building Fresh, Not on a False Memory — Verify the Asset, Record the Absence [audit: MISSING → restored in full]

Before building on a remembered asset, search for it; if it cannot be found, record the absence as UNKNOWN in the spec rather than guessing, and design fresh around the gap. In the source case Naya 2 searched the full repo and workspace for the remembered voice assets — a `NayaVoice/` directory and `voices/naya_reference.wav` — and found nothing, so the spec recorded: "the exact existing voice asset/model is currently UNKNOWN and must be recovered/verified rather than guessed". The pipeline was then built fresh — `IB text → Chatterbox → cached audio → browser plays` — gated only on Shawn supplying the true voice reference (`voices/naya_reference.wav` remains the gating item, out of source control per Shawn's spec §7: no private voice assets in the repo). Memory of an asset is not an asset.

### SN-0281 — Proof Gating — Never Let `if: always()` Manufacture Secondary Failures [audit: MISSING → restored in full]

Downstream proof jobs must never use `if: always()` after a failed prerequisite — it overrides normal `needs` skip semantics and manufactures misleading secondary failures out of one honest block. In the source case run `37231269905` failed closed correctly at source-integrity, but three downstream proof jobs — `independent-connect-verification`, `cold-successor`, and `cold-successor-verification` — used job-level `if: always()`, ran after the prerequisite chain was already invalid, and produced secondary artifact failures (e.g. missing `cold-successor-receipt`), turning one honest BLOCK into several misleading FAILs. Preserve the skip chain so the terminal state reads as ONE honest BLOCK at the true root. The repair was red-state-first: the regression test was written and the expected 3 FAIL red state observed before the fix; after removing the job-level `always()` from the three jobs, the regression went 3/3 PASS. Standing rule: no job-level `if: always()` on downstream proof jobs.

### SN-0417 — REGISTRY_RUNTIME_CONTENT_DRIFT — a Registry-Hash Hit Must Never Be Accepted as Reusable Until the Live Runtime Body Is Independently Content-Hash Verified [audit: PARTIAL → lost element restored]

The named drift rule: an exact-hash registry hit must never be accepted as reusable until the live runtime body is independently content-hash verified — registry metadata is a claim, not proof. In verify-only mode, fail closed with the named class `REGISTRY_RUNTIME_CONTENT_DRIFT`. In governed write mode, reconcile through the existing supersession path rather than silently reusing stale runtime content, preserving old lineage/provenance and never overwriting history. Add regression coverage for the combination registry-hash/current + runtime-body/stale.

### SN-0551 — An Ownership Move Earns Its Trust Mechanically: Diff-Fuzz the Seam, Don't Assert It [audit: MISSING → restored in full]

Moving code across an ownership boundary must be proven mechanically at the seam, not asserted: a diff-fuzz with a named comparison count, plus a behaviour matrix with named coverage, and the battery must be run at the new location — anything the move exposes becomes its own repair PR. In the source case the Graph V2 selector moved to the CONNECT-owned module `supabase/functions/_shared/connect_selector.ts`: a 6000-comparison diff-fuzz proved zero behaviour change, plus a 9/9 behaviour matrix, plus a full battery green except pre-existing base failures. The move exposed a test-gate seam — the new `_shared/` directory trips the `edge_execution_coverage` gate — which got its own repair PR (#1739) instead of being merged through or self-repaired onto main. A moved module inherits new gates; the old location's greenness proves nothing about the new one.

---

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20261004-sn0302-producer-computed-string-is-not-evidence`
- `IB-SMART-NOTE-20261004-sn0292-verifier-without-negative-control`
- `IB-SMART-NOTE-20261004-sn0286-restore-verifiable-mark-unverifiable`
- `IB-SMART-NOTE-20261004-sn0272-building-fresh-not-on-a-false-memory`
- `IB-SMART-NOTE-20261004-sn0316-local-until-pushed`
- `IB-SMART-NOTE-20261004-sn0234-implemented-not-proven-proof-packet-at-protected-boundary`
- `IB-SMART-NOTE-20261005-sn0376-gate-must-declare-coverage-before-verdict`
- `IB-SMART-NOTE-20261004-sn0281-proof-gating-no-if-always`
- `IB-SMART-NOTE-20261005-sn0417-registry-runtime-content-drift`
- `IB-SMART-NOTE-20260930-sn0551-ownership-move-diff-fuzz-seam-proof`
