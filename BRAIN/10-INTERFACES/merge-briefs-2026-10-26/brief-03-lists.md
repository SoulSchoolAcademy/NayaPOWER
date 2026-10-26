# DESIGN BRIEF — 03 · SMART LISTS: the overhaul, to the director's definition

**Surfaces found (THREE, not two — see Measured facts):** `/rooms/lists` standalone app · the hub shell's lists surface · `/personal#lists` fragment (DELETED)
**PI item:** `lists-overhaul-20261026` (owner Nitro, in motion)
**Order in build sequence:** 3 of 7
**Director's score on the current state: 1/10 — "if not a minus."**

## The spec (the director's definition IS the spec — no other spec outranks it)
Smart Lists is **where feed saves land**: clicking save on the main feed saves the note here. It is groupings of smart notes by topic/category. A list can be **added to a project**, **sent to a user**, or **kept private**. Lists can hold **smart notes AND Naya notes, connections, projects, pages/apps** — anything saved or favorited lands in the Smart Lists area, then gets organized into lists, nicely categorized. Mostly notes + connections in practice. It is an organizational system, not a page of cards.

## Contract read
Design Contract + Master Contract (canonical links in the Toolkit §3). The briefer read the Design Toolkit in full — `BRAIN/10-INTERFACES/NAYA-DESIGN-TOOLKIT.md` at main tip `57866113ca22c48c1580db8489ca8e35b88d6682`, blob `9bf8e446`, 6,546B — and this brief is written to its §4 template. The builder states their own contract read in the build pass before code (Toolkit §1.1).

## Factory / approved-page study notes
- **Nitro's rendered study** (board #3066, comment 6406326544; `lists-study/STUDY.md`, 1280+390, 0px overflow, on Nitro's box): personal#lists names the category idea right ("a category you file things into… the same lists on every door and device") but delivers one empty list, device-local, "filing and sync wait." The hub lists surface greets with an **Install modal blocking the whole view**; behind it a concept page (living lists, action intelligence, NOW/NEXT/WAITING…) in an honest unconnected state — no actual lists, no saved notes, no send/project actions.
- **Study's overhaul shape:** keep the dedicated lists app as the one home; the personal fragment goes; the personal Lists tab opens the one app; the app opens on your lists.
- **Factory inventory status (named gap):** the Smart Factory inventory (404 pieces) and the design-language extraction are on Nitro's box, moving to GitHub under PR #3075 — **unreachable from the briefer's seat**. The builder maps harvested elements to Factory pieces at build time or names the gap on the board.

## Measured facts (briefer's byte probes, 2026-10-26 ~02:31Z; saved under `hidden_files/merge-briefs/probes/`)
- `/rooms/lists`: 200, **339,789B** (byte-identical to the audit), viewport PRESENT (quote-agnostic), title "Smart Lists". Strings verified in served bytes: `NOW`, `NEXT`, `WAITING` (the status vocabulary), `category`, `project`, `private`, `note`. **`send` is ABSENT from the app bytes** — the director's "send a list to a user" has no presence in the current build.
- `/personal` flagship template (602,710B): the fragment's category definition string **`category you file`** verified in bytes; the section is one of the shared template's sections (see template warning below).
- Hub shell (5,438,679B) contains a lists surface (the modal-greeted one, per the study). The literal route string `hub/lists` does NOT appear in shell bytes — navigation is by section, not by that path string.
- **Route ambiguity, stated plainly:** three list surfaces exist by bytes and study. The study names "the hub lists route" as the one home, but a distinct standalone app also serves at `/rooms/lists`. **The builder's first act is to prove which served bytes are the citizen's lists home at the real address; exactly ONE app survives as home, and the other surface becomes a door to it or is removed.** This brief does not guess.

## Harvest inventory (element — source — proof)
- **The category definition, in the fragment's own words** — "a category you file things into" + "the same lists on every door and device" — source: `/personal#lists` — proof: [live bytes: `category you file`] + [rendered study 6406326544]. Harvested as the area's plain-words explanation AND as the promise the sync wiring must make true.
- **File-a-note-or-person action shape** — source: personal fragment per study — proof: [rendered study]. The filing gesture survives; its device-local backend does not.
- **Status vocabulary as VIEWS** — NOW / NEXT / WAITING — source: hub lists concept surface — proof: [live bytes in `/rooms/lists`: all three strings] + [rendered study]. Under the one-area law these become views WITHIN the one area, never separate pages.
- **The surviving app's own chrome** — whichever surface wins the route proof, its existing lists presentation is the edit-only base — proof: [live bytes] + [rendered study]. 
- **Killed, not harvested:** the Install-modal-first greeting. The app opens on your lists.

## What dies / what survives / what is harvested from the loser
- **Dies:** the `/personal#lists` fragment; the modal-first greeting; the concept-page state (honest-unconnected is still unconnected — it gets connected or it goes).
- **Survives:** ONE dedicated Smart Lists app. The personal Lists tab opens it. The hub door opens it.
- **Harvested from the fragment:** the category definition + the same-lists-every-door promise (made true) + the filing gesture. Nothing else — the fragment delivers one empty list.

## Build requirements (from the definition — these are features, not polish)
1. **Feed saves land here.** The save action on the main feed writes into Smart Lists. (Wiring seam with the feed — the feed's data endpoints are named in the page registry; the builder proves the real save path at build, does not assume it.)
2. **Mixed contents:** smart notes, Naya notes, connections, projects, pages/apps in lists.
3. **Organize:** groupings by topic/category, per the harvested definition.
4. **List → project:** a list can be added to a project (`project` string present in current bytes — prove the action works, not just the word).
5. **List → send:** a list can be sent to a user. **ABSENT from current bytes — this is a build, named as a gap, not a harvest.**
6. **List → private:** kept just for you (`private` present — same prove-the-action rule).
7. **Sync:** the same lists on every door and device — the fragment's promise, made true; device-local-only storage is the defect being removed.

## Scorer + verifier
- **Builder:** Naya Nitro. **Scorer + verifier:** Naya Resolve — rendered review at the real address (phone AND laptop) + scorecard, different seat from the builder. The scorecard posts under Resolve's seat identity; if the formal different-login prong needs a distinct GitHub login, that is named at scoring time, never assumed.
- **Deploy:** on the director's tap, after the scorecard.

## Proof required before announcement
Rendered review still owed — this brief rests on byte probes + the cited rendered study; **no rendered proof of the overhauled app exists yet**. Required: (1) staged render phone + laptop, 0px overflow measured, app opening on real lists (no modal gate); (2) SIGNED-IN citizen view — a note saved from the feed lands here, gets filed into a list, the list is added to a project, sent to a user, and kept private — each action proven, not screenshotted once; (3) same lists read back on a second door/device; (4) different-seat scorecard ≥ 9.0 — against the director's 1/10 baseline, the delta is the receipt.

## Land bar
**9.0 or better**, with link + verification + reconciled counts.

## The lesson this brief carries
When the director can state the product in one breath, that sentence is the spec — where the build can't do the sentence, the build is wrong. And count your surfaces before you merge them: this pair had three.
