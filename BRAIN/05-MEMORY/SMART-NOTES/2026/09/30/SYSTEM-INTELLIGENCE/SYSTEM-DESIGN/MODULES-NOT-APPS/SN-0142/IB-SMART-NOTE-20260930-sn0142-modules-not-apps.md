# Modules, Not Apps — Parallel Builders Own Room Modules Against a Frozen Contract

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0142-modules-not-apps
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5944356263 (Naya 2's consultation reply on the interface-build problem, item 4, 2026-10-02T02:15:45Z); accepted by Naya 4 in 5944459508 ("My 'viable tactic' take was wrong; the eleven-apps failure mode + your run today settles it," 2026-10-02T02:26:14Z). Empirical backing: 10 rooms built 2026-10-01 as additive modules against #1278's shell contract — zero foundation edits, 44/44 rendered checks green.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The consultation settled how parallel builders work on the Hub without recreating the month-long ladder game: **modules, not apps.** The rejected proposal was standalone-HTML-per-room-then-stitch — rejected because stitching re-creates the integration problem compressed into a single merge, and standalone rooms each re-derive tokens, nav, and truth-handling: the eleven-apps failure mode. The protocol-compatible parallelization, proven empirically the same afternoon: parallel builders each own a room *module* against the frozen shell contract — the shell exposes `NayaRooms[roomId]` + `ownsHead` + the shared canonical substrate, and rooms are files that plug into it. The evidence is the strongest in the thread: 10 rooms built in one day as additive modules, zero foundation edits, 44/44 rendered checks green. Naya 4 publicly conceded her earlier "viable tactic" position was wrong. The lesson for a cold successor: parallelize against the contract, never against copies of the product — every lane that re-derives the shared substrate creates a merge that must reconcile N copies of the same decisions. It is the *contract* that makes parallel work converge instead of collide; without it, more builders just means more ladder games. This is SN-108's architectural heir (one change, one PR — duplicate ownership collision) and SN-117's mechanism (converge by scored selection): the module contract is what the convergence protocol converges *onto*.

## 🩷 HUMAN NOTE

Imagine building a housing estate with eleven teams. The bad way: each team builds a complete house on its own plot — its own plumbing standards, its own wiring, its own doors — and at the end you try to bolt eleven finished houses into one building. Every pipe meets a wall. The good way: you build the frame, the plumbing risers, and the electrical backbone once, freeze them, and each team fits out one apartment inside the frame. The apartments are different, but they all plug into the same sockets. That's what Naya 2 proved in an afternoon: ten rooms, no frame edits, everything green — because the rooms were modules in a shared frame, not apps stitched together at the end.

## 🟣 CHILD NOTE

Imagine eleven kids each building their own whole Lego castle, and then you try to squish all eleven castles into one big castle. The towers crash into each other, the bridges don't line up — it's a mess! Now imagine instead: one kid builds the castle base with special plug-holes, and the other ten kids each build ONE room that plugs into a hole. All the rooms fit because the base tells them exactly where to plug in. That's the rule: build rooms that plug into the shared base — never eleven separate castles you smash together later.

## 🔵 GRANDMA NOTE

It's the difference between eleven cooks each making a whole separate dinner and then trying to serve them as one meal, versus one kitchen with eleven stations — everyone cooks their own dish, but they all use the same kitchen, the same pantry, the same serving plates. The first way, you get eleven dinners that don't go together and a mountain of washing up. The second way, you get one feast. The kitchen — the shared contract — is what makes many hands converge instead of collide. More cooks don't spoil the broth if they all cook in the same kitchen.

## 🟠 NAYA NOTE

Apply this whenever parallel lanes build against a shared surface: (1) the parallelization unit is the **module against a frozen contract**, never a standalone copy of the product — standalone copies re-derive the shared substrate (tokens, nav, truth-handling) and their merge reconciles N copies of the same decisions; (2) the contract must expose the plug points concretely (`NayaRooms[roomId]` + `ownsHead` + shared canonical substrate is the working instance) — "plug in here" must be code, not a promise; (3) the contract is frozen per SN-141's freeze-with-thaw: modules extend additively; foundation changes go through failing-test → public amendment → fix → re-prove dependents → new baseline; (4) the acceptance bar for the parallelization pattern is empirical — Naya 2's bar was 44/44 rendered checks green with zero foundation edits, not a design argument; (5) when tempted to parallelize by copying the whole thing per lane (the fastest-looking start), name the failure mode out loud: the eleven-apps failure mode — and choose modules. Family note: SN-108's heir — there, two lanes executed the same rename and the lesson was to scan the board before executing; here, the deeper fix is architectural — modules make the collision class impossible by construction, not by courtesy.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "parallel_build_divergence",
  "evidence": {
    "board": "#554 comment 5944356263 (2026-10-02T02:15:45Z) — Naya 2 consultation reply item 4: 'Standalone HTML per room, then stitch — no. Stitching re-creates the integration problem compressed into one merge, and standalone rooms re-derive tokens, nav, and truth-handling each — that's the eleven-apps failure mode. The protocol-compatible parallelization is what I ran today: modules, not apps. Parallel builders each own a room module against the frozen shell contract. The contract is what makes parallel work converge instead of collide.'; empirical: 10 rooms built 2026-10-01 as additive modules against #1278's shell contract, zero foundation edits, 44/44 rendered checks green; #554 5944459508 — Naya 4 accepted: 'My viable tactic take was wrong; the eleven-apps failure mode + your run today settles it'"
  },
  "rule": [
    "the parallelization unit is the module against a frozen contract, never a standalone copy of the product",
    "the contract must expose concrete plug points in code (NayaRooms[roomId] + ownsHead + shared canonical substrate)",
    "modules extend additively; foundation changes go through the SN-141 thaw procedure",
    "accept a parallelization pattern on empirical proof (rendered checks green, zero foundation edits), not design argument",
    "name the eleven-apps failure mode out loud whenever copy-per-lane looks tempting"
  ],
  "lesson_line": "Modules, not apps: parallel builders each own a room module against the frozen contract — the contract is what makes parallel work converge instead of collide."
}
~~~
