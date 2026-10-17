# Match Structure, Never Substrings, for Kind Classification

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1576-match-structure-never-substrings
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** t0707-lane11 lane receipt (Naya Heart, Lane 11, human-value observatory), hidden_files/twelve-lane-receipts/t0707-lane11.md (2026-10-17) — first census pass misclassified a sign-in as a sign-out because the body contained the prose phrase "no sign-out"; fixed by anchoring header patterns structurally

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The t0707-lane11 census parser classified feed posts as sign-ins or sign-outs. The first pass matched on the substring "sign-out" — and misclassified a sign-in whose body contained the prose phrase "no sign-out." Fixed by anchoring the patterns structurally to the header families instead of scanning the whole body. Principle: match structure, never substrings, for kind classification. Prose can mention a kind without instantiating it; a keyword's presence is not the event.

Why this is brain-grade: the failure mode is generic to every classifier built on keyword presence — mentions, negations, and meta-talk about a kind all contain the keyword while not being the kind. The error is silent (no exception, just wrong census numbers feeding the observatory instruments) and it scales: 529 sign events across 6 header families, one prose phrase per hundred events, each one a quiet misclassification. Structural anchors constrain the match to the syntactic position where the classification is actually true.

## 🩷 HUMAN NOTE

Shawn — a classifier rule from the human-value observatory work. We built a parser that reads feed posts and counts sign-ins vs. sign-outs. The first version just looked for the word "sign-out" anywhere in the post — and it counted a sign-in as a sign-out, because the sign-in's body happened to contain the phrase "no sign-out." The fix: don't match words anywhere — match the header, the structural part of the post that says what the post is. The standing rule: when you're classifying things, anchor your pattern to the structure that defines the kind, never to a substring floating anywhere in the text. Words get mentioned; structure is where things happen.

## 🟣 CHILD NOTE

Imagine sorting mail into "birthday cards" and "bills" by checking if the envelope says "birthday" anywhere. Then a bill arrives and the envelope says "NOT a birthday card" — your sorter puts it with the birthday cards, because it saw the word. That's what happened here. The fix: don't read the whole letter. Look at the stamp in the corner that says what the envelope is — that's the structure — and sort by that. Words inside can lie about what the thing is; the structure can't.

## 👵 GRANDMA NOTE

Like sorting recipe cards by whether the word "cake" appears. A card that says "this is NOT a cake recipe — it's a soup" goes into the cake pile, because the word is there. Of course it does — you sorted by the word, not the thing. The fix is the recipe card's header — the title line where the kind of recipe is declared. You read the title, you sort by the title. What matters is the label in the place where labels go, not a passing mention in the middle of the text.

## 🧠 NAYA NOTE

Cold successor: (1) When you write a classifier that distinguishes kinds of documents, anchor every kind-pattern to the structural position where the kind is declared (headers, family patterns, pinned positions) — never substring-match keywords across the whole body. (2) The concrete instance: the i2-census parser's first pass matched "sign-out" as a substring and misclassified a sign-in whose body contained the prose "no sign-out"; the fix anchored to the six header families (4-line era, tick+Lane, legacy, sign-in/out blocks). (3) Every classifier ships with prose-mention negatives in its regression corpus — inputs that contain the keyword in prose ("no sign-out") and must NOT classify; a classifier change is rejected if the negatives reclassify. (4) The error is silent and scales with corpus size: no exception, just wrong numbers downstream (here, observatory instruments I1/I2 computed on misclassified events). Prefer a no-match over a keyword-match — abstain is honest, keyword-hit is a guess.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1576",
  "title": "Match Structure, Never Substrings, for Kind Classification",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-17",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "VERIFICATION", "INSTRUMENT-DISCIPLINE"],
  "cousins": [],
  "applies_when": ["parse", "measurement", "classification"],
  "enforcement": "classifier regression corpus with prose-mention negatives: every kind-classifier carries negative test cases where the keyword appears in prose and must NOT classify (concrete seed: the t0707 i2-census parser's 'no sign-out' case); a classifier change is rejected if the negatives reclassify. Anchor kind-patterns to structural header positions, never body-wide substrings.",
  "evidence": {
    "event": "t0707-lane11 lane receipt MISS (hidden_files/twelve-lane-receipts/t0707-lane11.md, 2026-10-17): first census pass misclassified a sign-in as a sign-out on substring 'sign-out' matching the prose phrase 'no sign-out'; fixed by anchoring to structural header patterns across six families",
    "decision_change": "future classifiers anchor kind-patterns to structural positions and ship prose-mention negatives in the regression corpus",
    "falsifier": "a labeled corpus where body-wide substring matching beats structural anchoring on precision and recall for kind classification",
    "mechanism": "prose can mention a kind without instantiating it (negations, meta-talk); keyword presence does not imply the event, while structural anchors constrain the match to where the classification is actually true"
  }
}
```
