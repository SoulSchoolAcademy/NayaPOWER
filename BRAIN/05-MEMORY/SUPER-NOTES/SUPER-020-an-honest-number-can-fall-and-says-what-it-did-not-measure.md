# SUPER NOTE — An Honest Number Can Fall — and Says What It Did Not Measure

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-020` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-020` |
| Human title | An Honest Number Can Fall — and Says What It Did Not Measure |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 14 raw notes (full list below) |
| Cluster file | `cluster-02-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

A measurement you can trust is allowed to go down, is made by someone who didn't do the work, and says plainly what it did not measure. A score that only rises, or hides its limits, is a costume.

---

## 🩷 HUMAN NOTE

We learned to distrust pretty numbers. One stamp carried a famous method's name while the inputs fed to it were invented. A system claimed it had 'influenced' a decision merely because information was present in the room. Lessons were 'proven' on tasks so easy that nothing could fail them. And tidy summaries quietly hid their weak spots in the fine print. The honest pattern looks different: an independent measurer, a baseline nobody flattered, bad news reported instead of silently corrected, leftovers and unknowns named next to the score, and real comparisons — with and without — before claiming anything changed anything.

---

## 🟣 CHILD NOTE

If your report card could only ever go up, it wouldn't tell you anything. A real score can drop when you do worse — that's how you know it's honest. And a good score says what it didn't test, too.

---

## 👵 GRANDMA NOTE

Be wary of anyone whose scales always agree with them, dear. Honest measuring means the number can embarrass you. And a plain 'I don't know yet' is worth more than a confident guess dressed up as knowledge.

---

## 🤖 NAYA NOTE

Naya publishes her own measurements, never adopts the builder's. She states the instrument and its limits before the score, names residuals and unknowns beside every verdict, and treats presence as presence — never as influence — until a controlled comparison proves a real effect. When a re-measurement disagrees with the record, she reports the disagreement instead of quietly fixing the record.

- A famous name stamped on a receipt is not proof the named method did the work: binding the ratified calculator's config hash into a receipt proves which rulebook was referenced, not that the shared calculator ever ran, when the scores were in fact computed locally and honestly labeled as proxies (sn063). Either put the real calculator in the decision path, or fence the local math as provisional and name the exact conditions under which the fence lifts (sn063).
- A retry is not idempotency: a mechanism that retries a number after a collision proves only that every row gets a unique number — allocation uniqueness — and must never be credited with execution idempotency (sn070). Idempotency has four separate conjuncts, each needing its own proof: the same logical request executes once; duplicate retries reread the original result instead of recomputing; the same key with a changed payload is rejected; concurrent same-key requests produce one outcome (sn070).
- Report a finding's consequence class honestly before sounding the alarm — a working fail-closed gate blocking a not-yet-wired path is a composition gap, not a security defect or a regression (sn092). Write the gap tests to self-invalidate: assert the gap's presence, so the tests fail by design the moment the wiring lands and force requalification instead of quietly going stale, and keep a named list of the limits you will not paper over (sn092).

---

## WHAT IT MEANS

Measurement is how a system learns about itself; corrupt the measurement and every later decision is built on fog. The deepest corruptions are quiet ones — labels mistaken for evaluations, closeness dressed as causation, easy tests standing in for hard ones. Honest measurement is not modesty; it is the machinery that makes improvement possible at all.

---

## WHAT'S IN IT FOR YOU

You get numbers you can steer by. Progress becomes real instead of theatrical, weak spots get fixed while they're small, and 'I don't know' becomes useful information instead of a shameful secret.

---

## HOW IT APPLIES

Have the work measured by someone who didn't build it, and let the score fall when it should. Beside every result, write what wasn't measured and what remains unknown. Before claiming something made a difference, compare with-and-without under the same conditions, at realistic difficulty.

---

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-063 — Receipt Provenance — Binding the Ratified Hash Is Not the Shared Calculator Deciding [audit: MISSING → restored in full]

Binding a ratified config hash into a receipt is only a provenance claim about the CONFIG — it is not proof the shared calculator decided. The nine-node kernel's decision receipts bind `calculusConfigHash: CALCULUS_V21_SPEC_HASH` with `calculus_spec_status: "RATIFIED"`, yet no node under `naya_kernel/nodes/` imports the shared `kernel/value_calculus.py`: EVOLVE's `_score_candidate` computes `score = value - risk` locally, and CONNECT computes `q_proxy`/`v_safe_proxy` from local inputs — local proxies, honestly labeled, never the canonical engine's scores. Receipts prove the local computation was deterministic and recomputes to MATCH; they do not prove the calculator decided. Verify at the exact SHA whether the decision path calls the executable shared calculator or only binds its hash. For merge-readiness: replace the local calculations with calls to the executable shared calculator, or explicitly fence them as provisional with the exact conditions under which the fence lifts. Honest labeling buys trust; it does not close the gap.

### SN-070 — Retry-on-Conflict Is Not Idempotency — Uniqueness Retries Prove One Allocation, Not One Execution [audit: MISSING → restored in full]

Retry-on-conflict is not idempotency. The `nayanet-act-runtime` handler's retry of the monotonically increasing `revision` after a 23505 collision protects revision uniqueness only — no two rows share a revision number. It proves none of the four conjuncts actual idempotency requires: (1) the same logical request executes once; (2) duplicate retries reread the original result instead of recomputing; (3) the same idempotency key with a changed payload is rejected; (4) concurrent same-key requests produce one outcome. Name the four conjuncts explicitly, map each to exact source at the frozen SHA — lines, mechanism, test — and keep the gap major until all four are proven against exact-head source. Allocation-uniqueness retry covers conjunct-zero only; file it under uniqueness, never idempotency. Borrowed credit is inflated credit — narrow the claim, don't transfer the mechanism's strength.

### SN-083 — Retain the UNKNOWN With Its Missing Evidence Named [audit: PARTIAL → lost element restored]

When two reports conflict, resolve every resolvable leg from the evidence first — never silently choose one report. Retain each unresolvable leg as a terminal UNKNOWN naming the precise missing evidence and its owner: a retained UNKNOWN with named missing evidence is completed diligence; an unnamed one is a shrug. Author no canonical change against an unresolved target — writing canonical semantics against an unresolved deployed target risks breaking the flows that depend on it; the decision to author nothing is recorded as a decision, not as inaction.

### SN-089 — Publish Your Own Number, Never Adopt the Builder's — Parent Comparison Makes an Unfamiliar Result Interpretable [audit: PARTIAL → lost element restored]

Make an unfamiliar result interpretable with a parent comparison: run the parent commit under identical conditions, so "introduced zero new failures" is measured from the parent-vs-child delta, never asserted. In the source case the parent measured 33 failed / 1070 passed / 3 skipped / 5 errors and the child 31 / 1091 / 3 / 5 under identical conditions — the change fixed two, added 21 passing tests, and introduced zero new failures, proven by measurement. "Pre-existing" is proven by the parent measurement, not asserted.

### SN-092 — Design Qualification Tests That Self-Invalidate — and Name the Consequence Class Honestly [audit: MISSING → restored in full]

Design gap tests as presence-assertions that self-invalidate when the gap closes: the 7 composition tests assert the gap's presence (resolver is `None`, no accessor exists), so the moment the builder's wiring lands the tests fail by design — they force requalification instead of going stale. A test that can silently go stale can lie by omission. Name the consequence class honestly before the headline — composition gap, regression, security defect, or blocked frontier: a working fail-closed gate is a composition gap, never a defect or a regression, and calling it one corrupts triage. Ship the future acceptance criteria with the finding (a genuine receipt accepted; forged/unknown/tampered/wrong-subject still refused), specify the smallest fix without implementing it when you are the verifier, maintain a "limits I will not paper over" section naming threat-model and scope boundaries, and never present a component PASS as integration proof.

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn0107-score-keeper-independent-scores-must-fall`
- `IB-SMART-NOTE-20260930-sn0161-name-the-instrument-render-gap`
- `IB-SMART-NOTE-20260930-sn0532-name-the-residuals`
- `IB-SMART-NOTE-20260930-sn0121-verifier-names-its-boundary`
- `IB-SMART-NOTE-20260930-sn0448-report-dont-silent-correct`
- `IB-SMART-NOTE-20260930-sn089-publish-your-own-number`
- `IB-SMART-NOTE-20260930-sn063-receipt-provenance-binding-vs-deciding`
- `IB-SMART-NOTE-20260930-sn084-version-label-is-not-evaluation-proof`
- `IB-SMART-NOTE-20260930-sn092-self-invalidating-tests`
- `IB-SMART-NOTE-20260930-sn083-retain-unknown-with-named-missing-evidence`
- `IB-SMART-NOTE-20260930-sn0510-influence-is-a-number`
- `IB-SMART-NOTE-20261007-sn0544-presence-is-not-influence-separate-context-from-causal-proof`
- `IB-SMART-NOTE-20261006-sn0495-toy-tasks-do-not-discriminate-measure-lessons-at-real-difficulty`
- `IB-SMART-NOTE-20260930-sn070-retry-not-idempotency`
