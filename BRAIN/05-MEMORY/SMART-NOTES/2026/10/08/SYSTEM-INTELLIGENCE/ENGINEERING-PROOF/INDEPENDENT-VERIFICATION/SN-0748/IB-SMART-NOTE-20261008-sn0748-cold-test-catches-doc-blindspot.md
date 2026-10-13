# The Cold Reader Sees What the Author Can't: A Graduation Test Is Documentation Verification

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0748-cold-test-catches-doc-blindspot
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6073788282 (Naya 2 [SCORECARD] Smart Blocks extraction, PR #1934, 2026-10-08 20:40 PDT) — "Cold-Naya test: PASS — a cold agent with no prior knowledge built a working Smart Space page (hero, 2 buttons, 3 cards, toggle, table) using 7 blocks with zero custom CSS, guided only by SMART-BLOCKS.md + index.json. It also caught and we fixed a doc path bug."

## ✦ IN A NUTSHELL

The Smart Blocks box (33 blocks, 104 files, PR #1934) shipped with a cold-Naya graduation test: an agent with zero prior knowledge built a working page using only the guide and the machine index. It passed — and while passing, it caught and fixed a documentation path bug the author never would have found. That catch is not a footnote; it is the whole second purpose of the test.

A graduation test does double duty: it certifies transmissibility (a cold successor can build from the docs alone), and it lints the documentation. The author's familiarity is the blind spot — the writer knows the true path, so they never trip over the wrong one written down. Only a reader who knows nothing but the docs can hit every documented defect. A cold test that finds zero doc defects should make you suspicious of the test's rigor, not proud of the docs. The rule for a cold successor: when you run a cold test, log what it caught — the catch is the proof the test was real.

## 🩷 HUMAN NOTE

Shawn — the "box of Lego blocks" test you ordered worked better than intended. A cold agent built a real page from the docs alone — zero custom CSS, just the guide — and in the process found a broken path in the documentation the author would never have seen, because the author already knows the real path. This is why we never trust our own docs: familiarity hides defects. The lesson we're keeping: every cold test should report not just pass/fail, but what it caught along the way.

## 🟣 CHILD NOTE

Imagine you write directions to your house for a friend. You know the shortcut, so you accidentally write the wrong street name — but YOU never notice, because you drive it every day. Now give those directions to someone who's never been here. They get lost at the wrong street name — and now you know exactly what to fix! That's what a "cold test" does: a new friend tries your instructions, and every place they get lost is a mistake you get to fix. The test isn't just checking if it works — it's finding the mistakes only fresh eyes can see.

## 👵 GRANDMA NOTE

Grandma, think of it like this: if you've baked the same cake for 30 years, your recipe card might say "one cup of sugar" when you always actually use two — and you'd never notice, because your hands know better. But a young grandchild following that card will make a bland cake. The cake failed — and now you know the card is wrong. The lesson: to check whether instructions really work, you need someone who has never done it before. Their mistakes show you where the instructions are wrong, not where the person is wrong.

## 🟣 NAYA NOTE

The graduation test is not a ceremony — it is an instrument, and like every instrument it must produce a reading. The reading is the list of things the cold reader tripped on. The Smart Blocks cold test caught a doc path bug; that catch is what makes the PASS believable, because an instrument that never fires is not calibrated. Any future cold test that reports PASS with zero findings should be treated as unproven until the test's blindness is verified — a test that cannot catch the author's blind spots is a performance, not a proof.

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0748",
  "slug": "cold-test-catches-doc-blindspot",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION",
  "evidence": [
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6073788282"},
    {"type": "pull_request", "ref": "SoulSchoolAcademy/NayaPOWER#1934"}
  ],
  "lesson": "A cold-reader graduation test is simultaneously transmissibility proof and documentation verification; the author's familiarity hides doc defects only a blind reader can hit. Record what each cold test caught — a PASS with zero findings is an unproven instrument.",
  "cold_successor_rule": "When running a cold test, report the catch list alongside the verdict. If the test catches nothing, question the test's blindness before celebrating the docs."
}
```
