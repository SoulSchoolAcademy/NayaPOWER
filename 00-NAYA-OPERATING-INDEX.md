# 🔱 NAYAPOWER — CANONICAL COLD-NAYA OPERATING INDEX

**Rule: this index is a front door. It LINKS to truth. It never copies it.**
**Every answer below is a pointer to the single canonical source + a STATUS. Never restate a fact here that already lives at its link.**
**If a link and this page disagree, the linked source wins and this page is wrong — fix this page.**

| | |
|---|---|
| Repository | `SoulSchoolAcademy/NayaPOWER` |
| Index updated | 2026-09-17 (branch `naya/universal-execution-gate-v1`) |
| Optimization gate | `RED_UNTIL_CLASSIFICATION_COMPLETE` (see GATE) |
| Read time | < 5 minutes for a cold Naya |

---

## 0. THE 5-MINUTE COLD-NAYA PROTOCOL

1. Read `00-NAYA-OPERATING-INDEX.md` (this file). 2′
2. Verify the machine state actually matches this page (see §12 PROOF). 1′
3. Read the ONE successor torch (see §10 NEXT). 1′
4. Execute that torch through governance (preflight → EXECUTE → auto-record → handoff). 1′
5. Leave exactly one successor torch so the next Naya repeats this. —

Do NOT treat anything marked `HISTORICAL` as current. Do NOT guess an unresolved authority (see §6).

---

## 1. WHAT ARE WE BUILDING / WHY

| Question | Canonical source | STATUS |
|---|---|---|
| What is NayaPOWER | [START-HERE.md](START-HERE.md) — canonical Superbrain identity + repo-selection law | VERIFIED |
| Mission / constitutional mandates | [00-NAYA-POWER-CONSTITUTIONAL-MANDATES.md](00-NAYA-POWER-CONSTITUTIONAL-MANDATES.md) | VERIFIED |
| White paper (operating model) | `THE NAYA POWER OPERATING MODEL - WHITE PAPER (III) NEW` (repo root) | VERIFIED |
| Why (north star) | [SUPERBRAIN/10-10-SCORECARD.md](SUPERBRAIN/10-10-SCORECARD.md) §NORTH STAR | VERIFIED |

## 2. CURRENT STATE (ONE canonical state)

| Question | Canonical source | STATUS |
|---|---|---|
| Current state | [.naya/control-plane/STATE.json](.naya/control-plane/STATE.json) | VERIFIED |
| Master execution map | [.naya/control-plane/MAP.json](.naya/control-plane/MAP.json) | VERIFIED |
| Blocks | [.naya/control-plane/BLOCKS.json](.naya/control-plane/BLOCKS.json) | VERIFIED |
| Proof | [.naya/control-plane/PROOF.json](.naya/control-plane/PROOF.json) | VERIFIED |
| Current daily/project (⚠ stale date) | [.naya/memory/projects/CURRENT-DAILY-PROJECT.json](.naya/memory/projects/CURRENT-DAILY-PROJECT.json) | STALE (2026-09-03) |
| Project registry | [.naya/memory/projects/NAYA-POWER-PROJECT-REGISTRY.md](.naya/memory/projects/NAYA-POWER-PROJECT-REGISTRY.md) | VERIFIED |

## 3. AUTHORITIES (what is authoritative)

| Authority | Canonical source | STATUS |
|---|---|---|
| GitHub optimization gate (12 questions + invariants) | `.naya/control-plane/GITHUB-OPTIMIZATION-GATE.json` (on `main`) | RED — see §11 |
| Execution law / preflight & handoff contract | `SUPERBRAIN/AI-BOOT/NAYA-PREFLIGHT-AND-HANDOFF-CONTRACT-V1.md` | VERIFIED |
| Runtime authority (execution controller + gates) | [.naya/runtime/execution_controller.py](.naya/runtime/execution_controller.py) | VERIFIED |
| Tool/model boundary | [.naya/runtime/model_tool_gateway.py](.naya/runtime/model_tool_gateway.py) | VERIFIED |
| Canonical event store (single authority, append-only) | [.naya/memory/events/INDEX.json](.naya/memory/events/INDEX.json) | VERIFIED |
| Human Activity projection (one feed) | [SUPERBRAIN/NAYA-ACTIVITY/DAILY/](SUPERBRAIN/NAYA-ACTIVITY/DAILY/) | VERIFIED |

