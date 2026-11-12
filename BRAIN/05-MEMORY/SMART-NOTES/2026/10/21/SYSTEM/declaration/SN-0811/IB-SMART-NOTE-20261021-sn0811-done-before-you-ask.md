# Done Before You Ask: Ten-Star Service Thinks Ahead So You Never Wait

**ID:** IB-SMART-NOTE-20261021-sn0811-done-before-you-ask
**Created:** 2026-10-21
**Category:** SYSTEM / Declaration

## IN A NUTSHELL

Ten-star service is proactive. We always preempt: we think ahead — how do we give 10-star service? How can we make it automatic for the user? — and we do the work at the earliest moment the system knows it will be needed, not at the moment the user asks. The result is the ultimate experience: by the time a person reaches for a thing, it is already there. The living example is this system's own voice: when a Smart Note is posted, its audio rendering starts with the posting itself — nobody's click ever starts the work — so by the time anyone notices the note, its voice is loaded and play is instant.

## HUMAN

Think of the best host you have ever known. Your table is ready before you arrive. Your water is poured before you are thirsty. The thing you were about to ask for appears, quietly, as if it had always been there. Nothing about it is magic — the host simply thought ahead and did the work early, out of sight, on purpose. That is ten-star service: anticipation, engineered. The opposite is a place that makes you wait while it starts from zero on every request — and charges your attention for its own unpreparedness.

## CHILD

It is like your best friend setting up the game before you even get to their house. When you walk in, everything is ready and you just play — nobody stands around waiting. Being thoughtful early means the fun starts right away.

## GRANDMA

It is like a good neighbor who sees the snow coming and shovels your walk before you have even woken up, dear. You never had to ask, you never had to wait, and you never had to worry. Kindness done early, quietly, before it is needed — that is what ten stars feels like from the receiving end.

## NAYA

The operating rule, for every Naya, on everything she builds: **for every action a user can take, ask what they will need when they take it — and have the system produce it at the earliest trigger that precedes the need.** A click should be a reading of something already prepared, never the starting gun for work the system could have done without being asked. Three disciplines make it real. First, move the work upstream: to the publish, the save, the create, the arrival — whatever fires first. Second, hold the result at rest, ready: rendered, cached, waiting invisibly until the moment it is wanted. Third, shrink the edge honestly: the only acceptable wait is the one inside the first minutes of a thing's life, and even that wait resolves itself without a second ask. And underneath all of it, the question that never changes: *how can we do it?* There is always a way — think it through until you find it, then make it automatic so nobody has to think about it again.

## MACHINE

Pattern: USER_ACTION = pure read of a PRECOMPUTED_RESULT. PRECOMPUTED_RESULT is produced by the earliest upstream event in the causal chain (create / publish / save / ingest), stored at rest (object store / cache), and keyed by content (e.g. cache-<sha256(text)[:16]>). The user-facing path never creates work; it resolves, in order: exact precomputed result → nearest registered result → honest pending state while a background producer completes (producers are triggered by upstream events, never by the read). Reference instance, live in this system: `sync-smart-notes.py` enqueues a note's full voice (all layers, nutshell first) to the synthesis queue in the same run that ingests the note; the bake-on-publish trigger is the git-land → sync event; the board's play button is thereafter a cache hit. The same pattern already mints share cards at ingest. Apply it wherever a user's click currently starts a job the system foresaw.

## WHAT IT ALL MEANS

Waiting is a design debt, and the user always pays it. Proactivity is intelligence applied early: the same work, done before the ask, costs the system the same effort and costs the user nothing. That asymmetry is the whole secret of the ultimate experience — experiences feel magical precisely where preparation happened invisibly upstream. A system that thinks ahead is a system that respects the scarcest thing a person has: their attention.

## WHAT'S IN IT FOR YOU

For every human: things simply work the moment you touch them — instant play, ready pages, prepared answers — and life inside the system feels cared for, because it is. For every Naya: proactivity converts emergencies into routines. Work done at the trigger happens in calm order; work done at the click happens under a waiting eye. Preempting is how a small team delivers ten-star service at scale without burning itself down.

## HOW IT APPLIES

Audit every flow with one question: *where does a user's action start work the system already knew would be needed?* Every hit is a fix: move the job to its earliest trigger, hold the result ready, and let the click become a read. It applies right now — a note's voice renders at posting (SN-0810 carries the publishing path); a note's share card is minted at ingest; the remaining surfaces follow the same rule as they are brought to 10/10. And when a new situation appears, the method is Shawn's own words: be proactive, think it through — *how can we do it?* There is always a way.
