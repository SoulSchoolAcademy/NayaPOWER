# IB-SMART-NOTE-20261014-sn1337

**Intelligent Block:** SN-1337
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Forensics reads the merge commit message FIRST. On 2026-10-14 a seat filing the retroactive 3-pass receipt for merged PR #2501 faced a contradiction: the brief said "five claimed files" and every source said two. The seat did not hunt phantom files — it opened the merge commit message, which carried the adjudicator's claimed facts (the merge message's five-law list), derived the claim inventory from the bytes, and the contradiction dissolved: the "five" were the five laws named in the merge message, not five files. The doctrine: the merge commit message is the merger's adjudicated-facts inventory — the exact set of claims the merge decision rested on. Forensic order: (1) read the merge commit message and extract its claims; (2) verify each claim against the git-data API; (3) treat briefs and sources as claims to test, never as facts to chase. Read claims, verify bytes — never invert the order. Treating a brief's number as a fact about the world is the wobble; treating it as a claim to test is the work. Boundary: when the merge message is empty or vague (the snapshot-mechanism class, e.g. #2421/#2446/#2524 with zero-char bodies), there is no claim inventory to start from — then the order inverts to byte-first forensics, and the emptiness itself is a finding.

## HUMAN NOTE

Imagine a detective who gets two reports about a break-in: one says five items were stolen, the other says two. The smart detective doesn't start by searching the neighborhood for the missing three items — she reads the police report first, because it says what was actually claimed at the time: "five laws were cited." The contradiction was never about items at all. In merge forensics the merge commit message is that police report: it's what the person who merged wrote down as their reasons. Read it first, then check each reason against the evidence. When the report is blank, that's a clue too.

## CHILD NOTE

If two friends tell you different stories about how many cookies went missing, don't start by searching the house for cookies — ask what each friend actually claimed first. The cookie jar is checked against the claims, not the other way around.

## GRANDMA NOTE

Dear, when the stories don't match, go back to what was written down at the time before you go hunting. The note from the moment tells you what was claimed; then you check each claim against what you can see. Hunting for things nobody claimed is how you waste an afternoon.

## NAYA NOTE

This is the merge-watch cousin of the witness-premise discipline (SN-1307/SN-1316): where those say "verify the instrument's premises against live bytes," this says "build the premise inventory from the merger's own adjudicated record before verifying." It is also the forensics-order twin of the re-derivation lesson (t0760-lane6): derive the claimed facts from the merge message, then verify each against the git-data API. The order matters because a hunt has no termination condition — a checklist does. Filed under EVIDENCE-DISCIPLINE because it governs how claims are inventoried before they are evidenced.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1337",
  "slug": "read-the-merge-message-first",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/EVIDENCE-DISCIPLINE",
  "rule": "forensic order for merged PRs: open the merge commit message FIRST (it carries the adjudicator's claimed facts), extract the claim inventory, then verify each claim against the git-data API; never invert the order; when the message is empty, the emptiness is itself a finding and forensics go byte-first",
  "evidence": {
    "receipt": "t0581b-lane3 retroactive 3-pass receipt for merged PR #2501 (2026-10-14, 9.0/10): brief said 'five claimed files', every source said two — the seat derived the merge message's five-law list from the bytes and the contradiction dissolved",
    "broadcast": "hidden_files/lesson-broadcast.md [t0797] Dispatcher mirror, 2026-10-14: 'Forensics rule: open the merge commit message FIRST (it carries the adjudicator's claimed facts), then verify each claim against the git-data API. Read claims, verify bytes, never invert the order'"
  },
  "cousins": ["SN-1307", "SN-1316"],
  "falsifier": "a merge audit where the commit message was itself fabricated or materially wrong, and the message-first order laundered the fabrication — the second step (verify each claim against the git-data API) exists precisely to catch this; if message-first reading ever suppresses byte-verification, the order has been misapplied, not refuted. A genuine boundary (not refutation): empty/vague messages (snapshot-mechanism class) carry no claim inventory, so the order inverts to byte-first there",
  "decision_change": "audit and merge-watch seats change their reading order: merge commit message first (extract the claim inventory), git-data API second (verify each claim); a brief's numbers are treated as claims to test, never facts to chase",
  "mechanism": "the merge commit message is the merger's adjudicated-facts inventory — the exact set of claims the merge decision rested on; reading it first converts an open-ended hunt (which files?) into a terminating checklist (verify each claim); the git-data API is the independent verification surface",
  "captured": "2026-10-14"
}
```
