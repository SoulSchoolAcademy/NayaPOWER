# Conversation Endpoint Class — Spec (workspace only, NOT live)

**Status: WORKSPACE-ONLY SPEC + PROTOTYPE. Not a landing. Not live. Not a face change.**
**Lane:** Power's record-structure lane, merged completion-list item 2 (Conversation
control per block, record-backed).
**Governs:** Resolve's independent re-score finding (2026-10-28): NO Conversation
anywhere on the v4 preview (43 blocks). Each block needs a Conversation control
backed by the shared record — not chat-only, not device-local.
**Companion files:** `conversation-endpoint-2026-10-28.py` (prototype module),
`test-conversation-endpoint-2026-10-28.py` (tests, fixtures).
**Never:** a second mail system, a second notes system, a snapshot fallback,
a staged-as-live claim. Landing (production table + publisher wiring) is gated,
same as B1.

---

## 0. What live reads proved (2026-10-28, same pass, all by live read)

No existing store can carry per-block conversation. The class therefore gets its
own store; it composes with what exists instead of duplicating it.

- **74 public tables; zero tables or columns matching `%conver%` or `%discuss%`.**
  There is no conversation-ish storage by name anywhere in the record.
- **`smart_mail_threads` / `smart_mail_messages` are MAIL, not conversation.**
  Threads: id, subject, from_alias, to_alias, preview, created_at, updated_at.
  Messages: id, thread_id, from_alias, body, created_at. Threads are ADDRESSED
  (to_alias). Block conversation is unaddressed, per-block, seat-alias
  participants. Do not conflate them; this class never reads or writes mail.
- **`hub_smart_notes` is Smart Notes storage, not conversation.** Columns: id,
  ib_id, title, nutshell, human_note, child_note, grandma_note, naya_note,
  machine_note, what_it_means, whats_in_it_for_you, how_it_applies, source,
  author, github_path, created_at, note_created. No notes column, no
  conversation column.
- **`object_links` is object links, not conversation.** Columns: id,
  owner_alias, a_kind, a_id, b_kind, b_id, b_label, created_at. No body.
- **`smart_note_events` is note events, not conversation.** Columns: id,
  member_id, subject, event_type, source_context, privacy_state, status,
  created_at, verified_at. No message thread, no block key.
- **`work_transitions` is state transitions, not conversation.** Columns: id,
  item_id, item_key, project_id, from_state, to_state, actor_seat, proof_url,
  at. No body, no block key.
- **`work_items` has 22 columns and NO block key, NO area_key, NO conversation
  column.** Per-row `notes` is a jsonb OBJECT with varying keys (row
  `page-audit-booking`: keys `entries`, `fill_20261028`; new row
  `one-scheduler-two-faces`: empty object `{}`). Row notes stay per-row record
  notes. Block conversation is not row notes.
- **Hub row notes is a jsonb ARRAY, the project feed, not per-block
  conversation.** Row id `733b1eab-047a-45c6-b944-25a3edf8f08c`, count n=44,
  tail from `naya-power` at `2026-10-28T18:00Z` (count + tail only; the array
  itself was never fetched whole). The feed stays the feed.
- **One live-read failure, owned:** a combined shape query over the hub row
  plus two object-notes rows errored, because `jsonb_object_keys` cannot run
  on the hub row's array. Re-run split by shape proved both shapes. A failed
  read was never reported as a shape.

Conclusion: the endpoint class needs exactly one new store. Creating it is a
schema change and therefore gated. The prototype below proves the logic against
a fixture store so the gated landing wires proven logic, not a guess.

---

## 1. The class

```
ConversationService(store: ConversationStore)
  open_conversation(block_key, after_seq=None, limit=100)
      -> {block_key, messages[], participants[], count}
  append_message(block_key, message_id, author_alias, body)
      -> {message, duplicate: bool}
```

- **Block key:** an opaque string supplied by the face (the face's block
  identifier, e.g. one of the 43 preview block keys). The service does NOT
  invent block keys. V1 does NOT validate a block key against a block registry
  (the registry/mapping is owed work under G-1); when it lands, validation
  hooks in here and nowhere else.
- **Open creates nothing.** Opening a block with no messages returns an empty
  list, empty participants, count 0. No row is written on read, so no phantom
  blocks and no write-on-read races.
- **Participants are derived, never stored separately in v1:** the distinct
  `author_alias` values in the block's messages, in first-appearance order.
  No participants table in v1.
- **Ordering:** messages read back in `seq` order (per-block monotonic
  sequence, starting at 1). `seq` is the order; `created_at` is display only.
- **Pagination (transport honesty):** `after_seq` returns messages with
  `seq > after_seq`; `limit` defaults to 100, max 500. Narrow pages keep
  payloads safe on the known-flaky transport. The face pages; it never asks
  for a whole conversation in one call. `count` is always the block's TOTAL
  message count (unfiltered) and `participants` are always block-wide;
  only the `messages` page itself is sliced.

## 2. Message shape

```json
{
  "message_id": "<client UUID>",
  "block_key": "<face block key>",
  "seq": 3,
  "author_alias": "naya-power",
  "body": "…",
  "created_at": "2026-10-28T18:05:00Z"
}
```

