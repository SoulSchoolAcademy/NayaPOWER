# Organism loops — Smart Mail × Connections × Spaces × Lists (Naya 4, 2026-10-02)

Shawn's law: these are not four apps — they are parts of each other, one
organism. **One graph, four views.** Connections = the people spine, Mail =
the voice, Spaces = the gatherings, Lists = the memory.

Shared spine (implemented): `HUB/app/js/people-registry.js` →
`window.NayaPeople`, local key `naya.people.registry`. Every room resolves
people against it. No competing people stores.

## Loop 1 — Mail → Connections (IMPLEMENTED)

- Mail thread from an unknown sender → `ADD TO CONNECTIONS` → the person
  is filed into the shared registry with role `via Smart Mail`.
- Connection card → `WRITE MAIL` → `ctx.composeRequest` hands the person
  to Smart Mail's composer, pre-addressed.
- Both directions tested in the stub-DOM suites.

## Loop 2 — Connections → Mail compose (IMPLEMENTED)

- `+ Add person` in Connections writes straight into the shared registry.
- The new person appears in Smart Mail's recipient list on its next read.
- No dead buttons: `WRITE MAIL` only renders when `ctx.onCompose` exists.

## Loop 3 — Mail → Space feed (IMPLEMENTED 2026-10-02)

Contract: **a mail addressed to a space IS a post in that space — same
object, two views.**

- Smart Mail's composer already addresses spaces (`toKind:'space'`).
- On send, when `msg.toKind==='space'`, Smart Mail appends
  `{ts, text, author}` to localStorage `naya.smartspaces.posts[msg.to]`
  (cap 100 per space).
- Smart Spaces reads that key on load — the post appears in the space
  feed with zero changes to spaces.js.
- The thread also lives in Smart Mail (sent folder). Delete the thread
  in mail and the space post remains (independent views of one send;
  cross-view delete is a future spec, not silent behavior).
- Tested: post lands, carries the sender's name, thread exists in both.

## Loop 4 — Thread → Smart List (SPECIFIED, not built)

Contract (for the shell / list lane — do NOT build a competing note store):

- A thread the user marks "worth keeping" should be fileable as
  intelligence into Smart Lists.
- Smart Lists' notes arrive via `ctx.notes` (shell-fed); its local store
  `naya.smartlist` holds `{custom, tabs, hiddenTabs}` — there is no
  user-note creation path yet.
- Proposed contract: a writer key `naya.smartlist.inbox`, an array of
  `{id, kind:'thread', threadId, subject, excerpt, ts, from}` written by
  Smart Mail's `FILE IN SMART LIST` action; Smart Lists reads it and
  surfaces a "FILED FROM MAIL" section, the same way it already surfaces
  "SAVED FROM TODAY" from `nayanet.today.smartlist.v1`.
- Status: needs the list lane's read side. Until then, no button — a
  writer nobody reads is a shell, and shells are the enemy.

## Loop 5 — Space → Mail (already existed)

- Spaces calls `ctx.onMail(space, text)` when a message is posted from a
  space; the shell wires it to Smart Mail's composer.
