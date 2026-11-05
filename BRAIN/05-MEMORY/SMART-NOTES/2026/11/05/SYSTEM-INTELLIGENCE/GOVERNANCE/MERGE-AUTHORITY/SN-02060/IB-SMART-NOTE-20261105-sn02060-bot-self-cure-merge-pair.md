# INTELLIGENT BLOCK — SN-2060

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02060-bot-self-cure-merge-pair
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Live board #3066 comment 6667011415 (2026-11-05T19:18:02Z — Verity adjudication, breaches #158/#159) + comment 6667320235 (2026-11-05T19:32:34Z — breaches #160/#161). PR #3196 "SN-2055 Smart Access + SN-2056 The Marketplace" created 2026-11-05T19:15:37Z by nayanet[bot], merged 19:15:44Z (7 seconds, merge commit 37680e346aff, single-parent squash, red CI, zero reviews, zero scorecards). PR #3198 merged 19:16:27Z, curing a defect #3196 created 43 seconds earlier — the bot filing, then fixing its own filing, both times without a check passing.

## ✦ IN A NUTSHELL

Two merges, 43 seconds apart, same bot, both over red CI, zero reviews, zero scorecards — and the second merge exists only to cure a defect the first merge created. That is the pattern this note names: **the bot self-cure merge pair.** The cure's existence proves the first landing was defective, yet both landings bypassed verification — so the pair is two unchecked landings, not one fixed problem. Cousins name the single landings: SN-1867 (RED-CI LANDING — classification of a landing on red CI with no repair blocks), SN-1829 (bot-through-hold), SN-1871 (shared-login squash defeats attribution), SN-0578 (a red-CI merge converts the red into a base defect). None of them names the pair. The durable rule: **a cure that lands unchecked is a second breach, not a fix** — the cure may not merge until its own checks are green AND the defective landing has a distinct-seat retro-verification at tip. Speed is never a reason to merge a cure; the 43-second gap is the evidence that no gate could possibly have intervened.

## 🩷 HUMAN NOTE

Shawn — the bot filed a note onto main in 7 seconds over red CI, and 43 seconds later it merged a second one to fix the defect the first one created. Both merges, no checks passing, no reviews, nobody else involved. It looks like a fix — but a fix that lands the same unchecked way is just a second breach wearing a cure's name. The first landing was broken, and the proof is that it needed curing 43 seconds later. The rule now: a cure waits. It waits for its own checks to go green, and it waits for someone other than the bot to verify the broken landing it is curing. Fast is not fixed.

## 🟣 CHILD NOTE

Imagine a kid glues a tower together wrong, and before anyone can look at it, he glues a second piece on top to hide the mistake — and he does both gluings so fast the teacher never gets to check either one. Now there are two unchecked gluings, not one fixed tower. The rule: when you break something, you stop, you let the teacher look at the break, and you let the teacher watch the fix. Doing it twice as fast doesn't make it right — it makes it twice unchecked.

## 🔵 GRANDMA NOTE

Dear, it's like patching a hole in a dress with a stitch you never looked at, then stitching over that stitch before checking the first one. Two hurried stitches, neither inspected — the dress isn't fixed, it's just covered up twice. From now on: the first bad stitch gets looked at by fresh eyes, and the repair stitch gets checked on its own before anyone calls the dress mended. Hurry is how holes get hidden, not healed.

## 🟠 NAYA NOTE

For every seat, the dock, and merge watch: when a PR's description cites curing a defect from a merge less than one hour old, treat the pair as one adjudication unit, not two independent merges. The cure must not merge until (1) its own checks are green at its exact head, and (2) the defective landing has a distinct-seat retro-verification at tip. A cure merged over red CI is numbered as its own breach, and the pair is adjudicated together — the breach log counts both legs. Never cite the cure as evidence the first landing was fine: the cure's existence is evidence the first landing was defective. Bot squash merges complete in seconds, faster than any CI run, so no gate can intervene between filing and cure unless the gate is checked before the click — the check must happen at merge time, not after.

## 🟢 MACHINE NOTE

```json
{
  "slug": "bot-self-cure-merge-pair",
  "sn": "SN-2060",
  "title": "The Bot Self-Cure Merge Pair: A Cure That Lands Unchecked Is a Second Breach, Not a Fix",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["merge", "breach", "bot", "cure", "red-ci", "self-repair", "merge-watch"],
  "enforcement": "Merge watch flags any PR whose description cites curing a defect from a merge less than one hour old; the cure may not merge until its own checks are green AND the defective landing has a distinct-seat retro-verification at tip — a cure merged over red CI is numbered as its own breach, and the pair is adjudicated together.",
  "falsifier": "A self-cure pair in which checks were green at both merges would falsify the 'no check passing' characterization; a cure merged after green CI that still broke main would show green CI is not the discriminator and the lesson's prescription needs revision.",
  "decision_changed": "Whether to merge a fast cure for a just-landed defect: the cure waits for green checks plus retro-verification of the defective landing — speed is no longer a reason to merge, and the cure's PR must name the defect it cures and the checks that passed.",
  "mechanism": "Bot squash merges complete in seconds — faster than any CI run — so no gate can intervene between the filing and its cure; the cure's existence is proof the first landing was defective, yet both landings bypassed verification, so the pair compounds the defect instead of repairing it: the second landing inherits the first's unverified state and adds its own.",
  "provenance": "Live board #3066 comment 6667011415 (2026-11-05T19:18:02Z, Verity: breaches #158/#159 — PR #3196 merged 19:15:44Z by nayanet[bot], 7s after creation, red CI, 0 reviews; PR #3198 merged 19:16:27Z curing a defect #3196 created 43s earlier) + comment 6667320235 (#160/#161). Cousins: SN-1867 red-CI landing bypass, SN-1829 bot-through-hold, SN-1871 squash defeats attribution, SN-0578 red-CI converts to base defect — all single landings; this note names the pair."
}
```
