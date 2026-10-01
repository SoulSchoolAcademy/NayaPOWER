# Cold-Successor Retrieval & Continuity Protocol V1

**Seat:** Coda 4 · **Human Director:** Shawn Vibert (final authority)
**Scope:** successor restoration, applicability, reconstruction, later reuse
**Not in scope:** `naya_kernel/**`, `kernel/**`, persistence adapters,
migrations, calculator conformance (Coda 1), execution/handoff failure testing
(Coda 2), spec qualification (Coda 3).

**Exact revisions (verified live, not inherited):**

| Ref | SHA | State |
|---|---|---|
| `main` | `a726a8376559609a3620f948ec7bfcabdba50abb` | current |
| PR #1216 base | `a726a8376559609a3620f948ec7bfcabdba50abb` | current |
| PR #1216 head (CS-01 first published against) | `f58adf0826e0ea2c96d6e4a781b5191d2f4b8d5b` | superseded |
| PR #1216 head (CS-01 re-reproduced at) | `4e87d4a5810f6b0b5b72e254f3d37ddf69826c87` | **draft, unmerged — current tested** |

#1216 is an open **draft**. Nothing here is production proof.

The four commits added between those two heads (`a78227d8`, `9a21efda`,
`71c14f0a`, `4e87d4a5`) are the red→green hardening, the SELF tamper refusal,
the EVOLVE calculator gate, and the `inputs_hash` binding. CS-01 was
re-reproduced in a clean worktree at `4e87d4a5`, so it is not stale.

**Receipt contract status.** Naya 2's `naya-receipt-contract/1` proposal was
**withdrawn** in #554 comment `5934656876` as a competing format, after the
canonical `NAYANODE/0101-PERSISTENCE-CONTRACT-V1.md` was read. Naya 2 then
answered Naya 4's seam question in `5934779683`: the kernel keeps emitting its
native receipt unchanged, and the canonical 12-field contract stands. So
`naya-receipt-contract/1:PROPOSED` is **not** the live interface. This protocol
therefore consumes receipts in their native kernel shape and names no
competing format.

---

## 0. The contract this executes

Not an invented bar — the cold-successor clause already in the package:

- `COLD-GITHUB-BOOTSTRAP-ACCEPTANCE-V1.md` §*Cold-successor acceptance*: ten
  questions; *"Success requires durable-state reconstruction and
  evidence/claim distinction."*
- `INTELLIGENCE/CONTINUITY.md`: *"Continuity is behavioral… A document saying
  continue here is not proof."*
- `INTELLIGENCE/LEARNING.md` §*Acceptance*: a later authorized Naya must obtain
  the lesson without the predecessor handing it over, recognize applicability,
  change behavior, and leave evidence.
- `NAYANODE/00-KNOW-MASTER-CONTRACT-V1.md` acceptance item **13**: *"cold
  successor can continue without hidden reconstruction."*
- `SOURCE-PRECEDENCE-...-2026-09-29.md:86` already names this as the next action.

## 1. Existing seams only — no new store

| Step | Existing callable seam |
|---|---|
| decision | `Kernel.decide(state)` — `naya_kernel/kernel.py:338` |
| receipt verify | `verify_decision_receipt(receipt)` |
| kernel continuity | `Kernel.cold_reconstruct(receipts)` — `kernel.py:479` |
| durable knowledge | `KnowNode.cold_reconstruct(receipts)` — `know_node.py:1362` |
| governed retrieval | `KnowNode.retrieve(query, principal)` |
| provenance | `KnowNode.cite_provenance(block_id)` |
| handoff seal | `EvolveNode.build_successor_package(fields)` — `evolve_node.py:1212` |
| successor boot | `SelfNode.gate(state)` w/ `successor_package` — `self_node.py:243` |

Receipts are the persistence medium. The predecessor writes receipts; the
successor reads receipts only.

## 2. Isolation honesty — corrected

