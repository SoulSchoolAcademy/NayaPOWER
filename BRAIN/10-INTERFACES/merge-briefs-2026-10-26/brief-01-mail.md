# DESIGN BRIEF — 01 · MAIL: one mail, the right one survives

**Pair:** `/rooms/mail` (SURVIVOR) + `/personal#inbox` (DELETED outright)
**PI item:** `mail-right-one-20261026` (owner Nitro, in motion)
**Order in build sequence:** 1 of 7

## Contract read
Design Contract + Master Contract (canonical links in the Toolkit §3). The briefer read the Design Toolkit in full — `BRAIN/10-INTERFACES/NAYA-DESIGN-TOOLKIT.md` at main tip `57866113ca22c48c1580db8489ca8e35b88d6682`, blob `9bf8e446`, 6,546B — and this brief is written to its §4 template. The builder states their own contract read in the build pass before code (Toolkit §1.1: no code before the study is recorded).

## Factory / approved-page study notes
- **Nitro's rendered study** (board #3066, comment 6406233253; `mail-study/STUDY.md`, 4 screenshots, on Nitro's box): rooms/mail is a REAL mail app — brand, guide + play, + COMPOSE, Search mail, ALL / WITH NOTES / UNREAD, a real thread card, folders behind it (inbox, unread, sent, scheduled, smart posts, drafts, contacts, smart lists, spaces). Fit defect measured by her eyes: **overflow 102px at laptop width, 32px on the phone.**
- **Power's flagship inventory study** (guest view 2026-10-26 01:05–01:09Z; delivered file read in full by the briefer): the shared brand language — near-black backgrounds, white headings, gray-white secondary text, purple/violet primary accent, pill buttons and textboxes, rounded-rectangle cards, circular icon/avatar buttons, thin light or purple rims, glowing rims on primary actions, letter-spaced small capitals for labels, layered-card elevation with light-burst sheen.
- **Factory inventory status (named gap):** the Smart Factory inventory (404 unified pieces) and `team-nitro/DESIGN-LANGUAGE.md` are on Nitro's box, moving to GitHub under PR #3075 — **unreachable from the briefer's seat**. The builder holds both and maps each harvested element to its Factory piece at build time, or names the gap on the board. Never invent around it (Toolkit §3).

## Measured facts (briefer's byte probes, 2026-10-26 ~02:31Z; saved under `hidden_files/merge-briefs/probes/`)
- `/rooms/mail`: 200, **260,664B** (byte-identical to the 2026-10-26 audit), viewport meta PRESENT (quote-agnostic check), title "Smart Mail — NayaNET". Strings verified in served bytes: `COMPOSE`, `Search mail`, `WITH NOTES`, `UNREAD`, `scheduled`, `Smart Posts`, `drafts`.
- `/personal` flagship template: 200, **602,710B**, viewport present (single-quoted attribute — the audit's corrected finding). Strings verified in served bytes: `Smart Mail Inbox`, `Connection unavailable`, `Message this app`.
- Hub shell (`nayanet.live/`, 5,438,679B): references the hub mail route; "inbox" appears 14× in shell bytes. Nitro's rendered finding: the hub Inbox tab currently points at the DEAD personal section.

## Harvest inventory (element — source — proof)
- **The survivor's own mail chrome, kept whole** — compose action, search, ALL/WITH NOTES/UNREAD filters, thread card, folder rail (inbox · unread · sent · scheduled · smart posts · drafts · contacts · smart lists · spaces) — source: `/rooms/mail` served page — proof: [live bytes: strings above] + [rendered study 6406233253]. Edit-only: this page is the authority; the merge adds nothing to it except the fit fix.
- **Glowing-rim primary-action treatment** (for COMPOSE after the reflow) — source: Projects page CREATE PROJECT pill (purple gradient, glowing rim, white letter-spaced capitals), Power's flagship inventory study — proof: [rendered study]. Map to Factory piece at build time.
- **Shared brand language** (near-black, white text, purple/violet primary, pill forms, letter-spaced small-cap labels) — source: Hub + Welcome + Projects + Identity, Power's study — proof: [rendered study] + [audit signal counts: shell 140 gradients / 41 keyframes / 45 media queries].
- **NOTHING is harvested from `/personal#inbox`.** The study is explicit: no feature moves. An error card has no elements worth keeping.

## What dies / what survives / what is harvested from the loser
- **Dies:** the `/personal#inbox` section — the "Smart Mail Inbox" card reading "Connection unavailable" — removed outright. No stub, no placeholder, no redirect card. The hub Inbox tab stops pointing at it in the same pass.
- **Survives:** `/rooms/mail`, whole, as the ONE mail. The personal page's **"Message this app" visitor form STAYS untouched** — it is a message door, not an inbox (string verified in template bytes; do not let the section surgery touch it).
- **Harvested from the loser:** nothing. Stated plainly so no one goes looking.

## Shared-records / wiring requirement
- The hub Inbox tab and the dashboard smart tabs open `/rooms/mail` — the same app, the same records, active from the hub. One mail store; no in-shell twin inbox state.
- **Template-surgery warning:** the loser is a section of the shared flagship template that also serves Personal / Business / Space / Dashboard faces. The deletion must be proven against ALL flagship faces rendered after the edit (see Proof).
- **Privacy boundary:** this brief does NOT make Smart Mail private. The mail privacy fitting stays its own gated track (audit note on the mail page item); this surface job claims nothing about privacy.

## Fix on the survivor (part of "high level")
- Overflow: 102px laptop / 32px phone (study measurements) → **0px at 1280 and at 390**, measured, phone first (Toolkit: mobile first, review by measurement).

## Scorer + verifier
- **Builder:** Naya Nitro. **Scorer + verifier:** Naya Resolve — rendered review at the real address (phone AND laptop) + scorecard, different seat from the builder. The scorecard posts under Resolve's seat identity; if the formal different-login prong needs a distinct GitHub login, that is named at scoring time, never assumed.
- **Deploy:** on the director's tap, after the scorecard.

## Proof required before announcement
Rendered review still owed — every measurement in this brief is byte probes + the cited rendered studies; **no rendered proof exists yet**. Required before anything is announced: (1) staged render phone + laptop, overflow measured 0px at 390 and 1280; (2) SIGNED-IN citizen view — real mail, real threads, hub Inbox tab landing on the same mail; (3) all flagship faces rendered post-surgery (personal page intact, visitor message form working); (4) different-seat scorecard ≥ 9.0. Byte checks are not a review (Toolkit §2).

## Land bar
**9.0 or better**, with link + verification + reconciled counts. Never overwrite the proven mail page with unproven work.

## The lesson this brief carries
An error card wearing a feature's name is worse than no feature — it teaches the citizen the system lies. Stubs that inherit real names get deleted outright, and the door that pointed at them gets repointed in the same pass.
