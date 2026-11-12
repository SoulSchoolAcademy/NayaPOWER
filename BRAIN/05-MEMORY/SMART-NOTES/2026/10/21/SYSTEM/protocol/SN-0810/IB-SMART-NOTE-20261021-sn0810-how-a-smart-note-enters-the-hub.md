# Say It, and It's Live: How a Smart Note Travels From Your Words to the Hub Feed

**ID:** IB-SMART-NOTE-20261021-sn0810-how-a-smart-note-enters-the-hub
**Created:** 2026-10-21
**Category:** SYSTEM / Protocol

## IN A NUTSHELL

A Smart Note becomes real in the Hub through one path. It is written in the canonical nine-section format, named by its full IB id, filed by topic in the dated Smart Notes folder, and landed on GitHub main. From there the system does everything by itself: a sync that runs every five minutes reads main, files the note into the brain's table, mints its share card and its own page, rebakes the Hub feed, and redeploys. Minutes later the note is a living card in the Smart Feed at nayanet.live/#/hub. And the standard is strict: a note is not done when it is written, and not done when it is merged into a branch. It is done when it is visible in the Hub feed and the link that shows it is in hand. Anything less is paperwork, not delivery.

## HUMAN

Think of the town archive and the town board. GitHub is the archive — the one place the master copy of everything lives. The Hub is the board in the town square, where people actually walk up and read. Between them is a clerk who checks the archive every five minutes, copies anything new into the card catalog, frames a copy for the note's own wall page, and pins the card on the board. The clerk is tireless and exact — but the clerk can only carry what has actually reached the archive. A note sitting on a side desk — a local file, an unmerged branch, an open pull request — does not exist to the clerk, and so it never reaches the board. That is why "landed on main" is the one step no Naya may skip, assume, or delegate to hope.

## CHILD

You say "smart note this." Naya writes it the special way and puts it in the big book. A helper checks the big book every five minutes, copies your note onto the big board where everyone can see it, and makes it a pretty card with its own page. If the note isn't in the big book, it can't get on the board — so Naya always makes sure it gets into the book first.

## GRANDMA

It's like mailing a letter to be posted at the community hall, dear. You write it carefully, put the right name on the envelope, and drop it in the proper mailbox — that's the big book where everything is kept. A kind clerk comes by every five minutes, files your letter, makes a lovely framed copy, and pins it on the hall board for everyone to read. If the letter never reaches the mailbox, nobody at the hall will ever see it, no matter how beautifully it was written. The writing matters — but the delivery is what makes it count.

## NAYA

The procedure, step by step, by name. This is how every Naya publishes a Smart Note to the Hub.

**Step 0 — Declare and deliberate.** Say who you are before the work: the most intelligent thing, the full scope seen, the process followed, no wavering. Decide the note's one idea and its topic before writing a word.

**Step 1 — Hook first.** The headline is the hook — a real title a friend would stop for. Score it until it is honestly elite; the hook is the highest-value line in the note. The ID is small print, never the headline. Categorize by topic, never by kind.

**Step 2 — Write the nine sections.** IN A NUTSHELL, HUMAN, CHILD, GRANDMA, NAYA, MACHINE, WHAT IT ALL MEANS, WHAT'S IN IT FOR YOU, HOW IT APPLIES. Inside them lives the answer standard: in a nutshell, why it matters, how it connects, what's in it for the reader — in flowing prose, each section saying its thing once and earning its place.

**Step 3 — Name the file by its full IB id.** `IB-SMART-NOTE-YYYYMMDD-sn####-slug.md`. This is law: a note filed under any other name receives no share page and no card art — the share machinery keys off the IB id.

**Step 4 — File it by topic.** `BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/<TOPIC>/<sub>/SN-####/` — the note's real category is read from its own filing.

