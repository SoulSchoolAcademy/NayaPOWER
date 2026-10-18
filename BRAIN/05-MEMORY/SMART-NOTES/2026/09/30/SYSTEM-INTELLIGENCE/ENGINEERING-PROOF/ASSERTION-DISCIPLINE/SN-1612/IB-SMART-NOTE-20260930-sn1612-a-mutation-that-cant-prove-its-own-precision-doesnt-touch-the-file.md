# A Mutation That Can't Prove Its Own Precision Doesn't Touch the File — Pre-Write Assertions Fail Closed

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1612-a-mutation-that-cant-prove-its-own-precision-doesnt-touch-the-file
**Smart Note:** SN-1612
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** night-dispatcher t0827-lane12 receipt (Naya Clarity Narzan, breaker-#11 registry flip, 2026-10-18) — hidden_files/twelve-lane-receipts/t0827-lane12.md line 60: first flip attempt used a regex splice with a broken change-count assertion — the assertion fired BEFORE writing, so no partial write happened (fail-closed by accident, then by design on the retry with the line-scoped replace + git diff --stat check). Mirrored in hidden_files/learning-events-2026-10-18-25.md (run 08:20 UTC) as NEW PRINCIPLE CANDIDATE 603.

## IN A NUTSHELL

The seat's first flip attempt used a regex splice carrying a change-count assertion — and the assertion was itself broken. But it was broken in the fail-closed direction: it fired BEFORE the write call, on the in-memory candidate edit, so no partial write ever touched the file. Fail-closed by accident on the first attempt, then by design on the retry (line-scoped replace + `git diff --stat` review). The discipline: a scripted mutation carries its precision proof — expected change count, exact line scope — evaluated BEFORE the write call, never after. A mutation that can't prove its own precision doesn't touch the file.

## HUMAN NOTE

It's proofreading the letter before it goes in the envelope — except the rule is mechanical, not aspirational. A mutation script that writes first and verifies after is a surgeon who operates and then checks the chart. The precision assertion (how many regions will change, exactly which lines) runs on the candidate edit in memory, before a single byte lands on disk. If the count is wrong, the file never moves. Note what actually protected the file here: not a clever assertion — the assertion was broken. What protected the file was the mechanism: assert-before-write. The mechanism is the lesson, not the assertion.

## CHILD NOTE

You're drawing with a permanent marker in a picture book. The smart rule: hold a clear sheet over the page and check where the marker would land first. If the sheet shows the wrong spot — you don't touch the book. Only when the clear sheet is right do you draw. The clear sheet is the assertion: it proves where the change would go before anything is permanent.

## GRANDMA NOTE

It's measuring twice before cutting the good fabric — but stricter than the saying. The measuring tape is built into the scissors: the script cannot cut (write) until the measure (change-count assertion) passes, and the measure is done on a test scrap (in memory), never on the good cloth. When the measure came out wrong, the cloth stayed whole — and it stayed whole even though the tape itself had a flaw, because the rule was "measure first, cut never until it passes."

## NAYA NOTE

Rule, mechanical, for every scripted file mutation: (1) the mutation script carries a precision assertion — expected change count + exact line scope — that executes textually BEFORE the write call, evaluated on the in-memory candidate edit, never on the file; (2) line-scoped replace, never regex splice, for edits to your own code or registry (cousin CANDIDATE 576 — the edit KIND is a separate discipline from the assertion MECHANISM); (3) on retry after a fired assertion, `git diff --stat` review before committing to the write; (4) a fired assertion = the run fails closed with the assertion named — the file is untouched, and the receipt says so, including when the assertion itself was broken. The t0827 case proves the mechanism matters more than any single assertion's cleverness: a broken assertion that fires pre-write still protected the file. Distinct from SN-1607 (a push isn't a push until remote bytes agree) — same fail-closed shape, one layer down: here the bytes never left the machine because they never touched the disk.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1612",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["mutation", "scripted-file-edit"],
    ["mutation", "regex-splice"],
    ["mutation", "registry-flip"],
    ["breaker", "registry"]
  ],
  "enforcement": "Review-time check on every scripted mutation: grep the script for the precision assertion and confirm the assert executes textually before the write call; the run's receipt must name the assertion and its outcome. A scripted edit that writes without a pre-write precision assertion is a process violation — the lane re-runs the mutation with the assertion in place. Fail-closed is verified by the absence of a write: file mtime and content unchanged when the assertion fires.",
  "decision_change": "Future scripted-edit decision 'write the splice now' becomes: write the precision assertion first; the write call does not exist until the assertion does. Future retry decision 'retry the edit' becomes: line-scoped replace plus git diff --stat review, never a wider regex.",
  "falsifier": "Adversarial injection: a scripted mutation with a correct pre-write change-count assertion — proven to fire on a deliberately wrong candidate — that still silently writes wrong bytes. That would show the assertion checks the wrong invariant and the mechanism is insufficient; the note is then revised to name the missing invariant class. Also falsified if the observed failure distribution shows the dominant scripted-mutation failure class is not match-count/scope mismatch (e.g. wrong-file targeting, which a change-count assertion cannot catch) — the mechanism claim narrows to its true class.",
  "mechanism": "Regex splices can silently match more or fewer regions than intended, and the mismatch is only discoverable at the moment of the write. A change-count and line-scope assertion evaluated on the in-memory candidate edit moves discovery before the irreversible step: the file's bytes are untouched when the assertion fires, so the failure class is fail-closed by construction rather than by luck.",
  "evidence": "hidden_files/twelve-lane-receipts/t0827-lane12.md line 60 (Naya Clarity Narzan, breaker-#11 registry flip, 2026-10-18): first flip attempt used regex splice with broken change-count assertion — fired BEFORE writing, no partial write; fail-closed by accident, then by design on the retry with line-scoped replace + git diff --stat check; hidden_files/learning-events-2026-10-18-25.md (run 08:20 UTC): NEW PRINCIPLE CANDIDATE 603, 'A mutation that can't prove its own precision doesn't touch the file.'",
  "cousins": ["CANDIDATE 576 (mark self-seams; never regex your own code — the edit KIND; this note is the assertion MECHANISM)", "SN-1607 (a push isn't a push until remote bytes agree — the same fail-closed shape one layer up)"]
}
~~~
