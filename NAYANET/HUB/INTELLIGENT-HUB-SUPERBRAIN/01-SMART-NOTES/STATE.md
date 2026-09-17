# Smart Notes — Current State

**State:** IMPLEMENTATION SLICE — FOUR HARD GATES RECONCILED
**Last updated:** 2026-09-17

## Verified now

- Part `01-SMART-NOTES` exists in the canonical project map.
- Living feature contract exists.
- Existing Smart Note transaction runtime is the canonical persistence boundary.
- Canonical Smart Notes are persisted under `SUPERBRAIN/SMART-NOTES` and read back byte-for-byte after write before downstream projection proceeds.
- CIS learning and PIS projection remain downstream of the canonical Smart Note record.
- Canonical Smart Note PIS events preserve the Smart Note timestamp for `created_at` and `updated_at`.
- Canonical Smart Note PIS events carry explicit source ID and canonical source path provenance.
- Canonical Smart Note PIS events default to `privacy.visibility=private` and `privacy.consent_state=not_granted`.
- Transaction receipts now record authoritative persistence hash/path plus privacy and provenance evidence.
- The end-to-end verifier covers authoritative persistence, privacy default, timestamp provenance, source provenance, CIS learning, PIS projection, and cold-Naya recovery.

## Remaining verification

- Run the updated verifier against the repository/runtime environment.
- Verify downstream Hub rendering consumes the projected privacy/provenance fields without reinterpretation.
- Verify real production persistence/runtime behavior, not only the isolated repository-shaped fixture.
- Complete create/read/update lifecycle and downstream Library, Reports, Connections, and Smart Share adapters.
- Verify explicit consent transition from private to Collective behavior through the canonical authority path.

## Four hard gates

1. **Privacy:** canonical Smart Notes are private until explicit consent is represented.
2. **Timestamp:** canonical event timestamps come from the Smart Note record, not projection-time clock generation.
3. **Provenance:** event source ID and canonical path identify the authoritative Smart Note record.
4. **Authoritative persistence:** the canonical Smart Note is written and independently read back before the transaction can proceed or claim completion.

## Current boundary

This is a surgical reconciliation of existing implementation. No new Smart Note store, feed, or competing renderer was introduced. The PIS remains a projection, and the canonical Smart Note remains the durable source record.

## Evidence

- `.naya/runtime/smart_note_transaction.py`
- `scripts/build-smart-feed-projection.py`
- `scripts/verify-smart-note-transaction.py`
- `NAYANET/HUB/src/intelligence/types.ts`
- `NAYANET/HUB/FOUNDATION-CONTRACT.md`

## Next action

Run the updated Smart Note transaction verifier and inspect the resulting proof; then verify the live Hub consumes the canonical event privacy/provenance fields unchanged.
