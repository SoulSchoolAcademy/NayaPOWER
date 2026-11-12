# PROJECT INTELLIGENCE — BUILD INTELLIGENCE FOR NITRO
### From Naya Resolve · 2026-10-26 · the distilled essence of everything the face must be

## THE ESSENCE — read this first, build from this

Project Intelligence is the team's one working home made visible. It is not a report and not a dashboard of numbers — it is **a living map of the whole system that answers five questions in five seconds**: What matters now? What's blocked? What moved since I last looked? What's next? Where do I go to see it?

If a cold visitor — Shawn, a new citizen, a fresh Naya — cannot answer those five from the first screen, unaided, the face has failed no matter how beautiful it is. Beauty is required too (the Elevated Standard is law), but it serves the five answers, never replaces them.

**The one law underneath everything: if it's not written in the record, it's not done — and if the face shows it, it must be traceable to the record.** Every pixel is either computed from `work_items` or it does not ship.

## HOW THE SYSTEM THINKS — the organizing logic

1. **One record, three tongues.** The same truth renders three ways: HUMAN (front, plain words, the default), AI (exact values, procedures, constraints), MACHINE (structured). Every entry carries all three; the human view leads, the other two are one tap away. Never three different truths — one truth, three languages.
2. **Organized by interfaces — the face is a MAP.** The home is a map of the system's 12 areas. Each area is a room. Each page inside a room is a card. Navigation is walking the map, not searching a list.
3. **Two scores on everything.** Every area and every page carries an ENGINE score (the machinery under it) and a PAGE score (the surface itself). A pretty page on a dead engine shows both numbers — that honesty is the product.
4. **Priority is a computation, not a maintained list.** What rises: director's order first, then what blocks the most other work, then value, then age. What completes drops off by itself. Until the system computes this live, the face renders the record's priority order — and never a hand-arranged one.
5. **Movement is a first-class citizen.** The face shows what changed since the visitor last looked, per section. A quiet face on a working day is an ALARM state, visually distinct — never rendered as peace.
6. **Proven is different from claimed, visibly.** `done_proven` means evidence attached AND a different seat proved it. The face must render proven, in-motion, and merely-claimed as visually distinct states. Conflating them is the one unforgivable sin of this interface.

## PLACEMENT LAW — what goes where, and why

### The home (director's surface), top to bottom
1. **The lead sentence + the numbers.** One plain-words sentence saying where the whole project stands, then the headline numbers — percent proven done, in motion, blocked, needing a decision — **each with a plain-words caption** ("46 of 355 proven done — finished work, independently verified"). A number without its caption is a defect. **Every number is a DOOR**: tapping it opens the actual rows it counts.
2. **Needs-your-hands rail.** ONLY what is genuinely director-gated (his named gates: money/credentials, production database, irreversible, ratification, authority/security). Everything else appearing here is a bug — his attention is the scarcest resource in the system.
3. **The weakest three.** The three lowest-scoring parts of the whole system, named with their scores and the one-line reason. Weakness leads; the system does not hide its floor.
4. **The map — 12 area cards.** Each card: a real ICON (never a dot), the area's name, its computed percent proven done, its ENGINE and PAGE scores (or DARK with the reason printed), and a one-line preview of the area's current truth ("voice queue curing, first-sound proof owed"). The card is a door into the room.
5. **The master to-do.** The whole program in priority order — director's order as the spine — each row openable to full detail.
6. **Movement.** What changed since you last looked, then the recent activity stream (the pulse).

### An area room
- Header: what this area IS (one plain sentence), its two scores, its percent done.
- **Per-page cards**: every page in the area as its own card with its own percent done and an **Open control that goes to the real page** — not a description of it, the page itself.
- **Per-page completeness lists, split two ways**: INTERFACE (what the surface still owes) and FUNCTIONALITY (what the machinery still owes). Never one blended list — the split is how a reader knows whose work it is.
- The area's items as rows, priority order, each row openable.
- **Notes on anything**: every object on the face — area, page, item, list — accepts a note, and the note lands ON the object, in the open. Notes are how the team talks inside the record instead of around it.

### An item, opened
Full detail: the three tongues, the exact state, maker and prover named, the evidence link (a "go see it" that lands on the finished thing), its notes, its history of movement.

### The seats' working surface
One tap deeper, tied to the same record: queues, claims, the operational depth. Shawn's surface stays clean; the machinery of work is never hidden, just never in his face.

## THE 12 AREAS (the map's rooms)
`pi-hub` (the record itself) · `welcome` (birth chain, first citizens) · `connection` (Connect + other AIs, one door) · `mail-notifications` (Smart Mail + the pulse) · `match` (auto-match engine) · `factory-interfaces` (the Factory + Smart Factory) · `membership-money` (membership, courses, pricing, affiliate) · `hub-dashboard` (the Hub home + citizen dashboard) · `projects-spaces` (Projects + Spaces) · `voice-audio` (voice everywhere) · `identity-settings` (identity/certificate page + Settings) · `security-privacy` (privacy locks, the audit family).

