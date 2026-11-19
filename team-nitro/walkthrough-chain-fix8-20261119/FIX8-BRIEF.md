# WALKTHROUGH FIX-8 BRIEF — the agreement shell renders broken at desktop

**Base:** fix-7 landing — branch `walkthrough/chain-fix7-20261119`, commits `3fb28971` + `3c621b7d` (15 files, every blob read-back verified). Records: `~/workspace/team-nitro/walkthrough-chain-fix7-20261119/`.
**New branch:** `walkthrough/chain-fix8-20261119`.
**Eye verdict on fix-7 (cloud browser, desktop 1920×999, 2:33–2:43 PM MST): GOES BACK.** The shell is broken at desktop width — the agreement is not readable, and the frames never display their content. The eye signed in, submitted, signed up, or agreed to nothing. Staged only. One lane, one round.

## Activation (read FIRST, before any work)
- `~/workspace/team-nitro/THE-NAYA-DESIGN-LAWS.md` (the rule book — MUST / MUST NOT, text laws, 25/19/17 scale, the §11 check)
- `~/workspace/team-nitro/THE-PLAYBOOK.md` (the HOW)
- `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md` (the WHY)
- `~/workspace/team-nitro/THE-ANATOMY-OF-A-SMART-APP-PAGE.md` + `~/workspace/team-nitro/THE-HEART-OF-THE-MACHINE.md`
- `~/workspace/team-nitro/THE-ULTIMATE-ORIENTATION.md` + `~/workspace/team-nitro/THE-ARMY-TRAINING.md`
- After the work: check against the laws in writing (§11 + `check-design-laws.py` + the eye). Laws delta must be 0. If it breaks the laws, redo.

## The eye's findings — the fix checklist (all desktop 1920)
**F1 — Frame 1 renders as a ~90px strip.** Only its top bar and the top half of the "Hi, I'm Naya" heading are visible; the paragraph and the "Keep reading ◆" / "Next ◆" buttons are clipped below the strip and never visible on screen. The frame's content must sit INSIDE its visible area — heading whole, text whole, buttons visible.

**F2 — The board goes blank by itself.** Within a few seconds of loading, with NO input at all, the page pins a full-screen ornate frame and the content vanishes. From then on the viewport shows only an empty black frame. Scrolling back up (up to 20 pages), Home, Ctrl+Home, Tab, clicking Play, and clicking inside the frame all failed to restore the content or return to the hero. A new visitor who just reads watches the agreement disappear. The pinned state must never swallow the content; the content must stay visible and reachable.

**F3 — No visible frame-by-frame movement.** Clicking Next / Keep reading by their page references changed the page data once (the intro paragraph and "Keep reading" disappeared and an image "The old internet — a woman drowning in tabs, notifications, and noise" appeared in the data) but nothing became visible on screen, and a second Next click did nothing at all. The full agreement exists in the page data (47 frames) but none of it ever renders in the board. Next / Keep reading must move frame by frame, visibly, every click.

**F4 — Play does nothing visible.** The Play button ("Play — read the agreement with Naya") produced no visible change when clicked (tried twice, once with a 4-second wait). Play must do something visible — the agreement read with Naya, in the frame.

**F5 — Naya's top-bar photo is flaky.** Frame 1 only, in the brief strip state: a round photo of a woman at the left of the top bar. It rendered on most loads, was still loading (dark circle) on one reload, and failed to load entirely ("loading or decoding failed") on one fresh tab. Frames 2–47 never displayed on screen, so their top-bar pictures could not be verified. The picture element exists in the page data for all 47 frames ("Naya speaking"). Every frame's top-bar picture must load reliably and show.

**F6 — Home page entrance + top nav invisible.** On the walkthrough home page, the entrance section ("NAYA WELCOMES YOU", saved-account "Jump back in as…" buttons, "Create. Connect. Grow with us.") and the top navigation links (HOME, PRICING, ABOUT US, POWERCAST, WHITE PAPER, ACADEMY, AI SCORE, LIFE WITH NAYA, ASK NAYA) exist in the page data but are not visible on screen — only "‹ Login" (top-left) and a small purple diamond (top-right) show — and scrolling up / Ctrl+Home does not reveal them; the home page sits at its agreement section. The home page's agreement section itself renders fine as readable cards (Naya's photo visible, with its own scrollbar) — DO NOT BREAK IT. The entrance and the nav must be visible and reachable.

**F7 — The "big red piece with an N" does not match.** What the frame standard describes (a big red piece with an N, just above the three buttons) is not what shows: the visible N medallions are purple/silver, not red; the "NayaNET" logo image that sits above the buttons in the page data never renders; and NO frame has three buttons — frame 1 has two ("Keep reading ◆", "Next ◆"), frames 2–46 have two ("‹ Back ◆", "Next ◆"), and the final frame has two different buttons. No Back button appears on frame 1. Reconcile the frame to the standard: the N piece and the button row must read as the standard describes, in the frame, visible.

**F8 — THE WELCOME BUTTON: none exists.** The eye found NO button or pill reading "Welcome" on either page. "Welcome" appears only as plain text: on /agreement, frame 44's heading "Welcome home. Your world begins here." and the final frame's caption "The Collective Agreement — between NayaNET and you. Welcome aboard."; on the home page, the heading "NAYA WELCOMES YOU" (in page data, not visible), the subtitle "Welcome. Let's begin with trust." centred under "The Collective Agreement", and "AGREED ◆ WELCOME HOME." centred under Naya's photo. None is a button or pill, and none does anything. Confirm in the fix that no Welcome button or pill is introduced anywhere on either page.

## Known gap — NOT this round's scope (do not claim it fixed)
The 8 per-frame face images (`face-{1,3,4,5,6,7,8,9}.jpg`) are NOT in the repo — the frame JS will 404 them until the asset round files them. Fix-8 must render correctly with what is in the repo; note the gap in the report, do not wait on it.

## Rules
- HARVEST FIRST. Take the fix-7 shell's code verbatim and edit it — do not rebuild, do not make a new version. Compose, never create.
- Verify first: render proof before filing. Maker → checker (fresh bytes + render) → captain's eye. Nothing reaches Shawn that hasn't passed the eye.
- Laws delta 0. Small round — one hour max.
- Staged only. Nothing live. Do not sign in, submit, sign up, or agree to anything during verification.
- Report back: branch, tip commit, blob sha + byte size for every filed file, laws delta, and what renders now (frame 1 whole, Next/Keep reading moving visibly, Play doing something visible, photo loading, home entrance + nav visible, no Welcome button/pill).
