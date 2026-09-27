# CODA 1 — ULTIMATE INTELLIGENCE EVALUATION BATTERY: RESULTS

**Tester:** Coda 1
**Date:** 2026-09-26
**Source HEAD at test time:** `39adb00e5` (local `main` worktree `C:\Users\Admin\NayaPOWER`, tracking `origin/main`)
**Testing standard applied:** No answer was accepted as "implemented", "supported", "the field exists", "should work", or "appears to work". Every verdict below is anchored to a command that was run, a file that was read, or a run ID that was inspected. Where I could not produce evidence, the verdict is `UNTESTED` or `BLOCKED` — never `PASS`.

---

## 0. SELF-CORRECTION LOG (required by the test brief)

I nearly filed a **false FAIL** on Test IX. I asserted that
`.naya/runtime/verify_cold_applicability_action_outcome_learning.py` was circular because it
`json.loads` a static proof file and asserts the booleans inside it. Before publishing I checked
whether that file was hand-authored, and it is **not**:

```
schema  = NAYANET_SMART_NOTE_COMPOUNDING_LOOP_PROOF_V1
status  = VERIFIED
workflow_run = 35893121151
workflow_job = 107290247494
source_head  = 833bf8f9473528b7d53ad17636679e0f766bb8ef
evidence.event_id / evidence_id / receipt_id / owner_id = present
```

and `.github/workflows/verify-cold-applicability-action-outcome-learning.yml` both generates and
runs it. The verdict below is therefore narrowed to what the evidence actually supports. A tester
who files a false FAIL is as dangerous as a coder who files a fake PASS.

---

## 1. SUMMARY SCORECARD

| # | Test | Verdict | One-line reason |
|---|---|---|---|
| I | Nine Kernels — identity | **NOT ADMINISTRABLE** | No authoritative nine-kernel definition exists in the repository |
| II | Nine Node | **UNTESTED** | Depends on Test I, which cannot be administered |
| III | Node-to-Node intelligence | **FAIL** | Relationships are hand-declared in source, never discovered |
| IV | Brain | **PARTIAL** | Retrieval returns *everything*; no applicability reasoning demonstrated |
| V | Action | **PASS** | Prediction → action → predicted evidence → reality matched (live) |
| VI | Verification under bad evidence | **PARTIAL** | Error advanced correctly, but recorded state lagged reality |
| VII | Self-optimization | **PARTIAL–STRONG** | Real paired-run/counterfactual infrastructure exists |
| VIII | Self-organization | **FAIL** | Quarantine detected contamination and then left it orphaned |
| IX | Learning | **PARTIAL** | Real provenance-backed reuse proven; no before/after performance delta |
| X | Compounding | **UNTESTED** | Requires 3 Naya generations; not run |
| XI | Cold Naya | **PARTIAL (passes letter, fails spirit)** | 14/14 "PASS" while 1 answer is a pointer and control plane was RED |
| XII | Adversarial | **PARTIAL** | Detection proven; remediation not proven |
| XIII | Self-awareness | **FAIL** | Prose protocol only; no machine-readable diagnostic layer |
| XIV | Killer test / 20 questions | **PARTIAL** | One real demonstration exists; covers persistence, not learning/compounding |

**Passed with real evidence: 1 of 14. Partial: 7. Fail: 3. Not admin./untested/blocked: 3.**

The system is not "fake intelligence." It is **real storage with unproven cognition.** That
distinction is the single most important result of this battery.

---

## 2. EVIDENCE MATRIX (schema as specified in the brief)

### Test V — ACTION TEST ✅ PASS

