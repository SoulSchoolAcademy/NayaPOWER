# Author Once, Derive the Rest — Hand-Authoring Derived Artifacts Manufactures Drift

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0248-author-once-derive-the-rest
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5982175150 (2026-10-04T16:39:10Z, Naya 4 — conceding and adopting CODA 3's findings on the SN lifecycle backfill plan; Finding 2 on the three-artifact invariant).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Phase 1 of the PRIORITY ONE lifecycle work had established an invariant: every capture PR ships three artifacts — official-format markdown, capture JSON, and index entry. Conceding CODA 3's finding, Naya 4 reversed it: as *independently authored* artifacts, the three-artifact rule is architecturally backwards. The pipeline already generates the projection and the index entry from independently verified persisted intelligence — that IS the water-flow. **One authored capture; everything else derived.** Manually authoring all three is how we manufacture the drift we're trying to eliminate: three hands on three keyboards produce three slightly different truths, and every difference is a future debugging session. #1350/#1351 get reconciled to the ownership model before merge, not manually "satisfied" by touching up each file.

Why this is brain-grade: the whole cold-recall RED was authoring drift — SN-020/021/022 omitted keys the gate required, while hand-authored cousins had them. When humans author every layer of the artifact stack, drift isn't a bug, it's the production process. The ownership model is a single source of truth enforced by structure, not discipline: the author writes exactly one canonical artifact; the system derives the rest deterministically; verification checks the derivation, never a second hand-typed copy. This is the same law that already runs the brain: SN-0095 (compose at the consumer — authorship stays in the author, trust in the seal), SN-0069 (bindings at the observing layer — only the kernel observes the evaluated inputs), SN-0110 (one intelligence, three projections — canonical markdown wins on conflict). The new edge this note adds: a conformance story that requires humans to satisfy every projection by hand is not rigor — it is drift-by-design, and it will fail exactly like the RED it was built to prevent. A cold successor that sees "satisfy all N artifacts by hand" in a plan should recognize the anti-pattern and reassign: author the canonical one, generate the rest, verify the generation. Cousins: SN-0095 (compose at the consumer), SN-0069 (bindings at the observing layer), SN-0110 (one intelligence, three projections), SN-0244 (one format, one spot — specimen is law; the 3-artifact invariant, now superseded by the ownership model — do not cite them together without noting the supersession).

## 🩷 HUMAN NOTE

Shawn — banking the ownership-model correction: Phase 1's "three artifacts per PR" rule was architecturally backwards when it means three hand-authored files. The pipeline already generates the projection and index entry from the persisted intelligence — that's the water-flow. One authored capture, everything else derived. Hand-authoring every layer is how we manufacture the very drift we're trying to eliminate. #1350/#1351 get reconciled to this ownership model before merge.

## 🟣 CHILD NOTE

The team had a rule: every new note must ship three matching files. They realized the rule was backwards — when three different people (or the same person three times) write three matching files by hand, they always drift apart a little. The fix: one person writes ONE file, and the computer automatically creates the other two from it. You only ever need to check that the computer's copying is correct — you never need to keep three hand-written copies in sync.

## 👵 GRANDMA NOTE

We've corrected one of our own rules. We used to require three matching files for every note, all written by hand. That was backwards: anything written by hand three times will eventually disagree with itself. The new rule is simple — write the one original, and let the system generate the other two from it automatically. Then you only verify the generation, not three separate hand-written copies.

## 🤖 NAYA NOTE

Source: #554 5982175150 (2026-10-04T16:39:10Z, Naya 4 — Finding 2 of CODA 3's cross-layer verification: "Phase 1's 'three artifacts per PR' as independently authored artifacts is architecturally backwards. The pipeline already generates the projection and index entry from independently verified persisted intelligence — that IS the water-flow. One authored capture; everything else derived. Manually authoring all three is how we manufacture the drift we're trying to eliminate. This also means #1350/#1351 get reconciled to the ownership model before merge, not manually satisfied."). Note the supersession: SN-0244's "3-artifact invariant" (official-format md + capture v2 JSON + index entry, format drift = corruption) remains the *format* invariant; the *authoring* model changed — three required artifacts, one authored source. Cite SN-0244 for format, this note for authorship. Cousins: SN-0095, SN-0069, SN-0110, SN-0244.

## ⚙️ MACHINE NOTE

{"sn": "SN-0248", "title": "Author Once, Derive the Rest — Hand-Authoring Derived Artifacts Manufactures Drift", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-04", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "INTERFACE-OWNERSHIP"], "cousins": ["SN-0095", "SN-0069", "SN-0110", "SN-0244"], "authority": "PRIORITY ONE team deliberation on #554 (CODA 3 cross-layer verification; Naya 4 runtime/kernel concession and adoption)", "evidence": {"comment": "#554 5982175150", "finding": "CODA 3 finding 2 on the SN lifecycle backfill plan: three hand-authored artifacts = architecturally backwards; pipeline already derives projection + index entry from persisted intelligence", "reconciliation": "#1350/#1351 to be reconciled to the ownership model before merge, not manually satisfied"}, "doctrine": {"author_once": "exactly one canonical authored artifact per capture; everything else is derived deterministically by the pipeline", "verify_the_derivation": "verification checks the generation rule, never a second hand-typed copy", "supersession_note": "SN-0244's 3-artifact invariant remains the format invariant; this note governs the authoring model — cite format to SN-0244, authorship here", "antipattern": "\"satisfy all N artifacts by hand\" is drift-by-design; reassign to author-canonical / generate-rest / verify-generation"}}
