# NEXT NAYA BATON — Coda 2 → Coda 3 (round 2)

**Set by:** Coda 2 · **Branch:** `coda2/node-function-scorecard-2026-09-27` @ `dc19002c`
**Round 1 baton is COMPLETE.** All nine Nodes are now machine-typed; the lock passes. This is the next ball.

---

## 1. WHAT ROUND 1 ACHIEVED (verified, not claimed)

| | Before | After |
|---|---|---|
| Nodes with machine-typed decision outcomes | 4 / 9 | **9 / 9** |
| `build-node-function-lock.py` | `FAIL: 5 findings` | **`PASS`** |
| Contract diff | — | exactly 7 lines, all inside `## Outputs` |

`dc19002c`. Behavioural proof is still `NOT_PROVEN` for all nine — typing makes behaviour **checkable**, not **proven**.

## 2. CURRENT STATE

`main` = `62faa63b`. Nine Node contracts distinct and now typed. Node **objects** still templated. **No runtime on `main`** (0 `.ts`, 0 migrations, `supabase/` absent since `b31f37fd`; recoverable from `b31f37fd~1`).

**`main` is RED — 2 failed, 18 passed.** Pre-existing, caused by two unparseable canonical kernel files.

## 3. THE ONE NEXT ACTION

**Derive the Node machine objects from the function lock, closing the 9/9 fidelity gap.**

Measured precisely:

```
NODE     LOCK IN  OBJ IN  LOCK OUT  OBJ OUT  FIDELITY
SELF        5        8        5         6       MISMATCH
LAW         6        8        7         6       MISMATCH
ACT         5        8        5         6       MISMATCH
KNOW        5        8        5         6       MISMATCH
PROVE       5        8        5         6       MISMATCH
CONNECT     4        8        5         6       MISMATCH
VERIFY      5        8        5         6       MISMATCH
LEARN       5        8        5         6       MISMATCH
EVOLVE      5        8        5         6       MISMATCH

nodes whose machine object contradicts its own contract: 9/9
```

**Every Node object still carries 8 generic inputs and 6 generic outputs while its contract declares 4–7 specific ones.** A runtime loading the object today gives all nine Nodes identical behaviour — which is exactly the problem round 1 identified.

Exactly what to do:
1. Write `BRAIN/12-ENGINEERING/build-node-objects.py`. It reads `BRAIN/03-KERNEL/NODE-FUNCTION-LOCK-V1.json` and regenerates each `BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-KERNEL-{NODE}.json` `ai_view` from the lock. **Generated, never hand-edited** — that is what makes fidelity permanent.
2. Preserve the object's non-`ai_view` fields (`object_id`, `canonical_status`, `machine_view`, `provenance`, `proof`, `relationships`, `successor_effect`). Only `ai_view.inputs`, `ai_view.outputs` and `ai_view.failure_mode` are derived.
3. Make the failure-mode string **per-Node**, derived from that Node's own failure states. Today all nine share one identical string — that is the single most damaging templating left.
4. Run `python BRAIN/12-ENGINEERING/verify-node-function-scorecard.py`.

**Success:** `MISMATCH` count `9/9` → `0/9`, distinct `failure_mode` `1` → `9`, and the scorecard's `FIDELITY` column reads `OK` for all nine.

**Evidence:** the scorecard table itself, plus `--check` proving generated objects match the lock.

## 4. WHAT NOT TO DO

- Do **not** hand-edit the nine object files. Generated-from-lock is the whole point; hand edits restore the drift.
- Do **not** change `canonical_status` or `proof.behavioral_status`. Those stay `CANDIDATE` / `NOT_PROVEN` until a runtime proves otherwise.
- Do **not** mint an Intelligent Block id. Only the canonical receiver may, and it is not on `main`.
- Do **not** run the NAYA-NODE-0001 race; `0028` §4 bars it until `0027` is merged.
- Do **not** relax a gate to make it green.

## 5. BRANCHES YOU INHERIT

| Branch | Commit | Note |
|---|---|---|
| `coda2/brain-foundation-aaa-2026-09-27` | `b8d4daaf` | **Merge first.** Fixes main's 2 red tests + 2 unparseable files. |
| `coda2/node-function-scorecard-2026-09-27` | `dc19002c` | This one. Function lock + typed vocabularies + scorecard. |
| `coda2/collective-intelligence-chain-readiness-2026-09-27` | `e4740625` | 11-link chain measured at **1/11**. |
| `coda2/constitutional-authority-fail-closed-2026-09-26` | `8ddcd854` | Precedence recorded, fail-closed. |
| `coda2/nine-node-conformance-truth-2026-09-27` | `092b71be` | 28 controls on kernel binding + semantic fork. |

## 6. AFTER SUCCESS

When fidelity is closed, the machine layer is finally faithful to the contracts. Then the frontier is **behavioural**, and it needs a runtime:

1. Merge `b8d4daaf` so `main` is green.
2. Get the Director's decision on `b31f37fd` (clean start, or restore from `b31f37fd~1`).
3. With a runtime, prove one Node end to end: `LOADS -> INVOKES -> INFLUENCES -> APPLIES`.
4. `VERIFY-Node` first — it has the richest typed vocabulary (`outcome_status` + `acceptance_decision`) and is the natural first behavioural proof.

## 7. VERIFY

```bash
python BRAIN/12-ENGINEERING/build-node-function-lock.py --check     # PASS today
python BRAIN/12-ENGINEERING/verify-node-function-scorecard.py       # your action
python -m pytest tests -q                                          # 2 red until b8d4daaf merges
```

## 8. THE DISCIPLINE THAT MATTERS

Round 1 I reported two false findings from bad regexes and truncated output, and corrected both in public. The contracts were fine both times. **Re-read the source before trusting any tool output — including mine, and including a green gate.** A gate that only says green is the failure mode this whole system exists to prevent.
