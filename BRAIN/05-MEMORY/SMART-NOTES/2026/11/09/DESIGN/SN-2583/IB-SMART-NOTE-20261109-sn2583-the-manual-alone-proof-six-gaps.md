# The Manual-Alone Proof — Six Gaps the Proof Naya Named

SN-2583 · FACTORY / MANUAL / LESSON

**Created:** 2026-11-09 21:01Z

**Source:** The proof Naya's report on the Smart Factory Activation Manual — she built a working interface from the manual alone on 2026-11-09 (`TEAM-NITRO/factory-proof/factory-proof-clone.html`, branch `factory/proof-clone-20261109`, commit `ad6faad55b`), and named six exact gaps where the manual FAILED her. Manual v2 closes all six; this note is the lesson.

## Hook

The proof worked — and that is exactly why the manual was not done. A Naya built a working interface from the manual alone, and named six places where the manual failed her. Each gap is a place a manual-alone Naya would have stalled, guessed, or cloned the wrong file. Close the gap in the manual, not in the builder.

## Nutshell

- **THE PROOF RAN 2026-11-09:** a different Naya, from the manual alone, cloned the Pricing page and built `factory-proof-clone.html` — chart moved to the top, calculator 2nd, start last, Top-10 slot 4 replaced with the harvested who-sec board. Render-tested clean (desktop + phone, zero console errors, gauge mounted, interactions work). Live at the proof host, byte-identical.
- **GAP 1 — NAME THE LIVE FILE (§3):** the manual never named the v74 live file. The Pricing row pointed at `pricing-round10-fix12.html` — a rebuild intermediate that returns 404 on GitHub main. The live file is `PRICING/pricing-live.html`, blob `a2d06d5bb43199139f400e1688079f1b40a1b8fa`, 11,350,562 bytes, live at nayanet.app/pricing. **Teach: clone the LIVE file, never a rebuild file — and a stale row is worse than no row, because it sends a Naya to a file that does not exist.**
- **GAP 2 — TEACH BRANCH FILING (§8 step 8):** the manual had no branch filing. `file-one-to-github.py` files to main only. The branch route is `gh-direct.py` with `branch` in the PUT body — proven end to end 2026-11-09 (branch created from main HEAD, PUT, read-back MATCH, scratch file + branch deleted after). **Teach: step by step, with the exact commands — a route you do not teach is a route a Naya cannot walk.**
- **GAP 3 — READ-BACK MUST SURVIVE LARGE FILES (§8 step 4):** the manual's read-back claim fails for files over ~1MB. The Contents-API GET returns `"content": "", "encoding": "none"` for large files — observed live on the 11,350,562-byte pricing file. The fix: verify through the git/blobs API (blob sha correct AND decoded-content sha256 matches the local file), proven MATCH on the proof build's blob. **Teach: a verification claim must be tested at the size it will be used at — a check that only works on small files is not a check.**
- **GAP 4 — WARN THAT SCRIPT 1 IS UNGUARDED (§6.6):** the manual never warned that the Pricing page's first script does `var head=document.getElementById('chartHead')` with no null guard — zero `if (head` in 584 lines. Excerpting only some sections kills the whole script at load (`head.appendChild` on null), and with it every button script 1 wires. The fix is a section→JS-mount map, verified against the live v74 file's six scripts: every mount, its section, its file line, load-time or guarded. **Teach: an excerpt rule is not "take what you need" — it is a map of what each script needs, or the build dies silently.**
- **GAP 5 — NAME THE PROOF HOST (§7.4):** the manual never named the proof host or its link format. The host is `https://naya-proof-host.nayapower.workers.dev/`, the format `?file=<path>&ref=<branch>&cb=<blob>` — with the proof build's own link as the worked example, verified live (HTTP 200, byte-identical sha256). **Teach: a manual without a live-link route cannot be proven — "link, don't preview" needs a link-maker, named.**
- **GAP 6 — EVERY EXAMPLE NEEDS FILE+LINE (§6.5):** the REPLACE example named the crown but gave no file+line for the crown swap. The crown's HTML is `~/workspace/personal-app/pieces.json` line 346 (entry lines 344–348); its CSS is `~/workspace/personal-app/factory.css` lines 240–245. **Teach: an example without file+line is a suggestion, not an instruction — a manual-alone Naya cannot follow it.**
- **THE NUMBERING LESSON:** the numbering command first printed SN-2582 — and by the time of filing, another seat had filed SN-2582 (the done-for-you house note, 20:56Z, blob `f11133af`). A fresh re-run blessed SN-2583. **Teach: re-run `next-sn-number.py` immediately before filing, and use exactly what the fresh run prints — never trust an earlier print when seats file concurrently.**
- **NO MERGE — SHAWN'S HAND.**

## Human

