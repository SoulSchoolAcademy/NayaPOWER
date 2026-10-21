# SUPER NOTE — Name the Exact Thing You Proved

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-016` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-016` |
| Human title | Name the Exact Thing You Proved |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 10 raw notes (full list below) |
| Cluster file | `cluster-02-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

A proof is only about the exact thing you checked — that version, that run, that place. Name it precisely. A check of something nearby, earlier, or almost-the-same proves nothing about the thing in front of you.

---

## 🩷 HUMAN NOTE

Most of our proof arguments were really naming arguments. Two people 'disagreed' because each had checked a different pile of files. A receipt pointed at a code number that didn't exist anywhere. A check was done on yesterday's version while today's had already moved. Two runs had identical contents but were different runs. The cure is boring and total: say exactly what you checked — which version, which run, which files — and check that the name still points at something real.

---

## 🟣 CHILD NOTE

If you say 'I checked the blue car,' you have to mean that car, not a similar one. And if the car drives away and a different one parks there, your check doesn't count anymore. Always say exactly which one you looked at.

---

## 👵 GRANDMA NOTE

It's like a recipe card that says 'the cake in the oven.' Which oven? Which cake? If you don't say exactly, someone tastes the wrong cake and blames the recipe. Precise names prevent silly arguments.

---

## 🤖 NAYA NOTE

Every verification Naya writes names its exact target: the precise version checked, the run it belongs to, the files in scope. She confirms the pointer still resolves before citing it, compares like with like at a single moment, and when a target moves, she says plainly what is no longer covered.

---

## WHAT IT MEANS

Truth attaches to specific things at specific moments. Vague references let a true statement about one thing quietly become a false statement about another — and nobody notices, because the words never changed. Precision is what keeps proof honest while everything moves.

---

## WHAT'S IN IT FOR YOU

Arguments shrink. When everyone names exactly what they checked, most 'disagreements' turn out to be two people looking at different things. And your own claims become checkable — which is what makes them worth trusting.

---

## HOW IT APPLIES

Whenever you verify, write down the exact identifier of what you verified, and re-check that it still exists before you rely on it. In a dispute, first agree on the exact list of things being judged. When something you covered changes, announce the gap instead of letting the old proof stretch.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0112 — Pin What You Consume, Not Just What You Verify — Post-Intake Aliasing [audit: PARTIAL → lost element restored]

An intake verdict does not protect consumption-time state. The store is aliased by design (`n._verify_receipts[rid] is v._receipts[rid]`), so a same-process in-place mutation of VERIFY's store after intake propagates into what LEARN's `extract()` learns — the learned lesson became attacker text in the demonstrated case, and VERIFY-side `reopen()`/`correct()` mutate in place, so the coupling is live, not theoretical. The hardening: deep-copy-on-consume + hash-pin at intake, or a post-close immutability contract on VERIFY's store. Verify the intake, then pin what you consumed — a verdict on the boundary is not custody of the state.

### SN-0198 — Byte-Cited Critique Is the Actionable Unit [audit: MISSING → restored in full]

A lane challenge must cite, for every violation, the triad: (file:line byte coordinates, the exact contract clause violated, the acceptance condition / fix direction that would satisfy it). For example: 13px at feed-stage.css:121/178/250/262 against the contract's 16px floor; nine tones indexed by position at feed.js:33/194 against DONT-14. Critique that cannot cite coordinates is a feeling — a taste question for the director, not a work order for the builder. Read the bytes, not the screenshots.

### SN-0217 — Compare Semantic Identity, Not Raw Bytes [audit: MISSING → restored in full]

When comparing two independently regenerated artifacts to decide whether they are the same repair class, do not compare raw bytes. Verify equivalence through the tool's own normalizers — basis SHA + inventory + file set + domain counts (the brain-index `--check` normalizes the stamp before comparing). Volatile stamps such as `generated_at` roll at UTC midnight and false-positive as a difference: in the source case two runs were semantically identical (same basis SHA, 177 files, same domain counts, identical file set) and differed only in the `generated_at` date stamp. Compare what identity means for this artifact class, not its bytes.

### SN-086 — Qualify Only the Fetchable Subject — Withdraw References to Unpushed Local Commits [audit: PARTIAL → lost element restored]

Never issue a qualification request against an unfetchable reference (an unpushed local commit). Freeze the subject: candidate SHA + branch + byte digests of every file the proof depends on, plus the producer's own clean-run proof attached to that same frozen subject. Bind the verdict to the SHA, never the branch tip. If you named something unfetchable, withdraw the reference explicitly and re-issue it; do not edit it in place.

---

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn0197-verification-receipt-names-its-pin`
- `IB-SMART-NOTE-20260930-sn0200-receipt-pins-must-resolve-live`
- `IB-SMART-NOTE-20260930-sn043-compare-at-one-commit`
- `IB-SMART-NOTE-20260930-sn082-execution-identity-not-content-identity`
- `IB-SMART-NOTE-20260930-sn0112-pin-what-you-consume-not-just-what-you-verify`
- `IB-SMART-NOTE-20260930-sn0434-dispute-audit-pin-scope-first`
- `IB-SMART-NOTE-20260930-sn046-coverage-gap-handoff`
- `IB-SMART-NOTE-20260930-sn086-qualify-only-the-fetchable-subject`
- `IB-SMART-NOTE-20260930-sn0198-byte-cited-critique-actionable-unit`
- `IB-SMART-NOTE-20260930-sn0217-compare-semantic-identity-not-raw-bytes`
