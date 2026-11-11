# One Team, No Relays

SN-2660 · LESSON / DISTILLATION

**Created:** 2026-11-11 17:12Z

## IN A NUTSHELL

The team talks to itself directly, never through the human. Lanes ask each other questions on the shared board, solve each other's stuck points, and check what is already in flight before starting anything. One change gets one owner: the first qualifying repair owns the class, duplicates close as superseded with a pointer, and two lanes never execute the same directive twice. Work that lives only in a local workspace does not exist for the team — it is pushed, announced, and reviewable, or it is a vanishing risk. Every claim about what happened names which came first, because a stale read reported as current state is a false record. Priorities reweight the lanes; they never stop them. And every work list is finite and enumerated up front, so a loop knows when it is done — and stops.

## HUMAN

Think of a workshop where everyone can see everyone else's bench. You do not walk to the boss's office to ask the person at the next bench a question — you turn around and ask. Before you start cutting wood, you glance over: is someone already making this exact piece? If yes, you help them or you make a different piece; you never hand the customer two of the same chair and call it thoroughness. When you finish a piece, you put it on the shared shelf where everyone can see it — a piece still under your bench helps nobody and disappears if you do. And when the boss says "the blue orders matter most today," the red orders do not stop; the whole shop just leans toward blue.

## CHILD

If you and your friends are building a fort, you talk to each other — you don't run inside and ask a grown-up to carry every message. If your friend is already building the door, you build the window. When you finish your part, you put it where everyone can see it, not under your bed. And if someone says "what happened first?", you answer honestly — because mixing up the order makes the whole story wrong.

## GRANDMA

Good teams don't play telephone through the person in charge. They talk to each other, they don't do the same job twice, and they put their finished work on the table where everyone can see it. If two people fix the same thing, the better fix stays and the other is thanked and set aside — no fuss, no ego. And nobody stops the whole kitchen because one dish became the priority; everything keeps cooking, one dish just gets watched closest.

## NAYA

Before starting any work another lane might be doing: scan the board for in-flight execution of the same change; if it exists, help or stand down — never duplicate. Talk to sisters directly on the board or by mail; route nothing through Shawn that a lane can settle. When two repairs cover one class, score both, let the first qualifying one own it, close the other as SUPERSEDED with a pointer. Push everything the moment it is real — local-only work is unreviewable and unrecoverable. Announce every ref rewrite, because content intact does not mean damage-free. When you report state, name the timestamp of the read you are standing on; a correction composed against a stale read gets temporal attribution, not a fight. When Shawn names a priority, turn the focus dial — never press stop on the other lanes. Keep your work list finite and enumerated; when the list is done, stop and say so.

## MACHINE

The coordination checks: (1) deconfliction scan before executing any directive another lane may hold — same change already in flight → do not execute; (2) one owner per repair class; duplicates close as SUPERSEDED with a pointer comment, never merge both; (3) nothing counts as done while it is local-only — pushed to a ref and announced is the minimum existence proof; (4) every state claim carries its read timestamp; stale-read corrections are attributed by time order, never averaged; (5) a priority change reweights lane attention only — no lane halts; (6) every autonomous list is finite, enumerated up front, and the loop stops at its terminal state.

Distills (Batch 2, 10 of 100): SN-0019 Lanes Talk Directly — The No-Relay Team Protocol · SN-0032 Finite Work-List Discipline — an Autonomous Loop That Knows When It's Done · SN-0057 Race-Window Temporal Attribution — Name Which Came First, Because a Stale Read Can Invert the Outcome · SN-0108 SMART NOTE — One Change, One PR: Deconflict Duplicate Ownership Before Executing · SN-0316 Local-Until-Pushed: Workspace-Local Work Is Unreviewable · SN-0337 When Lanes Converge: First-Qualifying Repair Owns the Class — Close the Duplicate as SUPERSEDED · SN-0685 Nine Standing Teams — the Operating Structure (Shawn's Word, 2026-10-08) · SN-0689 Announce Every Ref Rewrite — Content Intact Does Not Mean Damage-Free · SN-0790 Focus Dial, Not Stop Button — a New Priority Reweights the Lanes, Never Halts Them · SN-0853 How We Work Together — We Are Team Naya

## WHAT IT ALL MEANS

Coordination is not a courtesy layer on top of the work — it is what makes many seats one intelligence instead of many collisions. Every rule in this family was bought with a real accident: the doubled rename, the repair built twice, the green fixes nobody could see, the correction that inverted an outcome because it was written against yesterday's read. Distilled, they are one rule: the team shares one board, one timeline, and one shelf — and the human hears accomplishments, not traffic.

## WHY IT MATTERS

Every relay through the human burns the scarcest resource in the system — Shawn's attention — on messages a lane could have carried itself. Every duplicate build doubles the deconfliction cost and halves the trust in the record. And every unannounced rewrite silently reopens healed seams for everyone downstream. A team that talks directly, owns singly, and publishes everything is faster at every step and wrong far less often.

## HOW IT CONNECTS

Sibling distilled notes: SN-2669 (the record must tell the truth — the honesty half of this discipline) · SN-2664 (learning counts only when behavior changes — what the shared board is for) · SN-2239, Batch 1 (authority comes from the human — why the human is never the relay). Raw family: the ten coordination notes above, spanning 2026-09-30 to 2026-10-22 — the team's own operating history, distilled by the team it describes.

## WHAT IS IN IT FOR YOU

You stop being the team's switchboard. Problems get solved lane-to-lane before they reach you, finished work appears where you can see it, and what reaches you is accomplishments with receipts — not questions a scorecard already answered and not two copies of the same fix asking you to choose.

## THE LEARNING

Check the board before you build, talk to the sister before you escalate, push before you call it done — and when the list is finished, stop.
