# NEXT NAYA BATON — Coda 2 → Coda 3

**Set by:** Coda 2 · **Set at:** `origin/main` `127e8b50` base, work on `coda2/node-function-scorecard-2026-09-27`
**Protocol:** You are the **executor**. When you finish, you become the **setter** and write a baton of equal or greater quality. The baton is not a courtesy — a weak baton is how work dies.

---

## 1. CURRENT STATE

`main` = `62faa63b`. Working tree: `BRAIN/` (15 domains, contracts + machine artifacts), `KNOWLEDGE/` (15 prose concept files), `NAYANODE/` (29 specs), `kernel/` (loader + value calculus), `verification/`.

**Measured on `main`, not assumed:**
- 9 Node contracts exist, are distinct, and are genuinely specific: 4–6 inputs, 5–6 MUST, 5–6 MUST NOT, 5–6 acceptance criteria, 4–5 failure states each.
- 9 machine-readable Node objects exist but are **one template across all nine** — 1 distinct `failure_mode`, 1 `successor_effect`, 1 input tuple, 1 output tuple (9/9 identical each).
- `kernel/brain_registry.py` validates the population; tests pass.
- **No runtime.** `supabase/functions/*` = 0, `supabase/migrations/*` = 0, all `.ts` on main = 0, `NAYANET/` `SUPERBRAIN/` `scripts/` absent. Removed by `b31f37fd`; recoverable from `b31f37fd~1`.

## 2. CURRENT AUTHORITY

Human Director is sovereign. Two decisions are **yours to make, not ours to assume:**
1. Whether `b31f37fd` was an intended clean start or the runtime should be restored.
2. Constitutional precedence (`0027` unmerged, commit `fc63402c8` on `naya/value-calculus-canonical-v1`).

**Do not self-authorize either.** If you reach them, leave the baton and prove the boundary.

## 3. WHAT IS PROVEN / NOT PROVEN

| Claim | State |
|---|---|
| Node contracts are specific and distinct | **PROVEN** — read and measured |
| Node machine objects are a shared template | **PROVEN** — measured 9/9 identical |
| `main` has a runtime | **FALSE** — measured 0 files |
| Any Node influences runtime behaviour | **NOT PROVEN** — all 9 `behavioral_status: NOT_PROVEN` |
| Collective Intelligence Chain | **1/11 links satisfied** — measured, not simulated |

## 4. BRANCHES YOU INHERIT (all pushed, none merged)

| Branch | Commit | What it does |
|---|---|---|
| `coda2/brain-foundation-aaa-2026-09-27` | `b8d4daaf` | **Merge this first.** Main is RED: 2 tests fail, 2 canonical kernel files are unparseable. Fixes both; adds 11 integrity tests. |
| `coda2/collective-intelligence-chain-readiness-2026-09-27` | `e4740625` | 11-link chain as a measured readiness contract + 7-control gate |
| `coda2/node-function-scorecard-2026-09-27` | `33fe35a9`→`a5630801`→`b0620afe` | Per-Node scorecard + the derived function lock |
| `coda2/constitutional-authority-fail-closed-2026-09-26` | `8ddcd854` | Constitutional precedence + fail-closed authority gate |
| `coda2/nine-node-conformance-truth-2026-09-27` | `092b71be` | Kernel binding + semantic-fork gates, 28 controls |

## 5. THE ONE NEXT ACTION

**Author machine-typed decision vocabularies for the five untyped Nodes: `SELF`, `ACT`, `KNOW`, `CONNECT`, `EVOLVE`.**

Exactly what to do:
1. Read each contract: `BRAIN/03-KERNEL/NODES/{NODE}/0001-CONTRACT.md`. Take its `## Outputs` and `## Failure States`.
2. Derive the decision vocabulary **from that contract only.** Do not invent behaviour. Each Node's outputs already imply its states — e.g. ACT's outputs (`Plan`, `Action`, `Execution state`, `Observation target`, `Proof requirement`) imply an execution-state enum; CONNECT's (`Relevant intelligence set`, `Applicability assessment`, `Freshness indicators`, `Reconciliation context`) imply an applicability enum.
3. Add the vocabulary in the same inline form the other contracts already use — `Label (A, B, C)` inside an output line, or one typed value per output line (LAW's form). Both are already supported by the extractor.
4. Re-run: `python BRAIN/12-ENGINEERING/build-node-function-lock.py --write`
5. **Success = `FAIL: 5 node-function lock finding(s)` becomes `PASS`.** That is the whole acceptance test.

**Evidence to obtain:** the command output, showing `decision=N` for all nine rows.
**Where:** `BRAIN/03-KERNEL/NODES/{NODE}/0001-CONTRACT.md` on your own branch.
**If it fails:** the extractor is strict on purpose — read its `Form A` / `Form B` patterns rather than loosening the gate.

## 6. WHAT NOT TO DO

- Do **not** mint an Intelligent Block id locally. Only the canonical receiver may allocate identity, and it is not on `main`.
- Do **not** run the NAYA-NODE-0001 race. `0028` §4 bars it until `0027` is satisfied.
- Do **not** simulate the Collective Intelligence Chain. A simulated PASS on the ultimate acceptance test is worse than a red board.
- Do **not** restore `b31f37fd~1` without the Director. It is 2,917 files and would collide with the whole clean start.
- Do **not** relax a gate to make it green. Every gate here has negative controls for exactly that reason.

## 7. AFTER SUCCESS

Once all nine are typed, the next frontier is the **machine-view fidelity** gap: the Node objects still carry 8 generic inputs and 6 generic outputs that contradict their own contracts. Derive the object `ai_view` from the lock so fidelity gaps close permanently, and extend `verify-node-function-scorecard.py` to fail when an object diverges from the lock.

Then write your baton. Name the exact next Node-level blocker, the exact command, and the exact success string — as this one does.

## 8. VERIFICATION YOU CAN TRUST

```bash
python -m pytest tests -q                                              # green baseline
python BRAIN/12-ENGINEERING/build-node-function-lock.py --write        # your action
python BRAIN/12-ENGINEERING/verify-node-function-scorecard.py         # fidelity + distinctness
python BRAIN/12-ENGINEERING/verify-collective-chain-readiness.py      # 1/11 today
python BRAIN/12-ENGINEERING/verify-brain-machine-conformance.py       # after merging b8d4daaf
```

Every one of these fails closed and has controls. A gate that only says green is worthless here.

## 9. ONE LAST THING

Two of my own reports this session were wrong and I corrected both in public: "three competing relationship vocabularies" (truncated output) and "0 MUST rules" (bad regex). The contracts were fine both times. **Re-read the source before you trust any tool output — including mine.**
