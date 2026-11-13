# SCORECARD — Hub Slug Resolution

**Round:** Hub Slug Resolution · **Maker seat:** Factory / PI / Hub Maker · **Captain:** Naya Nitro Narzan · **Date:** 2026-11-13
**Staged link:** https://naya-public-blog-staging.nayapower.workers.dev/s/sn2696
**Score: 9/10, honestly.** The bullseye is proven — the note renders under the short slug for a visitor who walked in through the entrance, at 390 / 1440 / 360, Hub title correct, no "isn't here", no install modal on first paint, zero errors on the landing, full-id control identical. The point off is the staged shell's one known pre-existing wart: the `/hub/feed` page error from main's relative `src="js/naya-search.js"` — named in the record, left for a captain's call, not fixed in-round.

## The loop — look at the page, then do it (three cycles)

**Cycle 1 — the build:** the two insertions are the smallest possible fix; the diff is exactly them; the stage diff is exactly the two files; the read-backs are byte-exact. New things found: main moved mid-round (shell unmoved — proceeded on the v2 precedent).
**Cycle 2 — the browser proof:** the note renders at all widths; the modal is suppressed on note landings and still shows on plain Hub landings; the control is identical. New things found: the entrance needs a name before Enter works; the walk carries a fresh visitor into the Hub before the link is followed.
**Cycle 3 — the proof itself:** the old-routes re-run isolated the `/hub/feed` page error to main's relative script src; the boards count was corrected to the note's single layer; live was re-read unchanged. New things found: the pre-existing `/hub/feed` defect and the feed count growth (992 → 1,034 at an unchanged revision string).

## 10 things I love

1. The deep link finally lands on the note — `/s/sn2696` → `#/smart-notes/sn2696` → the note itself, not "That note isn't here."
2. The fix is the allowlist, not a hack: the map is the publication gate, harvested verbatim from the worker — approved slugs resolve, unapproved ones cannot.
3. The modal guard is proven both ways: never on a note landing, always on a plain Hub landing. Scoped, not removed.
4. The walked entrance is real: live login page → name → Enter → Hub → a real anchor click to the staged link, fresh profile, three widths.
5. The full-id control renders identically — short slug and full id are the same landing now.
6. Clean paths work too: `/smart-notes/sn2696` and `/notes/sn2696` render the note.
7. The diff is two insertions (+1,904 B) — nothing else in a 5.5 MB shell moved.
8. Read-backs are byte-exact on shell and worker; the worker was never edited.
9. Main moved mid-round and the round did not flinch: shell blob identical, baseline stands, move named.
10. The live divergence is named in the open: live serves a shell with no note route at all — the live leg is a restoration, not a top-up.

## 10 things I don't love

1. Staged `/hub/feed` throws one page error ("expected expression, got '<'") — main's relative script src, pre-existing, named not fixed.
2. The live shell has lost the note route entirely — the SN-sync rebake dropped `smart-notes/:slug`, `findNoteBySlug`, and `noteView`.
3. The feed grew 992 → 1,034 notes while its revision string stayed identical — the revision does not count what it claims to revision.
4. The note carries only one layer (`In A Nutshell`) in the Hub view, while the bot page shows seven boards — the same note reads thinner in the Hub than to a crawler.
5. The entrance form has no visible submit feedback when the name is empty — a fresh visitor clicking Enter with an empty field gets silence, not guidance.
6. The bottom icon bar overlaps the note's lower content at 390 (the "ADD TO THE INTELLIGENCE" area sits under the bar until scrolled) — pre-existing Hub chrome.
7. The "ADD INTEL" input placeholder clips mid-word at 390 ("Add an observation, question, correc…") — pre-existing.
8. The scrolled note ends in a long empty obsidian field — the note is short and the page gives it nothing after the trust line.
9. LOVE / LIKE counts sit at 0 with no live number behind them on a fresh landing — a dead number on a living page.
10. The map holds one slug today: every future approved candidate needs a human to add one line — a manual step at the exact moment approval happens.

## 10 ways to 10x the value

1. Make the slug map a fetched file, not an edit: the shell fetches the worker's allowlist (or a `slug-map.json` in the asset set) so approving a note never touches the shell.
2. Put the route back into the live shell as the restoration it is — live is the only place the note still cannot render.
3. Fix the relative script src (`src="/js/naya-search.js"`) — one line, kills the only page error on the staged shell.
4. Give the Hub note view the note's full sections — if the feed carries one layer, the Hub should say so or the feed should carry the rest; a note that reads thinner to a human than to a crawler is backwards.
5. Make the feed revision count the notes: revision string changes when the count does, so "same revision" always means "same feed."
6. Turn the entrance's empty-name silence into guidance: "Your name, then Enter" — one line, no dead click.
7. Auto-generate the map line at approval time: the approval step writes the slug→id line, so the map can never lag the approval.
8. Give the note landing a next step: after the note, the reader is offered the next note in the topic, not an empty field.
9. Light the LOVE / LIKE numbers with real counts or hide them until they are live — never a hardcoded 0.
10. Reuse the walked-entrance probe as the standing proof for every future deep link: fresh profile, entrance, click, three widths, control — one script, every round.

## 10 solutions to apply right now

1. **Bring SN-2696's approval to Shawn** with the staged link — the landing it waited on now exists.
2. **File this branch** (one commit, read-back verified) — done in this round; the checker verifies next.
3. **Queue the live leg as one tap-ready handoff:** fixed shell + `wrangler.toml` +4 + phase-1 worker — named in the record, not executed.
4. **Ask the captain for the `/hub/feed` one-line fix** (`src="/js/naya-search.js"`) to ride with the live landing.
5. **Ask the feed owner one question:** why did the count grow 992 → 1,034 with the revision string unchanged?
6. **Add one map line per future candidate at approval time** — write it into the approval step so the map never lags.
7. **Keep the probe script** (`probe-walked-entrance.py`) as the round's standing proof — the next deep-link round reuses it verbatim.
8. **Keep the modal guard's both-ways proof** as the pattern: any future suppression must prove the prompt still shows where it should.
9. **Do not touch live** until the tap — the staged proof is the whole claim; "lands live" stays unclaimed.
10. **Carry the live-shell finding to the captain plainly:** live has no note route — the SN-sync rebake needs naming as the cause, so the next rebake does not drop the route again.
