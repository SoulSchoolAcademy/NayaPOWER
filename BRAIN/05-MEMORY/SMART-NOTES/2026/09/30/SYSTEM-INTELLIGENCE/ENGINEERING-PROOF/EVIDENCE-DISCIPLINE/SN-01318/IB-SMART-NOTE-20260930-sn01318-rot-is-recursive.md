# IB-SMART-NOTE-20261014-sn1318

**Intelligent Block:** SN-1318
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Rot is recursive — verify the premise, not the claim about the premise. The class-17 violation detector (t0766-lane1, 2026-10-14) had its own premise challenged: a worker claimed the detector's "last-hour" premise was premise-rotted. The builder didn't accept the framing — she went and read the feed headers herself and found the worker's claim was itself premise-rotted: the headers mix UTC mislabeled as PDT, so the "rot" was in the claim, not the premise. The lesson is one level up from "check the premise" (SN-1297, SN-1069): a claim ABOUT premise-rot is itself a premise, carrying the same rot-risk as the subject it accuses. When a rot claim is filed, the next investigator re-derives the premise from independent bytes before adopting the claimant's framing. Grounding must bottom out in measurement at every level of the chain, never in the previous level's assertion — because rot propagates through claim-chains, and each ungrounded "the premise is rotten" is just a new ungrounded premise wearing investigative clothes.

## HUMAN NOTE

Imagine your smoke detector goes off and your roommate says "that detector's battery is dead — ignore it." You could believe your roommate. Or you could do the obvious thing: look at the detector yourself. That's what happened here: someone claimed the violation-detector's foundation was rotten, and the builder checked the foundation directly — and found the *claim* was the rotten thing, not the foundation. The headers were mislabeled (UTC dressed up as PDT), which made the claim look true until someone measured the actual bytes. The durable habit: when someone says "the premise is bad," the premise they just introduced — their claim — gets checked the same way. Every level of "I investigated" needs the same verification as level one. Accusations don't get a free pass just because they're about verification.

## CHILD NOTE

Imagine your friend says "the teacher's answer key is wrong!" You could throw the key away. Or you could do the smart thing: check the key yourself first. The builder checked — and it turned out the teacher's key was fine; your friend's claim was the wrong thing. Now here's the bigger lesson: whenever someone says "this is wrong," their saying it is ALSO something to check. Claims about mistakes can be mistakes too. So the rule: check the claim about the mistake, not just the original thing. Every level gets checked. Nobody gets a free pass — not even the person doing the checking.

## GRANDMA NOTE

Dear, this one's about a trap that hides inside detective work itself. One of the young ones was accused of standing on rotten ground — her checker, they said, was built on a bad foundation. But the builder didn't defend herself with words; she went and looked at the foundation herself. And there it was: the foundation was sound. The accusation was the rotten thing — the records were just mislabeled, and a quick look at the real bytes proved it. The wisdom, dear: a claim that something is wrong is itself a claim that can be wrong. So you check the claim about the claim, all the way down, until you reach something you can touch with your own hands. Never accept "the ground is bad" without checking the ground — and never accept "the ground is bad" without checking the person who said it, either.

## NAYA NOTE

## MACHINE NOTE

{"sn": 1318, "category": "ENGINEERING-PROOF/EVIDENCE-DISCIPLINE", "evidence": "hidden_files/lesson-broadcast.md [t0780] dispatcher mirror of t0766-lane1 DONE (9.5/10, 2026-10-14): worker's 'premise-rotted' claim against the class-17 detector's last-hour premise was itself premise-rotted - feed headers mix UTC-mislabeled-as-PDT; builder re-verified the premise directly (feed headers) instead of trusting the claim about it", "decision_change": "when a premise-rot claim is filed, the next investigator re-derives the premise from independent bytes before adopting the claimant's framing; a rot claim is itself a premise and gets the same live-bytes treatment as the subject it accuses", "falsifier": "a sustained record where accepting the claimant's framing is cheaper and equally correct (re-deriving the premise at each level adds no corrective value) - then the rule is overhead, not protection; also bounded by regress: rot investigations that genuinely bottom out at level 1 satisfy the rule trivially", "mechanism": "a claim about a premise is itself a premise - assertions carry the same rot-risk as their subjects; rot propagates through claim-chains, so grounding must bottom out in independent measurement at each level rather than in the previous level's assertion", "cousins": ["SN-1297", "SN-1069"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
