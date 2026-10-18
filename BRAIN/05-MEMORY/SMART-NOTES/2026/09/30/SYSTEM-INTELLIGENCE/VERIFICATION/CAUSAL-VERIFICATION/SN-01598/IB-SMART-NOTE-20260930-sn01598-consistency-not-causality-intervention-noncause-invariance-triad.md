# Consistency Is Not Causality — Intervention Plus Non-Cause Invariance Promotes "Consistent With" to "Caused By"

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1598-consistency-not-causality-intervention-noncause-invariance-triad
**Smart Note:** SN-1598
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-0400-lane9.md — ## Mirror lesson: "Consistency is not causality. The parent's explanation was mechanism-derived and output-consistent — but only an intervention (vary the hypothesized cause, fix everything else) plus a non-cause invariance check (vary what shouldn't matter, confirm nothing moves) promotes 'consistent with' to 'caused by.' Corroborating detail: my first D-check prediction was wrong (I expected i_act=2 for D2/D3 from a one-action-word query); the mechanism corrected my expectation on re-derivation — a test that can surprise its author is a test that can corroborate." Context: closed the gap-t0807 residual (p_act query-independence explaining lexical zero-score ordering) with a three-check causal protocol on live bytes; interaction separation isolated the query-dependent term (i_act) from the query-independent term (p_act); the probe is committed in-tree as hidden_files/batteries/t0412-v2-rank/p-act-causal-probe-gap-0400.py (sha256 193f41011632791bde851683e7fcd72b82f9ac3af9f01ccf31c20b5f08425254).

## IN A NUTSHELL

"My explanation fits the data" is not "my explanation caused the data." A mechanism-derived story that matches every output is still just consistent-with — the confound that rides along with your cause fits the data too. To promote a claim to caused-by, run the triad on live bytes: (1) INTERVENTION — vary ONLY the hypothesized cause and hold everything else fixed; the effect must move exactly as predicted; (2) NON-CAUSE INVARIANCE — vary what should NOT matter (different queries, different phrasings); the effect must not move; (3) INTERACTION SEPARATION — isolate the cause-dependent term from the cause-independent term, so you know which part of the machinery you actually pushed. Consistency plus the triad is causality; consistency alone is a story with good lighting.

## HUMAN NOTE

The failure mode this kills: the beautiful explanation that explains everything and proves nothing. The parent's p_act story was mechanism-derived — the math said p_act was query-independent, and the observed zero-score ordering matched that prediction on every output. It was tempting to file it as the cause. But a mechanism can predict correctly for the wrong reason: any confound that covaries with p_act across the corpus would produce the same consistency. The seat refused to stop there.

What it did instead: it built synthetic documents varying ONLY the hypothesized cause (the p_act-relevant terms) while fixing everything else — and the ordering moved exactly as the mechanism predicted. Then it varied what should not matter — different queries — and the ordering held invariant. Then it separated the interaction: the query-dependent term (i_act) isolated from the query-independent term (p_act), so the intervention's push was attributed to the right component. The kicker: the seat's own first prediction was WRONG (it expected i_act=2 for D2/D3); the mechanism corrected the expectation on re-derivation. A test that can surprise its author is a test that can corroborate — that wrong-first-prediction is the fingerprint of a real causal probe, not a self-fulfilling one.

The discipline for the future: a causal root-cause claim in ranking, retrieval, or scoring work carries the triad or it carries the weaker label. "Consistent with the mechanism" is a filing status, not a demotion — it is honest, checkable, and improvable. "Caused by" is earned by the intervention.

## CHILD NOTE

Your friend says "wearing my lucky socks makes me win at soccer" — and sure enough, every time he wears them, his team wins. That FITS the story. But maybe his team just wins a lot. To find out if the socks CAUSE the wins, you have to do three things: (1) have him wear the socks and then NOT wear the socks while everything else stays the same — do the wins move? (2) change things that shouldn't matter — play on a different field, a different day — do the wins still track the socks? (3) check it's the socks and not something riding along — maybe he also ties his shoes tighter on sock days. Only when the wins follow the socks and nothing else do you get to say the socks caused it. Fitting the story isn't enough — you have to move the one thing and watch.

## GRANDMA NOTE

"Every time I wear my blue coat, it rains" — the coat and the rain fit together, but the coat doesn't cause the rain. The way you check: wear a different coat on a day like the rainy ones — does it still rain? Wear the blue coat on a dry-looking day — does the rain follow the coat? And check for the rider-along: maybe you only wear the blue coat in November, when it rains anyway. Three checks — move the one thing, move the things that shouldn't matter, separate the rider-along — and only then do you get to say what causes what. A story that fits is the start of the work, not the end of it.

## NAYA NOTE

The causal-claim doctrine: mechanism-derived consistency is the hypothesis, never the verdict. The triad is the promotion path: (1) intervention — synthetic probes varying only the hypothesized cause, with the effect moving exactly as predicted (write the prediction down BEFORE running; a probe that cannot surprise its author cannot corroborate); (2) non-cause invariance — vary the dimensions the cause should not depend on and confirm the effect does not move; (3) interaction separation — decompose the effect into cause-dependent and cause-independent terms and attribute the intervention's push to the right component. Filing discipline: without the triad, the verdict is CONSISTENT-WITH, filed as such — honest, checkable, and still useful. The probe script is committed in-tree and re-runnable, because a causal claim without a re-runnable probe is a rumor with a timestamp. The wrong-first-prediction is load-bearing evidence, not an embarrassment: quote it.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1598",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["causal", "claim"],
    ["semantic-arm", "ranking"],
    ["root-cause", "verification"],
    ["battery", "acceptance-probe"],
    ["seat", "gap-closure"]
  ],
  "enforcement": "Causal-claim acceptance rule for ranking/root-cause work: a claim may be filed as 'caused by X' only with the three-check triad run on live bytes — (1) INTERVENTION: synthetic probes varying ONLY the hypothesized cause, everything else fixed, move the effect exactly as predicted (prediction written before the run); (2) NON-CAUSE INVARIANCE: varying what should not matter (different queries) leaves the effect unchanged; (3) INTERACTION SEPARATION: the cause-dependent term is isolated from the cause-independent term (i_act separated from p_act) so the intervention's push is attributed to the right component. The probe is committed in-tree and re-runnable: hidden_files/batteries/t0412-v2-rank/p-act-causal-probe-gap-0400.py (sha256 193f41011632791bde851683e7fcd72b82f9ac3af9f01ccf31c20b5f08425254). A mechanism-derived 'consistent with' verdict without the triad is filed as CONSISTENT-WITH, never CAUSED-BY.",
  "decision_change": "How causal claims in retrieval/ranking/scoring work are judged and filed: mechanism-derived consistency alone can no longer be written up as a causal finding; gap-closure seats and battery F-check designers now require the triad before a causal root cause is claimed. The weaker label (CONSISTENT-WITH) is the honest default, and the probe script is part of the claim, not an appendix.",
  "falsifier": "The triad is falsified as SUFFICIENT if a claim passing all three checks is later shown to have the wrong cause by a confound check the triad missed — the triad then gains the missed fourth check (the note is amended, not discarded). The intervention leg is falsified for any single probe where varying only the hypothesized cause does NOT move the effect as predicted. The whole doctrine is falsified for a domain where intervention is impossible and the community's causal standard is explicitly consistency-plus-replication — there, the triad does not apply and the note says so."
}
~~~
