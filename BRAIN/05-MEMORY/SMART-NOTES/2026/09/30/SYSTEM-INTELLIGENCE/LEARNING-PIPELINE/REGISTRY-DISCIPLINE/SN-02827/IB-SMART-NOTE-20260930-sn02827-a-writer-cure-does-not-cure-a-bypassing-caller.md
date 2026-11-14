# A Writer Cure Does Not Cure a Caller That Bypasses the Writer — LIVE-LOOP-BYPASS

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02827-a-writer-cure-does-not-cure-a-bypassing-caller
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Director tick 2026-11-14 21:08Z (shared-state direct_push_1072_20261114); DP-1072 commit f70a10f6; board #3352 comment 6884213260; learning-events 2026-11-14-13.md; Daily Intelligence 2026-11-14 (SN-2826).

## ✦ IN A NUTSHELL

The P-152 writer cure landed in learning_loop.py (DP-1072, f70a10f6, 21:06:43Z): publish-note now registers in the same motion. But the live Intelligence Loop bot still files its pages by direct commit — it never calls the writer — so the registry still does not advance for its pages. A writer cure constrains only the callers that use the writer. Until every live caller is routed through the cured writer, the leak is partial-cured, not cured — and declaring it closed on the writer fix alone repeats the error. New failure mode LIVE-LOOP-BYPASS, named by the director 21:08Z; backfill of ~127 bot-filed pages still owed (PR #3354).

## 🩷 HUMAN NOTE

Shawn — imagine the mailroom finally gets its logbook rule: every letter logged the moment it arrives. But one courier still walks in the back door and drops letters straight on the shelves, never passing the front desk. The book stays empty for his letters, and anyone checking the book concludes they never arrived. The front-desk rule was real and right — it just doesn't reach the courier who never comes to the desk. That's this lesson: fixing the writer fixed the front desk; the live loop bot is the back-door courier. Until his path goes through the desk, the leak lives on.

## 🟣 CHILD NOTE

Imagine your teacher says "write down every picture in the notebook when you pin it up" — and you do. But your friend keeps pinning pictures on the wall without ever telling you, so the notebook still misses hers. The rule works for everyone who follows it. The fix isn't a better rule — it's making sure your friend's pictures go through the notebook too. A rule only works for the people who actually use it.

## 🔵 GRANDMA NOTE

Dear, it's like fixing the recipe box so every new card gets filed under its letter the moment it arrives — a good fix, and it works. But your grandson keeps tucking his cards straight into the drawer, never handing them to you to file. The box is fixed; his cards still aren't in the index. The filing habit has to reach every hand that touches the box, or the index stays wrong. Fix the box, and then bring every hand to it.

## 🟠 NAYA NOTE

Evidence, first-hand from the record: DP-1072 (commit f70a10f6, nayanet[bot], 2026-11-14T21:06:43Z, single parent of 74579352): tools/learning_loop.py +97/-0, "fix(learning-loop): the publish door — publish-note registers in the same motion (P-152)" — the exact writer cure SN-2823 / CANDIDATE 1062 prescribed, filed 12:20, enforced in code 13:06, ~46 minutes. Maker triple-check recorded in board #3352 comment 6884213260 (suite 28/2 env-only failures; dry-run publish 0 defects; round-trip byte-identical d09110c9). The same director tick (21:08Z) that verified the cure named the residual gap outright: the live Intelligence Loop bot still files pages by direct commit (proof 5620554c15) — NEW failure mode LIVE-LOOP-BYPASS; backfill ~127 pages (PR #3354) still owed. Delivery caveat: the cure itself landed as a direct push — code to main with no PR and no 3-pass receipt; dock adjudication owed. Cousin map: SN-2823 (cure the writer, not the backlog — the writer cure this note completes: the writer is fixed, the caller is not); SN-0491 (direct commit owes pipeline paperwork — the bot's pages owe registry entries; this note is about the cure-completeness judgment, SN-0491 about the paperwork owed after a bypass landing); SN-1887 (a post-landing binding check is a detector, not a gate — likewise, a writer fix is a cure for its callers, not a cure for the system).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "a_writer_cure_does_not_cure_a_caller_that_bypasses_the_writer",
  "mechanism": "the P-152 cure lives in the writer (learning_loop.py publish-note registers in the same motion), so it executes only for callers that invoke the writer. The live Intelligence Loop bot files pages by direct git commit and never calls the writer, so its pages land with no registry entry and the registry does not advance for them. Registry advance depends on the call path, not only on the writer's code: a cured writer plus a bypassing caller is still a leak",
  "evidence": "DP-1072 f70a10f6 (nayanet[bot], 2026-11-14T21:06:43Z, single parent of 74579352): tools/learning_loop.py +97/-0, publish-note door over canonical writer smart_note_v2.py; maker triple-check in board #3352 comment 6884213260 (suite 28/2 env-only; dry-run publish 0 defects; round-trip byte-identical d09110c9). Director tick 2026-11-14 21:08Z (shared-state direct_push_1072_20261114): live Intelligence Loop bot still files pages by direct commit (proof 5620554c15) — NEW failure mode LIVE-LOOP-BYPASS; backfill ~127 pages (PR #3354) still owed; cure landed as direct push, no PR, dock adjudication owed",
  "falsifiability": "if the loop bot is shown to file a page whose registry entry hashes to it (bot routed through publish-note), or the bot is shown to call learning_loop.py's publish path, the bypass is closed and the rule's live instance fails",
  "decision_change": "a future seat declaring a writer-cure complete first enumerates every live caller of the write path (starting with the Intelligence Loop bot) and verifies each routes through the cured writer; the leak item stays open while any caller still files by direct commit, and is closed on a probe page filed by the caller showing a registry entry hashing to it — never on the writer fix alone",
  "applies_when": ["learn", "registry", "writer-cure"],
  "enforcement": "before closing a writer-cure item, run a probe capture through every live caller of the write path (starting with the Intelligence Loop bot) and verify the registry advances for each (registry entry hashes to the probe page); the direct-push watch flags any main commit by the loop bot touching BRAIN/05-MEMORY/SMART-NOTES without a matching registry entry — while any such commit exists, the item stays open and the caller must be routed through publish-note",
  "related": ["SN-2823 cure-the-writer-not-the-backlog — the writer cure this note completes (writer fixed, caller not)", "SN-0491 direct-commit-capture-bypass — the bot's pages owe registry entries; this note is the cure-completeness judgment, SN-0491 the paperwork owed", "SN-1887 post-landing-binding-check-is-a-detector-not-a-gate — a writer fix cures its callers, not the system"]
}
~~~
