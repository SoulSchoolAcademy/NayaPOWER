# Scope the Fail-Closed Assertion to the Claim — and Know Which Way the Instrument Biases

**Intelligent Block:** IB-SMART-NOTE-20261013-sn01221-scope-fail-closed-assertion-to-claim-know-bias-direction
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE HEART] Naya Heart (Lane 11) tick t0660 sign-out, #2175 comment 6153897694 (2026-10-13 ~20:13Z); receipt `hidden_files/twelve-lane-receipts/t0660-lane11.md`; verdict `retrieval/cold-retrieve-isolated-t0660.md`; live tip `582e5e5f`. Related: SN-1030 (never score a void), SN-1058 (bound + presence, not equality), SN-1036 (creation warms the measurement).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two instrumentation rules from one honest incident in the t0660 cold-retrieve drill.

**Rule 1 — scope the assertion to the claim.** The instrument's fail-closed exit-3 fired on the first cold trial: 10 stdlib files were pinned mapped by *other VM processes*, so page eviction was impossible and the pre-trial `mincore` 0-residency assert tripped. The assertion was scoped wider than the claim: the trial claimed to measure 605 tree files on a disk-backed tree; the assertion demanded whole-VM residency silence, including processes the trial never claimed to control. A fail-closed guard scoped wider than its claim is a noise detector, not a guard — it voids the trial on background noise it never promised to exclude. The seat disclosed the void honestly, narrowed the assertion to tree scope, and both scored trials re-ran clean. The fix generalizes: every pre-assertion in a fail-closed instrument must name exactly the domain the trial claims (its files, its processes, its universe) — one inch wider and the instrument measures the weather instead of the claim.

**Rule 2 — know which way the instrument biases.** The same incident carried the second half: "Violation biases *toward* PASS, so the FAIL is the conservative direction." Imperfect eviction can only make a cold trial *faster* (a resident page is a hit you didn't deserve), never slower — so any residual-violation error pushes the verdict toward PASS. The observed verdict was FAIL (cold median 0.9682s vs the 0.5s bar). A verdict that runs *against* the instrument's bias is evidence: the FAIL survived an error mode that could only have helped it pass. The inverse is the discipline: a verdict that rides *with* the instrument's bias (a PASS from a leaky-cold rig) is a hypothesis, not a result — it needs a second, bias-fighting control before anyone believes it. The seat did not claim the isolation was perfect; she claimed the direction of the imperfection, and the FAIL outran it.

The pre-reg discipline for a cold successor: every fail-closed instrument declares (a) its assertion's domain, exactly co-extensive with the claim; (b) the direction its violations bias (toward PASS or toward NO-GO/FAIL); and (c) which verdict would have to fight the bias to be believed.

## 🩷 HUMAN NOTE

Shawn — two instrument-building lessons from tonight's cold drill, one incident, both banked. First: the fail-closed guard fired on the wrong thing — it checked the whole machine's memory was empty instead of just the files being measured, and other programs on the machine tripped it. A guard that watches more than it claims to watch is a noise detector, not a guard. The lane narrowed the check to the measured files and both clean trials ran. Second, and this is the one that generalizes: she knew which way her instrument's imperfections lean. Any leftover warmth can only make the run faster — so when the run still fails, the failure is real; the error was trying to help and it wasn't enough. A pass in the same situation would be the opposite: the error was pushing toward pass, so a pass proves nothing. The rule we're banking: name your instrument's lean, and only trust a verdict that had to fight it.

## 🟣 CHILD NOTE

Imagine a teacher checking that everyone closed their books before a test. She walks the whole school and finds an open book in the *library* — in a different class! — and cancels your test. That's the wrong check: she was supposed to check YOUR classroom, not the whole school. A rule that watches more than it claims to watch punishes people for things that aren't their test. Then the second trick: she knows that if anyone DID cheat, their score would be HIGHER. So if a student still scores low, the low score is honest — cheating would only have helped. But a HIGH score from that classroom proves nothing, because cheating pushes scores up. The smart teacher writes down both things before the test: exactly what she'll check, and which way cheating leans.

## 👵 GRANDMA NOTE

It's like a smoke alarm wired to the whole apartment building when you only cook in your kitchen — the neighbor's toast sets off your alarm and ruins your dinner party. A good alarm watches exactly the room it claims to protect, no more. And there's a second piece of wisdom: know which way your measuring cup leans. If your cup always measures a little *short*, then a recipe that still tastes too salty with a short cup is definitely too salty — the error was trying to hide it and couldn't. But if the recipe tastes just right with that same short cup, you haven't learned anything — the error was on salt's side. Declare the lean, and only believe the verdict that had to fight it.

## 💜 NAYA NOTE

Note to future me: TWO INSTRUMENT RULES, ONE INCIDENT. (1) SCOPE: a fail-closed assertion must be co-extensive with the claim — its files, its processes, its universe. The t0660 exit-3 void came from asserting whole-VM residency for a claim about 605 tree files; 10 stdlib files pinned by foreign processes made the void inevitable, not informative. Before sealing any instrument, read every pre-assertion and ask: "is this domain one inch wider than the claim?" If yes, narrow it or the instrument measures weather. (2) BIAS: declare the direction violations bias (toward PASS or toward FAIL), in the pre-reg, before the trial. A verdict against the bias is evidence — the t0660 FAIL (0.9682s vs 0.5s bar) outran a bias that could only have sped it up. A verdict with the bias is a hypothesis — a PASS from a leaky-cold rig must be re-proven with a bias-fighting control. Distinct from SN-1030 (discard the voided run — this note is about preventing the void) and SN-1058 (equality-vs-bound assertions — this note is about assertion *domain*, not assertion *shape*).

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1221",
  "lesson": "scope-fail-closed-assertion-to-claim-know-bias-direction",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "ASSERTION-DISCIPLINE"],
  "extends": [],
  "related": ["SN-1030", "SN-1058", "SN-1036"],
  "evidence": {
    "sign_out": "#2175 comment 6153897694 (Naya Heart t0660, 2026-10-13): first cold trial VOIDED by the instrument's own fail-closed exit 3 — 10 stdlib files pinned mapped by other VM processes (eviction impossible); assertion scoped wider than the claim; fixed to tree-scope, both scored trials re-ran clean",
    "bias": "same comment: 'Violation biases toward PASS, so the FAIL is the conservative direction.' Cold median 0.9682s (n_cold=2) vs CR-ACCEPT 0.5s bar; warm 0.32–0.35s; mincore 0-pre proven on 605 tree files both cold trials; exact SN-016 hits 5/5",
    "receipt": "hidden_files/twelve-lane-receipts/t0660-lane11.md; verdict retrieval/cold-retrieve-isolated-t0660.md"
  },
  "rule": "Scope every fail-closed assertion to exactly the claim's domain — one inch wider turns the guard into a noise detector. Declare the instrument's bias direction in the pre-reg: trust verdicts that run against the bias (evidence), re-prove verdicts that ride it (hypothesis)."
}
```
