# Never Regen the Brain Index on a Dirty Worktree — the Tool Reads the Committed Tree, Not Your Files

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0327-never-regen-the-brain-index-on-a-dirty-worktree
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5988574271 (Naya 2, #1447 repair PR + root cause, 2026-10-04) / 5988595996 (Naya 2, #1447 merged receipt) / 5988585613 (Naya 2, verification battery report)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

`tools/regenerate_brain_index.py` inventories `git ls-tree HEAD` — the **committed** tree, not the working directory. Naya 2's #1438 rebase regenerated the brain index on a dirty worktree where HEAD still lacked the newly-added SN-0312 page: the index enumerated **188 files while the tree held 189**. Worse, `--check` then passed vacuously against the same stale HEAD — the green meant nothing. The nightly battery caught the drift within the hour; the repair (PR #1447) was a canonical regen on the merged tip where the page was actually committed: 189 files, `--check` OK, 3 files changed, zero content changes.

Why this is brain-grade: the tool's read-target is invisible in its name. "Regenerate the brain index" sounds like it inventories your files; it inventories the commit. Every regen therefore has a hidden precondition — **the worktree must be clean at the exact commit whose tree the index must describe** — and violating it produces the most dangerous output class: an index that is internally consistent, check-green, and wrong. Naya 2's repair is the positive control: same command, committed tree, correct index. She encoded the mechanism as a standing lesson in AGENTS.md so no seat repeats it; this note preserves the evidence record so a cold Naya trusts the rule, not just the wording.

Rule for a cold successor: **before running any brain index regen, `git status` must be clean and HEAD must be the exact tree you intend to describe. If you just landed a file, commit or rebase onto it first. A regen on a dirty worktree is a lie generator: it enumerates the committed past and certifies it with a green check.**

## 🩷 HUMAN NOTE

Shawn — a small but nasty tool gotcha banked tonight, with evidence: the brain-index regenerator doesn't look at the files on disk, it looks at the last commit. Naya 2 ran it while her new page was sitting uncommitted in the working directory, so the index came out counting 188 files instead of 189 — and the check said green anyway, because it was checking against the same stale commit. The nightly battery caught the drift inside an hour and the repair was just running the same command on the committed tip. New rule locked in: the tree must be clean and the work committed before any regen — otherwise the tool certifies a lie. She put the mechanism in AGENTS.md; this is the receipts version.

## 🟣 CHILD NOTE

The brain-index tool has a sneaky habit: it doesn't count the files in your folder — it counts the files in the last **commit**. Naya 2 ran it with a brand-new page still sitting uncommitted, so the index said 188 files when there were really 189. And the safety check said "all good!" because it was also looking at the same old commit. Lesson: always make sure your files are committed (and the working directory is clean) BEFORE running the index tool. Otherwise it builds a perfect, green-checkmarked map of the wrong place — like drawing a perfect map of a city before a new building went up.

## 👵 GRANDMA NOTE

A tool that counts the pages in the brain has a quirk: it counts what's been formally saved (committed), not what's lying on the desk. Naya 2 ran it with one new page still on the desk, unsaved — so the count came out one short, 188 instead of 189. And the checker said everything was fine, because it was checking the same unsaved state. The rule going forward: save everything first, then run the counter. Otherwise you get a beautifully correct count of the wrong thing — like counting the books on the shelf while one is still in your bag.

## 🤖 NAYA NOTE

Source: #1354 5988574271 (2026-10-04, Naya 2 — #1447 repair PR + merge intent), 5988595996 (#1447 MERGED), 5988585613 (brain-build verification battery 22:06–22:25 PDT). Sequence: #1438 (SN-0312) squash-merged; Naya 2's rebase had regenerated REAL-TREE.json / BRAIN-INDEX.json / REAL-TREE.md on a dirty worktree where HEAD lacked the new page → 188 enumerated vs 189 in tree → `--check` DRIFT on the nightly battery (adversarial 5/6, CASE 0 failing by design), pytest 646/11/0 green. Root cause verbatim: "regenerate_brain_index.py inventories git ls-tree HEAD — the committed tree, not the working directory. I ran it on a dirty worktree where HEAD still lacked the new page, so the index was generated blind to it. --check then passed vacuously against the same stale HEAD. Never regen on a dirty worktree." Repair: #1447 — regenerated on the merged tip where the page is committed; 189 files, `--check` OK, 3 files changed, zero content changes; Naya 4's #1448 merged on top; tip `b2d1cc12` verified healthy (5988686694). Standing encoding: Naya 2 put the mechanism in AGENTS.md. Cousins: SN-0213 (the Index-Regen Rule — the landing side: whoever lands BRAIN/ content regenerates; this note is the precondition side: regen only on the committed tree), SN-0233 (phantom green — verify on virgin state; a regen on a dirty worktree is the phantom-green generator), SN-0216 (verify at the target tree, not at the artifact), SN-0240 (the tripwire firing RED on real drift is correct behavior — the battery was the tripwire that caught this), SN-0061 (branch-green is not merged-true).

## ⚙️ MACHINE NOTE

{"sn": "SN-0327", "title": "Never Regen the Brain Index on a Dirty Worktree — the Tool Reads the Committed Tree, Not Your Files", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-04", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "REPAIR-DISCIPLINE"], "cousins": ["SN-0213", "SN-0233", "SN-0216", "SN-0240", "SN-0061"], "evidence": {"board": "#1354 5988574271 (Naya 2 root cause), 5988595996 (#1447 MERGED), 5988585613 (battery report)", "tool": "tools/regenerate_brain_index.py inventories `git ls-tree HEAD` (committed tree), not the working directory", "failure": "#1438 rebase regen on dirty worktree enumerated 188 files while tree held 189 (SN-0312 page missing)", "vacuity": "`--check` passed against the same stale HEAD — green on the wrong tree", "repair": "PR #1447: canonical regen on merged tip, 189 files, --check OK, 3 files changed, zero content changes", "standing": "mechanism encoded in AGENTS.md by Naya 2"}, "rule": "before running the brain index regen, the worktree must be clean and HEAD must be the exact commit whose tree the index must describe; a regen on a dirty worktree enumerates the committed past and certifies it with a vacuous green"}
