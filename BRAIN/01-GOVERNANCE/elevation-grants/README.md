# Elevation Grants

Bounded capability records authorizing a single truth-state elevation from
VERIFIED to RATIFIED. Ratified 2026-10-06 (Shawn: Option C).

## The law

Authority travels **with the elevation request**, not as a standing identity.
A VERIFIED→RATIFIED write is rejected unless accompanied by a valid, unexpired
grant naming that exact note. No grant → rejected. Expired grant → rejected.
Grant for note X → cannot elevate note Y.

This encodes the standing law "only Shawn ratifies" as machine-enforced
structure. Previously it lived in convention; now the guard enforces it.

## Grant schema

```json
{
  "grant_id": "EG-20261006-SN0471-001",
  "note_id": "SN-0471",
  "target_state": "RATIFIED",
  "issuer": "Shawn Vibert",
  "issuer_role": "Human Director",
  "issued_at": "20261006T130000Z",
  "expires_at": "20261013T130000Z",
  "scope_note": "Why this elevation is authorized",
  "grant_hash": "<sha256 of canonical grant body>"
}
```

- `issuer_role` is `"Human Director"`, or `"Delegate"` with a `delegated_by`
  field naming the Director.
- `grant_hash` is computed over the grant body (all fields except the hash
  itself), canonical JSON. Tampering invalidates the grant.
- Grants are single-use in spirit: each names one note and one transition.
  Expiry bounds the window.

## Issuing a grant

Shawn runs:

```
python3 tools/issue_elevation_grant.py --note-id SN-0471 --expires-days 7 \
    --scope-note "Ratify per director's lock-in directive"
```

The tool writes the JSON file here and prints the grant_id. Grants are
governed records — they land via normal PR review, never by hand-editing
an existing grant (that breaks its hash).

## Enforcement

`tools/truth_state_guard.py::apply_elevation(..., elevation_grants=[...])`
checks grants only for VERIFIED→RATIFIED. All other transitions — including
demotion, which stays universally permitted — are untouched.
