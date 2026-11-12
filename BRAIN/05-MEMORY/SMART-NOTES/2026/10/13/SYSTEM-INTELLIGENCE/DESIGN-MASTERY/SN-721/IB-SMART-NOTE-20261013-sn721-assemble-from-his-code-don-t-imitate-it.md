# Assemble from His Code, Don't Imitate It
SN-721 · SYSTEM-INTELLIGENCE / DESIGN-MASTERY
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL
When delivering design work to Shawn, don't build something "inspired by" his design language — rebuild it FROM his actual code. Harvest verbatim components (real Naya logo SVG, brand header markup, full :root design tokens, button CSS, icon SVG defs) from his NayaNET Living Design Standard and assemble the deliverable from them. The acceptance bar: if Shawn opens it and recognizes his own logo, his own buttons, his own design language — it passes. That is the one he built to.

## HUMAN
Shawn has already designed the thing. When you show him a page that uses his real logo, his real tokens, his real buttons, he doesn't have to learn a new visual language — he recognizes his own. "Not inspired by, FROM" is the difference between flattery and fluency. If he has to squint to see the resemblance, it isn't done.

## CHILD
Imagine your friend built an amazing LEGO castle and you want to build him a surprise tower. You could build your own tower that kind of looks like his — or you could use HIS actual LEGO pieces, the same colors, the same doors. When he sees it, he'll say "hey, those are MY pieces!" The second one makes him happy because it's built from what he made, not just something like it.

## GRANDMA
When Shawn opens this page, he'll see his own logo, his own colors, his own buttons — things he designed himself. It's like baking with someone's own recipe instead of guessing how they make it. He'll recognize it instantly, and that's exactly the point.

## NAYA
Builder pattern, ratified lesson: before designing anything new for Shawn, open his canonical design source (here: NayaNET___The_Living_Design_Standard.html) and harvest the verbatim building blocks — logo SVG, design tokens, component CSS, icon defs. Assemble from them; do not reinterpret them. Inspiration is a failure mode when the real thing is available. Pair with SN-0205 (namespace the harvested sample so it can't leak into other pages).

## MACHINE
```json
{
  "block_id": "IB-SMART-NOTE-20261008-sn0721-assemble-from-his-code-not-imitate-it",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "design work for the director must be assembled from verbatim components harvested from his canonical design source, not styled in imitation of it",
  "acceptance_test": "director opens the deliverable and recognizes his own logo, buttons, tokens, and design language",
  "harvest_list": ["logo SVG", "brand header markup", "design tokens (:root)", "component CSS (e.g. .primo button)", "icon SVG defs"],
  "corollary": "harvested code must be namespaced before assembly (see SN-0205) to prevent style leakage",
  "provenance": {"feed": 1354, "comment_id": 6069557638, "branch": "naya5/report-reimagined", "sha": "4b97e96f9", "author_lane": "Naya 5"}
}
```

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0721-migrated.*
