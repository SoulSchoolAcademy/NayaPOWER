# The Build Plan — one system that builds itself

**In a nutshell:** Five areas. Each one has a contract: what it is, what goes where, how it works, what's done, what needs doing, who owns it. The machine runs them non-stop until every area scores 9.5+.

---

## Area 1 — The Design Language (the Lego box)

**What it is:** One visual language for everything. Buttons, boards, jewels, blocks — each exists once, canonically. Pages consume blocks; they never reinvent them.

**What goes where:**
- `HUB/design-system/100-LAWS.md` — the doctrine (all 100 laws)
- `HUB/design-system/tokens.css` — the single token set every page links
- `HUB/design-system/catalog.html` — the Lego box lid: browse every block
- `HUB/design-system/library/` — the source workshops (buttons, jewels, blocks, showcase)
- `HUB/design-system/README.md` — the law in short form + builder quickstart

**How it works:** A builder needs a button → opens the catalog → copies `.naya-btn` verbatim → varies only the variant class. Need a new element → build the block first (code + states + screenshot), then the app.

**Completed:** v1 organized and pushed — draft PR #2705. Tokens extracted. Catalog live. Dupes consolidated.

**Needs doing:**
1. Extract the single canonical `.naya-btn`, board, and jewel blocks (Law 92: take the actual code)
2. Build the 10 missing blocks (input, modal, toast, table, search, toggle, card, media player, chart, share sheet)
3. Re-skin all 12 rooms onto `tokens.css` — keep what's good (Reports, Hub shell, Get Started), consolidate the rest
4. Law-by-law audit of every page (Law 99) — scorecard before showing Shawn

**Owner:** Naya 4 (Clarity) + design lanes

---

## Area 2 — Room Contracts (sender → bridge → receiver)

**What it is:** Every room gets a contract naming three things: the **sender** (what emits data), the **bridge** (how it travels), the **receiver** (how the room renders it). No room is done until all three are named and working.

**What goes where:**
- `HUB/MASTER-BUILD-CONTRACT-v1.md` — the master contract (draft PR #2700)
- `HUB/ROOM-RECEIVER-CONTRACTS-v2.md` — per-room receiver specs

**How it works:** A Smart Note is captured → the sender shapes it into the Smart Note block schema → the bridge carries it through Supabase realtime → the room's receiver renders it as a living card. Each leg is independently testable.

**Completed:** Master contract drafted. Receiver contracts v2 specified. Supabase tables live with realtime publication.

**Needs doing:**
1. Ratify the master contract (score → consensus → Shawn's word)
2. Install receiver contracts as real code in each room (today: all rooms are local-only)
3. Wire rooms in order: Today → Mail → Lists → Spaces → Connections → Library → Ledger
4. Connect rooms to each other — a hub you can't walk through isn't a hub

**Owner:** Team Naya lanes (bridge + rooms)

---

## Area 3 — The Data Pipe (Supabase + GitHub)

**What it is:** Supabase is the live database (what's happening now). GitHub is the archive (what happened, permanently). Smart Notes land in Supabase first, archive to GitHub second.

**What goes where:**
- Supabase: `smart_note_events`, `smart_note_receipts`, `smart_note_artifacts`, `nayanet_intelligent_blocks`, `nayanet_smart_ledger` + Smart Mail tables
- GitHub: the repo — code, contracts, the design system, the archive

**How it works:** Capture → write event to Supabase (realtime notifies rooms) → archive the payload to GitHub → room renders within 60 seconds.

**Completed:** Tables created, realtime enabled, 30 Smart Note events verified live. (Shawn + Naya Resolve's win.)

**Needs doing:**
1. Capture the table setup as versioned migrations (not click-ops)
2. Privacy rules for Smart Mail tables (needs Shawn's explicit word before applying)
3. Finish the bridge sender (PR #2701 — four corrections owed by the builder)

**Owner:** Team Nitro (data layer) + Naya 4

---

## Area 4 — The One Flow (Smart Note → Hub, end to end)

**What it is:** Shawn says "smart note this" → it appears on the Hub as a living card he can read, play, save, and share — within 60 seconds.

**How it works:** Capture inbox → six-layer payload → Supabase write → GitHub archive → Today/Smart Feed renders the card.

**Completed:** Capture adapter scores 9.5/10 in isolation. Pipe verified. Receiver shape exists in the Today room.

**Needs doing:** The full observed run — a real Smart Note traveling the whole path and rendering on a deployed Hub page in a live browser. Nothing is "done" until this is seen.

**Owner:** Naya 4 (proof closer)

---

## Area 5 — Team Operations (the machine that runs the machine)

**What it is:** Twelve lanes working non-stop, every piece of work scored, every lesson captured, every update to Shawn in human language.

**How it works:** Dispatcher assigns → lanes build → scorer grades → lessons distill into the system → Shawn gets the human-language report with a clickable link.

**Completed:** Lanes running (tick ~569), 1,100+ receipts scored, learning loop live, Smart Note language law locked in.

**Needs doing:** Keep the bar at 9.5+. Keep updates in human language — the code-talk stays on the team feed. Never stop.

**Owner:** All seats, directed by the math

---

## The order of battle

1. **Design language to canonical blocks** (Area 1.1–1.2) — so every build from here is Lego, not craft
2. **The one flow, observed** (Area 4) — the moment everything is for
3. **Room wiring, Today first** (Area 2.4 + 3.3) — the faucet on the pipe
4. **Room re-skins** (Area 1.3) — twelve dialects become one family
5. **Contracts ratified** (Area 2.1) — the paperwork that locks it in

## The standing rules

- Done means observed in a live browser, with a clickable link. Specified ≠ implemented ≠ merged ≠ deployed ≠ observed.
- Every landing is scored. Below 9.5 goes back with the named gap.
- Updates to Shawn: Smart Note language first — nutshell, what happened, why, what it's for, how it connects, why it matters.
- Protected gates need Shawn's word: production deploys, credentials/money, destructive actions, ratification, privacy/security changes.
- The machine never stops. Build → test → upgrade → scorecard → repeat.
