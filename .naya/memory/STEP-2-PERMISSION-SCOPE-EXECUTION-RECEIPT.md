# Step 2 — Permission / Scope Enforcement Execution Receipt

**Status:** RED

## Exact files changed

- `.naya/memory/permission_scope.py` — hardened deny-by-default authorization model; explicit scope/project/principal grants; unknown scope/permission denied.
- `.naya/memory/smart_notes_v3.py` — surgical runtime integration. Authorization now filters the loaded event set before corpus construction, candidate generation, ranking, relationship reranking/expansion, and context delivery. CLI retrieval and daily-report entry points require principal identity, scope, and project.
- `.naya/memory/tests/test_permission_scope.py` — 11 adversarial tests, including the ten required security cases plus an explicit authorization-before-ranking test.
- `.naya/memory/test_smart_brain_v3.py` — regression fixtures updated to supply explicit authorization metadata for retrieval/context tests; missing authorization is explicitly denied.
- `.github/workflows/smart-brain-v3-enforcement.yml` — CI invokes the permission test discovery and Smart Brain regression suite.
- `.github/workflows/step2-permission-scope-gate.yml` — dedicated Step 2 syntax, adversarial, regression, and canonical-validation gate.

## Exact tests intended/executed

Commands configured for authoritative execution:

```text
python -m py_compile .naya/memory/permission_scope.py .naya/memory/smart_notes_v3.py .naya/memory/tests/test_permission_scope.py .naya/memory/test_smart_brain_v3.py
python -m unittest discover -s .naya/memory/tests -p 'test_*.py' -v
python .naya/memory/test_smart_brain_v3.py -v
python .naya/memory/smart_notes_v3.py validate
```

**Authoritative current-checkout execution count:** 0 completed for the Step 2 implementation.

The connected GitHub repository can be inspected and written, but no execution-capable checkout/runtime is available through the current connector session. A pull-request execution was requested to obtain CI evidence, but the available Smart Brain workflow run `34395881962` failed at its pre-existing **Cold-start Naya activation acceptance** job before reaching the permission tests. Therefore no permission-test pass/fail count is claimed here.

## Security proof status

| Required proof | Source-level implementation | Executed evidence |
|---|---|---|
| same-scope authorized → ALLOW | Implemented in `authorize()` | NOT EXECUTED |
| unauthorized private memory → DENY | Implemented | NOT EXECUTED |
| cross-project without grant → DENY | Implemented | NOT EXECUTED |
| explicit grant → ALLOW | Implemented | NOT EXECUTED |
| unknown scope → DENY | Implemented | NOT EXECUTED |
| unknown permission → DENY | Implemented | NOT EXECUTED |
| mixed relevance attack → unauthorized candidate excluded before `corpus()` | Implemented in `authorized_events()` → `corpus()` | NOT EXECUTED |
| private marker → zero leakage | Implemented by pre-ranking filter | NOT EXECUTED |
| relationship expansion → unauthorized object blocked | Implemented by `authorized_relationship_targets()` | NOT EXECUTED |
| direct event-ID attack → DENY | Authorization precedes exact-match scoring | NOT EXECUTED |
| authorization BEFORE ranking | `retrieve()` calls `authorized_events()` before `corpus()` / ranking | NOT EXECUTED |

## Regression result

**RED / NOT PROVEN.** The authoritative CI run did not reach the permission/regression commands because the cold-start acceptance gate failed first. No invented pass count is recorded.

## Current repository head

`a104b39d293cfd98c6776abacef596bd6f2844cd`

## Blocking weakness

1. Runtime execution of the Step 2 test suite is not yet independently evidenced.
2. Existing canonical `SE-*` memory events audited in Step 1 do not currently carry explicit `scope` and `permissions` metadata. The new fail-closed runtime therefore refuses those legacy events until their canonical schema is repaired. This is a security-preserving consequence, not a bypass.
3. The existing Smart Brain CI has an unrelated cold-start acceptance failure that prevents it from reaching the Step 2 tests in the observed run.

## Acceptance decision

**STEP 2 = RED**

Do not advance to Step 3 until an execution-capable run proves all adversarial tests, the full regression suite, and canonical validation pass, with the resulting evidence and final commit SHA recorded here.
