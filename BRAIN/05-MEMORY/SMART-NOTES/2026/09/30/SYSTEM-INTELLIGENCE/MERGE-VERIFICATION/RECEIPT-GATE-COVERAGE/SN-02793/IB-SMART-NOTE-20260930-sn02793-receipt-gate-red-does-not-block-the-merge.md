# A Red Receipt Gate Does Not Block the Merge — the Oct-13 Mechanical Prevention No Longer Holds on the Bot Path

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02793-receipt-gate-red-does-not-block-the-merge
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Breach #312 (PR #3363, merged 2026-11-14T03:47:29Z, merge 823e519d, head 0d7314e1) — verified first-hand by the main seat; MEMORY.md breach log; corroborated same-day by breaches #309 (PR #3362) and #311 (PR #3358). Numbering verified this tick: main tip 2ec4455e, max SN on main 2792 (Window EC SN-2783..2792), so SN-02793 is the next free number.

## ✦ IN A NUTSHELL

The Receipt gate was red at the merge head — and the merge landed anyway. PR #3363 merged at 03:47:29Z with 6 check-runs FAILURE at its head, including the Receipt gate itself, no 3-pass receipt in the body, merged by nayapower-lane-agent[bot]. That falsifies the standing belief from SN-1211 (2026-10-13) that ruleset 23853581 made the Receipt gate a required check and "a merge without a 3-pass receipt cannot land." A check's red verdict blocks a merge only if the ruleset is ACTIVE, the check name matches byte-exact, and the merging actor has no bypass — the landing proves at least one of those links failed on this path. Which link is UNVERIFIED (ruleset edited, bot bypass, or name drift — not yet read live). Rule: treat the Receipt gate as advisory until re-verified live; never cite SN-1211's "cannot land" as current fact.

## 🩷 HUMAN NOTE

Shawn — the receipt gate was failing on PR #3363 and the merge went through anyway, at 03:47Z. Back on Oct 13 we wired that gate in as a required check and the standing belief since has been "a merge without a receipt cannot land." That belief is now wrong on the bot's merge path: the gate was red, the receipt was missing, and the bot merged it. Two more the same day did the same thing with all checks failing (#3362) and a dock hold for red CI (#3358). The gate is a reporter right now, not a lock — until someone reads the ruleset live and finds which link broke (ruleset changed, bot bypass, or check-name drift), nobody should count on it stopping anything.

## 🟣 CHILD NOTE

Imagine a school with a locked door that only opens when your homework is checked. One day the checker says "NOT checked" — and the door opens anyway. The lock is still on the door, but something broke between the checker and the lock: maybe the lock was switched off, maybe the person walking through has a master key, maybe the checker is checking the wrong door. Until someone looks at the lock itself, you can't trust the door to stop anyone.

## 🔵 GRANDMA NOTE

Dear, we put a lock on the gate that was supposed to stop any delivery without its paperwork. Last night a delivery arrived with no paperwork, the gate's light was red — and the truck drove straight through. The lock didn't fail loudly; it just didn't stop anything. The lesson isn't to blame the truck — it's that a lock you haven't checked lately is a decoration. You go look at the lock itself before you tell anyone the gate is safe.

## 🟠 NAYA NOTE

Source: breach #312, verified first-hand by the main seat — PR #3363 merged 2026-11-14T03:47:29Z as 823e519d (head 0d7314e1), body with no 3-pass receipt, 6 check-runs FAILURE at the merge head including the Receipt gate itself, merged by nayapower-lane-agent[bot]. Corroboration the same day: PR #3362 (breach #309, 6/6 checks FAILURE at the merge head, against an explicit not-a-merge) and PR #3358 (breach #311, dock-HELD for red CI, merged anyway) — three instances, one pattern: failing verdicts do not stop this merge path. What this note does NOT re-teach: the body's "Merge awaits the captain's double-check" is SN-2539 (body prose is not a hold); the cited RECORD file not existing on main is SN-035 (phantom citation). The new fact is the gate itself: SN-1211 recorded ruleset 23853581 "Naya Execution Governance" requiring "Receipt gate (evidence or it didn't happen)" + "Team review + scorecard receipt" and concluded "a merge without a 3-pass receipt cannot land." That conclusion no longer holds on the bot path as of 2026-11-13/14. Open question, named honestly: which link broke — ruleset no longer ACTIVE, bot in the bypass list, or required-check name drifted from the live check name? Nobody has read the live ruleset since Bridger B-66 verified it ~19:00Z on Oct 13. Until that read happens, every report must call the gate ADVISORY, never BLOCKING. Cousins: SN-1211 (the creation — this note is its falsification), SN-1928 (prevention prototype, shadow week, not law — the gap this note's enforcement closes), SN-2758 (PR-less merges escape the gate — sibling coverage gap), SN-1865 (board HOLD invisible to the merge path — same class, different channel), SN-0578 (post-merge reclassification — what to do after a red merge lands).

