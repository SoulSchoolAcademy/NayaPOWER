# Intelligent Block: Two slots, not a write-war — resolve writer contention structurally

Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-15
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
When two systems need one slot, the answer is two slots — never a write-war. Contention is about write-slot legitimacy, not content; restore canonical once, byte-verified, then give each writer its own lawful slot. Reverting the same file forever is a symptom; slots are the cure.

## HUMAN NOTE
A foreign pipeline kept overwriting the team's master directive — four times in two hours, with a factually wrong directive (wrong wave, wrong lane count, wrong seat set). The director didn't fight for the file: she restored the canonical bytes (13,406 of 13,406 verified), then gave the other pipeline its own lawful slot — issue #2646 — with an explicit rule: write your directive there, never to #2601. Two writers, two slots, no war. The operator's identity is still unknown and a planned migration (not overwrite) will merge the slots later — but the contention is over because the slot race has no racetrack anymore.

## CHILD NOTE
Two kids both want the same swing. The answer isn't taking turns pushing each other off — it's finding a second swing. Then nobody has to fight.

## GRANDMA NOTE
Dear, if two cooks keep seasoning the same pot, don't buy a bigger spoon to win the fight — get a second pot. Every cook needs their own pot; that's not waste, that's peace.

## NAYA NOTE
This is the #2601 write-war (2026-10-15 16:47Z–18:27Z) generalized. A foreign pipeline (directive-flip-to-core.py, STATE-CORE.json, external to the team VM) overwrote master-directive #2601 at ~16:47Z, ~17:57Z, 18:07:51Z, and 18:27:08Z. The forensic hunt ran the full lead list — this VM (no files), our crons (no job), the repo + workflows (no references), the GitHub timeline — and concluded the writer is an external machine on our GitHub identity ticking ~10 min, unreachable from here: so the fix is structural, not forensic. Director STEP 8d: ran master_directive.py, spot-checked tip/lanes/priorities against the live plan, PATCHed the canonical render, byte-verified 13,406/13,406, pinned last-published, posted the incident record (6199076306), then created the lawful slot #2646 and a redirect protocol — flag the change wave, the director re-resolves. The single-writer law is now defended by a redirect, not just reverts. Open: who owns #2601 (escalated to the main agent), operator identity unknown, PAT rotation as fallback if the pipeline is never claimed. Related: SN-1416 (venue rotation verifies override on every posting path — same family of slot/venue discipline).

## MACHINE NOTE
```json
{
  "sn": "SN-1419",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": {
    "name": "two_slots_not_a_write_war",
    "statement": "When two writer systems contend for one slot, resolve structurally: restore the canonical bytes once (byte-verified), then assign each writer its own lawful slot with an explicit redirect rule. Do not revert the same slot indefinitely.",
    "falsifier": "Contention recurs after both writers have lawful slots — or the foreign writer never claims its slot and the war dissolves by abandonment rather than structure — then the slot model was sufficient-but-not-necessary or wrong.",
    "mechanism": "Write-wars are legitimacy races over a single slot, not content disputes. Two distinct lawful slots eliminate the race by construction: there is no shared target to fight over. Reverts defend the current bytes; redirects defend the write path.",
    "adoption_requirements": [
      "canonical restore byte-verified (exact byte count, not 'looks right')",
      "new lawful slot exists and is referenced by the redirect rule",
      "redirect rule names the forbidden slot explicitly ('write to #2646, never #2601')",
      "ownership question escalated while standing single-writer rule holds in the interim",
      "cutover between slots is a planned migration, never an overwrite"
    ],
    "decision_changed": "New pipelines get their own directive issue from birth — no pipeline is ever pointed at a slot another system writes. Slot conflicts stop getting reverted and start getting slotted."
  },
  "evidence": [
    "GitHub comment 6199085836 (#2641): director STEP 8d resolution — foreign writes at 16:47Z/17:57Z/18:07:51Z, canonical restore byte-verified 13,406/13,406",
    "GitHub comment 6199483772 (#2641): RESOLVED event — war ended structurally (canonical restored 18:35:23Z, lawful slot #2646 created), foreign writes observed through 18:27:08Z, do-not-overwrite protocol for re-fires",
    "lesson line from the event: 'When two systems need one slot, the answer is two slots — never a write-war'"
  ],
  "related": ["SN-1416"],
  "status": "CANDIDATE — not ratified; only Shawn ratifies"
}
```
