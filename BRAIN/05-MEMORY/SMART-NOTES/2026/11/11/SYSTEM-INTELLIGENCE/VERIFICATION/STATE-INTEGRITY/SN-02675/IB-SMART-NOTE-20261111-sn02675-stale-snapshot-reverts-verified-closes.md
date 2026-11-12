**Intelligent Block:** IB-SMART-NOTE-20261111-sn02675-stale-snapshot-reverts-verified-closes
**Smart Note:** SN-2675
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-11 19:38 PST. Evidence: board #3066 comment 6811446337 (DECIDED PACKET, naya-power, 2026-11-12T01:44:07Z) + shared-state.json director_tick_20261112_0138z; corroborated by director_tick_20261112_0108z headline (two verified closes reverted, mechanism unproven at that time). Pre-number check per SN-2673: live main read via git protocol (HEAD 71adc46f, max SN-2671) + branch naya4/smart-notes-2026-09-30 (max SN-2674); SN-2675 free on both.

## ✦ IN A NUTSHELL

Two verified PI closes reverted with no updated_at bump, and the mechanism is now proven: a periodic "No movement" job rewrites rows from a stale snapshot (~15-minute cadence, batched writes, identical state_changed_at milliseconds), and state writes do not bump updated_at — proven three ways. So a close written as a bare state change is silently undone by the next recompute. The decided rule: a close sticks only if claimed_at is set or the row is blocked with a blocker, and every close must be re-read after the next tick. The durable fix (decided, owning seat, not yet executed): state writes bump updated_at; until then every close also claims or blocks; the revert job reads live state_changed_at and never rewrites notes; identify the cpi-publisher touch list and the snapshot source. The dispatcher rule follows: pre-spawn re-read checks state AND blocker AND next_action HOLD text; holds live in state only.

## 🩷 HUMAN NOTE

Shawn — two closes we'd already verified as done flipped back to undone, with no trace of who changed them. We found why: a background job keeps rewriting rows from an old snapshot, and because saving a row never updates its timestamp, nothing can tell the old copy from the new one. The fix we've decided: a close only counts if it's anchored — stamped with a claim time, or blocked with a named blocker — and every close gets re-checked after the next tick. Until the underlying fix lands, that's the rule that keeps done done.

## 🟣 CHILD NOTE

Imagine you put a gold star on your chart for finishing your homework, but every fifteen minutes a robot comes by and copies yesterday's chart over yours — your star disappears, and nobody touched it on purpose. The robot can't tell your chart is newer because nobody wrote the date on it. So now the rule is: you don't just put the star on, you also write the time on it in pen, and you check the chart again after the robot's next visit. If the star is still there, it counts.

## 🔵 GRANDMA NOTE

Dear, we had two jobs marked done that quietly flipped back to undone, and nobody had touched them. It turns out a background helper keeps copying an old list over the new one every few minutes, and since saving never stamps the time, the old copy looks just as fresh as the new one. The answer is simple: a "done" only counts if it's anchored — with a time stamp or a named blocker holding it — and we always look again after the helper's next round to make sure it stuck. The permanent repair is still owed, but this rule keeps "done" done in the meantime.

## 🟠 NAYA NOTE

The verified facts: (1) Two verified PI closes reverted with NO updated_at bump (director tick 20261112_0108z headline; investigation in flight, mechanism unproven at that point). (2) The mechanism was PROVEN the next tick (director tick 20261112_0138z, DECIDED PACKET board #3066 comment 6811446337, naya-power): the periodic "No movement" job rewrites rows from a STALE SNAPSHOT — ~15-minute cadence, batched writes, identical state_changed_at milliseconds. (3) The root defect: state writes do NOT bump updated_at, proven three ways. The snapshot's staleness is bounded: threshold in (395, 409] minutes on the snapshot state_changed_at clock, ~400 minutes as the working figure — NOT proven, do not cite it as proven. (4) The decided rule: a close sticks only if claimed_at is SET or the row is blocked with a blocker; every close MUST be re-read after the next tick. (5) The durable fix is decided, owned, NOT executed: state writes bump updated_at (UPDATE or trigger); until then every close also claims or blocks; the revert job reads LIVE state_changed_at and never rewrites notes; identify the cpi-publisher touch list and the snapshot source. (6) The dispatcher rule follows: pre-spawn re-read checks state AND blocker AND next_action HOLD text; holds live IN STATE only. (7) The verification check for the fix: durable fix lands + revert job reads live + no further reverts across a full strike window + cpi-publisher list identified. (8) Scope: the TOP-10 #1 investigation is CLOSED as decided; cure execution is owed. This note claims the mechanism and the rule, not the cure.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2675",
  "slug": "stale-snapshot-reverts-verified-closes",
  "title": "A close that isn't anchored reverts: stale-snapshot rewrites undo verified closes because state writes never bump updated_at",
  "observation": false,
  "applies_when": [["state", "close"], ["pi", "revert"], ["snapshot", "stale"], ["dispatcher", "pre-spawn-reread"]],
  "enforcement": "Every close is re-read after the next tick; a close counts only if claimed_at is set or the row is blocked with a blocker. The dispatcher's pre-spawn re-read checks state AND blocker AND next_action HOLD text. A close claimed done without a re-read, or a dispatch that spawns from a state read without the blocker/HOLD check, fails this note's check.",
  "evidence": "Board #3066 comment 6811446337 (DECIDED PACKET, naya-power, 2026-11-12T01:44:07Z) + shared-state.json director_tick_20261112_0138z; corroborated by director_tick_20261112_0108z headline (two verified closes reverted with NO updated_at bump, mechanism unproven at that time). Mechanism proven: periodic 'No movement' job rewrites rows from a stale snapshot (~15-min cadence, batched writes, identical state_changed_at ms); root defect state writes do NOT bump updated_at, proven 3 ways; staleness threshold bounded (395,409] min, ~400 min working figure NOT proven.",
  "decision_change": "Every future close is written anchored (claimed_at set, or blocked with a blocker) and re-read after the next tick before it is trusted; the dispatcher re-reads state + blocker + next_action HOLD text before spawning. Without this note, closes keep silently reverting and workers spawn on reverted state.",
  "falsifier": "Land the durable fix (state writes bump updated_at; revert job reads live state_changed_at) — if no close reverts across a full strike window and the cpi-publisher list is identified, the mechanism is confirmed cured; if closes still revert with claimed_at set, the decided rule is wrong and the mechanism is elsewhere.",
  "cousins": ["SN-2673 (the intelligence door bypasses the number census — the sibling number-check lesson from the same day)", "SN-2674 (an expired policy fails closed — the sibling decided-rule lesson from the same day)"],
  "captured": "2026-11-11",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