## LABELING LAW — how things are named

- **Exact state language, always**: QUEUED · IN MOTION · BEING CHECKED · PROVEN DONE · BLOCKED · NEEDS DECISION. No synonyms, no softening. A thing is what the record says it is.
- **Plain words on every human surface.** No shorthand, no seat jargon, no internal codes in front of a human. If a grandmother couldn't follow the caption, the caption is wrong.
- **Two voices**: seat-to-seat text is literal (states, keys, scores); human-facing text is plain terms PLUS a clickable deep link onto the item itself. A human notice without the link fails the standard.
- **Numbers always carry captions** (see Placement). Percent done is always "X of Y" underneath — a bare percent is a claim, "46 of 355" is evidence.
- **Dark means dark**: anything unmeasured shows DARK with the reason ("not yet measured — no engine wired") instead of a zero or a guess. An honest dark is worth more than a lit lie.

## THE DATA CONTRACT — what you build against

- **Single source**: `public.work_items` (via its published projection). The face renders **ROWS, not counts** — every count on screen must be openable into the exact rows it counts. The current face's counts-only snapshot is the core defect being cured.
- **Computed, never typed.** No number, percent, or score is hand-entered anywhere in the face. If it can't be computed from the record, it renders dark-with-reason.
- **Freshness per section**: every section carries its own "as of" — a stale section says so on its face.
- **The record's current truth** (so you build for the real data, not the brochure): ~355 rows, of which ~46 raw / 40 unique proven done; duplicates exist (a dedup dataset with survivors is being prepared); ~179 items carry no trustworthy area yet (an item-by-item area dataset is being prepared — when it lands, every row arrives placeable); owner names need normalization (also in that dataset). Build the face so data quality improves underneath it without redesign: when the mapping lands, rooms fill; until then, an item with no area shows in its best-known place with its state honest.
- **Links cure**: every link lands on the current board (#3066), the live page, or the item itself. No staged, retired, or placeholder links anywhere.

## LIFE + LOOK — the Elevated Standard applied

- **Icons, never dots.** Shawn scored the current face down for dots; each area and part gets a real icon in the system's icon grammar. Color carries logic (state colors consistent everywhere); jewels, not dots.
- **Alive**: elements respond and move the way the approved pages do — the Life with Naya play button is the reference for "alive." **Shop from our own shop**: reuse elements from the approved pages (Life with Naya · the certificate page); never reinvent an element that already passed.
- **Contrast + elevation are their own passes**: high-contrast text, perfect placement and spacing, exactly what's needed and nothing more — awe-inspiring and push-button simple at once.
- **Tabs in the Smart Tabs pattern**, boards lighting in their own color (his Round-2 direction).
- **MOBILE FIRST — law.** Most of the world arrives on a phone. Every view is designed and proven at phone width (390px) FIRST, then laptop — and laptop must also be great. A page that fails on the phone cannot score 10, full stop.

## WHAT MATTERS MOST — when trade-offs bite

Truth of the numbers → doors that actually open → movement visible → beauty. In that order when forced to choose — but the standard is all four, and the last face failed on the first three, not the fourth. Shawn's words on the current face: overall 4/10, "5 would be a pass; this does not pass." The target is not a pass. It is a 10 he can cold-open.

## ACCEPTANCE — how we will know it's right

1. **The 42 checks** (already in the repo under `HUB/PROJECT-INTELLIGENCE-FACE-CHECKS.*` — build against them line by line; a build check closes only when its content renders LIVE, not when the code exists).
2. **The words are already written** (`HUB/PROJECT-INTELLIGENCE-FACE-WORDS.*`) — B7–B12 drafted in full: area descriptions, preview lines, captions. Your slots are waiting for words that exist; take them.
3. **The parts register** (`HUB/PROJECT-INTELLIGENCE-PARTS-REGISTER.*`) — every part of the face, scored; your build moves those scores.
4. **Cold-open test**: a fresh seat (or Shawn) opens it cold and answers the five questions in seconds, unaided. Then phone-width proof. Then my cold check as the different seat. Then it lands — decided by the scores, not by a tap.

## WHAT I OWE YOU, AND WHAT'S IN FLIGHT

- The readiness dataset (item-by-item areas, dedup survivors, owner normalization) — building now; lands as a file you and Power consume.
- The full inventory (everything that should be in PI, why, where — including the gap list) — building now; when it lands, what the face must hold is settled for every seat.
- Anything the face needs from the record that isn't there yet: ask me, addressed, on the board — the 15-minute clock is law now and I work under it too.

— Naya Resolve Narzan, main seat. This brief, the checklists, the words, and the parts register are one kit. Build the map, Nitro — we'll prove it cold together.
