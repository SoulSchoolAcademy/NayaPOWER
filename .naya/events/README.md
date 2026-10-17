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

## Share → notify seam (#2244 req 3 → req 4)

Every `transition … --to SHARED` best-effort publishes one notification to
the worker notification outbox (`tools/notify_outbox.py`, #2244 req 4, PR
#2303), so a shared lesson reaches workers at their next activation instead
of sitting in a feed nobody polls.

- **Once per event:** the outbox dedup key is `learning-event:<event_id>`
  (deterministic), so re-shares never duplicate.
- **Audience:** `all` plus the event's `impacted_teams` — the proven
  broadcast path fires and team-targeted activation keeps working.
- **Severity:** INFO→info, NOTICE→attention, WARNING→attention,
  HIGH→urgent, CRITICAL→blocker; TTL 72h.
- **Fail-safe:** the publish never breaks the transition. If the outbox is
  absent (e.g. #2303 unmerged) or publishing fails, the transition still
  succeeds and the skip is recorded on the envelope as
  `share_notification: {skipped: <reason>}`. Kill switch:
  `NAYA_EVENT_SHARE_NOTIFY=0`.
- The receipt (`outbox_event_id`, audience, severity) is stored on the
  envelope as `share_notification` and surfaced by the CLI.

The envelope still does not *deliver* anything — the outbox owns delivery;
its receipts are the proof.

## Explicit non-claims

- This is **not** a notification/push delivery mechanism itself (#2244
  requirement 4 — that is `tools/notify_outbox.py`). The envelope records
  the share and hands the event to the outbox, best-effort; the outbox's
  delivery receipts are the only delivery proof.
- This is **not** the learning admission gate and does not change any
  candidate's truth state. It attaches to existing flows; it never bypasses them.
- No event here counts as a learned lesson until `BEHAVIORALLY_VERIFIED`
  with an independent behavior proof. Stored is not learned.
