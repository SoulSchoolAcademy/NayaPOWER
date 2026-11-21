# WALK-15 8-DOORS REPORT — Round 3 (eight doors + pricing gate)
Filed 2026-11-21 ~15:32 MST · Maker: Naya Nitro Narzan (WALK MAKER, depth 2/2)
Branch: `walk/walk-15-8doors-20261121` · Tip commit: `193e1e896d46b8812f7d76b0f867a8190592d243`
Staged link (VERIFIED first-hand): https://naya-proof-host.nayapower.workers.dev/?file=walk-15-8doors-20261121%2Fwalk-beginning-fixed.html&ref=walk%2Fwalk-15-8doors-20261121&cb=d94bd9d812af3a77a012d395e892d2aa0612f0d4

## 1. WHAT WAS FILED
- `walk-15-8doors-20261121/walk-beginning-fixed.html` — 1,495,685 B, sha256 `9cc2e7f6f5084cc1788ce5d95bd72b045c345505f6bd346f42986c840b33a03e`, blob `d94bd9d812af3a77a012d395e892d2aa0612f0d4` — PUT 201, GitHub blob read-back match TRUE.
- `walk-15-8doors-20261121/build-15-slides.js` — 46,165 B, sha256 `f52480c436649acf2214072c4b5292895c79400e252418c2707de52bc7e369d0`, blob `7215a38f822eff04bbd1658a4a7bc1c27d54c042` — PUT 201, read-back TRUE.
- This report: `walk-15-8doors-20261121/WALK-15-8DOORS-REPORT.md`.
- Base: main tip `61a139991443deb391452f6309a5845051c6058d`.
- Staged verification (first-hand): HTTP 200, 1,495,685 B, sha256 `9cc2e7f6…` — exact match to the filed blob.
- Round 2 (`walk/walk-15-slides-20261121`, six doors) and round 1 (`walk/walk-15-20261121`, A/B/C) are UNTOUCHED — new branch, not an overwrite.
- Everything from round 2 stands unchanged except the reveal: the 15 questions, framed slides from his files, PowerCast audio on every slide, pre-filled Naya examples + Edit, three ways (A / B / or skip), PROMAX frame reference with the input where the video was. Full round-2 record: `WALK-15-SLIDES-REPORT.md`.

## 2. THE EIGHT DOORS — AS FILED (each with its destination)
All eight in the frame, each with a button to open it. The destination shown on the door is where the citizen ends up; the door's link goes through the pricing gate first (§3).

