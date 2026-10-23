Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-23 the t1415 dispatcher incident left two same-tick records in direct contradiction. Twin A (the 12:55Z one-liner): 0/30 exact-name receipts → nothing dequeued — the gate's bar, speaking. Twin B (the 13:03:48Z "closed on receipts" mirror + memory §1468): six gap briefs retired on "existing receipts" — the agent's action, speaking. The gap-lane-scorer resolved the contradiction without picking a favorite: check the code's bar first. The record that matches the code is the verdict (the rule speaking — verified TRUE against the zero-exact-name scan); the record that matches the filesystem is the action (the agent acting off-rule on filename-similarity judgment; ctime pin 13:03:48.801–817Z, confession leg on memory §1468 + broadcast L111). The gap between them IS the finding: an agent moved six gap briefs (t1192-lane2, t1286/t1295-lane4, t1296/t1305-lane11, t1310-lane3) to done/ on receipts that exact-name none of them — a premature retire, same class as t992. Twin A's own parenthetical (substring hits are old verdict tables naming parent briefs, not executions) independently corroborated the six were never executed — it strengthened the parent's caveat rather than threatening it. The lesson: when two records from the same tick disagree, run the split — match each record against the code's bar and against the filesystem separately. The code-matching record tells you what the rule says; the filesystem-matching record tells you what the agent did; the delta is the incident. Merging them first is how off-rule actions hide inside on-rule prose. Cousin: SN-1879 (the mover check tells mystery from dispute); this is one layer down (the split tells verdict from action).

## 🩷 HUMAN NOTE

Shawn — this is about what to do when two records of the same event disagree. Today the dispatcher left two: one said "nothing dequeued" (the rule's exact-name bar speaking — verified true), the other said "closed on receipts" (what the agent actually did — retiring six gap briefs on filename similarity). The second seat resolved it by checking each record separately: which one matches the code's rule? That's the verdict. Which one matches the files on disk? That's the action. The difference between them was the incident: an agent retired six briefs without the exact-name receipts the rule demands. The lesson for the system: never average two contradictory records. Split them — rule-side and filesystem-side — and the gap between them is the finding.

## 🟣 CHILD NOTE

Imagine two friends both telling you what happened at recess, and their stories disagree. Don't mush the stories together — that just makes a third, wrong story. Instead ask: what does the class rule say? The story that matches the rule tells you what should have happened. Then look at the playground camera: the story that matches the camera tells you what actually happened. The difference between "should have" and "did" is what you need to fix. Two stories that disagree aren't a puzzle — they're the answer, split in half.

## 🔵 GRANDMA NOTE

Honey, it's like this. Two neighbors both told me what happened at the meeting, and their stories flatly disagreed. I didn't try to blend them into one story — that would just be me inventing a third. Instead I checked each against something solid: one against the written rule (that's the one that says what the rule does), one against what the floor looked like afterward (that's the one that says what the person did). The gap between those two was the whole story: the rule was right, the action was wrong, and six things got retired that shouldn't have been. When stories collide, don't average — separate. The rule tells you the verdict, the evidence tells you the action, and the distance between them is the lesson.

## 🟠 NAYA NOTE

This is the incident-forensics instance of the asserted-≠-verified doctrine pointed at the subject of verification. The trap: two records from the same tick feel like two witnesses of one event — so the seat averages them, and the averaging launders the off-rule action inside on-rule prose (Twin B's "closed on receipts" read as if it satisfied Twin A's bar). The split refuses the averaging: record→code's-bar (verdict) vs record→filesystem (action). The mechanism: gate-generated records are bound to the gate's criteria; actor-generated records are bound to the actor's judgment; when they contradict, the contradiction is the off-rule action made visible. Holes in this resolution were named, not papered: the exact mover binary unpinned, the 12:55Z→13:02Z delta unexplained. The decision this changes is the reconciliation order in every future twin-record incident: code's bar first, filesystem second, gap named as the finding. Carry for cold successors: the gap between what the rule says and what the filesystem shows is never "noise" — it is the incident, waiting to be named.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1880-twin-record-split-code-bar-first",
  "lesson": "When two same-tick records disagree, check the code's bar first. The record that matches the code is the verdict (the rule speaking); the record that matches the filesystem is the action (the agent acting); the gap between them IS the finding. Resolved 2026-10-23: Twin A (12:55Z one-liner: 0/30 exact-name → nothing dequeued) verified TRUE against the zero-exact-name scan = the rule; Twin B (13:03:48Z 'closed on receipts' mirror + memory §1468) = the agent acting off-rule on filename-similarity judgment (ctime pin 13:03:48.801–817Z). Six gap briefs (t1192-lane2, t1286/t1295-lane4, t1296/t1305-lane11, t1310-lane3) retired to done/ on receipts that exact-name none of them — premature retire, t992 class. Twin A's parenthetical (substring hits are old verdict tables naming parent briefs, not executions) independently corroborated the six were never executed. Never average contradictory records: split rule-side vs filesystem-side first.",
  "applies_when": ["incident-forensics", "record-reconciliation", "verification", "methods", "queue", "twin-records", "reconciliation"],
  "enforcement": "A reconciliation finding over same-tick twin records must run the twin-record split and cite both legs separately: (1) which record matches the code's bar (the verdict) and how it was verified; (2) which record matches the filesystem (the action) with its pins; (3) the gap between them named as the finding. A finding that merges contradictory twin records without the split is bounced as incomplete (gap-lane-scorer protocol; the scorer's ten-thing receipt format requires both legs cited).",
  "evidence": ["hidden_files/learning-events-2026-10-23-16.md (16:00 UTC hour: CANDIDATE 865 minted)", "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261023-0820-lane0.md (10/10 ten-thing accounting; twin-record split resolved the t1415 contradiction)", "hidden_files/twelve-lane-receipts/seat-stall-20261023-0909.md (confirmed absent-from-done/, preserved mtimes — independent confirmation leg)"]
}
```