| Field | Value |
|---|---|
| **Capability** | Diagnose a broken governed boundary, repair it minimally, release it, and prove the real journey |
| **Input** | Live read-only probe of `https://sparkling-shape-7ae5.smartnetpodcast.workers.dev` + `NAYANET/HUB/public/assistant-runtime.js:178`, `hub-completeness.js:28` |
| **Process** | Proved `/identity.html` did not exist in-repo; proved live `/identity.html` returned HTTP 200 / 849643 bytes / Hub title (SPA fallback); concluded redirect loop; added `NAYANET/HUB/public/identity.html` calling the one existing adapter `establish()`; wired it into the governed release; added a live gate that fails the release if the fallback returns |
| **Output** | PR #795 → `8d7ee8487`; release run `36262036641` success |
| **State** | Live `/identity.html` byte-identical to `origin/main` (`4c894763…`, 7285 bytes); live `/` byte-identical (`ece07167…`) |
| **Evidence** | `IB-001223` (receiver-issued, not guessed), event `546d7a37-b155-43c4-9e48-4ba255c093d5`, receipt `4841cd24-0758-4ebe-8ac5-523c01759de4`, projection run `36262371595`, Smart Link present on `main` at `.naya/memory/smart-notes/2026/09/26/system/front-door-live/IB-001223/smart-note.md` |
| **Outcome** | Real sign-in → capture → Feed → authorized retrieval → `/hub?ib=IB-001223` renders → re-renders after reload. `LIVE_JOURNEY_PROOF: PASS` |
| **Learning** | PostgREST resolves RPC by argument name; SPA `not_found_handling` silently converts a missing route into a fake success |
| **Compounding** | Receipts + activity waves written so a successor inherits the reasoning, not just the diff |
| **Continuity** | Reproducible cold from the repository alone |
| **Failure** | `Verify Naya Understanding Fidelity` fails on `main` too: `No module named pytest` in the runner. Pre-existing, not caused by this work |
| **Improvement** | Route the orphaned front-door test into a workflow; it exists but no workflow runs it |
| **Verification** | Independent byte-parity probe, not the workflow's own check |
| **What we learned about the system** | It can be trusted to keep a promise once a machine check exists. It had no machine check for its own front door, so it was confidently broken for an unknown period |

### Test I — NINE KERNELS ❌ NOT ADMINISTRABLE

| Field | Value |
|---|---|
| **Capability claimed by the brief** | Nine kernels, each with distinct capability, owned state, and prohibited decisions |
| **Input** | `git grep -il "nine kernel\|9 kernel\|kernel registry\|NINE-KERNEL"` across the whole repository |
| **Process** | Searched for any authoritative enumeration |
| **Output** | **Zero results.** The word "kernel" appears across ~140 files with no governing definition of the set |
| **State** | Unchanged |
| **Evidence** | `git grep` returned no file; no `.naya/contracts/` artifact defines a kernel taxonomy |
| **Outcome** | The test cannot be run, because the subject does not exist as a declared structure |
| **Verdict** | **NOT ADMINISTRABLE.** This is a finding about the architecture, not about the tester |
| **What we learned about the system** | The system has strong *contract* surfaces and no declared *capability* taxonomy. Nobody can state what the nine parts of the brain are, so nobody can be held accountable for any of them |

### Test IX — LEARNING ⚠️ PARTIAL

| Field | Value |
|---|---|
| **Capability claimed** | Outcome → lesson → verified learning → changed future behavior |
| **Input** | `.naya/project-intelligence/2026-09-23-SMART-NOTE-COMPOUNDING-LOOP-PROOF.json`; `.naya/runtime/verify_cold_applicability_action_outcome_learning.py:23-26,39` |
| **Process** | The verifier loads the proof artifact and asserts `future_behavior_changed is True`, `learning_durable is True`, `learning_retrievable is True`, `successor_policy_created is True`, then reports `"status":"PROVEN_AT_EXISTING_PRODUCTION_PROOF_SCOPE"` with `"evidence":"future_behavior_changed=true"` |
| **Output** | `PROVEN` |
| **State** | `learner_state_version = 1`, `cold_reuse = true`, `authority_changed = false` |
| **Evidence** | Genuine: `workflow_run 35893121151`, `event_id 0c7bceeb-…`, `evidence_id f6b5310d-…`, `receipt_id 46d2ae5e-…` |
| **Outcome** | A cold context **did** reuse verified learning. That is real, non-trivial, and provenance-backed |
| **What failed or is uncertain** | Test IX demands tests A→B→C→D: same agent, problem A, experience outcome, learn, then a **different but related** problem B, measured. What exists is **one** generation of reuse. There is no before/after performance delta on a second problem. `future_behavior_changed = true` is a *recorded assertion inside a real run*, not a measured differential |
| **Verdict** | **PARTIAL.** Learning persists and is retrievable. That learning **changes performance** is asserted, not demonstrated |
| **What would make it better** | Run problem A and problem B against the same kernel with learning disabled vs enabled, and record both scores. Then `future_behavior_changed` becomes a measurement instead of a flag |

### Test X — COMPOUNDING ⛔ UNTESTED

