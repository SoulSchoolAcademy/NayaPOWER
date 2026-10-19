# Print the Pointer, Not the Value — Indirection Is the Only Fix for Rotating Live Numbers

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1676-print-pointer-not-value
**Smart Note:** SN-1676
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Any byte that names a live resource (a board number, a URL, a branch, a tip SHA) must name it by indirection to the standing pointer file, never as a literal value. A live number can rotate inside the shift — the live board rotated 2721→2765 mid-fix-window — and renumbering every consumer chases a moving target. Indirection moves the rot boundary to one pointer file whose update is atomic.

## 🩷 HUMAN NOTE

Don't write today's phone number in permanent ink — write "call the front desk" instead. The front desk's number changes; the sentence "call the front desk" stays true. Here the live board number changed from 2721 to 2765 while a lane was mid-fix, so every file that printed "2721" as a fact was wrong before the fix even landed. The lane that won printed the pointer (the one file that always names the current board) instead of the number — and it stayed right through the rotation.

## 🟣 CHILD NOTE

If the number might change, don't carve the number in stone — carve "look at the sign on the door." The sign is easy to change; the stone is not.

## 🔵 GRANDMA NOTE

Write down where to look, not what you'll see when you look. "The grocery list is on the fridge" stays true no matter what the list says. Lists change; the fridge doesn't move.

## 🟠 NAYA NOTE

The 2026-10-19 distill-daily lane (t-distill-daily-20261019.md, 9.2/10) repaired 5 stale board pointers in BRAIN/00-ACTIVATION/ by indirection to BRAIN/CURRENT-MISSION-STATE.md instead of renumbering: the live number rotated 2721→2765 inside the fix window, so any literal renumbering would have been stale before merge. The parent's own scorecard then named its residual hole honestly — the gate script's STANDING still hardcoded "live_board": "2721" — and the gap lane (gap-t-distill-daily-20261019-lane0.md, 9.0/10) closed it in the same hour: a self-named hole, claimed and closed within the shift. Recorded as CORE-PRINCIPLES.md CANDIDATE 665.

**Architectural rule:** a byte naming a live resource must be a pointer (file path + field) that resolves at read time, never a literal captured at write time. Indirection is the fix for rot; renumbering is chasing the rot. Exception: contexts with no pointer access (a board comment read outside the repo) — there the literal IS the pointer, and the note must carry its as-of date.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1676",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "any byte naming a live resource (board number, URL, branch, tip SHA) must name it by indirection to the standing pointer file, never as a literal; a live number can rotate inside the shift (2721->2765 mid-fix-window 2026-10-18), so literal renumbering is stale before merge while indirection stays right",
  "decision_change": "any future write to a doc, brief, script, or STANDING field that names a live resource must use indirection (path + field of the pointer file, e.g. BRAIN/CURRENT-MISSION-STATE.md) instead of printing the literal value; renumbering literals is not an acceptable repair",
  "falsifiability": "the doctrine fails if a case is shown where the pointer file itself rotted faster than literals would have (single point of failure proven worse), or where a cold reader with no repo access needed the literal — then the literal with an as-of date is the pointer, and the note's exception was wrong",
  "mechanism": "live numbers rotate on a shorter timescale than consumer files (board 2721->2765 within one shift); a literal baked at write time carries write-time truth into read time, so it decays; a pointer carries no truth, only an address, so it cannot decay until the address itself moves — the rot boundary collapses to one file whose update is atomic and mechanical",
  "applies_when": ["doc", "live-pointer", "brief", "live-reference", "fix", "stale-reference", "board", "rotated-number"],
  "enforcement": "the lane's 3-pass scorecard self-review must carry an explicit 'no literal live values in touched files' residual-hole line — this is the check that caught the STANDING 'live_board': '2721' hole in-run (gap-t-distill-daily-20261019-lane0.md, 13:07Z); the distill-daily gate script now reads the live board from BRAIN/CURRENT-MISSION-STATE.md instead of hardcoding it, so a hardcoded live value fails the gate",
  "evidence": "hidden_files/twelve-lane-receipts/t-distill-daily-20261019.md (12:31Z, 9.2/10): repaired 5 stale board pointers in BRAIN/00-ACTIVATION/ by indirection to BRAIN/CURRENT-MISSION-STATE.md after the number rotated 2721->2765 mid-fix-window; gap-t-distill-daily-20261019-lane0.md (13:07Z, 9.0/10): closed the self-named residual hole (gate script STANDING hardcoded live_board 2721); hidden_files/learning-events-2026-10-19-13.md; CORE-PRINCIPLES.md CANDIDATE 665"
}
~~~
