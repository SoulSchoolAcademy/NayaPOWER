# Step 2 — Next Execution Action

Use an execution-capable checkout of `SoulSchoolAcademy/NayaPOWER`.

1. Import `.naya/memory/permission_scope.py` into `.naya/memory/smart_notes_v3.py`.
2. Identify every retrieval/context-delivery entry point and require an `AuthorizationRequest` before candidate generation.
3. Pass only `filter_authorized(...)` candidates into lexical/TF-IDF ranking and relationship expansion.
4. Add integration tests proving unauthorized content never reaches the ranking candidate set, exact lookup, metadata diagnostics, or relationship expansion.
5. Run:
   - `python -m unittest discover -s .naya/memory/tests -p 'test_*.py'`
   - the existing Smart Brain validation/regression commands discovered in the repository.
6. Record exact stdout, pass/fail counts, changed files, and commit SHA in the Step 2 receipt.
7. Step 2 is GREEN only if the runtime integration is executed and all ten adversarial cases plus regression tests pass.

Do not advance to Step 3 until this gate is GREEN.
