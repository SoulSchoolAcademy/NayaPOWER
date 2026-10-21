# SUPER NOTE — When You Cannot Prove It, Refuse — Never Fake It or Weaken It

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-019` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-019` |
| Human title | When You Cannot Prove It, Refuse — Never Fake It or Weaken It |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 9 raw notes (full list below) |
| Cluster file | `cluster-02-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

If the safe tool doesn't exist, or the proof doesn't hold, the honest answer is 'no' or 'not proven' — never a weaker substitute dressed up as the real thing, and never a 'verified' stamp you didn't earn.

---

## 🩷 HUMAN NOTE

The tempting move is always available: the platform lacks the safety feature, so use a flimsier one and keep going. The evidence is missing a required piece, so stretch the rules to let it through. The check failed, so write 'verified' by hand. Every one of those moves was refused, and rightly. A system was stopped cleanly instead of running unprotected; claims were built from a fixed list of real facts so nothing injected could sneak in; a refusal was proven to have touched nothing at all. Refusing is not failure — pretending is.

---

## 🟣 CHILD NOTE

If you don't have your helmet, you don't ride — you don't tape a pillow to your head and call it a helmet. And you never say 'I finished' when you didn't. 'I can't do that safely' is a strong, honest answer.

---

## 👵 GRANDMA NOTE

If the bridge is out, dear, you turn around — you don't drive across on a plank and call it a bridge. And you never sign your name to something you didn't check. A clean 'no' protects everyone; a fudged 'yes' helps no one.

---

## 🤖 NAYA NOTE

Naya fails closed. When a required safeguard is unavailable, she refuses before changing anything. When evidence lacks an authoritative piece, she stops at the first gap rather than inventing the missing fact or widening the rules. Verification marks are always computed from the actual outcome — never written as constants — and the earlier a bad input is refused, the better.

---

## WHAT IT MEANS

Every fake pass and quiet downgrade converts a visible problem into an invisible one. The system keeps moving, but its safety story becomes fiction — and fiction compounds, because later decisions trust earlier stamps. Refusal keeps problems visible, priced, and fixable; pretending makes them free to grow.

---

## WHAT'S IN IT FOR YOU

You can trust the 'yes' when it comes, because 'no' was a real option. Things stop breaking in ways nobody can explain, because the weak substitute and the hand-written stamp were never allowed in.

---

## HOW IT APPLIES

When the proper safeguard isn't available, stop and say so instead of improvising a weaker one. Never widen a requirement to fit the evidence you have; get the real evidence or leave the gap named. And never mark anything verified by declaration — let the outcome itself produce the mark.

---

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0118 — SMART NOTE — A Crash Is Not a Verdict: Verifiers Must Fail Closed, Never KeyError [audit: PARTIAL → lost element restored]

A crash is not a verdict. A verifier must never crash on admissible input — an exception is a missing verdict, not a verdict. The discipline is tolerant reader, fail-closed writer: accept the persisted-name alias (`baseline_candidate_id` for `receipt["baseline_id"]` in `independent_recompute()`), and if both names are missing, raise an explicit `ValueError` refusing to recompute — a stated refusal — never a bare `KeyError` (an accident). Prove the fix with a negative control: the persisted-name test fails with `KeyError: 'baseline_id'` on pre-fix bytes and passes on fixed bytes.

### SN-0168 — Fail Fast at the Authoring Boundary — Refuse Bad Captures Before Persistence [audit: PARTIAL → lost element restored]

Fail fast at the authoring boundary: validate a capture's truth-boundary fields at discovery, before any runtime commit or persistence. A discovered capture missing either machine field — `machine_view.raw_source_separate_from_distillation is True` or `machine_view.automatic_truth_ceiling == "CANDIDATE"` — is refused at discovery with `CAPTURE_TRUTH_BOUNDARY_INVALID`, instead of REDing late in cold-successor after persistence.

### SN-0519 — Prove the Refusal Reached Nothing — Assert the Absence, and Run the Instrument on Its Author [audit: PARTIAL → lost element restored]

Run a new gate or instrument on its own author and the author's own work first. The first RED the instrument produces should be about the instrument's own territory: the canonical-capture gate caught its author's own incomplete allowlist in testing, and the author reported it as the finding, not as an embarrassment. An instrument that clears its author without inspection is unverified — verification before trust, applied to itself.

### SN-0573 — Every Learning Trial Ships a Fail-Closed Evidence Verifier — the Trial-4 Hole, Mechanized Shut [audit: MISSING → restored in full]

Every learning trial ships a fail-closed evidence verifier. A trial's raw data must be committed in-repo (never `/tmp`) with committed custody, or the verifier marks the trial INCONCLUSIVE — the same verdict an independent human verifier would give. Trial-4 was downgraded from PASS to INCONCLUSIVE because its raw data lived on ephemeral `/tmp` and was lost before independent verification, despite a statistically overwhelming result (20 fresh agents, p=0.0007, h=2.214). The machinery is the canonical `TRIAL-EVIDENCE-V1` spec plus `tools/verify_trial_evidence.py` plus an 11-test conformance suite that includes a Trial-4 regression replay: the verifier must reject the Trial-4 shape (summary statistics, no committed raw data) and accept the Trial-4R shape (raw data committed in-repo). Doctrine without enforcement is a wish; enforcement without a regression replay is untested — rule, enforcer, and replay together.

### SN-085 — Append-Only Is a Method, Not an Invariant — Resolve-Then-Trust Does Not Establish Origin [audit: MISSING → restored in full]

Append-only is a method (convention), not an invariant (structure) — conventions are attacker-reachable inside the boundary. In `VerifyNode._receipts`, append-only is enforced only by the `delete_receipt` method on a plain dict; any same-process holder can write a forged VERIFIED_PASS receipt directly into the dict, so resolve-then-trust does not establish origin on a poisonable store. Anchor trust in invariants: content-committed ids, allowlist comparison against the resolved object (the allowlist includes `subject_ref`), and store-identity consumption — consume the RESOLVED receipt, never the caller's object. Make dangerous seams structurally impossible: the resolver is construction-owned so callers cannot substitute it, stale/REOPENED receipts are refused, fixture mode is locked so it cannot be accidentally enabled, and ownership is proven through id format, issuer, and structural fields. Keep the falsifying counterexample in the record — it outvalues the design it breaks. Don't patch the resolver's reading — fix what it reads from.

### SN-090 — A PASS on Receipt Family X Never Qualifies Receipt Family Y — Fail Closed at the First Missing Authoritative Field [audit: PARTIAL → lost element restored]

A PASS on receipt family X never qualifies receipt family Y. Bind every proof artifact to the specimen family it exercised: 14/14 on the kernel `demo-001` receipt family is not 14/14 on the Demo-1 ACT receipt family, and citing it as such is misattribution, not efficiency. Borrowed evidence is not evidence. Verify the runner's own source for which family it proves before treating its result as transferable.

### SN-091 — Resolve Contract Mismatches at the Source, Not by Widening the Contract — the Five-Class Field-Binding Taxonomy [audit: PARTIAL → lost element restored]

When a contract mismatch blocks, source-find first: re-check authoritative tables, envelopes, writers, and run evidence — never widen the contract. Classify every field of the binding manifest into exactly one of five classes and refuse unlabeled fields: **RECEIPT-BOUND** — exact receipt bytes; **SOURCE-BOUND** — an authoritative external source, named, with its non-claim boundary stated; **WRITER-ASSIGNED** — allocated by the canonical writer at insert; **EXPLICIT-EMPTY** — a declared no-claim state, not a fabricated value or a placeholder; **UNKNOWN** — kept rather than guessed when authoritative proof is missing; UNKNOWN is a complete binding.

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn081-containment-never-degrades-platform`
- `IB-SMART-NOTE-20260930-sn0118-verifier-fail-closed-never-keyerror`
- `IB-SMART-NOTE-20260930-sn0573-trial-evidence-fail-closed-verifier`
- `IB-SMART-NOTE-20260930-sn0528-never-attest-with-a-literal`
- `IB-SMART-NOTE-20260930-sn0519-refusal-must-reach-nothing-instrument-audits-its-author`
- `IB-SMART-NOTE-20260930-sn0168-fail-fast-authoring-boundary`
- `IB-SMART-NOTE-20260930-sn085-append-only-method-not-invariant`
- `IB-SMART-NOTE-20260930-sn090-receipt-family-mismatch`
- `IB-SMART-NOTE-20260930-sn091-field-binding-taxonomy`