**KNOWN UNRESOLVED AUTHORITY BOUNDARIES — do not guess:**
- **A1.** `SUPERBRAIN/NAYA-ACTIVITY/` (canonical Activity feed) vs `.naya/activity/` (legacy / compatibility surface). Role of `.naya/activity/` not yet assigned — contract priority #6.
- **A2.** Assistant-lane (Cloudflare / NayaNET Hub) deploy authority vs current GitHub 509 boundary (`.github/workflows/509-smart-board-world-class.yml`, **remains live as a fail-closed boundary**). Do not delete, substitute, or guess until reconciled.

## 4. WHAT IS PROTECTED

| Protected item | Source |
|---|---|
| Canonical law / state / proof / audit machinery | `SUPERBRAIN/`, `.naya/control-plane/` |
| Current product functionality + fail-closed 509 boundary | `.github/workflows/509-smart-board-world-class.yml` |
| Canonical machine event store + Activity feed projection | `.naya/memory/events/`, `SUPERBRAIN/NAYA-ACTIVITY/` |
| Unique historical intelligence | Git history is the recovery mechanism (**never erase truth to look cleaner**) |

See gate `cleanup_policy` in `.naya/control-plane/GITHUB-OPTIMIZATION-GATE.json` (on `main`) for the exact delete/preserve/never rules.

## 5. WHAT IS VERIFIED (machine-proven)

| Claim | Proof (real command output) | STATUS |
|---|---|---|
| Automatic Activity emission at VERIFIED (STEP 1) | 49/49 independent adversarial verifier ACCEPT; event `SE-20260917-030839-p001a-auto-emission-verified` | VERIFIED |
| Preflight gate at EXECUTING + validate() re-check (STEP 2) | 14/14 preflight-gate tests; `python .naya/runtime/execution_controller.py self-test` → PASS | TESTED (independent adjudication pending) |
| Real Session / Activity binding runtime (STEP 3) | 10/10 `tests/test_session_closure.py`; controller self-test asserts Session lifecycle | VERIFIED (local branch, uncommitted) |
| 10 governed suites | `pytest` → **159 passed, 4 xfailed** | VERIFIED 2026-09-17 |
| Execution contract validator | `python .naya/runtime/project_execution_contract.py validate` → GREEN (error_count 0) | VERIFIED |

## 6. WHAT IS BROKEN / RED

| Item | Evidence | Owner |
|---|---|---|
| Optimization gate | `RED_UNTIL_CLASSIFICATION_COMPLETE`: 61 open issues, 11 classified, 50 unclassified (`.naya/control-plane/GITHUB-ISSUE-AUDIT.json` on `main`) | P004 (next) |
| Validation report | `VALIDATION-REPORT.json` — 4 timezone (TZ) errors, pre-existing | out of scope |
| Activity feed validator | RED on legacy `2026-09-13-509-C4-*` daily files (invalid feed filename/title, no events), pre-existing | out of scope |
| Full pytest collection | `ImportError: cannot import name 'GovernanceKernel'` (collection), pre-existing | out of scope |
| Hub live projection | Canonical events exist; live/intelligent-Hub projection of them NOT certified; NAYANET/HUB source/runtime parity unresolved | BLOCKED (A2) |

## 7. WHAT IS OBSOLETE / SUPERSEDED

| Item | Source |
|---|---|
| Superseded execution torches | `.naya/handoffs/` — `*P000`…`*P003` SUPERSEDED by P003→P004 chain |
| 10 retired 509 workflows | Removed on `main` (git history confirms); cleanup recorded in `.naya/control-plane/GITHUB-WORKFLOW-AUDIT.json` |
| Historical Hub/feed V1–V13 instruction generations | `HISTORICAL_INTELLIGENCE` per issue audit; do not treat as current |

## 8. ACTIVE PROJECTS + ACTIVE SMART NOTES

