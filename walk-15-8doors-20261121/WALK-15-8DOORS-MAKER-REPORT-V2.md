# WALK-15 8-DOORS MAKER REPORT V2 — Fix round (checker round-3 failures A–F)
Filed 2026-11-21 ~15:10 MST · Maker: WALK FIX MAKER (depth 2/2)
Branch: `walk/walk-15-8doors-20261121` · Repo: SoulSchoolAcademy/NayaPOWER.
Checker report: `walk-q2-whats-your-thing-20261113/WALK-15-8DOORS-CHECKER-REPORT.md`
(27,593 B, sha256 `c6b3b356a95b40724c29965a0d478daf89442ecd1a9fe16a9545ba6350a77f7b`).
Nothing in this report goes to Shawn.

## 1. WHAT WAS FILED (walk first, then this report)
- `walk-15-8doors-20261121/walk-beginning-fixed.html` — **1,564,022 B**,
  sha256 `33e5003e245f43b9e66d69d4d40698d99f0e4604915bf37dca967f8db85047ca`,
  blob `50100bfd15a143eade195a5f269d4c97c75fc99b` — PUT 200, blob read-back match TRUE.
  Commit `669b44c321dcd313d7f8ce9b7d5d22addb645f19` (2026-11-21T22:04:58Z).
- `walk-15-8doors-20261121/build-15-fix.js` — 65,648 B,
  sha256 `6ae11fd13e6f5b1141b8083bd6ca0b7cef34d396468880f4823c8bd61a20bd12`,
  blob `8e29d1352053256af7ab93c684c0e90c477afdc9` — PUT 201, read-back TRUE.
  Commit `800251aa846264e7c58be0588bdc53ce4c4a7fe0` (2026-11-21T22:05:02Z) — branch tip
  as of the walk filing. (This report files next, as its own commit; the tip
  after this report is named in §8.)
- Prior tip before this round: `98bd767d…` (the round-3 report commit). The base
  build was verified to reproduce the filed walk byte-exact before any edit
  (1,495,685 B, sha256 `9cc2e7f6…`, blob `d94bd9d8…` — the original build script
  run clean), so every byte that changed in this round is one of the fixes below.
- Staged link (VERIFIED first-hand, check 3 of 3):
  https://naya-proof-host.nayapower.workers.dev/?file=walk-15-8doors-20261121%2Fwalk-beginning-fixed.html&ref=walk%2Fwalk-15-8doors-20261121&cb=50100bfd15a143eade195a5f269d4c97c75fc99b
  — HTTP 200, 1,564,022 B, sha256 `33e5003e…` — exact match to the filed blob
  (fetched piped to hash, never `curl -o`).

## 2. THE FIXES — ONE BY ONE
### A. Slides 03–10 carried (item 3)
All nine sent slides (02–10) are now in the walk file, each as its own framed
step (`step-sent-2` … `step-sent-10`), each with its own question, its own
dictate/focus labels exactly as sent, a PowerCast talk panel, a pre-filled
Naya example + Edit button, and the three ways. They ride as a framed
**appendix after the end slide, outside the 15-question flow** — the locked
15, their order and the "N of 15" counters are untouched (15 headings,
"N of 15" ×15, " of 10" = 0, all re-verified). Progress on appendix steps
reads "Sent slide N of 9" (the "of 10" count was ordered changed; the sent
count must not come back).
Distinctive-question counts in the filed bytes: slides 02, 03, 04, 05, 06,
07, 09, 10 = **1 hit each**; slide 08 = **2 hits, by identity** — its
question "What do you offer?" IS locked Q11 (HARVESTED-VERBATIM, checker
item 2), so it occurs once as Q11 and once as appendix-08. That is the
question being the same question, not a miscount.
Honest limit: appendix steps are in-file, not in-flow. Their Play buttons
(open the PowerCast theatre) and Edit buttons are wired (engine glue,
appendix-scoped); their Enter / Skip / dictate controls are inert by
design — the appendix carries the sent slides as a record, it is not a
second flow. Wiring them into the flow would change the locked 15 flow
and needs its own order.