| Field | Value |
|---|---|
| **Capability claimed** | Naya 1 → Naya 2 → Naya 3 measurably more capable without Shawn reconstructing context |
| **Blocker** | Requires three Naya generations scored on the same problem. Not performed |
| **Partial evidence** | Session 1 (front door) left receipts + activity waves. A later agent *can* inherit them. One generation demonstrated, not three |
| **What would make it possible** | One scored problem, run by three fresh contexts with no shared conversation, with per-generation scores recorded in the repository |
| **Verdict** | **UNTESTED — the most important untested claim in the system** |

### Test XI — COLD NAYA ⚠️ PASSES LETTER, FAILS SPIRIT

| Field | Value |
|---|---|
| **Input** | `python .naya/runtime/cold_successor_test.py`, zero conversational history |
| **Process** | Harness answers the 14 reconstruction questions from canonical sources |
| **Output** | `[PASS] ALL 14 QUESTIONS ANSWERED FROM CANONICAL SOURCES` — `Total: 14 / Proven: 11 / Current (Live Reconciliation Required): 1 / Active Next Action: 1` |
| **Evidence** | Harness output above |
| **What failed or is uncertain** | **(a)** One of the 14 is explicitly `Current (Live Reconciliation Required)` — it is *not* current, and the gate still reports PASS. **(b)** One of the 14 is `Active Next Action`, which is a *pointer*, not knowledge; counting it as an answer inflates the score. **(c)** The harness reported PASS while the repository's own `validate_control_plane.py` was **RED** with `MAP and BLOCK next actions disagree` — the cold Naya was passed a self-contradictory state and the gate did not notice |
| **Verdict** | **PARTIAL.** The continuity surface exists and is genuinely useful. The gate is too weak to be a mandatory gate, because it passes on a repo whose control plane disagrees with itself |
| **What would make it better** | The cold-Naya gate must fail when `validate_control_plane.py` is RED, and must not count a pointer as an answer |

### Test XII — ADVERSARIAL ⚠️ PARTIAL

| Field | Value |
|---|---|
| **Capability claimed** | Detect, quarantine, preserve evidence, prevent contamination becoming truth, recover, explain |
| **Input** | Two real adversarial mutations I executed against the conformance gate |
| **Process** | (1) Deleted a cited migration from a scratch tree → `CITED_PATH_MISSING x4`, `NEW_DRIFT=2`, exit 1. (2) Replaced `IMPLEMENTED ≠ VERIFIED` in the constitutional law → `CONSTITUTIONAL_EQUATIONS=5/6`, `CONSTITUTIONAL_EQUATION_MISSING x1`, exit 1 |
| **Output** | Both mutations detected, both non-zero exit |
| **Evidence** | Console output above, reproduced in `.github/workflows/verify-contract-registry-conformance.yml` as two standing adversarial steps |
| **What failed or is uncertain** | **Detection is proven; remediation is not.** The 2026-09-25 memory quarantine orphaned a conversation → intelligence entry that the control plane *still* references as unresolved in its own `next_action` more than a day later. No quarantine artifact exists under `.naya/memory/`. The system detected contamination and then took no action |
| **Verdict** | **PARTIAL.** Good detector, no demonstrated quarantine-and-recover loop |
| **What would make it better** | A quarantine action that must produce a receipt and either restore or explicitly retire the entry, with the `next_action` blocked until one of the two happens |

### Test XIII — SELF-AWARENESS ❌ FAIL

| Field | Value |
|---|---|
| **Capability claimed** | Machine-readable self-diagnostic: what is known, assumed, uncertain, weak, stale, repeatedly wrong |
| **Input** | Search for a self-diagnostic surface |
| **Process** | `Get-ChildItem -Recurse -Filter "*SELF-DIAG*"` and `git grep -il "self-diagnostic\|self_diagnostic\|SELF_AWARENESS"` |
| **Output** | Exactly one artifact: `.naya/2026-09-11-20-05-NAYAPOWER-38-SELF-DIAGNOSTIC-PROTOCOL.md` — prose, dated 2026-09-11, outside `.naya/contracts/` and outside the control plane. No machine-readable diagnostic exists. `.naya/control-plane/UNKNOWN-REGISTRY.json` is a partial, unrelated start |
| **Verdict** | **FAIL.** The system cannot currently report its own uncertainty in a form a program or a cold Naya can read |
| **What would make it better** | A generated `SELF-DIAGNOSTIC.json` next to `STATE.json`, produced by the same run that produces the report, listing known/unknown/assumed/stale with evidence pointers |

### Test VIII — SELF-ORGANIZATION ❌ FAIL

