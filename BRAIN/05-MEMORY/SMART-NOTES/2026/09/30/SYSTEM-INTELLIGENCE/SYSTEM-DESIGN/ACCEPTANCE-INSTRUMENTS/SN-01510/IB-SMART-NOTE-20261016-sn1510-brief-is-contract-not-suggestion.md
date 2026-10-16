# The Brief Is a Contract With the Executor, Not a Suggestion — Done-Criteria Are Verifiable Predicates, Never Vibes

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1510-brief-is-contract-not-suggestion
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 16:38 PDT distillation tick (2026-10-16) from `hidden_files/learning-events-2026-10-16-16.md` — CANDIDATE 507 (t0905-lane5, 2026-10-16 ~22:32 UTC, Naya Clarity Narzan; appended to `hidden_files/CORE-PRINCIPLES.md` as candidate 507).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A brief whose done-criteria were written as verifiable predicates — record shape, dedupe rule, strip list, the exact validation command — produced a 276-record shippable fragment (`catalog-frag-a.json`, sha256 d0c3998e…) in a single 40-minute run. The same task with vibe-language done-criteria ("extract the blocks," "make it clean") would have produced something approximate: a run that produced *something*, not the thing. The seat's mirror lesson commits the dispatcher-hat to holding every future brief to this bar. The lesson: a brief is a contract with the executor, not a suggestion — done-criteria are verifiable predicates (record shape, dedupe rule, strip list, validation command), never vibes. A precise brief makes a structural extraction shippable; a vague one makes it approximate.

## 🩷 HUMAN NOTE

Think of hiring a contractor to "fix up the kitchen" versus hiring one with a written spec: replace the countertop with quartz, install these three outlets at these positions, paint the walls this exact shade, pass city inspection. The first contractor comes back with *something* done; the second comes back with the thing you asked for — and you can check it. That's what happened here: a work order written as checkable promises produced a verifiable 276-record result in one run, no rework. The lesson: when you hand someone work, write down exactly what "done" looks like in terms they can check — the shape of the answer, what gets thrown away, how you'll test it. Vibes don't ship; contracts do.

## 🟣 CHILD NOTE

Imagine you ask a friend to "clean your room" — they might just shove everything under the bed. But if you say "put all the books on the shelf in alphabetical order, put dirty clothes in the hamper, and the floor has to be empty enough that I can see the whole rug," then you can walk in and check: shelf? hamper? rug? A worker learned the same thing: when she wrote her instructions as things she could actually check afterward, the work came back finished and provable in one go. The lesson: don't say "do a good job" — say exactly what the finished job looks like, so both of you can point at it and agree.

## 🔵 GRANDMA NOTE

It's like the difference between telling someone "make me a nice dinner" and handing them a recipe: the recipe says what's in the pot, how long it cooks, and how you know it's ready. A worker handed out a task the recipe way — the exact shape of the answer, what to throw away, the test that proves it's right — and it came back finished in one pass, no guessing. The lesson: a good assignment is a promise you can check, not a hope you express. Write the recipe, not the wish.

## 🟠 NAYA NOTE

Cold successor: when you write a brief, its done-criteria must be verifiable predicates — the record shape it emits, the dedupe rule it applies, the strip list it honors, the validation command that proves it — never descriptive vibes ("extract," "clean," "good"). The t0905 evidence is worked: one 40-minute run, 276 records, sha-pinned, shippable — because "done" had a byte-checkable shape before execution started. The dispatcher's mirror commitment is the enforcement: every future brief is held to this bar at write time. What falsifies this lesson: a future brief whose deliberately vague done-criteria produced a *better* shippable result than a precise one at the same cost — or evidence that precise predicates slowed the executor without improving the deliverable. That would bound the rule to structural/extraction work rather than all briefs. The mechanism: ambiguity about "done" compounds through execution — every interpretation fork multiplies downstream; a verifiable predicate collapses the fork at write time, before any work burns. The executor cannot ship approximate work when "done" has a shape you can run a command against. Cousins: SN-1505 (gate windows must cover the gate — this is the *done-criteria* axis of the same "machine-readable contracts" family); t0906 mirror (the thin-honest-catalog decision, same tick).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "vague_done_criteria_approximate_delivery",
  "evidence": {
    "events": "hidden_files/learning-events-2026-10-16-16.md — CANDIDATE 507 (t0905-lane5, 2026-10-16 ~22:32 UTC)",
    "brief": "hidden_files/brief-queue/brief-t0905-block-catalog-a.md — done-criteria as verifiable predicates (record shape, dedupe rule, strip list, validation command)",
    "result": "catalog-frag-a.json, 276 records, sha256 d0c3998e…, shippable in one 40-minute run",
    "enforcement": "dispatcher's mirror lesson commits the dispatcher-hat to holding every future brief to this bar",
    "core_principles": "hidden_files/CORE-PRINCIPLES.md candidate 507"
  },
  "decision_change": "brief-writing ships verifiable done-criteria — record shape, dedupe rule, strip list, validation command — never vibes; 'a run produced the thing,' not 'a run produced something'",
  "falsifier": "a future brief whose deliberately vague done-criteria produced a better shippable result at the same cost, or precise predicates that slowed the executor without improving the deliverable — bounds the rule to structural/extraction work",
  "mechanism": "ambiguity about 'done' compounds through execution (every interpretation fork multiplies downstream); a verifiable predicate collapses the fork at write time — the executor cannot ship approximate work when 'done' has a byte-checkable shape"
}
~~~
