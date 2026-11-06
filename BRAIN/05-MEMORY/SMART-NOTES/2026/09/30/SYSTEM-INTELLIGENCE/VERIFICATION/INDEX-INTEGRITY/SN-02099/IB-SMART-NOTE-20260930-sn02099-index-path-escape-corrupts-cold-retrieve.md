# An Index Entry That Escapes Its Allowed Roots Corrupts Cold Retrieve

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02099-index-path-escape-corrupts-cold-retrieve
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Director tick 2026-11-05 19:08 PST (2026-11-06T03:16:44Z), ~/memory/2026-11-05.md — new failure mode INDEX_CORRUPT:PATH_ESCAPE named first-hand from the live tip; LEARN-builder re-measurement at 8b0e3fc4 in the same tick.

## ✦ IN A NUTSHELL

On 2026-11-05 the director tick named a new failure mode, INDEX_CORRUPT:PATH_ESCAPE: 23 index entries point at bare BRAIN/05-MEMORY/ files outside the allowed roots, written by the #3221 breach (#182). The Cold Retrieve drill run against that index collapsed 11/11 → 1/11, vanish list 3 → 10, Successor 3.0 → 2.5. The drill did not get worse at retrieval — it read a corrupt index. The retriever resolves index paths literally, so entries outside the allowed roots resolve to wrong or missing content; and nothing validates entry paths at write time, so the breach wrote them unchecked and the corruption stayed silent until a drill ran. The lesson: a drill collapse is an index-integrity signal first and a retrieval-quality signal second. Never quote a collapsed drill score as retrieval quality, and never tune retrieval against an unvalidated index: validate every entry's path against the allowed roots before the drill, repair first, re-drill after. The fix was proven locally and is unpushed — this note records the rule, not the repair.

## 🩷 HUMAN NOTE

Shawn — the library's card catalog had 23 cards pointing at shelves that don't exist. They got there through a bad merge, and nothing checks the cards when they're written — so nobody knew until someone tried to actually find things and the test collapsed from 11 out of 11 to 1 out of 11. The finding system didn't get worse; it was reading a broken catalog. The rule from now on: before anyone quotes a retrieval test score, check that every card points inside the allowed shelves. A bad score against a broken catalog is a catalog problem, not a finding problem. Fix the catalog first, then re-run the test.

## 🟣 CHILD NOTE

Imagine a treasure map with 23 X's drawn outside the playground fence — in places that aren't even on the map. You follow the map, you can't find the treasure, and you think you're bad at treasure hunting. But you're not bad — the map is wrong. The lesson: before you say "I'm bad at finding things," check that every X on the map is inside the playground. Fix the map first, then try again.

## 🔵 GRANDMA NOTE

Dear, we learned something plain: a test that says "you can't find anything" might be lying about you and telling the truth about the list it was given. Twenty-three entries in our index pointed to places outside where they're allowed to point — written in by a bad merge, and nobody checked them at the door. The list stayed wrong and quiet until the test ran and fell apart. So now we check the list before we trust the test: every entry must point inside the allowed shelves, or the test doesn't count. Fix the list, then run the test again. Don't blame the finder for a broken list.

## 🟠 NAYA NOTE

This note exists because a real drill collapsed on a real corrupt index, and the collapse was measured, not guessed: director tick 2026-11-05 19:08 PST named INDEX_CORRUPT:PATH_ESCAPE — 23 index entries pointing at bare BRAIN/05-MEMORY/ files outside the allowed roots, from #3221 breach #182 — with the Cold Retrieve drill at 11/11 → 1/11, vanish list 3 → 10, Successor 3.0 → 2.5, and the fix proven locally but unpushed. Future decision changed: no Cold Retrieve drill score is quoted or acted on until the index passes a path-root validation; a collapse with path-escape entries present is read as INDEX_CORRUPT first — repair, re-drill, and only then judge retrieval. Falsifier: if a drill scores 11/11 (or the vanish list stays at 3) with path-escape entries present, the link is broken and this lesson is wrong; if removing the 23 entries leaves the drill at 1/11, the collapse had a different cause. Mechanism: the retriever resolves index paths literally, so out-of-root entries resolve to wrong or missing content and the drill's vanish list grows; nothing validates entry paths at write time, so a breach can write them unchecked and the corruption stays silent until a drill runs. Relations: SN-0250 covers the adjacent trap (a green run coexisting with a corrupt registry — stale hash pointers, not path escapes); SN-2053 covers the landing side (a bulk import bypassing filing checks corrupts the registry); SN-1866 covers manifest staleness failing closed. This note covers the read side: the index itself can be corrupt in a way that makes a retrieval measurement lie, and the pre-drill path check is the control.

## 🟢 MACHINE NOTE

```json
{
  "applies_when": [
    ["index", "integrity"],
    ["retrieve", "cold-retrieve"],
    ["breach", "index-write"]
  ],
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "This note judges the index (entry paths must stay inside allowed roots), not the retriever's ranking or the drilled content's merit. A low drill score against a validated index is a retrieval finding; a low drill score against an unvalidated index is an index finding.",
  "decision_change": "Before any Cold Retrieve drill score is quoted or acted on, validate every index entry's path against the allowed roots; a drill collapse with path-escape entries present is read as INDEX_CORRUPT first — repair the index, re-drill, and only then judge retrieval. Index writers validate entry paths at write time.",
  "enforcement": "Cold Retrieve drill pre-check: every index entry's path checked against the allowed roots before the drill runs; any entry outside the roots fails the drill closed as INDEX_CORRUPT (no retrieval score is recorded) and the drill re-runs only after the repair. Index-write path validation rejects out-of-root entries at write time. Verified by the pre-check output itself, not by the drill score.",
  "evidence": [
    "Director tick 2026-11-05 19:08 PST (2026-11-06T03:16:44Z), ~/memory/2026-11-05.md: INDEX_CORRUPT:PATH_ESCAPE — 23 index entries point at bare BRAIN/05-MEMORY/ files outside allowed roots, from #3221 breach #182; Cold Retrieve drill 11/11 -> 1/11, vanish list 3 -> 10, Successor 3.0 -> 2.5; fix proven locally, unpushed",
    "Same tick: LEARN-builder re-measurement @8b0e3fc4 — 321 notes cured locally, LEARN 5.0 HELD, convergence 9.0 HELD, raw tip door 665 defects / 1126 pages"
  ],
  "falsifier": "If a Cold Retrieve drill scores 11/11 (or the vanish list stays at 3) with path-escape entries present in the index, the link is broken and this lesson is wrong; if removing the 23 entries leaves the drill at 1/11, the collapse had a different cause.",
  "mechanism": "The retriever resolves index paths literally; entries pointing at bare BRAIN/05-MEMORY/ files outside allowed roots resolve to wrong or missing content, so the drill's vanish list grows and the Successor score collapses. Nothing validates entry paths at write time, so a breach can write them unchecked and the corruption stays silent until a drill runs."
}
```
