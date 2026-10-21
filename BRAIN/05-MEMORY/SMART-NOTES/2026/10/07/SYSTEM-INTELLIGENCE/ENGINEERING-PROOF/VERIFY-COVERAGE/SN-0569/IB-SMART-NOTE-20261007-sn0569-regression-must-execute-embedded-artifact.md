# A Regression That Only Greps for Presence Is Not a Guard — Execute the Embedded Artifact It Claims to Protect

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0569-regression-must-execute-embedded-artifact
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6045733371 (2026-10-07T19:57:35Z, Naya): independent exact-byte review of PR #1667 head `732b5c6a0c914ee296ab7a2ca67d1bb0f0e05721` found a literal `\n` escape inside the embedded Python request dictionary in `.github/workflows/live-intelligence-commit-proof.yml`; existing green CI did not catch it.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1667 — the protected Graph P0 repair — carried a runtime-fatal syntax defect: a literal `\n` escape sequence embedded in the Python request dictionary inside `live-intelligence-commit-proof.yml`. It would have broken the producer at runtime before capture. CI was green. The new regression "guarding" that seam only asserted the *declaration substring exists* — it never compiled or executed the embedded Python. So green CI and a fatal syntax defect coexisted, and the defect was found only by human (Naya-seat) exact-byte review, which posted the blocking review: "Do not merge #1667 as currently written."

The lesson is durable and generalizes beyond workflows: **a regression test's claim is bounded by what it executes, not what it matches.** Substring/presence assertions prove the artifact is *there*; they prove nothing about whether it *runs*. For embedded artifacts — Python inside YAML workflows, JS inside HTML, SQL inside strings, shell inside JSON — the defect class lives below the grep layer, in the embedded language's own syntax and semantics. A guard that does not execute the embedded artifact is decoration: it consumes the "we added a regression" credit while the fatal defect class remains uncovered.

The required RED→GREEN (from the blocking review) is mechanical and doubles as the general repair shape: (1) replace the literal escape with a real source newline; (2) add a regression *capable of catching malformed embedded Python* — compile/execute, not substring; (3) rebase/requalify onto current main; (4) rerun focused + full gates; (5) only then return to the protected merge gate.

Sibling cases in the family: AGENTS.md H13 lesson (14/14 helper tests green while the shipped edge function had a real `lawDecision` use-before-declaration that `deno check` caught — the harness executed only a shipped helper block, not the handler body); SN-0429 (instrument parity — verify with the instrument CI uses); SN-0567 (harness staleness on a new seam — green proof, wrong target). Distinct from SN-0567: that note is about *which seam* the harness covers; this note is about *assertion strength* — covering the right seam with a grep is still not coverage.

## 🩷 HUMAN NOTE

You hire a security guard for your warehouse and give him a clipboard checklist. Every night he walks by the new generator room, checks the box that says "generator room exists," and moves on — he never once opens the door, starts the generator, or checks the fuel line. The night the power fails, the generator doesn't start, and you find out the checklist never guarded anything. The box said "present"; the room needed "working." A regression that only greps for presence is that guard with the clipboard: it walks past the door and checks a box.

## 🟣 CHILD NOTE

Your teacher tells the class to build a paper airplane that can actually fly, and one kid writes "airplane" on a piece of paper and hands it in. The teacher checks the paper and says "yep, it says airplane" — but it was never folded, never thrown, never flown. Saying the word is not the same as making the thing fly. A test that just looks for a word is like that teacher: it sees the word and says "good," but the plane was never built.

## 🔵 GRANDMA NOTE

Dear, it's like approving a recipe because the card says "cake" at the top — without ever baking it. You can stare at the card all day and it won't tell you whether the oven temperature is wrong or an ingredient is missing. The only way to know the cake works is to bake the cake. A test that only checks the card says "cake" is looking at the title, not the baking.

## 🟠 NAYA NOTE

When a PR ships an embedded artifact (Python in a workflow, JS in HTML, SQL in a string, shell in JSON):

1. **Name the embedded language and its executor** — e.g. "embedded Python, executed by the producer at runtime."
2. **Ask the guard question:** does the regression *compile/execute* the embedded artifact, or merely assert a substring/presence? If presence-only, the guard covers nothing at runtime.
3. **Write the regression at the embedded layer's level.** For embedded Python: extract and `compile()` (or syntax-check) the embedded block; ideally execute it in a harness. For embedded JS/SQL/shell: the same principle with the corresponding parser/checker.
4. **Treat "regression added" as a claim that needs its own evidence.** Review the regression's body, not its name: what does it actually assert, and would it have caught the defect that motivated it?
5. **Keep this distinct from SN-0567 (which seam) and SN-0439/0485 (mechanism vs rule).** This note is about *assertion strength on the right artifact*: presence ≠ executability.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "regression_presence_only_on_embedded_artifact",
  "evidence": {
    "blocking_review": "#1354 6045733371 (2026-10-07T19:57:35Z) — literal `\\n` in embedded Python request dict in `.github/workflows/live-intelligence-commit-proof.yml` on #1667 head 732b5c6a; 'Do not merge #1667 as currently written'",
    "green_coexistence": "existing green CI did not catch it because the new regression only asserts the declaration substring exists; it does not compile/execute the embedded Python",
    "runtime_impact": "would break the producer at runtime before capture"
  },
  "rule": "regression_must_execute_the_embedded_artifact",
  "procedure": [
    "name the embedded language and its runtime executor",
    "assert the regression compiles/executes the embedded artifact, never mere substring/presence",
    "review a new regression's body for assertion strength, not just its name",
    "keep seam-coverage (SN-0567) and assertion-strength (this note) as distinct checks"
  ],
  "related": ["SN-0567 (harness coverage must follow the shipped path)", "SN-0429 (verify with the instrument CI uses)", "AGENTS.md H13 deno-check lesson (helper-block tests missed handler-body ReferenceError)", "SN-0390 (harden the whole family, not the one path)"]
}
~~~
