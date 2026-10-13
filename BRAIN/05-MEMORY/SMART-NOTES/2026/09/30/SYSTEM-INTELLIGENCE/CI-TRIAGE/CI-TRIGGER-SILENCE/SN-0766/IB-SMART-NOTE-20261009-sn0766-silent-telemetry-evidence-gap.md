# Silent Check-Run Telemetry Is an Evidence Gap, Not a Verdict — Name the Attribution

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0766-silent-telemetry-evidence-gap
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6076858491 (Naya 2 overnight verification sweep, 2026-10-09 07:52 UTC); main tip `925e4c34`; Workers Builds silent on the last 3 main commits

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The overnight verification sweep found Workers Builds silent on the last 3 main commits. Its attribution was unknown — the sweep read the silence as "removed/disabled," but flagged that reading as an inference, **not** evidence. What the sweep did with the gap is the lesson: it took no action on the silence itself (no scorecard bump, no verdict change, no merge decision), re-verified every reachable gate live via gh-api and a fetched clone, and left the attribution gap named and visible.

The discipline: **silent telemetry is a missing measurement, not a measurement of zero.** It supports neither "green" (nothing proves behavior) nor "removed" (absence of evidence is not evidence of absence). Collapse it into a conclusion and you either trust unobserved behavior or act on an unproven removal — both violate the evidence law. The correct move has three parts: (1) name the attribution as unknown in the record; (2) keep re-verifying every gate you CAN reach — the sweep confirmed workflow files still absent, ledger parity perfect, proofs unchanged, kernel `test` and spec-integrity still red with owned repairs; (3) let the gap stay visible rather than resolving it by inference. A named gap is a ticket for the next lane; a collapsed inference is a lie waiting to be found.

## 🩷 HUMAN NOTE

Shawn — small evidence discipline from the overnight sweep: one of our CI signals went quiet — no build reports on the last few commits. Nobody knows why yet. The sweep did the right thing: it didn't read the silence as "everything's fine," and it didn't declare the builds broken either. It just wrote down "attribution unknown," re-checked every gate it could reach directly, and moved on. Missing information is not information — name the gap, don't fill it with a guess.

## 🟣 CHILD NOTE

Imagine your friend stops texting. You don't know if they're busy, asleep, or their phone died. Saying "they're ignoring me" and saying "they must be fine" are both guesses. The smart thing is to say "I don't know why they're quiet," check everything you CAN check, and leave the question open instead of guessing.

## 👵 GRANDMA NOTE

Grandma, one of the team's automatic health-check signals went silent overnight. The checker didn't pretend the silence meant "all good," and didn't pretend it meant "broken" either. She simply wrote down that the reason was unknown, double-checked everything she could reach, and kept the open question visible. A guess would have felt like an answer — but it wouldn't have been one.

## 🟣 NAYA NOTE

When check-run telemetry goes silent: (1) record "attribution unknown" — do not infer green, removed, or disabled; (2) re-verify all reachable gates independently (gh-api + fetched clone, never cached reads); (3) do not move any score or merge decision on the silence; (4) surface the gap in the sweep so the owning lane can claim it. Pairs with SN-0421 (a SUCCESS with skipped jobs is vacuous) and SN-0668 (verdicts bind to a tip, not a rumor) — here the topology's absence is the thing being audited.

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0766",
  "slug": "silent-telemetry-evidence-gap",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/CI-TRIGGER-SILENCE",
  "evidence": [
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6076858491 (Naya 2, 2026-10-09T07:52:00Z)"},
    {"type": "observation", "ref": "Workers Builds silent on last 3 main commits; attribution unknown"},
    {"type": "gate_state", "ref": "reachable gates re-verified live on tip 925e4c34: workflow files absent, ledger parity perfect (171 == 165 + 6), proofs unchanged, test/spec-integrity red with owned repairs #1840/#1952"}
  ],
  "lesson": "Silent check-run telemetry is an evidence gap, not a verdict: record the attribution as unknown, re-verify every reachable gate independently, and move no score or merge on the silence. Never collapse a missing measurement into green or into removal.",
  "related": ["SN-048", "SN-0421", "SN-0668"]
}
```
