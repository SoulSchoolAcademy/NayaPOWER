# STAGE-TWELVE — README (Step 5 handoff)

**What this is:** the exact procedure to put the twelve sisters' briefing notes onto the staged transparency page, once their walks have run and their notes are filed. Nothing here has run yet — there are no filed notes to stage.

**Chain (each step's output is the next step's precondition):**
1. `family-probe.py` runs on a living browser → `family-results.json` (0 fails, 12 sisters with page links).
2. `file-notes.py` fills the twelve drafts from the probe results and files them to `BRAIN/05-MEMORY/NAYA-NOTES/2026/11/13/` on main → `notes-filed.json` (12 blobs + Box blocks).
3. `stage-twelve.py` builds the twelve fragment entries from the FILED notes, inserts them into a freshly harvested live Hub, and stages the rebuilt hub on branch `team-transparency-20261112` → new staged link (same proof-host URL shape, new `cb`).

**What stage-twelve.py edits (the files the transparency stage step edits):**
- The surface fragment (`surface-fragment.html` on branch `team-transparency-20261112`) — ONLY the note-entries run is replaced; the two transparency-build notes are KEPT, newest first; head, kept entries, and tail are asserted identical.
- The staged hub (`team-transparency-hub.html` on the same branch) — rebuilt from a FRESH live-Hub harvest, never from the old staged bytes.

**The one deviation, named honestly:** the transparency round's builder (`build-surface.py`) asserts every byline starts with "Team Transparency build seat" — that rule rejects the spec-required sister bylines ("Briefed by Sophia — ..."). `stage-twelve.py` performs the builder's exact insertion (same `</style>\n</body>` anchor, same prefix/suffix byte-identical asserts) in-script, with the byline rule generalized to the spec's own law: every seat signs as herself, no "Nitro" byline, no seat signing as another. The builder is not edited; the deviation is in this script and in the record.

**What is NOT done by this step:** no live deploy, no merge, no PR, no sync trigger (the live feed carries the notes only when the sync runs — the staged page is true via its baked snapshot, like the Hub's own feed). After staging, the page is walked at 1440/390/360 (list → seat → tab → note link, scroll 0 + scrolled, zero overflow) before anything is reported done.
