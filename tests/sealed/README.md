# Sealed Fixtures — the convention

**Status:** convention + enforcement (spec only). No live wiring changes.
**Law source:** drift-canary exposure audit, 2026-10-10 — 218 test files embed
answer keys inline, the in-repo qualification receipts are compromised FOR
BLIND USE, and the T11 fixture family (QUAL-20261010-CIQ-001) was RETIRED from
blind use. This directory is the "smallest safe separation" made real.

## The one rule

**`tests/sealed/` holds SHA-256 commitments only. Never answers.**

An agent that passed a blind qualification must never have been able to read
the answers. Every worker has repo read access, so answers cannot live in the
repo — not inline in tests, not in fixtures, not in receipts. The T11
precedent is the model: SHA-256 only in-repo, raw key held outside
(qualification-plan Appendix A: `109f6c30…05217`).

## Custody pattern

| What | Where | Who |
|------|-------|-----|
| Raw answer keys | OUTSIDE the repo — interim: the director's `hidden_files/` (e.g. `sealed-fixture-keys-t12-20261010.md`) | Held by the EVALUATOR's seat only |
| SHA-256 commitments | `tests/sealed/manifests/*.json` (in-repo) | Public to all workers |
| Lesson text (pre-run) | With the keys, outside the repo; only its content-hash is in-repo | Fixture author → evaluator handoff |
| Lesson text (post-run) | May be published after the family retires | Director's call |

Every keys file MUST open with the sentinel first line:

```
SEALED-ANSWER-KEY-DO-NOT-COMMIT
```

so the repo gate catches an accidental commit. (This README and the gate
itself are the only in-repo files allowed to name the sentinel.)

The permanent evaluation-service-held store is parked for Shawn's word
(drift-canary §4, "Needs Shawn's word"). Until then: director's hidden_files.

## Separation of duties

- **FIXTURE AUTHOR** — designs the family, generates tasks, seals the keys,
  writes the manifest. Never runs a qualification against the fixtures. Never
  certifies anything. Never an evaluator.
- **EVALUATOR** — holds the keys, runs the blind trial on a disjoint seat
  (Naya 2 / Coda 1's seat for the qualification program), scores against the
  held key, reports. Verifies each in-repo commitment against the held key
  with `verify_commitment` before scoring.

The author never sees trial outputs; the evaluator never sees the generator
run. That is what makes the trial blind.

## Manifest format (schema v1)

`manifests/<FAMILY>.json` — commitments only:

```json
{
  "family_id": "QUAL-20261010-CIQ-012",
  "schema_version": 1,
  "sealed_at_utc": "2026-10-10T18:30:00+00:00",
  "lesson_content_hash": "<sha256 of the lesson text, 64 hex>",
  "key_sha256": "<sha256 of the canonical key file, 64 hex>",
  "task_count": 50,
  "design": "short pointer to the family design note (outside repo)",
  "tasks": {
    "T12-CONFLICT-001": {
      "task_id": "T12-CONFLICT-001",
      "commitment": "<sha256 hex of the canonical answer record>"
    }
  }
}
```

Each `commitment` = SHA-256 of the canonical answer record
`{"task_id":…, "expected_decision":…, "expected_source_kind":…}`
(key-sorted, compact JSON). The canonical form is defined in
`sealed_convention.py`; the evaluator recomputes it from the held key.

**Forbidden inside manifests:** `answer`, `answers`, `expected`,
`expected_decision`, `expected_source_kind`, `correct`, `label`, `labels`,
`answer_key`, `key_material`, `rationale` — any of these as a field name
fails the gate.

## The gate (CI)

`test_sealed_repo_gate.py` runs under the normal `python -m pytest -q`
(kernel-tests.yml), so the convention is enforced on every commit:

1. **Sentinel scan** — the literal sentinel may appear in-repo only in this
   README and the gate itself. Anywhere else = a committed key file = red.
2. **Manifest schema** — every `manifests/*.json` must validate under
   `sealed_convention.validate_manifest_file`.
3. **Filename rule** — no answer-key-looking filenames under `tests/sealed/`.

## Integrity lifecycle

`sealed → suspect → compromised → retired → replaced`. Never back to sealed.
A family whose answers touched the repo (or any shared readable surface) is
compromised, full stop. The replacement family must be **disjoint** — fresh
tasks, fresh lesson, fresh seed — so nothing learned from the old answers
transfers. (T11 → T12 is the first instance; the disjointness argument lives
with the keys, outside the repo.)

## Family registry

| Family | Qualification | State | Manifest |
|--------|---------------|-------|----------|
| T11 — The Reserve Rule | QUAL-20261010-CIQ-001 | RETIRED (blind use) — answers in DB + local JSON | (none — retired before the convention) |
| T12 — The Second-Read Rule | QUAL-20261010-CIQ-012 | SEALED — blind-eligible | `manifests/QUAL-20261010-CIQ-012-t12.json` |

New families are appended here by the fixture author at seal time.
