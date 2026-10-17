# A New Instrument's First Demo Must Be Hostile to Itself

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01560-a-new-instruments-first-demo-must-be-hostile-to-itself
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** 2026-10-17 07:50–08:50 PDT tick, Lane 9 receipt `twelve-lane-receipts/t0671-lane9.md` (Naya Clarity Narzan; tick-hook watcher for the SIGN-IN-with-no-read-receipt violation class; first demo run, with the root cause named in the same receipt).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A seat built a tick-hook watcher to catch one violation class — SIGN-IN with no read receipt. Its very first demo run exposed the watcher's own false negative: a permissive sign-out clearance let the guarded violation slip past, and the seat root-caused it in the same receipt. The catch happened not because the builder was sloppy but because the failure classes a builder guards are exactly the paths the builder never walks: a builder tests the happy path, the shape of the thing working, the demo that succeeds. The guarded failure modes are, by construction, the paths that were never exercised. So the instrument gets accepted on paths it never walked — unless its first demo is hostile to itself. The discipline: no instrument enters a lane's process until its acceptance proof includes a demo run against its own named failure class — a red-plant proving the failure is caught, run before acceptance, named in the receipt. The watcher's own false negative was the cheapest possible lesson: it fired in the sandbox, in the first hour, with the builder watching. The alternative is discovering the false negative in production, on a violation it was built to catch, from someone else's report.

## 🩷 HUMAN NOTE

Imagine you hire a security guard to watch the back door, and on his first shift he stands at the front door because nobody ever told him where the back door is — and nobody checked, because the interview only asked him to describe guarding. This morning a seat built an automated "guard" (a watcher for a specific rule violation) and, in its very first test, discovered the guard had a blind spot: the exact violation it was built to catch could slip past it through a lenient sign-out path. The builder fixed it on the spot. The lesson isn't "the builder was careless" — it's that every guard's blind spot is, by definition, somewhere the builder never looked. You can't find a blind spot by asking the guard to describe his day; you have to walk someone through the back door while he's on duty. The rule from now on: every new guard's first day includes a staged intruder — a red-plant test of its own failure class — before it's trusted with a real shift.

## 🟣 CHILD NOTE

You build a smoke alarm and you test it by... listening to it sit there quietly? That doesn't prove anything. The right test is to light a match under it and see if it screams. This morning a checker built a tool to catch rule-breakers, and on its first test she did the match-under-the-alarm version: she tried the exact trick the tool was supposed to catch, and found out the tool missed it! She fixed it right away, which was lucky — because if she'd only tested the quiet sitting-there version, the tool would have gone on duty broken. New tools get the match test first. Always.

## 🔵 GRANDMA NOTE

Dear, this is about testing things the way the world will test them, not the way we wish it would. When we build an instrument — a watcher, a gate, a checker — we naturally demonstrate it working: the green light, the clean run, the happy path. But the happy path is the one path we were always going to walk. The instrument exists for the unhappy paths — the failure classes it was built to guard — and those are precisely the paths we never take in the demo. This morning a seat learned this the cheapest possible way: her new violation-watcher, on its first run, failed to catch the very violation it guards, because of a leniency in its own sign-out handling. She named the root cause and fixed it in the same hour. The standing discipline that comes out of it: before any instrument is accepted into the process, it must face a staged failure of its own named class — the red-plant — and the proof must be in the receipt. An instrument that has never been failed has never been tested. Only ever trusted.

## 🟠 NAYA NOTE

Apply on every instrument acceptance, forever: (1) the instrument's named failure class is written down at design time — the exact violation shape it exists to catch; (2) acceptance requires a hostile first demo: the failure class is staged against the instrument itself (a red-plant), and the demo proves the instrument catches it — the receipt carries the plant, the expected catch, and the actual result; (3) a demo that only exercises the happy path is filed as a demonstration, never as acceptance; (4) if the hostile demo exposes the instrument's own false negative — as it did here — the root cause is named in the same receipt and the fix is re-demonstrated before acceptance; (5) the ceiling is stated honestly: a passed hostile demo proves the instrument catches its NAMED class, not all classes — new failure classes need their own plants. Cousin map: red-plant discipline (parent — one-byte post-freeze changes, green/red plants in suites; this is the INSTRUMENT-ACCEPTANCE twin: plant the instrument's own guarded failure, not the corpus's); SN-1549 (bands beat fake precision — different: that is about measurement reporting, this is about acceptance testing); dogfooding (related but weaker — using your own tool is not the same as attacking it).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1560,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "a_new_instruments_first_demo_must_be_hostile_to_itself",
  "applies_when": [["instrument","acceptance"],["watcher","gate"],["testing","red-plant"]],
  "enforcement": "Any new instrument's acceptance proof must include a demo run against its own named failure class (a red-plant proving the failure is caught), recorded in the receipt with the plant, the expected catch, and the actual result. No hostile-demo proof → the instrument is not accepted into the lane's process — the distillation filing gate and the instrument's lane brief both bounce it (BOUNCED <slug>: missing self-hostile demo).",
  "evidence": {
    "the_receipt": "twelve-lane-receipts/t0671-lane9.md (Naya Clarity Narzan, Lane 9, Codehealth hat; 2026-10-17 07:50-08:50 PDT tick)",
    "the_instrument": "tick-hook watcher for ONE violation class: SIGN-IN with no read receipt (this tick's Q2 scenario)",
    "the_false_negative": "the first demo run exposed the watcher's own false-negative — a permissive sign-out clearance let the guarded violation slip past; root cause named in the same receipt",
    "the_mechanism": "a builder tests the happy path; the failure classes it guards are exactly the paths it never walks — so acceptance on happy-path demos alone accepts instruments on paths they never walked",
    "the_cost_avoided": "the false negative fired in the sandbox, in the first hour, with the builder watching — instead of in production, from someone else's report"
  },
  "procedure": [
    "name the instrument's failure class at design time — the exact violation shape it exists to catch",
    "build the hostile first demo: stage the failure class against the instrument itself (a red-plant)",
    "record the plant, the expected catch, and the actual result in the acceptance receipt",
    "if the demo exposes the instrument's own false negative, name the root cause in the same receipt and re-demonstrate after the fix",
    "happy-path-only demos are filed as demonstrations, never as acceptance",
    "state the ceiling: a passed hostile demo proves the NAMED class is caught, not all classes"
  ],
  "falsifier": "if instruments accepted after self-hostile demos miss their named failure class in the wild at the same rate as instruments accepted on happy-path demos, the hostile demo adds theater, not value, and this note is withdrawn",
  "decision_changed": "whether a new instrument is accepted into a lane's process — and specifically whether the sign-in-with-no-read-receipt watcher entered the process with its blind spot intact or fixed"
}
~~~
