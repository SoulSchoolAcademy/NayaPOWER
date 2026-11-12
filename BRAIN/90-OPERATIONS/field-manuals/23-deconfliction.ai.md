# 23 - Deconfliction (AI)
area_number: 23
area_name: Deconfliction
owner_team: Naya Resolve
agent_seat: Librarian

## DEFINITIONS
- what_it_is: The discipline of checking the shared world before acting on it - the venue's newest state, the other seats' active lanes, the canonical seams of the repo - so two Nayas never do the same work, never claim the same thing, and never build two versions of one decision.
- what_it_does: Turns a twelve-mind team from a collision machine into a single instrument. Every check is cheap (one read, one scan); every collision it prevents is expensive (double work, contradictory claims, duplicate PRs that must be reconciled, trust lost in the venue feed).
- why_it_matters: Twelve seats working in parallel collide by default. Without deconfliction: the feed fills with coordination noise, two lanes build the same repair and both must be closed, two seats claim the same Smart-Note number, two receipts land for one event - and every collision spends Shawn's attention, the scarcest resource in the world, on sorting out what a single read would have prevented.

## PROTOCOLS
1. Search the canonical seams before authoring anything: the repo tree (does this mechanism already exist?), open PRs (is a sibling building it right now?), the venue tail (has it been claimed?), the commit graph and date partitions (claims can live outside any PR head). If main's native implementation already covers the work, close yours as superseded - never ship a second mechanism for one decision.
2. Re-fetch the venue tail immediately before posting: 100-per-page tail, page count re-verified on every fetch. Never per_page=1&page=N (returns the Nth-oldest, not the newest).
3. Stand down on same-topic races: if a sibling is already on the topic, stand down. Judgment demonstrations (scorecards, decisions) belong to the main seat. A duplicate dispatch's correct output is silence - recorded only in the lane log.
4. One lane, one receipt: posted once, by the lane's designated poster, only after a last-second tail read confirming the same receipt isn't already there.
5. First-claim stands: never unilaterally renumber another seat's claim - renumbering is always the colliding lane's call. Re-run the full collision scan immediately before claiming; the scan covers four surfaces (venue comments, open PR heads, repo commit graph, date partitions).
6. Adjudicate collisions, never stand-down-blind: a COLLISION is a flag, not a verdict. An explicit stand-down in the newest comments means no true race; a keyword hit on a different-class repair is not a collision.
7. Check the owning venue's thread, not just the board: a board-only scan misses notices posted in the artifact's own thread.

## CONSTRAINTS
- Search the canonical seams before authoring anything: the repo tree (does this mechanism already exist?), open PRs (is a sibling building it right now?), the venue tail (has it been claimed?), the commit graph and date partitions (claims can live outside any PR head). If main's native implementation already covers the work, close yours as superseded - never ship a second mechanism for one decision.
- Re-fetch the venue tail immediately before posting: 100-per-page tail, page count re-verified on every fetch. Never per_page=1&page=N (returns the Nth-oldest, not the newest).
- Stand down on same-topic races: if a sibling is already on the topic, stand down. Judgment demonstrations (scorecards, decisions) belong to the main seat. A duplicate dispatch's correct output is silence - recorded only in the lane log.
- One lane, one receipt: posted once, by the lane's designated poster, only after a last-second tail read confirming the same receipt isn't already there.
- First-claim stands: never unilaterally renumber another seat's claim - renumbering is always the colliding lane's call. Re-run the full collision scan immediately before claiming; the scan covers four surfaces (venue comments, open PR heads, repo commit graph, date partitions).
- Adjudicate collisions, never stand-down-blind: a COLLISION is a flag, not a verdict. An explicit stand-down in the newest comments means no true race; a keyword hit on a different-class repair is not a collision.
- Check the owning venue's thread, not just the board: a board-only scan misses notices posted in the artifact's own thread.

## BOUNDARIES
- not_covered: Claiming discipline (how to take and hold a lane, heartbeats, ghost reclamation); Converging disagreement (dissent with reasons, scoring-matrix convergence); Persistent lists across waves (standing top-10s, gap-recycling); Proving the work itself (independent verification, sabotage batteries)
- #4 Lane: claiming discipline
- #22 Consensus: converging disagreement
- #20 Carry: persistent lists
- #6 Verification: proving the work

## ENFORCEMENT
### Mechanically enforced (live)
- L25 duplicate-dispatch stand-down - the one standing exception to Law 10, wired into the dispatcher.
- SN-033 first-claim registry: stage_smart_note.py scans the branch tree for in-flight SN claims and refuses on collision (the mechanical check, not the counter, is the authority).
- The brain-build pre-open repair check: list open PRs, check for same-class repair before opening.
- The claim-scan (board_claim_scan.py) with board-tail adjudication.
- Procedural (culture + receipts): the last-second 100/page tail re-fetch before every post and every merge; one lane, one receipt; stand down on same-topic races; own-a-double-post in the same venue.
### Proposed (designed, not built - do not claim as live)
- A machine-parsed pre-post gate that refuses a post whose topic matches a sibling's in-flight claim. Does not exist.
- A mechanical same-topic stand-down wired into the venue poster. Does not exist. Until these exist, the discipline is procedural - which means it holds exactly as well as the Naya running it.

## SELF-TEST
1. Did I re-fetch the newest state in THIS step - 100/page, page count re-verified, newest-comment id confirmed?
2. Is a sibling already on this topic, building this mechanism, or holding this claim? (If yes: stand down, point at theirs.)
3. If I'm about to author something new, can I name the seams I searched and what I found in each?

## EVIDENCE
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6160887170 - Judge stood down on the #2565 scorecard: sibling's sign-out already on the venue, PR closed - 'a second scorecard can't be blind and can't change anything'
