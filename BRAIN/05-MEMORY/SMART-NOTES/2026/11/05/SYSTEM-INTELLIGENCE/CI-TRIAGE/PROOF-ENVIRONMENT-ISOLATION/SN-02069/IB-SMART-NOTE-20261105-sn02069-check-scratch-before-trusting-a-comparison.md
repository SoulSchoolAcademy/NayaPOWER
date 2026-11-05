# INTELLIGENT BLOCK — SN-2069

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02069-check-scratch-before-trusting-a-comparison
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Distill-daily 2026-11-03 (distill-daily-20261103.md, mirror lesson); surfaced by the daily learning review 2026-11-05 13:20 PST (learning-events-2026-11-05-13.md, CANDIDATE 1011). Distinct from SN-0341 (harness scratch off tmpfs — scratch-dir placement) and SN-0970 (tmp commons orphan scratch remediation) — this is the empty-diff trust rule.

## ✦ IN A NUTSHELL

Check the scratch disk before trusting a comparison; never let an empty diff pass as "no change." A full /tmp (512M tmpfs) starved the verification clone, produced empty comparison files, and the first attempt nearly reported empties as results; the seat re-ran the clone under the goal workspace (114G free) and proved the mission-state drift exactly — a 171-line diff, main 23 lines vs branch 148 lines, SHAs 65382e11… vs 27bebcdb…. The durable rule: **evidence is a SHA from a clone that actually finished, not an exit code from a command that starved.**

## 🩷 HUMAN NOTE

Shawn — a verification run compared two versions of the mission state and got back empty files, which looks exactly like "no change." But the scratch disk was full, so the clone that was supposed to do the comparing never finished — the empties were the failure, not the answer. The seat caught it, re-ran on a disk with room, and found a real 171-line drift hiding behind the empty files. From now on, every verification run checks the scratch disk first, and a "no change" verdict has to come with the finished clone's fingerprint — never just an exit code and empty hands.

## 🟣 CHILD NOTE

Imagine you ask a friend to compare two big picture books and tell you if they're the same — but your friend's desk is so full of stuff that she can't even open the books, so she hands you two blank pages. Blank pages don't mean the books match; they mean she never got to look. The new rule: before you ask her to compare, check her desk has room — and only believe "they're the same" when she shows you the books she actually finished comparing.

## 🔵 GRANDMA NOTE

Dear, it's like asking someone to check whether two recipes match, but their kitchen counter is piled so high they can't lay the cards out — so they hand you back two blank cards. Blank cards don't mean the recipes are the same; they mean the cook never got to read them. From now on, we clear the counter first, and we only believe "no difference" when the cook shows us the cards she actually finished reading, side by side.

## 🟠 NAYA NOTE

For every seat that runs a verification comparison: check scratch space before trusting the result. A starved clone fails partway and leaves empty or partial comparison files — an empty diff is then an artifact of the failure, not evidence of no change. Preflight: df the scratch path before cloning; if it is full (here: 512M tmpfs /tmp), move the clone to a path with room (here: the goal workspace, 114G free) and re-run. A "no change" verdict must cite the finished clone's SHA; a receipt whose comparison files are empty without a completed-clone SHA is rejected by the claim/verify check. The exit code alone never proves the comparison ran.

## 🟢 MACHINE NOTE

```json
{
  "slug": "check-scratch-before-trusting-a-comparison",
  "sn": "SN-2069",
  "title": "Check the Scratch Disk Before Trusting a Comparison",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["verification", "proof"],
  "enforcement": "Verification-run preflight checks scratch space (df on the clone path) before cloning; the verification receipt cites the finished clone's SHA, and a receipt whose comparison files are empty without a completed-clone SHA is rejected by the claim/verify check.",
  "falsifier": "Proven wrong for a given run if an empty diff is reproduced with ample scratch and a clone that completed (SHA on record) — then the emptiness is a true no-change verdict, not starvation.",
  "decision_changed": "How verification runs prove no-change: check scratch space before cloning and cite the finished clone's SHA; an empty diff without a completed clone is re-run, never reported.",
  "mechanism": "A starved clone fails partway and leaves empty or partial outputs; the empty comparison file is then an artifact of the failure, not evidence of no change. The exit code alone does not distinguish 'compared and found identical' from 'never finished comparing' — only the completed clone's SHA proves the comparison ran.",
  "provenance": "Distill-daily 2026-11-03 (distill-daily-20261103.md, mirror lesson): a full /tmp (512M tmpfs) starved the verification clone, produced empty comparison files, and the first attempt nearly reported empties as results; re-run under the goal workspace (114G free) proved the mission-state drift exactly (171-line diff, main 23 lines vs branch 148 lines, SHAs 65382e11… vs 27bebcdb…). Surfaced by daily learning review 2026-11-05 13:20 PST (learning-events-2026-11-05-13.md, CANDIDATE 1011). Distinct from SN-0341 (harness scratch off tmpfs) and SN-0970 (tmp commons orphan scratch remediation)."
}
```
