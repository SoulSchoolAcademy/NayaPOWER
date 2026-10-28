# Hygiene That Nulls Owners Is Integrity Loss, Not a Clean Pass — Never Re-Write Unilaterally

**Intelligent Block:** IB-SMART-NOTE-20261028-sn2037-hygiene-owner-loss-no-unilateral-rewrite  
**Smart Note:** SN-2037  
**Truth state:** CANDIDATE  
**Scope:** PRIVATE  
**Captured:** 2026-10-28  
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A hygiene pass that leaves content intact while nulling every owner is not a clean pass: on 2026-10-28, a second live re-read found owner_seat NULL on all 13 hygiene keys in work_items a554e536 (gap-d33–d44/d46) while 20 of 21 next_actions survived longer than their pre-hygiene lengths — selective owner nulling after verified application, not a full revert. Because owner_seat is the only attribution for those keys and updated_at does not move on these writes, the loss window cannot be bounded. Recovery is therefore a three-seat decision — confirm the gap-d43 mapping, name the pass that writes owner_seat, then re-apply exactly the 13 owners plus the gap-d28 text — never a unilateral re-write.

## 🩷 HUMAN NOTE

Hygiene is supposed to tidy things up without breaking them. This time the tidying looked successful: the actual work items survived, most of them longer than before. But every single owner label was gone — 13 keys, all ownerless. Without an owner, nobody can tell who was responsible for what, and because the system does not stamp a new time on these writes, nobody can tell when the labels vanished either. That is why the fix cannot be one person quietly typing the owners back in: a solo re-write would destroy the very evidence needed to understand what happened. The owners come back only after three seats agree, the key mapping is confirmed, and the pass that writes owners is named.

## 🟣 CHILD NOTE

Imagine a teacher tidies the classroom: all the homework is still there, even neater than before — but every name has been erased from the top of every page. The work survived, but nobody knows whose work is whose. And because nobody wrote down when the tidying happened, you cannot even figure out which tidy-up did it. The rule from now on: do not just write the names back yourself. First agree with others on which page belongs to whom, figure out which tidy-up erased the names, and only then put the names back together.

## 🔵 GRANDMA NOTE

Think of it like a filing cabinet that gets reorganized: all the folders are still there, fuller than before — but the labels on 13 folders have been peeled off. The contents are fine, yet the cabinet is broken in a quieter way: you no longer know who each folder belongs to, and there is no date stamp to say when the labels came off. The lesson is about how to repair that kind of damage: not by one person relabeling folders on their own, which would hide what went wrong, but by first confirming which folder is which, finding out what removed the labels, and then relabeling together, with witnesses.

## 🟠 NAYA NOTE

This is a failure-mode lesson about silent attribution loss, distinct from a content revert. The content survived — that is precisely what makes the loss dangerous: a pass that checks only content survival reads as clean while provenance is destroyed.

Decision this changes: when owner loss is found after a hygiene pass, the next move is never a unilateral re-write. The recovery order is fixed: (1) confirm the gap-d43 mapping for the affected keys, (2) name the pass that writes owner_seat, (3) take a three-seat decision to re-apply exactly that set — the 13 owners plus the gap-d28 recovered text (gap-d28 still sat at its pre-hygiene length of 312). Any future hygiene pass must also include an owner_seat non-null census in its post-pass verification, so this class of loss is caught by the pass itself instead of by a later re-read.

What would prove it wrong: a re-read showing the owners were already NULL before the hygiene pass, a gap-d43 mapping showing the 13 keys never carried those owners, or logs from a named pass showing owner_seat untouched — any of these would reclassify this from hygiene-caused loss to a pre-existing gap, and the recovery order would change with it.

Mechanism: owner_seat is the sole attribution on hygiene keys, so nulling it destroys provenance while content survives and the pass looks clean; and updated_at does not move on these writes, removing the temporal forensics that would bound the loss window — the same blind spot as the earlier notes-array loss. The pass that performed the nulling itself is still UNKNOWN; this note records the loss pattern and the recovery protocol, not a claimed root cause.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "knowledge_creates_authority": false,
  "applies_when": ["hygiene", "owner-attribution", "work-items", "recovery"],
  "enforcement": "A hygiene pass's post-pass verification must include an owner_seat non-null census over all hygiene keys, and any owner re-apply requires a confirmed gap-d43 mapping, a named owner_seat-writing pass, and a recorded three-seat decision before any write; a unilateral owner re-write is a violation of this note.",
  "evidence": "Director snapshot 2026-10-28 05:08 PDT (2026-10-28T12:08Z), live board #3066 comment 6468032525 (Power, second live re-read): owner_seat NULL on all 13 hygiene keys in work_items a554e536 (gap-d33-d44/d46) while 20/21 next_actions survived longer than pre-hygiene lengths; gap-d28 still at pre-hygiene 312; recorded in shared-state as named failure mode HYGIENE-OWNER-LOSS (2026-10-28T11:40Z). Cause of the nulling UNKNOWN; updated_at blind spot same as notes-array loss.",
  "decision_change": "On hygiene owner loss, do not re-write unilaterally: confirm the gap-d43 mapping, name the owner_seat-writing pass, then re-apply exactly the 13 owners plus gap-d28 text under a three-seat decision; future hygiene passes must census owner_seat non-null post-pass.",
  "falsifier": "Owners already NULL before the hygiene pass, a gap-d43 mapping showing the 13 keys never carried those owners, or named-pass logs showing owner_seat untouched would reclassify this as a pre-existing gap, not hygiene-caused loss.",
  "mechanism": "owner_seat is the sole attribution on hygiene keys, so nulling it destroys provenance while content survives and the pass looks clean; updated_at does not move on these writes, removing temporal forensics that would bound the loss window."
}
```
