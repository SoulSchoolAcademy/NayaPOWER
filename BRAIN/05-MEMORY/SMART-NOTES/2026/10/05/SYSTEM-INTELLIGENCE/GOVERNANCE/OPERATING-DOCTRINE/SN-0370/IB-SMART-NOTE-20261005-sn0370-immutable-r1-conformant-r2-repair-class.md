# Immutable R1 → Conformant R2: The Historical-Capture Repair Class

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0370-immutable-r1-conformant-r2-repair-class
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5999097328 ([NAYA][SCOPE CORRECTION], 2026-10-05T16:55:48Z / 09:55 PDT): the in-place plan for #1482 was withdrawn after exact live evidence on main cd60cb4f85a — kernel run: `entries_with_stale_hash` grew 0→1 (sole stale entry SN-346 / IB-SMART-NOTE-20261005-sn0355-nonstop-loop, persisted hash 8e0db26...); Live Intelligence run: fresh-lesson failed at the runtime call with HTTP 400 after changed capture could not hash-reconcile; canonical SQL rejects reusing the same event key via EVENT_ID_REPLAY. Correction confirmed: #1354 5999140626 ([NAYA VERIFIER][SIGN-OUT] — immutable R1 → conformant R2 is the correct repair). Precedent: SN-004 R2.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A persisted historical capture (R1) was found defective: SN-346's directory held the SN-0355 content (identity/routing defect) AND the hashed intelligence bytes had changed after capture (content-immutability defect — the historical R1 at merge `19526a8a...` had no `smart_note_id` and no `raw_source_separate_from_distillation`; after #1483 it had both, while the persisted R1 object and registry hash `8e0db26...` did not move; the runtime correctly refused same-event replay). The first repair plan — edit the capture in place — was **withdrawn on evidence** before anything merged. In-place repair of history is a contradiction: the persisted R1 bytes are the thing every later reconciliation measures against, so changing them poisons the measuring stick.

The correct repair class, same precedent as SN-004 R2:

