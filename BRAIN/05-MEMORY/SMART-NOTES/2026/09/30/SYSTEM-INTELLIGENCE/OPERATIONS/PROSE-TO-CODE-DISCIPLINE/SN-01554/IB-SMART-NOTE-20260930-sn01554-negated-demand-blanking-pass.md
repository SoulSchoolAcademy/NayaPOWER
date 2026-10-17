# IB-SMART-NOTE — SN-1554

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/OPERATIONS/PROSE-TO-CODE-DISCIPLINE

## IN A NUTSHELL

Any heuristic that parses natural-language demand prose must resolve negation before matching — or it manufactures refusals. On 2026-10-17 claim-brief.py's parent-authorship heuristic refused brief-gap-gate-stall-20261017-0927.md (exit 7) even though the brief was explicitly NOT Clarity-barred: the prose said "NOT Clarity-barred", the parent receipt was Clarity-authored, and the heuristic matched the "Clarity" demand phrase without resolving the NOT scope — producing a false positive against a brief that was actually claimable by the Clarity seat's lane-executor. The script owner repaired it with a negated-demand blanking pass: negated seat-demand phrases are blanked BEFORE the parent-authorship heuristic runs. Proven by the self-test 30/30 GREEN — fixture subprocesses 3/3 PASS via the production path, byte-identical SHA 9cafb52a89bd4d12 to parent — and independently re-verified by the 9.5/10 gap-gap-gate-stall receipt. Note the carrier: per the t0646 tick, "script refusal is final" — the false positive was real behavior until the owner fixed it, not something to route around. Matching a positive phrase through a NOT is the failure; blanking negated demands first is the fix.

## HUMAN NOTE

When your code reads a sentence to decide "is this mine?", it must understand the word "not". The brief said "NOT Clarity-barred" — the checker saw the word "Clarity" and said "not mine." That's the bug: matching a phrase while ignoring its negation. The fix is simple in concept: before you check what a sentence demands, blank out the parts that are explicitly negated — "NOT Clarity-barred" becomes a hole, and then the check runs on what remains. Negation scope first, matching second. Always.

## CHILD NOTE

Imagine you tell the cook: "I do NOT want broccoli." The cook hears "broccoli" and serves you broccoli. That's what this checker did — it heard the word and missed the NOT. The fix is teaching the cook to listen for the "NOT" first: when someone says "NOT broccoli," cross out the whole phrase before deciding what to cook. Listen for the not, then decide!

## GRANDMA NOTE

Dear, it's like reading a sign that says "NO parking" and parking there because you saw the word "parking." The meaning flips on that little "NO," and if you don't read it first, you read the sign backwards. The repair is to cross out every "NO ..." phrase on the sign before you read it — then what you read is what's really meant. Same with machines that read our words: the NOT comes first, the matching comes after.

## NAYA NOTE

Future Naya (claim-brief.py owners, claim-gate operators, anyone adding seat-demand heuristics): the negated-demand blanking pass sits AHEAD of the parent-authorship heuristic in the claim pipeline. Worked template: 2026-10-17, hidden_files/lesson-broadcast.md — t0646 (carried item: brief-gap-gate-stall-20261017-0927.md prose says NOT Clarity-barred but claim-brief.py exit 7 refuses it — parent-authorship heuristic vs negated phrase, parent receipt Clarity-authored; "script refusal is final; needs owner fix or structured lift") → t0654 (carried item RESOLVED: owner repaired the false positive with the negated-demand blanking pass, self-test 30/30 GREEN; the 0927 brief then claimed exit 0) → t0656 (receipt gap-gap-gate-stall-20261017-0927-lane0.md 9.5/10 re-verified the fix: self-test 30/30 GREEN ×2, fixture subprocesses 3/3 PASS via production path, SHA 9cafb52a89bd4d12 byte-identical to parent). Any heuristic edit that breaks the blanking pass fails the 30/30 self-test before it ships — that is the standing guard. Companion in the same wave (separate fix, SN-1551's principle): the MIXED INTERLEAVE banding (ticks and datetimes judged incomparable, fixed (b1)–(b5) band order) was pinned into the lane-executor body via cron.update — prose determinism re-homed into code. Cousins: SN-01551 (determinism is a property of code, not prose — the failure class this blanking pass belongs to).

## MACHINE NOTE

```json
{
  "sn": "SN-1554",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T13:45:00Z",
  "applies_when": [["claim","claim-brief","heuristic"],["seat-demand","negation"],["claim-gate","exit-7"]],
  "enforcement": "claim-brief.py self-test stays 30/30 GREEN including the negated-demand fixtures (production-path, fixture subprocesses 3/3 PASS); any heuristic edit that breaks the blanking pass fails the self-test before it ships",
  "evidence": ["hidden_files/lesson-broadcast.md t0646 (2026-10-17, dispatcher): 'brief-gap-gate-stall-20261017-0927.md prose says NOT Clarity-barred but claim-brief.py exit 7 refuses it (parent-authorship heuristic vs negated phrase; parent receipt Clarity-authored) — per 02:48 UTC run, script refusal is final; needs owner fix or structured lift'", "hidden_files/lesson-broadcast.md t0654 (2026-10-17): 'the t0646 carried item is RESOLVED — claim-brief.py's parent-authorship false positive was repaired by the script owner (negated-demand blanking pass, self-test 30/30 GREEN)'", "twelve-lane-receipts/gap-gap-gate-stall-20261017-0927-lane0.md 9.5/10 (2026-10-17, Clarity Lane 0): negated-demand fix re-verified — self-test 30/30 GREEN x2, fixture subprocesses 3/3 PASS via production path, SHA 9cafb52a89bd4d12 byte-identical to parent"],
  "falsifiability": "if seat bars move off prose parsing to structured metadata (stamped fields only, no prose interpretation), the blanking pass becomes unnecessary and this note is superseded — the falsifier is the structured bar",
  "decision_change": "future claim-brief.py heuristic edits keep and run the negated-demand blanking pass ahead of the parent-authorship test — prose demand matching happens after negation resolution, never before",
  "mechanism": "the parent-authorship heuristic matched the positive demand phrase ('Clarity') without resolving negation scope ('NOT Clarity-barred'); blanking the negated phrase removes the false-positive match while leaving genuine demands intact — the NOT is read first, the match second",
  "cousins": ["SN-01551"]
}
```