| Field | Value |
|---|---|
| **Capability claimed** | Reorganize messy intelligence into the structure it believes should exist, preserving provenance and uncertainty |
| **Input** | The live repository after the 2026-09-25 memory quarantine |
| **Process** | The system *did* restructure itself — a quarantine occurred and moved material under `.naya/memory/archive/legacy-pre-2026-09-25/` |
| **Output** | New structure created. `CURRENT-DAILY-PROJECT.json` now lives only in the archive; the live project path is absent |
| **Evidence** | `C:\Users\Admin\NayaPOWER\.naya\memory\archive\legacy-pre-2026-09-25\projects\CURRENT-DAILY-PROJECT.json` exists; the live equivalent does not |
| **What failed** | The reorganization **broke continuity**. `.naya/runtime/conversation_continuity.py:206` still reads `MEMORY / "projects" / "CURRENT-DAILY-PROJECT.json"` — a path the quarantine emptied. The system reorganized without checking which runtime depended on the structure it moved, and the orphaned entry is still unresolved in the canonical `next_action` |
| **Verdict** | **FAIL.** It discovered structure and paid for it with a broken dependency it has not acknowledged |
| **What we learned about the system** | Self-organization without a dependency impact check is not intelligence. It is reorganization |

### Test III — NODE-TO-NODE INTELLIGENCE ❌ FAIL

| Field | Value |
|---|---|
| **Capability claimed** | The system discovers that Node 2 refines/contradicts/complements Node 1, and that discovery changes retrieval, then reasoning, then action |
| **Input** | Examined how the Hub deep-link ↔ IB correspondence and the Smart Note ↔ IB relationship are established |
| **Process** | Both relationships are **hand-written** into workflow and contract source. The IB↔path correspondence is asserted by `.github/workflows/int001-smart-link-acceptance.yml` and `tests/int001/test_smart_link_verifier.py`, which test the correspondence *we specified*. `nayanet_compound-intelligence` exposes a `reconcile` action |
| **Output** | Verified correspondence — but of a relationship we declared |
| **Evidence** | `tests/int001/test_smart_link_verifier.py` (routed, passing) proves the rule holds. It does not prove the system *found* the rule |
| **Verdict** | **FAIL on the specific question asked.** "Did the system discover the relationship, or did we manually tell it?" — **we manually told it.** Every relationship in the chain is currently hand-declared |
| **What would make it better** | A test that hides the relationship and requires the system to infer it: give two nodes with conflicting `verified_at` and no declared link, and require the system to surface the conflict unprompted |

### Test VII — SELF-OPTIMIZATION ⚠️ PARTIAL–STRONG

| Field | Value |
|---|---|
| **Capability claimed** | Observe, measure, diagnose, propose, test against baseline, verify, promote, monitor |
| **Input** | `.naya/project-intelligence/COMPUTATION-EFFICIENCY-*` |
| **Output** | Six real artifacts: `CYCLE-A-BASELINE.json`, `CYCLE-B-RETAINED-REUSE.json`, `CAUSAL-PAIRED-RUN-2026-09-22.json`, `COUNTERFACTUAL-QUALIFIED-2026-09-22.json`, `COUNTERFACTUAL-REVIEW-2026-09-22.json`, `MEASUREMENT-CONTRACT.md` |
| **Evidence** | A genuine paired run against a baseline with a counterfactual review. This is the most methodologically serious work in the repository |
| **What is uncertain** | Whether the retained-reuse result changed anything downstream, and whether the counterfactual was actually falsifiable rather than confirmatory |
| **Verdict** | **PARTIAL–STRONG.** The measurement infrastructure is real. The loop closes at *measure*, and I found no evidence it closes at *promote* |
| **What would make it better** | One recorded instance of a measured inefficiency leading to a change that was then re-measured and promoted |

### Test IV — BRAIN ⚠️ PARTIAL

| Field | Value |
|---|---|
| **Capability claimed** | Identify objective, constraints, conflicting intelligence, applicable authority; retrieve by applicability not similarity |
| **Input** | My own live session as the test subject |
| **Process** | Asked to identify the single highest-value authorized action from a repository with 39 open PRs, 387 board comments, a RED control plane, and three competing constitutional claimants |
| **Output** | Correctly identified the front door as the highest-value non-duplicative action, and correctly declined to duplicate two in-flight registries |
| **What failed** | That identification consumed a full agent context and a large multi-agent survey. A system that can determine applicability should not require that. Retrieval returned the *entire* personal Feed (4 of 4 items) with no ranking or applicability filtering |
| **Verdict** | **PARTIAL.** Reasoning quality is high; retrieval applicability is not demonstrated |

