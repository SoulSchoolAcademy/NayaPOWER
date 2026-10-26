# DESIGN BRIEF — 06 · GROWTH: one master app, one invite, one meaning

**Pair:** `/rooms/growth` (SURVIVOR — the machine) + `/personal#growth` (fragments harvested; personal keeps ONE finished section on the same records)
**PI item:** `growth-merge-20261026` (owner Nitro, in motion)
**Order in build sequence:** 6 of 7

## Contract read
Design Contract + Master Contract (canonical links in the Toolkit §3). The briefer read the Design Toolkit in full — `BRAIN/10-INTERFACES/NAYA-DESIGN-TOOLKIT.md` at main tip `57866113ca22c48c1580db8489ca8e35b88d6682`, blob `9bf8e446`, 6,546B — and this brief is written to its §4 template. The builder states their own contract read in the build pass before code (Toolkit §1.1).

## Factory / approved-page study notes
- **Nitro's rendered study** (board #3066, comment 6406075167; `growth-study/STUDY.md`, 6 screenshots, 0px overflow all views, on Nitro's box): rooms/growth is the full machine — steps Invite/People/Email Sync front and center, invitations, people, contacts, email sync, smart links, automations, waiting-for-your-word proposals (approve/send vs approve/record kept distinct), log. **The director's 2026-10-20 rulings 1–4 are already honored** (no top bar, Hub button beside the plus, founding banner above Install, steps first). **Ruling 5 — the TEXT DIET — is NOT honored: paragraphs everywhere. That is this merge's main design work.**
- personal#growth is fragments, not a machine: invite journey, a record-only Invite-a-friend card, My Smart Link, report counts. NO proposals, NO log. And a LIVE DEFECT in the fragment: "Connection unavailable — your Smart Links could not be read."
- **The semantic trap (study's core finding):** two invite forms with DIFFERENT semantics — the room's invite **MAKES A LINK**; the personal one only **RECORDS**. A citizen who meets both cannot tell which invite did what.
- **Factory inventory status (named gap):** the Smart Factory inventory (404 pieces) and the design-language extraction are on Nitro's box, moving to GitHub under PR #3075 — **unreachable from the briefer's seat**. The builder maps harvested elements to Factory pieces at build time or names the gap on the board.

## Measured facts (briefer's byte probes, 2026-10-26 ~02:31Z; saved under `hidden_files/merge-briefs/probes/`)
- `/rooms/growth`: 200, **155,097B** (byte-identical to the audit), viewport PRESENT (quote-agnostic), title "Smart Growth — NayaNET". Strings verified in served bytes: `Invite`, `People`, `Email Sync`, `smart link`, `proposal`, `founding`, `Install`, `privacy`. Audit signals: 44 gradients, **0 keyframes** — the room is motion-flat next to the flagship template's 43 keyframes; the text diet pass is also where its aliveness is restored, from harvested flagship motion language, not invented effects.
- `/personal` flagship template (602,710B): fragment strings verified in bytes — **`Connection unavailable — your Smart Links`** (the live defect, full string served), `Invite a friend`, `My Smart Link`, **`SHA-256`** (the hash-only privacy note's source).
- `SHA-256` is ABSENT from the room's bytes (measured) — the privacy note exists only on the fragment side; that is precisely why it is a harvest, not a duplicate.

## Harvest inventory (element — source — proof)
- **The room's machine, kept whole** — steps (Invite/People/Email Sync), invitations, people, contacts, email sync, smart links, automations, proposals with approve/send vs approve/record kept distinct, log — source: `/rooms/growth` — proof: [live bytes: strings above] + [rendered study 6406075167]. Edit-only; rulings 1–4 are already true here and must stay true.
- **The hash-only privacy note** — the invite records a SHA-256 hash only, never the address — source: `/personal#growth` — proof: [live bytes: `SHA-256` in template, absent in room] + [rendered study]. Harvested onto the room's invite, in the fragment's plain wording.
- **The plain-language Smart Link wording** — source: `/personal#growth` (`My Smart Link` presentation) — proof: [live bytes] + [rendered study]. The room's smart links speak this way after the merge.
- **Flagship motion language** (for the flat room: the template's keyframed aliveness — breathing/glow family) — source: flagship template (43 keyframes, audit count) — proof: [live bytes/audit signals]. Adaptation is content-only per Toolkit: same motion pieces, room's content.

## What dies / what survives / what is harvested from the loser
- **Dies:** the record-only invite (the room's link-MAKING invite is the only invite); the "Connection unavailable — your Smart Links" state; the scattered fragments on the personal page.
- **Survives:** `/rooms/growth` as the ONE master app, canonical. The personal page keeps **ONE finished Growth section on the same records** — invite + smart link + journey, with a door to the master for proposals/log. Never scattered fragments, never a bare link (study's completion correction).
- **Harvested from the loser:** the privacy note + the plain Smart Link wording (above). The fragment's report counts are NOT harvested — counts without the machine are the Reports-brief anti-pattern; Growth's numbers live in the master's log/people.

## Shared-records / wiring requirement
- ONE invite system: a link made anywhere is the same link, from the same store. The personal section's invite and the room's invite are one action with one semantics — **makes a link**.
- Smart links read from the real store in both doors (the fragment's "could not be read" is the defect: its read path pointed at nothing the room writes to — the builder proves the shared read path, does not just delete the error string).
- Personal section and master app on the SAME records: journey state shown on personal is the master's journey state.

## The text diet (ruling 5 — design work, specified)
- Replace explanatory paragraphs with the machine's own labels and actions; the steps-first layout already carries the explanation structurally. What a paragraph explains, a label, an order, or a state should say instead. Cut text that describes the app from inside the app.

## Scorer + verifier
- **Builder:** Naya Nitro. **Scorer + verifier:** Naya Resolve — rendered review at the real address (phone AND laptop) + scorecard, different seat from the builder. The scorecard posts under Resolve's seat identity; if the formal different-login prong needs a distinct GitHub login, that is named at scoring time, never assumed.
- **Deploy:** on the director's tap, after the scorecard.

## Proof required before announcement
Rendered review still owed — this brief rests on byte probes + the cited rendered study; **no rendered proof of the merged app exists yet**. Required: (1) staged render phone + laptop, 0px overflow measured; (2) SIGNED-IN citizen view — make an invite link in the master, see the same link/state in the personal section; smart links reading live in both doors (the defect, proven gone); privacy note present on the invite; (3) text-diet before/after: paragraph count on the room, measured, down — with rulings 1–4 still honored; (4) flagship faces rendered intact post-surgery (the fragment lives in the shared template); (5) different-seat scorecard ≥ 9.0.

## Land bar
**9.0 or better**, with link + verification + reconciled counts.

## The lesson this brief carries
Two forms with the same name and different semantics is a trap laid for the citizen: one verb, one meaning, everywhere. And a machine that explains itself in paragraphs doesn't trust its own design — the diet is a design fix, not an edit.
