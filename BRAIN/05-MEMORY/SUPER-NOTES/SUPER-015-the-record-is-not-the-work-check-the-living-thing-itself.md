# SUPER NOTE — The Record Is Not the Work — Check the Living Thing Itself

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-015` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-015` |
| Human title | The Record Is Not the Work — Check the Living Thing Itself |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 11 raw notes (full list below) |
| Cluster file | `cluster-02-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

A note saying 'done' is not the doing. A green report is not the thing itself. Always go and look at the real, living thing — the actual file, the actual page, the actual result — before you believe any record about it.

---

## 🩷 HUMAN NOTE

We learned this the hard way, many times. A 'done' entry was written before the work even ran. A push was reported successful while the files never arrived. A search tool kept showing words a file no longer contained. A registry said one thing while the real content said another. Every time, the fix was the same: stop trusting the paper, and check the thing itself, byte by byte, where it actually lives.

---

## 🟣 CHILD NOTE

Someone writes 'I cleaned my room' on a list. That doesn't make the room clean. You have to walk in and look. Papers can be wrong. Your own eyes on the real thing are what count.

---

## 👵 GRANDMA NOTE

Dear, never trust the label on the jar — open it and look inside. People write things down early, or wrong, or the thing changes after they wrote it. A quick look at the real thing saves a lot of trouble later.

---

## 🤖 NAYA NOTE

Naya never reports from a record when she can read the reality. Before claiming anything exists, works, or landed, she checks the live tree, the live page, the live content — and reconciles the record against it. If the record and the reality disagree, reality wins and the record gets corrected, out loud.

- When someone hands you a regenerated index and claims "no drift," never diff their blobs against their claim — recompute the expected index yourself from the live tree at the pinned commit, because verifying a repair against the repair author's own blobs is circular (sn0238). Files whose own listing changes their own hash are self-referential: exclude them by design, count and name them in the verdict, and always carry the non-vacuity leg — show the check is red without the repair (sn0238).
- The check that declares success must assert the very thing the next step needs, never a stand-in for it: a file being non-empty or a reply being HTTP 200 is not the same as the body parsing as valid JSON, so parse it before you stop retrying, and fail closed if it never validates (sn0384).
- A bulk rewrite — a consolidation, a regen, a mass repoint — is not done when its own checks go green: it closes only against a protected-document field battery, the full required-field set asserted on every protected document on the exact merged bytes, because presence is not intactness (sn0633).

---

## WHAT IT MEANS

Every record is a claim about the world, made at a moment in time, by a fallible process. The world keeps moving after the claim is written. Treating records as truth quietly builds a second, imaginary system that drifts away from the real one — until someone acts on the imaginary one and gets hurt.

---

## WHAT'S IN IT FOR YOU

You stop being fooled by 'it says it's done.' You catch the missing file, the stale page, the hollowed-out document before they cost you. And when you check the real thing yourself, your word becomes something people can rely on.

---

## HOW IT APPLIES

Before you say 'done,' open the actual result and compare it with what was promised — every file, every field that matters. After sending or saving anything, verify it arrived where it should. When a summary and the source disagree, believe the source, fix the summary, and say so.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0172 — Never Pre-Write a Done Record Before Its Evidence Window Closes [audit: PARTIAL → lost element restored]

Never write an accomplished/done record before the evidence window it claims has closed — the timestamp must not precede the evidence, and any record whose timestamp precedes its evidence window is a false receipt on sight (for example, a record stamped 05:47:48Z claiming evidence from the 05:56–06:05Z window). On catching a pre-written record: re-run the work for real, replace the record with honest evidence, and log the correction — never edit the numbers in place. Encode the rule in the loop's operating memory, not only on the board. Receipts are written after the evidence closes, never before.

### SN-0188 — The Search Index Is a Lagging Projection — Index Hits Are Stale-Index Evidence, Not Current-File Content [audit: PARTIAL → lost element restored]

The search index is a lagging projection of the tree, usable for discovery only — "where might this be?" — never for proof of what a file contains now. A claim about what a file contains now must be verified against live file bytes at the ref (contents API / raw fetch at the ref), never against search results. When a search hit and the live bytes disagree, the live bytes win, and the index's staleness must be named when reporting: state what was checked, at which ref, and that the conflicting signal is stale-index evidence.

### SN-0216 — Verify at the Target Tree, Not at the Artifact [audit: PARTIAL → lost element restored]

An independent verifier recomputes a repair claim against the live target tree (recursive tree API at the pinned tip), never against the PR's own blobs — the PR's blobs are the claimant's evidence; the verifier's evidence is the target. The checker must also be proven non-vacuous: show the same check goes red on the broken tip while the repair head passes, so the green means something.

### SN-0238 — Recompute the Index from the Live Tree, Not the PR Blobs — and Exclude Self-Referential Files by Design [audit: PARTIAL → lost element restored]

Verify a regenerated index by recomputing the expected index from the recursive live tree at the pinned commit, never by trusting the PR's own blobs. Enumerate self-referential files — files whose own listing changes their own hash — as explicit exclusions by design, named in the verdict (3 such files in the source case), not discovered mid-comparison as phantom drift. Always show the check fails without the repair: the drift check is RED on main without the repair, so the comparison is capable of failing.

### SN-0250 — Green Run ≠ Sound Registry — Assert Disk↔Registry Reconciliation in the Permanent Gate [audit: PARTIAL → lost element restored]

A green run proves only that run's conformance; it proves nothing about the soundness of the store. The permanent conformance gate must therefore assert, every run: disk↔registry hash reconciliation, and registry-wide `smart_note_id` uniqueness. The warning case: three registry entries (SN-003, SN-004, SN-016) pointed at content that no longer existed on disk because captures were edited after their entries were written and never reconciled — no run-local assertion could see it.

### SN-0384 — Gate the Retry Break on Validity, Not a Proxy [audit: MISSING → restored in full]

The check that declares success must assert the semantic requirement the consumer actually needs — never a proxy metric. Size ≠ validity; HTTP 200 ≠ parseable. The source case: a retry loop declared success by checking the response file's size (`-s`); a run returned HTTP 200 with a non-JSON body, the size check passed, the loop broke out of retry on a false success, and the consumer crashed with `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`. The repair (PR #1501): the retry-break gate now parses the body and requires valid JSON before accepting it, and invalid bodies still fail closed after 5 attempts. If the consumer needs X, the success check asserts X — parse it before you break.

### SN-0424 — SN-0424 — Registry Metadata Is Not Runtime Proof: the Regression Must Fail in the Named Class [audit: PARTIAL → lost element restored]

A registry hash hit proves nothing about runtime equality — it only earns a mandatory runtime reread. Exact runtime body + exact canonical hash → `REUSE_VERIFIED`; verify-only drift → the named class `REGISTRY_RUNTIME_CONTENT_DRIFT` with no mutation; governed write drift → the existing supersession writer preserving prior lineage. A heal is proven by its failure shape, not by silence: replay the known-bad case and read the class name — the repair is real when the known-bad case fails specifically as `REGISTRY_RUNTIME_CONTENT_DRIFT`, with zero mutations on the verify-only path, instead of a bare `AssertionError`.

### SN-0533 — Fingerprint the Bytes Before You Prove Them — the Checkout Is an Instrument Too [audit: PARTIAL → lost element restored]

Before running any test in a verification battery: pin the tip via the refs API, pull the codeload tarball at that exact SHA, and verify every file's size (or blob SHA) against the API — only then run. A local checkout or worktree is an instrument, and instruments corrupt silently. Proof executed on unfingerprinted bytes is a claim about unknown bytes: cite it as such, or don't cite it.

### SN-0633 — A Bulk Merge Can Hollow a Protected Document — the Field Battery Is the Acceptance [audit: PARTIAL → lost element restored]

Every bulk rewrite (consolidation, regen, index rebuild, mass repoint) closes only against a protected-document field battery run on the exact merged bytes — the full required-field set asserted on every protected document. The merge's own green (index `--check` OK, file counts, suite pass) proves presence, never intactness. The source case: PR #1229 merged green on 796 files while seven required governance fields vanished from SN-0359 — `lifecycle_state`, `intelligence.epistemic_state`, `uncertainty`, `intelligence.measurement_contract`, `intelligence.successor_effect`, the truth ceiling, and the ratification provenance — and only the protected-integrity field battery caught it.

---

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn0172-never-prewrite-done-records`
- `IB-SMART-NOTE-20260930-sn0125-verify-the-tree-after-push`
- `IB-SMART-NOTE-20260930-sn0188-search-index-stale-evidence`
- `IB-SMART-NOTE-20260930-sn0424-registry-metadata-is-not-runtime-proof`
- `IB-SMART-NOTE-20260930-sn0533-fingerprint-the-bytes-before-you-prove-them`
- `IB-SMART-NOTE-20260930-sn0216-verify-at-target-tree-not-at-artifact`
- `IB-SMART-NOTE-20260930-sn0219-deployed-not-built-walk-the-live-site`
- `IB-SMART-NOTE-20260930-sn0238-recompute-index-from-live-tree`
- `IB-SMART-NOTE-20260930-sn0384-validate-semantics-not-proxies`
- `IB-SMART-NOTE-20261008-sn0633-bulk-merge-hollows-protected-document`
- `IB-SMART-NOTE-20261004-sn0250-green-run-compatible-with-corrupt-registry`
