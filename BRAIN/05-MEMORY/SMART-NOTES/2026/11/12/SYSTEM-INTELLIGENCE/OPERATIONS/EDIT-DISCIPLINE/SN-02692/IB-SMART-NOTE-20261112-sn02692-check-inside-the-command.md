**Intelligent Block:** IB-SMART-NOTE-20261112-sn02692-check-inside-the-command
**Smart Note:** SN-2692
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-12 00:38 PST. Evidence read first-hand from the local lane receipt + scripts on disk (no GitHub fetch — #1354 capped at 2500). Pre-number check (this tick, full-domain): SN-2692 free in every domain (capture, BRAIN tree, ledger, branch, registry next_sequence 2691).

## ✦ IN A NUTSHELL

A check a seat must remember to run is a wish with a script attached. The 1610 incident corrupted a live file because a duplicated marker looked like a safe anchor, and the gate that could have said no only worked if the seat ran it — before this run, no script had ever invoked it. `safe-edit.py` removes the "if": the edit command itself refuses a duplicated anchor, takes the backup, and proves the diff, so the next seat cannot skip the check by forgetting it exists. When a rule needs a human to remember a check, put the check inside the tool that does the work — make the safe path the only path.

## 🩷 HUMAN NOTE

Shawn — we had a checker that could have stopped a bad edit, but it only helped if someone remembered to run it — and nobody ever had. The fix this morning was to build the check into the edit command itself: now the command that makes the edit also runs the check, takes the safety copy, and proves the result, all in one step. A seat cannot forget the check anymore, because the check is inside the tool, not in someone's memory.

## 🟣 CHILD NOTE

Imagine a gate that keeps you safe — but only if you remember to close it. Someone will forget, and that is when things break. The fix is to build the gate into the door itself, so it closes every time you walk through, whether you remember or not. That is what happened here: the safety check now lives inside the edit tool, so it runs every time.

## 🔵 GRANDMA NOTE

Dear, there was a little checker that could have stopped a bad change — but it only worked if someone remembered to use it, and no one ever did. So the helpers built the checker right into the tool that makes the change, love: now the check runs by itself every single time, and nobody has to remember. The safe way is now the only way the tool knows.

## 🟠 NAYA NOTE

The verified facts: (1) The 1610 incident: a bare `# ---- falsifiers ----` marker matched the literal inside `_falsifier_block_sha()`, an edit landed on the wrong occurrence and corrupted the runner; caught only by read-back luck. The EDIT-ANCHOR RULE (SN-2686) plus the gate `check-edit-anchor.py` followed — but before this run, zero scripts had ever invoked the gate (bin callers: 0). (2) The graduation: `hidden_files/bin/safe-edit.py` (sha 1d4f4507e2eb6cac9003a3990aca567e13f1fde32fd9a7ef884d482d62f22411, 9,382 bytes, verified on disk) IS the edit — anchor check + backup + apply + reconstruction-verified diff in one command; it invokes `check-edit-anchor.py` itself, the first automatic invocation on record. (3) Tested 6/6 on /tmp fixtures including the exact 1610 reproduction — bare marker REFUSED exit 1, count 2 (lines 111/189), file sha unchanged d957847c. (4) The rule text now mandates `safe-edit.py` as the lane-run edit path, installed by a real edit performed through the path itself: template b62d515d → 970a886d, diff exactly 79c79, backup sha == pre-edit sha. Receipt `hidden_files/twelve-lane-receipts/gap-gap-gap-gap-lane-scorer-20261018-1610-lane12-lane12-lane12-lane12-lane12-lane12.md`, 9.1/10, 2026-11-12 08:13–08:19Z. (5) Honest scope, named not hidden: independent-seat adoption still unproven (zero independent-seat applications as of 08:17Z — time-blocked, the rule was ~34 minutes old); direct-tool edits still bypass the path (the rule text forbids them for lane runs, no mechanical enforcement exists); the exit-3 auto-restore path is defensive code never triggered in testing. (6) Mechanism: a check that lives in a seat's memory is skipped by inattention; a check that lives in the command is skipped only by leaving the command — and leaving the command is now the forbidden act, not the forgotten one. (7) This is the graduation of SN-2686, not a restatement of it: SN-2686 claims the anchor rule and the gate; this note claims the rule becoming machinery — the check moving from something a seat runs into something the edit path is.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2692",
  "slug": "check-inside-the-command",
  "title": "Make the safe path the only path: put the check inside the command",
  "observation": false,
  "applies_when": [["tool", "gate"], ["edit", "path"], ["rule", "enforcement"], ["lane-executor", "edit"]],
  "enforcement": "Lane-run edits go through hidden_files/bin/safe-edit.py (anchor check + backup + apply + reconstruction-verified diff in one command); lane-agent-brief-template.md PART 2 mandates safe-edit.py as the lane-run edit path. A receipt for an edit-touching run cites safe-edit.py + the pre/post shas; a run that edits without the path is scored down on the edit leg. Named gap, not hidden: direct-tool edits still bypass the path — rule text forbids them for lane runs, no tool-level enforcement exists yet.",
  "evidence": "Child receipt hidden_files/twelve-lane-receipts/gap-gap-gap-gap-lane-scorer-20261018-1610-lane12-lane12-lane12-lane12-lane12-lane12.md (Lane 12, 9.1/10, 2026-11-12 08:13–08:19Z): safe-edit.py sha 1d4f4507e2eb6cac9003a3990aca567e13f1fde32fd9a7ef884d482d62f22411 (verified on disk, 9,382 bytes); 6/6 tests incl. the 1610 reproduction (REFUSED exit 1, count 2, lines 111/189, sha unchanged d957847c); template b62d515d → 970a886d, diff exactly 79c79, via the path itself; bin callers of check-edit-anchor.py before this run: 0 — first automatic invocation on record. No existing note covers safe-edit.py or the mandatory-path idea — grep of learn/lessons.jsonl for 'safe-edit' / 'mandatory path' / 'cannot forget' = zero hits.",
  "decision_change": "When a rule needs a seat to remember a check, the next build puts the check inside the tool that does the work — the safe path becomes the path taken, not the path remembered.",
  "falsifier": "If seats keep corrupting files through direct-tool edits at the same rate after safe-edit.py is mandated, the tool-embedded check changed nothing — the bypass, not the check, is the failure. If a file is corrupted through safe-edit.py itself with its anchor check passing on a duplicate, the path is broken, not the lesson.",
  "cousins": ["SN-2686 (edit-anchor rule + gate — this note is that rule graduating from discipline to machinery)", "SN-2678 (pin the instrument before the run — same 1610 lineage)"],
  "captured": "2026-11-12",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```