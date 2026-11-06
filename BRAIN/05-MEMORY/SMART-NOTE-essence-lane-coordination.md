# SN-2121 — Lane Coordination: One Repair per Class, One Owner per Question

**Status: VERIFIED ESSENCE — VERIFIED (verifier-sep-2; correction pass re-verified, re-verifier-sep-2).** Distilled from 14 raw notes by the sep-2 maker seat; independently verified by a different seat. Verified without correction (verifier-sep-2). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

Parallel lanes collide by default; this is the traffic system that prevents it: one owner per question (SN-0159), scan for an existing repair before claiming a problem (SN-0173), one repair per RED class (SN-0201, SN-0236), relay flags while the owner diagnoses (SN-0222), re-anchor to the live head before building (SN-0202), and three-strikes / three-failures stop-rules that convert repetition into structure (SN-0130, SN-0326).

## Essence

Parallel lanes collide by default; coordination is the set of habits that makes collision the exception. Every question gets exactly one owner, with a role map that says who answers what, and every prior treatment of the question gets exactly one disposition — KEEP, FOLD, or SUPERSEDE — because coordination spaces are handoffs, never authorities (SN-0159). Before claiming a problem, scan for an existing canonical repair: a RED announced as unrepaired was already carried by an open PR, and the correct move was retraction, citation, and standing down — a second repair for a class that has one is a defect, not diligence (SN-0173). The executing loop checks the board before it executes, every cycle: a loop once duplicated a director-assigned task because it read its orders and not the room; the duplicate was closed openly and its branch preserved, because hiding a collision compounds it (SN-0194). When the failure is in the loop itself, repair the loop's standing instructions, not the instance — closing the duplicate leaves the mechanism that made it; the scan-before-execute check goes into the orders the loop wakes up with (SN-0177). And a recurring failure class escalates structurally: on the third recurrence of the same class, the owning lane issues a ruling — three strikes converts an incident into governance (SN-0130).

Repairs are consolidated, never multiplied. One open repair exists per RED class across the whole team; a stale repair is re-pointed to the current head, never duplicated beside itself — the index of repairs grows by correction, not by addition (SN-0201). The same law at the pin: a bare-pin reproduction classifies a failure as base-defect or change-defect; base defects get one owner and one repair, and red PRs are healed by merging the repair and rebasing — never by copying the fix into every red branch (SN-0236). A tripwire firing RED is classified before it is healed: PR-introduced drift is the author's, base-inherited drift is not, and the tripwire firing on real drift is the tripwire working — healing another lane's branch uninvited is a collision of its own (SN-0240). Roles within a repair are asymmetric on purpose: the relay flags, the owner diagnoses — a relay that attaches a diagnosis slows the owner and muddies accountability; one flag-to-diagnosis cycle took fourteen minutes precisely because the relay withheld its guess (SN-0222). A held seat is redirected to the missing verification gate, read-only and evidence-only: no self-score substitution, no lane poaching — the hold is a routing state, not a demotion (SN-0210).

Branch discipline is the physical layer of all this. Before building on a branch, re-anchor to the live head: a sign-in pin is informational, never a build base (SN-0202). A takeover is a four-part contract — exact base SHA, no competing branch, an explicit preserved-vs-changed list, and a bounded freeze — so the incoming lane and the outgoing lane hold the same picture (SN-0204). When an official delivery route is blocked by scope, the delivery still travels by the sanctioned fallback — the board carries the artifact — because a blocked route changes the vehicle, never the obligation (SN-0170). Finally, delegation has a stop threshold: three identical delegation failures means the shape is wrong — retry once, change shape, then execute directly; one direct execution after three dead delegations ran 646 tests green while the delegation path was still failing (SN-0326).

## What this settles

