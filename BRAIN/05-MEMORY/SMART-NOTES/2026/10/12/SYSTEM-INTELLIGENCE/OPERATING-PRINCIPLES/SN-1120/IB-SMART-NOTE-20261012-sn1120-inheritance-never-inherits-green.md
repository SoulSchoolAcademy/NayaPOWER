# Inheritance Never Inherits Green

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1120-inheritance-never-inherits-green
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 🧠 LEARNING EVENT 6132623609 (2026-10-12 ~21:05Z, distillation v2 — WP-8, promoted to L262, F7). Evidence: Naya Librarian wave-9 B-31 re-claim sign-in 6131898685.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Work you inherit arrives wearing someone else's green. It isn't.

Librarian's B-31 re-claim took wave-5's uncommitted scratch — previously "scored" green by a prior wave — and **scored it as a fresh build before any PR**. It found 4 real REDs: a wiring-test whose mock patched the wrong module identity and silently hit LIVE surfaces, an env-bypass hole, a second claim path around the gate, a mid-file `__main__` guard. All four are being fixed first, with the owner coordinated — before any PR exists.

The durable rule: **a prior wave's green is data, not a verdict.** Inheritance (scratch files, open branches, claimed scorecards, prior verdicts) is re-run through your own gate before it moves forward. The predecessor's evidence is input to your verification, never a substitute for it. Green does not transfer across hands.

This is the same disease as a stale certificate (Freshness Law: the `39558acc` green stays in history and does not transfer to `0b81b0c2`), applied to work ownership: a verdict is bound to the hands that produced it. When hands change, the verdict lapses. Re-verify, then claim.

The failure mode it kills: "it was green when they handed it to me" — the sentence that carries LIVE-surface mocks, env bypasses, and gate-bypassing claim paths into main. One of the four REDs silently hit live surfaces; inherited green would have shipped it.

## 🩷 HUMAN NOTE

Shawn — the re-claim lane just caught four live defects hiding inside "already green" work. Someone else's passed tests, someone else's green badge — Librarian re-ran everything as if it were brand new, and found a test silently touching live surfaces, a way around the environment guard, and a second path that skips the gate entirely.

The rule: every handoff resets the scoreboard. It doesn't matter who said it's green — your hands, your verification. Trust travels with evidence, not with momentum.

## 🟣 CHILD NOTE

If your friend says "I checked, it's safe," you still check yourself before you touch it.

## 🔵 GRANDMA NOTE

Secondhand "all clear" is not all clear. When something is handed to you, run the checks again as if nobody had — the last person might have missed the hole in the wiring.

## 🟠 NAYA NOTE

Make verdict-handoff boundaries explicit: a scorecard, test result, or "green" claim is bound to the seat, wave, and tree that produced it. Re-claims, re-anchors, and successor work score inherited artifacts as fresh builds (evidence from the predecessor is admissible as data, never as a verdict). The Freshness Law's "green does not transfer across tips" generalizes to "green does not transfer across hands."

## 🟢 MACHINE NOTE

~~~json
{
  "block_connections": ["SN-1106", "SN-1112", "SN-1113"],
  "failure_killed": "inherited green ships LIVE-surface mocks, env bypasses, and gate-bypass paths into main",
  "freshness_law_generalization": "a verdict is bound to (seat, wave, tree); any handoff lapses it",
  "handoff_protocol": {
    "predecessor_evidence": "admissible as data, never as a verdict",
    "re-claim": "score inherited artifacts as fresh builds before any PR",
    "verify": "re-run the gate under the new hands"
  },
  "learning_event": "WP-8 (promoted to L262, family F7)",
  "mechanical_check": "any PR whose content was authored by a prior wave/scratch must carry a fresh verification receipt from the re-claiming seat",
  "red_findings_precedent": "B-31 re-claim: 4 REDs (LIVE-surface mock, env-bypass, gate-bypass claim path, mid-file __main__ guard)"
}
~~~
