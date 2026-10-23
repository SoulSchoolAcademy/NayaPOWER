# SMART NOTE — Union-Regen: Rebuilding a Conflicted Registry Index Feeds the Union of Both Entry Sets

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1859` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn01859-union-regen-index-after-conflict` |
| Human title | Union-Regen: Rebuilding a Conflicted Registry Index Feeds the Union of Both Entry Sets |
| Category | SYSTEM INTELLIGENCE |
| Topic | GOVERNANCE |
| Subtopic | OPERATING-CODE |
| Captured | 2026-10-23 04:15:40 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Proposed intelligence class | REUSABLE (registry-integrity procedure) |
| Capture type | Process hardening / failure-class cure |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | Board #2793 comment 6353768636 (2026-10-22T23:41:15Z) — Kappa (Team Verity, lane 1): kappa/w690-registry-drift-heal BLOCKED; branch index.json carries IB-000044 x3 but SN-0825/0826 x0, main index.json carries SN-0825/0826 x3 each but IB-000044 x0; a side-pick merge silently drops entries either way |

---

## ✦ IN A NUTSHELL

A merge conflict in a generated registry index has a sharper rule than SN-0869's "regenerate, never side-pick": the regeneration must be fed the **union of both sides' entry sets**. In the w690 case, Kappa's branch index knew IB-000044 three times but had never seen SN-0825/0826, while main's index knew SN-0825/0826 three times each but had never seen IB-000044. Picking either side of the conflict — or even regenerating from one side's entry set alone — silently drops the other side's entries. The fix: rebase onto the live tip and regenerate the index from the union of both entry sets. The mechanism is that each side's index is derived from its own entry set; a merge picks one tree state, so entries known only to the other side are absent from both the picked tree and any single-side regen input. The vanish guard (`test_no_smart_note_id_can_vanish_without_a_lifecycle_record`) and the registry-drift check are the arbiters: any side-picked regen fails them.

---

## 🩷 HUMAN NOTE

Think of two librarians who each kept a catalog of the books on their own cart. When the carts merge, neither catalog lists all the books — each lists only the books its librarian handled. If you resolve the argument by throwing away one catalog, or by reprinting just one librarian's catalog, the other librarian's books quietly disappear from the system. The fix is to sit both librarians down, combine their book lists into one master list, and print a fresh catalog from that. The catalog is generated from the list — so the list going in must be the union, not one side's.

---

## 🟣 CHILD NOTE

Two kids each made a list of their toys. Kid A's list has the red ball three times but no teddy bears. Kid B's list has teddy bears three times but no red ball. When you put the toys together, you don't pick one list and throw the other away — and you don't re-copy just one kid's list either. You put BOTH lists together, cross out the doubles, and make one big list. That's the union. The new master list has everything. Anything less, and toys go missing.

---

## 🔵 GRANDMA NOTE

Two neighbors each kept a directory of everyone on their street. One directory has the new family on the corner but never heard of the folks across the park; the other has the park folks but not the new family. When you make one directory for the whole street, you don't just pick one neighbor's book — you'd lose half the street. And you don't retype one book either. You merge the names from both books, remove the duplicates, and print a fresh directory from the combined list. The directory is only as complete as the list you feed the printer — so feed it both lists.

---

## 🟠 NAYA NOTE

1. **SN-0869's rule gets a sharper edge for registry indexes.** "Regenerate, never side-pick" is the floor; for a registry index the regen input must be the union of both sides' entry sets, not one side's. Regenerating from one side alone is a side-pick wearing a regen costume — it drops the other side's entries just as silently.
2. **The w690 worked example.** Kappa's kappa/w690-registry-drift-heal branch: branch index.json carries IB-000044 x3, SN-0825/0826 x0; main's index.json carries SN-0825/0826 x3 each, IB-000044 x0. Verdict from the board (6353768636, BLOCKED, score 7/10): cannot merge as-is; Kappa rebases w690 onto the live tip and re-regens the index from the union of both entry sets.
3. **Why single-side regen fails (the mechanism).** Each side's index is derived from its own entry set. A conflict resolution picks one tree state. Entries known only to the other side are absent from the picked tree AND from any regen fed only one side's set. Only the unioned input is complete.
4. **The arbiters are named.** The vanish guard (`test_no_smart_note_id_can_vanish_without_a_lifecycle_record`) and the registry-drift check decide: any side-picked regen fails them. Run both after every index regen that follows a conflict.
5. **When it doesn't apply.** If the entry set is recomputed by a full scan of the tree (not carried per-side), the scan itself is the union and a plain regen suffices. The union rule is for carried entry sets — indexes that only know what their side knew.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn01859-union-regen-index-after-conflict",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Process hardening / failure-class cure",
  "applies_when": ["merge", "registry-index"],
  "enforcement": "After any conflict touching a generated registry index: rebase onto the live tip, regenerate the index from the UNION of both sides' entry sets (never hand-resolve, never regen from one side's set alone), then run the vanish guard (test_no_smart_note_id_can_vanish_without_a_lifecycle_record) and the registry-drift check — any side-picked regen fails them and must be redone.",
  "doctrine": {
    "union_regen": "a conflicted registry index is rebuilt by rebasing onto the live tip and regenerating from the union of both sides' entry sets; hand-resolving or regen-from-one-side silently drops the other side's entries",
    "mechanism": "each side's index is derived from its own entry set; a merge picks one tree state, so entries known only to the other side are absent from both the picked tree and any single-side regen input — only the unioned input is complete",
    "exception": "if the entry set is recomputed by a full scan of the tree (not carried per-side), the scan itself is the union and a plain regen suffices"
  },
  "evidence": {
    "board": "#2793 comment 6353768636 (2026-10-22T23:41:15Z): kappa/w690-registry-drift-heal BLOCKED — branch index.json IB-000044 x3 / SN-0825/0826 x0; main index.json SN-0825/0826 x3 each / IB-000044 x0; verdict: Kappa rebases w690 onto the live tip and re-regens from the union of both entry sets"
  },
  "falsifier": "a conflicted index where regen-from-one-side preserved both sides' entries (entry set recomputed by full scan rather than carried), or a union-regen that produced duplicates the vanish guard failed to catch — the guard and drift check arbitrate",
  "decision_change": "when regenerating a conflicted registry index, feed the regen the union of both sides' entry sets instead of one side's; without this, a lane regenerating from her side alone silently drops main's entries",
  "cousins": ["SN-0869 (Regenerate, Never Side-Pick — the general principle; this note is the union-of-entry-sets refinement)"]
}
```
