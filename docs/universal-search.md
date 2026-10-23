# Universal search — contract

Best-of-Best application map, element **#12** (command + universal
search — the Linear lesson: one place to find and do anything),
build-order step **13**. This file is the contract every search surface
reads: the Hub command palette today; the flagship standard feature
when its lane frees. **One service, one result shape, one ranking** —
if a surface needs a field that is not here, the field is added to the
service, never re-derived privately by the surface.

## Pieces

| Piece | Where | Job |
|---|---|---|
| Service | `public.search_universal(p_query, p_limit)` (migration `20261022214500_universal_search_v1.sql`; final definition in `20261022220000_alias_binding_v1.sql`) | The ranked merge over the five object types, behind the caller's JWT. Owner isolation and ranking live here and nowhere else. |
| Ranking | `public.search_score(field, query)` (migration `20261022214500`) | ONE definition: 100 exact · 80 prefix · 60 word-start · 40 contains, case-insensitive. |
| Binding | `public.owner_alias_claims` + `public.claim_my_alias(p_alias)` (migration `20261022220000_alias_binding_v1.sql`) | The ONE server-controlled uid↔alias binding: a normalized alias belongs to exactly one owner, first claim wins. Every alias decision in the system reads this table and nothing else. |
| Client | `HUB/app/js/naya-search.js` (`window.NayaSearch`) | Query/voice-intent parsing, the store, the command palette, Cmd-K. Holds no ranking and no identity logic of its own. |

## The result shape (every consumer reads exactly this)

| Field | Meaning |
|---|---|
| `object_type` | `person` · `smart_note` · `naya_note` · `mail_thread` · `smart_link`. |
| `object_id` | The object's key: `person_key`, naya-note / smart-link uuid, `thread_key`. Empty for `smart_note` — the wall table carries no id column the repo can evidence, and an id is never invented. |
| `title` | The object's own words: display name · note's first 80 chars · thread subject · link name. |
| `snippet` | One line of provenance: the type, plus the category / author / short URL where the source carries one. |
| `action_kind` | `open_person` · `open_room` · `open_url` — the action that acts on this result. A result without an action is never emitted. |
| `action_target` | For `open_person`: the `person_key`. For `open_room`: the Hub room id (`feed` · `lists` · `mail`); the object ref rides in `object_id`. For `open_url`: the short link (`https://nayanet.live/<name>`). |
| `score` | The ranking ladder's value for the best-matching field. |
| `occurred_at` | When the object last happened (source timestamp; person = last seen). Recency breaks score ties. |

## Sources and their fields

| Type | Source | Searched fields | Owner predicate |
|---|---|---|---|
| `person` | `person_identities` | `display_name` | `owner_id = auth.uid()` |
| `smart_note` | `smart_notes` | `content`, author name | `owner_alias` (normalized) in the caller's bound alias set |
| `naya_note` | `naya_notes` | `text`, `category`, `list_name` | `owner_id = auth.uid()` |
| `mail_thread` | `smart_mail_threads` | `subject`, `participants` | `owner_alias` (normalized) in the caller's bound alias set |
| `smart_link` | `smart_links` (active only) | `name`, `target_url` | `owner_id = auth.uid()` |

Lists are deliberately NOT a source yet: there is no server-side list
store to search (both list worlds are device-local today — map element
#16 tracks the store). When the Smart Lists build lands its store, its
branch joins this service by the same pattern; a surface never searches
a store that does not exist.

## Isolation (the contract's soul)

1. The function takes **no owner parameter**. Identity comes only from
   `auth.uid()`; there is nothing a client can pass to widen its reach.
   The client's request body is `{ p_query, p_limit }` and nothing else.
2. `SECURITY DEFINER` is required (the flagship tables carry no
   repo-governed RLS this function could lean on), so every source
   branch carries its own owner predicate, listed above. The alias
   set is derived inside the function from the server-controlled
   binding `public.owner_alias_claims` — the aliases bound to
   `auth.uid()`, and nothing else. Free-text `owner_alias` on
   caller-owned rows is never a binding: a BEFORE INSERT/UPDATE
   guard on `person_identities` / `naya_notes` / `smart_links`
   routes every such write through the binding and refuses a write
   whose alias another owner claimed first
   (`OWNER_ALIAS_ALREADY_CLAIMED`), and `claim_my_alias` is the
   explicit claim path. (This is the cure round-4 fix for the
   alias-poisoning defect: deriving the set from free text let one
   permitted insert claiming a victim's alias leak the victim's
   alias-keyed rows.) An empty alias set means the alias-keyed
   sources return nothing for that caller.
3. No identity (`auth.uid()` is null) returns **zero rows**. Fail
   closed, never open.
4. EXECUTE is granted to `authenticated` only — revoked from `public`,
   never granted to `anon`. Unlike `resolve_smart_link` (public by
   design), a person's own objects have no public moment.
5. The query cannot widen its own match: LIKE metacharacters (`%`,
   `_`, `\`) in the query are escaped inside `search_score` before any
   pattern is built.

These five are pinned structurally by
`tests/test_universal_search_contract.py`; the client's refusal
behaviors (no session → nothing sent; empty query → nothing sent) are
pinned by `tests/naya_search.test.mjs`.

## Entry points (the five checkable features)

1. **One search surface** — the Hub command palette
   (`NayaSearch.mountPalette`), wired in `HUB/app/index.html`.
2. **Cross-object results** — the service's one ranked set; the palette
   groups it by type without re-ranking.
3. **Act from the result** — Enter or click runs the result's action
   (`open_room` routes `#/hub/:room`; `open_person` routes the
   Connections room with the person ref; `open_url` opens the link).
4. **Voice command** — the palette's mic (Web Speech API where present,
   honestly absent where not). Transcripts reduce through
   `parseVoiceIntent` — "Naya, find Maria" → query `Maria` — onto the
   SAME query path as typing.
5. **Cmd-K parity** — `NayaSearch.installHotkey`: ⌘K / Ctrl-K opens the
   palette from anywhere in the Hub. (The chassis Ask-Naya box is a
   different surface — governed-runtime Q&A — and is untouched.)

## Speed

Every service branch filters on an owner index first, so an everyday
query reads one owner's corpus, never the estate's; the identity
registry additionally carries `(owner_id, lower(display_name))` for
name lookup. The service caps its page at 50 rows; the client's merge
of a deliberately fat 5,000-row page is benchmarked in
`tests/naya_search.test.mjs` (measured latency is stated in the PR and
the build evidence — the number lives where it was measured, not here).