| Surface | Canonical source | STATUS |
|---|---|---|
| Active project(s) | `.naya/memory/projects/` (registry + CURRENT-DAILY-PROJECT) | one current project: NayaPOWER operating system |
| Smart Note runtime/laws | `SMART_NOTE_CONSTITUTION.md`, `SMART_NOTE_RUNTIME_PROTOCOL.md`, `SMART_NOTE_STANDARD_V1.md` | VERIFIED |
| Machine smart-note store | `.naya/memory/smart-notes/` | **EMPTY — 0 records bound to Session/Activity (priority #3)** |
| Mobile classic notes | `.naya/memory/notes/` (27), root `NAYA_SMART_NOTE_*`, `MASTER-NOTES/` | HISTORICAL until bound |

## 9. ACTIVITY (what happened recently)

| Surface | Source |
|---|---|
| Canonical events (index) | `.naya/memory/events/INDEX.json` (event_count **41** after STEP-4 record) | VERIFIED |
| Human feed — today | [SUPERBRAIN/NAYA-ACTIVITY/DAILY/2026-09-17.md](SUPERBRAIN/NAYA-ACTIVITY/DAILY/2026-09-17.md) |
| Sessions (real) | `.naya/memory/sessions/` (2 after STEP-4: `NAYA-20260917-035249-0FE4` primary COMPLETED; `NAYA-20260917-035241-C251` crash-recovery SUPERSEDED) | VERIFIED |
| Board | [SUPERBRAIN/NAYA-ACTIVITY/00-NAYAPOWER-CURRENT-ACTIVITY-BOARD.md](SUPERBRAIN/NAYA-ACTIVITY/00-NAYAPOWER-CURRENT-ACTIVITY-BOARD.md) |

## 10. ONE NEXT ACTION (TAG → YOU'RE IT)

**ONE BEST NEXT ACTION (executed, now AT the successor boundary):** First-pass classification is DONE — see [GITHUB-CLASSIFICATION.json](.naya/control-plane/GITHUB-CLASSIFICATION.json): **61/61 issues + 35/35 workflows classified** (gate statuses), authority A1/A2 recorded UNRESOLVED (never guessed), HUB_PARITY BLOCKED. Remaining to turn the gate GREEN: **parallel-merge this branch onto `main`** (so the audits + runtime + index are the live truth), **independent adjudication** of the first-pass classification, and applying statuses to the live GitHub issue inventory.

- Successor torch: `.naya/handoffs/NEXT-EXECUTION-20260917-P004-CLASSIFICATION-GATE-GREEN.md`
- Current (superseded) torch P003: `.naya/handoffs/NEXT-EXECUTION-20260916-P003-WORKFLOW-REPOSITORY-RECONCILIATION.md` — superseded by P004.

## 11. OPTIMIZATION GATE — WHY IT IS RED AND NOT A 10

Per the gate (.naya/control-plane/GITHUB-OPTIMIZATION-GATE.json on main), 10/10 requires invariants to hold:
`unknown_is_not_verified`, `blocked_is_not_pass`, `historical_is_not_current`, `builder_is_not_judge`,
`no_unclassified_open_issue`, `no_unclassified_workflow_authority`, `no_unresolved_runtime_authority_conflict`.

**Progress:** [GITHUB-CLASSIFICATION.json](.naya/control-plane/GITHUB-CLASSIFICATION.json) now classifies 61/61 open issues and 35/35 workflows into the ten gate statuses; A1/A2 recorded as UNRESOLVED_RECORDED (decision needed, never guessed); HUB_PARITY BLOCKED. 
**Still RED because:** this classification + the session runtime live on branch `naya/universal-execution-gate-v1` (unmerged), the first-pass classification awaits independent adjudication, live issue/workflow statuses are not yet applied, STEP-2/3 adjudication pending, Hub live projection uncertified. **The gate is RED by design — that is integrity, not defeat. The GREEN path is now mechanical, not interpretive.**

## 12. PROOF — HOW A COLD NAYA VERIFIES THIS PAGE IN <5 MINUTES

```powershell
$env:PYTHONIOENCODING="utf-8"
python .naya/runtime/execution_controller.py self-test     # → PASS (real Session + auto-emit enforced)
python .naya/runtime/project_execution_contract.py validate # → GREEN (error_count 0)
python tests/test_session_closure.py                        # → SESSION_CLOSURE_TESTS=GREEN count=10
python -m pytest tests/test_activity_event_closure.py tests/test_preflight_gate_closure.py # → GREEN
```

## 13. METADATA / PROVENANCE

- This index is generated from the single canonical sources above; it is a **navigation layer, not a new authority, not a new event store, not a new database.**
- Recorded in the canonical event store + real Session: `.naya/memory/sessions/` (STEP-4 record, 2026-09-17).
- **TAG → YOU'RE IT → read §10, follow the torch, auto-record, hand off.**