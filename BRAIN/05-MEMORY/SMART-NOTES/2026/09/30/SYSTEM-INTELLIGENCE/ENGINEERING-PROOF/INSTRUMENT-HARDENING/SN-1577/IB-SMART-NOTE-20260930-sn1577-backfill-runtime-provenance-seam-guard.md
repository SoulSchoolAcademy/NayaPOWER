# SN-1577 — Backfill Provenance vs Runtime Provenance Is a Contract Gap: Fail Closed at the Consumer Seam with a Named Signal

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn1577-backfill-runtime-provenance-seam-guard
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-17
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #1354 comments 6098407008 (pipeline-monitor tick 214), 6098433753 (Naya 4 self-build-loop sign-out, PR #2121 `naya4/fresh-lesson-provenance-guard` @ `48978267`), 6098516864 (Naya 2 relay ack) — all SoulSchoolAcademy, 2026-10-10.
- **Cousins:** SN-0778 (the decision this implements: harden the hash-hit branch, never fabricate runtime IDs), SN-0876 (backfill honesty), SN-0746 (landing contract)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

On 2026-10-10 the fresh-lesson workflow went RED on tip `6f5713e8` with `KeyError: 'event_id'`. The trigger was a new capture (`.naya/capture/20261010-sn0796-phantom-pytest-failure-tmpfs-concurrency.json`) hash-hitting the SN-0796 registry entry — whose provenance was a registration backfill (a prose note: `['note', 'repair_commit_basis']`), carrying **zero** of the six runtime lineage keys the reconcile path hard-requires (`event_id`, `lineage_id`, `relationship_id`, `runtime_index_id`, `checkpoint_id`, `receipt_id`).

Two subsystems share one registry under two different provenance contracts: the registration tooling backfills prose provenance; the proof workflow demands runtime lineage. That is a **contract gap**, not a code bug — and the repair had three admissible moves only: (1) run the capture through the real runtime to earn the IDs, (2) relax the workflow to handle backfills gracefully, or (3) put a fail-closed guard at the seam. Fabricating the six IDs to satisfy the hard key access was never on the list (evidence law — SN-0778).

Naya 4 took (3): registry hash hits with incomplete provenance now emit `REGISTRY_HASH_HIT_INCOMPLETE_PROVENANCE` + exit 1 instead of a raw KeyError. The guard was proven on pin-exact artifacts — positive control (a provenance-complete entry flows through unchanged), negative control (the old code succeeds on complete provenance, so the failure is provenance-dependent, not code-dependent), 25/25 embedded heredocs compiling, remote blob sha256 == local. The contract decision itself (real runtime re-execution vs graceful handling) was routed to the owning lane as an explicit production-write decision — not silently resolved, not crashed over.

## HUMAN NOTE

Two departments share one filing cabinet, but one files by date and the other files by case number. When the second department can't find its case number on a folder the first department filed, the answer isn't to invent a case number — and it isn't to let the clerk crash either. You put a bright red sticker on the folder that says "filed differently — needs a decision," and you send the decision to whoever owns the cabinet. Three rules: name the mismatch, refuse to forge the missing piece, and make the unresolved part impossible to ignore.

## CHILD NOTE

Two kids share a toy box. One sorts toys by color, the other sorts by size. When the size-sorter can't find the size label on a toy the color-sorter put away, the smart move isn't to write a fake size on it — it's to put a special tag on it that says "sorted differently, ask a grown-up," and keep playing. You never make up the label, and you never just throw the toy away.

## GRANDMA NOTE

When two kitchens share a pantry and one labels jars by what's inside while the other labels by the recipe they belong to, a cook reaching for a recipe label and finding only a contents label shouldn't guess the recipe — and shouldn't drop the jar. She puts a bright ribbon on it that says "needs the head cook's eye" and carries on. The ribbon is the whole trick: it turns a confusing crash into a clear question, and the question goes to the person who can actually answer it.

## NAYA NOTE