1. Restore R1's intelligence payload to the exact persisted/hash-matching historical bytes — the past is not rewritten.
2. Preserve R1 provenance and mark it SUPERSEDED in top-level lifecycle metadata only — the metadata label moves, the bytes never do.
3. Create a new conformant R2 capture with a fresh event identity (canonical SQL's EVENT_ID_REPLAY makes reusing the old event key impossible anyway).
4. Assign the stable human ID (here SN-0355) to R2; the historical runtime allocation (SN-346) stays on R1 — humans read the stable ID, machines resolve the full lineage.
5. R2 explicitly SUPERSEDES R1 with a machine-resolvable edge; generated lifecycle state; CANDIDATE ceiling holds for the new capture.
6. Registry records lifecycle; canonical retrieval excludes SUPERSEDED entries.
7. Conformance tests fail closed if someone labels a bad capture SUPERSEDED without a real conformant successor plus an explicit edge — supersession must not become a hole to drop garbage through.
8. No baseline expansion, no workflow weakening, no production/DB/credential action.

Corollary from the same incident (verifier correction #1354 5999160496): do not collapse the diagnosis to the first visible defect. The board's first reading was "pipeline routed SN-0355 into the SN-346 directory" — routing only. Checking the actual persisted projection proved content drift too: the directory is evidence of the *earlier* ID allocation, not the whole defect. Measure the bytes, not the pathname. The in-place plan died twice — once to the runtime's hash refusal, once to the verifier's deeper inspection — which is exactly the order you want: machine enforcement first, human correction second.

Why this is brain-grade: a cold Naya months from now will face a defective historical capture and the obvious move will be "fix the bytes in place — it's just one file." This note teaches the structural reason that's forbidden: persisted captures are the evidence everything else is measured against; editing them is destroying the measuring instrument. The R1→R2 pattern turns a repair into a lineage: history preserved, correction explicit, machine-checkable.

## 🩷 HUMAN NOTE

Shawn — one important repair-class decision today on the SN-346 stale-hash red. The first instinct (edit the bad capture in place) was withdrawn before anything shipped: you can't repair history by rewriting it, because every later reconciliation measures against those exact persisted bytes. So the repair preserves R1's bytes exactly, marks it SUPERSEDED in metadata only, and issues a fresh conformant R2 carrying the stable SN-0355 ID with a machine-resolvable supersedes edge — same precedent as the old SN-004 R2 repair. The runtime already refused the in-place path (hash mismatch → HTTP 400; canonical SQL rejects event-key reuse), and a verifier caught that the defect was deeper than routing — content drift too. No production or database action anywhere in the repair.

## 🟣 CHILD NOTE

Imagine a class photo book. One photo has the wrong names written under the faces. You don't take a pen and scribble over the old book — because the old book is the record everyone compares against. Instead you leave the old page exactly as it is, put a sticker on it that says "outdated — see page 2," and add a new page 2 with the right names. Anyone can check: the old page proves nothing was hidden, and the new page is the correct one. That's the rule: never rewrite the past to fix it; add a corrected version and point from the old to the new.

## 👵 GRANDMA NOTE

It's like an official land registry. If an old entry has an error, you don't white-out the ledger — that would destroy the trust the whole registry rests on. You leave the old entry untouched, mark it superseded, and file a new corrected entry that explicitly replaces it. Anyone can audit the chain: old entry intact, new entry explicit, the link between them recorded. The repair class does exactly this for the brain's persisted captures — history preserved, correction forward, machine-checkable links.

## 💜 NAYA NOTE

Note to future me: the moment a repair plan involves editing already-persisted bytes, stop — that plan is dead and the evidence law will eventually say so loudly (HTTP 400 at the runtime call, stale-hash growth 0→1, EVENT_ID_REPLAY rejection). The R1→R2 class: (1) R1 bytes immutable, labeled SUPERSEDED in metadata only; (2) R2 with fresh event identity, stable human ID, explicit machine-resolvable SUPERSEDES edge, CANDIDATE ceiling; (3) retrieval excludes SUPERSEDED; (4) conformance tests fail closed on supersession-without-successor. And the diagnostic corollary: never collapse to the first visible defect — the directory name was evidence of the ID allocation, not the whole drift; check the persisted projection bytes themselves before declaring the diagnosis. Cite the precedent: SN-004 R2.

## ⚙️ MACHINE NOTE

{"sn": "SN-0370", "title": "Immutable R1 → Conformant R2: The Historical-Capture Repair Class", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "OPERATING-DOCTRINE"], "extends": [], "related": ["SN-004", "SN-0042"], "evidence": {"board": "#1354 5999097328 ([NAYA][SCOPE CORRECTION], 2026-10-05T16:55:48Z): in-place #1482 plan withdrawn on live evidence at main cd60cb4f85a — entries_with_stale_hash 0->1 (SN-346, hash 8e0db26...), fresh-lesson HTTP 400 on hash-reconcile failure, EVENT_ID_REPLAY rejects same-event-key reuse; verifier 5999140626 confirms immutable-R1->conformant-R2; correction 5999160496: not routing-only — persisted projection proves content drift too (R1 lacked smart_note_id + raw_source flag, #1483 changed hashed intelligence bytes, registry holds old hash); precedent SN-004 R2", "pins": {"main": "cd60cb4f85a90276ee0e6bcc245faa06121045c6", "merge_R1": "19526a8a", "stale_hash": "8e0db26..."}}, "rule": "never in-place edit a defective persisted capture: preserve R1 bytes exactly (label SUPERSEDED in lifecycle metadata only), issue conformant R2 with fresh event identity + stable human ID + machine-resolvable SUPERSEDES edge, retrieval refuses SUPERSEDED, conformance tests fail closed on supersession without a real conformant successor; diagnose the persisted bytes, never just the pathname"}
