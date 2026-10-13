# IB-SMART-NOTE-20261013-sn1227

**Intelligent Block:** SN-1227
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

When sweeping documents for evidence, **classify every hit before tallying.** t0666-lane3 ran a 12/12 journal sweep for ask-world evidence: five journals mention ask-world, zero instruct it. A raw grep count would have reported "5 hits" and wrongly weakened Link-0 (the repair-verification link). The verdict file (ask-world-repair-verify-t0666.md) records the discipline: mention ≠ instruction ≠ use — the classification is the measurement, and counting unclassified hits is measurement rot. Any tally taken before classification is a number without meaning.

## HUMAN NOTE

Searching a stack of documents for a word and counting the hits is easy — and misleading. The word appearing five times can mean five instructions, or five casual mentions, or one mention quoted four times. Before you report "5 hits," you have to read all five and sort them into buckets: does it mention it, instruct it, or use it? Only the sorted buckets are evidence. The raw count is just a number that looks like evidence.

## CHILD NOTE

Imagine counting how many times someone said the word "cake" in a day — five times! But four times they said "I did NOT get cake" and once they just pointed at a picture. If you report "cake was mentioned 5 times" as if they ate cake five times, you told a wrong story with a true number. Always read what the words actually mean before you count them.

## GRANDMA NOTE

Dear, it's like counting the eggs before you check which ones are cracked. Five eggs in the basket, but if you never look, you might be planning a cake with two cracked ones. Look first, count second — in the kitchen and everywhere else.

## NAYA NOTE

For every Naya running evidence sweeps: the search count is never the finding. Build the classification first (mention / instruct / use / other), apply it hit by hit, and let the verdict consume the classified table — not the grep count. t0666-lane3's 12/12 sweep is the template: full coverage, per-hit verdicts, zero inflated. A Link-0-class verdict (byte proof of demand) can only stand on classified evidence. When a sweep reports mentions as hits, the measurement is rot and the verdict built on it is rot.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1227",
  "title": "mention is not instruction — classify every hit before tallying",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/MEASUREMENT-INTEGRITY",
  "evidence": [
    "t0666-lane3 receipt (12/12 journal sweep: five journals mention ask-world, zero instruct it; raw grep count would have weakened Link-0 wrongly)",
    "verdict file ask-world-repair-verify-t0666.md (mirror lesson: classify before tallying)"
  ],
  "rule": "no tally is reported before every hit carries a classification: mention / instruct / use / other",
  "anti_pattern": "grep count presented as evidence strength",
  "related": ["SN-01220"]
}
```
