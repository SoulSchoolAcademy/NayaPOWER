Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When a lane adapts a battery instrument into a reference runner, the runner must be an asserted 2-anchor adaptation of the battery's own instrument — never hand-rolled. t1302 proved why: Lane 3's fresh reference runner reproduced the t1290 battery's published numbers exactly (tfidf 0.500 / lexical 0.000 / MRR gap +0.500, determinism byte-identical across two fresh-process runs), which is what made the clause-tfidf-maxpool CONFIRMED verdict (rank1 1.000 vs P1 bar 0.60) trustworthy rather than suspicious — a 1.0 that reproduces is evidence, a 1.0 that doesn't is a story. And the first build attempt proved the cost of hand-rolling: its HERE-anchor miss was caught only because the immediate byte-exact run exposed it. The instrument encodes its own semantics; a runner built from scratch can silently anchor differently and agree on the original battery by luck. The verdict also carries its honest bound: it covers this battery's operating range (exclusive lexical signal, df=1 rescue stems), not retrieval in general — the next battery must test decoys sharing rare terms.

## 🩷 HUMAN NOTE

Shawn — when a lane wants to double-check another lane's experiment, the checker has to rebuild the experiment's measuring tool from the experiment's own parts — never by hand from scratch. Here's why it matters: Lane 3's checker reproduced the original numbers exactly, down to the byte, across two fresh runs. That's what makes the 100% result believable instead of suspicious. And the first hand-built attempt got a detail wrong that only the exact reproduction caught. Rule: copy the instrument's own anchors, never improvise. And every verdict says what it actually covers — this one covers this battery, not all of retrieval. The next test has to try the hard case the first one didn't.

## 🟣 CHILD NOTE

Imagine two kids playing a game where one keeps score. The other kid wants to check the score — but they can't just make up their own scoring rules and claim it's a check. They have to use the SAME score sheet, line by line. If they build their own score sheet, they might count something differently without meaning to — like the first try, where one line was counted wrong and nobody noticed until the exact copy was compared. And the checker also has to say honestly: "this check only covers the levels we played, not every level in the game."

## 🔵 GRANDMA NOTE

It's like double-checking a recipe. You don't re-measure the ingredients with your own cup and say the recipe is right — you use the same measuring cups the cook used. If you use your own cup, you might get the same cake by luck and think everything's fine. The first checker here used their own cup and got one ingredient wrong — the exact copy caught it. And when you report, you say exactly what you tasted: this cake, not all cakes ever.

## 🟠 NAYA NOTE

Verification discipline, Naya to Naya: the reference-runner rule is now the t1302 receipt. The receipt (Lane 3 Judge, 9.5/10, COMPLETE) carried the full seal chain — frozen v3 battery, two fresh-process runs byte-identical (determinism PASS), sealed-prediction comparison direction + bar both confirmed, falsified arm untouched (sha re-verified) — and the GREEN verdict on clause-tfidf-maxpool earned its trust from the asserted 2-anchor adaptation: the runner was built as an adaptation OF the battery's own instrument, anchored twice, and it reproduced the published numbers exactly before any adaptation verdict was read. Two discipline points ride on this: (1) reproduction first, verdict second — a rank1 1.000 means nothing until the runner reproduces the battery's own numbers exactly; (2) never hand-roll: the first build's HERE-anchor miss (caught by the immediate run) is the concrete cost of improvising anchors — the instrument's semantics live in its anchors, and a scratch-built runner can agree on the original battery by luck while misjudging every adaptation. The receipt also sets the honest-bound pattern: the verdict covers THIS battery's operating range (exclusive lexical signal, df=1 rescue stems); the named next test is decoys sharing rare terms, assigned to the next battery — not left as a hope.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1836-reference-runners-asserted-adaptations-not-hand-rolled",
  "lesson": "A reference runner that re-checks a battery instrument must be an asserted 2-anchor adaptation of the battery's own instrument, never hand-rolled: the runner must reproduce the battery's published numbers exactly (determinism byte-identical) before any adaptation verdict is read, because a hand-rolled runner can silently anchor differently and agree on the original battery by luck. The verdict carries its honest bound — it covers the battery's operating range, and the next battery is assigned the adversarial case the current one didn't test.",
  "applies_when": ["verification", "instrument", "reference-runner"],
  "enforcement": "The SURGE retrieval brief template requires reference runners to be asserted 2-anchor adaptations of the battery's own instrument: the runner reproduces the battery's published numbers exactly on fresh-process runs (determinism byte-identical) before the adaptation verdict is read; a runner that cannot reproduce is refused, not tuned. Each verdict states its operating-range bound in the receipt and names the adversarial case (e.g. decoys sharing rare terms) assigned to the next battery — the bound is the receipt's, not the prose's.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t1290-lane3.md (Lane 3 Judge, 9.5/10, COMPLETE 2026-10-22T16:44Z: clause-tfidf-maxpool CONFIRMED — rank1 1.000 vs P1 bar 0.60; fresh reference runner reproduced the battery's published numbers exactly: tfidf 0.500 / lexical 0.000 / MRR gap +0.500; 17/24 labels moved up vs the falsified t1284 arm, 0 down; sealed-prediction comparison direction + bar both confirmed; falsified arm untouched sha c21d621a re-verified)",
    "hidden_files/lesson-broadcast.md [night-dispatcher t1302, 2026-10-22T16:44Z: mirror lesson — the bar was re-derived from live bytes in-step instead of inherited; build reference runners as asserted 2-anchor adaptations of the battery's own instrument, never hand-rolled (the first build's HERE-anchor miss was caught by the immediate run); honest bound carried: verdict covers THIS battery's operating range (exclusive lexical signal, df=1 rescue stems), not retrieval in general — next battery should test decoys sharing rare terms]"
  ],
  "decision_change": "Every future battery-adaptation check builds its reference runner as an asserted 2-anchor adaptation of the battery's own instrument, reproduces the published numbers exactly first, and only then reads the adaptation verdict. A hand-rolled runner is refused as evidence. Every verdict receipt states its operating-range bound and assigns the untested adversarial case to the next battery.",
  "falsifiability": "If a hand-rolled runner reproduces a battery's published numbers exactly on fresh data AND holds up on adversarial decoys sharing rare terms, the never-hand-roll rule is over-strict and the note is wrong. If a runner agrees on the original battery but disagrees after re-anchoring to the battery's own anchors, the note is confirmed.",
  "mechanism": "The battery's instrument encodes its own semantics in its anchors; a scratch-built runner re-implements those semantics from memory, and anchor drift (like the HERE-anchor miss) is silent — it changes what the runner measures while the numbers can still agree on the original battery by coincidence. Asserted 2-anchor adaptation keeps the semantics pinned to the instrument's own definitions, so the reproduction is a byte-exact check of the same thing, not a new instrument that happens to agree."
}
```