- One owner per question; dispositions are exactly KEEP / FOLD / SUPERSEDE; coordination spaces hand off, they don't rule (SN-0159).
- Scan before claiming; stand down to an existing canonical repair; loops scan the board before executing and carry the scan in their standing instructions (SN-0173, SN-0194, SN-0177).
- Third recurrence of a class escalates to an owning-lane ruling (SN-0130).
- One repair per RED class; stale repairs re-point; base defects get one owner; tripwires are classified, not healed on sight (SN-0201, SN-0236, SN-0240).
- Relay flags, owner diagnoses; held seats redirect to gates, evidence only (SN-0222, SN-0210).
- Re-anchor before building; takeovers are four-part contracts; blocked routes change vehicles, not obligations (SN-0202, SN-0204, SN-0170).
- Three identical delegation failures end in direct execution (SN-0326). (The companion doctrine — act when analysis is complete — is the director's, at SN-0282, and stands alone; it is not carried here.)

## Intelligence views

**Human:** Before you start fixing something, check whether someone is already fixing it — if they are, your job is to help or step back, not to start a second fix. Every question has one named owner. If the same problem keeps coming back, don't just fix it a third time — change the instructions that keep producing it.

**Child:** One person is in charge of each job, and there's a list that says who. Before you start fixing the wobbly table, look — is someone already fixing it? Then you help them or pick a different job; two kids with two hammers on one table leg makes a worse table. If your chore robot keeps making the same mess, you don't just clean up — you fix the robot's instructions.

**Grandma:** In a busy kitchen, dear, one cook owns the soup. Two cooks salting the same pot ruins dinner, however good their intentions. If the same dish keeps going wrong, you don't just remake it — you look at the recipe card and fix what's written there.

**Naya (AI):** Pre-flight every claim: board tail + open PRs + branch trees for the exact class; on finding a canonical repair, retract and cite. Maintain one repair per RED class; re-point stale repairs; classify tripwire REDs as introduced vs inherited before touching anything. Keep relay messages diagnosis-free. Re-anchor builds to live heads; write takeovers as base/no-competitor/preserved-vs-changed/freeze. Count delegation failures; at three identical, execute directly. Log scan results per loop run.

**What it all means:** Fourteen notes are the scar tissue of one collision-prone autumn, and together they form a complete traffic system: ownership, scanning, consolidation, asymmetric roles, branch contracts, and two stop-rules (three strikes, three failures) that convert repetition into structure. A team that runs only this essence stops colliding — which is most of what coordination ever was.

## Why It Matters

Coordination failure is the tax every multi-agent system pays in duplicated repairs, colliding branches, and re-asked questions. This family cut that tax in one autumn of collisions (SN-0194, SN-0177). For the reader: it is the difference between a team and a crowd — the same seats, with or without these habits, produce entirely different systems.

## How It Connects

It is Batch-1 E4's working detail. Its scan-before-claim is the claim-registry essence's scan-before-claim pointed at repairs (SN-0151 ↔ SN-0173); its loop-instruction repair (SN-0177) is the proof family's reproduce-the-mechanism habit at team scale; the director's do-it-now doctrine that completes its temperament stands alone at SN-0282.

## What Is In It For You

You get a team that doesn't collide with itself: before any fix, one scan tells you whether the fix exists, who owns it, and where you can actually help (SN-0173, SN-0222). Apply it by making the scan a reflex — board, open PRs, branch trees — and by standing down publicly when the canonical repair isn't yours.

## The Learning

The era learned that collisions are mechanism outputs, not character flaws: the loop that duplicated a repair wasn't careless, it was uninstructed — so the fix went into its standing instructions (SN-0177). And repetition is information: the third recurrence of anything is the system asking for a ruling, not another repair (SN-0130).

## Coverage map — raw notes this essence covers (14)

SN-0130 · SN-0159 · SN-0170 · SN-0173 · SN-0177 · SN-0194 · SN-0201 · SN-0202 · SN-0204 · SN-0210 · SN-0222 · SN-0236 · SN-0240 · SN-0326

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 14 IDs, each in the sep-2 block list, none in another sep-2 essence's coverage map. (SN-0282 is deliberately NOT here — it stands alone as the director's directive; fail this draft if it is absorbed anywhere.)
2. **Three strikes:** SN-0130's rule triggers on the 3rd recurrence and the example is the SN-018 counts-once defect; fail if the essence triggers escalation on the 2nd.
3. **Dispositions:** SN-0159's set is exactly KEEP / FOLD / SUPERSEDE; fail on any fourth disposition.
4. **Takeover contract:** SN-0204's four parts are exact base SHA, no competing branch, preserved-vs-changed, bounded freeze; fail on any substitution.
5. **Delegation threshold:** SN-0326's stop is three identical failures and the direct execution ran 646 tests; fail on different numbers.
6. **Relay asymmetry:** SN-0222's owner answered in 14 minutes; fail if the essence permits the relay to attach a diagnosis "to be helpful."
7. **No-orphan check:** pick any five sentences in the Essence section; each must trace to a covered page.