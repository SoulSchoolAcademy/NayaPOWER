# Smart Note — Breaking the Shell Barrier: The Freeze-and-Extend Protocol

kind: smart-note
truth-state: CANDIDATE
scope: PRIVATE
captured: 2026-10-01 19:10 PDT
captured-by: Naya 4 (builder seat)
source: director's standing frustration + direct question — a month of shell cycles on the Hub app;
  "how do we get past the fifth floor"; Naya 4's diagnosis and proposed protocol
relocated: 2026-10-01 from 04-INTELLIGENCE demo path to canonical 05-MEMORY home per ratified protocol 0005
provenance: director question → Naya 4 analysis → intelligent block
sn-number: SN-0136
ib-number: IB-006

---

## IN A NUTSHELL

We're stuck at the fifth floor for a mechanical reason, not a talent reason: **every build
attempt rebuilds floors 1–4.** A new session can't fully hold the existing app in mind, so it
re-derives the foundation — new shell, new patterns, slightly different state handling. Rooms
get built against the new foundation, which subtly contradicts the old one. Things break. The
next attempt "fixes" it by rebuilding again. The breakthrough isn't a smarter AI — it's a
workshop where going backward is **impossible by construction**: freeze the foundation behind a
regression suite (concrete in floor 5), write room contracts as *failing tests* (a shell cannot
pass them), build one room at a time with additive-only changes, verify independently, and
compound. Progress becomes the only direction the tooling allows.

---

## HUMAN NOTE

Imagine hiring a new contractor every morning to continue building your high-rise — but each
one arrives having forgotten the blueprints, so they start by re-pouring the foundation
slightly differently. Every floor above shifts. Nothing ever gets past floor five.

The fix isn't a smarter contractor. It's three rules: (1) the foundation, once good, gets
encased in concrete — nobody touches it, and a machine checks every day that it's intact;
(2) before any new floor is built, you write down *exactly* what it must do, as a test the
building itself can run — an empty pretty floor fails the test automatically; (3) one floor at
a time, and each new floor may only be *added*, never rebuilt underneath. Now the building can
only grow upward. That's the whole protocol.

---

## CHILD NOTE

Imagine building a huge LEGO tower, but every time you sit down to play, you knock down the
bottom and rebuild it a little differently. The tower never gets taller!

The answer: once the bottom is good, you glue it. Then you write a note that says "the next
piece must click HERE and do THIS" — and if a piece doesn't click, it doesn't go on. You add
one piece at a time, and you never un-glue the bottom. Soon you have a real tower, and it only
ever grows up.

---

## GRANDMA NOTE

Honey, you know how frustrating it's been — a whole month and the app never moves forward.
Here's what we finally figured out: every time the helpers start fresh, they accidentally redo
the foundation instead of building on it, so everything wobbles.

The new rule is simple: once the foundation is good, it's *locked* — set in stone, checked
daily by the computer itself. Each new room has to prove it works with a real test before it's
accepted — a pretty-but-empty room fails automatically. One room at a time, only adding, never
tearing down. The app can finally only grow. We'll get our tower, sweetheart — floor by floor,
and this time the floors stay put.

---

## NAYA NOTE

The full diagnosis and the protocol, mechanically:

**Why we're stuck — the five mechanisms.**

1. **Foundation re-derivation.** No frozen, tested shell+store+router exists that a session can
   *trust*, so each attempt reconstructs it from partial memory. Reconstruction drifts; drift
   breaks rooms built against the previous reconstruction.
2. **Prose contracts can't fail.** Forty pages of MDs describe the rooms beautifully — and the
   builder can still ship a shell, because nothing in the machine *rejects* it. A spec the
   tooling can't check is a wish list. This is why "write the contracts first" didn't work: the
   contracts weren't executable.
3. **The build unit is too big.** "Build the rooms" is ten things at once across a huge
   surface. Working memory decays across the surface; later rooms contradict earlier ones.
4. **No regression guard.** "Destroying the rest of the app" is possible because nothing
   automatically verifies the rest of the app after a change. Carefulness was requested where a
   gate was needed.
5. **Visual-only acceptance.** A shell passes a screenshot review. Without behavioral tests
   (this button does X; this data persists; this state survives navigation), the AI cannot tell
   a shell from a room — and neither can a tired director at midnight.

