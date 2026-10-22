# The linked-everything model — contract

Best-of-Best application map, element **#14** (a note belongs to a person
and sits in a list and came from a conversation — one thing, three homes,
zero copies), with element **#19**'s owner-named facts riding the same
model. This file is the contract every consumer reads: Smart Lists
(step 15), the timeline UI (step 7), command/search (step 13). **One
link model, one write operation** — if a surface needs a relationship
that is not here, the relationship is added to the model, never
re-invented privately by the surface.

## Pieces

| Piece | Where | Job |
|---|---|---|
| Link table | `object_links` (migration `20261022211500_object_links_v1.sql`) | One row per filing: subject object → target (person / list / thread), stamped with its owner. |
| Fact table | `object_facts` (same migration) | Element #19: plain owner-named key/value facts per object — at most 12, enforced by trigger. |
| Write operation | `file_object_under(...)` (SQL, SECURITY DEFINER) + `LinkStore.file_under()` (`tools/object_links.py`) | The one write surfaces call: "file this under …" — by tap today, by voice tomorrow. Ownership enforced in the database, identically for every caller. |
| Reads | `LinkStore.filed_under()` / `person_home()` / `homes_of()` | Resolution, not copying: every home returns the object's own store row. |

## Refs: the stores' own durable keys, as text

| Kind | Ref | Ownership proof |
|---|---|---|
| `naya_note` | `naya_notes.id` | `owner_id` in the store |
| `smart_link` | `smart_links.id` | `owner_id` in the store |
| `person` | `person_identities.person_key` (the timeline model's key — `h:<hash>@<owner>` or `n:<normalized name>@<owner>`) | `owner_id` in the store |
| `smart_note` | the note's brain-estate id | `owner_alias` scope |
| `mail_thread` | `smart_mail_threads.thread_key` | `owner_alias` scope |
| `list` | the list's name in owner scope (`naya_notes.list_name` is the standing precedent; step 15 gives lists durable ids and text refs carry either form) | `owner_alias` scope |

Subject kinds: `smart_note`, `naya_note`, `mail_thread`, `smart_link`,
`person`, `list`. Target kinds: `person`, `list`, `mail_thread`.
Relation in v1 is exactly `filed_under`.

## The rules (enforced in SQL and mirrored in the service layer)

1. **The caller files only their own.** `file_object_under` derives the
   owner from `auth.uid()` — there is no filing as someone else. The
   target person must be the caller's own person, and where the
   subject's store carries `owner_id`, the subject must be the caller's
   own too. Refusals are named: `FILE_OBJECT_UNDER_TARGET_NOT_OWNED`,
   `FILE_OBJECT_UNDER_SUBJECT_NOT_OWNED`, `FILE_OBJECT_UNDER_REQUIRES_AUTH`.
2. **Private by default.** Both tables are RLS owner-only for
   authenticated users; there are no anon policies and no anon execute
   on the operation. A person's links and facts are never public.
3. **Filing is idempotent.** The same (owner, subject, target) filed
   twice is one row (`object_links_unique` + `ON CONFLICT DO NOTHING`).
4. **Unfiling deletes the link, never the object.** Removing a row from
   `object_links` touches nothing else; the object remains in its store,
   readable from its own surface and its remaining homes.
5. **Facts are a handful, in plain words.** At most 12 per object
   (`OBJECT_FACT_LIMIT_REACHED`); keys are owner-named, normalized
   (lowercase, single spaces, ≤64 chars); values are words (≤500 chars).
   No types, no schema, no field editor — that is the element #19 line.
6. **No copies, ever.** Homes resolve the stored object row by ref.
   An edit made once — in the object's own store — is what every home
   reads. The test suite proves this by identity and by mutation.

## What v1 deliberately does not do

- **No UI.** Steps 7 (timeline UI) and 15 (Smart Lists) consume this
  model; this build is the data half only.
- **No link inference.** Links are filed explicitly (tap or voice). The
  name-matching derivations in Faces/the timeline stay what they are —
  derived events — and are never silently promoted to stored links.
- **No cross-owner sharing.** A link is the owner's private filing.
  Sharing an object with another person is a future element with its
  own consent rules, not a flag on this table.
