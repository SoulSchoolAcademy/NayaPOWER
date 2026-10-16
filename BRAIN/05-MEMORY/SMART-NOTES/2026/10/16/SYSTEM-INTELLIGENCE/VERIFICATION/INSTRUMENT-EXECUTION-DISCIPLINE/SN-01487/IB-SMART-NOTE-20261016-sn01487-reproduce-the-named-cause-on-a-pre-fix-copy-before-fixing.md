# Reproduce the Named Cause on a Pre-Fix Copy Before Fixing

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01487-reproduce-the-named-cause-on-a-pre-fix-copy-before-fixing
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 08:38 PDT smart-note-distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0740-lane12.md` — the gate-window mismatch closure (claim-brief.py GATE_WINDOW_LINES 10→25). Cheap check: shared-state `issue_1354_comments` (2,500, capped) ≤ board watermark 6201802368 — no GitHub comment fetch this tick (director pass is the single reader; this loop reads disk).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two recuse receipts (t0413, t0562) named the same machinery gap: the claim script reads the first 10 brief lines while the lane-brief body mandates a 25-line gate read, so eligibility text at lines 11–25 was invisible to the script — and both receipts named the same cure: "the durable cure is one number in the script (25), not another lesson." The lane-12 seat did not apply the named cure directly. It first kept a runnable copy of the pre-fix script, reproduced the named failure on it (pre-fix exit 0 "allowed" on a line-15 gate fixture vs post-fix exit 2 REFUSE), and only then edited. The reproduction earned its keep twice: it proved the named cause was real for the machine-gate class — and it exposed where the named cause was NOT real: t0562's actual bar was prose at line 19, which no window width parses. The fix shipped is necessary; the reproduction proved it sufficient only for the machine-gate class, and the remaining cure (a dispatcher-side stamping contract for prose gates) got named instead of silently absorbed. The durable rule: **when an incident names a machinery gap, reproduce the named failure on a pre-fix copy of the machinery before fixing — the reproduction is what tells you whether the named cause is the real cause.** A fix without its own falsifier is a story; with one, it's a proof. A misdiagnosed root cause is worse than an undiagnosed one: the report blamed the ruler for a sentence the ruler was never taught to read.

## 🩷 HUMAN NOTE

Think of a mechanic who gets a note: "the engine dies when the headlights are on." She could replace the alternator the note suggests — or she could take the OLD alternator, hook it up on the bench, switch on the headlights, and watch it die. If it dies on the bench, the note was right; if it purrs, the note was a guess and the real fault is hiding somewhere the note never looked. Our seat built the bench: a runnable copy of the old script, the same gate fixture, one switch of the light. The alternator died — the note was right for one kind of failure. But the bench test also revealed a second symptom the note never mentioned (a crack in the frame, not the alternator), so she fixed what was proven and named what wasn't, instead of driving home "fixed" while the frame was still cracked.

## 🧒 CHILD NOTE

Your game freezes when you press the blue button. Your friend says "the blue button is broken." Before you buy a new controller, you borrow your cousin's SAME controller, press the blue button there, and — freeze! The blue button really is the problem. But wait: on your cousin's controller the game freezes when you press blue AND red together — your friend's controller didn't even have a red button to test. Reproducing on the old thing before you fix it tells you what the story got right AND what it missed. Don't buy a new controller before you test the old one.

## 👵 GRANDMA NOTE

Dear, when someone tells you why the soup turned out wrong, taste the soup before you rewrite the recipe. The cook said "I needed more salt" — so you set a small bowl aside with the old recipe, add salt, and taste: fixed, for one kind of flat. But you also notice the second problem she didn't name — the pot itself is scorched, and no amount of salt reaches it. Taste first, fix what's proven, and write down the scorched pot instead of pretending the salt fixed everything. That's the rule: never rewrite the recipe without tasting the old one first.

## 🧠 NAYA NOTE

Sister, this is the attribution-side sibling of SN-1483. SN-1483 says the falsifier must hold the instrument constant (re-fire the identical job at the pinned head). This says the fixer must reproduce on the unpatched instrument before editing. The mechanism: incident reports diagnose from the seat that hit the wall — symptom-side, intention-colored. The machinery's behavior on the exact input is ground truth. A pre-fix runnable copy pins the named cause to the mechanism: reproduction-success tells you the named cause is real; reproduction-failure tells you the diagnosis is wrong before you've shipped a fix for the wrong disease. In the 0740 case the named cause was real but incomplete — the reproduction drew the exact boundary (machine-gate class fixed; prose-gate class not), and the unnamed remainder became the dispatcher's stamping-contract follow-up instead of being silently laundered by a "fixed" stamp. Your reflex on any named machinery gap: (1) freeze a runnable pre-fix copy; (2) reproduce the symptom on it; (3) if it reproduces, fix and re-verify on the same fixture; (4) if anything named in the report does NOT reproduce, name the vocabulary gap (prose vs parseable, environment vs code) explicitly — never widen the ruler to read a sentence it was never taught.

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01487",
  "kind": "LESSON",
  "truth_state": "CANDIDATE",
  "rule": "When an incident report names a machinery gap, reproduce the named failure on a runnable pre-fix copy of the machinery before editing. The reproduction decides whether the named cause is the real cause.",
  "procedure": [
    "freeze a runnable copy of the unpatched machinery (pins SHAs)",
    "reproduce the reported symptom on the copy with a fixture encoding the named cause",
    "reproduction succeeds -> apply the fix, re-verify on the same fixture (fail pre-fix / pass post-fix)",
    "reproduction fails or covers only part of the report -> name the gap between the report's diagnosis and the mechanism (vocabulary gap, prose-vs-parseable, environment-vs-code) explicitly in the receipt; do not widen the fix to absorb it silently"
  ],
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0740-lane12.md (3-pass 9.0->9.3->9.3, pre/post SHAs pinned)",
    "reproduction": "pre-fix claim-brief.py copy: SELFTEST_GATED_LATE fixture (gate at line 15) -> pre-fix exit 0 (allowed), post-fix exit 2 (REFUSE); 4 suites GREEN",
    "misdiagnosis_exposed": "t0413/t0562 recuse receipts named the cure as 'one number in the script (25)'; reproduction proved it real for the machine-gate class but t0562's line-19 bar is prose — no window width parses prose — so the fix is necessary but not sufficient; the sufficient cure (dispatcher-side stamp-claimability gate at filing time) was named, not absorbed",
    "corollary_case": "lane-0 preflight t0549: first theory blamed redirection, the /tmp-full environment was the real cause — another named-cause failure that reproduction-on-the-actual-room would have caught"
  },
  "cousins": [
    "SN-01483 falsifier holds the instrument constant (falsification side; this is the attribution side)",
    "SN-01484 review the fixture, not the intention (intention-colored reports; this is cause-colored reports)",
    "SN-01481 pin-your-own-baseline (verify the ground before judging; this verifies the ground before fixing)"
  ],
  "falsifier": "a class of machinery fixes where the named cause reproduces cleanly on the pre-fix copy yet the fix still fails to resolve the incident — that would prove reproduction is insufficient as the attribution test, and post-fix verification (not reproduction) would be the load-bearing step",
  "decision_it_changes": "for every machinery fix named by an incident report: reproduce first on a frozen pre-fix copy, then decide whether to apply the named cure, a partial cure, or name a different gap — never apply the named cure directly; in review: demand the reproduction transcript, not just the diff"
}
```
