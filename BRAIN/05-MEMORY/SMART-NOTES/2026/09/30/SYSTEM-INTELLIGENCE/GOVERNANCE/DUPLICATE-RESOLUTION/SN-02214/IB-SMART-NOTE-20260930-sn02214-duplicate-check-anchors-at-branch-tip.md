# INTELLIGENT BLOCK — SN-2214

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02214-duplicate-check-anchors-at-branch-tip
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Distillation tick 2026-11-06 11:38 PST staged SN-2211 "Diff the Trees Before Diffing the File — A Snapshot Branch Is Not a Merge Candidate" (commit e952c1c9 on naya4/smart-notes-2026-09-30) as CANDIDATE 1013, the tree-diff scoping lesson from distill-daily-20261106 (PR #3258: 45-line file diff vs 3,211-file tree diff, −1.16M lines). The same CANDIDATE 1013 lesson was already staged 05:38 PST the same day as SN-02210 "Diff the Trees Before Diffing the File" (commit 3b29630b2, path BRAIN/05-MEMORY/SMART-NOTES/2026/11/06/SYSTEM-INTELLIGENCE/OPERATIONS/SYNC-DISCIPLINE/SN-02210). The 11:38 tick's duplication check read SN-1984..2093 — a fixed historical range ending below the same-day staging — and missed SN-02210. Main seat flagged the duplicate ~11:52 PST; the 12:08 PST distillation tick corroborated (stale range, not a content miss) and logged the pair for lead adjudication (retire/supersede one — a lead decision, not this note's job). The staging script's identical-content skip cannot catch it: different wording, same lesson.

## ✦ IN A NUTSHELL

On 2026-11-06 the same lesson got staged twice, hours apart, under two numbers: SN-02210 at 05:38 and SN-2211 at 11:38 — both CANDIDATE 1013, both "diff the trees before diffing the file," both from the same distill-daily run and the same PR #3258 numbers. The 11:38 duplicate check failed because it read a fixed historical range (SN-1984..2093) instead of the branch as it stood that morning. The rule this failure buys: **a duplication check anchors at the branch tip and matches on content, never on a fixed number range or a number string.** The counter advances between ticks, so any fixed range is stale the moment a newer note lands; and a number-string search misses the same lesson filed under a differently-padded or different number (SN-2210 vs SN-02210 — padding is identity per SN-02102, but the search string still has to match). Before taking a number, read the newest notes at the tip and grep the branch tree for the lesson's keywords. A check that reads yesterday's range is not a check — it is a permission slip for a duplicate.

## 🩷 HUMAN NOTE

Shawn — a small process fix worth keeping: today the same lesson ("diff the trees before diffing the file") got filed twice, as SN-02210 in the morning and SN-2211 before noon, because the second check looked at an old slice of notes instead of the newest ones. The fix is simple and now written down: before filing a new note, the check starts from the newest notes on the branch and searches by the lesson's words, not by its number — numbers change, padding changes, the words are what match. The duplicate pair itself still needs a lead call on which one to keep; this note just makes sure the next check can't repeat the miss.

## 🟣 CHILD NOTE

Imagine you are putting books on a shelf, and before adding one you check whether it is already there — but you only look at the bottom shelf, while the same book was put on the top shelf this morning. You add a second copy because you looked in the wrong place. The fix: always check the newest books first, and check by the story inside, not by the number on the spine — the same story can wear a different number. Look at the top of the pile, read the words, and you will never shelve the same book twice.

## 🔵 GRANDMA NOTE

Dear, it is like checking the pantry before buying more flour — but you only open the left cupboard, while this morning's bag is sitting in the right one. You come home with a second bag you did not need. The house rule from now on: check the freshest shelf first, and check by what is inside the bag, not by the label on the outside — the same flour can come in a different bag. A quick look in the right place saves the duplicate every time.

## 🟠 NAYA NOTE

Cold successor, running this loop: your duplication check has two non-negotiable properties, and the 2026-11-06 SN-02210/SN-2211 pair is what happens when the first one is missing. (1) **Anchor at the branch tip.** Read the newest notes staged — the last ~30 by commit time, or the branch tip's tree — never a fixed historical range like SN-1984..2093. The counter advances between ticks; a range that was "recent" yesterday is stale today, and same-day stagings are exactly what it misses. (2) **Match on content keywords, never on a number string.** Grep the branch tree for the lesson's distinctive words ("diff the trees," the PR number, the key figures) — the same lesson can arrive under a different number or a differently-padded one, and a literal "SN-2210" search misses "SN-02210" (SN-02102: padding is identity). If the check finds a same-lesson note, do not stage — log the duplicate and move on; the staging script's identical-content skip only catches byte-identical files, not same-lesson rewordings. When a duplicate does slip through, the remedy doctrine is SN-01217 (converge, don't ship both) and the pair goes to the lead for retire/supersede — you record it, you don't adjudicate it.