### B. PowerCast — the ACTUAL player JS core harvested (item 4)
The new `speechSynthesis` engine and the new `talkBars` CSS are **removed**
(`speechSynthesis` = 0, `talkBars` = 0 in the filed bytes). In their place,
the harvested core from the staged Personal bytes drives the audio:
- Source re-fetched first-hand: 10,517,420 B, sha256
  `0b4fb0f5c3fb7258fda68a566b35ce2ab1ea9f47c6430e59291a827a45ef9362`
  (52,443 lines — matches the checker exactly; fix-tip blob `50867d86`).
- Harvested verbatim: `SA_PC` (42 episodes, R2 `.m4a` files), `SA_R2`,
  `SA_PC_URL`, `SA_PC_HERO`, `SA_PC_THUMBS`, `saPcThumb`, helpers
  `sa$`/`saEsc`/`saFmt`, `saAudio` (`new Audio()`), theatre state vars,
  `saPcUrl` / `saPcLoad` / `saPcToggle` / `saPcSync` / `saRenderPcList` /
  `saPcInit` / `saPcHandleClick` / `saPcFullscreen` / `saPcHome` /
  `saStopTheatre` (Personal L41467–41499, L41525–41533, L42002–42040,
  L42204–42222, L42411–42473), the `#saTheatre` shell (L36991–36994) and
  its CSS (L36861–36864, L36866–36867, L36869). `saPcSync` is in the bytes
  (definition ×1, ≥5 occurrences total); `#saTheatre` ×1.
- The ONLY wrapper change: in Personal this code lives inside one big
  course IIFE; it is carried at the top level (the IIFE wrapper alone is
  dropped) so the walk engine can call it. Every function line, the
  episode data and the state strings ("▶ Play" / "❚❚ Pause" /
  "On air — playing" / "Paused") are verbatim.
- NOT carried: the video half (`saTheatreOpenVideo` / `saTheatreNext` —
  they need `SA_CHANNEL` / `SA_ACADEMY`, not part of the audio core) and
  `#saTheatreTitle`'s 15px rule (L36865 — below the 17px scale; the title
  inherits, and the walk sets it at 19px in its own layout CSS).
- The player-card skeleton the JS expects (`saPcNum` / `saPcTitle` /
  `saPcDesc` / `saPcUpNext` / `saPcArt` / `saPcState` / `saPcPlay` /
  `saPcCur` / `saPcTot` / `saPcFill` / `saPcBar` / `saPcList` / `saPcAll` /
  `saPcPrev` / `saPcNext` / `saPcBack` / `saPcFwd`) has **no static markup
  in the Personal bytes** — I searched the whole served file; those ids
  occur only inside the JS. Personal's card is rendered by its course view
  at runtime, and its `saPcInit()` call (L42477) is try/catch-wrapped, so a
  missing card throws into a console warning, not a page break. The walk
  therefore houses that skeleton (ids taken verbatim from the harvested
  JS) inside `#saTheatreBody`. That skeleton is assembly, not a new
  player; the player logic, episode list, URLs and state strings are
  harvest. The theatre's own transport runs on the harvested
  `saPcHandleClick` delegation, bound by the engine glue as Personal's
  `saWire` binds it.
