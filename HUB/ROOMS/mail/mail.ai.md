# Smart Mail — Builder Spec (AI)

**Status:** PROPOSED. **Route:** `hub/mail`. **Accent:** indigo. **Build order:** 8.

## Shell contract

Sidebar + Naya rail unchanged; center swaps. `hub/mail?box=&thread=`.

## Component tree

1. `MailHero` — title + `BoxTabs` (IMPORTANT/RESPOND/FOLLOW UP/DRAFTS/SENT) + Compose.
2. `ThreadList` — threads with presence + authority badges.
3. `ReadingPane` — message thread, beautifully typeset; `ThreadBrief` ("what matters here") on top.
4. `ContextPanel` — who/why/history/related/potential response.
5. `Compose` — writing desk; Send is human-only.

## Data bindings

- Threads ← real message channels via Connect doors. Context ← Connections + Library + thread history.

## States

- `loading`, `empty_box` (honest per box), `no_thread_selected`, `offline` (cached with stamp). Draft vs sent strictly typed.

## Interactions

- Box tab → re-query. Thread select → reading pane + context. "Ask Naya to brief" → in-panel summary from real messages. "Ask Naya to draft" → draft marked DRAFT-BY-NAYA. Send → human press only → Ledger receipt.

## Design tokens

Indigo depth; letters-on-desk cards; reading pane with generous measure.

## Acceptance

No send path without human press (verify in code); drafts clearly marked; authority states visible pre-action; 9.0+.
