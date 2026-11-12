**Intelligent Block:** IB-SMART-NOTE-20261112-sn02686-edit-anchor-unique-context-sha-verify
**Smart Note:** SN-2686
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-12 00:08 PST. Evidence read first-hand from local receipts + template + gate script (no GitHub fetch — #1354 capped at 2500, commenting disabled 2026-10-10). Pre-number check: counter last line 2684, SN-2685 taken this tick for the relayed-ruling note; main holds SN-2679–SN-2684; branch max SN-02678; ledger max SN-2678; no open Smart Note PRs (carriers #2468/#2828/#2854 closed). No existing note covers edit anchoring — grep of learn/lessons.md + ledger.json for 'edit-anchor' / 'edit anchor' = zero hits.

## ✦ IN A NUTSHELL

Anchor every edit on unique surrounding context — and prove the file sha against the pre-edit backup before you run any test. The 1610 incident proved why: a bare `# ---- falsifiers ----` marker matched the literal of the same text inside `_falsifier_block_sha()`, so the edit landed on the wrong occurrence and corrupted the runner. The sha round-trip caught it; the tests never got the chance to pass on corrupted code. The rule is now in lane-agent-brief-template.md PART 2, and the gate is a script: hidden_files/bin/check-edit-anchor.py (anchor-uniqueness + sha-verify modes), tested 5/5 including the exact 1610 reproduction — the bare marker counts 2 (lines 111/189) and the gate refuses it with exit 1. A non-unique anchor is a wrong-location edit waiting to happen; the sha check is what catches it before it propagates.

## 🩷 HUMAN NOTE

Shawn — a seat edited a file by matching a short marker line, and the same words also appeared inside the code itself — so the edit landed in the wrong place and broke the file. The fix is now a standing rule: every edit has to point at text that appears exactly once, and the first thing checked after any edit is whether the file's fingerprint still matches what it should be — before any test runs. There is a small checker script that refuses a non-unique marker outright, and it caught the exact mistake in rehearsal. The rule is written into the brief template now, so every seat follows it.

## 🟣 CHILD NOTE

Imagine you tell a friend "change the word on line 5" — but the same word is on two lines, and your friend changes the wrong one. That is what happened. The new rule: always point at words that appear only once, so there is no wrong line to pick. And after you change something, check the fingerprint of the whole page before you do anything else — if it does not match, you know right away something went wrong.

## 🔵 GRANDMA NOTE

Dear, a helper edited a file by looking for a little marker line — but those same words were written inside the program too, so the change went to the wrong spot and spoiled the file. The repair is a simple habit now, love: always aim at words that appear just once, nowhere else, and after every change, check the file's fingerprint against the copy you saved first — before running anything. There is a little checker that says no to a marker that appears twice. It caught the exact mistake when we tried it on purpose.

## 🟠 NAYA NOTE

The verified facts: (1) The 1610 incident: a bare `# ---- falsifiers ----` marker matched the literal of the same text inside `_falsifier_block_sha()` in hidden_files/run_pilot12_battery.py, so an edit landed on the wrong occurrence and corrupted the runner; the sha round-trip caught it (comment L201, line-111 marker, diff +2/-1, runner sha d957847c...). (2) The rule landed: EDIT-ANCHOR RULE folded into lane-agent-brief-template.md PART 2 (c1508de2→3429eed4, diff exactly +2 lines) — every edit must anchor on unique surrounding context; first verification after any edit is the file sha vs the pre-edit backup, before any test runs. Receipt hidden_files/twelve-lane-receipts/gap-gap-gap-gap-lane-scorer-20261018-1610-lane12-lane12-lane12-lane12.md, 9.4/10, 2026-11-12 07:48Z. (3) The mechanical half closed the same night: hidden_files/bin/check-edit-anchor.py built (anchor-uniqueness + sha-verify modes), tested 5/5 including the 1610 reproduction — the bare marker counts 2 (lines 111/189), exit 1, the gate would have refused the corrupting anchor. Rule text gained a one-sentence gate pointer via a rule-following edit (backup sha-verified, anchor check PASS line 79 pre-edit, diff exactly line 79 post-edit; template 3429eed4→b62d515d). Receipt hidden_files/twelve-lane-receipts/gap-gap-gap-gap-lane-scorer-20261018-1610-lane12-lane12-lane12-lane12-lane12.md, 9.1/10, 2026-11-12 00:05 PST. (4) The mechanism: edit tools match the FIRST occurrence of the anchor text; a short or bare marker that also appears as a literal inside code matches the wrong occurrence silently — no error, no warning. The sha-vs-backup comparison catches the wrong-location edit in seconds, before tests can pass on corrupted code and before the corruption propagates to the next seat's read. (5) Scope: this note claims the rule and the gate, not adoption — at capture the rule was ~22 minutes old with zero independent-seat applications; adoption needs elapsed time plus another seat's edit-run, and that proof is still owed.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2686",
  "slug": "edit-anchor-unique-context-sha-verify",
  "title": "Anchor every edit on unique context, then prove the sha before you test",
  "observation": false,
  "applies_when": [["edit", "anchor"], ["lane-executor", "edit"], ["file-write", "verify"]],
  "enforcement": "hidden_files/bin/check-edit-anchor.py — anchor-uniqueness mode refuses a non-unique anchor (exit 1) and sha-verify mode compares the file sha against the pre-edit backup before any test runs; lane-agent-brief-template.md PART 2 carries the rule text with the gate pointer. An edit that cannot pass the anchor check does not run.",
  "evidence": "Receipt hidden_files/twelve-lane-receipts/gap-gap-gap-gap-lane-scorer-20261018-1610-lane12-lane12-lane12-lane12.md (Lane 12, 9.4/10, 2026-11-12 07:48Z): EDIT-ANCHOR RULE folded into lane-agent-brief-template.md PART 2 (c1508de2→3429eed4, diff exactly +2 lines). The 1610 incident: bare '# ---- falsifiers ----' marker matched the literal inside _falsifier_block_sha(), edit landed on the wrong occurrence, runner corrupted; caught by sha round-trip (comment L201, line-111 marker, diff +2/-1, runner sha d957847c...). Gate built 00:05 PST: hidden_files/bin/check-edit-anchor.py (anchor-uniqueness + sha-verify modes), tested 5/5 including the 1610 reproduction — bare marker counts 2 (lines 111/189), exit 1, gate would have refused the corrupting anchor; template gained gate pointer (3429eed4→b62d515d). Receipt hidden_files/twelve-lane-receipts/gap-gap-gap-gap-lane-scorer-20261018-1610-lane12-lane12-lane12-lane12-lane12.md, 9.1/10, 2026-11-12 00:05 PST. No existing note covers edit anchoring — grep of learn/lessons.md + ledger.json for 'edit-anchor' / 'edit anchor' = zero hits.",
  "decision_change": "Every future edit by any seat anchors on unique surrounding context, and the first verification after any edit is the file sha vs the pre-edit backup, before any test runs; a non-unique anchor is refused by the gate instead of edited and hoped about.",
  "falsifier": "If an edit with a non-unique anchor is shown to land on the intended occurrence every time, the rule is overstated — it cannot be, because the tool matches the first occurrence and a duplicate anchor leaves the choice to position, not intent. If sha-vs-backup misses a wrong-location edit, the check is broken — it compares exact bytes, so a changed byte is always visible. If check-edit-anchor.py passes a duplicate anchor, the gate is broken, not the rule.",
  "cousins": ["SN-2676 (falsifier line verbatim or unverified — same receipt, sibling rule: 2676 governs the report wording, this note governs the edit)", "SN-2678 (pin the instrument before the run — same 1610 lineage: pin the runner, then anchor the edit)", "SN-0586 (verify the instrument, not the receipt)"],
  "captured": "2026-11-12",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```