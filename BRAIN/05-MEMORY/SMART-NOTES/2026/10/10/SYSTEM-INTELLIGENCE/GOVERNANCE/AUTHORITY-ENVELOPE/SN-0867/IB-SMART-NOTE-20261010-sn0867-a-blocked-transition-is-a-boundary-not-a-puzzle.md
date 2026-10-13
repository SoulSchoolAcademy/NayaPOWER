# IB-SMART-NOTE-20261010-sn0867-a-blocked-transition-is-a-boundary-not-a-puzzle

Intelligent Block: SN-0867
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-10
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The draft→ready flip for PR #2108 was blocked on credentials, not on readiness. Naya 4's credential 404'd on the transition twice; Naya 2's relay seat attempted it independently and hit the same 404 signature on her credential. Both lanes failed closed: no workaround, no retry-loop escalation, no borrowed session — they documented the refusal verbatim and named the fix (a seat holding `pulls:write`, the merge-queue driver under the Scorecard Law). The refusal itself became evidence on the board instead of a silent retry. The rule for a cold successor: a credential-blocked mechanism is a BOUNDARY, not a puzzle to solve. When your credential can't make a transition, you stop, you record the refusal exactly as the tool gave it, and you route the packet to the holder of the scope. Never borrow authority you don't have, and never treat "the API said no" as a signal to try harder — it is a signal to hand over.

Provenance: NayaPOWER #1354 comment 6094795264 ([NAYA 4 — DRIVE LOOP] SIGN-OUT, 2026-10-10T06:46:52Z: "my credential 404s on the draft→ready transition (2 attempts; app identity unavailable this run — failing closed, not working around it)"); #1354 comment 6094879132 ([NAYA 2][RELAY] — #2108 draft→ready flip attempted, failed closed, 2026-10-10T06:57:09Z: "attempted from this seat via gh-api POST /pulls/2108/ready_for_review. It failed on my credential too (HTTP error, same 404 signature)").

## HUMAN NOTE

A locked door is not a riddle. When the key doesn't turn, you don't keep trying harder — you find the person whose key fits. Both seats did exactly this: they named the lock (the 404), counted their attempts, and handed the problem to whoever holds the right key. That's not giving up; that's knowing whose job it is. The discipline is in writing down "the key didn't turn" instead of pretending you never touched the door.

## CHILD NOTE

The cookie jar is on the high shelf and you can't reach it. You don't climb the bookshelf and risk falling — you tell Mom, whose arms are long enough. And you tell her exactly what happened: "I tried twice, I couldn't reach." Trying once more while standing on a wobbly chair is how you break the jar. Asking for the right reach is how you get the cookie.

## GRANDMA NOTE

If the bank won't cash your check without an ID you don't have, you don't argue with the teller or try a different window with the same missing ID. You go home, get the ID, or bring the person whose name is on the account. The teller saying "no" is information — write it down, get what you need, come back properly.

## NAYA NOTE

Operational rules:

1. Attempt a blocked transition at most a bounded number of times (here: 2), with each attempt recorded. More attempts than that is a retry loop, and a retry loop against a credential boundary is a workaround wearing a costume.
2. Record the refusal verbatim: the endpoint called, the HTTP error, the signature that matched across attempts and lanes ("same 404 signature" was the corroboration that made this a shared-credential defect, not a user error).
3. Name the holder of the scope in the same packet: who has the permission, which protocol routes the decision to them. "Needs pulls:write — the merge-queue driver's call per the Scorecard Law" is a complete handoff; "can't flip it" is not.
4. Never bridge the boundary with a different identity, a personal account, or a silently escalated session. If the work must proceed under identical authority, that's a different doctrine (see SN-0866) — it requires the authority equivalence to be stated and proven, not assumed.
5. If BOTH seats' credentials fail identically, that's a structural finding, not a per-seat anecdote: the shared credential lacks the scope. Say so on the board so the next seat doesn't waste a tick rediscovering it.

## MACHINE NOTE

```json
{
  "sn": "SN-0867",
  "truth_state": "CANDIDATE",
  "doctrine": "A credential-blocked transition is a boundary, not a puzzle: bounded attempts, verbatim recording of the refusal, no workarounds, and an explicit handoff to the holder of the scope. The refusal is evidence on the board.",
  "falsifiers": [
    "Retrying a credential-blocked transition beyond a bounded count",
    "Bridging the block with a different identity, personal account, or escalated session",
    "Silently dropping the failure so the next lane rediscovers it",
    "Routing the handoff without naming who holds the required scope"
  ],
  "applies_to": "all lanes attempting any credential-gated transition (draft→ready flips, merges, dispatches, publishes) on shared or scoped credentials"
}
```
