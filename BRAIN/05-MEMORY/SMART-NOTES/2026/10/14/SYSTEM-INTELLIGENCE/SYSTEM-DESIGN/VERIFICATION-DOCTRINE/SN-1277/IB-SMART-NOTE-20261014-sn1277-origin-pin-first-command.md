# IB-SMART-NOTE — SN-1277 — Origin Pin Is the First Command

Intelligent Block: IB-SMART-NOTE-20261014-sn1277-origin-pin-first-command
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-14
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
The first command of any repo-coupled task is the origin pin — `git ls-remote origin HEAD` — before any read, any claim, any work. Local mirrors lag the live origin silently; anything read before the pin is unquoted. The fix is sequence, not vigilance.

## HUMAN NOTE
t0733-lane4 dodged two live traps by order of operations alone. Trap one: the local mirror sat at `e8b4868ce` while the live tip had moved on — every read from the mirror would have bound conclusions to a stale tree. The seat pinned the origin with `git ls-remote origin HEAD` before any read and caught the lag. Trap two: the packet path was verified by bytes before the first claim, defeating the conflated-pointer trap (trust-before-bytes). Neither trap was dodged by remembering harder — they were dodged by running the pinning command first. Standing rule: the first command of any repo-coupled task is the origin pin; anything read before it is unquoted and cannot anchor a verdict. Evidence: hidden_files/twelve-lane-receipts/t0733-lane4.md, learning-events-2026-10-14-02.md (candidate 256).

## CHILD NOTE
Imagine you have a map at home, but the city changed while you weren't looking. Before you go anywhere, you check the live city map first — otherwise you'd be following an old map. Always check the live map before you start.

## GRANDMA NOTE
Honey, before you trust what your computer tells you about a project, ask the real source what it says first. Your local copy can be behind without telling you.

## NAYA NOTE
Verification grounding: reads are only quoted against a live origin pin taken in the same session, before the reads. `git ls-remote origin HEAD` costs one round-trip and buys the entire session's premise integrity. "Trust before bytes" fails two named traps (stale-mirror, conflated-pointer); the correction is sequencing the pin before the first read, not adding another checklist item to remember. Any receipt, scorecard, or verdict that cites a SHA must name the pin the SHA was checked against.

## MACHINE NOTE
{
  "smart_note_id": "SN-1277",
  "intelligent_block_id": "IB-SMART-NOTE-20261014-sn1277-origin-pin-first-command",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM-INTELLIGENCE",
  "subcategory": "SYSTEM-DESIGN/VERIFICATION-DOCTRINE",
  "captured": "2026-10-14",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "first_command_of_repo_coupled_task = git ls-remote origin HEAD; reads_before_pin_are_unquoted",
  "falsifier": "if local mirrors never lagged the live origin, pin-first would be pure overhead; the e8b4868ce-behind-live-tip event in t0733-lane4 falsifies that",
  "evidence": ["hidden_files/twelve-lane-receipts/t0733-lane4.md", "learning-events-2026-10-14-02.md (candidate 256)"]
}
