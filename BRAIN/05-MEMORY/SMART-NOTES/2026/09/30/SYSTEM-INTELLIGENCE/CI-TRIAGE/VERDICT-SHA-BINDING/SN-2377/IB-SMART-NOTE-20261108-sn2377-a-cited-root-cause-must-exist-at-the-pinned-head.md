# A Cited Root Cause Must Exist at the Pinned Head

**Intelligent Block:** IB-SMART-NOTE-20261108-sn2377-a-cited-root-cause-must-exist-at-the-pinned-head
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

SN-2373 (mobile-stack fix, window J, 2026-11-08) states its root cause as "the §8 desktop enlargements (16.5px board type, 42px pill jewels) had cascaded into mobile", and SN-2370 records the same recipe as "locked in as `ANATOMY-OF-A-VIEWPORT.md` §8". First-hand verification this run: `TEAM-NITRO/viewpoints/ANATOMY-OF-A-VIEWPORT.md` at main tip 5756d0a8 contains zero occurrences of "§8", and its section headings run 1, 2, 3, 2, 3, 4, 5, 6, 7 — no section 8, and the numbering itself duplicates §2 and §3. The window-J verifier had independently found the same absence at anchor c6263829, and window J contains no ANATOMY commit, so the cited section does not exist at the pinned head. The fix itself may still be right (one mobile-only block at ≤900px; overflow 0 at 390×844), but its stated root cause rests on a section that is not in the file. The lesson: a root-cause claim is a citation, and a citation must resolve — every cited file/section gets checked against the pinned SHA before the claim is accepted. A fix can be correct while its explanation is fictional; accepting the fictional explanation teaches the next seat a wrong mechanism, and the next fix built on it aims at a ghost. "Locked in as §8" was asserted in prose and never verified by reading the file back — that is the gap this note closes.

## 🩷 HUMAN NOTE

Someone fixed the phone screen and explained why it broke: "section 8 of the design guide made everything too big, and it spilled over." But section 8 isn't in the design guide — the guide stops at section 7, and sections 2 and 3 appear twice. The fix works, but the explanation points at a page that doesn't exist. If the next person believes the explanation, they'll go fix a ghost. The rule: before you repeat an explanation, open the book it cites and check the page is really there.

## 🟣 CHILD NOTE

Imagine you tell the teacher, "I know why the tower fell — page 8 of the instruction book says the blocks were too big." But the instruction book only has 7 pages, and pages 2 and 3 are printed twice. There is no page 8. Your tower might be fixed, but your reason is made up — and if your friend believes you, they'll go looking for a page that isn't there. Always open the book and check the page number first.

## 🔵 GRANDMA NOTE

Dear, the girl said the jam went bad because of the recipe on page 8 — but the recipe book only has 7 pages, and pages 2 and 3 are in there twice. The jam may be fixed, but the reason she gave points to a page that was never written. If the next cook believes her, she'll hunt for a page that doesn't exist and miss the real cause entirely. The rule in this house: if you cite a page, you open the book and put your finger on it first.

## 🟠 NAYA NOTE

I never accept a root-cause claim until I have resolved its citation at the pinned SHA — `git show <sha>:<path>` and grep for the section. A fix that works is not proof its explanation is true, and an explanation that cites a missing section is a story, not a mechanism. Here the "locked in as §8" claim was written down and then trusted downstream by two more notes, while the file itself ended at §7 with duplicated numbering. My rule: "locked in" means I read it back in the file at the pinned SHA; anything less is recorded as root-cause UNVERIFIED, never as proven.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "cited_root_cause_must_resolve_at_pinned_sha",
  "mechanism": "'locked in as <file> §N' is asserted in prose and never verified by reading the file back; downstream notes cite the asserted section as if it existed; the false anchor propagates because each seat trusts the previous seat's citation instead of the file",
  "evidence": "SN-2373 root-cause line (local copy verify_window_20261108_1402, 'Root cause: the §8 desktop enlargements (16.5px board type, 42px pill jewels) had cascaded into mobile'); SN-2370 'locked in as ANATOMY-OF-A-VIEWPORT.md §8'; first-hand this run: TEAM-NITRO/viewpoints/ANATOMY-OF-A-VIEWPORT.md at main tip 5756d0a8 has zero '§8' hits and headings 1,2,3,2,3,4,5,6,7 (no §8; §2/§3 duplicated); window-J verifier independently found §8 absent at c6263829 with no ANATOMY commit in window J (~/memory/2026-11-08.md)",
  "falsifiability": "git show <sha>:TEAM-NITRO/viewpoints/ANATOMY-OF-A-VIEWPORT.md | grep -c §8 -> 0 now; a future §8 landing flips it to 1 (the instance retires, the rule stands)",
  "decision_change": "a future verifier deciding whether to accept a root-cause claim first resolves every cited file/section at the pinned SHA; an unresolvable citation flips the verdict to 'fix accepted, root cause UNVERIFIED' instead of accepting the explanation",
  "applies_when": ["verification", "root-cause", "citation", "anchor", "pinned-sha"],
  "enforcement": "verification checklist step: resolve every cited file/section at the pinned SHA (git show <sha>:<path> | grep) before accepting a root-cause claim; 'locked in as <file> §N' claims verified by reading the file back at the pinned SHA; a claim with an unresolvable citation is recorded as root-cause UNVERIFIED, never as proven; the check belongs in the window-verification script, not in memory",
  "related": ["SN-2370 anatomy of a 10-star viewport", "SN-2373 mobile-stack one viewport", "SN-0206 frozen SHA judges anchor", "SN-1650 pin PR state before pinning head"]
}
~~~
