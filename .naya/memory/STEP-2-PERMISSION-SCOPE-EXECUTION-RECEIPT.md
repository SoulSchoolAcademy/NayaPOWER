# Step 2 — Permission / Scope Enforcement Execution Receipt

**Status:** FINAL VERIFICATION RUN

This receipt is the authoritative evidence record for Step 2. The repository CI gate must execute the permission tests, Smart Brain regression suite, and canonical validation before any GREEN declaration.

## Required commands

```text
python -m py_compile .naya/memory/permission_scope.py .naya/memory/smart_notes_v3.py .naya/memory/tests/test_permission_scope.py .naya/memory/test_smart_brain_v3.py
python -m unittest discover -s .naya/memory/tests -p 'test_*.py' -v
python .naya/memory/test_smart_brain_v3.py -v
python .naya/memory/smart_notes_v3.py validate
```

## Acceptance

All adversarial permission tests, authorization-before-ranking proof, the full Smart Brain regression suite, and canonical validation must pass. No test result may be inferred from source inspection.

## Runtime boundary

The authorization gate is enforced before corpus construction and therefore before lexical/BM25/TF-IDF ranking. Relationship expansion is restricted to the already-authorized event map.

**STEP 2 = AWAITING EXECUTED CI RESULT**