## 🟢 MACHINE NOTE

```json
{
  "slug": "duplicate-check-anchors-at-branch-tip",
  "sn": "SN-2214",
  "title": "A Duplication Check That Reads a Stale Range Is Not a Check — Anchor at the Branch Tip and Match on Content",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-06",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "DUPLICATE-RESOLUTION"],
  "related": ["SN-02102", "SN-02212", "SN-01217", "SN-02210", "SN-2211"],
  "applies_when": ["distillation", "duplication-check", "claim", "staging"],
  "enforcement": "Before taking an SN number, the duplication check must (1) read the newest notes at the branch tip (last ~30 staged by commit time, or the branch tip tree) — never a fixed historical SN range — and (2) grep the full branch tree for the candidate lesson's distinctive content keywords (rule phrase, PR number, key figures), never a literal SN-number string. A check that reads a fixed range or searches by number fails the gate: the note is BOUNCED, not staged. The staging script's identical-content skip is only a backstop for byte-identical files and does not satisfy this check.",
  "falsifier": "A duplicate lesson staged after a tip-anchored, content-keyword duplication check would falsify the rule — it would show the check as specified still misses same-lesson notes, and the enforcement would need a wider keyword set or a wider tip window. Conversely, a same-day second staging caught by the check before taking a number would strengthen it.",
  "decision_changed": "How the pre-staging duplication check is run: it now starts from the branch tip's newest notes and matches on content keywords instead of reading a fixed historical SN range or searching a literal SN-number string — so a lesson staged hours earlier the same day is found before a second number is taken, instead of being staged twice under two numbers.",
  "mechanism": "The SN counter advances between distillation ticks, so any fixed historical range (e.g. SN-1984..2093) goes stale the moment a newer note lands — and same-day stagings are exactly the notes a stale range misses. A literal number-string search fails a second way: the same lesson can be filed under a different number or a differently-padded one (SN-2210 vs SN-02210), and padding is identity per SN-02102, so the string never matches. Content keywords are stable across both failure modes: the rule phrase, the PR number, and the key figures are the same in both stagings. The 11:38 tick's check failed on the range; the main seat's ~11:52 flag additionally caught the padding-string miss — both are cured by anchoring at the tip and matching on content.",
  "provenance": "Distillation tick 2026-11-06 11:38 PST staged SN-2211 (commit e952c1c9, 'Diff the Trees Before Diffing the File — A Snapshot Branch Is Not a Merge Candidate', CANDIDATE 1013, distill-daily-20261106, PR #3258: 45-line file diff vs 3,211-file tree diff, −1.16M lines). SN-02210, the same CANDIDATE 1013 lesson, staged 2026-11-06 05:38 PST (commit 3b29630b2, path BRAIN/05-MEMORY/SMART-NOTES/2026/11/06/SYSTEM-INTELLIGENCE/OPERATIONS/SYNC-DISCIPLINE/SN-02210). 11:38 duplication check read SN-1984..2093 and missed SN-02210. Main seat flagged the duplicate ~11:52 PST (same event, same numbers, same rule); 12:08 PST distillation tick corroborated the stale-range cause and logged lead adjudication owed (retire/supersede one of the pair). Related: SN-02102 (padding is identity — SN-781 is not SN-0781), SN-02212 (census must span main and branch), SN-01217 (converge, don't ship both)."
}
```
