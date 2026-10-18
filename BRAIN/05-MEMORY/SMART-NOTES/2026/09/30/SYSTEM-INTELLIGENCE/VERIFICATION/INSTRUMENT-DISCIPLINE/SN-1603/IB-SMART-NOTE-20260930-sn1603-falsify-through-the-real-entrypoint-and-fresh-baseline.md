# Falsify Through the Real Entrypoint and Re-read the Live Baseline — Anything Else Is a Receipt About Yesterday's World

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1603-falsify-through-the-real-entrypoint-and-fresh-baseline
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-0424-lane6.md (Naya Clarity Narzan, Lane 6 Heir hat — Mirror lesson), reported as CANDIDATE 591 in hidden_files/learning-events-2026-10-18-22.md (2026-10-17 22:20 PDT hour). No formal note filed — SN-1594 through SN-1599 formalized candidates 587–590 and the stale-brief premise; 591 remained unfiled.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A falsifier proved its predicates through a monkeypatched harness but never walked through the door the real system walks through — the instrument's actual `__main__`/entrypoint — and it read the baseline from a saved snapshot instead of re-reading live bytes at run start. Within 24 hours the live baseline drifted, proving the second seam too. The verdict: a falsification receipt built on a monkeypatch plus a snapshot is a receipt about yesterday's world. Future falsification runs must (1) enter through the instrument's real entrypoint, and (2) re-read the live baseline at run start. Anything else claims a proof the run never earned.

Why this is brain-grade: SN-1589 already requires a falsifier to *name* its seams (monkeypatch vs subprocess fidelity declared in writing). This note is the stronger action on top: don't just name the seam — close it. The named seam from SN-1589's era predicted exactly this miss, and the miss happened: entrypoint-level logic can change under a monkeypatched harness, and baselines drift under a snapshot. Naming was the honest half; walking the real path on fresh bytes is the whole proof. A cold successor designing a falsifier a year from now reads this first and builds the harness right.

## 🩷 HUMAN NOTE

Shawn — one from the verification work tonight. We had a test that proved the logic right by plugging directly into the code's internals — but it never ran the tool the way the tool actually gets run, and it checked yesterday's saved data instead of today's live data. The live data moved within a day. So the test's "proof" was about a world that no longer existed. The new rule: when we build a test to prove something works, the test has to walk through the real front door and read the real current numbers — no side entrances, no old copies. A test that runs the real thing on the real data is one you can bank.

## 🟣 CHILD NOTE

Imagine you wanted to prove a recipe works, but instead of cooking in the real kitchen, you just read the recipe out loud and taste yesterday's leftovers. That's what happened: the test never used the real kitchen (the actual program's front door) and never tasted today's food (today's real data). Of course it said everything was fine — it tested the wrong thing! The rule is simple: cook in the real kitchen, taste today's food. Test the real thing, with the real numbers, right now.

## 👵 GRANDMA NOTE

Dear, there's an old carpenter's habit: measure the board you're actually cutting, not the one you measured yesterday. Tonight someone learned why the hard way — a test proved its point by looking at a shortcut copy of the program and a day-old copy of the data, and the world had already moved on. The honest fix isn't to apologize; it's to change the habit: run the real program through its real front door, and always measure the live world fresh. A proof that skips the front door is a promise made to yesterday.

## 🧠 NAYA NOTE

This extends SN-1589 (name your seams) into action: when designing or scoring a falsification run, require two load-bearing facts in the receipt: (1) the entrypoint the run actually entered through — the instrument's real `__main__`/invocation path, not a monkeypatched module harness; a monkeypatch-only proof that skips the door the system walks through is non-evidentiary for entrypoint-level behavior; (2) the baseline the run read — re-read from live bytes at run start with the read timestamp logged; a run that rode a saved snapshot is a receipt about yesterday's world, and the lane-6 case proved a baseline can drift within 24 hours. The scorer's Mirror section asks both questions; either answer missing or wrong → the falsification verdict is scored non-evidentiary and the receipt says so plainly. Cousin of SN-1592 (absence-falsifiers need positive controls): the same "the instrument is only as honest as its falsifier" family, now with the entrypoint + freshness legs.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1603",
  "applies_when": [["falsification", "receipt"], ["instrument", "verification"], ["verify", "baseline"]],
  "enforcement": "gap-lane scorer receipt Mirror section must confirm (1) the run entered through the instrument's real __main__/entrypoint, and (2) the live baseline was re-read at run start with the read timestamp logged. A falsification receipt that rode a monkeypatch-only harness or a saved snapshot is scored non-evidentiary — the re-score checklist treats 'which door did the run walk through, and what did the baseline say at run start?' as the falsification-entry check.",
  "falsifier": "Run the same falsification twice — once through a monkeypatch harness + saved snapshot, once through the real entrypoint + fresh live baseline. If the verdicts never differ across many trials AND live baselines never drift within the run's decision window, the rigor buys nothing and this lesson is wrong.",
  "mechanism": "Entrypoint-level wiring (top-level code, real invocation path) can change under a monkeypatched module harness, and live baselines drift under saved snapshots — both seams are real, the second one proved within 24 hours. Testing the real path on fresh bytes removes both.",
  "decision_change": "When designing any falsification run, enter through the instrument's real __main__/entrypoint and re-read the live baseline at run start (timestamp logged) — never a monkeypatch-only proof on a saved snapshot.",
  "related": ["SN-1589", "SN-1592"],
  "provenance": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-0424-lane6.md (Mirror lesson); hidden_files/learning-events-2026-10-18-22.md (CANDIDATE 591)"
}
```
