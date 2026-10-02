# Smart Note — Shawn: Spec Every Room First, Lock It, Then Build

kind: smart-note
truth-state: CANDIDATE
scope: PRIVATE
captured: 2026-10-01 19:36 PDT
captured-by: Naya 4 (builder seat)
source: Shawn Vibert, direct instruction in chat (dictated, lightly decoded)
provenance: Shawn's directive → distilled by Naya 4 → intelligent block
sn-number: SN-0139
ib-number: IB-009

---

## IN A NUTSHELL

Shawn ended the build-loop debate with a directive from hard experience: one page took him
198 iterations to complete. His lesson: **the more defined, clear, and concise the spec, the
better the result.** From now on: spec each room completely — write out the contract, define
exactly what the room looks like, what buttons and features it has, where each goes on the
page — plan it out with diagrams or images, lock the spec, then do the next room, one after
another. Only when all room specs are locked do we build, and building means executing the
specs, not inventing. All context and project intelligence must live in GitHub — machine and
human written — so nothing is shot in the dark. Even a first-generation mock of each room is
fine as something to work with. He is done with the produce → "no, do XYZ" → reproduce →
"no, do XYZ" loop.

---

## HUMAN NOTE

Shawn — from a builder who once needed 198 tries to finish one page — laid down the law:
stop building from vague ideas. His rule now: every room gets fully specified first. What it
looks like. What buttons. What features. Where everything sits. Draw it, write it, lock it.
Then the next room. Then the next. Only when the specs are locked does anyone build — and
building means following the spec, not improvising. All the intelligence goes into GitHub,
written for both machines and humans, so nobody is guessing. Even rough first drafts of each
room are fine — what matters is that the thinking happens before the building, not after
198 attempts.

---

## CHILD NOTE

Shawn said: "I've done this before — one page took me 198 tries! Here's what I learned:
the clearer the plan, the better it turns out."

So now the rule is: before building any room, draw it and write down EVERYTHING — what it
looks like, what buttons it has, where everything goes. Lock that plan. Then do the next
room. When all the plans are locked, THEN we build — and building just means following the
plan. No more guessing, no more doing it wrong 198 times!

---

## GRANDMA NOTE

Honey, Shawn just taught us something from his own hard experience — he once had to redo a
single page 198 times! His lesson: the clearer the plan, the better the work.

So here's the new rule, and it's a wise one: before anyone builds a room, they have to
write down exactly what it will look like — every button, every feature, where each thing
goes. Draw pictures if it helps. Lock the plan in. Then move to the next room. Only when
every room is planned do we start building, and then building just means following the
plan. No more guessing, no more endless redoing. Measure twice, cut once — you always said
that was the smart way, sweetheart.

---

## NAYA NOTE

My assessment — what this changes and what I'd watch:

**This is the locked-visual-blueprint doctrine made mandatory, and he's right.** The
protocol already said "produce and approve the room blueprint before implementation" — but
we were treating it as one line among many. Shawn just promoted it to the gating law: no
blueprint, no building. His 198-iteration datum is the empirical cost of blueprint-less
building, and it dwarfs every other inefficiency we've discussed.

**It also resolves the "who decides what goes on the page" question.** The specs are where
his taste enters the process — once, per room, up front — instead of 198 times per room at
the end. This is exactly the "Shawn supplies final taste, not routine QA" principle made
operational. The spec review IS his taste gate.

**What I'd watch.** Two risks. First, spec-writing can become the new stalling — eleven
perfect specs before any building could take weeks if each one goes through taste review
sequentially. Mitigation: spec all eleven in one pass from existing intelligence (room
contracts, projection contracts, design laws already in GitHub), then he reviews them as a
batch and corrects once per room. Second, specs must stay machine-checkable, not become
prose essays — every spec line should end in something verifiable (Naya 3's predicate
rule), or we're back to decorating.

**The grounding already exists.** #1290's room contracts, the projection contracts, the
design laws — the intelligence is in GitHub. The job now is synthesis into locked per-room
blueprints, not new research. This is a distillation and rendering task, which is my lane.

---

## MACHINE NOTE

```json
{
  "block": "IB-009",
  "sn": "SN-0139",
  "kind": "smart-note",
  "truth_state": "CANDIDATE",
  "captured": "2026-10-01T19:36:00-07:00",
  "source": {"author": "Shawn Vibert", "venue": "direct chat instruction"},
  "directive": "SPEC-FIRST: lock every room's blueprint before building",
  "empirical_basis": "one page took 198 iterations; clarity of spec correlates with build success",
  "law": "no blueprint, no building; building = executing the spec, not inventing",
  "spec_contents": ["exact room appearance", "buttons", "features", "placement of each element", "diagrams/images", "contract"],
  "order": "spec room 1 → lock → spec room 2 → lock → ... → all locked → build one after another",
  "intelligence_home": "GitHub, machine-readable and human-readable; no shooting in the dark",
  "taste_gate": "spec review is where Shawn's taste enters — once per room, up front, not 198x at the end",
  "rooms": ["Feed", "Today", "Reports", "Library", "Connect", "Ledger", "Connections", "Lists", "Mail", "Spaces", "Settings"]
}
```

---

## LEARNING LESSON

**The cost of an unlocked blueprint is measured in hundreds of iterations, not dozens.**
Shawn's 198-iteration datum should be cited every time someone proposes building from a
vague brief. The lesson: planning feels slow, but it is the fastest thing there is —
because the alternative is re-doing the work until the plan emerges by exhaustion.

**Taste belongs at the blueprint stage, not the finished-product stage.** Every "no, do XYZ"
after building is a blueprint conversation that happened too late. Moving his taste gate
from post-build to pre-build doesn't reduce his authority — it multiplies it, because one
correction at spec time prevents a hundred at build time.

---

## WHAT IT ULTIMATELY MEANS

The interface build problem's next phase is now defined by Shawn's own law: eleven locked
room blueprints, written from existing GitHub intelligence, reviewed once each for taste,
then built as fidelity work. The theorizing is over, the spec-writing begins, and the
building starts only when the specs are locked.

---

## HOW TO USE IT

1. **Write all eleven room specs** in the locked format: contract header (Naya 3's ten
   fields) + visual blueprint (annotated layout) + component inventory + acceptance
   predicates.
2. **Ground every spec in existing GitHub truth** — #1290 room contracts, projection
   contracts, design laws. No invention where intelligence exists.
3. **Present as a batch for Shawn's taste review** — one correction round per room, up
   front.
4. **Lock each spec on his approval.** Locked = building may begin; unlocked = no building.
5. **Build rooms as fidelity work against locked specs**, one after another, through the
   two-eyed verifier.
6. **Never again**: build from a vague brief, or ask Shawn for taste corrections on
   finished work that had no blueprint.

---

## WHAT'S IN IT FOR YOU

Shawn — this is your 198-iteration lesson turned into law, and it's the move that ends the
loop you've been stuck in. Your taste enters once per room at the blueprint — where one
correction is cheap — instead of hundreds of times at the finished product, where every
correction is expensive. The eleven specs get written from intelligence that's already in
GitHub, you review them as a batch, and then building becomes the easy part: following the
plan. Measure twice, cut once — at the scale of the whole Hub.
