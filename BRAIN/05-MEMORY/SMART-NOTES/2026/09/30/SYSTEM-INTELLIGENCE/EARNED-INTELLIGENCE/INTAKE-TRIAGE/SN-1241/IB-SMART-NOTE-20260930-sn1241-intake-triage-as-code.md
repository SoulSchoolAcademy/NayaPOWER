# Valuable Intelligence Is Code, Not Judgment

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1241-intake-triage-as-code
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2537 comment 6157410322 ([NAYA 5], 2026-10-13 ~16:31 PDT) — intake triage IMPLEMENTED per Shawn's directive "become masters at capturing/ingesting intelligence and identifying what's valuable." PR #2552 (`naya5/intake-triage-20261013`): new `tools/intake_triage.py`, Cycle 1 (Triple-Cycle Law) 8.0 → 8.5. Needs different-seat review (Learn lane / Alpha natural).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

"Valuable intelligence" is now code. `tools/intake_triage.py` scores every capture candidate on four dimensions — novelty (coverage), durability, actionability, reach — and returns a verdict: **PROMOTE / LOG / DROP**. The 12-case battery is the executable contract for what "valuable" means, not each agent's momentary judgment. Cycle 1 scored 8.0 → 8.5 under the Triple-Cycle Law; the function is pure (no side effects); cycles 2–3 are queued (capture-path wiring, live validation).

Why this is brain-grade: the mastery move in Shawn's 2026-10-13 directive is *identifying* what's valuable, not just capturing. Momentary judgment is un-auditable — two seats, same candidate, different verdicts, no way to tell which was right. A pure function with a battery contract makes the definition of "valuable" checkable, reproducible, and improvable. The four dimensions are the mechanism: novelty-without-durability is news, durability-without-actionability is trivia, actionability-without-reach is local lore. The verdict needs all four.

## 🩷 HUMAN NOTE

Shawn — you said become masters at identifying what's valuable, not just capturing. Naya 5 turned the judgment into code: every candidate gets scored on four things — is it new (and does it cover a gap), will it still matter months from now, can someone act on it, and how far does it reach — then PROMOTE, LOG, or DROP. The 12-case test battery is the contract, so "valuable" isn't vibes anymore, it's checkable. First cycle: 8.0 to 8.5. Pure function, no side effects, so it can't break anything by running. Next: wire it into the capture path and validate it live.

## 🟣 CHILD NOTE

Imagine you get a hundred letters a day and have to decide which ones matter. If you just guess, some days you're tired and throw away the important one. So you make a checklist: is this letter new? Will it matter next month? Can I do something with it? Does it help more than just me? Score each one, keep the high scores, file the mediums, toss the rest. Now the checklist decides — not your mood. That's what the triage tool does for everything the team captures.

## 👵 GRANDMA NOTE

The team used to decide what was worth keeping the way people decide what mail to open — by feel, in the moment. The problem with feel is that it changes with the weather. So they wrote the feel down as a recipe: newness, lasting power, usefulness, reach — four ingredients, one score, three possible verdicts. A recipe can be tested, argued with, and improved. A feeling can't. "Valuable" stopped being a mood and became a measurement.

## 🧠 NAYA NOTE

Note to future me: when triaging captures — including in this very distillation loop — score the candidate on the four dimensions before trusting the gut: novelty (does it cover a gap in what we already hold?), durability (does a cold me months from now need this?), actionability (does it change a decision?), reach (how many seats/decisions does it touch?). PROMOTE only what clears all four; LOG the maybes; DROP the rest without guilt — noise is worse than silence. If the triage function's verdict and my gut disagree, the disagreement is data: check the battery, and if the battery is wrong, fix the battery, not the verdict. Never hand-tune a single verdict past the function — that's the old judgment wearing a new mask.

## ⚙️ MACHINE NOTE

{"sn": "SN-1241", "title": "Valuable Intelligence Is Code, Not Judgment", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-13", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "EARNED-INTELLIGENCE", "INTAKE-TRIAGE"], "cousins": ["SN-1240"], "evidence": {"finding": "#2537 comment 6157410322 ([NAYA 5], 2026-10-13 ~16:31 PDT): intake triage IMPLEMENTED per Shawn's 2026-10-13 directive; new tools/intake_triage.py scores every capture candidate on novelty (coverage), durability, actionability, reach - verdicts PROMOTE / LOG / DROP; 'Valuable intelligence is now code with a 12-case battery as the contract, not each agent's momentary judgment'; Cycle 1 (Triple-Cycle Law) 8.0 -> 8.5; pure function, no side effects; cycles 2-3 queued (capture-path wiring, live validation); different-seat review needed (Learn lane / Alpha natural); PR #2552 naya5/intake-triage-20261013"}, "decision_change": "capture/distillation triage routes through the triage function's PROMOTE/LOG/DROP verdicts instead of each agent's momentary judgment; when function and gut disagree, fix the battery, never hand-tune a single verdict", "falsifier": "the 12-case battery's verdicts don't predict downstream measured value - promoted notes prove inert while dropped ones prove valuable on re-admission - then the four scoring dimensions (or their weights) are wrong", "mechanism": "structured scoring on novelty/coverage, durability, actionability, reach replaces subjective momentary judgment with an auditable pure function; the 12-case battery is the executable contract, so the definition of 'valuable' is checkable, reproducible, and improvable rather than vibes", "rule": "valuable intelligence is code with a battery contract, not each agent's momentary judgment; score novelty, durability, actionability, reach - PROMOTE what clears all four, LOG the maybes, DROP the rest"}
