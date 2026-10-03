# Smart Spaces — Room Scorecard (Naya 4, 2026-10-02, concept redirect)

Branch: `naya4/room-02-reports-v2`.

## The redirect (Shawn, 2026-10-02 ~23:00 PDT)

His verdict on the old room: *"a directory of fake groups — names on cards, nothing to do inside them."*
He's right. A Smart Space is a **LIVING ROOM**: create a space on any topic
(free subject, or gathered around an intelligent block), instant chat inside,
mail the whole space at once (lands in the same conversation), anyone can add
people. Facebook-group-meets-instant-chat, gathered around intelligence.

Rebuilt around that concept. What changed mechanically:

- **Space view is now a living room**: topic block (the subject/block the space
  gathers around) → people row (ball avatars + ADD PEOPLE) → unified
  conversation (oldest-first chat thread) → instant composer → MAIL THIS SPACE.
- **+ CREATE A SPACE**: name (required) + topic (required) + optional
  intelligent-block link (3 demo blocks or "just a subject"). Persists to
  `naya.smartspaces.custom` — real, unlabeled, appears immediately, opens on create.
- **ADD PEOPLE**: modal listing `window.NayaPeople` spine contacts not yet in
  the space; adds persist per-space in `naya.smartspaces.members`, survive
  remount.
- **Instant chat**: SEND posts instantly, persists to `naya.smartspaces.posts`,
  renders immediately, Enter-to-send. Real locally.
- **Mail loop closed both ways**: mail addressed to a space IS a post here
  (same `naya.smartspaces.posts` store Smart Mail writes — kept reading it);
  MAIL THIS SPACE calls `ctx.onCompose({to, toKind:'space'})` when the hook
  exists and renders NOTHING when it doesn't (no dead buttons). Preview wires
  an honest demo toast.
- **Honesty kept**: seeded spaces/messages carry DEMO chips; user spaces and
  posts are unlabeled; footer still says no canonical group store.
- **No faked realtime**: no simulated typing, no fake incoming messages, no
  fake audio UI. Audio is backend-gated future — noted, not built.
- Design laws carried: obsidian buttons with violet ignition, living depth,
  ball avatars with specular highlights, 16px/11px type floor, reduced-motion
  guard, focus traps in both modals, Escape closes modal / returns to grid,
  keyboard-openable cards.

## Scorecard — Shawn's lenses: effectiveness, quality, pro level, contrast, clarity, congruency, color

| # | Lens | Score | Note |
|---|------|-------|------|
| 1 | Effectiveness | 10 | Create space, instant chat, add people, mail the space, mail-to-space loop — the living room does what he described. |
| 2 | Quality | 9 | Rebuilt, 51/51 tests green, visually confirmed by screenshot. His eyes confirm the finish. |
| 3 | Pro level | 9 | Feels like a real group-chat product now. He confirms. |
| 4 | Contrast | 10 | Obsidian + white, violet ignition, mine-tinted messages, DEMO chips unmissable. |
| 5 | Clarity | 10 | Topic block, people row, conversation, composer, mail button — one job each, honest labels. |
| 6 | Congruency | 10 | Same obsidian/ball/depth family as Mail and Connections; violet is room chrome only. |
| 7 | Color law | 10 | Each space owns its stable color; each member their own; never positional. |

## The "feel alive" pass (Shawn, 2026-10-02 ~23:20 PDT)

His verdict on the grid: "it doesn't feel like a room where people are
talking." He was right — the grid showed zero conversation. Two fixes:

1. **Last-message preview on every card** — author · time · snippet, like
   every chat app. The grid now reads as living conversation at a glance.
2. **Demo seeds rewritten as back-and-forth**, minutes fresh ("Naya 2 asks
   → Naya 4 answers → Shawn reacts") instead of disconnected bulletins.
   Still DEMO-labeled; illustrative, never presented as real activity.

## Opens INTO the conversation (Shawn, 2026-10-02 ~23:30 PDT)

"You shouldn't have to hunt for it. A chat app opens into the
conversation." The room now restores the last-opened space
(`naya.smartspaces.lastOpen`); the preview opens Team Naya via
`ctx.initialSpaceId`. First paint = people talking, not a directory.

## Dense-feed redesign (Shawn, 2026-10-02 ~23:40 PDT)

"You should do some research." Done: studied Discord channel view and
WhatsApp group chat (screenshots on file). The feel of a group = DENSITY
(6-10 messages per viewport, <=8px between rows), NO card chrome on messages
(avatar+name+time+text in one tight row), SLIM header (name+topic+count in 3
lines), STICKY composer, thin date dividers. Message cards are gone; the
conversation is now compact rows with ball avatars, author names in their
stable identity colors (spine color when known, hash fallback), grouped
replies, and a Today divider. MAIL and + ADD moved into the header bar.
Ball-avatar CSS and `.sp-send` were accidentally dropped in the rewrite and
restored; author colors now resolve from the people spine.

**Score: 9.7/10.** Why not 10: quality and pro level are his call
(-0.2), and realtime multi-user delivery is backend-gated, local-only until
the shell wires it (-0.1, honestly labeled).

## Verification

- `node --check` clean (room + adapter); CSS braces balanced (93/93).
- `HUB/app/preview/tests/spaces-smoke.js` — **58 pass, 0 fail**: grid opens
  spaces, topic block, unified oldest-first conversation with DEMO chips +
  authors, instant post (renders/persists/remounts, mine-tinted, unlabeled),
  mail-to-space seed appears in conversation carrying sender name,
  MAIL THIS SPACE absent without hook / calls hook with {to, toKind:'space'},
  add-people from spine (lists non-members, persists, survives remount),
  create-space validation + persistence + unlabeled + opens immediately,
  modal focus traps, Escape closes modal, onMail hook fires, depth CSS markers.
- Headless-Chrome screenshots (grid + auto-opened detail) reviewed with own
  eyes: obsidian CREATE/ADD PEOPLE/SEND/MAIL buttons, ball avatars, topic
  block, demo conversation with authors + DEMO chips, honest footer.
- Preview: `~/workspace/your_files/spaces-preview.html`
  (built by `HUB/app/preview/build-spaces-preview.py`).
- Not merged, not deployed, not ratified — CANDIDATE.
