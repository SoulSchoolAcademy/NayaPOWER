# SN-4577 — Personal R5 — Render Proof Landed: Mostly Pass, Three Real Fails

**Category:** PERSONAL — the R5 render proof — 2026-11-21 ~13:29 MST

*Paired Naya Note: NN-20261121-personal-r5-render-proof-landed — the verbatim record of the proof.*

**Filed:** SN-4577 — Intelligence Loop run 475, 2026-11-21. Build ~13:13 MST; proof 13:13–13:29 MST, task `77cac025`, 1920px only, as recorded in the curated memory. Tip commit `f04a783c`, blob `50867d86`. Lane: `~/workspace/team-nitro/personal/side-rail-fix-20261121/`.

## In a Nutshell

The checker PASS was a milestone, never the verdict — the render proof is the verdict's first half: mostly pass, three real fails. (1) The stub STILL did not land — the proof post hit the "one-time permission from Shawn" gate and NO card landed, not even a stub; the R5 resolver is in the bytes but did not fire at runtime (diagnostic owed). (2) The right sidebar cannot be reopened by click — × closes it, Menu cycles without reopening it, only reload restores it. (3) No single labelled Mail↔Messenger toggle found — Personal Mail and Personal DMs both land on the same rooms/mail, and that page's rooms menu has no Messenger room. PASS: loads clean, rail renders 13 people, About/Skills scroll, Invite → joinus, Calendar button reads "Calendar" and nav works, WORLDS → /space, ADD menu + composer, bottom bar = locked six.

## The Lesson

**PERSONAL ROUND — R5 COMPLETE ON BYTES, RENDER PROOF LANDED (2026-11-21 ~13:13 MST build; proof 13:13–13:29 MST, task `77cac025`, 1920px only):** coordinator `37e5034c` complete. Tip commit `f04a783c`, blob `50867d86`, 10,517,341 B, sha `578b2102…` — staged link verified 200 + exact sha. R5 checker PASS: Calendar rename is exactly 4 lines, delta 0; everything already passing still passes; §11 design laws delta 0.

**RENDER PROOF — MOSTLY PASS, THREE REAL FAILS.** PASS: loads clean (feed shows live SN-4569/4568/4567), rail renders 13 people in match order with i/DM/Mail/Audio/Video buttons, About/Skills scroll to sections, Invite → joinus, Calendar button reads "Calendar" and month/day nav works, WORLDS → /space, ADD menu "Which feed?" + exactly four rows + in-page composer, bottom bar = locked six. FAILS: (1) **the stub STILL did not land** — proof post "Proof test — do not publish" hit the "one-time permission from Shawn" gate and NO card landed, not even a stub; the R5 resolver is in the bytes but did not fire at runtime (diagnostic owed); (2) **the right sidebar cannot be reopened by click** — × closes it, Menu cycles without reopening it, only reload restores it; (3) **no single labelled Mail↔Messenger toggle found** — Personal Mail and Personal DMs both land on the same rooms/mail, and that page's rooms menu has no Messenger room. NOT VERIFIED: photo grids (no file picker, no files granted), deep-cyan gem beside "Connect with Like Minds", JS errors by console (visible behaviour only), any phone-width behaviour. Audio/Video show the honest "aren't here yet — they arrive with Smart Meet" lines; the DM room opens but says "this room capability is not exposed yet"; Send button present, never clicked.

**NOT DONE (named, not hidden):** rail auto-organize NOT achieved (neither file derives people from feed items — needs a BUILD, not a harvest; captain's call); Item 3 intelligent boards NOT done (no buildIntelLayerBoards transplant, flip unverified); DM Audio/Video NOT built — but harvestable player cores EXIST in the bytes (PowerCast player + #saTheatre stage player), a follow-on round could wire them; Message Send disabled ("Send · runtime required") — messenger opens but cannot send yet; bottom-bar MAIL bypasses the toggle page (goes to nayanet.app/rooms/mail); ECOSYSTEM tile goes to nayanet.app/hub, not the drawer.

**FOLLOW-UP QUESTION OWED TO SHAWN:** the calendar view heading and settings button still say "My World" beside the "Calendar" button — rename those to "Calendar" too, or leave them? (Brief ordered the button only; checker says ask, don't silently fix.)

## Why It Matters

The checker PASS was a milestone, never the verdict — and the render proof is the verdict's first half: mostly pass, three real fails. The stub still did not land even though the resolver is in the bytes — it did not fire at runtime, and that diagnostic is owed. The sidebar cannot be reopened by click, which is the exact failure SN-4542 was filed for. And the Mail↔Messenger toggle — the one-page-with-a-toggle from SN-4544 — is not found as a single labelled control. Those three are the next round, named exactly. Phone-width behaviour is still unverified — the thing he judges first is the thing the cloud browser cannot prove.

## How to Use It

The diagnostic on the stub resolver comes first: why bytes that contain the resolver do not fire it at runtime. The sidebar reopen is a click-level fix, proven by click. The toggle must be one labelled control, found by the walk. Nothing here is claimed done that the proof did not pass.

## Owed from This Dictation

- Stub-resolver diagnostic: R5 resolver in bytes, did not fire at runtime.
- Sidebar reopen by click (SN-4542's failure, still open).
- One labelled Mail↔Messenger toggle, found by the walk.
- Follow-up question to Shawn: "My World" heading + settings button — rename to "Calendar" too, or leave them?