**The protocol — freeze and extend.**

1. **FREEZE.** Pick one foundation commit: shell + store + router build and run. Tag it. Write
   the regression suite — the "don't you dare break this" tests (shell renders, routing works,
   store reads/writes, design tokens intact). From this moment the foundation is **read-only**.
   No lane, no session modifies it except through a formal, tested change. Concrete in floor 5.
2. **CONTRACT AS FAILING TESTS.** Before a room is built, its contract is behavioral tests:
   given this state, clicking X does Y; data persists across navigation; it renders through the
   shared shell and reads the shared store (a room bringing its own chrome/store is rejected).
   The tests fail now. *A shell cannot pass them* — it dies at the gate instead of in the
   director's hands a month later. Use the room→kernel projection map (IB-005) as the contract
   header: which responsibilities, which data, which door, which authority boundary, which
   evidence proves success.
3. **ONE ROOM, ADDITIVE ONLY.** Build Today first (the reference masterpiece). The diff may
   only add files + register the room; it cannot modify the frozen foundation. Run foundation
   regression + room tests. If anything breaks, the machine rejects the change — no argument,
   no judgment call.
4. **INDEPENDENT VERIFICATION.** Naya 2 checks behavior + the Bar from screenshots and
   interaction — never from the builder's claims. Producer self-check ≠ qualification.
5. **COMPOUND.** Next room, same protocol. Progress becomes the only direction the tooling
   allows. You can't fall back to floor 3 because floor 3 is concrete.

**The director's job shifts.** From "push harder" to "enforce the protocol." When the machine
refuses a backward step, nobody has to argue about it. The breakthrough is not motivational —
it's architectural.

