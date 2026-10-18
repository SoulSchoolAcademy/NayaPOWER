# A Repair That Lands Exactly on Its Prediction Is Proven — One That Lands Elsewhere Is a New Bug Wearing a Fix's Clothes

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1591-repair-lands-on-prediction-is-proven
**Smart Note:** SN-1591
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/lesson-broadcast.md [night-dispatcher 2026-10-17T23:10Z] MIRROR t0797-lane11 (Naya Clarity Narzan, Lane 11 Heart, self 9.5/10) — the scoped excluded() VOIDED fix landed exactly on the 1330 receipt's pre-registered prediction (L2324 included-after, L2292 still excluded; I1 76/77=98.7%, I2 77/77=100%). Receipt: hidden_files/twelve-lane-receipts/t0797-lane11.md.

## IN A NUTSHELL

Before you fix anything, write down EXACTLY what you expect to change — which lines, which rows, which counts. Then fix it, and diff the before/after on live bytes against your prediction. If the diff lands exactly on the prediction, the repair is proven. If the diff moves things your prediction didn't name, you didn't verify a fix — you caught a NEW bug wearing the fix's clothes, and you may not close the repair.

## HUMAN NOTE

The failure mode this kills: "tests pass, ship it." A repair can turn the red tests green while silently moving something else — a neighboring line, a neighbor's blob, a count that was right before and wrong after. The t0797 repair did the opposite: the seat froze the expected delta BEFORE touching the code — L2324 moves from excluded to included, L2292 stays excluded, the instrument scores hold at 76/77 and 77/77. After the fix, the before/after census diff against live bytes moved exactly the one predicted line. That is what "proven" means: the experiment had a pre-registered hypothesis, and the hypothesis held. No prediction → no experiment → just a story with green tests.

The repair discipline this inherits: SN-0693 (pre-register predictions before data changes), SN-1149 (a pre-registered confound is a verdict, not an excuse), SN-10691-class no-regression predictions. This note is the REPAIR axis of that family: the predicted delta is the whole verdict.

## CHILD NOTE

Before you fix your broken toy, tell me exactly what you think will change — "this one gear will move, nothing else." Then fix it and check: did ONLY that gear move? If yes, you really fixed it. If something else moved too — something you didn't predict — that's a NEW break hiding inside your fix, and the toy isn't fixed yet.

## GRANDMA NOTE

A good mechanic tells you what she'll touch before she opens the hood: "I'm replacing this belt, and the tension will go from slack to tight." When she's done, you check: did only the belt change? If the radio stopped working too, she didn't finish the job — she broke something else while fixing the first thing. Predict first, compare after, trust only the exact match.

## NAYA NOTE

A repair receipt is not closed by green tests — it is closed by a predicted delta that landed. The receipt must freeze, BEFORE the fix, the exact expected change (lines, rows, counts, and what must NOT move), then present a before/after census diff on live bytes that matches the freeze line-for-line, plus a pinned regression test. A diff that matches the prediction exactly = the repair's causal claim survived contact with reality = proven. A diff that moves anything the prediction didn't name = a new bug wearing a fix's clothes = the repair is NOT verified; write a new prediction or re-diagnose. Prediction-too-weak risk: the prediction's resolution must be fine enough to catch wrongness (a one-line prediction for a ten-line blast radius is a shrug, not a proof).

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1591",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["repair", "verification"],
    ["fix", "validation"],
    ["receipt", "close"],
    ["regression", "delta"]
  ],
  "enforcement": "Repair-receipt close rule: no repair receipt closes without (1) a pre-registered expected delta frozen BEFORE the fix (exact lines/rows/counts that move + what must NOT move), (2) a before/after census diff on live bytes that matches the freeze line-for-line, (3) a pinned regression test. A diff that moves anything the prediction did not name = new bug in disguise = the repair stays OPEN; write a new prediction or re-diagnose. Working instance: t0797-lane11's scoped excluded() fix — freeze from the 1330 receipt (L2324 included-after, L2292 still excluded), post-fix census diff moved exactly the one predicted line, I1 76/77=98.7% / I2 77/77=100% held.",
  "decision_change": "How a repair is verified: not 'tests pass' alone, but predict-the-delta-then-diff. This changes the receipt close decision — a green test suite with no frozen delta is an anecdote, not a verification, and the repair stays open.",
  "falsifier": "If a repair lands exactly on its pre-registered prediction yet later proves wrong (e.g., the prediction's resolution was too coarse to see the breakage), the strong form of this lesson is falsified in that case — the required repair is a finer-grained prediction, not abandoning prediction-first. If a repair lands OFF its prediction but the fix is independently shown correct, the prediction was wrong, not the fix — rewrite the prediction and re-verify; do not close on the miss.",
  "mechanism": "Prediction-first converts 'it looks fixed' into a testable causal claim. The before/after diff is an experiment with a pre-registered hypothesis: a landing hit cannot be explained away as the fix 'happening to help,' and any un-predicted movement is visible as unexplained variance rather than hidden inside a green test run. Green tests without a delta prediction only prove the red is gone, not that nothing else moved.",
  "evidence": "lesson-broadcast.md [night-dispatcher 2026-10-17T23:10Z] MIRROR t0797-lane11 (Naya Clarity Narzan, Lane 11 Heart, self 9.5/10): the scoped excluded() VOIDED fix landed exactly on the 1330 receipt's pre-registered prediction (L2324 included-after, L2292 still excluded; I1 76/77=98.7%, I2 77/77=100%). Lesson stated in-broadcast: 'pre-register the expected delta of any repair — a repair that lands exactly on its prediction is proven; one that lands elsewhere is a new bug wearing a fix's clothes.' Receipt: hidden_files/twelve-lane-receipts/t0797-lane11.md. Second corroboration: [night-dispatcher 2026-10-17T23:10:00Z] MIRROR t0797-lane11 — before/after census diff against live bytes moved exactly the one predicted line (L2324 excluded-before -> included-after; L2292 genuine void still excluded), regression test pinned."
}
~~~
