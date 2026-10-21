# Never-Registered Is Not Deleted — A Deletion Claim Must Survive Two Byte Tests Before a Ruling Accepts It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01756-never-registered-is-not-deleted
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

PR #2839 claimed five smart-note registry entries were "dropped without lifecycle record" — a deletion story. The main-seat adjudication (board 6312255661, 2026-10-21) voided it on live bytes, not on narrative: the cited tip commit 895d7361 touched exactly one file (HUB/MAP-STATE.json) — it never touched the registry — and the five IDs were already absent at the pre-cure base per #2831's VERIFY control (6310156804). The coherent story was direct-push debt (never registered), not deletion. The two-byte test every deletion/absence claim must survive: (1) the tip commit's touched-file list — did any commit actually touch the registry? (2) the pre-cure-base absence control — were the entries present before the cure window? Fail either, and the deletion story fails. A claim that cites no live bytes is VOID before it can hold a merge. SN-1757 (competing cures) is the same incident's second lesson.

## 🩷 HUMAN NOTE

Shawn — today a "five entries deleted without a trace" claim almost held a merge hostage. The truth was duller: those entries were never registered in the first place — direct pushes had skipped the registry pipeline. The rule I filed: nobody gets to say "deleted" until they show two byte-level facts — which commit touched the registry file, and whether the entries existed before the cure window. Both answers tonight said no. The claim was void; the right cure (#2831) kept its path. No drama, just the bytes deciding.

## 🟣 CHILD NOTE

Imagine someone says "my homework vanished from the teacher's folder!" Before anyone searches the school, two questions: did anyone's hands actually open that folder today — and was the homework ever put in the folder at all? If nobody opened the folder, and the homework was never turned in, then nothing vanished — it was never there. That's the rule: "deleted" needs proof of a hand on the folder AND proof the thing was inside. Without both, the story doesn't count.

## 🔵 GRANDMA NOTE

Like a recipe box. Your neighbor swears five recipe cards were stolen from your box. Before you call anyone, check two things: did anyone open the box lately (the box lid shows one file was touched, and it wasn't the recipes), and were those five cards ever written down at all (the older copy of the box never had them). If no hand opened the box and the cards were never written, nothing was stolen — they were never made. Always count what's in the box first; a loud story is not evidence.

## 🟠 NAYA NOTE

Lane discipline: when a claim says entries were dropped/deleted from the registry, do not adjudicate the narrative — run the two-byte test first. Byte test 1: `git show --name-only <tip>` (or the tip commit's touched-file list via API) — did any commit in the claim's window touch the registry file at all? Byte test 2: the pre-cure-base control — check the registry at the base before the cure window; entries already absent there = never-registered, i.e. direct-push debt, not deletion. Both tests are already proven on record: #2831's VERIFY control (6310156804) gave test 2, the adjudication (6312255661) gave test 1. A claim that names neither byte is VOID pre-ruling — route it back for the bytes before any HOLD can attach to a competing cure. The ruling that held #2839 cited both bytes and named direct-push debt as the coherent story; copy that shape.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1756",
  "title": "Never-registered is not deleted — deletion claims must survive two byte tests",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "applies_when": [
    ["adjudication", "registry"],
    ["verify", "deletion-claim"],
    ["merge", "hold-decision"],
    ["dock", "cure-routing"]
  ],
  "enforcement": "Every ruling on a deletion/absence claim must cite (1) the tip commit's touched-file list for the claim window and (2) the pre-cure-base absence control; a claim citing no live bytes is VOID pre-ruling and no HOLD attaches to any competing cure until both bytes are named. The named check is the 'deletion-claim two-byte test': tip file list + pre-base absence.",
  "evidence": {
    "adjudication": "#2793 comment 6312255661 (2026-10-21): #2839 HELD, deletion claim VOID on live bytes; tip 895d7361 touched exactly one file (HUB/MAP-STATE.json); five IDs absent at pre-compiler base per #2831 VERIFY control",
    "control": "#2793 comment 6310156804 (#2831 VERIFY receipt: base 895d7361 = 5 failed/26 passed, the exact claimed set; entries absent before cure window)",
    "divergence": "#2793 comment 6312255918 (#2839 VERIFY receipt: CURE REAL 9.5, content-divergent from #2831)"
  },
  "decision_change": "Future adjudicator faced with a 'registry entries dropped without lifecycle record' claim runs the two-byte test before routing: tip-file-list + pre-cure-base absence. This changes HELD-vs-merge decisions — a void claim cannot hold a cure PR.",
  "falsifier": "A deletion claim that PASSES both byte tests (tip commit DID touch the registry file AND entries WERE present at the pre-cure base) is a real deletion — the rule admits this outcome. The principle is wrong only if real deletions routinely evade both tests.",
  "mechanism": "The tip commit's file list is the ground truth of what changed in that commit; absence at the pre-cure base proves the entries never existed in the registered lineage. Direct pushes bypass the registry pipeline, so unregistered entries are debt, not victims — and the bytes distinguish the two deterministically.",
  "related": ["SN-1757 (competing cures content fork — same incident)", "SN-0176 (cross-partition content fork — ID-level collision)", "SN-0406/SN-0408 (deletion discipline for ratified captures — different principle: disposal, not adjudication)"]
}
```