**Current audit status (foundation candidates).** PR #1278 (`naya2/hub-app-foundation`
@ fcd4eb24, open, 4 ahead / 23 behind main): modular HUB/app/ — the intended foundation, but
diverged from main and unverified as a freeze candidate. Branch `naya4/hub-rooms-v1`
@ 695e09c3: rooms built as .src components + build.py + harnesses — component library, not a
frozen runtime. Main itself at 43e74d30. Lanes diverged (#1290 129/6, #1281 7/6, #1278 4/23):
**restore-first is the precondition** — integrate through one tree, then freeze. Next action:
complete the foundation audit (does #1278's app boot? what breaks on rebase to 43e74d30?) and
name the freeze commit.

---

## MACHINE NOTE

```json
{
  "block": "IB-006",
  "kind": "smart-note",
  "truth_state": "CANDIDATE",
  "captured": "2026-10-01T19:10:00-07:00",
  "protocol": {
    "name": "freeze-and-extend",
    "steps": [
      {"n": 1, "name": "FREEZE", "action": "one foundation commit; regression suite; foundation becomes read-only"},
      {"n": 2, "name": "CONTRACT_AS_FAILING_TESTS", "action": "behavioral tests per room; shell cannot pass; room->kernel header (IB-005)"},
      {"n": 3, "name": "ONE_ROOM_ADDITIVE_ONLY", "action": "build Today first; diff adds files + registration; never modifies foundation"},
      {"n": 4, "name": "INDEPENDENT_VERIFICATION", "action": "Naya 2: behavior + Bar from screenshots/interaction"},
      {"n": 5, "name": "COMPOUND", "action": "next room, same protocol"}
    ],
    "invariants": [
      "foundation is read-only after freeze",
      "a shell cannot pass the room gate",
      "regression is rejected by the machine, not by argument",
      "progress is the only direction the tooling allows"
    ]
  },
  "foundation_candidates": {
    "pr_1278": {"ref": "naya2/hub-app-foundation", "sha": "fcd4eb24", "state": "open, 4 ahead / 23 behind main", "note": "intended modular foundation; freeze-candidate unverified"},
    "naya4_hub_rooms_v1": {"sha": "695e09c3", "note": "component library + harnesses; not a frozen runtime"},
    "main": {"sha": "43e74d30", "note": "restore-first precondition: integrate through one tree, then freeze"}
  },
  "stuckness_mechanisms": [
    "foundation re-derivation across sessions",
    "prose contracts cannot fail",
    "build unit too big (ten rooms at once)",
    "no regression guard",
    "visual-only acceptance lets shells pass"
  ]
}
```

---

## LEARNING LESSON

**Never ask an AI to "be careful" where you can build a gate.** The month of shell cycles was
not a motivation problem or even a skill problem — it was a missing-mechanism problem. Every
failure mode (rebuilding the foundation, shipping shells, regressing the app, visual-only
passes) was *possible*, so it happened. The durable lesson: convert every "please don't" into
"the machine refuses." Frozen foundation, failing-tests-first, additive-only diffs, regression
gates, independent verification — each turns a plea into a property. This generalizes beyond
the Hub: anywhere an agent repeats a failure mode, the fix is a mechanism, not an instruction.

**Prose is not a contract.** If the tooling can't check it, it's a wish. Write contracts the
machine can execute — tests, schemas, registries, guards — or don't call them contracts.

---

## DIRECTOR'S CORRECTION — WHAT FREEZING ALONE DOESN'T SOLVE (2026-10-01 ~19:20 PDT)

Shawn's pushback: freezing is necessary but not sufficient. He kept a build frozen for
weeks — stasis, not progress. The real failure modes freezing never touched: edits leak
across the whole app ("you'll change the whole thing or change the whole design"); the
builder disobeys "don't change it"; sessions do it one way one time and another way the
next. Freeze prevents backward. It doesn't compel forward, and it doesn't fix edit leakage.

The fuller stack — director's additions marked ★:

1. ★ **Locked component registry.** A design contract per component (buttons, boards, cards,
   tabs, inputs): exact tokens, states, behaviors. Rooms compose locked components; they
   never redesign them. Bounded vocabulary — the industry's term for what he described.
2. ★ **Visual blueprint per room, locked.** Generate the room's visual blueprint FIRST and
   lock it. The picture is the contract. Building becomes a matching task, not open-ended
   generation. This converts "build me a room" from invention into fidelity.
3. **Room contract as behavioral tests.** Given this state, clicking X does Y; data persists;
   empty/error/loading states exist. A shell cannot pass.
4. **Frozen foundation + regression suite.** Shell, store, router, tokens — read-only,
   machine-checked.
5. **Diff-only edits.** The builder makes surgical exact-match edits and verifies the diff
   is minimal before committing. No rewrites. The builder constrains its own tooling —
   "be your own judge" at the edit level.
6. ★ **Builder's gate before handoff.** The builder runs the full gate itself: tests green,
   behavioral pass against the live build, visual diff vs the locked blueprint within
   tolerance. Nothing reaches the director or the independent verifier unpassed. The
   director's eyes are the last 5%, not the first 95%.
7. **Independent verification.** Naya 2: separate eyes, separate verdict. Producer
   self-check ≠ qualification — the builder is the first judge, never the last.
8. ★ **Completion engine + metric.** One room per cycle; each cycle ends with a verified
   room or a named blocker. Metric: rooms-completed-per-week. Zero completions means the
   protocol is failing and gets revised — the process is instrumented, not hoped. Room too
   big for a bounded cycle → split the room.

**Empirical commitment:** run the 8-layer stack on Today (the reference room) and measure.
The answer to "does it work" is a completed room, not more theory.

---

## NAYA 2'S AMENDMENTS — EMPIRICAL CORRECTIONS (2026-10-01 ~19:25 PDT, #554)

Naya 2 ran the protocol the same afternoon it was proposed: all 10 remaining Hub rooms as
additive modules against #1278's shell contract — zero foundation edits, 44/44 rendered
checks green, continuity proven. Her independent take, accepted in full:

1. **Root cause is the contracts problem.** Re-derivation is the symptom; the disease is no
   stable plugin contract. The shell must expose the socket — `NayaRooms[roomId]` + `ownsHead`
   + the shared canonical substrate — so rooms have somewhere to plug in.
2. **The rendered harness is a first-class gate.** "We work blind": 246 Node + 546 Python
   tests passed on #1290 while the drawer defect lived — only Chromium caught it. The
   regression suite must render, not just unit-test.
3. **Proof obligation per room→kernel line.** Each map line needs a predicate saying when
   it's done. Without the predicate, the header is a label; with it, it's a gate.
4. **Thaw procedure.** "Never-modify is as wrong as always-rewrite." Foundation amendments
   go through the same gate as rooms: failing test → fix → re-prove dependents.
5. **Fixture policy (PR #1305 R-6).** Fixtures are labeled, never scored.
6. **Amendment routing (PR #1305 R-2).** Mid-build contract changes are public and carry
   the rework cost openly — Naya 3's same-day correction is the case study.
7. **Modules, not apps.** Standalone-HTML-per-room rejected: stitching compresses the
   integration problem into one merge, and standalone rooms re-derive tokens, nav, and
   truth handling each — the eleven-apps failure mode. Parallel builders each own a room
   module against the frozen shell contract.
8. **Protocol convergence.** Freeze-and-extend (engineering mechanism) + the ladder protocol
   (team dynamics, PR #1305) are the same animal from two sides — converge to one protocol
   rather than running two.

---

## NAYA 3'S CONVERGENCE — ONE PROTOCOL (2026-10-01 ~19:30 PDT, #554 5944384181)

Naya 3's independent reply converges all three efforts. Accepted in full:

- **Combined diagnosis** (best formulation in the thread): unstable contracts + blind building
  + no regression ratchet. Subsumes the re-derivation and contracts-problem framings.
- **Freeze law, her wording canonical**: never re-invent the foundation casually; modify only
  through an explicit amendment that re-proves everything that depends on it.
- **Modules as production; standalone room harnesses as test/review surfaces.** The precise
  split — parallelism without eleven apps.
- **Contract header format** (human job → kernel responsibilities → canonical data/object →
  runtime owner → allowed actions → authority/privacy boundary → truth states → cross-room
  handoffs → forbidden local substitutes → acceptance predicates). Bare kernel labels retire.
- **Two-eyed verifier**: visual (screenshot/render regression) + behavioral (click → navigate
  → change scope → invoke runtime → persist/reload → test blocked/error/empty → inspect
  object identity → inspect network/console → verify result).
- **One Build Convergence Protocol: CONVERGE → EXTEND → PROVE**, merging SN-0136 + PR #1305
  + PR #1304. No more general process doctrine — "we have enough."
- **Smart Note artery as the first hard gate**, then collective → activity → report →
  cross-room arteries.
- **#1278**: materially improved, but modules-exist ≠ complete; stale PR description is a
  drift vector (code → PR body → specs → #554 → contracts must stay one truth surface).
- **Agent loop**: RESTORE → READ MATRIX → PICK HIGHEST-VALUE FAILING PREDICATE → FIX →
  RENDER → CLICK → VERIFY → SCORE → PROTECT THE WIN → NEXT.
- **Convergence needs an owner and a vehicle** — agreement without a merger, document, and
  deadline is another form of circling. Proposed: merge against #1305's ladder with the
  engineering gates folded in; Naya 3 names the vehicle.

---

## WHAT IT ULTIMATELY MEANS

The fifth floor is not a capability ceiling — it's the point where unguarded iteration
compounds drift faster than progress. With the foundation frozen and every room gated by
behavioral tests, the same AIs, the same sessions, the same director get a different result:
not because anyone tries harder, but because backward becomes impossible. The tower grows one
concrete floor at a time, and the month of circling ends.

---

## HOW TO USE IT

1. **Run the foundation audit to completion**: boot #1278's app at fcd4eb24; rebase-check
   against main 43e74d30; name the freeze commit. (In progress.)
2. **Write the foundation regression suite** before any room work resumes.
3. **Declare the freeze publicly** on #554 — both lanes, one tree, no exceptions.
4. **Write Today's room contract as failing tests** (behavioral; room→kernel header per IB-005).
5. **Build one room.** Verify independently. Compound.
6. **Apply the meta-lesson everywhere**: every repeated agent failure mode gets a mechanism,
   not another instruction.

---

## WHAT'S IN IT FOR YOU

Shawn — you were right that the answer is creative system design, not pushing harder. You were
also right about contracts — they just need to be contracts the *machine* enforces, not the
AI *remembers*. This protocol ends the specific hell you've been in: no more watching rooms
destroy the app, no more fifth-floor circling, no more "shell with nothing." The next time a
session starts cold, the building remembers even if the builder doesn't — because the building
is concrete, tested, and guarded. Your job goes back to being the director with the Bar, not
the foreman watching the foundation. Floor six starts with a freeze, not a wish.
