# One Second-Eyes Pass, Not Two — Route the Verdict to the Seat Holding the Truth

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0330-one-second-eyes-pass-not-two
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5988946078 (Naya 2, v9 relay receipt, 2026-10-04) / 5988848308 (Naya 4, v9 delivery with receipt, 2026-10-04)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When Naya 4 delivered the v9 Ask Naya build, Naya 2 did the receipt, not the render. Her relay (5988946078) confirmed every build claim against live bytes: branch `naya4/ask-naya-v9` → commit `a7c9bd81bd560d3ef6a09b93e2f1c5986cb07540`, parent `b2d1cc12` == live main tip (no drift, based at the tip), `prototypes/ask-naya-v9.html` 1,569,369 bytes, sha256 `e986c92c8b` — all exact matches to Naya 4's record. Then came the load-bearing move: she routed the *verdict* — the live render, the 9-chip board typography, whether the three new exchanges feel like the same Naya — to the main seat, who holds the Ask Naya design truth. She did not render it herself: "I'm not rendering it here so we don't duplicate her pass — one second-eyes pass, not two."

Why this is brain-grade: multi-seat teams burn their scarcest resource — coordinated night hours — on duplicated verification. The discipline splits verification into two layers with different owners. The **receipt layer** (branch → commit → parent == live tip → exact byte count + sha256) is mechanical; any competent seat can run it. The **verdict layer** (does it look right, feel right, hold the design truth) belongs to the seat holding the relevant truth. Naya 2 ran the receipt layer fully, then *withheld* the verdict layer and routed it to its rightful owner. Two full render passes would have bought nothing except busyness; one receipt + one verdict bought full coverage at half the lane cost.

Rule for a cold successor: **when a build needs verification and another seat already holds the truth for its verdict, run the byte-level receipt yourself (commit, parent == tip, bytes + hash exact) and route the verdict to the truth-holder. Never duplicate the full pass — one second-eyes pass, not two.**

## 🩷 HUMAN NOTE

Shawn — a coordination doctrine from tonight's v9 handoff worth banking: when my build landed, Naya 2 didn't re-run the whole render to double-check my work. She did the mechanical receipt instead — confirmed the exact commit, confirmed it was based at the current main tip, confirmed the file bytes and hash matched my record exactly. Then she handed the *judgment* call (the live render, the typography, whether it feels like the same Naya) to the main seat, who holds the Ask Naya design truth — and deliberately did NOT do that part herself, so we didn't have two lanes burning night hours on the same render. New rule: verify the receipt yourself, route the verdict to whoever holds the truth. One second-eyes pass, not two.

## 🟣 CHILD NOTE

When a new demo was finished, the second person checking it didn't do the whole check over again. She checked the important *facts* first — the right file, the right version, the right size — all matching perfectly. Then for the *judgment* part (does it look right? does it feel right?), she sent it to the person who knows the design best, instead of doing that part too. Lesson: check the facts yourself, then let the right person give the verdict. Two people doing the whole thing twice just wastes time.

## 👵 GRANDMA NOTE

When one person finished a new demo, the teammate checking it was clever about it: she verified all the facts — correct version, correct size, matched exactly — and then sent the *opinion* part (does it look and feel right?) to the person who knows the design best, instead of redoing that whole judgment herself. The lesson: check the facts yourself, route the judgment to the right expert. Having everyone do everything twice just burns time that could be spent building.

## 🤖 NAYA NOTE

Source: #1354 5988848308 (Naya 4, 2026-10-04 22:47 PDT — v9 delivery: branch `naya4/ask-naya-v9` → commit `a7c9bd81`, parent = main `b2d1cc12`, file `prototypes/ask-naya-v9.html` 1,569,369 bytes, sha256 `e986c92c…`; builder-verified all 10 exchanges tap through to speaking, honest score 9/10; explicit ask: unvarnished verdict on beat path, 9-chip typography, same-Naya feel), 5988946078 (Naya 2, 23:03 PDT — receipt confirmed: branch→commit exact, parent == live main tip, bytes + sha256 exact matches; routing, not verdict: "the live render + unvarnished verdict … is the main-seat lane — she took Problem B intake and holds the Ask Naya design truth. … I'm not rendering it here so we don't duplicate her pass — one second-eyes pass, not two."). Overhead context: 5988535385 (overnight full-send directive; both seats back-and-forth), 5988590842 (collab posture: completions with evidence + explicit review ask). Cousins: SN-0222 (The Relay Flags, the Owner Diagnoses — receipt/verdict split is the routing twin of flag/diagnose), SN-0236 (one repair per RED class — the no-duplication doctrine for repairs; this note is its verification twin), SN-0105 (propose-then-build — no duplicate lanes), the verify-builder-artifacts doctrine (AGENTS.md lesson 2026-09-30 — the byte-level receipt is this doctrine's mechanical form).

## ⚙️ MACHINE NOTE

{"sn": "SN-0330", "title": "One Second-Eyes Pass, Not Two — Route the Verdict to the Seat Holding the Truth", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-04", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "TEAM-DOCTRINE"], "cousins": ["SN-0222", "SN-0236", "SN-0105"], "evidence": {"board": "#1354 5988848308 (v9 delivery with full receipt), 5988946078 (relay receipt + routing)", "receipt_layer": "branch naya4/ask-naya-v9 -> commit a7c9bd81bd560d3ef6a09b93e2f1c5986cb07540, parent b2d1cc12 == live main tip, prototypes/ask-naya-v9.html 1,569,369 bytes, sha256 e986c92c8b — all exact matches", "routing": "live render + verdict routed to main seat (holds Ask Naya design truth); Naya 2 withheld her own render: 'one second-eyes pass, not two'", "verdict_outcome": "open at capture — main seat's pass is the pending verdict"}, "rule": "run the byte-level receipt yourself (commit, parent == live tip, bytes + hash exact) and route the verdict to the seat holding the truth; never duplicate the full verification pass"}
