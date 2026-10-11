# Falsification-Check Your Gates: Prove It Fails on the Broken Thing First

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0719-falsification-check-your-gates
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6068863725 (Naya 5 — DESIGN EXEMPLAR REPAIR ROUND 2 COMPLETE, 2026-10-08T20:54:13Z) — SoulSchoolAcademy

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

In Design Exemplar Repair Round 2, the real deliverable wasn't the seven fixed violations — it was `tests/test_exemplar_adjacency.py`, a mechanical gate that renders the PDF and asserts on **every page** that no two adjacent colored elements share a color (vertical flow and horizontal tile flow, every element type: bars, pills, icons, table cells) and that gray appears nowhere. What made it a gate instead of a wish was the **falsification check**: run against the pre-repair PDF it FAILS — 17 adjacent-dupes, 10 grays, including the exact violations named in Shawn's review — and only then, against the fixed render, it PASSES. The author stated the principle in one line: **eyes are now the backup, not the gate.**

Why this is brain-grade: most teams ship checks and trust the green. But a check that has never failed is a check you haven't tested — it might be asserting the wrong thing, asserting nothing (SN-0421: run-level SUCCESS with skipped behavioral jobs is vacuous), or asserting against a subject that already absorbed the repair (SN-0233: the phantom green — verifying on state that already absorbed the fix). The exemplar gate closed all three holes at once: mechanical (no human eyes in the loop), exhaustive (every page, every element type, both flow directions), and falsification-checked (proven to fail on the known-broken artifact, in the exact ways named, before it was allowed to pass anything). That last step is the admission gate for the gate itself: **a gate that cannot demonstrate its own failure is inadmissible as evidence of anything passing.**

This is distinct from its cousins. SN-0655 (corruption-proof metric extraction) is about not letting LLM text extraction silently invent numbers — falsifying the extractor. The delivery-evidence convention is about proving what shipped (hash + screenshot) — falsifying "it's done." This note is about **proving the instrument**: before a new check earns its place in a CI gate or a scorecard, run it against the broken version of the thing it guards and watch it fail in exactly the named ways. If it can't fail loudly on the broken artifact, it can't be trusted to vouch for the fixed one.

Rule for a cold successor: **every new gate ships with its own falsification receipt** — the broken artifact it was run against, the failures it named, and the pass it gave the fixed one. Eyes review the output; the gate reviews the artifact. Never reverse that order.

## 🩷 HUMAN NOTE

Shawn — the real lesson from tonight's exemplar repair wasn't the seven design fixes, it was how they made the fix stick. The new test renders every page of the report and mechanically checks that no two adjacent elements share a color and no gray sneaks in — and before it was trusted, it was run against the *broken* version, where it failed with 17 dupes and 10 grays, exactly the violations you'd named. Their line: "eyes are now the backup, not the gate." The standing rule we're recording: a new check has to prove it fails on the broken thing before its green means anything. A gate that's never failed is a gate that hasn't been tested.

## 🟣 CHILD NOTE

Imagine you build a smoke alarm, and then you celebrate that it has never gone off. That doesn't mean there's no smoke — it might mean the alarm is broken! The smart way to test an alarm is to blow real smoke at it and make sure it screams. That's what the team did with their design test: they ran it against the broken report first and confirmed it caught all 17 color mistakes and all 10 gray sneaks. Only then did they trust it to guard the fixed report. New rule: every alarm has to scream at real smoke before we believe it's working.

## 👵 GRANDMA NOTE

The team built an automatic checker to make sure the design reports always look right — no two neighboring boxes the same color, no gray anywhere. But before trusting the checker, they did something clever: they fed it the *broken* report first to prove it could actually spot the problems. It found all of them. That's the new rule: never trust an inspector who has never caught anything. Every new checker has to demonstrate it can catch the exact mistakes it's meant to prevent — only then does its green light mean something.

## 🟣 NAYA NOTE

I never accept a green from a check that hasn't earned its red. When I add a gate, I keep the broken artifact around specifically to run against it — the pre-repair PDF, the failing corpus, the red fixture — and I record what the check named when it failed. Mechanical over visual: eyes are the backup, not the gate. Exhaustive over sampled: every page, every element type, both flow directions. And falsification before admission: if the gate can't fail loudly on the thing it's meant to guard, it doesn't guard anything. A green check without a falsification receipt is decoration.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0719",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/TEST-DESIGN",
  "doctrine": "falsification-check-your-gates",
  "rule": "Every new gate ships with a falsification receipt: run it against the known-broken artifact first and confirm it fails in exactly the named ways before its PASS is admissible. Eyes are the backup, not the gate.",
  "failure_mode": "untested green — a check that never failed may assert the wrong thing, assert nothing, or assert on state that already absorbed the repair (phantom green); eyes-as-gate miss violations across 10 pages",
  "cousins": ["SN-0655", "SN-0421", "SN-0233", "SN-0442"],
  "evidence": [
    "#1354 comment 6068863725 (Naya 5, 2026-10-08T20:54:13Z) — 'Process fix (the actual lesson): tests/test_exemplar_adjacency.py — renders the PDF and mechanically asserts on EVERY page: no two adjacent colored elements share a color (vertical flow + horizontal tile flow, all element types: bars, pills, icons, table cells), no gray anywhere. Falsification-checked: FAILS on the pre-repair PDF (17 adjacent-dupes, 10 grays incl. the exact violations named), PASSES on the fixed render. Eyes are now the backup, not the gate.'",
    "Same comment — 38/38 exemplar tests (20 repair + 18 adjacency) green, 42/42 design-law green, all 10 pages visually inspected; honest scorecard 8.5/10 (claim), below the 9.0 birth threshold"
  ]
}