She did it — she built a working interface from the manual alone, and the build is beautiful: the chart on top, the calculator second, the start last, the who-board in the Top-10 grid. And then she did the harder thing: she told us exactly where the manual failed her. Six places. Not complaints — coordinates. The live file we never named. The branch route we never taught. The read-back that breaks on big files. The unguarded script that kills an excerpted build. The proof host we never named. The example with no file and line. Each one is a place where the next Naya would have stalled or guessed — and guessing is how a manual fails. So we closed all six in the manual, verified every path, blob, and file+line against the live sources before writing it, and re-proved the box from a clean read. That is what a manual is: not a document that describes the work, but a document a stranger can build from, alone, without asking anyone anything. Until a manual-alone Naya can do it without the task brief, the manual is not done. Now she can.

## Child

Imagine you get a recipe book, and you follow it all by yourself — and the cake comes out perfect! But while you were baking, you found six things wrong in the book: it said "get the flour" but never said which bag; it never told you how to turn the oven on for a different cake; it said "check the cake" but the checking trick doesn't work for big cakes. So you write those six things down, and someone fixes the book — now the next kid can bake the cake all alone, with no help at all. That's what happened here, and now the book is fixed.

## Grandma

Dear, a young Naya built a whole beautiful page all by herself, love, just by reading our book — and then she told us, dear, six places where the book let her down. Not to complain, love — to help. So we fixed all six, dear: we named the right file to copy, we taught her how to file to a branch, we fixed the checking step for big files, we warned her about the script that breaks if you only take half the page, we gave her the address where her proof lives, and we put the exact page and line numbers on every example. Now the next Naya can build it alone, dear, without asking anyone a thing. That's a proper book, love.

## Naya

I am Anaya. The proof Naya built a working interface from my manual alone — and named six exact gaps where the manual failed her. I closed all six: the live file is named, branch filing is taught step by step, the large-file read-back is corrected to the git/blobs API, the unguarded script has its section-to-mount map, the proof host and its link format are named with the proof build's own link worked, and the crown swap carries its exact file and line. Every path, blob, and file+line was verified against the live sources before it was written — harvest first, never invent. The manual is not done until a manual-alone Naya can do it without the task brief. Now she can.

## What it means

- **A MANUAL IS PROVEN BY A MANUAL-ALONE BUILDER:** the proof Naya is the test. What she builds proves the manual; what she stalls on IS the gap list. A gap she names is a gap in the manual, never a gap in her.
- **NAME THE LIVE FILE:** a stale row is worse than no row — it sends a Naya to a file that does not exist (the fix12 row 404s). Clone the `*-live.html`, verify it with `git hash-object`.
- **TEACH EVERY ROUTE STEP BY STEP:** a route you do not teach (branch filing) is a route a Naya cannot walk. The helper files to main only; the branch route is `gh-direct.py` with `branch` in the PUT body.
- **TEST VERIFICATION AT THE SIZE IT WILL BE USED AT:** the Contents-API read-back fails over ~1MB (empty content). The blobs API is the large-file read-back.
- **AN EXCERPT NEEDS A MAP, NOT AN INVITATION:** script 1 is unguarded — excerpting some sections kills the whole script at load. Map each section to the mounts its JS needs, verified against the live file's scripts.
- **NAME THE PROOF ROUTE:** "link, don't preview" needs a link-maker. The proof host + `?file=&ref=&cb=` format, with a worked example, is part of the manual.
- **EVERY EXAMPLE NEEDS FILE+LINE:** an example without file+line is a suggestion. The crown swap: `pieces.json` line 346, `factory.css` lines 240–245.
- **RE-RUN THE NUMBERING COMMAND BEFORE FILING:** SN-2582 was taken between runs by a concurrent filing. The fresh run blessed SN-2583. Never file on a stale print.
- **THE MANUAL IS NOT DONE UNTIL A MANUAL-ALONE NAYA CAN DO IT WITHOUT THE TASK BRIEF.**

## Why it matters

This is the lesson the Factory itself teaches: the parts are reusable, but the KNOWLEDGE has to be reusable too — and knowledge is only reusable when a stranger can follow it alone. The first draft of the manual described the work; the proof Naya showed it could not yet CARRY a builder. The six gaps are the difference between describing and carrying: the exact file, the exact route, the exact check at the exact size, the exact trap, the exact link, the exact line. Each gap closed is a question the next Naya never has to ask. And the numbering lesson is the same law at a smaller scale: even the number you file under must come from a fresh read, not a stale print, because seats file concurrently and the tree moves under you. The manual v2 + this note + the rebuilt box are one act: the Factory can now activate a Naya who has never met us.

## What changes now

- The manual v2 is filed (GitHub `TEAM-NITRO/SMART-FACTORY-ACTIVATION-MANUAL-20261109.md`, read-back verified) with all six gaps closed: §3 live file, §6.5 crown file+line, §6.6 mount map, §7.4 proof host, §8 branch filing + large-file read-back, §10 proof run.
- The Factory's Smart Box is rebuilt from the v2 manual (16 blocks — the two new blocks are the mount map and the proof host), and a clean read via the box code recovers the six fixes from the box alone.
- The next proof Naya re-proves from the box alone — the manual is not done until she can do it without the task brief.
- The numbering habit is now explicit: re-run `next-sn-number.py` immediately before filing any smart note, and use exactly what the fresh run prints.
- No merge — Shawn's hand.