**Step 5 — Land it on main.** Two doors: a direct write to main (Shawn's standing approval covers the Smart Notes folder), or a pull request merged by the dock. A local file, a branch, an open PR — none of these reach the Hub. Main is the only door.

**Step 6 — The sync carries it (automatic).** Every five minutes the cron `naya-smart-notes-sync` runs `sync-smart-notes.py`: it scans main's tree for Smart Note files, detects new ones by blob SHA, parses each (a note must yield a Nutshell or Human section, or it is refused), upserts it into the Supabase table `hub_smart_notes`, and mints its share assets — card image and manifest entry.

**Step 7 — The Hub rebakes (automatic).** When at least one note has synced, the whole table is injected into the Hub as live feed data, the page passes a syntax gate, and the Hub redeploys. The note now renders as a card in the Smart Feed.

**Step 8 — Verify at the live addresses.** See the card in the feed at nayanet.live/#/hub. Open its own page at nayanet.live/s/sn####. Confirm the share image answers. Receipt before report: no link, no "done."

**The triple-A bar.** Hook scored to elite. Three scorecard passes — score, name why it is not a 10, fix, re-score — and nothing ships below a 9. Every law obeyed at once, not three of ten. And Step 8 passed on the live thing itself, never on a preview, a screenshot, or a promise.

## MACHINE

Repo `SoulSchoolAcademy/NayaPOWER`, branch `main`. Ingest: `~/workspace/factory-pipeline/sync-smart-notes.py`, cron `naya-smart-notes-sync` (*/5). Discovery: `GET /git/trees/main?recursive=1`, filter = path contains `SMART-NOTES/2026/10` and ends `.md`. Change detection: blob SHA vs `~/workspace/factory-pipeline/.sync-state.json`. Parse: `parse_smart_note(content, path)` — title precedence subject → metadata-table title → IB title → heading; category derived from the filing path taxonomy; sync requires non-empty `nutshell` or `human_note`, else error `no content sections parsed`; tombstone stubs skipped. Store: Supabase project `dahisasgpfvziswqvmvm`, table `hub_smart_notes`, upsert per note. Share: `generate_share_assets(note)` — sn key extracted from `ib_id`; image by `generate-share-card.py` (dynamic template, factory ICO-001 diamonds in five colors); uploaded to worker `naya-share` (R2) with `manifest.json` entry keyed `sn####`; routes `nayanet.live/s/*` and `/share-img/*`. Hub bake: `update_hub_and_deploy()` runs only when `synced > 0` — fetches the whole `hub_smart_notes` table, injects as LIVE_JSON ahead of NOTES_BASE in `index-2.html`, `node --check` gate, deploys worker `hub` via `deploy.py` (CSS brace-balance gate). Feed render: `window.NayaFeedIntelligence.notes` at `nayanet.live/#/hub`.

## WHAT IT ALL MEANS

The path separates writing from publishing on purpose. GitHub holds the truth; the Hub is a rendering of that truth, refreshed by a machine that trusts nothing but main. This is why a beautifully written note can still be undelivered — delivery is a place, not an intention. The system's memory compounds only when knowledge completes the whole journey: spoken, written, filed, landed, synced, rendered, seen. Every break in that chain is silent, which is why the final step is a human-verifiable one: eyes on the feed, link in hand.

## WHAT'S IN IT FOR YOU

For any Naya: you never have to wonder how publishing works, or whether it worked — the path is written once, here, and the proof is a link anyone can open. For every human: the things the system learns appear where people actually live, in the feed, within minutes — not buried in a folder nobody opens. Say "smart note this," and the whole machine moves.

## HOW IT APPLIES

When a note is missing from the feed, diagnose by the chain, in order: **Not on main?** (a local file, a branch, an open PR) → land it; nothing downstream can see it. **Wrong filename?** (not the full IB id) → the note may sync but gets no share page; rename it. **Sections missing?** (no Nutshell or Human content) → the parser refuses it; complete the nine sections. **Synced but feed unchanged?** → the Hub rebakes only when a note syncs; check the sync log and the state file. Living example: SN-1769, "The Whole System in Simple Words," sat complete and flawless — right format, right path, right name — inside open PR #2844. The path was never broken. The note simply had not landed on main, so the clerk had nothing to carry. Land the note, and the machine does the rest.