- `message_id` is a client-generated UUID, supplied on every append, and is
  the idempotency key. The client generates it ONCE and reuses it across
  retries. A retry with a new id is a new message by definition.
- `author_alias` is a seat alias string (`naya-power`, `nitro`, `resolve`,
  `nayacodex`, …). V1 accepts any non-empty alias (≤ 64 chars); production
  validation against `smart_mail_aliases` is a wiring hook, not v1 logic.
- `body` is non-empty text, max 8,000 chars (spec decision: long bodies are
  the known transport failure mode; the cap keeps every message safely
  readable in slices).
- `created_at` is server time, ISO Z. The client never supplies it.

## 3. Append, guarded (the rule that makes retry safe)

Proven guarded-write rule, applied: read state before any retry, verify after
write, every retry is a new decision.

1. **Validate.** Empty block key, unparseable message_id, empty or overlong
   author_alias, empty or overlong body → 400 `{error: "invalid_message",
   detail: …}`. Nothing is written.
2. **Read state.** Look up (block_key, message_id). If a message exists,
   return it with `duplicate: true`. NO new row, NO new seq, NO side effect.
   A lost-response retry therefore lands exactly once.
3. **Assign seq** = max seq in this block + 1 (first message = 1).
4. **Insert.**
5. **Verify by re-read.** Read the inserted row back by (block_key,
   message_id). If the re-read fails or mismatches, raise store-unavailable
   and NEVER claim success. A write whose verification is unknown is not a
   success.
6. **Return** the stored message with `duplicate: false`.

Production concurrency note (honest scope): two simultaneous appends to one
block need the production table's UNIQUE(block_key, seq) constraint, with a
seq-conflict handled as a NEW decision (re-read max, re-assign, re-insert),
never a blind retry. The prototype serializes in-process; it proves the
logic, not concurrent writers. The constraint is part of the gated landing,
not an afterthought.

## 4. Error semantics (never a snapshot fallback)

| Condition | Result |
|---|---|
| Store answers, block has no messages | 200, empty list, count 0 |
| Store answers, block has messages | 200, messages in seq order |
| Store unreachable / verification fails | **503 `{error: "conversation_store_unavailable"}`** |
| Invalid append input | 400 `{error: "invalid_message", detail}` |

An empty list is only ever returned when the store answered. A store failure
is always a 503. There is no cached copy, no snapshot, no device-local
fallback, and no empty list masquerading as an outage. This mirrors B1's
failure contract (503, never snapshot fallback).

## 5. Per-block isolation

Every operation filters by `block_key`. One block's conversation can never
leak into another's read, count, participants, or seq. The face must ALSO
key any client cache by `block_key`; server isolation does not excuse a face
that shows block A's thread under block B's header. Tests prove isolation
with fixtures (see §7).

## 6. Production store (GATED — not built by this beat)

One new table, created only through the gated schema path:

```sql
-- GATED: schema change, never applied by a workspace beat.
CREATE TABLE block_conversation_messages (
  id          uuid PRIMARY KEY,          -- = message_id
  block_key   text NOT NULL,
  seq         integer NOT NULL,
  author_alias text NOT NULL,
  body        text NOT NULL,
  created_at  timestamptz NOT NULL DEFAULT now(),
  UNIQUE (block_key, seq)
);
CREATE INDEX block_conversation_messages_block_seq
  ON block_conversation_messages (block_key, seq);
```

The production store adapter implements the same four operations the
prototype's fixture store implements (`get_messages`, `find_by_id`,
`max_seq`, `insert`), so the service logic is unchanged at landing. No
other table is touched: no mail tables, no hub row, no work_items.notes.

## 7. What Nitro's face needs to call

```
GET  /pi/api/conversation?block=<block_key>[&after_seq=N][&limit=M]
  -> {block_key, messages[], participants[], count}

POST /pi/api/conversation
  {block_key, message_id, author_alias, body}
  -> {message, duplicate}   (duplicate=true means "your retry; already stored")
```

Face rules:
- Generate `message_id` once per composed message (UUID) and reuse it on
  every retry of that send. This is what makes a lost response safe.
- Render messages in `seq` order; show `author_alias` + `created_at`.
- Never invent messages, never render one block's thread under another block.
- A 503 means "conversation unavailable right now" — show that honestly,
  never an empty thread, never a stale copy.
- Page with `after_seq` + `limit`; never fetch whole.

## 8. What remains gated (NOT done by this beat)

- Production table creation (schema change — Shawn's only-he-can-clear list
  class: production DB writes).
- Publisher/worker wiring of the two routes into the merged worker.
- Face control build + Nitro rendered review (desktop + phone, real address).
- Block-registry validation hook (rides G-1 mapping DATA).
- Different-seat verification of a landed conversation (append → re-read by
  another seat → same message, same seq, no duplicate after a forced retry).

## 9. Scope guards (what this beat deliberately does NOT do)

- Does NOT touch the live record (reads only, this pass).
- Does NOT modify `b1-live-rows-core-2026-10-27.py` or any B1 file.
- Does NOT build a second mail system (mail tables untouched, by design).
- Does NOT close merged-list item 2 (closes when the face control lands,
  a different seat verifies a live append + retry, and a rendered check
  shows Conversation on blocks).
- Does NOT claim anything live. Every "live" word in this file refers to a
  live READ performed during discovery, never to a live conversation.
