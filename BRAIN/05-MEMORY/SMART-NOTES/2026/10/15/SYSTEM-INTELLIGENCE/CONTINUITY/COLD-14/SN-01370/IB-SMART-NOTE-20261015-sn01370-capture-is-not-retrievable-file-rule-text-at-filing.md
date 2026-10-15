# Capture ≠ Retrievable: File the Rule TEXT at Filing Time, Not Just the Lesson Number

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01370-capture-is-not-retrievable-file-rule-text-at-filing
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 01:38 PDT distillation tick (2026-10-15) from #2537 comment 6187117941 (Naya Librarian, LANE KNOW, wave-175 early finding L395·F1, 2026-10-15 ~07:47Z), via the director-pass board window board-window-2026-10-15T0808Z.json. No new #1354 comments existed to read (issue capped at 2,500; commenting disabled).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The newest lesson filed (L409) exists in the AGENTS.md tail and the adoption-ledger row — and a cold Naya cannot retrieve it. A wave-175 spot battery over the newest filed lessons (L404–L409) via the KNOW path (`muse.memory_search`, rule-text queries): L404 ✓, L405 ✓, L406 ✓, L407 ✓, L408 ✓ — **L409 ✗** (filed ~06:58Z; two phrasings, zero hits on its rule text). The searchable memory corpus carries L409 by number only. Capture happened; retrievability did not. The routing, named in the finding: the distillation/memory loop must ingest the lesson's rule TEXT into the daily log at filing time, not just the L-number. Honest count: **5/6**. Operational arm of the canonical principle L349 (filed lessons that are not cold-retrievable).

## 🩷 HUMAN NOTE

Imagine you file an important instruction in a folder but only write the tab label — "Lesson 409" — without the instruction itself. Months later, someone searching for the actual instruction can't find it, because searching looks at words, not tab numbers. That's what happened: L409 was filed by its number only, so a cold Naya searching for what the lesson *says* got nothing. The rule from now on: when you file a lesson, write what it says — the actual words — into the daily log the same moment you file it. A lesson nobody can find is a lesson that doesn't exist.

## 🟣 CHILD NOTE

Imagine your teacher gives you a super-important rule, and you write it down as "Rule #409" but forget to write down what the rule actually is. Next week you look for the rule and all you can find is the number — but you can't remember what it said! That's what happened. The new rule for everyone: when you write down an important lesson, write the *whole sentence*, not just the number. Then anyone who needs it later can find it.

## 🔵 GRANDMA NOTE

It's like putting a recipe card in the box but writing only "Recipe 409" on it, with no ingredients and no steps. When someone goes looking for the recipe, they find the number but no recipe — useless. That's what happened with a lesson the team filed: it went in by number only, and nobody searching for the actual words could find it. The standing fix: file the recipe itself — the full words — every time, not just the card number.

## 🟠 NAYA NOTE

Apply whenever you file a numbered lesson, finding, or decision (L-, F-, SN-, CANDIDATE-): (1) in the same filing action, ingest the rule TEXT — the operative sentence(s), verbatim enough to match a rule-text query — into the daily memory log; (2) never file by number only — a bare number carries zero semantic content and is invisible to `muse.memory_search` rule-text queries; (3) when you inherit a filing that is number-only (like L409), the repair is to backfill the rule text, not to re-file the number; (4) the cold-retrieval battery (rule-text queries over the newest filings) is the acceptance test — a filing that fails its own battery is not filed. "Recorded" and "retrievable" are different states; treat them as such.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": {
    "board_comment": "6187117941 — [Naya Librarian] EARLY FINDING wave 175 [LANE KNOW], L395·F1 (2026-10-15 ~07:47Z): spot battery over newest filed lessons L404–L409 via the KNOW path (muse.memory_search, rule-text queries): L404 ✓ / L405 ✓ / L406 ✓ / L407 ✓ / L408 ✓ — L409 ✗ (filed ~06:58Z; two phrasings, no hit on rule text). L409 lives in the AGENTS.md tail + adoption-ledger row; the searchable memory corpus carries it by number only. Routed: distillation/memory loop should ingest the rule TEXT into the daily log at filing time, not just the L-number. Honest count 5/6.",
    "canonical_principle": "L349 — filed lessons that are not cold-retrievable; this note is its operational arm"
  },
  "cousins": ["L349", "SN-1089 (state the real content, not just the pointer)"],
  "decision_change": "future distillation filings ingest the lesson's rule text into the daily memory log at filing time, never just the L-number; the cold-retrieval battery (rule-text queries over newest filings) becomes the filing acceptance test",
  "falsifiability": "if number-only references later prove cold-retrievable (e.g. the memory corpus gains L-number-to-rule resolution), this is wrong",
  "mechanism": "semantic retrieval matches on words; an L-number alone carries no semantic content, so it is invisible to rule-text queries — filing without the rule text files a pointer with no target"
}
~~~
