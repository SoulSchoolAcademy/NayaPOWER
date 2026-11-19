# Walkthrough Fix-9 — Brief (2026-11-19)

## Assignment
Fix the three measured gaps from the fix-8 checker (verdict GOES BACK), so the agreement reads as a framed presentation all the way through — his words ~15:44 MST: "if we reframed it the whole thing would be a better presentation." The fix-8 round rebuilt the shell; this round finishes the reframe.

## Base — harvest, never rebuild
- Base: `walkthrough/chain-fix8-20261119`, tip `aa35e2c971a45274a511e8fa68f2a7d1ee103aa2`
- Checker report (the whole assignment's proof): `~/workspace/team-nitro/walkthrough-chain-fix8-20261119/CHECKER-REPORT.md`
- Maker report: `~/workspace/team-nitro/walkthrough-chain-fix8-20261119/MAKER-REPORT.md`
- Staged now: https://naya-walk-beginning-staging.nayapower.workers.dev/ (agreement sha `11130770`, home sha `2062739e`)
- New branch: `walkthrough/chain-fix9-20261119`
- Records dir: `~/workspace/team-nitro/walkthrough-chain-fix9-20261119/`

## The three gaps (checker's own fresh bytes + render — fix exactly these)
1. **F1 — frame 1 shows no agreement words at load.** The reading window (219px) is shorter than the media board (183px) + first paragraph offset (+227px); all paragraphs `vis:false` at load. A visitor who never discovers the inner scroll reads nothing. Fix: the first paragraph's words must be visible at load without discovering the inner scroll — shrink/slim the media board, lift the text, or both.
2. **F3 — no way back from the final frame.** Next +1 every click through all 47 frames and Back works 3→2→1→0 — but the final frame's visible row holds only "I agree"; the 47 jewel dots are display-only spans (clicking dot 23 left cur at 46); only "read the whole agreement at once" returns (cur → 0). Fix: add a working Back on the final frame (and/or make the jewel dots real navigation), so a visitor can step back without restarting at frame 1.
3. **F7 — seal and button row not uniform.** 3 buttons on every reading frame cur 0–45, but the red seal exists only on frame 1 (frames 2–46 have none); the final frame has 1 button only ("I agree") with its seal `display:none`. Fix: red seal on every frame; final frame keeps the three-button row (Back + the I-agree action) with its seal shown, not `display:none`.

## What already PASSES — do not touch, do not regress
- F2: the board never goes blank by itself (t+2s vs t+10s identical).
- F4 (corrected): the orb reveals the waiting note; 0 `<audio>`, 0 `<video>`, nothing plays.
- F5: all 47 frames' faces render; all 8 faces + deck-logo + welcome-0 serve 200.
- F6: home entrance + top nav visible; all 9 nav links present; `?stage=bridge` opens the stage.
- F8: no button reading "Welcome" anywhere.
- F9 (corrected): AUDIO orb above VIDEO button; staged `/agreement` bytes contain no audio, no mp3 name, no NotebookLM filename; both buttons reveal their waiting notes on tap.

## NOT in this round
- **Anthem video wiring — separate round after fix-9 lands.** The video is live on YouTube (https://www.youtube.com/watch?v=a06pPpxRil4, "NAYANET: Welcome Home — Meet Naya, Your Guide to a New Internet!"). It goes in the agreement frame at the second level down, the little bit about it on the SIDE of the frame, per the master video template. Do not wire it here — same file, one lane one round.
- **Audio — waits on Shawn.** The audio is cut FROM his video; he cuts it. Do not wire `agreement-naya-voice.mp3` (filed but unwired; do NOT delete it — deletion was never instructed).
- **The 8 per-frame face images** are owed to the repo as an asset round, not this one. They serve 200 from the proof-host and render; leave that alone.

## Process (the law)
- Read `~/workspace/team-nitro/THE-NAYA-DESIGN-LAWS.md` FIRST, then THE-PLAYBOOK.md, then DESIGN-INTELLIGENCE-REPORT.md, plus THE-ULTIMATE-ORIENTATION.md and THE-ANATOMY-OF-A-SMART-APP-PAGE.md. Design-laws delta must be 0 vs base (welcome 83/4, identity 11/2, walk 128/8, unfold 1/2).
- Maker → checker (fresh bytes + render) → captain's eye. Staged only; nothing goes live. One lane, one round: no other round touches these files while this one runs. One hour max.
- The checker re-proves F1, F3, F7 in bytes AND on render, and re-proves the six passes above still hold.
- Do not remove anything Shawn didn't ask to remove. Do not redesign his pages — harvest the systems we have and compose.