This is **object-level isolation inside one process**: fresh node objects,
receipt-only inputs, no builder conclusions passed to the successor.

It is **not** process-level isolation. Process-level isolation requires a
separate OS process, which is §7 and is **not yet built**. It is not a fully
independent cold agent; the harness is mine and known to me.

## 3. Defect CS-01 — BLOCKS cold-start restoration

**Reproduced at both `f58adf08` and `4e87d4a5`.**

`KnowNode.cold_reconstruct` rebuilds into a **local** `fresh = KnowNode()`
(`know_node.py:1372`) and never installs it on `self`. Measured at `4e87d4a5`:

```
REPORTED restored_block_count : 1
REPORTED store_hash           : 71d1ce8361027a81
PRODUCER live _store_hash()   : 71d1ce8361027a81
hashes equal                  : True
ACTUAL successor.blocks       : 0
ACTUAL successor._hash_index  : 0
ACTUAL retrieve() blocks      : []
```

The report is accurate about the *rebuilt* store and silent about the *node*.
A caller that trusts the report gets a green restore and an empty node.

**Governing contract:** §10 of the KNOW cold-reconstruction procedure
(`know_node.py` docstring) requires *restore → replay → re-derive indexes →
provenance_audit → RESTORE receipt*. Re-deriving indexes into a throwaway local
does not leave the node restorable, so `provenance_audit`, `retrieve`,
`cite_provenance`, supersession and contradiction are all unreachable after a
cold start. Contract item 13 (*"cold successor can continue"*) cannot hold.

**Expected public behavior:** after `cold_reconstruct(receipts)`, the node's own
public operations — `retrieve`, `cite_provenance`, `provenance_audit`,
`invalidate`, `contradict` — operate on the restored state.

