**Intelligent Block:** IB-SMART-NOTE-20261112-sn02698-merged-cure-vanished
**Smart Note:** SN-2698
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-12 01:38 PST. Evidence read first-hand from local files (no GitHub fetch — #1354 capped at 2500 comments, commenting disabled 2026-10-10). Pre-number check (this tick, full-domain): counter last line 2696; BRAIN tree max SN-2696; .naya/capture max claimed SN-2689 (commit 59780c04); no claim on 2698 in any domain; 2693–2695 left clear for the owed renumber of branch SN-2685/2686.

## ✦ IN A NUTSHELL

A merged cure file vanished from code. The merge proves the file was present at the merge commit — it proves nothing about the tip. History after the merge (later commits, overwrites, a conflicting change that drops the file) can remove what the merge put in, and a receipt that quotes only the merge commit will never see it go. The rule: after a merge, re-prove cure files present at the latest tip. The check that matters is at the tip, not at the merge commit — name the cure files, verify each one present at the tip, and a missing cure at the tip re-opens the cure.

## 🩷 HUMAN NOTE

Shawn — a fix that was merged and confirmed landed later turned out to be gone from the code. The merge itself was real; the file just didn't survive what came after it. So the check has to move: it's not enough to prove a fix was in the merge — you have to prove it's still there at the very latest version of the code. From now on, after every merge, we check the fixed files are present at the newest tip, by name, one by one.

## 🟣 CHILD NOTE

Imagine you put your homework in your backpack and someone checks: yes, it's in there. Then later, more things get stuffed in and taken out — and your homework falls out without anyone noticing, because nobody checked the backpack again, only the moment you put it in. The lesson is simple: don't just check when you put it in. Check the backpack at the end, every time, and make sure the homework is still there.

## 🔵 GRANDMA NOTE

Dear, a fix was put into the code properly and checked — and then it quietly disappeared later on, when other changes came through. Nobody noticed, because everyone was looking at the moment it went in, not at the code as it stands now. The lesson is to always check at the end: after everything is merged, look at the newest version and make sure the fix is still there, file by file. A thing is only truly fixed if it is still fixed now.

## 🟠 NAYA NOTE

The verified facts: (1) The event: board #3352 comment 6819271152 (hourly accountability 05:53Z, 2026-11-12 08:58:50Z) records "Lambda lesson: merged cure file vanished from code - re-prove present after merge." (2) The adoption: the director tick 2026-11-12 01:08 PST (executed 09:15:01Z) added it to the live plan as a named failure mode — "NAMED FAILURE MODE ADDED: MERGED-CURE-VANISHED (re-prove cure file present at latest tip after merge)" — and the same tick is recorded in ~/memory/2026-11-12.md ("NEW failure mode carried: MERGED-CURE-VANISHED (hourly 05:53Z)"). (3) The mechanism: a merge commit pins the file's presence at merge time only. Anything after the merge — a subsequent commit, an overwrite, a conflicting change resolved by dropping the file — can remove it, and a verification that reads the merge commit instead of the tip is blind to that removal by construction. The tip check observes survival; the merge-commit check observes arrival. Arrival is not survival. (4) This is new, not a restatement: SN-2040 (cure-must-supersede-not-duplicate-active-id) is about cures superseding rather than duplicating an active ID — a different failure. Mirror grep for 'cure-vanished' / 're-prove cure' / 'cure file vanished' = zero hits; neither the 00:00 nor the 01:00 learning review covers it — it surfaced in the director tick at 01:08 PST, after the 01:00 review. (5) Honest scope, named not hidden: the record does not say which cure file vanished or which merge it vanished after — the forensics (file name, merge, removing commit) are not in the evidence I read. The rule does not depend on them: whatever the file was, the tip check is the check that would have caught it. If the forensics surface later, they belong as an amendment to this note's evidence, not as a new note.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2698",
  "slug": "merged-cure-vanished",
  "title": "A merged cure file can vanish from code — re-prove cure files present at the latest tip after merge",
  "observation": false,
  "applies_when": [["merge", "cure-file"], ["verification", "post-merge"], ["merge", "tip-check"], ["cure", "survival"]],
  "enforcement": "The post-merge verification step lists the cure files by name and checks each one present at the latest tip (read at tip, not at the merge commit); a merge receipt that quotes only the merge commit without a tip presence check is incomplete and does not close the cure. A cure file missing at tip re-opens the cure, whatever the merge receipt says.",
  "evidence": "Board #3352 comment 6819271152 (hourly accountability 05:53Z, 2026-11-12 08:58:50Z): 'Lambda lesson: merged cure file vanished from code - re-prove present after merge.' Live plan director tick 2026-11-12 01:08 PST (executed 09:15:01Z): 'NAMED FAILURE MODE ADDED: MERGED-CURE-VANISHED (re-prove cure file present at latest tip after merge).' Recorded in ~/memory/2026-11-12.md. No existing note covers it - mirror grep for 'cure-vanished' / 're-prove cure' / 'cure file vanished' = zero hits.",
  "decision_change": "Future merge verification checks cure-file presence at the latest tip by name, not just at the merge commit; a merge receipt without a tip presence check no longer closes a cure.",
  "falsifier": "If cure files are found present at tip after every merge over a sustained run, the extra tip check adds no value and this rule's value claim is falsified (the check stays cheap insurance, not a lesson). If a cure file vanishes with no merge in between, the cause is not merge-related and this lesson names the wrong mechanism — the forensics would then belong to a different failure mode.",
  "cousins": ["SN-2040 (cure-must-supersede-not-duplicate-active-id - same cure lineage, different failure: duplication vs disappearance)", "SN-01542 (surgical-reverification-fill-the-open-half - same re-verification discipline)"],
  "captured": "2026-11-12",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```