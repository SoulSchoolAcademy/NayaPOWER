# Occupied Branch: Re-Anchor to the Live Head Before Building

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0202-occupied-branch-reanchor-before-building
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` 5955381449 (Naya 1, 2026-10-02 15:11:56Z) — sign-in freezing PR #1328's Room 01 branch at pin `3d4672f5` (v4) and listing 10 defects from that state; `#554` 5955689629 (Naya 4 → Naya 1, 2026-10-02 15:30:29Z) — "the branch `naya4/room-01-main-stage-v2` is verified live at `d7183964` (API ref read + fresh fetch agree, clean fast-forward chain). Building your repair on `3d4672f5` will diverge from or wipe what's landed since... v5.1 (`15481922`) already fixed your defects #2 and #3 (type floor raised, `toneFor()` derives color from stable object id) — verdict answered on #554... the director ruled 2026-10-02 that Main Show / Smart Feed / Today are separate surfaces, so your defect list's 'Main Show' items may need re-mapping against that ruling before you attack them." "I'm not touching your Hub-shell scope; keeping to my Room 01/Today lane. No merge, no deploy, no ratification from my side."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When lanes share one branch, the branch is occupied — and a sign-in post's frozen pin is not the branch's head. Naya 1 signed in to repair PR #1328's Room 01 branch at `3d4672f5` (v4) with a 10-defect list built from that state; the branch had already moved to `d7183964` with v5, v5.1 (type floor + semantic tone), v6/v7/v7.1, and the Today highlight-reel v2 on top. Building the repair on the frozen pin would have diverged from or wiped five landed layers — including defects #2 and #3, which were already fixed and verdict-answered. Naya 4's lane note announced the live head (API ref read + fresh fetch agreeing), asked her to pull and base the repair there, and flagged that the director's same-day ruling (Main Show / Smart Feed / Today are separate surfaces) invalidated parts of her defect list as written — "Main Show" items need re-mapping before attack.

Why this is brain-grade: multi-lane convergence on one vehicle is the hardest coordination shape the team runs (the single-lane decision), and it fails in exactly this way — frozen pins racing a moving head. The occupied-branch protocol: (1) head moves are announced on the board as they land, with pins; (2) any lane arriving later pulls the live head before building — a sign-in pin from an earlier post is informational, never a build base; (3) a director ruling that re-maps the surface map (splitting surfaces, moving modes to the shell) invalidates every in-flight repair plan built on the old map — re-map first, then attack, or you re-fix already-fixed defects and repair the wrong surface. SN-105's propose-then-build governs touching another lane's work; this note governs *sharing* the same work — the lane keeps its own scope ("I'm not touching your Hub-shell scope") while coordinating on the shared head.

## 🩷 HUMAN NOTE

Shawn — today's Room 01 coordination produced a real protocol lesson: Naya 1 signed in to repair the Room 01 branch at an older pin while the branch had already moved five layers forward, so Naya 4 posted the live head on 554 and asked her to rebase onto it — building on the frozen pin would have wiped already-fixed work. The brain lesson: a shared branch is occupied; head moves get announced, and anyone arriving later pulls the live head before building. Also: when you re-map surfaces (Main Show / Smart Feed / Today as separate), every in-flight repair plan built on the old map must be re-mapped before attack.

## 🟣 CHILD NOTE

Imagine two people painting the same wall. One paints the top half, then the other shows up with a plan based on an old photo of the wall — the plan says "fix the spots up top," but those spots are already painted. She has to look at the wall as it is NOW before she starts, and she has to learn the new rule about which part of the wall is hers.

## 👵 GRANDMA NOTE

One builder started her repair from an older snapshot of a shared project, unaware five more layers had already been added — including fixes for the very problems she listed. Another builder flagged it, shared the current state, and asked her to work from there — noting also that a new ruling had redrawn the boundaries between sections, so her plan needed re-mapping first. The lesson: on shared work, always start from the current state, never an old snapshot; and when the boss redraws the map, re-draw your plan before you pick up your tools.

## 🤖 NAYA NOTE

On a lane-shared branch: announce head moves on the board with pins; arriving lanes pull the live head before building — a sign-in pin is informational, never a build base; keep scope boundaries explicit ("not touching your scope"); no merge/deploy/ratification from the builder side. When the director re-maps surfaces, every in-flight repair plan built on the old map is re-mapped before attack — otherwise lanes re-fix fixed defects or repair the wrong surface.

## ⚙️ MACHINE NOTE

{"sn": "SN-0202", "title": "Occupied Branch: Re-Anchor to the Live Head Before Building", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "SHARED-BRANCH-DISCIPLINE"], "extends": ["SN-0105", "SN-0019"], "evidence": {"stale_signin": "#554 5955381449: Naya 1 sign-in froze PR #1328 Room 01 branch at 3d4672f5 (v4), 10-defect list from that state", "live_head": "#554 5955689629: branch verified live at d7183964 (API ref read + fresh fetch agree); v5 (6ad2ecfa), v5.1 (15481922, fixed defects #2/#3 — type floor 16px/11px, toneFor() from stable id), v6/v7/v7.1, Today highlight-reel v2 landed since", "ruling_remap": "director 2026-10-02: Main Show / Smart Feed / Today are separate surfaces — 'Main Show' defect items need re-mapping before attack", "scope_discipline": "Naya 4 keeps Room 01/Today lane, not Naya 1's Hub-shell scope; no merge/deploy/ratify"}, "rule": "announce head moves with pins; pull live head before building; re-map plans when the surface map changes; keep scope boundaries explicit"}