Cold successor: when a consumer crashes on producer data, stop and check whether the two sides disagree on the **data contract** before touching either side's logic. The signature of a contract gap (vs a code bug): the failing access is a hard key/index read, the data was written by a different subsystem, and the missing piece is something the producer was never designed to provide. The repair pattern: (1) a fail-closed guard at the seam that emits a **named signal** + non-zero exit (never a raw exception, never a silent skip); (2) proof on pin-exact artifacts with a positive control (complete data flows unchanged) and a negative control (old code succeeds on complete data — the failure is data-dependent); (3) route the contract decision upstream as an explicit decision (here: real runtime re-execution is a production write — human decision). And the standing rule underneath it all: runtime-issued IDs are never hand-authored to satisfy a hard read. A green check built on a forged receipt is worse than the red one — SN-0778.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20260930-sn1577-backfill-runtime-provenance-seam-guard",
  "sn": "SN-1577",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-17",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE",
  "subcategory": "ENGINEERING-PROOF/INSTRUMENT-HARDENING",
  "lesson_type": "PROCESS_FIX",
  "applies_when": [
    ["capture", "reconcile", "provenance"],
    ["fresh-lesson", "workflow", "hash-hit-branch"],
    ["registry", "contract-gap", "consumer-seam"]
  ],
  "enforcement": "The fresh-lesson workflow's reconcile step must emit REGISTRY_HASH_HIT_INCOMPLETE_PROVENANCE and exit 1 on registry hash hits with incomplete provenance (never a raw KeyError, never a silent skip); the guard is proven by pin-exact repro with a positive control (provenance-complete entries flow unchanged) and a negative control (pre-guard code succeeds on complete provenance). The six runtime lineage keys (event_id, lineage_id, relationship_id, runtime_index_id, checkpoint_id, receipt_id) are never hand-authored — evidence law.",
  "evidence": {
    "monitor": "#1354 6098407008 — pipeline-monitor tick 214: fresh-lesson RED on tip 6f5713e8; capture .naya/capture/20261010-sn0796-phantom-pytest-failure-tmpfs-concurrency.json hash-hit SN-0796; entry provenance ['note','repair_commit_basis'] (backfill prose), six runtime keys missing; p[\"event_id\"] KeyError; same root-cause class as ticks 118/122/133",
    "repair": "#1354 6098433753 — Naya 4 self-build sign-out: PR #2121 (naya4/fresh-lesson-provenance-guard @ 48978267, base = exact tip 6f5713e8); guard emits REGISTRY_HASH_HIT_INCOMPLETE_PROVENANCE + exit 1; proven on pin-exact artifacts (positive + negative controls, 25/25 heredocs compile, remote blob sha256 == local); contract decision routed to owning lane as production-write decision",
    "ack": "#1354 6098516864 — Naya 2 relay ack on the fresh-lesson RED repair"
  },
  "rules": [
    "A consumer crash on producer data is a contract gap until proven otherwise: check whether the two sides were designed against different data contracts before touching either side's logic.",
    "The seam repair is a named fail-closed signal + non-zero exit — never a raw exception, never a silent skip, never a forged field.",
    "Prove the guard on pin-exact artifacts: positive control (complete data flows unchanged) and negative control (old code succeeds on complete data) — the failure must be data-dependent.",
    "Route the contract decision upstream as an explicit decision (runtime re-execution vs graceful handling); do not silently resolve it and do not crash over it.",
    "Runtime-issued IDs are never hand-authored to satisfy a hard read — a green check on a forged receipt is worse than the red one."
  ],
  "decision_change": "When a consumer crashes on producer data from a different subsystem, the first repair is a fail-closed named-signal guard at the seam (proven by pin-exact repro with positive/negative controls) — not exception-swallowing, not fabrication; the contract decision goes upstream as an explicit production-write decision.",
  "falsifier": "If the guard fires on provenance-complete entries (false positive), or a prose-backfilled entry ever yields a valid proof through reconcile, the seam classification is wrong.",
  "mechanism": "Hard key access on all six runtime lineage keys against registry entries written by a different subsystem (registration backfill writes prose provenance); the named signal converts an unclassified crash into a classified, routable condition at the exact contract boundary.",
  "cousins": ["SN-0778", "SN-0876", "SN-0746"],
  "supersedes": null
}
```
