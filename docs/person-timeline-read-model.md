# The per-person timeline read model — contract

Best-of-Best application map, element **#1** (the living timeline of
everything with every person, derived — zero manual logging). This file is
the contract every consumer reads: the flagship People door, Smart People
Search, Naya's morning briefs. **One derivation, one event shape** — if a
consumer needs a field that is not here, the field is added to the model,
never re-derived privately by the consumer.

## Pieces

| Piece | Where | Job |
|---|---|---|
| Identity tables | `person_identities`, `person_identity_aliases` (migration `20261022203000_person_timeline_v1.sql`) | The durable registry: who a person is, under every name they arrive by. |
| Resolution functions | `normalize_person_name`, `resolve_person_key` (SQL) + mirrors in `tools/person_timeline.py` | ONE rule, two runtimes: email hash wins when known; otherwise the normalized name keys the person; alias-registry rows fold variants into the canonical person. |
| Event stream | `person_timeline_events` view (SQL) + `build_timeline()` (`tools/person_timeline.py`) | The unified chronological stream. The builder is the full derivation (incl. outbound-mail participant fan-out); the view is the SQL projection of the same shape for direct readers. |
| Person summary | `summarize_person()` | last spoke / waiting on owner / open threads / invite state — derived, never stored by hand. |

## The event shape (every consumer reads exactly this)

| Field | Meaning |
|---|---|
| `person_key` | The resolved person (`h:<email_hash>@<owner>` or `n:<normalized name>@<owner>`). |
| `owner_alias` | Whose timeline this is. |
| `event_at` | When it happened (source row's timestamp). |
| `event_kind` | `wall_note` · `mail_message` · `invite`. |
| `source_table` | `smart_notes` · `smart_mail_messages` · `invites` — provenance, always. |
| `source_id` | Source row id when the source carries one; else `null`. |
| `title` | Thread subject for mail; else `null`. |
| `body` | Note content / message body; `null` for invites. |
| `direction` | `inbound` (they → owner) or `outbound` (owner → them). |
| `counterparty_name` | Display name as it arrived; `null` for hash-only people (invites) — a name is never invented. |
| `thread_key` | Mail thread key; else `null`. |
| `status` | Invite status for invite events; else `null`. |

## Derivation rules (the Faces derivation, made explicit)

1. **Wall notes** key to the note's author (`author_name` COALESCE
   `sender_name` — the canon Faces pattern). Owner-authored notes are the
   owner's own wall, not a relationship event.
2. **Inbound mail** keys to the sender. **Outbound mail** fans out to the
   thread's participants minus the owner — each participant gets the
   event (a group thread is a relationship with each person in it).
3. **Invites** key by `invitee_email_hash` only. When the same hash later
   arrives via a mail participant carrying that email, the two records
   are the same person — the hash-keyed identity is the merge point.
4. **The owner is never a person** in their own timeline.
5. **Unresolvable rows are quarantined and counted** in the build report
   with reasons (`wall_note_without_author`, `inbound_message_without_sender`,
   `outbound_message_without_counterparty`, `message_without_direction`,
   `invite_without_email_hash`) — never silently attached, never dropped
   without a count.
6. **Honest nulls.** A field the sources do not carry stays `null`.
   "Last spoke" and "waiting" derive from event order and direction
   only; nothing is inferred about sentiment or importance.

## Status

Migration ships as code (PENDING in the ledger; production application is
human-gated) and OPENS with a fail-loud source-column check: the flagship
source tables were created outside repo migration history, so if any
required column is absent in the applying project, the migration raises
`PERSON_TIMELINE_SOURCE_COLUMNS_MISSING` and stops rather than creating a
silently empty view. The Python builder + tests prove the derivation
today against fixture rows shaped to the evidenced columns.
