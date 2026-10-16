# WAVE 2 NOTES — comments · chat · onboarding

9 blocks, 3 families, all shippable specs. Built 2026-10-16 by three parallel builders (seat Nu), coordinated merge with collision repair.

## What shipped

**COMMENTS (CMT-001…003)** — `comments-blocks.md`
- CMT-001 Comment thread: composer (Post truly inert until text), honest 2px depth rails to a hard cap of 3, then a dashed "Continue thread" panel that names the cap; collapse/expand with real counts; tombstones; plain-words timestamps over real datetimes.
- CMT-002 Single comment: the atom — 52px avatar diamond, serif name, action row (reply purple / love pink toggle / share blue), honest 4-line clamp keeping full text in the a11y tree.
- CMT-003 Reaction row: jewel pills, toggle with held-glow "mine" state, fixed five-reaction set in wheel order; zero-count reactions absent, never grayed. No badges, no streaks, no "top fan".

**CHAT (CHT-003…005)** — `chat-blocks.md` (renumbered: CHT-001/002 belong to the chart family in the main catalog)
- CHT-003 Chat bubbles in/out: incoming white-lit edge vs outgoing held purple edge; rotated-square tails; group collapsing (<5min same sender); read receipts as four forward-only truth-states (sending→sent→delivered→read/gold SEEN), single-writer setReceipt contract.
- CHT-004 Typing indicator: three dots at 72bpm, calm; signal-gated render (throws without live signal id); 30s watchdog dismisses honestly, fires `chat:typing-expired`.
- CHT-005 Message list: serif date dividers, 64px-edge scroll contract (sticks only if already at bottom, else a 44px "New messages" pill with honest count), "No messages yet — say the first word."

**ONBOARDING (ONB-001…003)** — `onboarding-blocks.md`
- ONB-001 Stepper: 5-step rail, jewel nodes on the 5-stop strip, spectrum thread fill from real index, optional steps honestly chipped; "No steps yet — this is not step zero of five."
- ONB-002 Welcome card: Naya face in SVG with breathing halo, exactly one 52px CTA, one quiet exit, visible footnote: "This card knows only what you've told it." Ships nameless; name fills from data-name only.
- ONB-003 Progress indicator: linear + ring from one source of truth; honest indeterminate ("No number yet"), never fake 99%; one 1.1s gold ignition on complete, then calm.

## Key decisions

- **ID repair:** chat shipped as CHT-001…003 but CHT-001 (Chart/Data-viz) and CHT-002 (Metric ribbon) already exist in BLOCK-INDEX.json. Renumbered to CHT-003…005 in both spec and index before merge. Lesson for wave 3: check prefix ranges against the main index *before* briefing builders.
- **Truth-states everywhere:** read receipts, typing, percentages, reaction counts — nothing renders a state it didn't earn. Each family states its honesty contract once at top ("What it will NOT fake") and enforces per block.
- **Reaction color table fixed** (love pink, celebrate magenta, thoughtful purple, agree blue, laugh green; sixth indigo) — shared by CMT-002/003 as one object, one count, one truth.
- **Purple = my voice, gold = seen** (chat); **gold reserved for today/completion** across families — wheel discipline held.
- **Calm motion law:** 72bpm typing, 1.1s single ignition, prefers-reduced-motion on onboarding. Living, never jittery.
- **Private-by-default:** display names only, no emails/handles; content renders in bubbles and nowhere else; tombstones leave no remains.
- **Deliberately out (named, not implied):** moderation queues, report flows, rich mentions, threaded DMs, composers, voice notes, message reactions, branching onboarding flows, streaks, badges → CMT-004+, CHT-006+, ONB-004+.

## Verification

- 9/9 HTML blocks parse clean; CSS braces balanced (57/57, 14/14, 19/19 comments; chat + onboarding verified by builders).
- Zero yellow-hex hits across all three specs (gold `#ffbf3d` only).
- All four parts + "What it will NOT fake" on all 9 blocks.
- `gap-blocks-2-index.json`: 9 entries, exact 10-key set, parses via json.tool, zero collisions vs 191 existing ids (181 main + 10 wave-1).

## Remaining gaps (build order)

Per BLOCK-GAPS.md, after this wave: notification center (HIGH), error state block (HIGH — Law 75), form validation states + file upload (HIGH), auth companions signup/reset/SSO (HIGH), then profile cover + stats row, lightbox, video playlist, pagination (MEDIUM). Calendar + checkout (CRITICAL) closed in wave 1; comments + chat + onboarding (HIGH) closed here.

## Merge path

`gap-blocks-2-index.json` is a merge fragment: 191 → 200 at adoption into BLOCK-INDEX.json. Specs adopt into DESIGN/BLOCKS.md via the catalog lane. Repo untouched by this wave per constraints.
