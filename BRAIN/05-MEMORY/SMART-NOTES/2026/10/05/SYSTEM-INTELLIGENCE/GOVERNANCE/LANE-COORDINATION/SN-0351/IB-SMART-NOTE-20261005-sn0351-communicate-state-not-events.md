# Communicate State, Not Just Events — The Sign-In/Out Law

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0351-communicate-state-not-events
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Shawn directive, main chat 2026-10-05 ~07:30 PDT — "there's gotta be a set process... you're signing in and out... this is where I'm at, this is what I'm working on, this is what we achieved, this is what I suggest we do next"

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On the morning of 2026-10-05, the Governed Production Promotion workflow was dispatched four times (06:48, 06:53, 06:54, 07:15 PDT) and the 06:54 run actually deployed production (`b057720e`, policy-enforcement step skipped while deploy steps succeeded). The post-mortem found the root cause was not technical — it was communicative. The lanes WERE signing in and out on the board. What they were posting was events ("started X", "finished Y", receipts) without state: nobody's posts said where they were at, what problems they'd hit, or what they were about to ask the human director to click. Shawn was asked to click four times without the full picture; Naya 4 relayed an unverified lane report ("nothing deployed") as fact. Silent coordination produced real damage.

Shawn's ruling, same morning: every board touch must carry full state, every time, from every lane. The 554-trail rule (2026-10-01) logged events; this law adds the state layer on top of it:

**SIGN-IN** (before touching work): lane / seat / scope (what I'm about to touch, so no silent collisions) · intent + why (what I'm trying to achieve) · dependencies (what I need from others, what might affect them).

**SIGN-OUT** (after work): what I did + evidence (branch, commit, PR, test counts) · the state I left behind (what is true now that wasn't before) · problems hit (anything that didn't go as expected) · what I suggest next + who it's for — tag them — or the explicit words "no action needed."

The deeper doctrine: every action must be documented with WHAT was done and WHY — an action ledger where every entry carries its rationale. This is the Scorecard Law's receipt requirement extended from decisions to all actions: no silent moves, no context-free events. A cold successor reading the board must be able to reconstruct not just what happened, but the reasoning state of every lane at every step.

Why this is brain-grade: teams don't fail from lack of talent; they fail from lack of shared state. Every "I didn't know you were doing that" is a communication defect with a mechanical fix. Months from now, when a seat posts a bare "done" receipt with no state, this note is the correction: events tell the log what happened — state tells the TEAM what to do next.

## 🩷 HUMAN NOTE

Shawn — this is your sign-in/out ruling from this morning, captured as law. The production incident happened because the lanes were posting events without state: sign-ins and sign-outs that never said where anyone was at, what problems they'd hit, or what they were about to ask you to click. The new bar: every board touch carries the full picture — where I'm at, what I'm working on and why, what I accomplished (with proof), what problems came up, and what I suggest next, tagged to whoever it's for. Or the explicit words "no action needed." Naya 4 posted the exemplar on #1354 the same morning — leading by example, not just describing. The deeper piece is your action-ledger vision: every action documented with what and why, so a future Naya can reconstruct not just what happened but what every lane was thinking.

## 🟣 CHILD NOTE

Imagine a team building a giant Lego castle, but nobody says what they're building — they just shout "done!" when they finish a piece. Soon two people build the same tower, nobody builds the door, and someone glues a piece on crooked because they didn't know it was load-bearing. That's what happened: everyone said "done!" but nobody said what they were doing. The new rule is simple: before you start, say what you're going to build and why. When you finish, say what you built, what went wrong, and what should happen next — and name who should do it. Then everyone always knows what's going on, and nobody glues the wrong piece.

## 👵 GRANDMA NOTE

A good kitchen runs on call-outs: "behind you with the hot pan," "soup's on in five," "we're out of thyme." Nobody just silently finishes a dish and walks away — everyone announces what they're doing, what's ready, what's missing, and what they need next. That's all this law is: the team's call-outs. Before starting work, announce your intention. After finishing, announce what you did, what went wrong, and what should happen next — and say who it's for. The morning's trouble came from a quiet kitchen where everyone assumed someone else knew.

## 💜 NAYA NOTE

For any future seat posting to the board: a sign-in/out without state is a defect, not a courtesy. Minimum viable board post:

SIGN-IN: `Lane / seat / scope` — name exactly what you are about to touch (branch, workflow, area). `Intent + why` — the outcome you're pursuing and the reason. `Dependencies` — what you need from others, and what of yours might affect them.

SIGN-OUT: `Actions + evidence` — what you did, with branch/commit/PR/test counts. `State left behind` — what is true now that wasn't before. `Problems` — anything unexpected, however small. `Suggestions + owner` — what should happen next and WHO it's for (tag them), or the literal words "no action needed."

Never post a bare "done." Never assume another lane read your mind. The exemplar is Naya 4's #1354 post of 2026-10-05 ~07:35 PDT (the communication-law rollout post) — copy its shape. Shawn's action-ledger vision (every action documented with what + why) is the direction: receipts for decisions (Scorecard Law) extend to receipts for all actions.

## 🖥️ MACHINE NOTE

{"sn": "SN-0351", "title": "Communicate State, Not Just Events — The Sign-In/Out Law", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "LANE-COORDINATION"], "cousins": ["SN-0350", "SN-0340", "SN-0343"], "evidence": {"directive": "Shawn, main chat 2026-10-05 ~07:30 PDT: set process for sign-in/out — where I'm at, what I'm working on, what I achieved, problems, what I suggest next; every action documented with what and why; smart ledger vision", "incident": "2026-10-05 06:48-07:15 PDT: 4x workflow_dispatch of Governed Production Promotion; 06:54 run deployed production b057720e with policy-enforcement step skipped; #1354 5996124057 (sweep alert), Naya 2 decision brief 5996448226", "prior_rule": "554-trail rule (Shawn, 2026-10-01): log starting/finishing/findings — events without the state layer this law adds"}, "rule": "every board touch carries full state: SIGN-IN = lane/seat/scope + intent/why + dependencies; SIGN-OUT = actions/evidence + state left behind + problems + suggestions/owner (or 'no action needed'); bare 'done' receipts are defects", "exemplar": "Naya 4 #1354 post 2026-10-05 ~07:35 PDT (communication-law rollout) — copy its shape"}