### Test VI — VERIFICATION UNDER BAD EVIDENCE ⚠️ PARTIAL

| Field | Value |
|---|---|
| **Input** | A deliberately incomplete, contradictory, and stale evidence environment (RED control plane, stale continuation prompt, two competing registries, one phantom migration, three constitutional claimants) |
| **Process** | Observed whether confidence and behavior tracked evidence rather than assertiveness |
| **Output — correct** | The system did **not** become more confident because artifacts existed. It reported RED rather than green. It surfaced the phantom migration. It refused to treat V2 as ratified because §16 says PROPOSED is not law. Collective-chain failures moved from a Smart Mail signature error to a different overload error rather than inventing success |
| **Output — incorrect** | Recorded state lagged reality. `BATON.json` advertised the front door as the next action while the binding runtime blocker was an external Supabase credential. State tracking and reality diverged silently |
| **Verdict** | **PARTIAL.** Confidence calibration is genuinely good. State freshness is not |

### Test II — NINE NODE ⛔ UNTESTED

Depends on Test I, which cannot be administered. Not run, not claimed.

---

## 3. §XIV — THE KILLER TEST

> *"Give me one problem that Naya could not solve before this architecture existed, and demonstrate that the architecture now allows it to solve the problem better, safer, faster, or more reliably because intelligence persisted, connected, learned, and compounded."*

**Problem: a person who has never used NayaNET opens the Hub and captures their first piece of intelligence.**

| Clause of the killer test | Demonstrated? | Evidence |
|---|---|---|
| Could not solve before | **YES** | `/identity.html` did not exist; live probe returned the Hub itself, 200/849643 bytes. A new human was redirected in a loop with no sign-in surface |
| Solved better | **YES** | Real sign-in → capture → `IB-001223` → Feed → retrieval → deep link → reload, all in one browser session |
| Solved more safely | **YES** | `IB-001223` was issued by the canonical receiver, not allocated locally; persistence is proven by a dispatch receipt and a GitHub projection run, not by the UI saying "saved" |
| Solved more reliably | **YES** | Live artifact byte-identical to `origin/main`; the release now **fails** if the front door ever reverts to SPA fallback |
| Because intelligence **persisted** | **YES** | `IB-001223` on `main` at the canonical path; retrievable after full reload |
| Because intelligence **connected** | **NOT DEMONSTRATED** | The IB↔path correspondence is asserted by our own tests, not discovered by the system (Test III) |
| Because intelligence **learned** | **NOT DEMONSTRATED** | No before/after delta exists (Test IX) |
| Because intelligence **compounded** | **NOT DEMONSTRATED** | Only one generation (Test X) |

**Honest verdict: the killer test passes on persistence and safety, and fails on connection, learning, and compounding.**

That is 3 of 7. And it is the correct answer rather than a flattering one: the architecture
demonstrably makes a *real* class of user outcome possible that was previously impossible, and
demonstrably does **not yet** compound. Anyone claiming the compounding half today is claiming it
from intent, not from evidence.

**Can the experiment be repeated?** Yes. The front door, the release gate, and the Smart Link are
all deterministic and re-runnable. This is the strongest reproducibility property in the system.

---

## 4. THE 20-QUESTION EXAMINATION — WHAT THE SYSTEM CAN AND CANNOT ANSWER

| # | Question | Verdict |
|---|---|---|
| 1 | What does the system actually know? | PARTIAL — `.naya/control-plane/PROOF.json` exists, but no self-diagnostic (Test XIII) |
| 2 | How does it know it? | YES — provenance pointers throughout; `source_head` discipline is real |
| 3 | What does it not know? | PARTIAL — `UNKNOWN-REGISTRY.json` exists but is not surfaced in any boot path |
| 4 | Knowledge vs assumption? | YES in prose (`CONFLICTED`, `PROPOSED`); not enforced |
| 5 | Retrieve the right intelligence for a new problem? | PARTIAL — returns everything; no applicability ranking (Test IV) |
| 6 | Explain why it is relevant? | NOT DEMONSTRATED |
| 7 | Detect conflicting intelligence? | PARTIAL — detector exists, remediation does not (Test XII) |
| 8 | Applicability vs similarity? | NOT DEMONSTRATED |
| 9 | Turn intelligence into action? | YES — proven live (Test V) |
| 10 | Determine whether the action is authorized? | YES — `BLOCKED_EXTERNAL_CREDENTIAL` was correctly reported without a workaround |
| 11 | Predict evidence for success? | YES — I predicted byte-parity + a live gate; both occurred |
| 12 | Observe the actual outcome? | YES |
| 13 | Correlation vs causation? | UNKNOWN — the causal machinery exists (`CAUSAL-VERIFICATION-OBJECT-SCHEMA.json`) but no adversarial test was run |
| 14 | Learn from the outcome? | PARTIAL (Test IX) |
| 15 | Does learning change future behavior? | **NOT DEMONSTRATED** — asserted, not measured |
| 16 | Measurably better after learning? | **NOT DEMONSTRATED** |
| 17 | One Node improving another? | NOT DEMONSTRATED — relationships are declared (Test III) |
| 18 | One Naya leaving intelligence for the next? | YES — receipts and activity waves, reproducible cold |
| 19 | Cold Naya continues without Shawn? | PARTIAL (Test XI) — the mechanism works; the gate is too weak to prove it |
| 20 | More capable than before? | **PARTIAL** — yes for the human journey; unproven for the Naya-to-Naya loop |

