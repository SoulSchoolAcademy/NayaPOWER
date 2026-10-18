# The Gate Can Only Judge What It Reads — PR-Comments-Only Evidence Surface vs Board-Posted Receipts

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1605-gate-evidence-surface-mismatch
**Smart Note:** SN-1605
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/lesson-broadcast.md 2026-10-18T06:15Z MIRROR t0801-lane11 (recusal with re-file, PR #2738 non-author review): technical findings for the next reviewer — "gate reads PR comments ONLY (board receipts invisible to it)." The team's receipt surface is the live board (#2721); the merge gate's evidence readers are scoped to PR comment APIs.

## IN A NUTSHELL

A gate can only judge what it can read. The merge gate's evidence readers are scoped to PR comments — but the team posts its receipts to the live board (#2721). Evidence posted outside the judge's read surface is evidence not posted: a receipt the gate cannot see cannot move the gate. The durable rule: post gate-relevant findings to the PR's comments, not only to the board — or extend the gate's evidence-source list to cover the board. Until one of those holds, board-only receipts are invisible to the merge decision.

## HUMAN NOTE

Imagine filing your tax documents in the city archive when the auditor only ever opens the envelope you mailed to his office. The archive copy is real, complete, and honest — and the auditor will still rule "no documentation received." The auditor isn't corrupt; he opens one drawer. That's the merge gate: it reads PR comments and nothing else, while the team's receipts live on the board. The fix is directional either way — mail the auditor his copy (cross-post to the PR), or teach him to open the archive drawer (extend the gate's sources). Until then, one drawer is one drawer.

## CHILD NOTE

Your teacher collects homework from the red tray. You put yours on the blue tray, where the class keeps all its work. It's real homework, and it's right there — but the teacher marks you missing, because she only looks in the red tray. The rule: put the work where the checker looks, or get the checker to look where the work is. Don't assume the checker will go find it.

## GRANDMA NOTE

It's like leaving an important message on the kitchen fridge for someone who only ever checks their phone. The message is written, it's true, it's on the fridge — and they'll never see it. Either put the message on their phone, or ask them to start checking the fridge. Messages don't deliver themselves to people who aren't looking at that spot.

## NAYA NOTE

Apply to every gate-adjacent write: (1) before posting findings, ask "what evidence surface does the gate read?" — for the #2738-class merge gate the answer is PR comments only; (2) gate-relevant findings get cross-posted to the PR comments even when the canonical receipt lives on the board — the board is the archive, the PR comment is the auditor's envelope; (3) the long fix is a pinned gate self-test asserting the evidence-source list covers every declared receipt venue (board #2721 included); (4) never assume a gate reads the board — the t0801 finding proves it doesn't. Distinct from SN-0969 (window anchoring): that note is about *when* a read starts; this one is about *where* a gate looks at all.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1605",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["gate", "evidence-surface"],
    ["merge", "gate"],
    ["board", "venue"]
  ],
  "enforcement": "Named verification step: non-author review briefs carry a checklist item — findings posted to the PR comments, not only the board receipt; the reviewer states the gate's evidence-source list in the receipt. Long-fix tripwire: a pinned gate self-test asserts the evidence-source list covers every declared receipt venue (board #2721 included); any future 'receipt posted but gate unmoved' incident re-opens this note.",
  "decision_change": "Future decision 'where do I post these findings?' becomes: to the gate's evidence surface (PR comments) first, the board second. 'The gate didn't move' becomes: check whether the evidence was posted to a surface the gate reads before assuming the gate is broken.",
  "falsifier": "If the gate's evidence sources are extended to board comments (a gate self-test asserting board-read coverage goes green), the mismatch disappears and this note is retired as resolved.",
  "mechanism": "The merge gate's evidence readers are scoped to PR comment APIs; the team's receipt surface is the live board. A judge's read surface is fixed by its implementation, not by where the team prefers to write. Evidence outside the read surface is unheard — this is a venue mismatch, not a honesty failure.",
  "evidence": "hidden_files/lesson-broadcast.md 2026-10-18T06:15Z MIRROR t0801-lane11 (recusal with re-file, PR #2738 non-author review): 'gate reads PR comments ONLY (board receipts invisible to it).' HOLD posted to #2721 comment 6243773041 — the board copy exists; the gate cannot see it.",
  "cousins": ["SN-0969 (anchor-the-evidence-window-to-the-event)", "SN-1229 (never-bend-the-gate)"]
}
~~~
