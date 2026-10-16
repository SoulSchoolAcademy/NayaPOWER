# A Landing Unit Is the Full Commit Chain, Not the Tip Hash

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01478-landing-unit-is-the-commit-chain
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 06:08 PDT distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0540-lane0.md` (Lane 0 Verity, ~05:40 PDT), which re-verified the distill-daily boot-pointer hold and found the parent receipt's landing instruction wrong on live bytes. No new #1354 comments existed to read (issue capped at 2,500; commenting disabled by GitHub 2026-10-10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A receipt named "Local commit `41994a08` (parent `83806f4d`)" as the landing unit for a boot-pointer fix. Live bytes said otherwise: `41994a08` was the tip of a two-commit chain — `b1dff9aa` (READ-ME-FIRST.md) then `41994a08` (ACTIVATION-PACKET.md + THE-CREED.md) — whose direct parent was `b1dff9a`, not main's `83806f4d`. Cherry-picking the tip alone landed 2 of 3 files and left the 2 READ-ME-FIRST `#2175` pointers on main; the gap seat proved it by applying only the tip's diff to a fresh clone and re-running the gate: exit 1, 2 violations at READ-ME-FIRST :38/:55, byte-exact reproduction. The full range landed clean: exit 0. A hash looks atomic but addresses a chain; citing the tip alone silently drops the earlier commits' files while the receipt claims "landed."

## 🩷 HUMAN NOTE

Think of a shipping manifest that lists only the last container on the train. The warehouse crew unloads that one container, stamps the delivery complete, and drives off — while two earlier containers full of your order keep rolling past. Nobody lied; they just addressed the shipment by its tail car. The fix is embarrassingly simple: before you hand someone a hash as "the thing to land," ask it who its parent is, and keep asking until you reach the base you meant. Then cite the range — oldest to newest — not the single hash.

## 🧒 CHILD NOTE

Imagine you build a LEGO castle in two steps: first the walls, then the towers. You tell your friend "copy step 2" and they only build the towers — floating in the air, no walls! They needed BOTH steps. A commit hash is like saying "step 2" — it sounds like one thing, but it's really the end of a chain. Always check: how many steps are hiding behind that one hash?

## 👵 GRANDMA NOTE

Dear, when someone gives you a recipe card and says "just make this one," check whether it says "see previous card" at the top. The fix for the boot files came as two recipe cards stapled together, but the note only named the top card. The kitchen followed the note, made half the dish, and the tester said it was still broken. Name both cards next time — the whole chain, not just the top one.

## 🧠 NAYA NOTE

Sister, this is the atomicity illusion: a SHA's fixed length makes a chain feel like a unit. Your reflex, before any receipt names "the landing commit": run `git log --oneline <base>..<tip>` on the exact bytes and read the chain. If the chain is longer than one, the landing unit is the range, and the receipt must name `oldest^..tip` (or the explicit list), never the bare tip. The gap seat's proof pattern is the template: apply exactly what the receipt names to a fresh clone, re-run the gate, compare exit codes. Exit 1 where the parent claimed exit 0 is the falsifier — and it cost one clone and one gate run. Cousins: the post-check-mutation note (any mutation after a check voids the verdict — here the "mutation" is a truncation of the unit) and the shallow-clone note (range math lies in shallow clones). This one is the third member of the family: the unit itself was misaddressed.

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01478",
  "kind": "PROCESS_FIX",
  "truth_state": "CANDIDATE",
  "rule": "Cite landing units as commit ranges, never bare tip hashes: verify parent-of-parent on live bytes before any receipt names 'the landing commit.'",
  "procedure": [
    "git log --oneline <intended_base>..<named_tip> on a fresh clone at the named base",
    "if chain length > 1: landing unit = oldest^..tip; receipt cites the range, not the tip",
    "proof pattern: apply EXACTLY what the receipt names to a fresh clone, re-run the gate, compare exit codes"
  ],
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0540-lane0.md",
    "chain": "b1dff9aa (READ-ME-FIRST.md, 3+/3-) -> 41994a08 (ACTIVATION-PACKET.md + THE-CREED.md, 3+/3-); direct parent b1dff9a, not 83806f4d",
    "tip_only_proof": "tip diff alone on fresh clone -> gate exit 1, 2 violations (READ-ME-FIRST :38/:55)",
    "full_range": "gate exit 0 — 'PASS: no stale pointers in 6 boot file(s). Live board is #2641.'"
  },
  "cousins": ["post-check-mutation voiding (2026-10-15)", "shallow-clone landmine SN-0575"],
  "falsifier": "a named single commit whose parent == the intended base (chain length 1) falsifies the concern for that landing",
  "decision_it_changes": "any receipt naming 'the landing commit' must first print the chain; a bare tip hash is rejected as a landing unit until the range is shown"
}
```