**Minimal reproducer:** `repro_cs01.py` (posted with the #1216 handoff).
Ingest one block in a producer, `cold_reconstruct([receipt])` in a successor,
print `report["restored_block_count"]` against `len(successor.blocks)`.

**Not fixed here.** `naya_kernel/` is Naya 4's lane. Two dictionaries may or may
not be sufficient: receipt sequencing, lifecycle state, supersession links,
contradiction lists and integrity indexes all have to be reconciled by the
owner. The repair acceptance list is in the #1216 handoff.

**Naya 4's existing `test_act_to_know_handoff_write_and_retrieve` asserts the
hash but never retrieves from the reconstructed node** — an untested seam, not a
test bug.

## 4. Behavioral-reuse predeclaration (pre-run, fixed)

| Field | Value |
|---|---|
| Lesson id | `PROV-BEFORE-APPLY-1` |
| Applicable task | cite provenance before treating a retrieved block as current truth |
| Expected observable behavior | a real citation call resolving to the recorded source, recorded **before** any application through an authorized seam |
| Unrelated-task control | a second lesson must not be credited as the applied one |
| Authority requirement | none — retrieval and citation are read-only; consequential action is refused |
| Success | cited-then-applied on the applicable task; not attributed on the control |
| Failure | applies without citing; cites the control lesson; treats retrieval as permission; reports production |

**No causal-improvement claim.** No A/B was run; access to the intelligence was
not varied against a held task. Correcting an earlier draft of this protocol: a
single run demonstrating retrieval and citation is **not** evidence of improved
performance.

## 5. Proof-language corrections (per coordinator review)

Corrections applied to this protocol and its tests:

1. **No test-authored booleans as behavior.** An earlier helper set
   `applied=True` after a citation call. That credited a test flag, not runtime
   behavior. Renamed: the trace reports `cited` / `citation_resolved_to` /
   `application_attempted`, and no helper asserts on a flag it set itself.
2. **Attribution ≠ refusal.** Distinct block IDs show the control resolves
   separately. They do **not** show unrelated-task refusal. Refusal and
   applicability decisions belong to CONNECT and PROVE; this protocol does not
   invent a substring applicability engine.
3. **Derived, not hardcoded.** Source revision, proof status, blockers and next
   action are read from preserved artifacts. A kernel version string is not a
   source SHA.
4. **Object-level, not process-level** isolation (§2).
5. **Partial acceptance stays visible.** CS-01 tests are `xfail(strict=True)`
   with the assertion constrained to the reproduced defect, so an unrelated
   harness error cannot masquerade as the known failure. Markers are removed
   only after the owner's repair is independently accepted.

## 6. Steps

1. **Decide** — `Kernel.decide`; keep the decision receipt.
2. **Execute + persist** — ACT `execute()` → KNOW `ingest()`; keep receipts.
3. **Restore** — fresh `KnowNode.cold_reconstruct(receipts)`, then `retrieve`.
   **BLOCKED at the retrieve step by CS-01.**
4. **Reconstruct** — derive current revision, proof state, blockers, next
   action from preserved artifacts, labeling VERIFIED / CANDIDATE / UNKNOWN.
5. **One next action** — read from the sealed successor package; confirm it and
   state its verification and preservation route. Not executed: no authority is
   transferred.
6. **Negative controls** — stale evidence, unrelated lesson, authority
   inheritance, unverified learning, missing evidence, production overclaim.
7. **Preserve** — successor writes its result through the existing seam.
8. **Second cold reader** — a fresh reader reconstructs the improved state.

Steps 3, 4 and 8 depend on CS-01 and are **blocked**, not met.

## 7. Cross-process restoration (next, after CS-01 closes)

- **Process A** — producer operations + receipt serialization → a safe temp
  evidence bundle, with hashes and exact source recorded; then exit.
- **Process B** — separate interpreter, same frozen candidate source. Receives
  the artifact path and canonical source pointers only — no predecessor node
  objects, no hidden answers. Restores, retrieves, validates through public
  interfaces. Requires: same admissible content and provenance; **actual**
  retrieval from the restored node; no authority inherited; governing failure on
  missing or tampered evidence; one bounded authorized operation with
  independently observable output.
- **Process C** — recovers a **new** result from B. Rereading A's unchanged
  receipts is not an improved-state cycle.

This proves local cross-process continuity only. It does not prove database
persistence, production readiness, independent-agent reasoning, or causal
improvement.

## 8. Five labels kept separate

| Label | Requires | Status |
|---|---|---|
| Document recovery | successor reads files | PROVEN |
| Object-level restoration | fresh objects rebuilt from receipts, hash-verified | **PARTIAL — CS-01 blocks usable state** |
| Process-level continuity | separate OS process, public interfaces only | **NOT BUILT** (§7) |
| Behavioral reuse | preserved lesson changes observable behavior | NOT CLAIMED — see §4 |
| Causal improvement | controlled A/B, only intelligence varies | **NOT CLAIMED** |
| Production proof | ratified, merged, deployed, runtime-observed | **NOT CLAIMED** |

## 9. Reproduce

```powershell
git clone --branch coda4/cold-successor-continuity https://github.com/SoulSchoolAcademy/NayaPOWER.git
cd NayaPOWER
git config core.autocrlf false       # required; see W-1
git checkout -q -- .                 # required: core.autocrlf alone does NOT
                                     # rewrite already-checked-out files
python -m pytest tests/test_nodes/test_coda4_cold_successor.py -q
python -m pytest tests/test_ci_declares_test_dependencies.py -q
python CODA-4/repro_cs01.py          # exit 1 == CS-01 present, 0 == repaired
python CODA-4/make_evidence.py       # write evidence receipts
python CODA-4/make_evidence.py --verify   # re-verify their self-consistency
```

Artifacts:

| File | Role |
|---|---|
| `tests/test_nodes/test_coda4_cold_successor.py` | 22 cases: 20 pass, 2 xfail |
| `CODA-4/repro_cs01.py` | standalone minimal CS-01 reproducer |
| `CODA-4/make_evidence.py` | evidence-receipt writer / verifier |
| `CODA-4/evidence/*.json` | 6 receipts, each SHA-256 sealed over its own body |

The receipts record the tested SHA, command, stdout tail, and exit code. A receipt
whose body was edited to claim success is caught: I rewrote the CS-01 receipt's
`exit_code` to `0` and `--verify` reported `TAMPERED`, exit 1. That is the property
that matters here — a receipt in this lane must not be able to claim a green
restore, which is the exact failure CS-01 demonstrates.

**Not full acceptance.** On the current candidate the expected result is
**20 passed, 2 xfailed**, and both xfails are CS-01. A green-looking total here
means CS-01 is still open — the pass count is not the acceptance signal, the
xfails are. They will XPASS (and fail the run under `strict=True`) once the
repair lands, at which point the markers must be removed and §7 started.

The count changed from an earlier **16**, then **18**, to **20** as the
proof-language corrections of §5 added cases. The reconciliation: the original
16 passed; renaming the trace helper and splitting derivation added one; the
omission/UNKNOWN control added one; the exact CS-01 signature pin added one;
and the reconstruction test was split into a derivation test plus a falsifiability
control. Only the current **20 / 2 xfail** is claimed.

**The xfails are constrained, not blanket.** `pytest.raises(AssertionError,
match=...)` guards pin the exact failure text in the non-xfail signature test,
and mutation checks confirm a harness break surfaces as a hard failure rather
than hiding inside an xfail:

| Injected break | Result |
|---|---|
| wrong stage set (decide cannot PASS) | **14 failed**, exit 1 — constraint HELD |
| reconstruction input key wrong | **2 failed**, exit 1 — constraint HELD |

## 10. Human reading of the demonstration

Scope this carefully, because "preserved" is doing a lot of work. **No receipt
has been written to disk in this protocol yet.** Receipts exist as the runtime's
own in-memory objects, produced and consumed through the real seams in one
process. Serializing them to a file is §7 and is **not built**. So this is
*object-level* restoration of preserved receipts, not durable restoration.

> **The task.** One cold successor must recover preserved work.
> **What Naya used.** Receipts from the real ingest seam, in memory. Nothing
> else — no builder conclusions, no successor-package answers, no hidden state.
> **What she did.** Rebuilt state from those receipts, hash-checked it, then
> tried to retrieve through the governed seam.
> **The verified result.** The report is green and the hash matches the
> predecessor exactly — and the node is empty. Nothing was retrievable.
> **What the next Naya recovered.** The blocker itself, which is the most useful
> thing this protocol produced. A receipt that reports success over an unusable
> store is worse than a failure, because it is believed.

**Evidence receipts.** `CODA-4/evidence/` holds machine-checkable JSON produced by
`CODA-4/make_evidence.py`. Each receipt records the exact tested SHA, the command,
the captured stdout, the exit code, and a SHA-256 over its own body, so a later
reader can re-derive rather than trust. They are **observations of this run**, not
a substitute for §7 and not a durability claim.

## 11. Windows findings

### W-1 — CRLF breaks the ratified calculator pin

Keep the integrity check intact; do **not** normalize bytes inside the verifier.

| Fact | Value |
|---|---|
| OS | Windows (PowerShell 5.1) |
| Git | 2.55.0.windows.5 |
| Python | 3.13.15 |
| `core.autocrlf` | `true` (Git-for-Windows default) |
| `.gitattributes` | **absent at repo root** |
| Git blob at HEAD | `cac79b6595ca651d8a110b71f25fff9fe50e67bc` (== ratified pin) |
| Worktree bytes | 34551 B, 816 CRLF pairs |
| Blob of worktree bytes | `4cb941b2264fb61ccb4706f320a628984c0c6a2b` |
| Blob after LF normalization | `cac79b6595ca651d8a110b71f25fff9fe50e67bc` |
| Effect | `v21_executable_status()` → MISMATCH → EVOLVE refuses to score |
| Suite at CRLF checkout | `test_kernel_handoff_integration.py` → 2 failed, 5 passed |
| Suite after `core.autocrlf=false` + re-checkout | 7 passed |

Content is byte-identical after LF normalization, so this is not calculator
tampering — it is an unspecified checkout-byte question. **Narrow recommendation
to Naya 4:** add a `.gitattributes` making `*.py` (or at least
`kernel/value_calculus.py`) `text eol=lf` so the pinned blob is checkout-stable,
or have the verifier hash the git-normalized form explicitly and document it.
`core.autocrlf=false` alone does not rewrite already-checked-out files — a
re-checkout is required, as measured above.

### W-2 — Windows suite failures, precisely classified

Not dismissed as pre-existing, and not all the same cause. Measured on the Coda 4
branch, same interpreter, same worktree, two modes:

| Run | Result |
|---|---|
| `python -m pytest -q` | **7 failed, 1034 passed, 3 skipped, 2 xfailed** |
| `python -X utf8 -m pytest -q` | **2 failed, 1039 passed, 3 skipped, 2 xfailed** |

**Cause A — environment encoding, 5 of the 7 (fixed by `-X utf8`).**
`tests/test_smart_note_v2.py` reads repository files with
`Path.read_text()` and **no `encoding=` argument**, so Python uses the Windows
ANSI code page (`cp1252`):

```
capture = json.loads((ROOT / ".naya/capture/...json").read_text())
rendered = path.read_text()
-> cp1252.IncrementalDecoder
-> UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 2994
```

That is the precise failing read. It is an encoding-environment artifact, not
project behavior: the same 5 pass under `-X utf8`. The narrow fix is
`read_text(encoding="utf-8")`, i.e. make the encoding explicit rather than
inherit it. Not this seat's file; reported, not patched.

**Cause B — real Windows path behavior, 2 survivors under `-X utf8`.**
These are not encoding artifacts and are not dismissed:

1. `tests/test_smart_note_v2.py::test_projection_generator_targets_brain_and_preserves_private_default`
   asserts `str(mod.BRAIN_SMART_NOTE_ROOT).endswith("BRAIN/05-MEMORY/SMART-NOTES")`
   — a **forward-slash** literal. On Windows the value ends with
   `...\BRAIN\05-MEMORY\SMART-NOTES`, so the assertion fails on path separators.
   A test asserting a POSIX separator is not portable; `Path(...) == ...` or
   `os.sep`-aware comparison is.
2. `tests/test_brain_registry.py::test_brain_population_rejects_node_relationship_drift`
   fails inside `shutil.copytree(root / "BRAIN", tmp_path / "BRAIN")` with
   `[WinError 3] The system cannot find the path specified` on long
   `IB-SMART-NOTE-*.md` paths. That is the Windows path-length limit
   (`MAX_PATH`, 260 chars) under a pytest temp directory, combined with the
   deep `SMART-NOTES/<Y>/<M>/<D>/<ORG>/<CHART>/SN-NNN/` layout. Not an encoding
   issue.

Owner of both files is not this seat. Reported with the exact read and the exact
assertion so the owners can fix them rather than re-classify them.

**Baseline comparison** (`git stash -u`, identical interpreter): **7 failed,
1014 passed, 3 skipped** — the same 7, so none of the above were introduced by
this branch. The 18-pass difference is entirely this protocol's own tests.

## 12. Remaining acceptance failures

| # | Item | State |
|---|---|---|
| 1 | Cold-start **retrieval** (CS-01) | **BLOCKED** — Naya 4 |
| 2 | Process-level restoration (§7) | NOT BUILT |
| 3 | Second cold reader recovering a **new** result | NOT BUILT |
| 4 | Behavioral reuse via an authorized application seam | NOT CLAIMED |
| 5 | Causal improvement | NOT CLAIMED — no A/B |
| 6 | Production proof | NOT CLAIMED — #1216 draft |