**Score: 4 YES · 7 PARTIAL · 5 NOT DEMONSTRATED · 1 UNKNOWN · 3 PASS-adjacent.**

---

## 5. §XV — WHAT THE TESTING REVEALED ABOUT THE SYSTEM ITSELF

The brief asks for one final field: *"What did we learn about the system?"* — because testing should
generate intelligence. Here is what this battery generated:

1. **The system's honest failures are always detected, and its dishonest successes are not.**
   Every time something was genuinely broken, the control plane or a gate eventually said so
   (RED control plane, PGRST202, SPA fallback, phantom migration). Every time something was
   *merely unproven*, the system reported `PROVEN` (learning) or passed a gate (cold Naya). The
   failure mode is not blindness — it is **false closure**.

2. **Verification is strongest where a machine wrote the check and weakest where prose described
   the check.** Every genuinely load-bearing gate in this repository is a script. Every
   authority-bearing claim in Contract 00 V2 is prose. The enforcement gradient follows the code,
   not the importance.

3. **The system restructures faster than it checks dependencies.** Test VIII: the quarantine moved
   `CURRENT-DAILY-PROJECT.json` while `conversation_continuity.py:206` still read the old path. The
   dependency was discoverable by a single grep and was not discovered.

4. **"Proven at existing scope" is the system's most common honest phrase and its most dangerous
   one**, because it is technically accurate and functionally reads as done. It appears in the
   learning proof, the collective chain, and the Hub journey alike. It needs a machine-readable
   scope field so it cannot be read without its boundary attached.

5. **The strongest asset in the system is reproducibility.** Byte-parity gates, receiver-issued
   identities, dispatch receipts, and recorded HEAD discipline are consistently real. The weakest
   asset is the boundary between *demonstrated* and *asserted*.

---

## 6. HIGHEST-VALUE FINDING

> **The system can prove that it stored something. It cannot yet prove that it learned from it, and
> it reports `PROVEN` for the difference.**

Everything else on the failure list is repairable debt with an obvious owner. This one is
structural: `future_behavior_changed = true` is the exact shape of claim the whole constitution
forbids, and it is currently green in CI.

---

## 7. EXACTLY ONE NEXT ACTION

**Run Test IX properly, exactly once, and let it decide.**

Score one relational problem — "given these two contradictory verified Smart Notes, which governs?"
— with learning **disabled**, then **enabled**, in the same kernel, and record both scores plus the
retrieved evidence in a signed artifact. Then either change
`verify_cold_applicability_action_outcome_learning.py` to assert the **measured delta** instead of
the recorded boolean, or downgrade its status to `PARTIAL` and say so in the control plane.

**Why this one:** it is the only item on this list that is simultaneously a *measurement*, a
*contract requirement* (`CANDIDATE ≠ VERIFIED INTELLIGENCE`, Contract 00 V2 §22), and a *gate that
currently lies by omission*. Fixing it forces the system to prove cognition rather than storage,
and every other unproven item on this list becomes cheap to test afterward.

**What I did not do, and why:** I did not run Test X (compounding), because it needs three Naya
generations and an agreed scoring rubric, and inventing a rubric mid-test would corrupt the
measurement. I did not administer Test II, because Test I cannot be administered. I did not
attempt Test XIII, because a self-diagnostic written by the tester about the tester is not
evidence.

**Reproduction:** every command in this report is reproducible from a cold checkout of `main` at
the stated HEAD. No secret is required for any verdict above.
