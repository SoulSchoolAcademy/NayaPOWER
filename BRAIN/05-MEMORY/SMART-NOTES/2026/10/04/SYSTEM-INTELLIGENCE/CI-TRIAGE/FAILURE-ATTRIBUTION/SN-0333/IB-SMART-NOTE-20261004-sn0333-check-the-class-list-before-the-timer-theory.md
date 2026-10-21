# Check the Class List Before the Timer Theory — Falsify Against the State Evidence Before You Build a Mechanism

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0333-check-the-class-list-before-the-timer-theory
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5989315746 (Naya 2, corrected diagnosis — paint not formation, 2026-10-04 23:30 PDT) / 5989083176 (Naya 4, fallback acceptance + hardening dispatch, context)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

During the v9 beat-bug investigation, the working theory was a **formation** problem: the setTimeout-based `.formed` timers were suspected of not firing, so the answer beats never got their formation class. Then Naya 2 did what nobody had done — she looked at the actual DOM: **the beats already carried `.formed`.** The timers work fine. The CSS is correct (`.beat.formed{opacity:1}`, colors correct, no `content-visibility`/`contain`/`will-change` quirks, no specificity override). The fallback hardening (force-form after the formation window) is well-built but targets the wrong layer — formation was never broken. What was actually happening: headless Chromium doesn't paint them, while the real-browser screenshot paints them fine. A compositing quirk, not a code defect.

The evidence that falsified the formation theory was in hand **all along** — the class list. It was checked only after theorizing about timers. Naya 2 owned it on the board: *"My earlier 'formation' hypothesis was wrong — owning that. The evidence (formed classes present in DOM) falsified it, and I should have checked the class list before theorizing about timers."*

Why this is brain-grade: it is a **debugging doctrine in three clauses**:

1. **Read the state before you build the mechanism.** The cheapest evidence is the observable state you already have — the class list, the attribute list, the network tab, the log. A theory that contradicts observed state is dead on arrival; theorizing first and checking later is how you ship a well-built repair for the wrong layer.
2. **Publish the correction where the original landed.** Naya 2 didn't silently revise her diagnosis in a new lane — she wrote the corrected diagnosis on the same board (#1354), naming exactly what changed ("it's paint, not formation") and what falsified the old theory. Nobody downstream builds on a stale theory they never saw retracted.
3. **Close environment-specific divergence with layered evidence, not another patch.** Formation path correct + CSS correct + fallback correct + real browser paints fine = the divergence is in the harness's compositor, not the product. Close it as environment-specific. And the carve-out: if headless verification ever becomes a hard requirement, that's a **separate investigation into Chromium's headless compositor** — never a reason to reshape the product around the test harness.

Rule for a cold successor: **when you're theorizing about why something failed, first enumerate what the evidence already shows. If the DOM says `.formed` and you're theorizing about broken timers, the theory is wrong, not the DOM.**

## 🩷 HUMAN NOTE

Shawn — a debugging lesson worth banking from the v9 beat-bug thread. The running theory was that the answer beats weren't getting their formation class — a timer problem. Turns out the beats had the class all along; the timers were fine. The real issue was headless Chrome's renderer simply not painting them, while a real browser paints them fine. Nobody looked at the DOM's class list before building the timer theory. Naya 2 caught it and owned the correction on the board: "I should have checked the class list before theorizing about timers." New standing rule: read the evidence you already have before you invent a mechanism — and when your diagnosis was wrong, publish the correction where the original was published so nobody builds on the stale version.

## 🟣 CHILD NOTE

The team was trying to figure out why the demo's pretty animation wasn't showing. Their theory was that the timer that "wakes up" the animation was broken. But when someone finally looked at the page's actual parts, the timer had worked fine all along — the test browser's *painter* was just being weird, while a real browser paints it perfectly. The lesson: before you guess *why* something is broken, look at what is actually there first — the answer might already be staring at you. And if your guess was wrong, say so out loud where everyone can hear it, so nobody else chases your wrong guess.

## 👵 GRANDMA NOTE

Honey, this one's about how we solve puzzles. The team had a theory about why something wasn't working, but nobody checked the simplest thing first — they didn't look at what the page was actually doing. When someone finally did, the answer was obvious: the part they suspected was fine all along. The lesson is one you taught me years ago: look before you leap. Check the facts you have before inventing new explanations — and when you're wrong, say so plainly so the whole family can move on together.

## 🤖 NAYA NOTE

Source: #1354 5989315746 (Naya 2, 2026-10-04 23:30 PDT — "Beat-bug: corrected diagnosis — it's paint, not formation": verified fallback-hardened build headless; ".beat.formed{opacity:1} applied, colors correct (--ink:#f8f7fb on --bg:#040405), no content-visibility/contain/will-change quirks, no specificity override. Yet headless Chromium doesn't paint them. Real-browser screenshot paints them fine"; verdict: "headless-Chromium compositing quirk, not a code defect"; recommendation: "close this as environment-specific... If headless verification ever becomes a hard requirement, that's a separate investigation into Chromium's headless compositor, not a v9 defect"; owned: "My earlier 'formation' hypothesis was wrong — owning that. The evidence (formed classes present in DOM) falsified it, and I should have checked the class list before theorizing about timers"). Context: 5989083176 (Naya 4 — verdict accepted, hardening dispatched; SN-0331's design law "enhancement, not a gate"), 5989211194 (FALLBACK-DONE — ensureAudio can-never-throw + formation safety sweep, 10/10 headless). Cousins: SN-0329 (the environment-suspect discipline that framed the whole thread — this note is its diagnostic sibling: read state before theorizing), SN-0332 (pin the working environment as control), SN-044 (name the failed layer, not just the failed run — same attribution instinct at CI level).

## ⚙️ MACHINE NOTE

{"sn": "SN-0333", "title": "Check the Class List Before the Timer Theory — Falsify Against the State Evidence Before You Build a Mechanism", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-04", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "FAILURE-ATTRIBUTION"], "cousins": ["SN-0329", "SN-0332", "SN-044"], "evidence": {"board": "#1354 5989315746 (Naya 2 corrected diagnosis: 'The beats already carry .formed in the DOM'; headless-Chromium compositing quirk; recommendation: close as environment-specific)", "mechanism": "setTimeout .formed timers fire fine -> DOM classes correct -> CSS correct -> headless Chromium doesn't paint; real browser screenshot paints; formation was never broken", "admission": "naya2: 'I should have checked the class list before theorizing about timers'"}, "rule": "read the observable state before building a mechanism theory; publish corrections where the original diagnosis landed; close environment-specific divergence with layered evidence rather than patching code for the wrong layer; never reshape the product around the test harness"}
