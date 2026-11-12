# DESIGN BRIEF — 05 · SETTINGS: one page, logical toggles only, canon defaults true

**Pair:** `/dashboard#settings` (toggles, incomplete set) + `/#/hub/settings` (install modal + account actions, no toggles) → ONE page
**PI items — RECORD HYGIENE, READ FIRST:** two keys may exist for this job: `settings-merge-20261026` (filed by Resolve in the completion pass) and `settings-one-20261026` (filed per Nitro's study). **Reconcile to ONE item at build start** — a doubled record for the merge that kills doubled pages would be its own lesson.
**Order in build sequence:** 5 of 7

## Contract read
Design Contract + Master Contract (canonical links in the Toolkit §3). The briefer read the Design Toolkit in full — `BRAIN/10-INTERFACES/NAYA-DESIGN-TOOLKIT.md` at main tip `57866113ca22c48c1580db8489ca8e35b88d6682`, blob `9bf8e446`, 6,546B — and this brief is written to its §4 template. The builder states their own contract read in the build pass before code (Toolkit §1.1).

## Canon that governs the content (on record, honored unless the director re-rules)
- **Page Settings Law (2026-10-24):** 3 switches per page — **INSTALLABLE · VISIBILITY · DISCOVERABILITY**. Personal page: **PRIVATE + FINDABLE default ON**. Business/Space: PUBLIC + findable.
- Every toggle says plainly what it does. Identity/account appears ONCE. Install appears ONCE — as an action, never as a gate or modal.

## Factory / approved-page study notes
- **Nitro's rendered study** (board #3066, comment 6406394271; `settings-study/STUDY.md`, 1280+390, 0px overflow, on Nitro's box): dashboard#settings has preference toggles that ARE nice — jewel-colored, labeled (Deep black; Notifications "kept on this device — nothing is sent yet"; Smart Tabs drift; Motion & glow; Auto-refresh) + Identity + Install — but the SET is random and incomplete: six toggles on record, **the canon trio MISSING, findable OFF where canon says ON**. Hub settings is an Install modal blocking the whole first view; behind it account/install actions (identity page listed TWICE, log in, log out, install) — NO feature toggles at all.
- **Power's flagship inventory study** (read in full by the briefer): the shared brand language the unified page must speak — near-black, white text, purple/violet primary, pill forms, letter-spaced small-cap labels, glowing rims on primary actions.
- **Factory inventory status (named gap):** the Smart Factory inventory (404 pieces) and the design-language extraction are on Nitro's box, moving to GitHub under PR #3075 — **unreachable from the briefer's seat**. The builder maps harvested elements to Factory pieces at build time or names the gap on the board.

## Measured facts (briefer's byte probes, 2026-10-26 ~02:31Z; saved under `hidden_files/merge-briefs/probes/`)
- `/dashboard` flagship template (602,801B, viewport present): toggle strings verified in bytes — `Deep black`, `Smart Tabs`, `Auto-refresh`, `Notifications`, `Motion`, `Install`, `VISIBILITY`. **Absent from dashboard bytes: `findable`, `DISCOVERABILITY`, `INSTALLABLE`** — the canon trio as a set is NOT in the dashboard surface's bytes (measured).
- Hub shell (5,438,679B, viewport present): **`findable` PRESENT, `INSTALLABLE` PRESENT**, and the route string `hub/settings` present. The canon vocabulary lives on the shell side — the two halves of the canon are split across the two pages, which is the merge in one sentence.
- **What bytes cannot prove:** toggle STATES. "Findable OFF where canon says ON" is the rendered study's finding (Nitro's eyes), not a byte fact — the proof pass must verify state by render + persistence read-back, not by grep.

## Harvest inventory (element — source — proof)
- **The jewel-toggle language** — jewel-colored toggles with plain labels and honest scope notes ("kept on this device — nothing is sent yet" is the honesty standard every toggle's line must meet) — source: `/dashboard#settings` — proof: [live bytes: strings above] + [rendered study 6406394271]. Kept: it is the nicest element either page has.
- **The real preference toggles, where real** — Deep black, Notifications, Smart Tabs, Motion & glow, Auto-refresh — source: dashboard surface — proof: [live bytes] + [rendered study]. Each survives ONLY with a stated, true effect; any toggle without one is cut (study's rule).
- **The canon trio** — INSTALLABLE / VISIBILITY / DISCOVERABILITY with Page Settings Law defaults — source: canon (2026-10-24 record) + shell-side bytes — proof: [live bytes: `findable`, `INSTALLABLE` in shell] + [canon]. This is a build-to-canon, not a harvest from the dashboard page — the trio is missing there.
- **Account actions, once** — identity page link, log in, log out — source: `/#/hub/settings` — proof: [rendered study]. Harvested as actions on the one page; the duplication (identity listed twice) and the modal die.

## What dies / what survives / what is harvested from the loser
- **Dies:** the Install modal as a gate (install becomes one action among actions); the duplicated identity entry; every toggle without a stated effect; the second settings surface as a separate truth.
- **Survives:** ONE Settings page, reachable from **hub + sidebar + smart tabs** — three doors, one page, same records.
- **Harvested:** from dashboard — the jewel toggles + real preferences. From hub — the account actions (once) + the canon vocabulary made real. Neither page survives as-is; the one page is composed from these parts in the existing language (edit-only on the surviving route; the builder names which route carries it and proves the other door lands there).

## Shared-records / wiring requirement
- One settings store behind all three doors: a toggle changed from the hub reads identically from the sidebar door and the smart-tabs door.
- Toggles must REFLECT and PERSIST (the study's proof bar): set → leave → return → read back. A toggle that only moves is decoration.
- Defaults set to canon at build: findable ON for Personal (private + findable), per the Page Settings Law — and the page's own copy says so in plain words.

## Scorer + verifier
- **Builder:** Naya Nitro. **Scorer + verifier:** Naya Resolve — rendered review at the real address (phone AND laptop) + scorecard, different seat from the builder. The scorecard posts under Resolve's seat identity; if the formal different-login prong needs a distinct GitHub login, that is named at scoring time, never assumed.
- **Deploy:** on the director's tap, after the scorecard.

## Proof required before announcement
Rendered review still owed — this brief rests on byte probes + the cited rendered study; **no rendered proof of the unified page exists yet**. Required: (1) staged render phone + laptop, 0px overflow measured, NO modal gating the first view; (2) SIGNED-IN citizen view — canon trio present with canon defaults (findable ON), every toggle carrying its plain-words effect line; (3) persistence read-back: change a toggle at one door, read it at another; (4) identity/account appearing exactly once (counted); (5) different-seat scorecard ≥ 9.0.

## Land bar
**9.0 or better**, with link + verification + reconciled counts.

## The lesson this brief carries
A settings page is a promise list: every toggle that doesn't do what its label says, and every default that contradicts canon, spends the citizen's trust. And the canon itself was split across two pages — half the law on each — which is how both pages could look finished while neither was true.
