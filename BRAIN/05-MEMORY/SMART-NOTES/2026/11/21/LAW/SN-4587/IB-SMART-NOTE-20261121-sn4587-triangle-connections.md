# SN-4587 — Triangle Connections — Hub, Calendar, Dashboard, Wired Together

**Category:** CONNECTIONS — the triangle, wired — 2026-11-21 ~13:34 MST

*Paired Naya Note: NN-20261121-triangle-connections — the verbatim record of the order and the three legs.*

**Filed:** SN-4587 — Intelligence Loop run 476, 2026-11-21. Order ~13:34 MST; Personal leg DONE checker PASS ~13:59 MST; render proof PASSED 14:00–14:02 MST; Hub leg dispatched ~14:00 MST, as recorded in the curated memory. Lane: `~/workspace/team-nitro/connections/triangle-20261121/`.

## In a Nutshell

Shawn's order: "the personal hub and the dashboard are not connected. Add the calendar to the personal hub, like the button, because you can put it on the calendar URL. And add the dashboard to the stats in the calendar, because that's where you get the stats, right in the calendar." Flow confirmed: portal → hub → calendar with the Dashboard stats inside. Three legs: Personal — DONE, checker PASS (~13:59 MST) AND render proof PASSED (14:00–14:02 MST, 1919px) — fully proven, bytes + render; Calendar — QUEUED on calendar round 2; Hub — DISPATCHED (~14:00 MST). The subdomains answer nothing yet (HTTP 000) — the doors are built before the destinations are live, and that is named, not hidden.

## The Lesson

**TRIANGLE CONNECTIONS (Shawn's order, voice, ~13:34 MST):** "the personal hub and the dashboard are not connected. Add the calendar to the personal hub, like the button, because you can put it on the calendar URL. And add the dashboard to the stats in the calendar, because that's where you get the stats, right in the calendar." Flow confirmed: portal → hub → calendar with the Dashboard stats inside.

**PERSONAL LEG — DONE, CHECKER PASS (coordinator `895f9d68`, completed ~13:59 MST):** `#myworldbtn` on Personal is now an anchor to `https://calendar.nayanet.app/sean` (same button, spot, label, burnt-orange; in-page #myworld view intact); commit `20ac9192`, blob `60c050ac`, 10,517,420 B (+79), sha `0b4fb0f5…`; staged link verified 200 + size/sha exact; checker 7/7 from the filed bytes (navigation proven — no preventDefault intercepts the anchor; design laws delta 0). Calendar destination dark until the calendar lands (known).

**RENDER PROOF PASSED (browser task, 14:00–14:02 MST, 1919px):** page loads ("Shawn's Personal feed — NayaNET"); Calendar button confirmed right after About, label "Calendar", href exactly `https://calendar.nayanet.app/sean` (read from the element); tap navigated to that address and failed with a DNS error — expected, the address is not live yet, and it is the address failing, not the page; Back returned to the staged page intact (same bar, header, feed SN-4578/4577/4576). One qualification: the browser could not locate a literal "#myworld" identifier or labelled Settings control in the accessible elements — the in-page personal-feed view itself was verified intact instead; the checker had already proven the view div 1→1 from the bytes. Personal leg fully proven (bytes + render).

**CALENDAR LEG — QUEUED on calendar round 2:** "Your Stats" / Daily Reports door → `https://dashboard.nayanet.app/sean`, in-page Daily Reports view intact; base = round 2's tip.

**HUB LEG — DISPATCHED (~14:00 MST, new coordinator `5ef335d4`):** Hub file verified to have NO calendar or dashboard door (zero refs); build both doors on Hub fix-1e base `30c7244d`/blob `485cdf63`, harvested from the Personal bar pattern, staged only.

**LIVE STATES:** dashboard.nayanet.app + calendar.nayanet.app answer nothing yet (HTTP 000).

## Why It Matters

Three apps that do not connect are three islands, and the citizen has to swim between them. The triangle is the flow itself: portal → hub → calendar, with the Dashboard's stats sitting inside the calendar where the citizen already looks at their day. Each leg is small — a button here, a door there — but together they make one system instead of three pages. The honest edge is stated plainly: the doors point at subdomains that answer nothing yet, so the wiring is proven at the button while the destinations are still being built. A door to a dark address is a promise, not a lie — as long as it is named as a promise. The Personal leg shows what "proven" means here: bytes say the anchor is right, the render says the tap goes to the right address, and the DNS error is the address failing, not the page — three different kinds of proof, all pointing the same way.

## How to Use It

Personal's button already points at the calendar URL — proven at byte and render level; the calendar's stats door points at the dashboard URL when round 2 lands; the Hub's two doors are being built on the fix-1e base from the Personal bar pattern. When calendar.nayanet.app and dashboard.nayanet.app answer, the triangle closes — portal → hub → calendar with stats inside — and the flow is proven end to end at click level.

## Owed from This Dictation

- Calendar leg (round 2): "Your Stats" / Daily Reports door → dashboard URL.
- Hub leg (coordinator `5ef335d4`): calendar + dashboard doors on the fix-1e base.
- The two subdomains going live (calendar + dashboard) — the triangle closes only then.