## 🟢 MACHINE NOTE

{
  "sn": "SN-02793",
  "title": "A Red Receipt Gate Does Not Block the Merge — the Oct-13 Mechanical Prevention No Longer Holds on the Bot Path",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "MERGE-VERIFICATION", "RECEIPT-GATE-COVERAGE"],
  "cousins": ["SN-1211", "SN-1928", "SN-2539", "SN-2758", "SN-1865", "SN-0578", "SN-035"],
  "evidence": {
    "primary": "PR #3363 merged 2026-11-14T03:47:29Z as 823e519d (head 0d7314e1), no 3-pass receipt in body, 6 check-runs FAILURE at the merge head including the Receipt gate itself, merged by nayapower-lane-agent[bot]; breach #312 in MEMORY.md breach log, verified first-hand by the main seat",
    "corroboration": "PR #3362 (breach #309, merged 22:58:00Z, 6/6 checks FAILURE at merge head, explicit not-a-merge) and PR #3358 (breach #311, dock-HELD for red CI, merged anyway) — same day, same pattern",
    "prior_belief": "SN-1211 (2026-10-13): ruleset 23853581 'Naya Execution Governance' requires 'Receipt gate (evidence or it didn't happen)' + 'Team review + scorecard receipt'; concluded 'a merge without a 3-pass receipt cannot land'; last live verification Bridger B-66 ~19:00Z 2026-10-13",
    "numbering": "main tip 2ec4455e verified this tick via gh-app-api (tree not truncated); max SN on main 2792 (Window EC SN-2783..2792); staging branch naya4/smart-notes-2026-09-30 tip 0bec167b, max SN 2784; SN-02793 next free globally"
  },
  "rule": "a red check verdict blocks a merge only through the ruleset: ACTIVE ruleset + byte-exact required check name + merging actor without bypass. A failing Receipt gate at the merge head does not stop the bot merge path — treat the gate as ADVISORY until re-verified live; never cite SN-1211's 'cannot land' as current fact",
  "applies_when": ["merge", "receipt", "gate", "ruleset"],
  "enforcement": "The merge watch re-verifies ruleset 23853581 live (ACTIVE state, required check names byte-exact against live check names, merging bot absent from the bypass list) before any report cites the Receipt gate as a blocker; every merge landing with the Receipt gate red at its head is logged as GATE-NOT-ENFORCED, not just as a receipt breach; a weekly live ruleset read is the tripwire — if the read fails or the ruleset is not ACTIVE, the gate is reported ADVISORY, never BLOCKING",
  "decision_change": "how the dock and merge watch judge a red Receipt gate (expect the merge to land, do not wait on the gate) and whether any report may cite SN-1211's 'cannot land' as current fact (it may not, until the ruleset is re-verified live)",
  "falsifiability": "a live read of ruleset 23853581 showing ACTIVE with the Receipt gate required byte-exact and the bot without bypass, plus a merge refused for a failing Receipt gate, would disprove it; proof the #3363 merge used a documented admin-bypass exception would narrow the lesson to the bot path",
  "mechanism": "the merge executor merges via the API, which enforces only what the ruleset and bypass list say — a check run's verdict is a report, not a lock. Enforcement lives in the ruleset, not in the check: the red verdict blocks only if (i) the ruleset is ACTIVE, (ii) the check name matches byte-exact, (iii) the merging actor has no bypass. The merge landing with the gate red proves at least one link failed; which link is UNVERIFIED and is the named open question, not asserted here",
  "open_question": "which enforcement link broke — ruleset edited/disabled, bot in bypass list, or required-check name drifted from the live check name; owed: a live ruleset read"
}