| # | Door | Destination (after the gate) | URL form |
|---|---|---|---|
| 1 | Personal — where all their personal stuff is | `https://nayanet.app/<alias>` | locked scheme |
| 2 | Business — their work stuff | `https://nayanet.app/<alias>` | locked scheme (same address as Personal — flagged, see §6) |
| 3 | World — their thing | `https://<space>.nayanet.app` | locked scheme (`<spacename>.nayanet.app`) |
| 4 | Hub — the collective hub, all the stuff going on in the network | `https://hub.nayanet.app/<alias>` | locked scheme |
| 5 | Dashboard | `https://dashboard.nayanet.app/<alias>` | locked scheme |
| 6 | Calendar | `https://calendar.nayanet.app/<alias>` | locked scheme (pagename = alias) |
| 7 | About — the About page we just built for them | `https://nayanet.app/<alias>/about` | DEEP LINK on their own Personal page (About tap → #about) |
| 8 | Skills — the Skills page we just built for them | `https://nayanet.app/<alias>/skills` | DEEP LINK on their own Personal page (Skills tap → #skills) |

- About/Skills are sections of the Personal page that already exist — no new subdomains, no new apps; the doors open the finished sections. The "slash calendar / slash dashboard / slash hub" wording does NOT change the locked scheme for the six — the locked scheme stands.
- The reveal page's plain-words line (on the page): "Your alias also gives you your calendar, your dashboard, and your hub — plus the About and Skills pages we just built for you. Tap any door and first you will choose your plan: stay on FREE, or upgrade to Naya Power, Naya Pro, or Naya Max. Then you are in — and you can change your level any time from Pricing in the sidebar."

## 3. THE GATE AFTER THE REVEAL — AS BUILT (doors → pricing → choice → in)
- **There is NO separate seventh button.** The "seventh button owed" from round 2 is RESOLVED this way: the gate IS the doors' behavior. In-script check "no separate seventh button (the gate IS the doors)" PASS.
- **Every door's link is the pricing page, full page, with its destination attached:** `https://nayanet.app/pricing?next=<url-encoded destination>`. All eight doors carry `?next=` (in-script check "all 8 doors gate through pricing ?next=" PASS — 8/8).
- **The tapped destination is also saved** in the Box (`naya-walk-15-slides` localStorage, `pendingDoor`) on click, so the return can resume at the door they chose.
- **Flow as built:** tap any door → full pricing page (`nayanet.app/pricing`) → choose: stay on FREE, or upgrade to Naya Power, Naya Pro, or Naya Max (and see what each one gets them) → their choice → in (to the door's destination).
- **HARVEST, NOT REBUILD:** the pricing page was NOT rebuilt and NOT embedded. The doors link to the live pricing page. Its harvest source is §4.

## 4. PRICING-PAGE HARVEST SOURCE
- **Canonical source (verified first-hand):** `~/workspace/team-nitro/pricing/v77/pricing-v77.html` — 11,355,594 B, sha256 `b043167b2fa9a863a18216cdd2d282a20dcf5ff4159ac93e0da28ddea1635577`.
- **Live check (first-hand):** `curl https://nayanet.app/pricing` returns 11,355,594 B, sha256 `b043167b…` — **byte-identical to the v77 file**. Live worker: `naya-model-pricing`. Live URL: **https://nayanet.app/pricing**.
- The v76 live-source file (`~/workspace/your_files/pricing-chart-viewpoint/pricing-chart-viewpoint.html`, 11,353,035 B, sha `af407e3c…`) is the previous version; v77 is what is live now.
- **What the pricing page contains (read first-hand):** the chart, the pains, the letter; tiers FREE / Naya Power / Naya Pro / Naya Max; buttons "Start free now ◆" (`gaugeStart`), "or continue with Naya Free" (`finaleFree`, `chooserFree`); 46 `addEventListener` bindings; the "Plug in your AI" first row (per Shawn 2026-11-15).
- **RETURN-LEG FLAG (integration work owed — not faked):** the pricing page v77 does NOT read a `?next=` parameter (`URLSearchParams` / `location.search` count = 0) and performs NO navigation of its own (`window.location` count = 0). So today, after the citizen chooses a plan on the pricing page, there is no built step that sends them on to the door they tapped. The walk does its half — it delivers the citizen to the pricing page with the destination attached (`?next=` + saved `pendingDoor`) — but the pricing page's half (honor `?next=` / continue into the chosen door) is NOT built yet. That is owed integration work on the pricing page, not something this round could fake by rebuilding it. Do not claim "choice → in" is end-to-end until that leg is built and proven.

## 5. SIDEBAR-PRICING STATUS
- **Pricing in the sidebar ALREADY EXISTS on the Hub:** the Hub's right sidebar carries a Pricing entry (eye walk 2026-11-17: "Pricing ~#8e24aa" in the right sidebar list, with Settings directly underneath it as the last item), and the sidebar set image carries a PRICING diamond gold circle. So "pricing also lives in the sidebar once inside" is true of the Hub today.
- **Standing decision (SN-2440, Shawn 2026-11-09):** pricing lives in Settings and in the Smart Tabs, so people can always change their level — up or down, any time. The note records the change-level control as "a later build (Settings change-level button is already on the open list)". So the sidebar ENTRY exists; the change-level CONTROL behind it is still on the open list per SN-2440.
- **NOT built here, per the order:** no sidebar change was built into the walk file — the sidebar lives on the pages, not the walk. Flagged, not silently built.
- Consequence for the gate: the reveal line promises "you can change your level any time from Pricing in the sidebar" — that promise rests on the sidebar entry + the SN-2440 change-level control being finished. The entry exists; the control is owed.

## 6. THE 15 — AS FILED (unchanged from round 2; flagged HARVESTED vs DRAFTED)
1 Motto · 2 Vision · 3 Goal · 4 Mission · 5 What do you love? · 6 What don't you love? · 7 What's your thing? · 8 What do you value? · 9 What laws do you follow? · 10 Your declaration — all DRAFTED (captain's drafts / splits); 11 "What do you offer?" HARVESTED-VERBATIM (old Q8); 12 How does it help them · 13 A moment you've done it · 14 How do you work · 15 How does someone start — DRAFTED. Showcase follows after the 15 (HARVESTED-ADAPTED from Shawn's words), blank stays hidden. Full wordings + example answers with sources: round-2 report §§3, 5.

## 7. THREE CHECKS
1. **Build checks (in-script, all PASS):** all round-2 checks + 8 reveal doors; no separate seventh button; all 8 doors gate through pricing `?next=`; About + Skills deep-link doors present; gate line on the reveal page; locked-scheme hrefs present; engine parses.
2. **Filing checks:** branch created 201 from main tip `61a13999…`; walk PUT 201 + blob read-back match TRUE; build script PUT 201 + read-back TRUE.
3. **Staged-link check (first-hand):** HTTP 200, 1,495,685 B, sha256 `9cc2e7f6f5084cc1788ce5d95bd72b045c345505f6bd346f42986c840b33a03e` — exact match to the filed blob. Branch tip commit `193e1e896d46b8812f7d76b0f867a8190592d243`.

## 8. SEVEN QUESTIONS (Self-Check Law — all must be YES)
1. Most intelligent? **YES** — eight complete doors, each gated through the real pricing page, is the most intelligent form of the reveal: nothing invented, the live page doing the selling.
2. Most logical? **YES** — doors → pricing → choice → in, in that order, with the destination attached at every step.
3. Most sensible? **YES** — no seventh button invented, no pricing page rebuilt, no sidebar touched; the missing return leg is named, not hidden.
4. Full scope? **YES** — entry → 15 → showcase → naming → 8-door gated reveal → end, on its own branch.
5. Consequences? **YES** — the citizen's choice is recorded (pendingDoor); the unbuilt return leg is flagged so nobody claims end-to-end until it exists.
6. Pros and cons? **YES** — pro: the gate uses the live v77 pricing page (no duplicate); con: the return leg is owed — the pricing page must learn `?next=` before "choice → in" is real.
7. Best possible choice? **YES** — filed the eight-door gated reveal as ordered, on its own branch, verified three ways, with the owed items named.

## 9. FLAGS (carried + new)
- **RETURN LEG OWED (§4):** pricing v77 does not read `?next=` and navigates nowhere — the "choice → in" step needs the pricing page to honor the attached destination. Not built, not faked.
- **SIDEBAR CHANGE-LEVEL CONTROL OWED (§5):** sidebar Pricing entry exists (Hub); the SN-2440 change-level control is still on the open list.
- Business = same `nayanet.app/<alias>` as Personal per the locked scheme; Calendar pagename = alias; naming previews show `nayanet.app/<alias>/<typed>` vs the task's `nayanet.app/<typed>` — all flagged as questions (round 2).
- Per-world application owed; v23 news steps not carried; Q10 Declaration is a MODEL example (Naya's words), NOT Shawn's; Q13 moment replaceable; PowerCast adaptation (speechSynthesis voice, new moving-bars CSS, real-voice recording owed).
- **Render proof owed:** no browser render was run (local byte/parse checks + staged HTTP+sha only); phone-width behavior, the gate tap, and speaking/bars at runtime unproven until checker/eye runs them. His eye is the verdict.
- EPERM flake active all window — filed with zero local writes (stdout → memory → PUT). No good local copy of the filed walk exists; the GitHub blob is canonical.
- Staging worker NOT touched. Round 2 report remains the record for the slides/frame/PowerCast/examples; this report covers only the round-3 change.