- **What "moving" is, honestly:** nothing animates to fake speech any
  more. What moves is the real player's own motion: the progress fill
  (`#saPcFill` width), the time counters, the episode list advancing on
  `ended` (auto-next through the 42). A real voice IS present — the 42
  recorded PowerCast episodes (R2 `.m4a`). **What is still owed: a real
  voice for the questions themselves.** Play on a question opens the
  theatre and plays Naya's PowerCast recordings; it does NOT speak that
  question. The panels say so plainly now ("Tap play — hear Naya's
  PowerCast, her real recordings"). Do not present this as Naya speaking
  the questions — that recording does not exist yet.
- Talk panels: present on all 25 question steps (16 flow + 9 appendix).
  Entry (`step-door`), naming (`step-names`), reveal (`step-reveal`) and
  end (`step-end`) have no talk panel — and none belongs there: there is
  no question text on those pages to speak, and the player itself is
  global (the fixed `#saTheatre` overlay lives on every step once opened;
  audio continues across steps, and every panel mirrors its state).
  The flank play buttons on the question steps now open the theatre and
  toggle the harvested player, as do the hint "play" actions.
- Glue, named: `openPc` / `closePc` / `playPc` / `syncPanels` /
  `pcRebuild` + theatre bindings. One deliberate deviation, with reason:
  the harvested `saStopTheatre()` clears the theatre body, which in the
  walk houses the player card — so close pauses first, then calls it
  (a playing episode ending while the card is gone would throw inside the
  harvested `ended` handler); reopening rebuilds the card and re-syncs
  through `saPcLoad`. `saPcFullscreen` / `saPcHome` are carried but have
  no pane to move cards from in the walk (they return early).
- Dictation (`SpeechRecognition`, the slide's mic input) is untouched —
  it is input, not the player, and is a different API from the removed
  `speechSynthesis` output engine.

### C. Showcase pre-filled + Edit wording + Q1 downgrade (item 5)
- Showcase (`answer-16`) is now **pre-filled** with Naya's example
  (DRAFTED): "NayaNET — built live, in front of everyone: the first live
  Smart Notes, the Hub, and this walk, one frame at a time." Pre-filled
  count is now 25/25 (15 + showcase + 9 appendix). An untouched example
  still cannot be submitted (the engine refuses it, as before).
- The exact Edit wording **"just click edit — this is an example of what
  to write"** now occurs **25×** in the walk bytes — once per Edit button,
  as the button's `title`. The buttons still read EDIT.
- Q1 motto "VERBATIM Shawn (SN-0823)" is **downgraded to DRAFTED**.
  Verification first-hand: the sentence occurs 0 times in `MEMORY.md`,
  `THE-NAYA-DESIGN-LANGUAGE.md`, the Playbook and the Intelligence
  Report; `SN-0823` appears in `DESIGN-LANGUAGE.md` only as a cited
  "ratified standard" with no motto text; the sentence itself surfaces
  only in relayed reports (Seat E / Seat H) and in our own round-2
  files — claims, not a primary source. The build script comment now
  says DRAFTED with this reason. (The background workspace grep that
  finished after the build confirmed the same: SN-0823 cited as a
  standard only; the sentence appears only in relayed Seat E/H reports
  and our own files.)

### D. Sidebar Pricing — gate line STANDS (item 12)
Checked the **staged Hub tip bytes first**, as ordered:
- Branch `hub/detail-boards-unify-20261121`, tip
  `b02e6aa8fdf797bd14db4a16061e7ea337af3ab1` ("Hub triangle leg 2026-11-21:
  Calendar + Dashboard doors in the Where-you-go rail").
- The cited blob `485cdf63` is a short prefix and was **not found** in the
  tip tree; the Hub file at tip is `HUB/app/index.html`, blob
  `4127be0b7ae738975cc87b89e4381ec461581cdc`, 7,637,122 B, sha256
  `af325ea886557432f52804059c60fccca34503c16bb02a94532faf3c946db6ef`.
- That file **does** carry the Pricing entry, at **L8233**, in the
  `RIGHT_ITEMS` (right sidebar) array, rendered as sidebar links
  (`nav-btn nav-right`, `data-right` = id, label shown):
  `{ id: 'pricing', label: 'Pricing', icon: 'tag', color: '#d4a017',
  href: 'https://naya-model-pricing.nayapower.workers.dev/' }`
  — with the comment at L8219–L8221: "White Paper (magenta) ≠ Pricing
  (violet); Settings sits underneath Pricing, with its own icon (gear)".
  `>Pricing<` = 0 (the label is rendered by JS, as the entry above shows);
  `id: 'pricing'` = 1.
- So the gate line's promise — "you can change your level any time from
  Pricing in the sidebar" — stands on staged bytes, and the gate line is
  **unchanged** in the walk. Three honest caveats: (1) the entry's href is
  the `naya-model-pricing` worker URL, not `nayanet.app/pricing`;
  (2) its color in the tip is `#d4a017` (gold), where the 2026-11-17 eye
  walk cited `~#8e24aa`; (3) the live Hub the checker fetched (~4.46 MB)
  did not show it — staged tip (7.6 MB) does; live ≠ staged here. The
  SN-2440 change-level control behind the entry remains owed, as before.
  No sidebar change was built into the walk.

### E. Design laws — the 13 introduced fails are gone (item 14)
Independent in-memory run of `check-design-laws.py`'s own regexes on the
filed bytes: **39 fails, 8 warns** (was 52 fails, 8 warns). The 13
introduced fails are removed:
- The 12 layout sizes at walk L202–229 raised to the 25/19/17 scale:
  talk title 14→19, talk state 13→17, talk words 13.5→17, Edit 13→17,
  three-ways 15→17, Skip 15→17, names-sub 16→17, name label 11→17,
  name URL 13.5→17 (×2 lines), name note 13→17, names-smart 14→17.
- Q6 example reworded: "no gray text" → "no faint text" (the example is
  drafted, not Shawn's verbatim words).
- The 39 remaining fails are all inherited/harvested (slide-02 head 11,
  end-slide style 23, lane naming CSS 4 SIZE + 1 GRAY — the L230
  "no gray." comment). Exactly **1 GRAY** fail remains (that L230 comment).
  The 8 warnings are unchanged. No new fails were introduced by the
  harvest (the 42-episode data carries 0 gray/grey; the harvested theatre
  CSS lines carry no sub-17px size — the 15px `#saTheatreTitle` rule was
  deliberately not carried).
- Attribution note, honestly: the 6 names sizes raised above are
  line-filtered from the lane walk (their values are identical there), but
  the checker counted them among the 13 introduced and the task ordered
  those 12 raised — raised as ordered. The other 4 naming sizes
  (`.p3-nc-urlinput` 13.5, `.p3-nc-nutshell` 13.5, `.p3-build-link` 14.5,
  `.p3-build-link span` 12.5) stay as inherited/harvested, untouched.

### F. Naming previews aligned (carried flag)
All three previews now read `nayanet.app/<typed>` as they type. The
business/space prefix alias spans (`url-biz-alias` / `url-space-alias`)
are removed from the naming markup and from `syncNames`; `url-business`
and `url-space` values were already the typed slug. Verified: both alias
spans = 0 in the filed bytes. The reveal doors and their destinations are
untouched (Business door still `nayanet.app/<alias>` per the locked
scheme, as passed).

## 3. UNTOUCHED (as ordered)
The 15 questions, their order, the "N of 15" counters; the eight doors +
destinations + the gate (`?next=` + `pendingDoor`); the pricing harvest
(pricing page NOT embedded or rebuilt); the naming page except fix F.
The pricing return leg is NOT built (checker item 11, CONFIRMED — pricing
v77 reads no `?next=` and navigates nowhere). "Choice → in" is NOT
end-to-end, and this report does not claim it is.

## 4. THREE CHECKS
1. **Build checks (in-script, all PASS):** sources (slide-02 / end /
   lane base / agreement) + Personal fetch anchors (incl. all new player
   core lines); 25 qsteps; 25 pre-filled; 25 talk panels; 25 qa-rows;
   25 Edit buttons; 25 Skip buttons; Edit wording ×25; showcase
   pre-filled; sent-slide questions 8×1 + slide-08 ×2; harvested player
   core present + parses; no `speechSynthesis`; no `talkBars`; Q6 gray
   gone (gray ×1, inherited comment only); no alias spans; player
   skeleton present; 8 reveal doors; no seventh button; frame div +
   agreement L340–348 verbatim; PowerCast CSS verbatim; state strings;
   no "of 10"; "N of 15" ×15; showcase line; slide-02 question 1×
   (appendix only); no A/B/C boards; entry / naming / end present;
   locked-scheme reveal hrefs; all 8 doors gate through pricing `?next=`;
   About + Skills deep-link doors; gate line; key + heading per question;
   engine parses.
2. **Independent verification (separate script, in memory, all PASS):**
   re-decoded the filed bytes from the build's base64 and re-counted
   everything above from scratch, plus the design-laws replication:
   **39 fails / 8 warns / 1 GRAY** (all inherited). Filing ran only
   after this passed; an earlier miscounted check failed fast and filed
   nothing (the "Show all 42" string occurs 3× — skeleton HTML +
   harvested JS + the `PC_SKELETON` rebuild string — not 1×; corrected,
   not fudged).
3. **Staged-link check (first-hand):** HTTP 200, 1,564,022 B, sha256
   `33e5003e…` — exact match to the filed blob.

## 5. SEVEN QUESTIONS (Self-Check Law — all must be YES)
1. Most intelligent? **YES** — the nine sent slides are carried whole
   without disturbing the locked 15, and the audio is the real harvested
   player instead of a rebuilt voice.
2. Most logical? **YES** — each fix follows the checker's evidence to its
   own source (slide files, Personal bytes, staged Hub tip, the laws
   script's own regexes).
3. Most sensible? **YES** — nothing claimed that the bytes don't show:
   the appendix's limits, the question-voice gap, the sidebar caveats
   and the return leg are all named, not hidden.
4. Full scope? **YES** — items A–F plus the filing (G), all covered with
   first-hand evidence.
5. Consequences? **YES** — Play now opens real recordings instead of
   speaking the question; the gate line stands on staged bytes while
   live differs; the appendix is a record, not a flow.
6. Pros and cons? **YES** — pro: all six failures fixed on the bytes,
   laws down 52→39, staged link exact; con: question-specific real voice
   still owed, return leg still owed, render proof still owed.
7. Best possible choice? **YES** — file the fix with the honest limits
   stated, rather than softening any of them into a pass.

## 6. FLAGS (carried + new)
- **RETURN LEG OWED (item 11, CONFIRMED, carried):** pricing v77 must
  learn `?next=` (and navigate after a choice) before "choice → in" is
  real. Not built, not faked.
- **QUESTION-SPECIFIC REAL VOICE OWED (item 4, NEW wording):** the
  harvested player plays Naya's 42 real PowerCast recordings; no
  recording of any of the 15 questions exists. Play does not speak the
  question. A real voice per question is a recording job, not a code job.
- **APPENDIX IS A RECORD, NOT A FLOW (item 3, NEW):** the nine sent
  slides are in the file, framed and complete, but outside the
  15-question flow; their Enter / Skip / dictate controls are inert.
  Flow integration is a separate order if wanted.
- **SIDEBAR PRICING: STAGED YES, LIVE NO (item 12, RESOLVED on staged
  bytes):** entry exists in the staged Hub tip (`HUB/app/index.html`
  L8233, `RIGHT_ITEMS`); the checker's live-Hub fetch did not show it.
  Live ≠ staged here — the Hub round owns reconciling that, and the
  SN-2440 change-level control behind the entry is still owed.
- **Q1 MOTTO NOW DRAFTED (item 5, NEW):** the SN-0823 verbatim claim is
  unverified from files on hand; the example stays, flagged DRAFTED.
- **DESIGN LAWS (item 14, PARTIAL):** 39 fails remain, all
  inherited/harvested (slide head 11, end style 23, lane naming 5).
  Clearing those means touching harvested bytes — a separate decision,
  not taken silently here.
- **RENDER PROOF OWED (carried):** no browser render was run by maker
  (local byte/parse checks + staged HTTP+sha only); phone-width behavior,
  the theatre opening, real `.m4a` playback and the naming-preview typing
  are unproven until the eye runs them. His eye is the verdict.
- **EPERM FLAKE (carried):** active all window — large writes to disk
  EPERM or land 0 bytes (30/30 attempts failed on one path); the walk was
  filed with zero local writes (build prints base64 to stdout, piped
  straight to the filer, which decodes in memory and PUTs from memory).
  No good local copy of the filed walk exists on disk; the GitHub blob is
  canonical.

## 7. FILES IN THE LANE
- `build-15-fix.js` (filed, blob `8e29d135…`) — the fix build script.
- `file-15-fix-stdin.py` — the filer (build → in-memory verify → PUT).
- `fix-scratch/` — probe scripts (Hub tip/blob/tree checks, walk
  inspection, Personal player extraction). Scratch only.
- Prior round files untouched: `build-15-slides.js`,
  `WALK-15-8DOORS-REPORT.md`, `WALK-15-8DOORS-CHECKER-REPORT.md`.

## 8. FILING RECORD
- Walk commit: `669b44c321dcd313d7f8ce9b7d5d22addb645f19`
- Build-script commit / tip after walk filing:
  `800251aa846264e7c58be0588bdc53ce4c4a7fe0`
- This report: `walk-15-8doors-20261121/WALK-15-8DOORS-MAKER-REPORT-V2.md`
  — filed after the walk, on the same branch; its own commit and the
  resulting branch tip are in the maker's handoff to the coordinator
  (a report cannot name its own commit sha before it exists).
