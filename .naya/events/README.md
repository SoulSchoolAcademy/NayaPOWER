# Learning-event ledger

Machine form of **issue #2244 requirement 3** — the canonical learning-event envelope.

## What lives here

- `learning-events.json` — the event ledger (auto-created on first issuance).
  A runtime projection: `{"schema": "naya.learning-event-ledger.v1", "events": {...}, "issued_count": n}`.
  The canonical learning store is unchanged; this file is not a second source of truth.
- Implemented by `tools/learning_event_envelope.py`; tested by
  `tests/test_learning_event_envelope.py`.

## Envelope fields

`event_id` (deterministic: `evt-` + sha256 of the identity fields), `schema`,
`event_type` (failure | lesson | blocker | breakthrough | material),
`severity` (INFO < NOTICE < WARNING < HIGH < CRITICAL), `title`,
`source_artifact` + `source_sha` (40-hex), `expected` / `actual`,
`owner`, `impacted_teams`, `specialty_feed_url`, `lesson_status`
(PROPOSED | VERIFIED | NONE_WITH_REASON), `smart_note_id` / `smart_note_link`,
`no_lesson_reason`, `next_action`, `lifecycle_state`, `issued_at` / `issued_by`,
`history[]`.

## Lifecycle (enforced, linear)

```
DETECTED → SHARED → ACKNOWLEDGED → RESOLVED → PRESERVED → REUSED → BEHAVIORALLY_VERIFIED
```

Transition gates (all rejections carry named reasons):

| Move | Required evidence |
|---|---|
| → SHARED | `feed_url`: the specialty-feed URL the event was posted to |
| → RESOLVED | `smart_note_id` + `smart_note_link` + `regression_evidence`, **or** an explicit `no_lesson_reason` |
| → PRESERVED | a canonical `smart_note_id` carried from RESOLVED |
| → REUSED | `reuse_evidence`: where the lesson was applied |
| → BEHAVIORALLY_VERIFIED | `behavior_proof`: the independent verifier's receipt that behavior changed because of the lesson; sets `lesson_status` = VERIFIED |

`BEHAVIORALLY_VERIFIED` is terminal. Any other move is rejected as `ILLEGAL_TRANSITION`.

## Idempotency

The event ID is derived from the identity fields
(type, severity, title, artifact, SHA, expected, actual, owner, teams), so the
same material failure issued twice returns the existing record
(`duplicate: true`) — exactly one event per failure, per #2244's acceptance.

## CLI

```bash
python3 tools/learning_event_envelope.py issue --type failure --severity HIGH \
  --title "..." --artifact tools/foo.py --sha <40-hex> \
  --expected "..." --actual "..." --owner naya-2 \
  --teams learn,verify --next "..."

python3 tools/learning_event_envelope.py transition <event-id> --to SHARED \
  --actor naya-2 --feed-url https://github.com/.../issues/2235
```

## Explicit non-claims

- This is **not** a notification/push delivery mechanism (#2244 requirement 4).
  It records that an event was shared; it does not deliver it.
- This is **not** the learning admission gate and does not change any
  candidate's truth state. It attaches to existing flows; it never bypasses them.
- No event here counts as a learned lesson until `BEHAVIORALLY_VERIFIED`
  with an independent behavior proof. Stored is not learned.
