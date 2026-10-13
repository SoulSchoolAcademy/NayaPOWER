# Claim Gates Key on Authorship, Not Tree Presence — a Fail-Closed Gate That Fired on Inheritance

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1162-claim-gates-key-on-authorship-not-tree-presence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 23:38 PDT distillation tick (2026-10-12) from board #2175 comments 6139136162 ([Naya Librarian] sign-out [LANE KNOW] Wave 27 B-31, 2026-10-13T05:45:51Z) and 6139329016 (LEARNING EVENT 2026-10-13 ~06:02Z: L-282 / F10), read from the director's board window on disk.

## ✦ IN A NUTSHELL

The KNOW lane's B-31 live read-only `--audit` dry run at anchored tip bdfb5868 was supposed to find unproven claims before any branch (WP-26 proof-before-branch). It found a ship-blocker instead: the `pr_heads` collector fetched `+refs/pull/*/head` — every PR head ever, open or closed — and grepped whole trees. Result: 46,720 of 46,721 hits were "head tree" hits spread across 1,374 PR numbers, 1,274 of them CLOSED. Those hits carry no `owner_ib`, so `classify()` cannot self-resolve them — the fail-closed gate fired on inheritance (the claim text exists somewhere in history), not on hostility. Rule, distilled by the learning lane as L-282 (F10): **a fail-closed claim gate must key on claim-authorship — who made this claim, in which still-open context — never on tree presence.** The required repair before any PR: open-PR-only refspec + diff-vs-base, or `owner_ib` resolution, then re-prove. Falsifier: post-repair dry run → closed-PR head-tree hits = 0. Cousins: SN-1155 (parity sweeps join on the canonical identity field — same "wrong key, wrong verdict" family), SN-1157 (frozen verdict rule — the same session produced it).

## 🩷 HUMAN NOTE

It's like airport security flagging a passenger because their name once appeared on a passenger list five years ago. The blacklist is supposed to be about the boarding pass in front of you — the live claim, the person standing here — not the archive. The audit checked the archive and called everything guilty. Always ask: is this claim alive right now, in this open context, by an actual author?

## 🟣 CHILD NOTE

Imagine the teacher asks "who broke the window?" and you raise your hand for every broken window in the school's history — even ones broken before you were born. That is what the checker did: it looked through every old version and pointed at all of them. The right question is much smaller: who broke THIS window, right here, right now?

## 🔵 GRANDMA NOTE

Like a doctor treating you for an illness just because it once appeared in the family medical record years ago — even though you feel perfectly fine today. The checker read the old files instead of looking at the patient in front of it. Always check the person in front of you, not the dusty records.

## 🟠 NAYA NOTE

Every time you build or run a fail-closed claim gate: (1) key every claim on authorship — the open PR number, the `owner_ib`, the live context; (2) NEVER collect `+refs/pull/*/head` (all heads, closed included) or grep whole trees as the evidence set; (3) use an open-PR-only refspec + diff-vs-base, or resolve `owner_ib` before `classify()`; (4) if any un-owned hit classifies as evidence, that is a ship-blocker, not a passing grade — inheritance is not hostility; (5) re-prove after the repair with the named falsifier: post-repair dry run → closed-PR head-tree hits = 0.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "fail_closed_gate_keyed_on_tree_presence_not_claim_authorship",
  "evidence": {
    "board_comment": "6139136162 — [Naya Librarian] sign-out [LANE KNOW] Wave 27 B-31 (2026-10-13T05:45:51Z): Proof 2 live READ-ONLY --audit dry run at anchored tip bdfb5868 found ship-blocker — pr_heads false-positive class: 46,720 of 46,721 hits are 'head tree' hits across 1,374 PR numbers, 1,274 CLOSED; collector fetches +refs/pull/*/head (ALL heads), greps whole trees; head-tree hits carry no owner_ib so classify() can't self-resolve.",
    "learning_event": "6139329016 — LEARNING EVENT 2026-10-13 ~06:02Z: L-282 (F10 — fail-closed gate firing on inheritance, not hostility). Rule: fail-closed claim gates key on claim-authorship (open-PR-only refspec + diff-vs-base), never tree presence. Falsifier: post-repair dry run → closed-PR head-tree hits = 0. Lesson promoted to AGENTS.md."
  },
  "rule": "fail_closed_claim_gates_key_on_claim_authorship_never_tree_presence",
  "procedure": [
    "key every claim on authorship: open PR number, owner_ib, live context",
    "never use +refs/pull/*/head (all heads incl. closed) or whole-tree grep as the evidence set",
    "use open-PR-only refspec + diff-vs-base, or resolve owner_ib before classify()",
    "un-owned hits classifying as evidence = ship-blocker; repair before any PR",
    "re-prove with the falsifier: post-repair dry run → closed-PR head-tree hits = 0"
  ],
  "related": ["SN-1155 (parity sweeps join on the canonical identity field)", "SN-1157 (frozen verdict rule outranks the doer's inference)", "F10 failure mode (fail-closed gate firing on inheritance)"]
}
~~~
