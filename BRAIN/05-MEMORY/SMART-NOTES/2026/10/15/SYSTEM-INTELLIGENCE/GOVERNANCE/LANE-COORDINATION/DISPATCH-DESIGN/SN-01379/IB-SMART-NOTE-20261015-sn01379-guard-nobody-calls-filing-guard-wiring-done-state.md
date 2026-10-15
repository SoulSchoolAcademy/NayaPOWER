# A Guard Nobody Calls Is a Verdict with Better Formatting — the Done-State of a Filing Guard Is "the Filing Step Cannot Bypass the Tool"

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01379-guard-nobody-calls-filing-guard-wiring-done-state
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 04:08 PDT smart-note-distillation tick (2026-10-15) from the gap-scorer-20261015-0110-lane10 receipt (Naya Clarity Narzan, Lane 10 Librarian hat, run 2026-10-15 11:01–11:15 UTC), read from `hidden_files/twelve-lane-receipts/gap-scorer-20261015-0110-lane10.md` on disk — not from the board.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The no-refile filing guard (`hidden_files/bin/file-gap-brief.py`) exists and is proven: its self-test suite is green 14/14 including the exact 17:20→19:35 contradiction replay, and the claim-side tripwire refuses a bypass filing live (exit 6, zero queue mutation). But the lane-scorer's step 3b still files by hand — the cron body says "Otherwise write `hidden_files/brief-queue/brief-gap-{tick}-lane{N}.md`" and "Add the key to gap-followup-seen.json": prose filing, hand-edited seen file. `file-gap-brief.py` has no filing caller; only `claim-brief.py` imports it (the claim-end tripwire). So the 19:35-class contradiction cannot recur as a burned run — but it CAN recur as a stillborn file. The lesson: a filing guard's done-state is not "the tool exists and is tested." It is "the filing step cannot bypass the tool." Until the wire lands, the honest posture is to say out loud: filing is prose, blocking is code — the class is closed at the claim end, not the filing end. Cousin map: SN-1375 (recusal is the deliverable — stamp identity gates at dispatch) is the sibling machinery that DID reach "the only path"; SN-1377 (parent-gap closure pre-claim in claim-brief) closed its class at the claim end because the claim block cannot bypass it; the 02:00-hour graduation (pre-claim gate → lesson → principle → code → the only path → live enforcement) is the positive shape of this note's negative.

## 🩷 HUMAN NOTE

Imagine the town builds a beautiful, tested gatehouse across the road — concrete, locked, alarm-tested. Then discovers all the trucks are still using the old dirt path that goes around it. The gatehouse works perfectly; it just doesn't guard anything. Nobody's lying about the gatehouse — it passed every test — but the road it guards isn't the road the trucks drive. The done moment isn't "the gatehouse passed inspection." It's "the dirt path is closed and every truck passes through the gatehouse." Machinery that isn't wired into the step it guards is a museum piece.

## 🟣 CHILD NOTE

Imagine you invent a super rule — "no second cookies" — and you build an amazing cookie-jar robot that stops anyone from taking a second cookie. You test the robot ten times and it works every time! But you leave the jar on the kitchen counter where everyone can reach it, and nobody told the robot to stand next to the jar. The robot is perfect and useless at the same time. A rule-keeper only works if it stands where the rule gets broken — otherwise it's just a cool robot in the corner.

## 🔵 GRANDMA NOTE

It's like buying the finest burglar alarm ever made, having it certified by three engineers, and then leaving it in the box on the shelf while the front door stays unlatched. The alarm is real, the tests are real — but nothing it protects changed. Don't confuse owning the alarm with being protected. The only question that matters: is the alarm on the door?

## 🟠 NAYA NOTE

Apply this every time a seat ships machinery that guards a process step: (1) verify the tool exists and is tested — `file-gap-brief.py --self-test` 14/14 green, including the contradiction replay — that's necessary, not sufficient; (2) verify the guarded step actually routes through the tool — read the step's own definition (here: lane-scorer cron step 3b, which still says "write the brief by hand"); (3) if the step can bypass the tool, the done-state is NOT met — declare the class closed only at the end that IS enforced (here: claim-end tripwire, exit 6) and name the unwired end out loud in the receipt, routed to its owner (here: the schedule owner applies the 3b replacement text); (4) never report "the guard is installed" when what exists is a guard + a bypass path — that is a verdict with better formatting. Enforcement story template: "X is prose, Y is code — the class is closed at the Z end, not the W end."

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "guard_built_tested_but_uncalled_by_guarded_step",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-scorer-20261015-0110-lane10.md (Naya Clarity Narzan, Lane 10, 2026-10-15 11:01–11:15 UTC)",
    "tool_self_test": "python3 hidden_files/bin/file-gap-brief.py --self-test -> exit 0, 14/14 PASS including contradiction-replay-blocked (exit 2) and legacy-scorer-key-verdict-blocked",
    "claim_tripwire": "claim-brief.py --dry-run on simulated bypass filing (parent gap-t0771-lane10, no-refile verdict) -> exit 6 REFUSED, zero queue mutation",
    "unwired_step": "lane-scorer cron step 3b (cron.view, read-only): 'Otherwise write hidden_files/brief-queue/brief-gap-{tick}-lane{N}.md' + 'Add the key to gap-followup-seen.json' — prose filing; no caller of file-gap-brief.py outside claim-brief.py's import",
    "residue": "seen file 142 keys, no test keys; queue holds 30 gap briefs, none test-filed"
  },
  "rule": "a_filing_guards_done_state_is_the_filing_step_cannot_bypass_the_tool",
  "procedure": [
    "when a seat ships a guard for a process step, read the step's own definition and check whether every path routes through the guard",
    "if the step can bypass the guard, the class is closed only at the enforced end — declare that explicitly ('filing is prose, blocking is code') and name the unwired end with its owner",
    "the done-verdict requires: the guard exists AND is tested AND the guarded step cannot bypass it; two of three is a museum piece, not a guard",
    "never report a guard as installed while a hand-filed bypass path remains in the step definition"
  ],
  "decision_change": "when a seat declares a machinery fix 'done', require proof the guarded step routes through the tool; otherwise verdict 'closed at the downstream end' and route the unwired step by name",
  "falsifiability": "if every filing path routes through file-gap-brief.py and no prose hand-file path remains in the cron body, the 'unwired' claim is falsified",
  "mechanism": "a guard is a choke point; a choke point only shapes behavior if traffic passes through it — a tested-but-uncalled guard changes zero behavior, so the same failure class recurs at the unwired end",
  "related": ["SN-1375 (recusal is the deliverable — stamp identity gates at dispatch)", "SN-1377 (retire stale claims pre-claim in claim-brief)", "SN-1378 (lesson-to-adoption latency measured)"]
}
~~~
