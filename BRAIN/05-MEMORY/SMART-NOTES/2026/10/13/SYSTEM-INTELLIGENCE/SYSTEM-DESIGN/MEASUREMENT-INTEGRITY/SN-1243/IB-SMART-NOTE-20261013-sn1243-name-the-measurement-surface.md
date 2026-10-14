# Name the Measurement Surface Before Judging the Verdict

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1243-name-the-measurement-surface
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** lesson-broadcast.md t0695 entry ([NAYA NARZAN 4] cold-Naya proof, 2026-10-13) — mission snapshot existed twice: fresh on branch naya/mission-state, stale on main; a fresh clone reads main by default, so the cold Naya's "last verified 10:08 PDT" reading was CORRECT on the surface she used; fix: boot entry must name exactly one canonical home + the fetch command — done in PR #2561. Corroborated by shared-state.json mission_snapshot_note (2026-10-13 ~17:08 PDT): "cold-activation repair PROPOSED (READ-ME-FIRST routes cold Nayas to capped #2175; snapshot stamps stale tip) — new top hole."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A cold Naya's measurement was called wrong. It wasn't — it was right **on the surface she read**. The mission snapshot existed in two places: fresh on the branch `naya/mission-state`, stale on `main`, and a fresh clone reads `main` by default. Two truths, one default read, one stale surface: a verdict that is correct on its surface and wrong about the world. The repair is not to relitigate the verdict — it is to name **exactly one canonical home plus the fetch command** in the boot entry (shipped in PR #2561). The lesson for every future dispute: **when a measurement surprises you, ask which surface it was measured on before calling it wrong.** Two readings from two surfaces are not a contradiction; they are a naming failure.

Why this is brain-grade: cold successors are the entire point of the brain — if the first thing a cold Naya reads is a stale surface presented as canonical, every downstream judgment inherits the rot while looking evidence-backed. The failure mode is silent: each surface is self-consistent, so no single reader can detect the split from inside it. Naming one canonical home with the exact fetch command is the only fix that survives a cold start, because a cold start cannot ask follow-up questions.

## 🩷 HUMAN NOTE

Shawn — the cold-Naya proof today caught a nasty one: the mission snapshot lived in two places, one fresh and one stale, and a fresh clone reads the stale one by default. So a Naya read "last verified 10:08 PDT," said so honestly, and was wrong about the world while being right about what she saw. The fix is already built (PR #2561): the boot entry now names exactly one canonical home and the exact command to fetch it — no ambiguity a cold mind has to resolve. The standing lesson is the first line of defense: before calling any surprising measurement wrong, ask which surface it was measured on.

## 🟣 CHILD NOTE

Imagine your classroom has two clocks — one on the wall, one in the hallway — and they show different times. A new student walks in, reads the wall clock, and tells you it's 2:00. She's not lying! She read the clock she was supposed to read. The problem isn't the student; it's that nobody said which clock is the real one. Now the teacher tapes a sign on the door: "The hallway clock is the official time, and here's how to read it." That's the fix — name the one true clock and show exactly how to read it.

## 👵 GRANDMA NOTE

There's a reason the post office has one official clock and everyone sets their watch by it. If the bank's clock says noon and the town clock says twelve-fifteen, people will miss appointments and blame each other, when the real problem is that nobody agreed which clock counts. The team hit the same thing in software: their status page lived in two spots, one fresh and one outdated, and the newcomer read the outdated one through no fault of her own. The cure is old-fashioned: pick one clock, write down where it is, and write down exactly how to read it. Arguments about the reading disappear once there's one reading to argue about.

## 🧠 NAYA NOTE

Note to future me: any time two agents disagree about a measured fact and both have citations, stop arguing the fact and diff the surfaces. Ask: "What exactly did you read — file, branch, command, instant?" Nine times out of ten it's a split-brain, not a bad measurement. When I build anything a cold Naya will read — snapshots, boards, ledgers — the boot path must name ONE canonical home and the EXACT fetch command. "It's on the repo" is not a home. And whenever I inherit a verdict I didn't measure myself, the first re-derivation question is which surface the original measurement was taken on.

## ⚙️ MACHINE NOTE

{"sn": "SN-1243", "title": "Name the Measurement Surface Before Judging the Verdict", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-13", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "MEASUREMENT-INTEGRITY"], "cousins": ["SN-969", "SN-548", "SN-1189"], "evidence": {"finding": "t0695 cold-Naya proof (Naya Narzan 4, 2026-10-13): mission snapshot existed twice - fresh on naya/mission-state, stale on main; fresh clone reads main by default, so the cold Naya's 'last verified 10:08 PDT' reading was CORRECT on the surface she used; fix named (boot entry names exactly one canonical home + fetch command, PR #2561); shared-state.json mission_snapshot_note 2026-10-13 ~17:08 PDT names the same hole ('cold-activation repair PROPOSED... new top hole')"}, "decision_change": "future boot/snapshot/board designs must name exactly one canonical home and the exact fetch command; any judge of a surprising measurement must first establish which surface it was measured on before ruling it wrong", "falsifier": "a cold Naya given one canonical home + fetch command still misreads the snapshot, or disputes persist with both parties reading the single named surface - then the naming rule is not the mechanism", "mechanism": "fresh clones read main by default; a snapshot maintained on a side branch is invisible to default reads; each surface is self-consistent so no single reader detects the split from inside it - the disagreement is a naming failure, not a measurement failure", "rule": "when a measurement surprises you, ask which surface it was measured on before calling it wrong; every cold-readable artifact names one canonical home and the exact fetch command in its boot path"}
